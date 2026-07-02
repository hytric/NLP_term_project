# 01 Figures

Use this folder for plots, diagrams, and embedding maps.

## Next Step Gate

Move figures into `../02_slides/` and `../03_final_report/` only after the figure
source is reproducible.

Pass line:

- every figure has source data path and plot command/notebook path.
- axis labels, metric direction, and model labels are readable.
- figure caption draft is written.
- visual claim is consistent with the corresponding table.
- generated file format is suitable for slides/report.

Required artifacts:

- figure file
- source data path
- plot command or notebook path
- caption draft

If a figure is illustrative rather than measured, label it as schematic.

Current plan:

- `figure_plan.md`

Generated from measured artifacts:

- `generated/figure_manifest.tsv`
- `generated/captions.md`
- `generated/figure_02_tokenizer_fertility_delta.png`
- `generated/figure_03_zero_step_initialization.png`
- `generated/figure_05_evaluation_coverage.png`

Regenerate with:

```bash
python3 scripts/plot_v5_reporting_figures.py
```
