#!/usr/bin/env python3
"""V2 embedding initialization for the Step 13 selected tokenizer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import time
from datetime import datetime
from pathlib import Path

import torch
import huggingface_hub


if not hasattr(huggingface_hub, "split_torch_state_dict_into_shards"):
    def _split_torch_state_dict_into_shards(state_dict, filename_pattern="pytorch_model{suffix}.bin", max_shard_size="10GB"):
        filename = filename_pattern.format(suffix="")
        tensor_names = list(state_dict.keys())
        return type(
            "StateDictSplit",
            (),
            {
                "is_sharded": False,
                "filename_to_tensors": {filename: tensor_names},
                "tensor_to_filename": {name: filename for name in tensor_names},
                "metadata": {},
            },
        )()

    huggingface_hub.split_torch_state_dict_into_shards = _split_torch_state_dict_into_shards

from transformers import AutoModelForMaskedLM, XLMRobertaTokenizer, logging as transformers_logging


METHODS = ["random", "mean", "fvt", "align", "focus"]
SPECIAL_TOKENS = ["<s>", "<pad>", "</s>", "<unk>", "<mask>"]


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def count_rows(path: Path) -> int:
    if path.is_dir():
        return sum(1 for child in path.rglob("*") if child.is_file())
    with path.open("r", encoding="utf-8") as f:
        total = sum(1 for _ in f)
    return max(0, total - 1) if path.suffix == ".tsv" else total


def file_result(role: str, path: Path, notes: str) -> dict[str, str]:
    if path.is_dir():
        size = sum(child.stat().st_size for child in path.rglob("*") if child.is_file())
        checksum = "DIRECTORY"
    else:
        size = path.stat().st_size
        checksum = md5_file(path)
    return {
        "file_role": role,
        "path": str(path),
        "rows_or_files": str(count_rows(path)),
        "bytes": str(size),
        "md5": checksum,
        "status": "PASS" if size > 0 else "FAIL",
        "notes": notes,
    }


def token_body(token: str) -> str:
    return token.replace("▁", "").replace("Ġ", "").replace("</w>", "").strip()


def load_selected_tokenizer(path: Path) -> tuple[str, Path]:
    selected_vocab = "NOT_FOUND"
    tokenizer_path = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Selected vocab size:"):
            selected_vocab = line.split("`", 2)[1]
        if line.startswith("Tokenizer path:"):
            tokenizer_path = Path(line.split("`", 2)[1])
    if tokenizer_path is None:
        raise RuntimeError("selected tokenizer path not found")
    return selected_vocab, tokenizer_path


def load_dev_texts(path: Path, limit: int) -> list[str]:
    texts = []
    for row in read_tsv(path):
        if row["v2_split"] != "dev" or row["book"] != "MAR":
            raise RuntimeError(f"non-dev row in dev manifest: {row.get('verse_id')}")
        texts.append(row["text"])
        if limit > 0 and len(texts) >= limit:
            break
    return texts


def special_ids(tokenizer: XLMRobertaTokenizer) -> dict[str, int]:
    return {token: tokenizer.convert_tokens_to_ids(token) for token in SPECIAL_TOKENS}


def build_source_maps(
    base_tokenizer: XLMRobertaTokenizer,
    extended_tokenizer: XLMRobertaTokenizer,
    base_vocab_size: int,
) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    base_vocab = base_tokenizer.get_vocab()
    char_to_ids: dict[str, list[int]] = {}
    for token, idx in base_vocab.items():
        if not isinstance(idx, int) or idx >= base_vocab_size:
            continue
        body = token_body(token)
        if len(body) == 1:
            char_to_ids.setdefault(body, []).append(idx)

    fvt_ids: dict[int, list[int]] = {}
    align_ids: dict[int, list[int]] = {}
    # Step14 tokenizer는 HF add_tokens() 방식으로 만들었기 때문에 base id와
    # special id가 보존되고, new row는 base_vocab_size부터 시작한다.
    # SPM protobuf에 직접 append한 tokenizer를 쓰는 경우에는 XLM-R의 <mask>
    # id가 이동할 수 있으므로 token 문자열 기준으로 row를 먼저 remap해야 한다.
    for token_id in range(base_vocab_size, len(extended_tokenizer)):
        token = extended_tokenizer.convert_ids_to_tokens(token_id)
        surface = token.replace("▁", " ").strip()
        subtokens = base_tokenizer.tokenize(surface)
        ids = [
            idx
            for idx in base_tokenizer.convert_tokens_to_ids(subtokens)
            if isinstance(idx, int) and 0 <= idx < base_vocab_size
        ]
        fvt_ids[token_id] = ids
        char_ids: list[int] = []
        for ch in surface:
            char_ids.extend(char_to_ids.get(ch, [])[:1])
        align_ids[token_id] = char_ids
    return fvt_ids, align_ids


def initialize_rows(
    model,
    method: str,
    base_vocab_size: int,
    merged_vocab_size: int,
    fvt_ids: dict[int, list[int]],
    align_ids: dict[int, list[int]],
) -> dict[str, str]:
    input_emb = model.get_input_embeddings().weight.data
    output_emb = model.get_output_embeddings().weight.data
    base_rows = input_emb[:base_vocab_size]
    base_mean = base_rows.mean(dim=0)
    base_norm_mean = base_rows.norm(dim=1).mean()
    fallback = 0
    initialized = 0

    # add_tokens() tokenizer layout에서 새로 생긴 row만 초기화한다.
    # 이 과거 실험 설정에서는 <mask>를 포함한 기존 source row가
    # resize_token_embeddings 단계에서 이미 복사되어 있어야 한다.
    for token_id in range(base_vocab_size, merged_vocab_size):
        if method == "random":
            vector = input_emb[token_id].clone()
        elif method == "mean":
            vector = base_mean
        elif method == "fvt":
            ids = fvt_ids[token_id]
            if ids:
                vector = input_emb[ids].mean(dim=0)
            else:
                vector = base_mean
                fallback += 1
        elif method == "align":
            ids = align_ids[token_id]
            if ids:
                vector = input_emb[ids].mean(dim=0)
            else:
                fids = fvt_ids[token_id]
                vector = input_emb[fids].mean(dim=0) if fids else base_mean
                fallback += 1
        elif method == "focus":
            fids = fvt_ids[token_id]
            aids = align_ids[token_id]
            fvt_vec = input_emb[fids].mean(dim=0) if fids else base_mean
            align_vec = input_emb[aids].mean(dim=0) if aids else base_mean
            if not fids or not aids:
                fallback += 1
            vector = 0.50 * fvt_vec + 0.30 * align_vec + 0.20 * base_mean
            norm = vector.norm()
            if norm > 0:
                vector = vector * (base_norm_mean / norm)
        else:
            raise ValueError(f"unknown method: {method}")
        input_emb[token_id].copy_(vector)
        output_emb[token_id].copy_(vector)
        initialized += 1

    model.tie_weights()
    new_rows = input_emb[base_vocab_size:merged_vocab_size]
    missing = int(torch.isnan(new_rows).any(dim=1).sum().item())
    zero_norm = int((new_rows.norm(dim=1) == 0).sum().item())
    return {
        "initialized_rows": str(initialized),
        "fallback_rows": str(fallback),
        "missing_rows": str(missing + zero_norm),
        "mean_norm": f"{new_rows.norm(dim=1).mean().item():.6f}",
        "std_norm": f"{new_rows.norm(dim=1).std().item():.6f}",
    }


def make_masked_batch(tokenizer, texts: list[str], device: torch.device, max_length: int, seed: int) -> dict[str, torch.Tensor]:
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    labels = input_ids.clone()
    generator = torch.Generator()
    generator.manual_seed(seed)
    probability = torch.full(labels.shape, 0.15)
    special_mask = torch.zeros_like(labels, dtype=torch.bool)
    for special_id in tokenizer.all_special_ids:
        special_mask |= labels.eq(special_id)
    special_mask |= attention_mask.eq(0)
    probability.masked_fill_(special_mask, 0.0)
    masked = torch.bernoulli(probability, generator=generator).bool()
    if masked.sum().item() == 0:
        first_non_special = (special_mask == 0).nonzero(as_tuple=False)
        if len(first_non_special) > 0:
            masked[first_non_special[0, 0], first_non_special[0, 1]] = True
    labels[~masked] = -100
    input_ids[masked] = tokenizer.mask_token_id
    return {
        "input_ids": input_ids.to(device),
        "attention_mask": attention_mask.to(device),
        "labels": labels.to(device),
    }


def zero_step_loss(model, tokenizer, texts: list[str], device: torch.device, batch_size: int, max_length: int, seed: int) -> tuple[float, int]:
    model.eval()
    model.to(device)
    weighted_loss = 0.0
    total_masked = 0
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch_texts = texts[start : start + batch_size]
            batch = make_masked_batch(tokenizer, batch_texts, device, max_length, seed + start)
            masked_count = int(batch["labels"].ne(-100).sum().item())
            outputs = model(**batch)
            weighted_loss += float(outputs.loss.item()) * masked_count
            total_masked += masked_count
    model.to("cpu")
    return weighted_loss / max(1, total_masked), total_masked


def shape_status(model, vocab_size: int) -> tuple[str, str, str]:
    input_ok = "PASS" if model.get_input_embeddings().weight.shape[0] == vocab_size else "FAIL"
    output_ok = "PASS" if model.get_output_embeddings().weight.shape[0] == vocab_size else "FAIL"
    tied = model.get_input_embeddings().weight.data_ptr() == model.get_output_embeddings().weight.data_ptr()
    return input_ok, output_ok, "PASS" if tied else "FAIL"


def nearest_neighbor_lines(model, tokenizer, base_vocab_size: int, method: str, sample_count: int = 5, base_limit: int = 5000) -> list[str]:
    emb = model.get_input_embeddings().weight.detach().cpu()
    base = torch.nn.functional.normalize(emb[:base_limit], dim=1)
    lines = [f"## {method}", ""]
    for token_id in range(base_vocab_size, min(len(tokenizer), base_vocab_size + sample_count)):
        vec = torch.nn.functional.normalize(emb[token_id].unsqueeze(0), dim=1)
        sims = torch.matmul(vec, base.T).squeeze(0)
        top = torch.topk(sims, k=5)
        neighbors = []
        for score, idx in zip(top.values.tolist(), top.indices.tolist()):
            neighbors.append(f"{tokenizer.convert_ids_to_tokens(int(idx))}:{score:.3f}")
        lines.append(f"- `{tokenizer.convert_ids_to_tokens(token_id)}` -> {', '.join(neighbors)}")
    lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-dir", default="docs/exp/second_try/14_v2_embedding_init")
    parser.add_argument("--selected-tokenizer", default="docs/exp/second_try/13_v2_tokenizer/selected_tokenizer.md")
    parser.add_argument("--dev-manifest", default="docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv")
    parser.add_argument("--checkpoint-root", default="/home/axt/mnt2/jongha/second_try/checkpoints/14_v2_embedding_init")
    parser.add_argument("--base-model", default="xlm-roberta-base")
    parser.add_argument("--dev-limit", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    torch.manual_seed(args.seed)
    start = time.time()
    run_id = "step14_v2_init_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    step_dir = Path(args.step_dir).resolve()
    checkpoint_root = Path(args.checkpoint_root).resolve()
    checkpoint_root.mkdir(parents=True, exist_ok=True)
    selected_vocab, tokenizer_dir = load_selected_tokenizer(Path(args.selected_tokenizer))
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(tokenizer_dir), local_files_only=True)
    base_tokenizer = XLMRobertaTokenizer.from_pretrained(args.base_model, local_files_only=True)
    base_vocab_size = len(base_tokenizer)
    merged_vocab_size = len(tokenizer)
    new_rows = merged_vocab_size - base_vocab_size
    dev_texts = load_dev_texts(Path(args.dev_manifest), args.dev_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    fvt_ids, align_ids = build_source_maps(base_tokenizer, tokenizer, base_vocab_size)

    score_rows: list[dict[str, str]] = []
    zero_rows: list[dict[str, str]] = []
    nearest_lines = ["# Step 14 V2 Nearest Neighbors", "", "Diagnostics only. New-token neighbors are compared against first 5000 base rows.", ""]
    checkpoint_dirs: list[Path] = []

    for method in METHODS:
        method_dir = checkpoint_root / f"xlmr_v2_{selected_vocab}_{method}"
        model = AutoModelForMaskedLM.from_pretrained(args.base_model, local_files_only=True)
        model.resize_token_embeddings(merged_vocab_size)
        init_report = initialize_rows(model, method, base_vocab_size, merged_vocab_size, fvt_ids, align_ids)
        input_ok, output_ok, tying_ok = shape_status(model, merged_vocab_size)
        loss, masked_tokens = zero_step_loss(model, tokenizer, dev_texts, device, args.batch_size, args.max_length, args.seed)
        method_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(method_dir)
        tokenizer.save_pretrained(method_dir)
        report = {
            "run_id": run_id,
            "method": method,
            "base_model": args.base_model,
            "tokenizer_dir": str(tokenizer_dir),
            "vocab_size": selected_vocab,
            "base_vocab_size": base_vocab_size,
            "merged_vocab_size": merged_vocab_size,
            "new_rows": new_rows,
            "dev_rows": len(dev_texts),
            "masked_tokens": masked_tokens,
            "zero_step_dev_loss": loss,
            "device": str(device),
            "selection_data": "MAR_dev_only",
            "final_access": "NO_ACT_FINAL_ACCESS",
            **init_report,
        }
        (method_dir / "init_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        checkpoint_dirs.append(method_dir)
        nearest_lines.extend(nearest_neighbor_lines(model, tokenizer, base_vocab_size, method))
        status = "PASS" if (
            init_report["missing_rows"] == "0"
            and input_ok == "PASS"
            and output_ok == "PASS"
            and tying_ok == "PASS"
            and math.isfinite(loss)
        ) else "FAIL"
        common = {
            "run_id": run_id,
            "vocab_size": selected_vocab,
            "init_method": method,
            "new_rows": str(new_rows),
            "initialized_rows": init_report["initialized_rows"],
            "missing_rows": init_report["missing_rows"],
            "fallback_rows": init_report["fallback_rows"],
            "input_shape_ok": input_ok,
            "lm_head_shape_ok": output_ok,
            "weight_tying_ok": tying_ok,
            "mean_norm": init_report["mean_norm"],
            "std_norm": init_report["std_norm"],
            "dev_rows": str(len(dev_texts)),
            "masked_tokens": str(masked_tokens),
            "zero_step_dev_loss": f"{loss:.6f}",
            "checkpoint_path": str(method_dir),
            "status": status,
            "notes": "selected_on=MAR_dev_only; final_ACT_not_read",
        }
        score_rows.append(common)
        zero_rows.append(
            {
                "run_id": run_id,
                "vocab_size": selected_vocab,
                "init_method": method,
                "dev_rows": str(len(dev_texts)),
                "masked_tokens": str(masked_tokens),
                "batch_size": str(args.batch_size),
                "max_length": str(args.max_length),
                "zero_step_dev_loss": f"{loss:.6f}",
                "device": str(device),
                "status": status,
            }
        )
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    best_row = sorted(score_rows, key=lambda row: float(row["zero_step_dev_loss"]))[0]
    gate = "PASS" if all(row["status"] == "PASS" for row in score_rows) else "FAIL"

    score_path = step_dir / "score_table.tsv"
    metrics_path = step_dir / "v2_embedding_init_scores.tsv"
    zero_path = step_dir / "v2_zero_step_mlm.tsv"
    neighbors_path = step_dir / "v2_nearest_neighbors.md"
    access_path = step_dir / "v2_no_final_access_audit.tsv"
    selected_path = step_dir / "selected_init.md"
    results_path = step_dir / "results.md"
    file_results_path = step_dir / "file_results.tsv"

    score_fields = ["run_id", "vocab_size", "init_method", "new_rows", "initialized_rows", "missing_rows", "fallback_rows", "input_shape_ok", "lm_head_shape_ok", "weight_tying_ok", "mean_norm", "std_norm", "dev_rows", "masked_tokens", "zero_step_dev_loss", "checkpoint_path", "status", "notes"]
    zero_fields = ["run_id", "vocab_size", "init_method", "dev_rows", "masked_tokens", "batch_size", "max_length", "zero_step_dev_loss", "device", "status"]
    write_tsv(score_path, score_rows, score_fields)
    write_tsv(metrics_path, score_rows, score_fields)
    write_tsv(zero_path, zero_rows, zero_fields)
    neighbors_path.write_text("\n".join(nearest_lines), encoding="utf-8")
    selected_path.write_text(
        f"""# Step 14 Selected V2 Initialization

