#!/usr/bin/env python3
"""Branch 001 retry: fine-tune ByT5-small for usp->kbh translation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
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

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def count_files(path: Path) -> int:
    return sum(1 for child in path.rglob("*") if child.is_file()) if path.is_dir() else 1


def file_bytes(path: Path) -> int:
    return sum(child.stat().st_size for child in path.rglob("*") if child.is_file()) if path.is_dir() else path.stat().st_size


def load_high_resource_score(path: Path) -> float:
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["model_setup"] == "retrieval_augmented_reference":
                return float(row["high_resource_score"])
    raise RuntimeError("high-resource score not found")


def load_pairs(path: Path, src_iso: str, tgt_iso: str) -> dict[str, tuple[dict[str, str], dict[str, str]]]:
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["iso"] in {src_iso, tgt_iso}:
                by_key[(row["iso"], row["verse_id"])] = row
    pairs: dict[str, tuple[dict[str, str], dict[str, str]]] = {}
    for (iso, verse_id), src in by_key.items():
        if iso != src_iso:
            continue
        tgt = by_key.get((tgt_iso, verse_id))
        if tgt and src["split"] == tgt["split"]:
            pairs[verse_id] = (src, tgt)
    return pairs


def split_pairs(pairs: dict[str, tuple[dict[str, str], dict[str, str]]], split: str, limit: int) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for verse_id in sorted(pairs):
        src, tgt = pairs[verse_id]
        if src["split"] == split:
            rows.append((verse_id, src["text"], tgt["text"]))
        if len(rows) >= limit:
            break
    return rows


def make_source(text: str, src_iso: str, tgt_iso: str) -> str:
    return f"translate {src_iso} to {tgt_iso}: {text}"


def batchify(rows: list[tuple[str, str, str]], batch_size: int, rng: random.Random):
    shuffled = list(rows)
    rng.shuffle(shuffled)
    for start in range(0, len(shuffled), batch_size):
        yield shuffled[start : start + batch_size]


def encode_batch(tokenizer, batch: list[tuple[str, str, str]], src_iso: str, tgt_iso: str, max_source_length: int, max_target_length: int, device: torch.device):
    sources = [make_source(src, src_iso, tgt_iso) for _, src, _ in batch]
    targets = [tgt for _, _, tgt in batch]
    model_inputs = tokenizer(
        sources,
        padding=True,
        truncation=True,
        max_length=max_source_length,
        return_tensors="pt",
    )
    labels = tokenizer(
        targets,
        padding=True,
        truncation=True,
        max_length=max_target_length,
        return_tensors="pt",
    )["input_ids"]
    labels[labels == tokenizer.pad_token_id] = -100
    return {
        "input_ids": model_inputs["input_ids"].to(device),
        "attention_mask": model_inputs["attention_mask"].to(device),
        "labels": labels.to(device),
    }


def evaluate(model, tokenizer, rows: list[tuple[str, str, str]], src_iso: str, tgt_iso: str, device: torch.device, args: argparse.Namespace, prediction_path: Path) -> dict[str, float]:
    model.eval()
    hyps: list[str] = []
    refs: list[str] = []
    pred_rows: list[dict[str, str]] = []
    with torch.no_grad():
        for start in range(0, len(rows), args.eval_batch_size):
            batch = rows[start : start + args.eval_batch_size]
            sources = [make_source(src, src_iso, tgt_iso) for _, src, _ in batch]
            encoded = tokenizer(
                sources,
                padding=True,
                truncation=True,
                max_length=args.max_source_length,
                return_tensors="pt",
            )
            generated = model.generate(
                input_ids=encoded["input_ids"].to(device),
                attention_mask=encoded["attention_mask"].to(device),
                max_length=args.generation_max_length,
                num_beams=args.num_beams,
            )
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for (verse_id, source, reference), pred in zip(batch, decoded):
                pred = " ".join(pred.split())
                hyps.append(pred)
                refs.append(reference)
                pred_rows.append(
                    {
                        "verse_id": verse_id,
                        "source": source,
                        "prediction": pred,
                        "reference": reference,
                    }
                )
    write_tsv(prediction_path, pred_rows, ["verse_id", "source", "prediction", "reference"])
    chrf = sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score if hyps else 0.0
    bleu = sacrebleu.corpus_bleu(hyps, [refs]).score if hyps else 0.0
    copy_rate = sum(1 for h, row in zip(hyps, rows) if h == row[1]) / max(1, len(hyps))
    avg_len = sum(len(h.split()) for h in hyps) / max(1, len(hyps))
    return {"chrf": chrf, "bleu": bleu, "copy_rate": copy_rate, "gen_len": avg_len}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-dir", default="/home/axt/mnt2/jongha/second_try/branches/branch_001_translation_retrieval_gap/byt5_usp_kbh")
    parser.add_argument("--verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--step07-score", default="docs/exp/second_try/07_translation_benchmark/score_table.tsv")
    parser.add_argument("--model-name", default="google/byt5-small")
    parser.add_argument("--source-iso", default="usp")
    parser.add_argument("--target-iso", default="kbh")
    parser.add_argument("--train-limit", type=int, default=4096)
    parser.add_argument("--dev-limit", type=int, default=256)
    parser.add_argument("--test-limit", type=int, default=100)
    parser.add_argument("--train-steps", type=int, default=800)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--eval-batch-size", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--max-grad-norm", type=float, default=1.0)
    parser.add_argument("--max-source-length", type=int, default=256)
    parser.add_argument("--max-target-length", type=int, default=256)
    parser.add_argument("--generation-max-length", type=int, default=160)
    parser.add_argument("--num-beams", type=int, default=1)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    branch_dir = Path(args.branch_dir).resolve()
    run_id = "branch001_byt5_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_dir = Path(args.artifact_dir).resolve() / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    high_score = load_high_resource_score(Path(args.step07_score))
    threshold = 0.8 * high_score
    pairs = load_pairs(Path(args.verse_table), args.source_iso, args.target_iso)
    train_rows = split_pairs(pairs, "train", args.train_limit)
    dev_rows = split_pairs(pairs, "dev", args.dev_limit)
    test_rows = split_pairs(pairs, "test", args.test_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name, local_files_only=True)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    scaler = torch.cuda.amp.GradScaler(enabled=args.fp16 and torch.cuda.is_available())
    rng = random.Random(args.seed)
    losses: list[float] = []
    start_time = time.time()
    step = 0
    while step < args.train_steps:
        for batch in batchify(train_rows, args.batch_size, rng):
            model.train()
            encoded = encode_batch(tokenizer, batch, args.source_iso, args.target_iso, args.max_source_length, args.max_target_length, device)
            optimizer.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=args.fp16 and torch.cuda.is_available()):
                loss = model(**encoded).loss
            if not torch.isfinite(loss):
                raise RuntimeError(f"non-finite training loss at step {step + 1}: {loss.item()}")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)
            scaler.step(optimizer)
            scaler.update()
            losses.append(float(loss.detach().cpu().item()))
            step += 1
            if step % 50 == 0:
                print(f"step={step} loss={sum(losses[-50:]) / len(losses[-50:]):.4f}", flush=True)
            if step >= args.train_steps:
                break

    dev_pred_path = artifact_dir / "dev_predictions.tsv"
    test_pred_path = artifact_dir / "test_predictions.tsv"
    dev_metrics = evaluate(model, tokenizer, dev_rows, args.source_iso, args.target_iso, device, args, dev_pred_path)
    test_metrics = evaluate(model, tokenizer, test_rows, args.source_iso, args.target_iso, device, args, test_pred_path)
    checkpoint_dir = artifact_dir / "checkpoint"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    runtime_minutes = (time.time() - start_time) / 60.0

    report = {
        "run_id": run_id,
        "model_name": args.model_name,
        "source_iso": args.source_iso,
        "target_iso": args.target_iso,
        "train_rows": len(train_rows),
        "dev_rows": len(dev_rows),
        "test_rows": len(test_rows),
        "train_steps": args.train_steps,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "train_loss": sum(losses) / max(1, len(losses)),
        "runtime_minutes": runtime_minutes,
        "dev_metrics": dev_metrics,
        "test_metrics": test_metrics,
    }
    (artifact_dir / "run_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    existing_rows = read_tsv(branch_dir / "score_table.tsv")
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
    for split, rows, metrics, pred_path in [
        ("dev", dev_rows, dev_metrics, dev_pred_path),
        ("test", test_rows, test_metrics, test_pred_path),
    ]:
        ratio = metrics["chrf"] / max(1e-9, high_score)
        existing_rows.append(
            {
                "run_id": run_id,
                "setup": "byt5_small_finetune",
                "split": split,
                "source_lang": args.source_iso,
                "target_lang": args.target_iso,
                "rows": str(len(rows)),
                "chrf": f"{metrics['chrf']:.6f}",
                "bleu": f"{metrics['bleu']:.6f}",
                "retrieval_acc": "NOT_APPLICABLE",
                "high_resource_score": f"{high_score:.6f}",
                "required_score": f"{threshold:.6f}",
                "ratio_to_high_resource": f"{ratio:.6f}",
                "status": "PASS" if split == "test" and ratio >= 0.8 else "MEASURED",
                "artifact_path": str(pred_path),
            }
        )
    write_tsv(branch_dir / "score_table.tsv", existing_rows, fieldnames)

    test_ratio = test_metrics["chrf"] / max(1e-9, high_score)
    branch_pass = test_ratio >= 0.8
    (branch_dir / "results.md").write_text(
        f"""# Branch Results

