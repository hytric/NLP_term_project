# 01 Random Training

MLM training run for the random-resize baseline.

Expected artifacts:

- launch command
- checkpoint paths
- train log path
- checkpoint-wise MLM proxy summary

Current 10K run:

- run name: `v5_random_mlm_10k`
- init model:
  `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_random`
- tokenizer:
  `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- train file:
  `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt`
- output dir:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k`
- log:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/logs/train_v5_v5_random_mlm_10k_20260627_005616.log`
- GPUs: `2,3`
- max steps: `10000`
- save steps: `10000`
- status: launched; Trainer optimization has started
- observed progress: tokenizer map reached `100%` in the active log on
  2026-06-27; grouping/cache materialization completed far enough for
  `***** Running training *****` to appear
- Trainer setup:
  - train examples after grouping: `6,893,482`
  - total train batch size: `384`
  - total optimization steps: `10,000`
  - trainable parameters: `369,563,951`
- checkpoint status: no checkpoint has been written yet

Execution note:

The run has passed the full-corpus preprocessing barrier and is now in the
actual training stage. Keep monitoring the active log for step/loss entries and
checkpoint creation.

## Next Step Gate

This run is eligible for `../05_checkpoint_selection/` only after it becomes a
fair baseline for `../02_fvt/`.

Pass line:

- data path, tokenizer path, seed, batch/effective batch, learning rate, max
  length, and checkpoint interval are recorded.
- training reaches the planned step budget or has a documented stop reason.
- checkpoint-wise MLM proxy is computed.
- training curve is saved or summarized.
- command and logs are enough to reproduce the run.

Required artifacts:

- launch command
- train log
- checkpoint list
- checkpoint-wise MLM proxy table
- run config note

If `v5_random` is missing, no final novelty claim can compare embedding
initialization methods.
