# Step 08 Claim Evidence Map

Run id: `step08_final_analysis_20260610_branch_pass`, superseded for translation by `step09_top_tier_20260611_144919`

Gate status: `PASS`

## Supported Claims

| Claim | Evidence | Strength | Final wording |
| --- | --- | --- | --- |
| XLM-R tokenizer bottleneck exists | Step 02 `score_table.tsv`: `syr` reaches `tokens_per_word=4.854` and `single_char_token_pct=74.251` | strong | Original XLM-R fragments target10 text heavily. |
| Extended tokenizer reduces fragmentation | Step 03 `score_table.tsv`: selected 32k row has `avg_tokens_per_word_delta_pct=-31.766` and `single_char_delta_pct=-42.365` | strong | Appending target10 pieces reduces fragmentation while preserving XLM-R ids. |
| Initialization matters | Step 04 `score_table.tsv`: zero-step dev loss ranges from `20.809267` random to `8.490678` fvt | strong | New-token initialization materially affects MLM readiness. |
| MLM adaptation recovers extended checkpoint | Step 05 `score_table.tsv`: fvt zero-step `8.490678` to adapted `7.134023` | partial | Adaptation improves the extended checkpoint from its initialized state. |
| Encoder proxy improves | Step 06 `score_table.tsv`: retrieval recall@1 and matching improve over original XLM-R averages | moderate | Selected adapted checkpoint helps nontrivial frozen encoder proxies. |
| V2 tokenizer and initialization reruns are clean | Steps 12-14: ACT final held out; 32k tokenizer selected; `fvt` initialization selected | strong for preprocessing/init | V2 split, tokenizer, and initialization are not using the final test set. |
| V2 smaller-vocab branch is viable | Step 23: 8k raw mean final loss `4.541285` vs 32k `4.946829`; added/base/all category gates pass `3/3` | moderate redesign evidence | Smaller 8k/16k tokenizer branches reduce the 32k added-token burden under the same MLM budget. |
| Top-tier diagnostic claim is ready | Step 26: `PASS_DIAGNOSTIC_CLAIM_READY`; evidence rows `14`; blocked positive claim rows `10` | strong for final wording | The paper can be framed as a controlled diagnostic negative result with unsupported positive claims removed. |
| Diagnostic manuscript package is ready | Step 27: `PASS_MANUSCRIPT_READY`; table/figure rows `8`; reviewer-risk rows `10`; reproducibility checks `10` | strong for writing | The paper can now be drafted from the Step27 manuscript package without changing the claim. |

## Unsupported Or Downgraded Claims

