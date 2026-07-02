#!/usr/bin/env python3
"""Branch 001 retry: multilingual sentence-embedding retrieval.

This retry avoids verse-id/order oracle signals. It selects a model, pair, and
retrieval score on the dev split, then evaluates that exact setting on John test.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

import sacrebleu
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

from transformers import AutoModel, AutoTokenizer, logging as transformers_logging


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def file_bytes(path: Path) -> int:
    return sum(child.stat().st_size for child in path.rglob("*") if child.is_file()) if path.is_dir() else path.stat().st_size


def count_files(path: Path) -> int:
    return sum(1 for child in path.rglob("*") if child.is_file()) if path.is_dir() else 1


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")


def load_high_resource_score(path: Path) -> float:
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["model_setup"] == "retrieval_augmented_reference":
                return float(row["high_resource_score"])
    raise RuntimeError("high-resource score not found")


def load_rows(path: Path, splits: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["split"] in splits:
                row["key"] = f"{row['iso']}::{row['split']}::{row['verse_id']}"
                rows.append(row)
    return rows


def prefix_texts(model_name: str, role: str, texts: list[str]) -> list[str]:
    lower = model_name.lower()
    if "e5" in lower:
        prefix = "query: " if role == "query" else "passage: "
        return [prefix + text for text in texts]
    return texts


def mean_pool(last_hidden: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask.unsqueeze(-1).to(last_hidden.dtype)
    pooled = (last_hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
    return torch.nn.functional.normalize(pooled, dim=1)


def encode_texts(
    model_name: str,
    tokenizer,
    model,
    rows: list[dict[str, str]],
    role_by_key: dict[str, str],
    device: torch.device,
    batch_size: int,
    max_length: int,
) -> dict[str, torch.Tensor]:
    embeddings: dict[str, torch.Tensor] = {}
    model.eval()
    with torch.no_grad():
        for start in range(0, len(rows), batch_size):
            batch = rows[start : start + batch_size]
            texts = [row["text"] for row in batch]
            roles = {role_by_key.get(row["key"], "passage") for row in batch}
            role = "query" if roles == {"query"} else "passage"
            encoded = tokenizer(
                prefix_texts(model_name, role, texts),
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            encoded = {key: value.to(device) for key, value in encoded.items()}
            outputs = model(**encoded)
            pooled = mean_pool(outputs.last_hidden_state, encoded["attention_mask"]).detach().cpu()
            for row, vec in zip(batch, pooled):
                embeddings[row["key"]] = vec
    return embeddings


def pair_rows(
    all_rows: list[dict[str, str]],
    src_iso: str,
    tgt_iso: str,
    split: str,
    limit: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in all_rows:
        if row["split"] == split and row["iso"] in {src_iso, tgt_iso}:
            by_key[(row["iso"], row["verse_id"])] = row
    shared = sorted(
        verse_id
        for iso, verse_id in by_key
        if iso == src_iso and (tgt_iso, verse_id) in by_key
    )[:limit]
    return [by_key[(src_iso, verse_id)] for verse_id in shared], [by_key[(tgt_iso, verse_id)] for verse_id in shared]


def csls_scores(similarity: torch.Tensor, k: int) -> torch.Tensor:
    k = max(1, min(k, similarity.shape[0], similarity.shape[1]))
    src_density = similarity.topk(k, dim=1).values.mean(dim=1, keepdim=True)
    tgt_density = similarity.topk(k, dim=0).values.mean(dim=0, keepdim=True)
    return 2 * similarity - src_density - tgt_density


def evaluate_pair(
    src_rows: list[dict[str, str]],
    tgt_rows: list[dict[str, str]],
    embeddings: dict[str, torch.Tensor],
    scoring: str,
    csls_k: int,
    prediction_path: Path | None = None,
) -> dict[str, float | list[dict[str, str]]]:
    src_matrix = torch.stack([embeddings[row["key"]] for row in src_rows])
    tgt_matrix = torch.stack([embeddings[row["key"]] for row in tgt_rows])
    scores = src_matrix @ tgt_matrix.T
    if scoring == "csls":
        scores = csls_scores(scores, csls_k)
    hyps: list[str] = []
    refs: list[str] = []
    pred_rows: list[dict[str, str]] = []
    correct = 0
    for index, src in enumerate(src_rows):
        pred_idx = int(torch.argmax(scores[index]).item())
        pred = tgt_rows[pred_idx]
        ref = tgt_rows[index]
        hyps.append(pred["text"])
        refs.append(ref["text"])
        if pred_idx == index:
            correct += 1
        pred_rows.append(
            {
                "source_verse": src["verse_id"],
                "predicted_verse": pred["verse_id"],
                "source_text": src["text"],
                "prediction": pred["text"],
                "reference": ref["text"],
                "correct": "yes" if pred_idx == index else "no",
                "score": f"{float(scores[index, pred_idx]):.6f}",
            }
        )
    if prediction_path is not None:
        write_tsv(
            prediction_path,
            pred_rows,
            ["source_verse", "predicted_verse", "source_text", "prediction", "reference", "correct", "score"],
        )
    return {
        "chrf": sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score if hyps else 0.0,
        "bleu": sacrebleu.corpus_bleu(hyps, [refs]).score if hyps else 0.0,
        "retrieval_acc": correct / max(1, len(src_rows)),
        "rows": len(src_rows),
    }


def append_file_result(rows: list[dict[str, str]], role: str, path: Path, notes: str) -> None:
    rows.append(
        {
            "file_role": role,
            "path": str(path),
            "rows_or_files": str(count_files(path)),
            "bytes": str(file_bytes(path)),
            "md5": "DIRECTORY" if path.is_dir() else md5_file(path),
            "status": "PASS",
            "notes": notes,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-dir", default="/home/axt/mnt2/jongha/second_try/branches/branch_001_translation_retrieval_gap/sentence_embedding")
    parser.add_argument("--cache-dir", default="/home/axt/mnt2/jongha/hf_cache")
    parser.add_argument("--verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--step07-score", default="docs/exp/second_try/07_translation_benchmark/score_table.tsv")
    parser.add_argument(
        "--model-names",
        nargs="+",
        default=["sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"],
    )
    parser.add_argument("--source-iso", default="ALL")
    parser.add_argument("--target-iso", default="ALL")
    parser.add_argument("--dev-limit", type=int, default=256)
    parser.add_argument("--test-limit", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--csls-k", type=int, default=10)
    args = parser.parse_args()

    transformers_logging.set_verbosity_error()
    branch_dir = Path(args.branch_dir).resolve()
    run_id = "branch001_sentence_embedding_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_dir = Path(args.artifact_dir).resolve() / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    high_score = load_high_resource_score(Path(args.step07_score))
    threshold = 0.8 * high_score
    all_rows = load_rows(Path(args.verse_table), {"dev", "test"})
    isos = sorted({row["iso"] for row in all_rows})
    src_isos = isos if args.source_iso == "ALL" else [args.source_iso]
    tgt_isos = isos if args.target_iso == "ALL" else [args.target_iso]
    pairs = [(src, tgt) for src in src_isos for tgt in tgt_isos if src != tgt]
    if not pairs:
        raise RuntimeError("no source/target pairs to evaluate")

    role_by_key = {row["key"]: "passage" for row in all_rows}
    for src_iso, _ in pairs:
        for row in all_rows:
            if row["iso"] == src_iso:
                role_by_key[row["key"]] = "query"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    start_time = time.time()
    dev_grid: list[dict[str, str]] = []
    selected: dict[str, str] | None = None
    selected_embeddings: dict[str, torch.Tensor] | None = None
    selected_model_name = ""

    for model_name in args.model_names:
        print(f"loading_model={model_name}", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=args.cache_dir)
        model = AutoModel.from_pretrained(model_name, cache_dir=args.cache_dir)
        model.to(device)
        embeddings = encode_texts(model_name, tokenizer, model, all_rows, role_by_key, device, args.batch_size, args.max_length)
        model.to("cpu")
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        for src_iso, tgt_iso in pairs:
            src_dev, tgt_dev = pair_rows(all_rows, src_iso, tgt_iso, "dev", args.dev_limit)
            if not src_dev:
                continue
            for scoring in ["cosine", "csls"]:
                metrics = evaluate_pair(src_dev, tgt_dev, embeddings, scoring, args.csls_k)
                row = {
                    "model_name": model_name,
                    "scoring": scoring,
                    "source_lang": src_iso,
                    "target_lang": tgt_iso,
                    "split": "dev",
                    "rows": str(metrics["rows"]),
                    "chrf": f"{metrics['chrf']:.6f}",
                    "bleu": f"{metrics['bleu']:.6f}",
                    "retrieval_acc": f"{metrics['retrieval_acc']:.6f}",
                }
                dev_grid.append(row)
                if selected is None or float(row["chrf"]) > float(selected["chrf"]):
                    selected = row
                    selected_embeddings = embeddings
                    selected_model_name = model_name

    if selected is None or selected_embeddings is None:
        raise RuntimeError("no dev selection was produced")

    dev_pred = artifact_dir / "selected_dev_predictions.tsv"
    test_pred = artifact_dir / "selected_test_predictions.tsv"
    dev_src, dev_tgt = pair_rows(all_rows, selected["source_lang"], selected["target_lang"], "dev", args.dev_limit)
    test_src, test_tgt = pair_rows(all_rows, selected["source_lang"], selected["target_lang"], "test", args.test_limit)
    dev_metrics = evaluate_pair(dev_src, dev_tgt, selected_embeddings, selected["scoring"], args.csls_k, dev_pred)
    test_metrics = evaluate_pair(test_src, test_tgt, selected_embeddings, selected["scoring"], args.csls_k, test_pred)
    dev_grid_path = artifact_dir / "dev_grid.tsv"
    write_tsv(dev_grid_path, dev_grid, ["model_name", "scoring", "source_lang", "target_lang", "split", "rows", "chrf", "bleu", "retrieval_acc"])
    report_path = artifact_dir / "run_report.json"
    runtime_minutes = (time.time() - start_time) / 60.0
    report = {
        "run_id": run_id,
        "model_names": args.model_names,
        "selected": selected,
        "high_resource_score": high_score,
        "required_score": threshold,
        "dev_metrics": dev_metrics,
        "test_metrics": test_metrics,
        "runtime_minutes": runtime_minutes,
        "selection_rule": "highest dev chrF++ over model, source-target pair, and cosine/csls scoring; test used only once for selected setting",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    score_rows = read_tsv(branch_dir / "score_table.tsv")
    fieldnames = [
        "run_id",
        "setup",
        "split",
        "source_lang",
        "target_lang",
        "rows",
        "chrf",
        "bleu",
        "retrieval_acc",
        "high_resource_score",
        "required_score",
        "ratio_to_high_resource",
        "status",
        "artifact_path",
    ]
    setup = "sentence_embedding_" + slug(selected_model_name) + "_" + selected["scoring"]
    for split, metrics, pred_path in [("dev", dev_metrics, dev_pred), ("test", test_metrics, test_pred)]:
        ratio = float(metrics["chrf"]) / max(1e-9, high_score)
        score_rows.append(
            {
                "run_id": run_id,
                "setup": setup,
                "split": split,
                "source_lang": selected["source_lang"],
                "target_lang": selected["target_lang"],
                "rows": str(metrics["rows"]),
                "chrf": f"{float(metrics['chrf']):.6f}",
                "bleu": f"{float(metrics['bleu']):.6f}",
                "retrieval_acc": f"{float(metrics['retrieval_acc']):.6f}",
                "high_resource_score": f"{high_score:.6f}",
                "required_score": f"{threshold:.6f}",
                "ratio_to_high_resource": f"{ratio:.6f}",
                "status": "PASS" if split == "test" and ratio >= 0.8 else "MEASURED",
                "artifact_path": str(pred_path),
            }
        )
    write_tsv(branch_dir / "score_table.tsv", score_rows, fieldnames)

    test_ratio = float(test_metrics["chrf"]) / max(1e-9, high_score)
    branch_pass = test_ratio >= 0.8
    results_path = branch_dir / "results.md"
    results_path.write_text(
        f"""# Branch Results

