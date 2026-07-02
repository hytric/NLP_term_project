# V3.1 Overall Plan

작성일: 2026-06-18

## Objective

`v3.1` reframes the positive route around encoder embedding quality.

The question is:

> After append-only vocabulary extension and continued MLM adaptation, do target10 low-resource languages attach to the shared XLM-R semantic embedding space better than the XLM-R-base baseline, and do those embeddings improve downstream transfer?

## Hypotheses

| ID | Hypothesis | Test |
| --- | --- | --- |
| H1 | Same-meaning target10 sentences become closer across languages after adaptation. | Experiment 1 alignment margin, MRR, Recall@1/5, hubness, 2D map. |
| H2 | Improved alignment is useful, not just prettier. | Experiment 2 translation retrieval, pair classification, topic classification. |
| H3 | Gains are not caused by language/script siloing or high-resource hubs. | language silo score, hubness@k, high-resource control pairs. |
| H4 | A frozen-feature probe can reveal representation gain without overfitting the encoder. | logistic regression / linear probe on cached embeddings. |
| H5 | A simple decoder can use the adapted encoder states for low-resource translation better than the same decoder on XLM-R-base states. | Experiment 3 chrF++, BLEU, copy/script diagnostics. |

## Stage Order

| Stage | Folder | Depends On | Must Produce | Exit Gate |
| --- | --- | --- | --- | --- |
| 00 | `00_append_only_tokenizer_protocol.md` | v3 tokenizer/init evidence, vocab tutorial | tokenizer merge/audit contract | no model run may replace or reindex the base tokenizer |
| 01 | `01_embedding_alignment` | v3 manifests/checkpoints, target10 parallel data | embedding cache, alignment metrics, 2D maps | `PASS_ALIGNMENT_READY` or diagnostic failure |
| 02 | `02_embedding_downstream` | 01 | retrieval, pair classification, topic classification | `PASS_EMBEDDING_DOWNSTREAM_READY` or diagnostic failure |
| 03 | `03_decoder_translation` | 00, 01, 02, parallel translation data | decoder config, training curves, BLEU/chrF++, samples | `PASS_DECODER_TRANSLATION_READY` or diagnostic failure |
| 04 | `04_ablation` | 01, 02, 03 | ablation placement matrix | ablations explain sensitivity without replacing main claim |

Stage 04 is not a fourth main experiment. It is the ablation packaging layer for stages 01-03.

## Tokenizer Protocol Summary

The tokenizer operation must be append-only.

1. Train an auxiliary tokenizer on low-resource target10 + high-resource replay text.
2. Do not use the auxiliary tokenizer as the final tokenizer.
3. Extract candidate pieces absent from the original XLM-R vocabulary.
4. Append only those new pieces after the original XLM-R vocabulary.
5. Preserve all existing token ids and special token ids.
6. Resize embeddings and initialize only appended rows.
7. Record `append_only_merge_report.tsv`, `id_preservation_audit.tsv`, and row-copy audit.

Any reindexing of existing XLM-R tokens invalidates the main experiment.

## Experiment 1 Summary

Run cross-lingual semantic embedding alignment.

Main metric groups:

1. Same-meaning positive cosine.
2. Positive-minus-hard-negative margin.
3. Sentence/verse retrieval MRR and Recall@1/5.
4. Centroid variance for same `item_id` across languages.
5. Language silo score.
6. Hubness@k.
7. UMAP/t-SNE/PCA 2D maps.

Main pass condition:

- macro target10 alignment margin improves over XLM-R-base;
- macro MRR or Recall@1 improves;
- at least `7/10` target languages improve;
- `cop` and `syr` are explicitly reported;
- no high-resource control collapse or hubness concentration.

## Experiment 2 Summary

Use the cached embeddings from Experiment 1 as frozen features.

Main downstream tasks:

1. **Translation retrieval**
   - source vector retrieves aligned target vector.
   - metrics: Recall@1, Recall@5, MRR, median rank.

2. **Translation pair classification**
   - classify whether two texts in different languages share the same semantic item.
   - features: cosine, abs difference, product.
   - model: cosine threshold and logistic regression.

3. **Topic / Taxi1500-style classification**
   - train on English or high-resource labels, evaluate target10.
   - model: frozen embedding + linear probe/logistic regression.

Optional:

- few-shot target10 classification as a weaker but useful low-resource usability check.
- Coptic POS as auxiliary evidence, not broad target10 proof.

Main pass condition:

- translation retrieval macro MRR improves over XLM-R-base;
- pair classification macro F1/AUROC improves;
- topic classification macro F1 improves;
- at least `7/10` target languages improve on the primary downstream metric;
- results are stable over seeds where candidate checkpoints exist.

