# Step 27 Manuscript Outline

## Recommended Title

Vocabulary Extension Is Not Enough: A Controlled Failure Analysis of XLM-R Adaptation for Unsupported Scripts

## One-Sentence Thesis

Appending target-language vocabulary can fix tokenization fragmentation, but the current extended-vocabulary XLM-R adaptation fails under clean matched-control MLM audits because appended-token prediction becomes the dominant bottleneck.

## Abstract

Multilingual encoders often tokenize low-resource and unsupported-script languages into highly fragmented units. We evaluate a controlled XLM-R vocabulary-extension pipeline over target10 Bible languages, preserving original XLM-R ids while appending target-language SentencePiece units. The tokenizer intervention substantially reduces fragmentation, and initialization plus vocabulary size strongly affect early MLM behavior. However, under a clean v2 book-level split with `ACT` final held out and matched-token original continued-pretraining controls, the adapted extended-vocabulary model is not competitive. Word/character-normalized MLM diagnostics confirm that this is not merely a raw-token metric artifact. Loss decomposition localizes the failure to appended-token prediction: added tokens account for most adapted MLM loss despite being roughly half of non-special tokens. Added-token weighting, strict new-row-only updates, lower-rate staged updates, `mean`/`align` initialization probes, smaller-vocabulary controls, and longer 8k MLM do not produce a positive adapted-model result. The result is a leakage-audited diagnostic negative finding: vocabulary extension is useful for preprocessing, but reliable low-resource adaptation requires stronger objectives or data redesign beyond appending vocabulary rows.

## Contributions

1. A leakage-audited v2 experimental protocol with `ACT` final protected and burned `JOH` excluded.
2. A tokenizer-level finding: target vocabulary extension reduces XLM-R fragmentation while preserving original ids.
3. A controlled negative model result: adapted extended-vocabulary checkpoints fail against original continued-pretraining controls under matched-token and normalized MLM metrics.
4. A failure diagnosis: appended-token prediction dominates the adapted loss.
5. A repair map: intuitive fixes and smaller-vocabulary branches mitigate symptoms but do not restore original-control competitiveness.

## Paper Structure

1. Introduction
   - Motivation: unsupported-script tokenization bottleneck.
   - Main message: tokenizer fixes are not sufficient for model adaptation.
2. Related Work
   - Multilingual vocabulary extension.
   - Low-resource adaptation.
   - Negative results and leakage-safe evaluation.
3. Experimental Protocol
   - Data, target10, Bible-domain limitation.
   - v2 split: train excludes `MAR`, `JOH`, `ACT`; `MAR` dev; `JOH` burned; `ACT` protected.
   - Tokenizer merge and id preservation.
4. Tokenization and Initialization
   - Fragmentation reduction.
   - Initialization comparison.
5. Controlled MLM Failure
   - Step15 raw matched-token control.
   - Step16 normalized word/char audit.
6. Failure Localization
   - Added-token category loss.
   - Language-level and token-level examples.
7. Repair Attempts
   - Added-token weighting.
   - New-row-only and staged lower-rate updates.
   - Alternative initialization.
   - Smaller vocab and longer-budget probes.
8. Discussion
   - Why vocabulary extension is necessary but insufficient.
   - What a future positive claim must pass.
9. Limitations
   - Bible domain.
   - No positive final downstream/translation claim.
   - No `ACT` final readout for diagnostic path.
10. Conclusion
   - Controlled negative result and future objective/data redesign.

## Main Claim To Preserve

The paper is a diagnostic negative result, not a positive performance paper.
