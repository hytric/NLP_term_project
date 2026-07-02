# v5 Evaluation Execution Queue

Last updated: 2026-06-27 10:22 KST

This file is the operational queue for completing the Glot500-required
evaluation stage. It keeps final metric execution separate from draft reporting
so the report and slides only use measured artifacts.

Live progress snapshots are recorded in `running_status.md`; do not promote
those running counts to final claims until the metric-specific result gate is
crossed.

Immediate post-job commands and launch order are recorded in
`next_runbook.md`.

## Current Running Jobs

| Job | Status | Evidence | Action |
| --- | --- | --- | --- |
| `v5_random_mlm_10k` | running | `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log` | wait for checkpoint, then allow paired launcher to start `v5_fvt` |

## Recently Completed Or Unblocked

| Job | Status | Evidence | Action |
| --- | --- | --- | --- |
| baseline PPPL `xlmr_base` | measured | `docs/exp/v5/3_evaluation/01_pseudoperplexity/xlmr_base/summary.tsv`; aggregation lists `xlmr_base` as measured for PPPL | keep as baseline row; refresh aggregation after new PPPL runs |
| baseline PPPL `glot500_base` | measured | `docs/exp/v5/3_evaluation/01_pseudoperplexity/glot500_base/summary.tsv`; aggregation lists `glot500_base` as measured for PPPL | keep as external reference row; v5 rows still wait for checkpoints |
| Tatoeba retrieval `xlmr_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/xlmr_base/xlm-roberta-base/test_results.txt`; aggregation lists `xlmr_base` as measured for Tatoeba | keep as baseline row; run remaining models when their paths are ready |
| Tatoeba retrieval `glot500_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/retrieval_tatoeba/glot500_base/cis-lmu__glot500-base/test_results.txt`; aggregation lists `glot500_base` as measured for Tatoeba | keep as external reference row; v5 rows still wait for checkpoints |
| Taxi1500 text classification `xlmr_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/xlmr_base/summary.json`; aggregation lists `xlmr_base` as measured for text classification | keep as limited English-only baseline row |
| Taxi1500 text classification `glot500_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/text_classification/taxi1500/glot500_base/summary.json`; aggregation lists `glot500_base` as measured for text classification | keep as limited English-only external-reference row |
| NER `xlmr_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/xlmr_base/xlm-roberta-base/test_results.txt`; aggregation lists `xlmr_base` as measured for NER | keep as baseline row; v5-target actual row is `fur_Latn` only |
| NER `glot500_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/glot500_base/glot500-base/test_results.txt`; aggregation lists `glot500_base` as measured for NER | keep as external reference row; v5-target actual row is `fur_Latn` only |
| POS `xlmr_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/xlmr_base/xlm-roberta-base/test_results.txt`; aggregation lists `xlmr_base` as measured for POS | keep as baseline row; local train language is `tur_Latn` |
| POS `glot500_base` | measured | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/glot500_base/glot500-base/test_results.txt`; aggregation lists `glot500_base` as measured for POS | keep as external reference row; local train language is `tur_Latn` |
| NER materialization | ready | `docs/exp/v5/3_evaluation/00_coverage/coverage_ner.tsv` shows `78/102` local coverage | run NER for baseline/reference models first, then v5 checkpoints after post-checkpoint preflight is ready-to-launch |
| POS materialization | ready | `docs/exp/v5/3_evaluation/00_coverage/coverage_pos.tsv` shows `58/102` local coverage | run POS for baseline/reference models first, then v5 checkpoints after post-checkpoint preflight is ready-to-launch |
| tagging runner fixes | ready | `evaluate_ner.py` and `evaluate_pos.py` now resolve lang lists relative to the script, build output dirs with `os.path.join`, honor `--overwrite_output_dir`, and preprocess `args.train_langs` | use the current runner for NER/POS result jobs |
| PPPL wrapper syntax | ready | `bash -n scripts/run_v5_eval_metric.sh` passes | use current wrapper for `v5_random` and `v5_fvt` after checkpoints exist and post-checkpoint preflight is `post_checkpoint_preflight_ready_to_launch` |
| retrieval lang-list path | ready | `evaluate_retrieval_tatoeba.py` and `evaluate_retrieval_bible.py` now load lang lists relative to their script directory | keep wrapper execution from repo root |
| Bible retrieval materialization | ready | `docs/exp/v5/3_evaluation/03_retrieval_bible/materialization_summary.tsv`; coverage is `74/102`, target10 `0/10` | run `retrieval_bible` for ready baseline/reference models; run v5 rows after checkpoints and post-checkpoint preflight |

## Immediate Queue

1. Use measured PPPL rows for `xlmr_base` and `glot500_base` as the current
   intrinsic baseline/reference rows.
2. Use the measured `xlmr_base` and `glot500_base` Tatoeba rows as the current
   downstream baseline/reference rows while keeping the metric partial until
   the v5 checkpoints are evaluated.
3. Use the measured `xlmr_base` and `glot500_base` Taxi1500 rows as limited
   English-only text-classification baseline/reference rows.
4. After `v5_random` and `v5_fvt` matched checkpoints exist, refresh the model
   matrix, selected checkpoint manifest, queue, and gates:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

5. Run the guarded paired post-checkpoint evaluation wrapper:

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

The `all` mode runs PPPL first, then Tatoeba, Bible, Taxi1500, NER, POS, and
Roundtrip for `v5_random` and `v5_fvt`, refreshing reporting after each metric
family.
For staged execution, run:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

The PPPL wrapper uses an example cache by default:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/cache/
```

