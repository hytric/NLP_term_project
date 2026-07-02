# Step 26 Paper Framing

## Recommended Title

Vocabulary Extension Is Not Enough: A Controlled Failure Analysis of XLM-R Adaptation for Unsupported Scripts

## Alternative Titles

1. When Tokenization Improves but Adaptation Fails: Auditing Vocabulary Extension for Low-Resource XLM-R
2. Appended Tokens as a Bottleneck in Multilingual Vocabulary Extension
3. A Leakage-Audited Negative Result for Vocabulary-Extended XLM-R Adaptation

## Abstract Skeleton

Multilingual encoders often tokenize low-resource and unsupported-script languages into fragmented units. We study a controlled XLM-R vocabulary-extension pipeline over target10 Bible languages, preserving original XLM-R ids while appending target-language SentencePiece units. The extension substantially reduces tokenization fragmentation, and initialization plus vocabulary size strongly affect early MLM behavior. However, under a clean v2 book-level split with a protected `ACT` final set and matched-token original continued-pretraining controls, the extended adapted model is not competitive. Normalized word/character MLM diagnostics confirm that this is not only a raw-token metric artifact. Loss decomposition localizes the failure to appended-token prediction, and a sequence of repair attempts does not produce seed-stable recovery. Smaller 8k/16k vocabularies mitigate the 32k failure mode, but selected 8k controls and longer 8k MLM still fail original-control competitiveness. We conclude that vocabulary extension is a useful preprocessing intervention but not sufficient for reliable model adaptation without a stronger objective or data redesign.

## Main Contributions

1. A reproducible, leakage-audited protocol for multilingual vocabulary-extension evaluation.
2. A clear tokenizer-level win: target-language pieces reduce fragmentation without changing XLM-R ids.
3. A controlled negative model result: adapted extended-vocabulary MLM fails against original continued pretraining under matched-token and normalized metrics.
4. A diagnosis of the failure source: appended-token prediction dominates the adapted loss.
5. A repair map showing which intuitive fixes are insufficient: added-token weighting, strict new-row-only updates, lower-rate staged updates, alternative initialization, and longer 8k MLM.

## Primary Tables

| Table | Source | Purpose |
| --- | --- | --- |
| Tokenization bottleneck and extension | Steps 02, 03, 13 | Show fragmentation reduction |
| Initialization and vocab-size diagnostics | Steps 14, 21, 23 | Show initialization/vocab-size effects |
| MLM control failures | Steps 15, 16, 24, 25 | Show model noncompetitiveness |
| Added-token failure decomposition | Step 17 | Explain why adaptation fails |
| Repair attempt matrix | Steps 18, 19, 20, 21, 23, 24, 25 | Show what was tried and why it failed |
| Claim evidence contract | Step 26 | Prevent unsupported positive claims |

## Recommended Final Discussion

The result should be written as a strong negative finding: reducing fragmentation is necessary but not sufficient. The experiment isolates a specific failure mode introduced by appending many new vocabulary rows. The clean v2 split and no-final audits strengthen the result because the negative conclusion is not an artifact of test leakage or branch search.

## Do Not Include As Main Results

- Step07 Branch001 translation as a success result.
- LaBSE+CSLS target score compared against an XLM-R high-resource reference.
- `ACT` final downstream or translation metrics.
- Language identification as proof of semantic downstream improvement.
- Step23 as a positive model-dependent result.
