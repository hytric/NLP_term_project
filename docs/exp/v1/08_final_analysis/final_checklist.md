# Step 08 Final Checklist

Run id: `step08_final_analysis_20260610_branch_pass`

| Check | Status | Evidence |
| --- | --- | --- |
| Step folders 00-27 exist | PASS | `docs/exp/second_try/[00-27]_*` |
| Each executable step has `results.md` | PASS | Step 00 through Step 27 |
| Each completed executable step has `score_table.tsv` | PASS | Step 00 through Step 27 |
| Each completed executable step has `file_results.tsv` | PASS | Step 00 through Step 27 |
| Score tables contain no `TBD` | PASS | verified after Step 27 fill |
| Step 07 initial failure is not hidden | PASS | `07_translation_benchmark/results.md` and branch folder |
| Branch retry evidence is recorded | PASS | `branches/branch_001_translation_retrieval_gap/score_table.tsv` |
| Branch translation pass is marked exploratory | PASS | `08_final_analysis/claim_evidence_map.md` |
| Method-matched translation audit is complete | PASS_NEGATIVE_RESULT | `09_top_tier_validation/score_table.tsv` |
| Leakage/selection audit is complete | PASS_NEGATIVE_RESULT | `10_leakage_selection_audit/score_table.tsv` |
| Fresh-heldout feasibility audit is complete | PASS_NEGATIVE_RESULT | `11_fresh_holdout_feasibility/score_table.tsv` |
| V2 split protocol is complete | PASS | `12_v2_split_protocol/score_table.tsv` |
| V2 tokenizer rerun is complete | PASS | `13_v2_tokenizer/score_table.tsv` |
| V2 embedding init rerun is complete | PASS | `14_v2_embedding_init/score_table.tsv` |
| V2 MLM control rerun artifact gate is complete | PASS | `15_v2_mlm_control/score_table.tsv` |
| V2 MLM control claim gate passes | FAIL | token-matched adapted/original diagnostic ratio `1.964580`, required `<=1.100000` |
| V2 normalized MLM metric claim gate passes | FAIL | estimated NLL per word/char ratio `1.438660`, required `<=1.100000` |
| V2 added-token failure source is diagnosed | PASS | added/base loss ratio `2.835906`; added loss share `74.269955%` |
| V2 added-token weighted repair succeeds | FAIL | added loss improves `3/3`, all-token loss nonworse `0/3` |
| V2 new-row-only repair succeeds | FAIL | trainable audit passes `3/3`, base loss nonworse `3/3`, added loss improves `0/3` |
| V2 staged/lower-rate repair succeeds | FAIL | passing variants `0/3`; best variant mean added delta `-0.004565`, but added improves only `1/3` seeds |
| V2 alternative initialization probe succeeds | FAIL | passing methods `0/2`; best `align` raw mean is worse than `fvt` by `0.139823` |
| V2 smaller-vocab redesign probe succeeds | PASS | 8k/16k passing variants `2/2`; best 8k raw delta vs 32k `-0.405544`, but ratio vs original remains `1.803523` |
| V2 selected 8k normalized control succeeds | FAIL | word/char normalized ratio `1.472019`, required `<=1.100000` |
| V2 continued 8k budget probe succeeds | FAIL | word/char normalized ratio `1.587381`, required `<=1.100000` |
| Top-tier diagnostic claim synthesis is complete | PASS_DIAGNOSTIC_CLAIM_READY | Step26 evidence rows `14`, blocked positive claim rows `10` |
| Final manuscript synthesis is complete | PASS_MANUSCRIPT_READY | Step27 manuscript outline, claims, table manifest, reviewer-risk audit, and reproducibility checklist |
| Final claim caveats are recorded | PASS | `08_final_analysis/score_table.tsv` |

## Next Allowed Move

Top-tier translation success is not currently supported. The next top-tier-safe move is writing the diagnostic negative manuscript from Step27, or objective/data redesign beyond longer 8k MLM if a future positive model-dependent claim is required.
