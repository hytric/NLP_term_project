# v5 Comparison Materiality Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `comparison_materiality_waiting_results`

This audit adds practical reporting bands to the generated FVT-vs-random
method comparison table. It is not a statistical significance test. Its
purpose is to prevent the final report/PPT from turning tiny numerical
differences into strong method claims.

Source: `docs/exp/v5/4_reporting/method_comparison_summary.tsv`

Band counts: `large=8; moderate=3; not_applicable=4; small=1`

Rules:

- Accuracy/F1-style scores use absolute-score bands: tie `<0.002`, small `<0.010`, moderate `<0.030`, large `>=0.030`.
- Weighted NLL uses a strict tie band of absolute delta `<0.01` or relative delta `<0.1%`; then small `<1%`, moderate `<5%`, large `>=5%`.
- Pseudo-perplexity-style rows use relative bands: tie `<0.1%`, small `<1%`, moderate `<5%`, large `>=5%`.
- `tie_band` means `no clear practical separation` for report/PPT wording.

| Phase | Metric | Group | Score | Status | Delta | Relative % | Raw FVT Better | Band | Practical Winner | Claim Use |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| zero_step | mlm_proxy | head | weighted_mean_nll | measured | -6.273844 | -48.65 | yes | large | fvt | supports_intrinsic_initialization_claim |
| zero_step | mlm_proxy | head | weighted_pseudo_perplexity | measured | -397684.565864 | -99.81 | yes | large | fvt | supports_intrinsic_initialization_claim |
| zero_step | mlm_proxy | v5_target | weighted_mean_nll | measured | -9.626238 | -52.28 | yes | large | fvt | supports_intrinsic_initialization_claim |
| zero_step | mlm_proxy | v5_target | weighted_pseudo_perplexity | measured | -99104957.546638 | -99.99 | yes | large | fvt | supports_intrinsic_initialization_claim |
| zero_step | mlm_proxy | all | weighted_mean_nll | measured | -8.471624 | -51.31 | yes | large | fvt | supports_intrinsic_initialization_claim |
| zero_step | mlm_proxy | all | weighted_pseudo_perplexity | measured | -14821619.507153 | -99.98 | yes | large | fvt | supports_intrinsic_initialization_claim |
| after_mlm_or_downstream | retrieval_bible | all | top10_accuracy | measured | 0.042330 | 12.90 | yes | large | fvt | eligible_for_final_method_decision |
| after_mlm_or_downstream | retrieval_bible | head | top10_accuracy | measured | 0.042330 | 12.90 | yes | large | fvt | eligible_for_final_method_decision |
| after_mlm_or_downstream | retrieval_tatoeba | all | top10_accuracy | measured | 0.007154 | 1.17 | yes | small | fvt | eligible_only_for_cautious_or_mixed_wording |
| after_mlm_or_downstream | retrieval_tatoeba | head | top10_accuracy | measured | 0.012384 | 1.77 | yes | moderate | fvt | eligible_for_final_method_decision |
| after_mlm_or_downstream | text_classification | all | macro_f1 | measured | 0.014840 | 2.11 | yes | moderate | fvt | eligible_for_final_method_decision |
| after_mlm_or_downstream | text_classification | head | macro_f1 | measured | 0.014840 | 2.11 | yes | moderate | fvt | eligible_for_final_method_decision |
| after_mlm_or_downstream | pseudoperplexity | - | weighted_pseudo_perplexity | pending_result |  |  |  | not_applicable | pending_or_blocked | not_claimable_until_measured |
| after_mlm_or_downstream | ner | - | f1 | pending_result |  |  |  | not_applicable | pending_or_blocked | not_claimable_until_measured |
| after_mlm_or_downstream | pos | - | f1 | pending_result |  |  |  | not_applicable | pending_or_blocked | not_claimable_until_measured |
| after_mlm_or_downstream | roundtrip_alignment | - | accuracy | pending_result |  |  |  | not_applicable | pending_or_blocked | not_claimable_until_measured |

Final report/PPT use:

- Use `large` or `moderate` FVT wins for stronger method wording, if the claim gates are also open.
- Use `small` FVT wins only with cautious or mixed wording.
- Use `tie_band` as no clear separation, regardless of the raw sign.
- Keep `not_applicable` rows out of final method claims until measured artifacts exist.
