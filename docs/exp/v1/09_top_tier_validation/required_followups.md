# Step 09 Required Follow-Ups

These are the additional experiments required before making a top-tier translation or broad downstream claim.

## Immediate Decision

The current final claim must stay limited to tokenizer extension, initialization, MLM recovery from the initialized state, and weak-to-moderate frozen encoder proxy improvements.

The translation success claim is blocked until the `P0` follow-ups in `required_followups.tsv` are run and pass.

Diagnostic-paper path: Step26 has locked a top-tier-safe diagnostic negative claim. This path does not require `ACT` final readout, but it must remove positive adapted-model, downstream, and translation success wording.

Update after Step 10: `F06_leakage_and_selection_audit` has been run and failed the translation selection protocol. The split structure passes, but Step 07/Branch 001 translation success remains invalidated by test-aware selection and mixed-method comparison.

Update after Step 11: `F02_method_matched_fresh_translation` and `F03_adapted_encoder_only_translation` cannot be run as top-tier fresh-heldout experiments from the current artifacts. A new Step 01 split with a reserved final held-out book, or a newly imported external corpus with provenance, is required first.

Update after Step 12: a v2 split now exists. It reserves `ACT` as a clean final held-out book, excludes burned `JOH`, and marks all v1 checkpoints/results invalid for v2 final claims.

Update after Step 15: `F01_longer_mlm_control` has been rerun under v2 with 3 seeds for both the adapted checkpoint and original continued-pretraining control. The latest run uses a matched train-token budget of 500k tokens per run (`token_ratio=1.000798`). The artifact gate passes and the adapted checkpoint improves over its own zero-step loss in all 3 seeds, but the claim gate fails because the adapted mean Mark/dev loss is not competitive with the original-control mean (`ratio=1.964580`, required `<=1.100000`). Top-tier downstream or translation claims should not proceed as positive claims until Step 15 is rerun successfully under a revised objective or the claim is downgraded.

Update after Step 16: cross-tokenizer metric normalization does not rescue the Step 15 claim. Estimated NLL per word and per character both have adapted/original ratio `1.438660`, above the required `<=1.100000` margin. The next repair should revise the method or objective, not merely argue that raw token loss was incomparable.

Update after Step 17: the failure is concentrated in added-token prediction. Added tokens are `50.456741%` of adapted non-special tokens but account for `74.269955%` of adapted MLM loss; added-token mean loss `7.267345` is `2.835906x` adapted base-token loss. The next repair should target added-token learning/init/objective.

Update after Step 18: simple added-token weighting is not enough. It improves added-token dev loss in `3/3` seeds with mean delta `-0.508373`, but worsens all-token dev loss in `3/3` seeds with mean delta `+0.122137`. The next repair should preserve base-token behavior, for example frozen-base/new-row-only training or staged training.

Update after Step 19: strict new-row-only repair from the Step15 adapted checkpoints preserves base rows and base-token loss, but it does not repair added-token prediction. Trainable audit passes in `3/3`, base-token loss is nonworse in `3/3`, added-token loss improves in `0/3`, and mean added-loss delta is `+0.240600`. The next repair should change schedule/objective, such as lower learning rate, staged unfreeze, or a different added-token objective.

Update after Step 20: staged/lower-rate added-only variants are closer but still fail the top-tier repair gate. The grid completed `9/9` variant-seed runs with no trainable audit failures. `bias_only_added_lr1e-4` improves added-token loss in `2/3` seeds and all/base in `3/3`; `new_row_added_lr1e-5` improves mean all/base/added loss, but added-token loss improves only `1/3` seeds. Passing variants are `0/3`, so no Step15/16 rerun should proceed as a positive model-dependent claim.

Update after Step 21: alternative initialization does not rescue the v2 MLM failure. `mean` and `align` complete `6/6` runs with matched token budget, but passing methods are `0/2`. The best alternative, `align`, has raw mean final Mark/dev loss `5.086652`, worse than Step15 `fvt` mean `4.946829`, and category gates vs `fvt` are added `0/3`, base `0/3`, all `0/3`.

Update after Step 23: smaller vocabulary size is a viable redesign direction but not yet a positive model-dependent claim. The 8k and 16k branches complete `6/6` runs with train-token ratio `1.000450`; both pass added/base/all category gates in `3/3` seeds and beat the 32k Step15 raw mean final loss. The selected 8k branch has raw mean final loss `4.541285` versus 32k `4.946829`, but its raw ratio to the original-control mean is still `1.803523`. The next required run is Step15/16-style control and normalized-metric evaluation with the 8k branch.

Update after Step 24: the selected 8k branch still fails the original-control normalized audit. It improves over zero-step in `3/3` seeds and has matched train-token ratio `1.000714`, but word/char normalized adapted/original ratios are both `1.472019`, above the required `<=1.100000`. Positive downstream and translation final readout remain blocked.

Update after Step 25: longer 8k MLM budget does not rescue the model-dependent claim. Continuing both 8k adapted and original-control checkpoints to about 1M total train tokens keeps artifact gates clean and 8k continues improving, but original-control improves faster. Word/char normalized ratio worsens to `1.587381`, above the required `<=1.100000`.

Update after Step 26: the allowed top-tier framing is now a diagnostic negative claim. Step26 records `PASS_DIAGNOSTIC_CLAIM_READY`, maps `14` evidence rows, and blocks `10` positive claim rows until a future objective/data redesign passes Step15/16-style controls.

Update after Step 27: the diagnostic negative claim is packaged for manuscript writing. Step27 records `PASS_MANUSCRIPT_READY` and provides a manuscript outline, paper claims, table/figure manifest, reviewer-risk audit, and reproducibility checklist. This does not unblock positive performance claims.

## P0 Experiments

1. Repair MLM adaptation with an original continued-pretraining control, using objective/data redesign beyond the Step23 selected 8k branch and Step25 longer-budget probe.
2. Method-matched translation evaluation on fresh held-out data.
3. Adapted XLM-R-only translation retrieval or generation.
4. Leakage and selection audit covering branch count, candidate pools, duplicate verses, and test feedback.
5. Use Step26 diagnostic claim wording if the paper proceeds without a new positive-control-passing branch.
6. Use Step27 manuscript package for the diagnostic negative paper draft.

## P1 Experiments

1. Stronger downstream hard-negative tasks with confidence intervals.
2. A real generation baseline evaluated with method-matched high-resource and target protocols.

## Exit Rule

No positive translation claim is allowed unless a method-matched main-model row reaches target/high-resource ratio `>=0.800000` on a held-out set that was not used during branch search.
