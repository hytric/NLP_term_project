# Step 26 Final Claim Contract

Run id: `step26_top_tier_diagnostic_claim_20260611`

Gate status: `PASS_DIAGNOSTIC_CLAIM_READY`

## Main Claim

For the current `second_try` evidence, the defensible top-tier claim is:

> Vocabulary extension for low-resource and unsupported-script languages can substantially reduce XLM-R tokenization fragmentation, and careful initialization plus smaller target vocabularies reduce the appended-token learning burden. However, under a clean v2 split with matched-token original continued-pretraining controls, the adapted extended-vocabulary model is not competitive; the failure is concentrated in appended-token prediction and is not fixed by simple weighting, new-row-only updates, lower-rate staged repair, alternative `mean`/`align` initialization, or longer 8k MLM budget.

## Claim Type

Diagnostic negative result with reproducible controls.

This is suitable only if the paper is framed as a controlled failure analysis and method lesson, not as a performance-improvement paper.

## Allowed Contributions

1. A leakage-audited v2 protocol for vocabulary-extension experiments with `ACT` final protected and `JOH` excluded as burned test data.
2. Evidence that target-language vocabulary extension reduces fragmentation while preserving XLM-R ids.
3. Evidence that initialization and vocabulary size materially affect early MLM behavior.
4. Evidence that the main model-dependent bottleneck is appended-token prediction.
5. Evidence that smaller 8k/16k vocab branches mitigate the 32k failure mode, while still failing original-control competitiveness.
6. A negative result showing that longer MLM budget alone does not rescue the adapted model.

## Required Wording

- Say "reduces tokenization fragmentation" rather than "improves downstream performance" unless citing v1 proxy evidence as exploratory.
- Say "diagnoses an appended-token learning failure" rather than "solves low-resource adaptation".
- Say "smaller vocabularies mitigate the 32k added-token burden" rather than "smaller vocabularies make the adapted model competitive".
- Say "positive downstream and translation final readout remain blocked" until a future repaired branch passes Step15/16-style gates.

## Forbidden Wording

- Do not claim that the adapted model beats original XLM-R or original continued pretraining.
- Do not claim method-matched translation reaches 80 percent of the high-resource reference.
- Do not claim Step23 is a completed positive model result.
- Do not use Step07 or Branch001 as top-tier translation evidence.
- Do not imply that longer 8k MLM closes the gap.
- Do not report `ACT` final performance, because no v2 downstream or translation final readout has been legitimately opened.

## Minimum Future Gate For Positive Claim

A future positive model-dependent claim requires all of the following before any `ACT` final readout:

1. A new objective/data redesign beyond smaller vocab and longer 8k MLM.
2. At least 3 seeds for adapted and original-control runs with matched train-token budget.
3. Step15-style raw control recorded.
4. Step16-style word and character normalized ratios `<=1.100000`.
5. Added/base/all category gates pass seed-stably.
6. Downstream and method-matched translation decisions frozen on Mark/dev before `ACT` is read exactly once.
