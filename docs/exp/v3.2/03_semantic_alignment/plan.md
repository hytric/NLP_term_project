# Stage 03: Semantic Alignment

작성일: 2026-06-19

## Goal

Add a semantic alignment stage after MLM, because MLM alone did not produce robust target10 sentence retrieval in v3.1.

This stage answers:

> Given item-aligned Bible/dev data, can the encoder learn to retrieve same-meaning target10 sentences instead of only predicting local tokens?

## Candidate Objectives

| Objective | Description | First-Pass Recommendation |
| --- | --- | --- |
| contrastive InfoNCE | same `item_id` cross-language pairs are positives; in-batch and hard negatives are negatives | primary |
| TLM-style MLM | concatenate parallel sentences and mask across both sides | secondary |
| supervised pair classification | train shallow head over frozen or lightly tuned encoder | diagnostic |

## Contrastive Setup

Recommended first pass:

- encoder starts from selected Stage 02 checkpoint;
- positives are same `item_id` across target10 languages;
- negatives include in-batch random negatives and same-book hard negatives;
- train with language-balanced batches;
- keep a small high-resource/replay alignment batch if needed;
- evaluate without using final-test for selection.

## Metrics

Primary:

- centered-CSLS R@1/R@5/MRR;
- positive-minus-hard-negative margin;
- median rank;
- hubness@10 max/gini;
- source-language and target-language macro.

Secondary:

- raw cosine;
- centered cosine;
- same-random gap.

## Required Language Breakdowns

Always report:

- all target10 macro;
- worst-language source macro;
- worst-language target macro;
- `cop` source and target;
- `syr` source and target;
- `chr/oji` script-specific retrieval.

## Required Outputs

| Artifact | Purpose |
| --- | --- |
| `alignment_training_manifest.tsv` | run metadata |
| `contrastive_learning_curves.tsv` | train/dev contrastive loss |
| `target10_centered_csls_scores.tsv` | per-direction retrieval |
| `target10_centered_csls_summary.tsv` | model-level summary |
| `target10_language_breakdown.tsv` | source/target language macro |
| `hubness_summary.tsv` | hubness diagnostics |
| `alignment_checkpoint_selection.md` | selected aligned checkpoint |

## Exit Gate

`PASS_SEMANTIC_ALIGNMENT` if:

- target10 macro centered-CSLS R@1 and MRR improve over Stage 02 MLM-only;
- hard margin is less negative or positive;
- `syr` and `cop` source/target retrieval improve;
- hubness@10 does not worsen materially;
- content-token MLM does not collapse after alignment.

