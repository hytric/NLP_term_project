# v5 Figure Plan

Last updated: 2026-06-27

Figures should be generated only from measured artifacts. Until the remaining
MLM and downstream runs complete, use these as planned figure slots.

## Figure 1. Experiment Pipeline

Type: schematic

Status: generated.

Purpose:

```text
Show the controlled Glot500 replay: raw 92+10 corpus -> SPM append tokenizer ->
initialized checkpoints -> continued MLM -> Glot500 metric replay.
```

Source:

- `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`
- `docs/exp/v5/0_tokenizer/03_audit/main/vocab_audit.json`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`

Caption draft:

```text
v5 preserves the Glot500-style experimental structure while limiting the
language set to 92 XLM-R-seen Glot500 languages and 10 Glot500-internal target
languages.
```

## Figure 2. Tokenizer Fertility Delta

Type: bar chart

Status: generated.

Source data:

- `docs/exp/v5/0_tokenizer/03_audit/main/tokenization_comparison.tsv`

Required axes:

- x-axis: language-script
- y-axis: target tokens/word - base tokens/word
- color: head vs v5_target
- mark `dzo_Tibt` explicitly

Caption draft:

```text
The main v5 tokenizer reduces tokens per word for 29 of 30 audited languages,
with `dzo_Tibt` as the remaining target-side regression.
```

## Figure 3. Zero-Step Initialization Comparison

Type: grouped bar chart

Status: generated.

Source data:

- `docs/exp/v5/1_embedding/04_zero_step_eval/main/summary.tsv`

Required axes:

- x-axis: summary group (`head`, `v5_target`, `all`)
- y-axis: weighted mean NLL, lower is better
- bars: `v5_random`, `v5_mean`, `v5_fvt`

Caption draft:

```text
FVT initialization substantially lowers zero-step MLM proxy NLL compared with
random resize and mean initialization, especially on the v5 target group.
```

## Figure 4. Training Curves

Type: line chart

Source data:

- `train_results.json` / logs from matched `v5_random` and `v5_fvt` runs
- checkpoint-wise MLM proxy summaries after they are generated

Required axes:

- x-axis: step
- y-axis: train loss or PPPL/NLL
- lines: `v5_random`, `v5_fvt`

Caption draft:

```text
Matched continued MLM curves test whether the zero-step initialization
advantage persists into early training.
```

Status: pending matched checkpoints.

## Figure 5. Downstream Metric Completion

Type: heatmap or checklist table

Status: partially generated as an evaluation coverage chart. Final metric
completion heatmap should be regenerated after downstream runs finish.

Source data:

- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_summary.tsv`

Caption draft:

```text
Metric completion and coverage are reported explicitly so unavailable target
language task data is not confused with negative downstream performance.
```

Status: pending final metric execution.