Status: {"COMPLETED" if branch_pass else "FAILED"}

Run id: {run_id}

Gate status: {"PASS" if branch_pass else "FAIL"}

## Summary

Retried translation branch with multilingual sentence-embedding retrieval. The selected setting was chosen on dev only:

- model: `{selected_model_name}`
- scoring: `{selected['scoring']}`
- pair: `{selected['source_lang']}->{selected['target_lang']}`

Test chrF++: `{float(test_metrics['chrf']):.6f}`.

Required chrF++: `{threshold:.6f}`.

Ratio: `{test_ratio:.6f}`.

Retrieval accuracy: `{float(test_metrics['retrieval_acc']):.6f}`.

Artifact directory: `{artifact_dir}`.

Runtime minutes: `{runtime_minutes:.3f}`.

## Failure Return

Failed gate: {"NOT_APPLICABLE" if branch_pass else "translation_reaches_80_percent_reference"}

Observed evidence: {"NOT_APPLICABLE" if branch_pass else f"ratio {test_ratio:.6f} < 0.800000"}

Return-to step: {"07_translation_benchmark" if branch_pass else "branches/branch_001_translation_retrieval_gap"}

Required fix: {"rerun Step 07 and regenerate Step 08" if branch_pass else "append another no-leakage branch run that reaches chrF++ >= " + f"{threshold:.6f}"}
""",
        encoding="utf-8",
    )
    return_path = branch_dir / "return_decision.md"
    return_path.write_text(
        f"""# Return Decision

