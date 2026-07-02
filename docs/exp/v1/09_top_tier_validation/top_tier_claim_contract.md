# Step 09 Top-Tier Claim Contract

Run id: `step09_top_tier_20260611_144919`

## Main Claim Status

| Claim | Status | Evidence |
| --- | --- | --- |
| Tokenization bottleneck and fragmentation reduction | SUPPORTED | Steps 02-03 |
| New-token initialization matters | SUPPORTED | Step 04 |
| MLM adaptation recovers selected extended checkpoint | PARTIAL_SUPPORT | Step 05, but original XLM-R still has lower dev loss |
| Adapted encoder improves proxy retrieval/matching | SUPPORTED_WEAK_TO_MODERATE | Step 06 |
| Adapted encoder reaches 80% translation reference | UNSUPPORTED_FOR_MAIN_MODEL | Step 09 selected adapted method-matched ratio `0.638034` |
| External sentence embedding upper bound reaches 80% translation reference | FAIL | Step 09 LaBSE method-matched ratio `0.567179` |
| Existing translation branch passes selection-validity audit | FAIL | Step 10 invalidates Step 07/Branch 001 for test-aware selection and mixed-method comparison |
| V2 fresh held-out split is available for F02/F03 rerun | SUPPORTED | Step 12 creates `ACT` clean final heldout with `9804` rows and excludes burned `JOH` |
| V2 tokenizer rerun is complete | SUPPORTED | Step 13 selects the 32k tokenizer using Mark/dev only and records no ACT final access |
| V2 embedding initialization rerun is complete | SUPPORTED | Step 14 selects `fvt` using full Mark/dev zero-step MLM loss and records no ACT final access |
| V2 MLM control artifact rerun is complete | SUPPORTED_NEGATIVE | Step 15 completes 3 seeds for adapted and original-control families with matched train-token budget and no ACT final access |
| V2 adapted checkpoint is competitive with original continued-pretraining control | FAIL | Step 15 adapted mean final Mark/dev loss `4.946829`; original-control mean `2.518008`; diagnostic ratio `1.964580` |
| V2 normalized MLM metric audit supports adapted competitiveness | FAIL | Step 16 estimated NLL per word/char ratio `1.438660`, required `<=1.100000` |
| V2 failure source is diagnosed | SUPPORTED_DIAGNOSTIC | Step 17 added/base loss ratio `2.835906`; added tokens are `50.456741%` of adapted non-special tokens but `74.269955%` of adapted loss |
| V2 added-token-focused repair succeeds without regression | FAIL | Step 18 improves added-token loss in `3/3` seeds but worsens all-token loss in `3/3` seeds; mean all-loss delta `+0.122137` |
| V2 new-row-only repair succeeds without regression | FAIL | Step 19 trainable audit passes `3/3` and base loss is nonworse `3/3`, but added-token loss improves `0/3`; mean added-loss delta `+0.240600` |
| V2 staged/lower-rate repair succeeds without regression | FAIL | Step 20 completes `9/9` variant-seed runs with trainable audit failures `0`, but passing variants are `0/3`; best variant `new_row_added_lr1e-5` improves mean added loss `-0.004565` but added improves only `1/3` seeds |
| V2 alternative initialization resolves MLM failure | FAIL | Step 21 completes `6/6` mean/align runs, but passing methods are `0/2`; best method `align` raw mean final loss `5.086652` is worse than `fvt` `4.946829` |
| V2 model-dependent evidence supports a top-tier positive claim | FAIL | Step 15 claim gate fails; downstream and translation v2 final readouts remain blocked for positive claims |

## Top-Tier-Safe Final Claim

The current evidence can support a representation-learning claim about tokenizer extension and initialization as clean v2 evidence, plus low-resource encoder proxy improvements as exploratory v1 evidence. Under v2, token-matched MLM adaptation improves the adapted checkpoint over its own zero-step state in all 3 seeds, but it is not competitive with an original XLM-R continued-pretraining control. Step 16 shows the negative result remains after word/character normalization. Step 17 localizes the failure to added-token prediction. Step 18 shows simple added-token weighting improves added loss but damages all-token loss. Step 19 shows strict new-row-only repair preserves base rows and base-token loss but worsens added-token loss. Step 20 finds a lower-rate added-only variant with mean improvements, but it is not seed-stable. Step 21 shows plausible alternative initializations do not beat `fvt`. A top-tier positive model-dependent claim remains unsupported unless a stronger tokenizer/objective redesign succeeds or the final claim is explicitly downgraded.

## Required Next Experiments

Detailed checklist: `required_followups.tsv` and `required_followups.md`.

1. Revisit tokenizer construction or objective-level added-token learning; rerun Step 15 only if a repair/probe gate passes in all seeds.
2. If Step 15 passes, run dev-only model selection followed by a fresh held-out book or corpus for final downstream/translation tests.
3. Run adapted-encoder-only translation retrieval or generation benchmark only after the model checkpoint is frozen.
4. Statistical confidence intervals across languages and seeds for retrieval/matching.
5. External LaBSE results reported only as an upper bound, not as evidence for the adapted encoder.
