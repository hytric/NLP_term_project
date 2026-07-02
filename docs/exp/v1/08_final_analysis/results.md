# Step 08 Results: Final Analysis And Report Tables

Status: SUPERSEDED_BY_STEP09_TOP_TIER_AUDIT

Run id: step08_final_analysis_20260610_branch_pass

Completed date: 2026-06-10

Gate status: PASS_NEGATIVE_RESULT_AFTER_STEP09

Post-audit note: Step 09 was added on 2026-06-11 to check whether the Step 07/Branch 001 translation result was a shortcut. Step 10 was added on 2026-06-11 to audit leakage and selection validity. Step 11 was added on 2026-06-11 to check whether a fresh held-out rerun can be done from current artifacts. Step 12 was added on 2026-06-11 to create a v2 fresh-heldout split. Steps 13-27 rerun tokenizer, initialization, MLM control, normalized MLM metric audit, added-token failure analysis, repair attempts, alternative initialization probes, shortcut audit, smaller-vocab redesign probes, selected 8k normalized control audit, continued-budget probe, final diagnostic claim synthesis, and manuscript package synthesis under v2. Steps 15-16 have artifact gate `PASS` but claim gate `FAIL`; Step 17 diagnoses the repair target; Step 18 shows simple added-token weighting is insufficient; Step 19 shows strict new-row-only repair preserves base rows but does not improve added-token prediction; Step 20 shows lower-rate added-only variants are closer but not seed-stable; Step 21 shows `mean` and `align` do not beat `fvt`; Step 23 shows a smaller 8k vocab branch is viable; Step 24 shows the 8k branch still fails original-control normalized competitiveness; Step 25 shows longer 8k MLM alone does not close the gap; Step 26 locks the top-tier-safe wording as a diagnostic negative claim; Step 27 packages that claim for manuscript writing.

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | all claim rows filled; no TBD values |
| claim evidence map | `claim_evidence_map.md` | yes | evidence files and claim strength mapped |
| paper tables | `paper_tables.md` | yes | report-ready compact tables |
| qualitative analysis | `qualitative_analysis.md` | yes | tokenization/downstream/translation observations |
| limitations | `limitations.md` | yes | caveats and branch constraints documented |
| final checklist | `final_checklist.md` | yes | step gates and file outputs checked |
| file results | `file_results.tsv` | yes | generated final files recorded |

## Summary

The final evidence supports the tokenizer-bottleneck, vocabulary-extension, initialization, MLM-recovery, and frozen retrieval/matching proxy claims. The Step 07 original adapted-encoder translation row failed. Branch 001 produced an exploratory LaBSE+CSLS pass, but Step 09 later showed that this was not a method-matched top-tier translation result.

## Final Claim

Final claim: v1 evidence suggests target-language vocabulary extension plus MLM adaptation can reduce fragmentation and improve selected encoder-only proxy tasks, but these are not top-tier final claims. V2 clean evidence supports the split, tokenizer, initialization, added-token failure diagnosis, and a smaller-vocab redesign direction. V2 MLM control does not support a positive model-dependent claim because neither the original 32k branch, the selected 8k branch, nor the continued-budget 8k branch is competitive with the original continued-pretraining control. The current evidence also does not support a top-tier claim that the selected adapted XLM-R encoder, or the external LaBSE retrieval upper bound, reaches 80% of a method-matched high-resource translation reference. Step 26 fixes the top-tier-safe final framing as a controlled diagnostic negative result, and Step 27 packages that framing as a manuscript-ready diagnostic negative paper.

## Gate Evidence

Evidence:

