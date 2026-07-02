# Reproducibility Checklist

작성일: 2026-06-04

## Repository Start

Before any run:

```bash
cd /home/axt/jongha/Glot500-py39-eval
git pull --ff-only
```

Current pull status checked on 2026-06-04:

- already up to date.

## Storage Layout

Large local artifacts are stored on `/disk1`; repository paths remain usable through symlinks.

| Repo path | Real location |
| --- | --- |
| `data` | `/disk1/axt/jongha/Glot500-py39-eval/data` |
| `download` | `/disk1/axt/jongha/Glot500-py39-eval/download` |
| `docs/exp/2026-06-03_05_mlm_adaptation` | `/disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_05_mlm_adaptation` |
| `docs/exp/2026-06-03_06_nmt_baselines` | `/disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_06_nmt_baselines` |

Check with:

```bash
readlink -f data download docs/exp/2026-06-03_05_mlm_adaptation docs/exp/2026-06-03_06_nmt_baselines
df -h . /disk1
```

## GPU Policy

Use only physical GPU 3, `NVIDIA RTX A6000`.

Before GPU experiments:

```bash
source scripts/gpu3_env.sh
```

This sets:

```bash
CUDA_VISIBLE_DEVICES=3
TOKENIZERS_PARALLELISM=false
```

Inside Python/Torch, physical GPU 3 appears as `cuda:0`.

Check with:

```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader
```

## Documentation Location

Experiment documentation lives in:

```text
docs/exp/
```

Folder rule:

```text
YYYY-MM-DD_NN_short_slug/
  plan.md
  results.md       # when results exist
  metrics.*        # when tabular metrics exist
```

Current ordered stages:

- `00_final_goal`
- `01_data_and_splits`
- `02_tokenization_audit`
- `03_vocab_extension`
- `04_embedding_init`
- `05_mlm_adaptation`
- `06_nmt_baselines`
- `07_pivot_backtranslation`
- `08_evaluation_analysis`
- `09_report_release`
- `10_source_grounding_editing`
- `11_release_audit`

## Main Evidence Files

| Claim | Evidence |
| --- | --- |
| target10 set and data split | `docs/exp/2026-06-03_01_data_and_splits/results.md` |
| tokenizer bottleneck | `docs/exp/2026-06-03_02_tokenization_audit/results.md` |
| target10 tokenizer merge | `docs/exp/2026-06-03_03_vocab_extension/results.md` |
| embedding initialization | `docs/exp/2026-06-03_04_embedding_init/results.md` |
| MLM checkpoint selection | `docs/exp/2026-06-03_05_mlm_adaptation/results.md` |
| NMT/retrieval baselines | `docs/exp/2026-06-03_06_nmt_baselines/results.md` |
| pivot/back-translation gate | `docs/exp/2026-06-03_07_pivot_backtranslation/results.md` |
| final metric table | `docs/exp/2026-06-03_08_evaluation_analysis/final_metrics.tsv` |
| qualitative/error analysis | `docs/exp/2026-06-03_08_evaluation_analysis/qualitative_analysis.md`, `docs/exp/2026-06-03_08_evaluation_analysis/error_taxonomy.md` |
| source-grounding/editing gate | `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_results.tsv`, `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_controls.md` |
| release/storage/license audit | `docs/exp/2026-06-04_11_release_audit/release_audit_summary.md`, `docs/exp/2026-06-04_11_release_audit/artifact_inventory.tsv` |

## Large-File Discipline

When running diagnostic GPU experiments:

- prefer `--skip_save_model` unless a checkpoint is explicitly needed;
- write metrics and predictions under `docs/exp/...`;
- keep large model/data artifacts on `/disk1`;
- check `df -h . /disk1` after long runs.

## Minimal Rerun Order

If rebuilding from prepared local artifacts:

1. Verify symlinks and disk state.
2. Verify GPU policy.
3. Read `docs/exp/README.md`.
4. Re-run only the needed stage, not the entire pipeline.

For a new GPU run, use this pattern:

```bash
source scripts/gpu3_env.sh
python3 <script> ... --output_dir docs/exp/<stage>/<run_name> --report_to none --skip_save_model
```
