# Step 27 Paper Claims

## Final Main Claim

Vocabulary extension reduces tokenizer fragmentation for target10 low-resource and unsupported-script languages, but the current extended-vocabulary XLM-R adaptation is not competitive with original continued pretraining under clean v2 controls. The failure is concentrated in appended-token prediction and remains unresolved after multiple repair probes.

## Allowed Strong Claims

- XLM-R has a measurable target10 tokenization bottleneck.
- Appending target-language SentencePiece units reduces fragmentation while preserving XLM-R ids.
- Initialization and vocabulary size materially affect early MLM behavior.
- Under v2 controls, the adapted extended-vocabulary model fails original-control competitiveness.
- Added-token prediction is the dominant diagnosed failure source.
- Smaller vocabularies mitigate the 32k burden but do not produce a positive adapted-model result.
- Longer 8k MLM does not rescue the normalized gap.
- The current top-tier-safe framing is a diagnostic negative result.

## Required Numeric Anchors

| Finding | Numeric anchor |
| --- | ---: |
| XLM-R fragmentation | `syr tokens_per_word=4.854`; `single_char_token_pct=74.251` |
| Step03 extension | `avg_tokens_per_word_delta_pct=-31.766`; `single_char_delta_pct=-42.365` |
| Step15 matched control failure | adapted/original ratio `1.964580` |
| Step16 normalized failure | word/char ratio `1.438660` |
| Step17 added-token hotspot | added/base loss ratio `2.835906`; added loss share `74.269955%` |
| Step23 smaller-vocab probe | 8k raw loss `4.541285` vs 32k `4.946829`; raw ratio to original `1.803523` |
| Step24 8k normalized control | word/char ratio `1.472019` |
| Step25 longer 8k budget | word/char ratio `1.587381` |
| Step26 claim contract | diagnostic ready `1`; positive ready `0` |

## Forbidden Claims

- Do not claim the adapted model is competitive with original XLM-R or original continued pretraining.
- Do not claim downstream or translation improvement as a v2 final result.
- Do not claim method-matched translation reaches 80 percent of high-resource reference.
- Do not present Step23 smaller-vocab `PASS` as model success.
- Do not report or imply `ACT` final performance.

## Reviewer-Safe Rephrasing

| Risky wording | Safer wording |
| --- | --- |
| "Vocabulary extension improves XLM-R" | "Vocabulary extension improves tokenization but not current controlled MLM competitiveness." |
| "The 8k branch fixes the model" | "The 8k branch mitigates the 32k failure mode but still fails original-control normalized audits." |
| "Translation remains future work" | "Translation success is unsupported by method-matched audits and is blocked until a control-passing model exists." |
| "Downstream gains are shown" | "Legacy downstream proxy gains are exploratory; v2 positive downstream final readout is blocked." |

## Proposed Remedy For Future Work

The diagnosis should lead to a concrete next method:

1. Use original XLM-R subtoken decomposition as a teacher signal for appended-token spans.
2. Initialize or train appended embedding/LM-head rows with span-level teacher distillation.
3. Increase added-token MLM pressure with a curriculum rather than a fixed high weight.
4. Preserve base-token behavior with KL/replay loss during repair training.
5. Reopen positive claims only if added/base/all gates pass in `3/3` seeds and Step16-style word/char normalized ratios are `<=1.100000`.

This remedy is proposed, not proven. It is documented in [Step28 solution roadmap](../28_appended_token_solution_roadmap/solution_roadmap.md).
