# Decoder-Link Alignment Plan

작성일: 2026-06-18

## Purpose

The full-data decoder probe now shows a stable chrF++ gain across third_try replay-safe seed13/17/23 checkpoints. The next question is whether that gain reflects better cross-lingual semantic alignment or mostly tokenizer/script recovery.

This document defines the minimum alignment experiment needed to connect Experiment 1 and Experiment 3.

## Models

| Model | Role |
| --- | --- |
| `xlm-roberta-base` | baseline |
| `fvt_replay_safe_lr1e5_seed13_step1000` | candidate seed13 |
| `fvt_replay_safe_lr1e5_seed17_step1000` | candidate seed17 |
| `fvt_replay_safe_lr1e5_seed23_step1000` | candidate seed23 |

## Data

Use the exact v3.1 pair data already used by the decoder:

| Direction | Pair file |
| --- | --- |
| `cop -> syr` | `/home/axt/mnt2/jongha/v3_1/translation_pairs/cop_to_syr.tsv` |
| `syr -> cop` | `/home/axt/mnt2/jongha/v3_1/translation_pairs/syr_to_cop.tsv` |

Primary split for reporting:

- `final_test`, because decoder scores are already measured there.

Dev split remains for threshold/model-selection diagnostics only.

## Embedding Extraction

For each model and each side of the pair:

1. tokenize text with that model's tokenizer;
2. run encoder in eval mode;
3. mean-pool last hidden states over non-padding tokens;
4. L2-normalize sentence embeddings;
5. cache embeddings keyed by `model`, `split`, `language`, `item_id`.

## Metrics

For each direction:

| Metric | Meaning |
| --- | --- |
| aligned cosine | cosine between same `item_id` source/target embeddings |
| random negative cosine | cosine to nonmatching target rows |
| margin | aligned cosine minus hardest in-batch negative cosine |
| Recall@1 | source retrieves exact target item |
| Recall@5 | exact target in top 5 |
| MRR | reciprocal rank of exact target |
| hubness@10 | whether a few target items dominate retrieval |

## Link To Decoder Result

After computing alignment metrics, create a table:

| Model | Direction | final chrF++ | Recall@1 | MRR | margin | script-valid |
| --- | --- | ---: | ---: | ---: | ---: | ---: |

Interpretation rule:

- If chrF++ and retrieval/margin both improve, the decoder gain can be cautiously linked to semantic alignment.
- If chrF++ improves but retrieval/margin does not, frame the decoder gain as tokenizer/script recovery or target-language prior.
- If retrieval improves but decoder remains weak, report that the encoder aligns semantically but the simple decoder is underpowered.

## Required Output

| Artifact | Path |
| --- | --- |
| embedding cache manifest | `embedding_cache_manifest.tsv` |
| alignment scores | `alignment_scores.tsv` |
| retrieval scores | `retrieval_scores.tsv` |
| decoder/alignment joined table | `decoder_alignment_join.tsv` |
| result note | `results.md` |

This is now the highest-priority next experiment before making a paper claim about semantic transfer.
