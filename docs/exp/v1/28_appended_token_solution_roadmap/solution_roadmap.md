# Step 28 Appended-Token Solution Roadmap

## Why A Solution Is Needed

Step17 localizes the main failure to appended-token prediction. That diagnosis is useful, but by itself it is not enough for a strong paper story. The paper should also explain what kind of method could plausibly fix the bottleneck and how that method would be tested.

The current evidence says:

- Added tokens are `50.456741%` of adapted non-special tokens.
- Added tokens account for `74.269955%` of adapted MLM loss.
- Added/base loss ratio is `2.835906`.
- Simple added-token weighting improves added loss but worsens all-token loss.
- Strict new-row-only training preserves base behavior but does not improve added-token prediction.
- Smaller vocabularies mitigate the burden but still fail original-control competitiveness.

Therefore the next solution should not merely "train longer" or "weight added tokens more". It must teach the model how appended tokens relate to existing XLM-R subtoken behavior while preserving base-token competence.

## Recommended Solution Hypothesis

The most plausible next method is:

> Subtoken-teacher distillation for appended tokens, followed by a curriculum that gradually increases appended-token prediction pressure while constraining base-token behavior with KL preservation.

In simpler terms:

1. Use the original XLM-R tokenizer/model as a teacher over the old subtoken decomposition.
2. For each appended token, derive a teacher signal from the original subtokens that would have represented the same surface span.
3. Train the extended model so appended-token embedding and LM-head rows imitate the teacher span representation and prediction behavior.
4. During MLM, oversample masks involving appended tokens, but add a base-token KL or replay loss so the model does not damage old-token predictions.
5. Use curriculum scheduling rather than a fixed added-token weight from the first step.

## Why This Directly Targets The Diagnosed Failure

The failed repairs show two constraints:

- Added-token prediction needs stronger supervision.
- Base/all-token behavior must not be sacrificed.

Subtoken-teacher distillation provides the missing supervision for new rows. Base KL/replay prevents the repair from becoming another Step18-style tradeoff. Curriculum scheduling avoids shocking the model with high added-token pressure before the new rows are aligned.

## What Would Count As A Real Fix

A future method is not a fix unless it passes all of these gates:

1. Added-token loss improves in `3/3` seeds versus Step15 or selected 8k baseline.
2. Base-token loss is nonworse in `3/3` seeds.
3. All-token loss is nonworse or improved in `3/3` seeds.
4. Step15-style adapted/original raw control is recorded.
5. Step16-style word and character normalized adapted/original ratios are `<=1.100000`.
6. No `ACT` final access occurs before model and scoring decisions are frozen.

## Recommended Priority

Priority order:

1. `S01_SUBTOKEN_TEACHER_DISTILLATION`
2. `S02_CURRICULUM_ADDED_MLM_WITH_BASE_KL`
3. `S03_SPAN_AWARE_ADDED_TOKEN_ALIGNMENT`
4. `S04_DATA_REDESIGN_WITH_NONFINAL_TARGET_TEXT`
5. `S05_CONSERVATIVE_VOCAB_PRUNING_PLUS_DISTILLATION`

The first two should be implemented together if compute allows, because the teacher signal addresses added-token learning and the KL/curriculum addresses base preservation.

## How To Present This

Do not say "we solved the appended-token bottleneck." Say:

> The diagnosis points to a concrete remedy: appended tokens need teacher-guided supervision from the original subtoken decomposition, and repair training must preserve base-token behavior. We propose this as the next experiment, with strict gates before any positive claim.
