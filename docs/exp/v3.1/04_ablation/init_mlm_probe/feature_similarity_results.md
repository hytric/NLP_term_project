# MLM Dev Encoder Feature Similarity

작성일: 2026-06-19

## Setup

- Dataset: Stage01 target10 MLM dev split, reconstructed from the v3.1 parallel item manifest.
- Same-meaning key: shared Bible verse `item_id` across languages.
- Representation: encoder last hidden state, attention-mask mean pooling, L2 normalization.
- Metrics: directed language-pair exact retrieval over the paired dev subset.
- Scope: this measures semantic attachment of encoder output features, not MLM token prediction loss.

This run produced `990` directed language-pair rows: `11` models times `90` target10 directed language pairs.

## Macro Summary

| Model | Phase | Same cosine | Random neg cosine | Hard neg cosine | Margin | R@1 | R@5 | MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `baseline` | 0.986126 | 0.985937 | 0.989126 | -0.003 | 0.006874 | 0.018346 | 0.020418 |
| `random_zero` | `zero_step_init` | 0.993204 | 0.992941 | 0.996161 | -0.002957 | 0.005451 | 0.019885 | 0.020485 |
| `mean_zero` | `zero_step_init` | 0.995272 | 0.994729 | 0.99744 | -0.002168 | 0.005801 | 0.023059 | 0.023546 |
| `fvt_zero` | `zero_step_init` | 0.988678 | 0.988294 | 0.992353 | -0.003675 | 0.004211 | 0.018596 | 0.019434 |
| `align_zero` | `zero_step_init` | 0.985721 | 0.985401 | 0.991051 | -0.00533 | 0.004022 | 0.016815 | 0.018028 |
| `focus_zero` | `zero_step_init` | 0.988897 | 0.988465 | 0.992401 | -0.003504 | 0.004217 | 0.017256 | 0.018802 |
| `random_mlm200` | `mlm200` | 0.993669 | 0.993432 | 0.996281 | -0.002612 | 0.005793 | 0.022624 | 0.021748 |
| `mean_mlm200` | `mlm200` | 0.996556 | 0.996348 | 0.998212 | -0.001656 | 0.005724 | 0.022415 | 0.022055 |
| `fvt_mlm200` | `mlm200` | 0.990975 | 0.99076 | 0.993506 | -0.00253 | 0.004551 | 0.018259 | 0.019034 |
| `align_mlm200` | `mlm200` | 0.990067 | 0.989869 | 0.99267 | -0.002603 | 0.004292 | 0.018398 | 0.01903 |
| `focus_mlm200` | `mlm200` | 0.984526 | 0.984009 | 0.988873 | -0.004347 | 0.004553 | 0.017845 | 0.019333 |

## Cosine Attachment Score Table

| Model | Phase | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `baseline` | 0.986126 | +0.000000 | +0.000189 | -0.003000 | 0.006874 | 0.020418 |
| `random_zero` | `zero_step_init` | 0.993204 | +0.007078 | +0.000263 | -0.002957 | 0.005451 | 0.020485 |
| `mean_zero` | `zero_step_init` | 0.995272 | +0.009146 | +0.000543 | -0.002168 | 0.005801 | 0.023546 |
| `fvt_zero` | `zero_step_init` | 0.988678 | +0.002552 | +0.000384 | -0.003675 | 0.004211 | 0.019434 |
| `align_zero` | `zero_step_init` | 0.985721 | -0.000405 | +0.000320 | -0.005330 | 0.004022 | 0.018028 |
| `focus_zero` | `zero_step_init` | 0.988897 | +0.002771 | +0.000432 | -0.003504 | 0.004217 | 0.018802 |
| `random_mlm200` | `mlm200` | 0.993669 | +0.007543 | +0.000237 | -0.002612 | 0.005793 | 0.021748 |
| `mean_mlm200` | `mlm200` | 0.996556 | +0.010430 | +0.000208 | -0.001656 | 0.005724 | 0.022055 |
| `fvt_mlm200` | `mlm200` | 0.990975 | +0.004849 | +0.000215 | -0.002530 | 0.004551 | 0.019034 |
| `align_mlm200` | `mlm200` | 0.990067 | +0.003941 | +0.000198 | -0.002603 | 0.004292 | 0.019030 |
| `focus_mlm200` | `mlm200` | 0.984526 | -0.001600 | +0.000517 | -0.004347 | 0.004553 | 0.019333 |

## Reading

Absolute cosine is high for both aligned and negative pairs, so the useful columns are margin, Recall@1, and MRR. If same cosine rises but margin/retrieval stays weak, the model is more anisotropic or script-clustered rather than reliably semantically aligned.

Among the 200-step MLM initialization variants, best macro MRR is `mean_mlm200` at `0.022055`.
Best macro margin is `mean_mlm200` at `-0.001656`.
Best macro Recall@1 is `random_mlm200` at `0.005793`.
`fvt_mlm200` has macro MRR `0.019034` and Recall@1 `0.004551`, so the method that wins MLM loss is not the method that wins this feature-similarity probe.
`xlmr_base` has macro Recall@1 `0.006874` and MRR `0.020418`; several init variants improve one metric but not both, and all absolute retrieval values remain very weak.

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

## Pooling Ablation

CLS-style pooling is possible by using the first XLM-R `<s>` hidden state, but it is not the preferred main metric here. This encoder was adapted with MLM, not with a contrastive sentence embedding loss or a classification fine-tuning objective. The completed pooling ablation shows mean pooling is stronger on retrieval-oriented metrics.

| Model | Mean cosine | CLS cosine | Mean R@1 | CLS R@1 | Mean MRR | CLS MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.986126 | 0.985600 | 0.006874 | 0.002862 | 0.020418 | 0.015012 |
| `random_mlm200` | 0.993669 | 0.997086 | 0.005793 | 0.004721 | 0.021748 | 0.018970 |
| `mean_mlm200` | 0.996556 | 0.994511 | 0.005724 | 0.004709 | 0.022055 | 0.019113 |
| `fvt_mlm200` | 0.990975 | 0.993396 | 0.004551 | 0.003802 | 0.019034 | 0.017251 |

Reading: keep mean pooling as the main frozen-feature similarity metric; report CLS as a pooling ablation.

## Artifacts

- Pair metrics: `mlm_dev_feature_pair_scores.tsv`
- Macro summary: `mlm_dev_feature_summary.tsv`
- Pooling comparison: `pooling_comparison_results.md`
- Embedding caches: `/home/axt/mnt2/jongha/v3_1/mlm_dev_feature_similarity/`