- Step 02 baseline bottleneck: maximum `tokens_per_word=4.854`, maximum `single_char_token_pct=74.251`.
- Step 03 selected 32k tokenizer: `avg_tokens_per_word_delta_pct=-31.766`, `single_char_delta_pct=-42.365`.
- Step 04 best initialization: `fvt` zero-step dev loss `8.490678`.
- Step 05 selected adapted checkpoint: `fvt` dev loss improves from zero-step `8.490678` to `7.134023`, but remains worse than original XLM-R `6.330356`.
- Step 06 selected adapted checkpoint improves retrieval recall@1 and parallel matching over original XLM-R.
- Step 07 original adapted-encoder translation row fails: target chrF++ `31.613700`, required `49.567925`, ratio `0.510228`.
- Branch 001 LaBSE+CSLS sentence-embedding retrieval is exploratory only because the high-resource reference was XLM-R-based while the target row used LaBSE+CSLS.
- Step 09 method-matched validation fails the 80% translation claim: selected adapted XLM-R ratio `0.638034`; LaBSE+CSLS upper-bound ratio `0.567179`.
- Step 10 leakage/selection audit keeps the translation success claim invalidated: Step 07 selected a target pair on John/test and Branch 001 used repeated test feedback plus a mixed-method high-resource comparison.
- Step 11 fresh-heldout feasibility audit finds no current `USABLE_NOW` fresh held-out set; F02/F03 require a new Step 01 split or a newly imported external corpus.
- Step 12 creates the v2 split: train excludes `MAR`, `JOH`, and `ACT`; `JOH` is burned/excluded; `ACT` clean final has `9804` rows with minimum `852` rows per target language.
- Step 13 completes the v2 tokenizer rerun: all 8k/16k/32k candidates pass Mark/dev tokenization gates, 32k is selected, and no ACT final file is read.
- Step 14 completes the v2 embedding initialization rerun: all required init methods pass, `fvt` is selected with full Mark/dev zero-step MLM loss `8.681328`, and no ACT final file is read.
- Step 15 completes the token-matched v2 MLM control artifact run: adapted improves over zero-step in 3/3 seeds, original-control completes 3/3 seeds, train-token ratio is `1.000798`, and no ACT final file is read.
- Step 15 claim gate fails: adapted mean final Mark/dev loss `4.946829`, original-control mean `2.518008`, diagnostic ratio `1.964580`, required `<=1.100000`.
- Step 16 confirms the Step 15 failure is not only a raw-token-loss artifact: estimated NLL per word/char adapted/original ratio is `1.438660`, required `<=1.100000`.
- Step 17 localizes the failure to added-token prediction: added/base loss ratio `2.835906`; added tokens are `50.456741%` of adapted non-special tokens but account for `74.269955%` of adapted loss.
- Step 18 tests added-token-weighted repair: added-token loss improves in `3/3` seeds with mean delta `-0.508373`, but all-token loss worsens in `3/3` seeds with mean delta `+0.122137`, so repair gate fails.
- Step 19 tests strict new-row-only repair from Step15 adapted checkpoints: trainable audit passes `3/3` and base-token loss is nonworse `3/3`, but added-token loss improves `0/3` with mean delta `+0.240600`, so repair gate fails.
- Step 20 tests staged/lower-rate added-only variants: `9/9` variant-seed runs complete with trainable audit failures `0`, but passing variants are `0/3`; best variant `new_row_added_lr1e-5` has mean added delta `-0.004565` but added-token loss improves only `1/3` seeds.
- Step 21 tests alternative initialization methods `mean` and `align`: `6/6` runs complete with matched token budget, but passing methods are `0/2`; best method `align` has raw mean final loss `5.086652`, worse than `fvt` `4.946829`.
- Step 22 audits the full experiment trail: no active v2 shortcut is found, v1 translation shortcuts remain invalidated, and positive model-dependent claims remain blocked until a redesign branch passes controls.
- Step 23 tests smaller 8k and 16k vocabulary branches: `6/6` runs complete, train-token ratio is `1.000450`, passing variants are `2/2`, best 8k raw mean final loss is `4.541285` versus 32k `4.946829`, and added/base/all category gates pass `3/3`; however 8k raw ratio to original-control mean is still `1.803523`.
- Step 24 audits the selected 8k branch against the original continued-pretraining control: artifact gate passes, token budget ratio is `1.000714`, 8k improves over zero-step in `3/3`, but word/char normalized ratios are both `1.472019`, above the required `<=1.100000`.
- Step 25 continues the selected 8k and original-control checkpoints to about 1M total train tokens: artifact gate passes and 8k keeps improving, but original-control improves more; word/char normalized ratios worsen to `1.587381`, required `<=1.100000`.
- Step 26 locks the final claim contract: diagnostic claim ready, positive adapted-model claim blocked, positive translation/downstream final readout blocked until a future objective/data redesign passes Step15/16-style controls.
- Step 27 creates the manuscript-ready package: abstract, paper claims, table/figure manifest, reviewer-risk audit, and reproducibility checklist.

## Failure Return

Failed gate: v2_mlm_control_claim_gate; normalized_mlm_competitive_gate; method_matched_translation_80_percent

Observed evidence: Step 15 token-matched adapted/original diagnostic ratio `1.964580 > 1.100000`; Step 16 normalized word/char ratio `1.438660 > 1.100000`; Step 17 added/base loss ratio `2.835906`; Step 18 all-token loss nonworse `0/3`; Step 19 added-token loss improves `0/3`; Step 20 passing variants `0/3`; Step 21 passing methods `0/2`; Step 23 best 8k branch improves over 32k but still has raw ratio `1.803523` to original-control mean; Step 24 8k normalized word/char ratio `1.472019 > 1.100000`; Step 25 continued-budget normalized word/char ratio `1.587381 > 1.100000`; Step 09 selected adapted XLM-R ratio `0.638034 < 0.800000`; LaBSE+CSLS upper-bound ratio `0.567179 < 0.800000`

Return-to step: objective/data redesign beyond longer 8k MLM, or Step26 diagnostic synthesis

Required fix: redesign objective/data beyond the selected and longer 8k branch or downgrade the model-dependent claim before making a positive v2 model-dependent claim; if that succeeds, run dev-only model and pair selection plus a fresh held-out translation retrieval or generation benchmark.
