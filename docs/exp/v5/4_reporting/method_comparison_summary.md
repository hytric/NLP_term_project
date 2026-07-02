# v5 Method Comparison Summary

Last checked: 2026-06-28 18:08 KST

Verdict: `method_comparison_zero_step_ready_pending_after_mlm`

This generated summary is the central FVT-vs-random comparison table for
the v5 novelty claim. Zero-step rows are intrinsic initialization
evidence. After-MLM and downstream rows become promotable only after
matched `v5_random` and `v5_fvt` checkpoints are evaluated and parsed.

Measured rows: `12`; pending rows: `4`; blocked rows: `0`.

## Decision-Tree Input Summary

| Layer | Status | Evidence | Decision use |
| --- | --- | --- | --- |
| zero_step_intrinsic | ready | v5_target weighted NLL random=18.411756; fvt=8.785518; fvt_better=yes | supports only the pre-MLM initialization novelty claim |
| after_mlm_pppl | pending_result | waiting for parsed v5_random/v5_fvt PPPL rows | unlocks or rejects the intrinsic after-training method claim |
| available_downstream | partial_result | measured_metrics=3; fvt_wins=3; random_ties_or_wins=0; pending=ner,pos,roundtrip_alignment; blocked=- | bounds any downstream-transfer claim to available task coverage |

## Full Comparison Rows

| Phase | Metric | Group | Score | Direction | Random | FVT | FVT-random | Relative % | FVT better | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| zero_step | mlm_proxy | head | weighted_mean_nll | lower_is_better | 12.895301 | 6.621457 | -6.273844 | -48.65 | yes | measured |
| zero_step | mlm_proxy | head | weighted_pseudo_perplexity | lower_is_better | 398435.604683 | 751.038819 | -397684.565864 | -99.81 | yes | measured |
| zero_step | mlm_proxy | v5_target | weighted_mean_nll | lower_is_better | 18.411756 | 8.785518 | -9.626238 | -52.28 | yes | measured |
| zero_step | mlm_proxy | v5_target | weighted_pseudo_perplexity | lower_is_better | 99111496.403139 | 6538.856501 | -99104957.546638 | -99.99 | yes | measured |
| zero_step | mlm_proxy | all | weighted_mean_nll | lower_is_better | 16.511807 | 8.040183 | -8.471624 | -51.31 | yes | measured |
| zero_step | mlm_proxy | all | weighted_pseudo_perplexity | lower_is_better | 14824722.688186 | 3103.181033 | -14821619.507153 | -99.98 | yes | measured |
| after_mlm_or_downstream | retrieval_bible | all | top10_accuracy | higher_is_better | 0.328019 | 0.370349 | 0.042330 | 12.90 | yes | measured |
| after_mlm_or_downstream | retrieval_bible | head | top10_accuracy | higher_is_better | 0.328019 | 0.370349 | 0.042330 | 12.90 | yes | measured |
| after_mlm_or_downstream | retrieval_tatoeba | all | top10_accuracy | higher_is_better | 0.610353 | 0.617507 | 0.007154 | 1.17 | yes | measured |
| after_mlm_or_downstream | retrieval_tatoeba | head | top10_accuracy | higher_is_better | 0.700285 | 0.712669 | 0.012384 | 1.77 | yes | measured |
| after_mlm_or_downstream | text_classification | all | macro_f1 | higher_is_better | 0.702956 | 0.717796 | 0.014840 | 2.11 | yes | measured |
| after_mlm_or_downstream | text_classification | head | macro_f1 | higher_is_better | 0.702956 | 0.717796 | 0.014840 | 2.11 | yes | measured |
| after_mlm_or_downstream | pseudoperplexity | - | weighted_pseudo_perplexity | lower_is_better |  |  |  |  |  | pending_result |
| after_mlm_or_downstream | ner | - | f1 | higher_is_better |  |  |  |  |  | pending_result |
| after_mlm_or_downstream | pos | - | f1 | higher_is_better |  |  |  |  |  | pending_result |
| after_mlm_or_downstream | roundtrip_alignment | - | accuracy | higher_is_better |  |  |  |  |  | pending_result |

Claim rule:

- `zero_step` rows can support the intrinsic initialization claim.
- `after_mlm_or_downstream` rows are the only rows that can unlock final
  after-training method claims.
- For `lower_is_better` rows, a negative `FVT-random` is favorable to FVT.
- For `higher_is_better` rows, a positive `FVT-random` is favorable to FVT.
