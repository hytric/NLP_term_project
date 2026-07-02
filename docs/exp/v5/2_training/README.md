# v5 MLM Training

This stage stores pilot and method-specific MLM training records.

Subfolders:

- `00_pilot/`: smoke tests and small-budget runs
- `01_random/`: random initialization baseline training
- `02_fvt/`: main proposed initialization training
- `03_mean/`: mean initialization ablation
- `04_align/`: align initialization ablation
- `05_checkpoint_selection/`: checkpoint choice for downstream evaluation

All method-specific runs should share the same data, schedule, seed, and
checkpoint interval whenever possible.

Canonical commands:

```bash
INIT_MODEL_DIR=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_random \
  RUN_NAME=v5_random_mlm \
  bash modeling/train_v5_glot50010_mlm.sh

INIT_MODEL_DIR=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_fvt \
  RUN_NAME=v5_fvt_mlm \
  bash modeling/train_v5_glot50010_mlm.sh
```

Current paired 10K launch:

```bash
setsid bash -c 'cd /home/axt/jongha/Glot500-py39-eval && bash modeling/launch_v5_random_fvt_10k.sh' \
  > /home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs/launch_random_fvt_10k_setsid_20260627_005616.log \
  2>&1 < /dev/null &
```

Launch status:

- launcher PID: `1868654`
- GPUs: `CUDA_VISIBLE_DEVICES=2,3`
- run order: `v5_random_mlm_10k` then `v5_fvt_mlm_10k`
- max steps: `10000`
- save steps: `10000`
- cache dir: `/home/axt/mnt2/jongha/v5_glot50010/cache_mlm10k`
- random train log:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log`
- output root:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/`

This is a detached run. Check status with:

```bash
pgrep -af 'modeling/run.py|launch_v5_random_fvt_10k'
nvidia-smi
tail -n 80 /home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log
```

Current bottleneck note:

The active `v5_random_mlm_10k` run spent a long time in HuggingFace datasets
tokenization/materialization because the inherited `modeling/run.py` tokenizes
and groups the full `92,452,251`-line corpus before Trainer starts stepping.
This preprocessing stage completed far enough for Trainer to start. The log now
contains:

```text
***** Running training *****
Num examples = 6893482
Total train batch size (w. parallel, distributed & accumulation) = 384
Total optimization steps = 10000
```

`--max_steps 10000` limits optimization steps, but does not skip full
preprocessing. Report this as an execution cost of faithful full-corpus replay.
If a faster early-step diagnostic is needed, create a separately labeled
sampled-corpus run and keep it out of the main full-corpus claim.

Parity guard:

```text
training_parity_audit.md
```

This generated audit must stay ready before any `v5_fvt` versus `v5_random`
after-MLM or downstream claim is promoted. It checks that the two main methods
share corpus, tokenizer, schedule, checkpoint rule, and downstream eligibility.

Live progress guard:

```text
mlm_progress_eta.md
mlm_progress_eta.tsv
training_loss_snapshot.md
training_loss_snapshot.tsv
live_training_health.md
live_training_health.tsv
storage_readiness.md
storage_readiness.tsv
paired_launcher_transition.md
paired_launcher_transition.tsv
```

These generated files summarize the active paired 10K run, ETA, source logs,
Trainer-log loss rows, process/GPU health, critical log-pattern scan, and the
`ready_for_wrapper` handoff line, plus storage/path readiness for checkpoint
saves and queued FVT launch. `training_loss_snapshot.md` is the training-curve
snapshot required for operational handoff, but it is not PPPL/downstream
evidence. `paired_launcher_transition.md` additionally checks that the detached
launcher still has the expected random-then-FVT ordering: while random is
running, FVT should be waiting; after random writes the selected checkpoint, FVT
should start from the same paired launcher. They are operational status evidence
only, not final model-quality metrics.

## Stage Exit Line

Move to `../3_evaluation/` only after all of the following are true:

- `00_pilot/` passes a short run without tokenizer/model/data errors.
- `01_random/` and `02_fvt/` have comparable training runs under the same data,
  seed, schedule, and checkpoint interval.
- failed or skipped `03_mean/` and `04_align/` runs have explicit reasons.
- `05_checkpoint_selection/` records the checkpoint chosen for each model.
- training curves and checkpoint-wise MLM proxy summaries are available.

Minimum artifact line:

```text
pilot pass + random/fvt comparable checkpoints + checkpoint selection written
```

If this line is not met, downstream evaluation can run for debugging but should
not be used in the final result table.