Status: {"COMPLETED" if branch_pass else "FAILED"}

Run id: {run_id}

Gate status: {"PASS" if branch_pass else "FAIL"}

## Summary

Retried translation branch with ByT5-small fine-tuning for `{args.source_iso}->{args.target_iso}` using train split only. Dev was used for measurement, and John test was held out for final scoring.

Test chrF++: `{test_metrics['chrf']:.6f}`.

Required chrF++: `{threshold:.6f}`.

Ratio: `{test_ratio:.6f}`.

Checkpoint artifact: `{checkpoint_dir}`.

Runtime minutes: `{runtime_minutes:.3f}`.
""",
        encoding="utf-8",
    )
    (branch_dir / "return_decision.md").write_text(
        f"""# Return Decision

Decision: {"MERGE_TO_MAIN" if branch_pass else "RETRY_BRANCH"}

Reason: {"ByT5 fine-tuning reached the Step 07 80% threshold" if branch_pass else "ByT5 fine-tuning did not reach the 80% translation threshold"}
""",
        encoding="utf-8",
    )
    file_rows = [
        {
            "file_role": "score_table",
            "path": str(branch_dir / "score_table.tsv"),
            "rows_or_files": str(len(existing_rows)),
            "bytes": str((branch_dir / "score_table.tsv").stat().st_size),
            "md5": md5_file(branch_dir / "score_table.tsv"),
            "status": "PASS",
            "notes": "branch score table with ByT5 retry",
        },
        {
            "file_role": "byt5_checkpoint",
            "path": str(checkpoint_dir),
            "rows_or_files": str(count_files(checkpoint_dir)),
            "bytes": str(file_bytes(checkpoint_dir)),
            "md5": "DIRECTORY",
            "status": "PASS",
            "notes": "large branch checkpoint",
        },
        {
            "file_role": "byt5_test_predictions",
            "path": str(test_pred_path),
            "rows_or_files": str(len(test_rows)),
            "bytes": str(test_pred_path.stat().st_size),
            "md5": md5_file(test_pred_path),
            "status": "PASS",
            "notes": "held-out John predictions",
        },
        {
            "file_role": "byt5_run_report",
            "path": str(artifact_dir / "run_report.json"),
            "rows_or_files": "1",
            "bytes": str((artifact_dir / "run_report.json").stat().st_size),
            "md5": md5_file(artifact_dir / "run_report.json"),
            "status": "PASS",
            "notes": "training and metric config",
        },
    ]
    write_tsv(branch_dir / "file_results.tsv", file_rows, ["file_role", "path", "rows_or_files", "bytes", "md5", "status", "notes"])
    print(f"run_id={run_id}")
    print(f"gate_status={'PASS' if branch_pass else 'FAIL'}")
    print(f"test_chrf={test_metrics['chrf']:.6f}")
    print(f"ratio={test_ratio:.6f}")
    print(f"decision={'MERGE_TO_MAIN' if branch_pass else 'RETRY_BRANCH'}")


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
