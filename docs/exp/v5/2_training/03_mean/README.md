# 03 Mean Training

MLM training run for the mean initialization ablation. Run after random/fvt
unless compute allows all methods in parallel.

## Next Step Gate

This ablation is eligible for `../05_checkpoint_selection/` only when it follows
the same training contract as `v5_random` and `v5_fvt`.

Pass line:

- run config matches the main runs.
- checkpoint-wise MLM proxy is computed.
- stop reason is documented if the run is incomplete.
- result role is labeled as ablation, not main claim.

Required artifacts:

- launch command
- train log or skip note
- checkpoint list when run
- checkpoint-wise MLM proxy table when run

If skipped, write a short compute or priority reason here so the report can be
honest about the method matrix.