This cache should be reused for all models with the same PPPL split and example
selection.

## Downstream Metric Queue

Run every metric for `xlmr_base`, `glot500_base`, `v5_random`, and `v5_fvt`.
If a metric lacks local data, record the blocker rather than silently dropping
the metric.

| Metric | Current data status | Run condition | Command pattern |
| --- | --- | --- | --- |
| PPPL | 102/102 raw coverage | models ready | `bash scripts/run_v5_eval_metric.sh pppl <model_key> <gpu>` |
| Tatoeba retrieval | 63/102 local coverage, target10 0/10 | models ready | `bash scripts/run_v5_eval_metric.sh retrieval_tatoeba <model_key> <gpu>` |
| Bible retrieval | 74/102 local coverage, target10 0/10 | models ready | `bash scripts/run_v5_eval_metric.sh retrieval_bible <model_key> <gpu>` |
| Taxi1500 text classification | 1/102 local coverage | models ready | `bash scripts/run_v5_eval_metric.sh text_classification <model_key> <gpu>` |
| NER | 78/102 local coverage, target10 0/10 | models ready | `bash scripts/run_v5_eval_metric.sh ner <model_key> <gpu>` |
| POS | 58/102 local coverage, target10 0/10; local data lacks `train-eng_Latn.tsv` | models ready with explicit train-language note | `TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos <model_key> <gpu>` |
| Roundtrip alignment | 74/102 local coverage, target10 0/10; XLM-R/Glot500-base and v5_random diagnostic rows measured | v5_fvt waits for matched checkpoint | `bash scripts/run_v5_eval_metric.sh roundtrip_alignment <model_key> <gpu>` |

## Refresh Commands

Run these after any data materialization, model checkpoint, or metric output
changes:

```bash
python3 scripts/audit_v5_eval_coverage.py
python3 scripts/refresh_v5_reporting.py --with-plots
```

## Reporting Rule

- A metric row becomes a final result only when `09_aggregation/` sees measured
  outputs for the required model set.
- A metric may still appear in the final report as blocked if its data or runner
  is unavailable, but the blocker and affected claim must be explicit.
- Target10 downstream improvement is not a supported claim until partial official
  target task membership is materialized and evaluated correctly.
