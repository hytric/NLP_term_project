# Reproduction Commands

작성일: 2026-06-19

Run from repository root:

```bash
cd /home/axt/jongha/Glot500-py39-eval
```

## Pseudoperplexity

GPU 0 run:

```bash
CUDA_VISIBLE_DEVICES=0 python3 docs/exp/v3.1/05_additional/code/run_v31_pseudoperplexity.py \
  --device cuda \
  --output-dir docs/exp/v3.1/05_additional \
  --output-prefix pseudoperplexity_gpu0 \
  --max-examples-per-lang 50 \
  --max-length 128 \
  --mask-batch-size 64 \
  --model-keys xlmr_base fvt_mlm200 focus_mlm200
```

GPU 3 run:

```bash
CUDA_VISIBLE_DEVICES=3 python3 docs/exp/v3.1/05_additional/code/run_v31_pseudoperplexity.py \
  --device cuda \
  --output-dir docs/exp/v3.1/05_additional \
  --output-prefix pseudoperplexity_gpu3 \
  --max-examples-per-lang 50 \
  --max-length 128 \
  --mask-batch-size 64 \
  --model-keys random_mlm200 mean_mlm200 align_mlm200
```

Merge the two outputs:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

base = Path("docs/exp/v3.1/05_additional")
pairs = [
    ([base / "pseudoperplexity_gpu0_scores.tsv", base / "pseudoperplexity_gpu3_scores.tsv"], "pseudoperplexity_scores.tsv"),
    ([base / "pseudoperplexity_gpu0_summary.tsv", base / "pseudoperplexity_gpu3_summary.tsv"], "pseudoperplexity_summary.tsv"),
]

for files, out_name in pairs:
    rows = []
    fields = None
    for path in files:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if fields is None:
                fields = reader.fieldnames
            rows.extend(reader)
    rows.sort(key=lambda row: (row.get("model_key", ""), row.get("language_id", "")))
    with (base / out_name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
PY
```

## Pseudoperplexity Top-K / Content-Token Diagnostic

```bash
CUDA_VISIBLE_DEVICES=0 python3 docs/exp/v3.1/05_additional/code/run_v31_pseudoperplexity_accuracy_samples.py \
  --device cuda \
  --output-dir docs/exp/v3.1/05_additional \
  --max-examples-per-lang 20 \
  --max-length 128 \
  --mask-batch-size 64 \
  --sample-limit-per-lang 5
```

## Target10 Sentence Retrieval With CSLS

```bash
python3 docs/exp/v3.1/05_additional/code/run_v31_target10_csls_feature_similarity.py \
  --output-dir docs/exp/v3.1/05_additional
```

## Coptic POS Re-Aggregation

```bash
python3 preprocessing/evaluate_third_try_coptic_pos_metrics.py \
  --data-dir /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos \
  --run-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200 \
  --doc-dir docs/exp/v3.1/05_additional \
  --split test \
  --requested-max-steps 200 \
  --downstream-seed 13 \
  --model xlmr_base=baseline=NA=xlm-roberta-base \
  --model fvt_replay_safe_seed13=fvt_replay_safe=13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed13_step1000 \
  --model fvt_replay_safe_seed17=fvt_replay_safe=17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed17_step1000 \
  --model fvt_replay_safe_seed23=fvt_replay_safe=23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed23_step1000 \
  --result-name coptic_pos_results_replay_safe.tsv \
  --summary-name coptic_pos_summary_replay_safe.tsv \
  --label-metrics-name coptic_pos_label_metrics_replay_safe.tsv
```

## Validation

```bash
python3 -m py_compile \
  docs/exp/v3.1/05_additional/code/run_v31_pseudoperplexity.py \
  docs/exp/v3.1/05_additional/code/run_v31_pseudoperplexity_accuracy_samples.py \
  docs/exp/v3.1/05_additional/code/run_v31_target10_csls_feature_similarity.py

test -s docs/exp/v3.1/05_additional/pseudoperplexity_summary.tsv
test -s docs/exp/v3.1/05_additional/pseudoperplexity_accuracy_summary.tsv
test -s docs/exp/v3.1/05_additional/pseudoperplexity_gold_probability_scores.tsv
test -s docs/exp/v3.1/05_additional/pseudoperplexity_prediction_samples.tsv
test -s docs/exp/v3.1/05_additional/target10_sentence_retrieval_csls_summary.tsv
test -s docs/exp/v3.1/05_additional/target10_sentence_retrieval_csls_summary_mlm200_only.tsv
test -s docs/exp/v3.1/05_additional/coptic_pos_summary_replay_safe.tsv
test -s docs/exp/v3.1/05_additional/method_task_results.md
```
