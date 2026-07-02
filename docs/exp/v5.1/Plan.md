# v5.1 Plan

작성일: 2026-06-28

## Objective

Re-run the v5 Glot500-style pipeline with a downstream-aware target10 so that
the experiment can report target-subset evidence beyond PPPL/MLM proxy and
measure PPPL on a Glot500-style held-out test set.

Current recommended first run:

```text
DATA_FRACTION=5%
SCALE=1.5
MAX_STEPS=3000 first, then 10000 if time allows
GPU=up to 4x A6000
EFFECTIVE_BATCH=384
```

Current execution state:

```text
MLM_3K_STATUS=running_random_first
FINAL_EXPERIMENT_LINE=v5.1
V5_USAGE=diagnostic / fallback / ablation
EVAL_DATA_READY=yes
```

Decision boundary:

```text
v5 train-source PPPL is not a final Glot500-style PPPL result.
v5.1 held-out test PPPL is the required final PPPL line.
```

## Selection Rule

The v5.1 target set is selected from Glot500 raw languages satisfying:

1. not marked as XLM-R seen;
2. local Glot500 raw directory exists;
3. `new_length >= 30000`;
4. prefer overlap with local downstream resources;
5. keep at least two script-diversity anchors.

## Target10

```text
guj_Gujr
asm_Beng
srp_Cyrl
sun_Latn
zsm_Latn
aze_Latn
fil_Latn
bos_Latn
dzo_Tibt
sat_Olck
```

## Execution Stages

### -1. Deterministic Held-Out Split

Status: done.

Rule:

```text
For each language-script, reserve dev=1000 and test=1000 before tokenizer
training and MLM merge. Use only train for merge/tokenizer/continued MLM.
```

Exit line:

```text
every selected language has split_manifest rows for train/dev/test; train-only
merge input excludes dev/test; PPPL examples come from held-out test
```

Current planning artifacts:

```text
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_manifest.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl
```

Status note: current split manifest is stats-based planning output
is preserved as `strict_split_manifest.stats_plan.tsv`. The default
`strict_split_manifest.tsv` and `strict_split_indices.jsonl` are now
Arrow-verified with status `PASS`. Three small seen languages use
`small_policy=shrink`.

### 0. Data Scope

Status: done.

Outputs:

```text
docs/exp/v5.1/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv
docs/exp/v5.1/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.md
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_verification_summary.md
/home/axt/mnt2/jongha/v5_1_glot50010/raw
```

Exit line:

```text
raw symlink count = 102 and merge dry-run missing_language_dirs = 0
strict data composition table records train/dev/test, XLM-R status, and task overlap
```

### 1. Full Merge

Status: done for first strict 5% run.

Command:

```bash
DOCS_EXP_ROOT=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1 \
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100_strict_5pct \
SCALE=1.5 \
SPLIT=train \
SPLIT_INDICES_PATH=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl \
bash preprocessing/run_v5_glot50010_merge.sh
```

Expected output:

```text
/home/axt/mnt2/jongha/v5_1_glot50010/data/Glot500_v51_glot50010_xlmr100_strict_5pct.txt
```

Exit line:

```text
merge report status PASS and actual_total_samples matches train-only split plan
```

Current evidence:

```text
status = PASS
actual_total_samples = 8,130,401
wc -l = 8,130,401
size = 1.7G
```

### 2. Tokenizer

Status: done for first strict 5% run.

Command:

```bash
DOCS_EXP_ROOT=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1 \
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100 \
bash tokenization/train_v5_glot50010.sh
```

Exit line:

```text
extended tokenizer exists and tokenizer audit has failures = 0
```

Current evidence:

```text
tokenizer_dir = /home/axt/mnt2/jongha/v5_1_glot50010/tokenization/output_strict_5pct/Glot500_extended_spm
target_vocab_size = 370,051
novel_tokens = 120,049
audit_failures = 0
base_mask_id = 250,001
target_mask_id = 370,050
```

### 3. Embedding Initialization

Status: done for first strict 5% run.

Command:

```bash
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
bash scripts/run_v5_build_initializers.sh
```

Minimum methods:

```text
v5_random
v5_fvt
```

Exit line:

```text
random and fvt init reports pass mask remap and LM-head tie checks
```

Current evidence:

```text
random_dir = /home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct/v5_random
fvt_dir = /home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct/v5_fvt
mask_max_abs_diff_after_copy = 0.0
lm_head_tied_after_init = true
```

### 4. MLM Training

Status: running for first strict 5% run. The launcher is running the matched
pair sequentially, with `random` first and `FVT` next.

Command:

```bash
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100_strict_5pct \
CUDA_VISIBLE_DEVICES=0,1,2,3 \
NPROC_PER_NODE=4 \
PER_DEVICE_TRAIN_BATCH_SIZE=8 \
GRADIENT_ACCUMULATION_STEPS=12 \
EXTRA_ARGS="--max_steps 3000 --save_steps 3000 --save_total_limit 2 --logging_steps 100" \
bash modeling/launch_v5_random_fvt_10k.sh
```

Exit line:

```text
v5_random and v5_fvt both finish at checkpoint-3000 for the first strict line
```

Current evidence:

```text
launcher_pid = 2985609
current_run = v51_strict5pct_random_mlm_3k
gpus = 0,1,3
effective_batch = 384
max_steps = 3000
train_log = /home/axt/mnt2/jongha/v5_1_glot50010/runs/logs/train_v5_v51_strict5pct_random_mlm_3k_20260628_182508.log
```

### 5. Evaluation

Status: data/wrappers ready, waiting for `v51_random` and `v51_fvt`
checkpoints.

Required:

```text
held-out PPPL / MLM proxy
Tatoeba retrieval
Bible retrieval
Roundtrip alignment
NER
POS
Taxi1500
```

Target-subset claim is allowed only for metrics with target coverage.
PPPL claim is allowed as Glot500-style only if `PPPL_SPLIT=test` and
`PPPL_EVAL_ROLE=heldout_test` are recorded in `run_meta.tsv`.

Current coverage:

```text
PPPL                 total=102 head=92 target10=10
Tatoeba retrieval    total=66  head=63 target10=3
Bible retrieval      total=80  head=74 target10=6
Text classification  total=1   head=1  target10=0
NER                  total=84  head=78 target10=6
POS                  total=58  head=58 target10=0
Roundtrip alignment  total=80  head=74 target10=6
```

Post-checkpoint commands:

```bash
bash scripts/run_v51_post_checkpoint_evals.sh status
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh pppl
GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh downstream
```

Evidence:

```text
docs/exp/v5.1/3_evaluation/README.md
docs/exp/v5.1/3_evaluation/POST_CHECKPOINT_EVAL_RUNBOOK_KO.md
docs/exp/v5.1/3_evaluation/00_coverage/coverage_summary.tsv
docs/exp/v5.1/3_evaluation/03_retrieval_bible/materialization_summary.tsv
docs/exp/v5.1/3_evaluation/07_roundtrip_alignment/materialization_summary.tsv
```

## Runtime Warning

v5.1 full rerun will not finish by the 2026-06-29 morning deadline if started
from scratch. Use current v5 as the main genuine low-resource experiment and
v5.1 as the downstream-aware diagnostic/ablation line.