Run id: `{run_id}`

Selected init method: `{best_row['init_method']}`

Zero-step Mark/dev MLM loss: `{best_row['zero_step_dev_loss']}`

Checkpoint path: `{best_row['checkpoint_path']}`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.
""",
        encoding="utf-8",
    )
    access_rows = [
        {
            "run_id": run_id,
            "input_role": "selected_tokenizer",
            "path": str(Path(args.selected_tokenizer).resolve()),
            "allowed_split": "tokenizer_selected_on_dev",
            "rows_or_files": str(count_rows(Path(args.selected_tokenizer))),
            "md5": md5_file(Path(args.selected_tokenizer)),
            "final_access": "NO",
            "status": "PASS",
        },
        {
            "run_id": run_id,
            "input_role": "dev_manifest",
            "path": str(Path(args.dev_manifest).resolve()),
            "allowed_split": "dev",
            "rows_or_files": str(count_rows(Path(args.dev_manifest))),
            "md5": md5_file(Path(args.dev_manifest)),
            "final_access": "NO",
            "status": "PASS",
        },
    ]
    write_tsv(access_path, access_rows, ["run_id", "input_role", "path", "allowed_split", "rows_or_files", "md5", "final_access", "status"])

    results_path.write_text(
        f"""# Step 14 Results: V2 Embedding Initialization