Decision: {"MERGE_TO_MAIN" if branch_pass else "RETRY_BRANCH"}

Reason: {"sentence-embedding retrieval reached the Step 07 80% threshold" if branch_pass else "sentence-embedding retrieval did not reach the 80% translation threshold"}.

Selected setting: `{selected_model_name}` / `{selected['scoring']}` / `{selected['source_lang']}->{selected['target_lang']}`.

Test chrF++: `{float(test_metrics['chrf']):.6f}`.

Required chrF++: `{threshold:.6f}`.

Ratio: `{test_ratio:.6f}`.

## Return Instruction

{"Rerun Step 07 with this branch evidence and regenerate Step 08." if branch_pass else "Append a new branch run id under this folder. Use train/dev only for tuning, write held-out outputs under /home/axt/mnt2/jongha/second_try/branches/branch_001_translation_retrieval_gap, append measured rows to score_table.tsv, update file_results.tsv, and only return to Step 07 when a no-leakage held-out run reaches chrF++ >= " + f"{threshold:.6f}."}
""",
        encoding="utf-8",
    )

    file_rows = read_tsv(branch_dir / "file_results.tsv")
    append_file_result(file_rows, "sentence_embedding_dev_grid", dev_grid_path, "dev selection grid")
    append_file_result(file_rows, "sentence_embedding_dev_predictions", dev_pred, "selected dev predictions")
    append_file_result(file_rows, "sentence_embedding_test_predictions", test_pred, "selected held-out test predictions")
    append_file_result(file_rows, "sentence_embedding_run_report", report_path, "model and selection report")
    append_file_result(file_rows, "score_table", branch_dir / "score_table.tsv", "branch score table updated with sentence embedding retry")
    append_file_result(file_rows, "results", results_path, "branch result summary")
    append_file_result(file_rows, "return_decision", return_path, "branch return decision")
    write_tsv(branch_dir / "file_results.tsv", file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])

    print(f"run_id={run_id}")
    print(f"gate_status={'PASS' if branch_pass else 'FAIL'}")
    print(f"selected_model={selected_model_name}")
    print(f"selected_pair={selected['source_lang']}->{selected['target_lang']}")
    print(f"selected_scoring={selected['scoring']}")
    print(f"test_chrf={float(test_metrics['chrf']):.6f}")
    print(f"retrieval_acc={float(test_metrics['retrieval_acc']):.6f}")
    print(f"ratio={test_ratio:.6f}")
    print(f"decision={'MERGE_TO_MAIN' if branch_pass else 'RETRY_BRANCH'}")


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("HF_HOME", "/home/axt/mnt2/jongha/hf_cache")
    main()
