# v5 Reproducibility Appendix

Last updated: 2026-06-27 05:25 KST

This appendix records the minimum information needed to reproduce or audit the
v5 report and presentation. It is written for the final paper package, while
the live operational queue remains in `../../3_evaluation/`.

## Scope Lock

Allowed scope:

```text
92 XLM-R-seen Glot500 language-scripts + 10 Glot500-internal target
language-scripts.
```

Disallowed scope:

```text
full 511-language Glot500 reproduction.
```

Target10:

```text
fur_Latn
krc_Cyrl
acm_Arab
dzo_Tibt
sat_Olck
mad_Latn
bam_Latn
kjb_Latn
quw_Latn
rap_Latn
```

## Canonical Local Roots

| Item | Path |
| --- | --- |
| repository | `/home/axt/jongha/Glot500-py39-eval` |
| v5 workspace | `/home/axt/mnt2/jongha/v5_glot50010` |
| raw symlink root | `/home/axt/mnt2/jongha/v5_glot50010/raw` |
| merged corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt` |
| tokenizer | `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm` |
| initialized models | `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/` |
| MLM runs | `/home/axt/mnt2/jongha/v5_glot50010/runs/` |
| evaluation outputs | `/home/axt/mnt2/jongha/v5_glot50010/evaluation/` |

## Core Evidence Artifacts

| Stage | Evidence |
| --- | --- |
| data scope | `../../0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| merge | `../../0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json` |
| tokenizer audit | `../../0_tokenizer/03_audit/README.md` and tokenizer audit tables |
| initialization audit | `../../1_embedding/05_audit/README.md` |
| zero-step eval | `../../1_embedding/04_zero_step_eval/README.md` |
| training status | `../../2_training/README.md` |
| checkpoint selection | `../../2_training/05_checkpoint_selection/selection_plan.md`; `../../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` |
| coverage | `../../3_evaluation/00_coverage/coverage_summary.tsv` |
| metric completion | `../../3_evaluation/09_aggregation/metric_completion.tsv` |
| normalized result rows | `../../3_evaluation/09_aggregation/main_head_tail_all.tsv` |
| report tables | `../00_tables/` |
| reproduction fidelity matrix | `../00_tables/table_15_glot500_reproduction_fidelity.md` |
| generated figures | `../01_figures/generated/figure_manifest.tsv` |
| bibliography | `references.bib` |

## Canonical Commands

Merge:

```bash
python3 preprocessing/merge_files.py \
  --data_directory /home/axt/mnt2/jongha/v5_glot50010/raw \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/data \
  --experiment_name Glot500_v5_glot50010_xlmr100 \
  --stats_csv docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv \
  --manifest_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv \
  --report_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json \
  --missing_policy fail
```

Tokenizer:

```bash
python3 tokenization/run.py \
  --input_fname /home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt \
  --model_name xlm-roberta-base \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/tokenization/output \
  --vocab_size 250000
```

Paired MLM launch:

```bash
setsid bash -c 'cd /home/axt/jongha/Glot500-py39-eval && bash modeling/launch_v5_random_fvt_10k.sh' \
  > /home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs/launch_random_fvt_10k_setsid_20260627_005616.log \
  2>&1 < /dev/null &
```

Metric wrapper pattern:

```bash
bash scripts/run_v5_eval_metric.sh <metric_id> <model_key> <gpu_id>
```

Paired post-checkpoint wrapper:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

Split phase form:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

The launch environment, output/log targets, and promotion rule are generated in:

```text
3_evaluation/post_checkpoint_execution_plan.md
```

The paired wrapper first checks that both `v5_random` and `v5_fvt` are
`ready_for_wrapper=yes` in the generated model matrix and that
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`.
It then runs the matched random/FVT rows and refreshes reporting after each
metric family.

Examples:

```bash
bash scripts/run_v5_eval_metric.sh pppl xlmr_base 0
bash scripts/run_v5_eval_metric.sh retrieval_tatoeba glot500_base 1
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner glot500_base 0
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos glot500_base 1
```

Refresh after any new result:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

## Model Keys

| Key | Meaning | Current role |
| --- | --- | --- |
| `xlmr_base` | `xlm-roberta-base` | no-adaptation baseline |
| `glot500_base` | `cis-lmu/glot500-base` | external reference, not equal-budget baseline |
| `v5_random` | XLM-R + v5 tokenizer + random new rows | equal-budget random baseline |
| `v5_fvt` | XLM-R + v5 tokenizer + source-token decomposition rows | main novelty candidate |

## Required Metric Families

| Metric | Required handling |
| --- | --- |
| PPPL | measure for all ready models; target10 has 10/10 raw coverage |
| Tatoeba retrieval | measure available local languages; report target10 0/10 coverage |
| Bible retrieval | local parallel data materialized for 74/102; XLM-R/Glot500-base and v5_random diagnostic rows measured; run v5_fvt after checkpoint and post-checkpoint preflight; keep target10 0/10 caveat |
| Text classification | measure local Taxi1500 split; report English-only coverage |
| NER | measure available tagging languages; keep target coverage caveat |
| POS | measure available tagging languages; preserve `TRAIN_LANGS=tur_Latn` note |
| Roundtrip alignment | XLM-R/Glot500-base and v5_random diagnostic rows measured over 74/102; run v5_fvt after checkpoint and post-checkpoint preflight; target10 remains 0/10 |

## Result Promotion Rule

Only these may enter final result tables:

- audited artifacts such as merge/tokenizer/init reports,
- non-empty completed metric outputs parsed by `scripts/aggregate_v5_metrics.py`,
- blocked-data rows with explicit blocker and claim impact.

These must not enter final result tables:

- current training step,
- tagging dev F1 during training,
- partially written output files,
- target10 downstream rows inferred from missing data.

The detailed insertion map is in:

```text
../result_insertion_matrix.md
```

## Current Known Deviations

| Deviation | Handling |
| --- | --- |
| v5 is 102 language-scripts, not 511 | state as controlled Glot500-style subset replay |
| `dzo_Tibt` tokenizer fertility worsens | keep as visible tokenizer regression |
| PPPL target10 coverage is 10/10, retained downstream target10 coverage is 0/10 | separate target intrinsic claims from available-language downstream claims |
| POS lacks local `train-eng_Latn.tsv` | train with `TRAIN_LANGS=tur_Latn` and report the note |
| Glot500-base has different original training budget | treat as external reference only |

Current POS reference evidence:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/xlmr_base/xlm-roberta-base/test_results.txt
/home/axt/mnt2/jongha/v5_glot50010/evaluation/pos/glot500_base/glot500-base/test_results.txt
```

Both files are parsed by `scripts/aggregate_v5_metrics.py`; the resulting POS
rows must keep the `TRAIN_LANGS=tur_Latn` note.
