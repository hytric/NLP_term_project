# Table 15. Glot500 Reproduction Fidelity Matrix

Last updated: 2026-06-27

Caption draft:

```text
The v5 experiment is a controlled-subset replay of the Glot500 workflow. This
matrix separates the parts of the original experimental surface that are
faithfully retained from the parts that are intentionally adapted, still
pending, or disallowed as claims.
```

| Glot500 surface | v5 implementation | Fidelity status | Current evidence | Claim rule |
| --- | --- | --- | --- | --- |
| Language/corpus scale | `92` XLM-R-seen Glot500 language-scripts + `10` Glot500-internal targets | adapted by design | merge report PASS, raw symlink count `102`, actual samples `92,452,251` | say controlled 102-language replay, not full 511-language reproduction |
| Target inclusion threshold | target10 selected from Glot500 raw with `new_length >= 30000` and local raw directory present | retained for selected targets | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` | target set is Glot500-internal, not an external corpus novelty |
| Tokenizer expansion | auxiliary SentencePiece training followed by append-style extension over XLM-R tokenizer | retained in method family | full tokenizer has `368,687` HF tokens, `118,685` novel token strings, `<mask>` remap audited | valid Glot500-style tokenizer replay, with `dzo_Tibt` fertility caveat |
| Continued MLM pretraining | paired `v5_random` then `v5_fvt` 10K MLM under the same corpus/tokenizer/schedule rule | pending matched-pair completion | `v5_random` has the selected 10K model artifact; `v5_fvt` is still running and not wrapper-ready | do not claim after-MLM method results until both checkpoints are selected |
| Initialization comparison | random resize vs source-token decomposition FVT, with mean/align as supporting ablations | novelty layer added to replay | FVT zero-step target weighted NLL delta vs random: `-9.626238` | safe as intrinsic novelty now; downstream novelty waits for v5 rows |
| Source-token preservation | source rows copied by token identity; `<mask>` row remapped; LM head tied | retained and strengthened by audit | copied rows `250,002`, FVT rows `118,427`, byte rows `256`, fallback rows `2`, `<mask>` diff `0.0`, tied `true` | use as correctness evidence for vocabulary extension |
| Evaluation metric families | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip retained | retained as required surface | metric fidelity audit `metric_fidelity_ready_current_pending_v5`; baseline/reference rows measured where local data exists | every metric must be measured, pending, or explicitly coverage-limited |
| Head/tail/all reporting | head/all and v5-target subset reported where coverage permits | retained with coverage boundary | PPPL target10 coverage is `10/10`; official downstream target membership is partial but local tail materialization needs repair | target10 downstream improvement is disallowed unless target task data is materialized |
| External Glot500 model | `cis-lmu/glot500-base` used as external reference | adapted role | baseline/reference rows parsed for `xlmr_base` and `glot500_base` | do not call Glot500-base an equal-budget baseline |
| Final result promotion | aggregation scripts promote only completed parsed outputs | retained as reproducibility guard | `aggregate_v5_metrics.py`, result insertion matrix, finalization gates | live logs and partial files cannot become final result claims |

Short answer for report/PPT:

```text
v5 is ready as a faithful controlled-subset replay of the Glot500 experimental
logic. It is not, and should not be described as, a full 511-language Glot500
reproduction.
```

Source artifacts:

- `docs/exp/v5/goal_readiness.md`
- `docs/exp/v5/3_evaluation/metric_mapping.md`
- `docs/exp/v5/4_reporting/metric_fidelity_audit.md`
- `docs/exp/v5/4_reporting/03_final_report/claim_ledger.md`
- `docs/exp/v5/4_reporting/03_final_report/reproducibility_appendix.md`
