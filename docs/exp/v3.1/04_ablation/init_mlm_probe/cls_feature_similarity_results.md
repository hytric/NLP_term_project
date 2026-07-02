# MLM Dev Encoder Feature Similarity

작성일: 2026-06-19

## Setup

- Dataset: Stage01 target10 MLM dev split, reconstructed from the v3.1 parallel item manifest.
- Same-meaning key: shared Bible verse `item_id` across languages.
- Representation: encoder last hidden state, `cls` pooling, L2 normalization.
- Metrics: directed language-pair exact retrieval over the paired dev subset.
- Scope: this measures semantic attachment of encoder output features, not MLM token prediction loss.

This run produced `990` directed language-pair rows: `11` models times `90` target10 directed language pairs.

## Macro Summary

| Model | Phase | Same cosine | Random neg cosine | Hard neg cosine | Margin | R@1 | R@5 | MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `baseline` | 0.9856 | 0.985528 | 0.993091 | -0.007491 | 0.002862 | 0.013071 | 0.015012 |
| `random_zero` | `zero_step_init` | 0.996681 | 0.996531 | 0.998575 | -0.001894 | 0.004292 | 0.016933 | 0.017926 |
| `mean_zero` | `zero_step_init` | 0.993457 | 0.992744 | 0.997935 | -0.004478 | 0.004287 | 0.018929 | 0.019571 |
| `fvt_zero` | `zero_step_init` | 0.981432 | 0.981018 | 0.992049 | -0.010618 | 0.003262 | 0.014348 | 0.015888 |
| `align_zero` | `zero_step_init` | 0.982 | 0.981752 | 0.992563 | -0.010562 | 0.002995 | 0.013112 | 0.015315 |
| `focus_zero` | `zero_step_init` | 0.971619 | 0.971335 | 0.990756 | -0.019137 | 0.003103 | 0.013292 | 0.01532 |
| `random_mlm200` | `mlm200` | 0.997086 | 0.996951 | 0.998766 | -0.001679 | 0.004721 | 0.017663 | 0.01897 |
| `mean_mlm200` | `mlm200` | 0.994511 | 0.993901 | 0.998539 | -0.004028 | 0.004709 | 0.018155 | 0.019113 |
| `fvt_mlm200` | `mlm200` | 0.993396 | 0.993279 | 0.996107 | -0.002711 | 0.003802 | 0.01608 | 0.017251 |
| `align_mlm200` | `mlm200` | 0.994633 | 0.994555 | 0.996773 | -0.00214 | 0.003535 | 0.014232 | 0.016243 |
| `focus_mlm200` | `mlm200` | 0.994485 | 0.99427 | 0.996715 | -0.00223 | 0.00379 | 0.01523 | 0.017142 |

## Cosine Attachment Score Table

| Model | Phase | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `baseline` | 0.985600 | +0.000000 | +0.000072 | -0.007491 | 0.002862 | 0.015012 |
| `random_zero` | `zero_step_init` | 0.996681 | +0.011081 | +0.000150 | -0.001894 | 0.004292 | 0.017926 |
| `mean_zero` | `zero_step_init` | 0.993457 | +0.007857 | +0.000713 | -0.004478 | 0.004287 | 0.019571 |
| `fvt_zero` | `zero_step_init` | 0.981432 | -0.004168 | +0.000414 | -0.010618 | 0.003262 | 0.015888 |
| `align_zero` | `zero_step_init` | 0.982000 | -0.003600 | +0.000248 | -0.010562 | 0.002995 | 0.015315 |
| `focus_zero` | `zero_step_init` | 0.971619 | -0.013981 | +0.000284 | -0.019137 | 0.003103 | 0.015320 |
| `random_mlm200` | `mlm200` | 0.997086 | +0.011486 | +0.000135 | -0.001679 | 0.004721 | 0.018970 |
| `mean_mlm200` | `mlm200` | 0.994511 | +0.008911 | +0.000610 | -0.004028 | 0.004709 | 0.019113 |
| `fvt_mlm200` | `mlm200` | 0.993396 | +0.007796 | +0.000117 | -0.002711 | 0.003802 | 0.017251 |
| `align_mlm200` | `mlm200` | 0.994633 | +0.009033 | +0.000078 | -0.002140 | 0.003535 | 0.016243 |
| `focus_mlm200` | `mlm200` | 0.994485 | +0.008885 | +0.000215 | -0.002230 | 0.003790 | 0.017142 |

## Reading

Absolute cosine is high for both aligned and negative pairs, so the useful columns are margin, Recall@1, and MRR. If same cosine rises but margin/retrieval stays weak, the model is more anisotropic or script-clustered rather than reliably semantically aligned.

Among the 200-step MLM initialization variants, best macro MRR is `mean_mlm200` at `0.019113`.
Best macro margin is `random_mlm200` at `-0.001679`.
Best macro Recall@1 is `random_mlm200` at `0.004721`.
`fvt_mlm200` has macro MRR `0.017251` and Recall@1 `0.003802`, so the method that wins MLM loss is not the method that wins this feature-similarity probe.
`xlmr_base` has macro Recall@1 `0.002862` and MRR `0.015012`; several init variants improve one metric but not both, and all absolute retrieval values remain very weak.

Conclusion: the MLM dev feature-similarity probe is feasible and useful as a diagnostic, but it does not currently support a strong target10-wide semantic alignment claim. Report it as evidence that MLM loss, absolute cosine, and same-meaning retrieval measure different things.

The MLM dev set is useful here because it is exactly the eval split used for initialization/MLM loss checks, but unlike the plain `target10_dev.txt`, the manifest keeps the verse ids needed to define same-meaning pairs.

## Cause Analysis

Why the same-pair cosine looks good:

- Append-only tokenizer adaptation and MLM training make target10 text less out-of-distribution for the encoder.
- The Bible-domain dev rows share discourse structure, named entities, verse style, and repeated formulaic phrases across languages.
- Mean pooling over XLM-R-style sentence states gives a stable global sentence vector, so low-resource scripts do not fall completely outside the shared representation space.

Why retrieval/margin remains weak:

- XLM-R sentence embeddings are anisotropic: many unrelated sentences already have very high cosine, so same-pair cosine alone is inflated.
- MLM optimizes masked token prediction, not contrastive separation of same-meaning and different-meaning sentences.
- Hard negatives often come from the same Bible book/chapter/domain and can be more similar than the exact aligned verse.
- Script/language/domain cues can dominate the mean-pooled vector, while verse-level semantics are a smaller signal.
- Hubness remains high: a few target vectors appear in many top-k lists, which depresses exact retrieval even when average cosine rises.

Report wording: same-pair cosine provides positive attachment evidence, but the tiny same-random gap and negative hard margin show that semantic discrimination is not solved.

## Artifacts

- Pair metrics: `mlm_dev_cls_feature_pair_scores.tsv`
- Macro summary: `mlm_dev_cls_feature_summary.tsv`
- Embedding caches: `/home/axt/mnt2/jongha/v3_1/mlm_dev_feature_similarity/`
