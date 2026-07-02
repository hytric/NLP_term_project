# 02 FVT Training

MLM training run for the main proposed `fvt` initialization.

Compare directly against `../01_random/` with identical data, schedule, seed,
and checkpoint intervals.

Current paired 10K run:

- run name: `v5_fvt_mlm_10k`
- init model:
  `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_fvt`
- tokenizer:
  `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- train file:
  `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt`
- output dir:
  `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k`
- GPUs: `2,3`
- max steps: `10000`
- save steps: `10000`
- status: queued after `v5_random_mlm_10k` in
  `modeling/launch_v5_random_fvt_10k.sh`

## Next Step Gate

This run is eligible for `../05_checkpoint_selection/` only after it is directly
comparable with `../01_random/`.

Pass line:

- data path, tokenizer path, seed, batch/effective batch, learning rate, max
  length, and checkpoint interval match `v5_random`.
- only the initialization method differs from `v5_random`, unless a difference
  is explicitly justified.
- training reaches the planned step budget or has a documented stop reason.
- checkpoint-wise MLM proxy is computed.
- training curve is saved or summarized.

Required artifacts:

- launch command
- train log
- checkpoint list
- checkpoint-wise MLM proxy table
- run config diff against `v5_random`

If this run is not comparable to `v5_random`, report it as exploratory and do
not use it for the main initialization claim.
