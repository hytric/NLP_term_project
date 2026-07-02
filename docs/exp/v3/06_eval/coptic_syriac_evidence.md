# Coptic And Syriac Evidence

작성일: 2026-06-13

## Summary

Coptic and Syriac are main target10 languages, not extension-case languages. Current evidence is asymmetric:

- Coptic has a local supervised downstream task through UD Coptic-Scriptorium POS.
- Syriac has target10 Bible-domain proxy coverage and legacy Coptic-Syriac parallel data, but no fresh local supervised encoder-only downstream task in the current protocol.

The local Syriac search record is `syriac_downstream_search.tsv`.

## Coptic

| Evidence | Value | Reading |
| --- | ---: | --- |
| tokenizer tokens/word delta | -12.539893% | Fragmentation improves. |
| replay-safe MLM proxy delta loss | +5.414744 | Worse than XLM-R, with XLM-R `<unk>` shortcut caveat. |
| replay-safe POS token accuracy delta | +0.006781 | Weak positive, 3/3 checkpoint seeds positive. |
| replay-safe POS macro F1 delta | -0.002656 | Negative. |

Coptic supports only a narrow pilot claim: token-level POS accuracy improves slightly for the current fvt checkpoint seeds. It does not support a broad target10 or robust downstream claim by itself.

## Syriac

| Evidence | Value | Reading |
| --- | ---: | --- |
| tokenizer tokens/word delta | -66.873096% | Fragmentation improves strongly. |
| replay-safe MLM proxy delta loss | +3.025674 | Worse than XLM-R, with XLM-R `<unk>` shortcut caveat. |
| local supervised encoder-only downstream | not found | Positive Syriac downstream claim is unavailable. |
| proxy coverage | Bible frozen proxy and legacy Coptic-Syriac parallel | Diagnostic only under current protocol. |

Syriac is the clearest example of the diagnostic negative pattern: tokenization improves substantially, but current model-level evidence does not show a downstream gain.

## Claim Consequence

The report may say that Coptic/Syriac were included in target10 evidence and that both show tokenizer fragmentation reduction. It must not say that both improved downstream performance. Coptic has weak supervised pilot evidence; Syriac remains proxy-only and negative/mixed at the model-proxy level.