| Claim | Evidence | Decision | Return path |
| --- | --- | --- | --- |
| Adapted model beats original XLM-R MLM dev loss | Step 05 original XLM-R dev loss `6.330356`, selected adapted `7.134023` | unsupported | Return to Step 05 with longer adaptation or revised vocab/init if this claim is required. |
| V2 adapted model is competitive with original continued-pretraining control | Step 15 token-matched adapted mean final Mark/dev loss `4.946829`, original-control mean `2.518008`, ratio `1.964580` | unsupported | Rerun Step 15 with revised init/objective, or downgrade the model-dependent claim. |
| V2 adapted model is competitive after tokenizer-normalized MLM scoring | Step 16 estimated NLL per word/char ratio `1.438660` | unsupported | Treat Step15 failure as robust to the current normalization audit. |
| V2 model-dependent failure source is understood | Step 17 added/base loss ratio `2.835906`; added loss share `74.269955%` | diagnostic support | Repair should target added-token learning/init/objective before rerunning Step 15. |
| V2 simple added-token weighted repair solves the failure | Step 18 added loss improves `3/3`, but all-token nonworse is `0/3` | unsupported | Move to base-preserving repair such as frozen-base/new-row-only or staged training. |
| V2 new-row-only repair solves the failure | Step 19 trainable audit passes `3/3`, base nonworse is `3/3`, but added loss improves `0/3` | unsupported | Move to staged/lower-rate repair or revisit initialization/objective. |
| V2 staged/lower-rate repair solves the failure | Step 20 passing variants `0/3`; best mean added delta `-0.004565` but added improves only `1/3` seeds | unsupported | Revisit initialization/objective or downgrade model-dependent claim. |
| V2 alternative initialization solves the failure | Step 21 passing methods `0/2`; best `align` raw mean final loss `5.086652` vs `fvt` `4.946829` | unsupported | Revisit tokenizer/objective or downgrade model-dependent claim. |
| V2 smaller-vocab branch is already competitive with original control | Step 23 best 8k raw ratio vs original-control mean is `1.803523`, still above the `<=1.100000` competitive margin | unsupported pending rerun | Rerun Step15/16-style control and normalized metric audits with the selected 8k branch. |
| V2 selected 8k branch passes original-control normalized audit | Step 24 word/char normalized ratio `1.472019`, threshold `<=1.100000` | unsupported | Redesign objective/data beyond smaller-vocab branch or downgrade model-dependent claim. |
| Longer 8k MLM budget closes the original-control gap | Step 25 word/char normalized ratio `1.587381`, threshold `<=1.100000` | unsupported | Budget extension alone is insufficient; objective/data redesign or negative framing is required. |
| Positive top-tier adapted-model/downstream/translation claim is ready | Step 26 blocks positive wording until future Step15/16-style controls pass | unsupported | Use the diagnostic claim contract, or run a new objective/data redesign. |
| Adapted encoder alone reaches 80% translation reference | Step 09 selected adapted XLM-R method-matched ratio `0.638034` | unsupported | Report as a failed top-tier translation claim. |
| External LaBSE retrieval reaches 80% method-matched translation reference | Step 09 LaBSE+CSLS method-matched ratio `0.567179` | unsupported | Keep LaBSE as exploratory branch evidence only, not a successful top-tier upper bound. |

## Exploratory Branch Result

| Claim | Evidence | Strength | Final wording |
| --- | --- | --- | --- |
| Mixed-method Branch 001 translation retrieval | Step 07 `score_table.tsv`: Branch 001 LaBSE+CSLS `chrF++=64.434500`, ratio `1.039939` against an XLM-R high-resource reference | exploratory only | This row motivated the Step 09 audit and must not be used as top-tier evidence because the high-resource and target methods differ. |

## Guardrails

- Do not count language identification as positive downstream evidence.
- Do not use first_try metrics as second_try evidence.
- Treat Step 09 as the authority for top-tier translation claims.
- Treat Step 15 as the current authority for v2 MLM control. Its token-matched artifact gate passes, but its claim gate fails.
- Treat Step 16 as the current authority for the cross-tokenizer MLM metric caveat. It does not rescue the Step15 claim.
- Treat Step 17 as the current authority for the Step15 repair target: added-token prediction dominates the adapted loss.
- Treat Step 18 as evidence that simple added-token weighting trades off against base/all-token loss and is not enough.
- Treat Step 19 as evidence that strict new-row-only repair preserves base behavior but does not improve added-token prediction.
- Treat Step 20 as evidence that lower-rate added-only variants are closer but not seed-stable enough for a top-tier positive claim.
- Treat Step 21 as evidence that `mean` and `align` alternative initializations do not beat `fvt` under the matched MLM budget.
- Treat Step 23 as evidence that smaller vocab size is a viable repair direction, not as a completed positive model-dependent claim.
- Treat Step 24 as evidence that the selected 8k branch still fails original-control normalized competitiveness.
- Treat Step 25 as evidence that simply extending 8k MLM budget does not close the gap.
- Treat Step 26 as the authority for final claim wording: diagnostic negative claim is ready, positive adapted-model/downstream/translation claims are blocked.
- Treat Step 27 as the authority for paper packaging: manuscript outline, claims, tables, reviewer risks, and reproducibility checklist are ready for diagnostic writing.
- Keep the caveat that the Step 07 passing translation row is a dev-selected external sentence-embedding retrieval branch compared against a different high-resource method.
