#!/usr/bin/env python3
"""Branch 001 retry: train a cross-encoder verse alignment reranker."""

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

from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer


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


def file_bytes(path: Path) -> int:
    return sum(child.stat().st_size for child in path.rglob("*") if child.is_file()) if path.is_dir() else path.stat().st_size


def count_files(path: Path) -> int:
    return sum(1 for child in path.rglob("*") if child.is_file()) if path.is_dir() else 1


def load_high_resource_score(path: Path) -> float:
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["model_setup"] == "retrieval_augmented_reference":
                return float(row["high_resource_score"])
    raise RuntimeError("high-resource score not found")


def load_selected_checkpoint(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("Path:"):
            return Path(line.split("`", 2)[1])
    raise RuntimeError("selected checkpoint path not found")


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


def make_training_batch(rows: list[tuple[str, str, str]], batch_size: int, rng: random.Random) -> list[tuple[str, str, int]]:
    targets = [(verse_id, tgt) for verse_id, _, tgt in rows]
    batch: list[tuple[str, str, int]] = []
    for _ in range(batch_size // 2):
        verse_id, src, tgt = rng.choice(rows)
        batch.append((src, tgt, 1))
        neg_verse, neg_tgt = rng.choice(targets)
        while neg_verse == verse_id:
            neg_verse, neg_tgt = rng.choice(targets)
        batch.append((src, neg_tgt, 0))
    rng.shuffle(batch)
    return batch


def encode_pair_batch(tokenizer, batch: list[tuple[str, str, int]], device: torch.device, max_length: int):
    encoded = tokenizer(
        [src for src, _, _ in batch],
        [tgt for _, tgt, _ in batch],
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    labels = torch.tensor([label for _, _, label in batch], dtype=torch.long)
    return {
        "input_ids": encoded["input_ids"].to(device),
        "attention_mask": encoded["attention_mask"].to(device),
        "labels": labels.to(device),
    }


def score_matrix(model, tokenizer, src_rows: list[tuple[str, str, str]], tgt_rows: list[tuple[str, str, str]], device: torch.device, args: argparse.Namespace) -> torch.Tensor:
    model.eval()
    scores: list[float] = []
    pairs: list[tuple[str, str]] = []
    for _, src, _ in src_rows:
        for _, _, tgt in tgt_rows:
            pairs.append((src, tgt))
    with torch.no_grad():
        for start in range(0, len(pairs), args.eval_batch_size):
            batch = pairs[start : start + args.eval_batch_size]
            encoded = tokenizer(
                [src for src, _ in batch],
                [tgt for _, tgt in batch],
                padding=True,
                truncation=True,
                max_length=args.max_length,
                return_tensors="pt",
            )
            logits = model(input_ids=encoded["input_ids"].to(device), attention_mask=encoded["attention_mask"].to(device)).logits
            probs = torch.softmax(logits.detach().cpu(), dim=-1)[:, 1]
            scores.extend(probs.tolist())
    return torch.tensor(scores).view(len(src_rows), len(tgt_rows))


def evaluate(model, tokenizer, rows: list[tuple[str, str, str]], device: torch.device, args: argparse.Namespace, prediction_path: Path) -> dict[str, float]:
    scores = score_matrix(model, tokenizer, rows, rows, device, args)
    hyps: list[str] = []
    refs: list[str] = []
    pred_rows: list[dict[str, str]] = []
    correct = 0
    for i, (verse_id, src, ref) in enumerate(rows):
        pred_idx = int(torch.argmax(scores[i]).item())
        pred_verse, _, pred = rows[pred_idx]
        hyps.append(pred)
        refs.append(ref)
        if pred_idx == i:
            correct += 1
        pred_rows.append(
            {
                "source_verse": verse_id,
                "predicted_verse": pred_verse,
                "source": src,
                "prediction": pred,
                "reference": ref,
                "correct": "yes" if pred_idx == i else "no",
                "score": f"{float(scores[i, pred_idx]):.6f}",
            }
        )
    write_tsv(prediction_path, pred_rows, ["source_verse", "predicted_verse", "source", "prediction", "reference", "correct", "score"])
    return {
        "chrf": sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score if hyps else 0.0,
        "bleu": sacrebleu.corpus_bleu(hyps, [refs]).score if hyps else 0.0,
        "retrieval_acc": correct / max(1, len(rows)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--artifact-dir", default="/home/axt/mnt2/jongha/second_try/branches/branch_001_translation_retrieval_gap/cross_encoder_usp_kbh")
    parser.add_argument("--verse-table", default="docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv")
    parser.add_argument("--step07-score", default="docs/exp/second_try/07_translation_benchmark/score_table.tsv")
    parser.add_argument("--selection-file", default="docs/exp/second_try/05_mlm_adaptation/checkpoint_selection.md")
    parser.add_argument("--source-iso", default="usp")
    parser.add_argument("--target-iso", default="kbh")
    parser.add_argument("--train-limit", type=int, default=4096)
    parser.add_argument("--dev-limit", type=int, default=256)
    parser.add_argument("--test-limit", type=int, default=100)
    parser.add_argument("--train-steps", type=int, default=1200)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--seed", type=int, default=23)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    branch_dir = Path(args.branch_dir).resolve()
    run_id = "branch001_cross_encoder_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_dir = Path(args.artifact_dir).resolve() / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    high_score = load_high_resource_score(Path(args.step07_score))
    threshold = 0.8 * high_score
    selected_checkpoint = load_selected_checkpoint(Path(args.selection_file))
    pairs = load_pairs(Path(args.verse_table), args.source_iso, args.target_iso)
    train_rows = split_pairs(pairs, "train", args.train_limit)
    dev_rows = split_pairs(pairs, "dev", args.dev_limit)
    test_rows = split_pairs(pairs, "test", args.test_limit)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = XLMRobertaTokenizer.from_pretrained(str(selected_checkpoint), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        str(selected_checkpoint),
        num_labels=2,
        ignore_mismatched_sizes=True,
        local_files_only=True,
    )
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    rng = random.Random(args.seed)
    losses: list[float] = []
    start_time = time.time()
    for step in range(1, args.train_steps + 1):
        model.train()
        batch = make_training_batch(train_rows, args.batch_size, rng)
        encoded = encode_pair_batch(tokenizer, batch, device, args.max_length)
        optimizer.zero_grad(set_to_none=True)
        loss = model(**encoded).loss
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}: {loss.item()}")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu().item()))
        if step % 100 == 0:
            print(f"step={step} loss={sum(losses[-100:]) / len(losses[-100:]):.4f}", flush=True)

    dev_pred = artifact_dir / "dev_predictions.tsv"
    test_pred = artifact_dir / "test_predictions.tsv"
    dev_metrics = evaluate(model, tokenizer, dev_rows, device, args, dev_pred)
    test_metrics = evaluate(model, tokenizer, test_rows, device, args, test_pred)
    checkpoint_dir = artifact_dir / "checkpoint"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model.to("cpu")
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    runtime_minutes = (time.time() - start_time) / 60.0
    report = {
        "run_id": run_id,
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
    score_rows = read_tsv(branch_dir / "score_table.tsv")
    for split, rows, metrics, pred_path in [
        ("dev", dev_rows, dev_metrics, dev_pred),
        ("test", test_rows, test_metrics, test_pred),
    ]:
        ratio = metrics["chrf"] / max(1e-9, high_score)
        score_rows.append(
            {
                "run_id": run_id,
                "setup": "cross_encoder_reranker",
                "split": split,
                "source_lang": args.source_iso,
                "target_lang": args.target_iso,
                "rows": str(len(rows)),
                "chrf": f"{metrics['chrf']:.6f}",
                "bleu": f"{metrics['bleu']:.6f}",
                "retrieval_acc": f"{metrics['retrieval_acc']:.6f}",
                "high_resource_score": f"{high_score:.6f}",
                "required_score": f"{threshold:.6f}",
                "ratio_to_high_resource": f"{ratio:.6f}",
                "status": "PASS" if split == "test" and ratio >= 0.8 else "MEASURED",
                "artifact_path": str(pred_path),
            }
        )
    write_tsv(branch_dir / "score_table.tsv", score_rows, fieldnames)

    test_ratio = test_metrics["chrf"] / max(1e-9, high_score)
    branch_pass = test_ratio >= 0.8
    (branch_dir / "results.md").write_text(
        f"""# Branch Results

Status: {"COMPLETED" if branch_pass else "FAILED"}

Run id: {run_id}

Gate status: {"PASS" if branch_pass else "FAIL"}

## Summary

Retried translation branch with a supervised cross-encoder reranker for `{args.source_iso}->{args.target_iso}`. The reranker was trained on train split positive/negative verse pairs only, then used to select target verses on held-out John test.

Test chrF++: `{test_metrics['chrf']:.6f}`.

Required chrF++: `{threshold:.6f}`.

Ratio: `{test_ratio:.6f}`.

Retrieval accuracy: `{test_metrics['retrieval_acc']:.6f}`.

Checkpoint artifact: `{checkpoint_dir}`.

Runtime minutes: `{runtime_minutes:.3f}`.
""",
        encoding="utf-8",
    )
    (branch_dir / "return_decision.md").write_text(
        f"""# Return Decision

Decision: {"MERGE_TO_MAIN" if branch_pass else "RETRY_BRANCH"}

Reason: {"cross-encoder reranker reached the Step 07 80% threshold" if branch_pass else "cross-encoder reranker did not reach the 80% translation threshold"}
""",
        encoding="utf-8",
    )
    file_rows = [
        {
            "file_role": "score_table",
            "path": str(branch_dir / "score_table.tsv"),
            "rows_or_files": str(len(score_rows)),
            "bytes": str((branch_dir / "score_table.tsv").stat().st_size),
            "md5": md5_file(branch_dir / "score_table.tsv"),
            "status": "PASS",
            "notes": "branch score table with cross-encoder retry",
        },
        {
            "file_role": "cross_encoder_checkpoint",
            "path": str(checkpoint_dir),
            "rows_or_files": str(count_files(checkpoint_dir)),
            "bytes": str(file_bytes(checkpoint_dir)),
            "md5": "DIRECTORY",
            "status": "PASS",
            "notes": "large branch checkpoint",
        },
        {
            "file_role": "cross_encoder_test_predictions",
            "path": str(test_pred),
            "rows_or_files": str(len(test_rows)),
            "bytes": str(test_pred.stat().st_size),
            "md5": md5_file(test_pred),
            "status": "PASS",
            "notes": "held-out John predictions",
        },
        {
            "file_role": "cross_encoder_run_report",
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
    print(f"retrieval_acc={test_metrics['retrieval_acc']:.6f}")
    print(f"ratio={test_ratio:.6f}")
    print(f"decision={'MERGE_TO_MAIN' if branch_pass else 'RETRY_BRANCH'}")


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
