# 04 Align Training

MLM training run for the align initialization ablation. Treat as exploratory
unless zero-step eval strongly supports it.

## Next Step Gate

This exploratory run is eligible for `../05_checkpoint_selection/` only if its
motivation and setup are clear.

Pass line:

- zero-step or audit evidence motivating `align` is recorded.
- run config matches the main runs unless explicitly justified.
- checkpoint-wise MLM proxy is computed.
- result role is labeled as exploratory or ablation.

Required artifacts:

- motivation note
- launch command or skip note
- train log when run
- checkpoint-wise MLM proxy table when run

If the align rule is weakly motivated, skip full training and keep the method in
the analysis section as future work or ablation design.