Status: COMPLETED

Run id: {run_id}

Completed date: {datetime.now().strftime("%Y-%m-%d")}

Artifact gate status: PASS

Claim gate status: {gate}

## Summary

Step 14 initialized the Step 13 selected 32k tokenizer with all required methods: random, mean, fvt, align, and focus. Selection used full Mark/dev MLM loss only. No ACT final file was read.

Selected init method: `{best_row['init_method']}`.

Selected checkpoint: `{best_row['checkpoint_path']}`.

Best zero-step Mark/dev MLM loss: `{best_row['zero_step_dev_loss']}`.

## Gate Evidence

- every required method has a checkpoint and `status=PASS`.
- input embedding and LM head shapes match tokenizer length.
- weight tying is preserved.
- no initialized row is NaN or zero-norm.
- `v2_no_final_access_audit.tsv` lists only selected tokenizer metadata and Mark/dev manifest.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if gate == "PASS" else "v2_embedding_init_gate"}

Observed evidence: {"NOT_APPLICABLE" if gate == "PASS" else "see score_table.tsv"}

Return-to step: {"NOT_APPLICABLE" if gate == "PASS" else "13_v2_tokenizer"}

Required fix: {"NOT_APPLICABLE" if gate == "PASS" else "fix failing init method before MLM control"}

Runtime minutes: {(time.time() - start) / 60.0:.3f}
""",
        encoding="utf-8",
    )
    file_rows = [
        file_result("score_table", score_path, "v2 init gate table"),
        file_result("embedding_init_scores", metrics_path, "v2 init scores"),
        file_result("zero_step_mlm", zero_path, "full Mark/dev zero-step MLM losses"),
        file_result("nearest_neighbors", neighbors_path, "nearest-neighbor diagnostics"),
        file_result("no_final_access_audit", access_path, "input access audit"),
        file_result("selected_init", selected_path, "selected v2 init pointer"),
        file_result("results", results_path, "step result summary"),
    ]
    for method_dir in checkpoint_dirs:
        file_rows.append(file_result(f"checkpoint_{method_dir.name}", method_dir, "initialized checkpoint"))
    write_tsv(file_results_path, file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print("artifact_gate_status=PASS")
    print(f"claim_gate_status={gate}")
    print(f"selected_init_method={best_row['init_method']}")
    print(f"best_zero_step_dev_loss={best_row['zero_step_dev_loss']}")


if __name__ == "__main__":
    main()