## Experiment 3 Summary

Train a simple decoder layer stack over the encoder states for translation.

Main setup:

1. encoder: XLM-R-base or candidate encoder;
2. decoder: identical small Transformer decoder, 1-2 layers;
3. first pass: encoder frozen, decoder trainable;
4. output vocabulary: append-only expanded tokenizer;
5. training objective: teacher-forced autoregressive cross-entropy.

Main translation directions:

- `cop -> syr` and `syr -> cop` if data is sufficient;
- otherwise `eng -> target10` and `target10 -> eng` as broad fallback.

Main pass condition:

- XLM-R-base encoder + same decoder baseline is run;
- candidate encoder + identical decoder improves chrF++ and at least one semantic/retrieval metric;
- BLEU/sacreBLEU and chrF++ are reported;
- copy rate, length ratio, and script validity do not show collapse;
- qualitative examples are included.

## Data Rules

1. Use aligned target10 Bible verses or other sentence-aligned data with stable `item_id`.
2. Freeze train/dev/test before model comparison.
3. Prefer book/chapter-group split over random row split.
4. Do not use test items for checkpoint/model selection.
5. Remove duplicate or near-duplicate leakage across splits where possible.
6. Downstream topic/class labels must be external or fixed before test evaluation.
7. Book/chapter classification is diagnostic only, not the main classification claim.

## Model Rules

| Model | Required? | Role |
| --- | --- | --- |
| `xlm-roberta-base` | yes | baseline |
| v3 replay-safe third_try checkpoints | yes if available | diagnostic candidate |
| future v3.1 positive-route checkpoint | optional until trained | main candidate |
| `cis-lmu/glot500-base` | optional | paper-reference context |

## Artifact Contract

| Artifact | Stage |
| --- | --- |
| `parallel_item_manifest.tsv` | 01 |
| `split_manifest.tsv` | 01 |
| `embedding_cache_manifest.tsv` | 01 |
| `alignment_scores.tsv` | 01 |
| `retrieval_scores.tsv` | 01/02 |
| `csls_retrieval_scores.tsv` | 01 |
| `csls_retrieval_metric_summary.tsv` | 01 |
| `csls_decoder_alignment_delta_summary.tsv` | 01 |
| `semantic_margin_scores.tsv` | 01 |
| `hubness_scores.tsv` | 01 |
| `map_points.tsv` | 01 |
| `figures/*.png` | 01 |
| `downstream_task_manifest.tsv` | 02 |
| `pair_classification_results.tsv` | 02 |
| `topic_classification_results.tsv` | 02 |
| `fewshot_classification_results.tsv` | 02 optional |
| `decoder_config.json` | 03 |
| `decoder_training_curves.tsv` | 03 |
| `translation_results.tsv` | 03 |
| `translation_diagnostics.tsv` | 03 |
| `decoder_collapse_diagnostics.tsv` | 03 |
| `decoder_collapse_metric_summary.tsv` | 03 |
| `decoder_collapse_delta_summary.tsv` | 03 |
| `sample_translations.md` | 03 |
| `ablation_matrix.tsv` | 04 |
| `results.md` | each stage |

## Final Claim Routes

| Exit State | Meaning | Allowed Claim |
| --- | --- | --- |
| `PASS_ALIGNMENT_AND_DOWNSTREAM` | 01 and 02 both pass | broad target10 embedding/downstream improvement claim |
| `PASS_DECODER_TRANSLATION` | 03 passes against XLM-R-base decoder baseline | simple-decoder low-resource translation improvement claim |
| `PASS_ALIGNMENT_ONLY` | alignment improves but downstream fails | representation alignment diagnostic only |
| `PASS_DOWNSTREAM_WITH_WEAK_ALIGNMENT` | downstream improves but alignment metrics mixed | report task improvement cautiously; analyze metric mismatch |
| `FAIL_BOTH` | no alignment/downstream improvement | return to tokenizer/init/training schedule redesign |

## Report Placement

For the term report:

1. Introduction: low-resource tokenizer/embedding problem.
2. Method: append-only vocab extension and encoder embedding evaluation.
3. Experiment 1: semantic alignment and 2D maps.
4. Experiment 2: embedding-vector downstream tasks.
5. Experiment 3: simple decoder translation task.
6. Ablation: tokenizer append protocol, layer/pooling/map/negative construction, decoder depth/freeze, init/training schedule.
7. Error analysis: nearest-neighbor failures, language silos, hubness, copy/script errors.
8. Conclusion: positive route if gates pass; diagnostic if not.
