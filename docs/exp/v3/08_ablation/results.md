# Stage 08 Results: Ablation Study Packaging

작성일: 2026-06-13

Gate status: PASS_ABLATION_PACKAGE_READY

## Summary

The previous first_try and second_try experiments are now explicitly mapped into ablation/failure-analysis roles. None of them is treated as the third_try main result. The package supports the Stage07 diagnostic negative claim by showing which axes plausibly explain the gap between tokenizer improvement and model-quality failure.

## Core Outputs

- Ablation matrix: `ablation_matrix.tsv`
- second_try mapping: `second_try_mapping.tsv`
- first_try mapping: `first_try_mapping.tsv`
- Negative diagnostic summary: `negative_diagnostic_summary.md`
- Report placement guide: `report_placement.md`

## Interpretation

The ablation package supports this report structure:

1. Main result: current XLM-R-base append-only high-resource-replay pilot is diagnostic negative.
2. Ablations: vocab size, init, fallback, retained checkpoint selection, replay/control, appended-token learning, repair objective, and downstream proxy.
3. Appendix: first_try translation/retrieval prototypes and second_try branch details.

## Failure Return

- failed gate: NOT_APPLICABLE
- observed evidence: all prior experiment groups are mapped away from the main claim
- likely cause: NOT_APPLICABLE
- return-to stage: Stage 07 if claim wording changes
- required fix before retry: keep first_try/second_try wording as ablation-only
