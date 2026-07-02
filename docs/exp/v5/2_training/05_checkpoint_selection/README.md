# 05 Checkpoint Selection

Use this folder to choose which checkpoints go into downstream evaluation.

Current selection plan:

- `selection_plan.md`
- generated selected-checkpoint manifest:
  `selected_checkpoint_manifest.md` and `selected_checkpoint_manifest.tsv`

Selection should consider:

- tail MLM proxy
- head control metric
- v5-target subset metric
- checkpoint stability
- training cost

## Next Step Gate

Move to `../../3_evaluation/` only after the downstream checkpoint set is
frozen.

Pass line:

- selected checkpoint for each required model is written:
  `xlmr_base`, `glot500_base`, `v5_random`, `v5_fvt`.
- optional `v5_mean` and `v5_align` inclusion/exclusion is documented.
- selection criterion is fixed before downstream results are inspected.
- checkpoint paths and tokenizer paths are recorded.
- head/tail/all MLM proxy at selected checkpoints is summarized.

Required artifacts:

- checkpoint selection table
- model path list
- tokenizer path list
- selection rationale
- frozen downstream model matrix
- generated selected-checkpoint manifest

Model path rule:

- Prefer the root-level final Trainer directory when it contains
  `pytorch_model.bin` or `model.safetensors`.
- If the root directory has not been finalized but the fixed matched
  `checkpoint-10000` directory contains a model file, use `checkpoint-10000`.
- Do not use an earlier checkpoint for the main random/FVT comparison unless
  the run is explicitly downgraded to incomplete or exploratory.

If checkpoint selection changes after downstream evaluation starts, document the
reason and rerun affected metrics.

Regenerate the manifest with:

```bash
python3 scripts/write_v5_eval_model_matrix.py
python3 scripts/write_v5_checkpoint_selection_manifest.py
```

The canonical reporting refresh command also regenerates it:

```bash
python3 scripts/refresh_v5_reporting.py
```
