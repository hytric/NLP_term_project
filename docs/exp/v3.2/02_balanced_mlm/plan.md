# Stage 02: High-Resource-Source-Augmented MLM

작성일: 2026-06-19

## Goal

Train a longer MLM adaptation schedule that uses high-resource language source as aggressively as possible to improve low-resource target10 Pseudoperplexity / MLM Intrinsic Evaluation.

This stage answers:

> Does high-resource-source-augmented MLM improve actual low-resource content-token prediction, especially for `chr/cop/oji/syr`?

This is the primary v3.2 proxy task. Sentence retrieval and translation are downstream diagnostics; they should not replace this stage as the first success criterion.

## Baseline To Beat

Use `v3.1` structured variants as the reference:

| Model group | Strength | Weakness |
| --- | --- | --- |
| `fvt_mlm200` | best dynamic MLM dev loss | weak content-token top-k and retrieval |
| `focus_mlm200` | near-tied MLM dev loss | weak content-token top-k and retrieval |
| `align_mlm200` | best sampled pseudoPPL among mlm200 | weak content-token top-k |

`random` and `mean` remain controls only.

## Training Design

Recommended first schedule:

| Item | Value |
| --- | --- |
| init candidates | `fvt`, `focus`, `align` |
| checkpoint steps | `1k`, `5k`, `10k`, `20k`; optional `50k` |
| high-resource source policy | use as much clean high-resource source as available for transfer/replay |
| target10 sampling | target-aware/language-balanced so weak scripts are not drowned out |
| high-resource replay | not just retention; treat eng/deu/jpn/kor and other available high-resource text as the main transfer source |
| max length | `512` |
| objective | standard MLM first; fixed-mask eval separately |
| seed | at least seed `13`; add seeds after first pass |

## High-Resource Source Usage Policy

The default assumption is:

> more high-resource source is useful if target10 content-token metrics improve and weak scripts do not get diluted.

Recommended data ladder:

| Tier | Data | Role |
| --- | --- | --- |
| Tier 1 | domain-matched high-resource Bible/control text | closest bridge to target10 Bible-style evaluation |
| Tier 2 | large high-resource GlotCC-style text | broad language modeling transfer and stability |
| Tier 3 | target10 low-resource text | direct target adaptation; must be oversampled relative to raw size |
| Tier 4 | weak-script focused target text | repair `chr/cop/oji/syr` content-token failures |

Sampling should be reported explicitly. A high-resource-heavy run is acceptable only if the target10 fixed-mask/content-token metrics improve.

## Evaluation Design

At every checkpoint:

1. Dynamic MLM dev loss.
2. Fixed-mask target10 dev loss.
3. Content-token pseudoPPL.
4. Content-token top-1/top-5/top-10.
5. Content-token average gold probability.
6. Language macro and worst-language score.
7. Token-category score: boundary, punctuation, content, script-specific content.

## Selection Rule

Do not select by dynamic MLM dev loss alone.

Select the checkpoint using this order:

1. worst-language content-token top-5 improves;
2. `chr/cop/oji` content-token top-10 becomes nonzero;
3. macro content-token gold probability improves;
4. high-resource-source usage is documented and reproducible;
5. no severe high-resource replay regression;
6. retrieval preview does not collapse.

## Required Outputs

| Artifact | Purpose |
| --- | --- |
| `balanced_mlm_training_manifest.tsv` | run metadata |
| `high_resource_source_manifest.tsv` | high-resource source inventory and sampling ratios |
| `balanced_mlm_learning_curves.tsv` | dynamic and fixed-mask losses |
| `fixed_mask_content_mlm_scores.tsv` | primary MLM eval |
| `content_token_language_breakdown.tsv` | per-language content-token table |
| `token_category_loss.tsv` | boundary/punctuation/content split |
| `checkpoint_selection.md` | selected MLM checkpoint and rationale |

## Exit Gate

`PASS_CONTENT_TOKEN_MLM` if:

- content-token average gold probability improves over v3.1 structured candidates;
- worst-language content-token top-5 improves;
- `chr/cop/oji` no longer all have top-10 `0`;
- the improvement is not explained by boundary or punctuation tokens;
- the high-resource source policy is explicitly recorded.
