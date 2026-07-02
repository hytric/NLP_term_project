# 00 Pilot

Use this folder for small runs before full training.

Recommended pilot knobs:

- `--max_samples_per_language`
- reduced scale
- 1K-2K MLM steps
- one GPU smoke test

## Next Step Gate

Move to method-specific training folders only after the pilot proves the
pipeline is stable.

Pass line:

- training starts from a v5 initialized checkpoint and v5 tokenizer.
- data loading, masking, forward/backward, checkpoint save, and resume all work.
- loss is finite throughout the pilot.
- GPU memory and wall-time estimates are recorded.
- at least one pilot checkpoint can be loaded for MLM proxy evaluation.

Required artifacts:

- launch command
- environment note
- train log
- checkpoint path
- short pilot summary

If the pilot fails, do not launch full random/fvt runs. Fix the failing stage and
rerun the pilot.
