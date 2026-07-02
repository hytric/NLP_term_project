# Embedding Alignment and Downstream Plan

작성일: 2026-06-18

## 목적

이 stage는 broad target10 positive route에서 두 가지를 검증한다.

1. Low-resource language가 XLM-R/third_try encoder embedding space에 잘 붙었는지 확인한다.
2. 그 embedding vector 자체를 사용해 downstream task를 정의하고, XLM-R-base 대비 개선 여부를 평가한다.

핵심 아이디어는 CLIP/CLAP식 shared embedding space 평가를 multilingual text에 적용하는 것이다. CLIP/CLAP에서는 서로 다른 modality의 paired item이 가까워지는지를 본다. 여기서는 modality 대신 언어가 다르다. 같은 `verse_id` 또는 sentence id의 여러 언어 표현이 가까워지고, 다른 의미의 문장은 멀어지는지를 본다.

## Scope

Target languages:

`acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp`

Models:

| Model id | Role |
| --- | --- |
| `xlm-roberta-base` | mandatory baseline |
| current third_try replay-safe checkpoints | diagnostic candidate |
| future positive-route checkpoints | main candidates |
| `cis-lmu/glot500-base` | optional paper-reference model only |

Primary data:

| Data | Use |
| --- | --- |
| target10 aligned Bible verses | semantic alignment, retrieval, pair classification |
| high-resource English/German/Japanese/Korean Bible control | high-resource embedding control |
| Taxi1500 or equivalent fixed-label Bible classification data | embedding-based classification |
| Coptic UD POS | auxiliary Coptic-specific downstream check |

## Experiment 1: Cross-Lingual Semantic Embedding Alignment

### Unit

The basic item is a semantic id:

`item_id = verse_id` or `parallel_sentence_id`

For each `item_id`, there can be one text per language. A good encoder should place texts with the same `item_id` close together even when scripts and languages differ.

### Splits

| Split | Use | Rule |
| --- | --- | --- |
| train | train lightweight downstream classifiers only | never used for final alignment plots |
| dev | checkpoint/model selection | no final claim |
| test | final alignment and downstream report | touched once after all choices are frozen |

If Bible verses are used, split by book or chapter group, not random rows, to reduce near-duplicate leakage. Current `MAR` dev and `JOH` test convention can be kept only if the same split is documented for every language.

### Embedding Extraction

| Choice | Default | Ablation |
| --- | --- | --- |
| layer | 8 | last layer, average of last 4 layers |
| pooling | attention-mask mean pooling | CLS pooling |
| normalization | L2 normalization before cosine | none only as diagnostic |
| max length | 256 or 512, fixed per run | local max length not used for final comparison |
| seeds | model seeds `13/17/23` where available | embedding extraction deterministic |

Layer 8 is the default because Glot500 uses layer 8 for retrieval/alignment-style evaluation.

### Pair Construction

| Pair type | Definition | Purpose |
| --- | --- | --- |
| positive | same `item_id`, different languages | target alignment signal |
| easy negative | different `item_id`, different book/topic | sanity check |
| hard negative | different `item_id`, same book/chapter/topic | prevents shortcut alignment |
| same-language negative | different `item_id`, same language | checks language-only clustering |
| high-resource control pair | high-resource language pair with same `item_id` | ensures control space does not collapse |

### Metrics

| Metric | Definition | Reading |
| --- | --- | --- |
| positive cosine mean | mean cosine over positive cross-lingual pairs | higher is better |
| hard-negative cosine mean | mean cosine over hard negative pairs | should not rise with positives |
| alignment margin | positive cosine minus hard-negative cosine | higher is better |
| Recall@1 / Recall@5 | source sentence retrieves aligned target sentence | translation-retrieval proxy |
| MRR / median rank | rank of aligned target sentence | robust retrieval score |
| centroid variance | dispersion of same `item_id` vectors across languages | lower is better |
| language silo score | how strongly nearest neighbors share language instead of meaning | lower is better |
| hubness@k | number of times each vector/language appears in top-k neighbors | lower concentration is better |
| semantic-vs-language clustering delta | silhouette by `item_id` group minus silhouette by language | positive is better |

### 2D Map

Use UMAP as the primary map and t-SNE/PCA as sensitivity checks.

Required map outputs:

| Figure | Coloring | Purpose |
| --- | --- | --- |
| `umap_by_language.png` | language/script | checks language siloing |
| `umap_by_item_group.png` | verse/topic/item group | checks semantic clustering |
| `umap_base_vs_candidate.png` | model and item group | shows whether third_try tightens cross-lingual clusters |
| `umap_hubness_overlay.png` | top-k hub count | identifies hub languages or hub sentences |

Plot rules:

1. Use the same sampled `item_id`s for every model.
2. Use balanced language sampling.
3. Fix UMAP/t-SNE random seed.
4. Report numbers beside the plot. The 2D map is diagnostic, not sufficient evidence by itself.

### Alignment Gate

`PASS_ALIGNMENT_READY` requires all of the following on dev before final test:

1. Macro target10 alignment margin improves over XLM-R-base.
2. Macro target10 MRR or Recall@1 improves over XLM-R-base.
3. At least `7/10` target languages improve on alignment margin or retrieval MRR.
4. `cop` and `syr` have explicit language-pair rows; they cannot be omitted from the macro claim.
5. Language silo score does not worsen sharply.
6. Hubness does not concentrate in one high-resource language or one script group.
7. High-resource control pairs do not collapse.

If the map looks better but metrics fail, the result is `DIAGNOSTIC_MAP_ONLY`, not a positive claim.

## Experiment 2: Downstream Tasks From Embedding Vectors

This experiment treats encoder outputs as frozen semantic features. The first pass should not fine-tune the encoder. This keeps the claim clean: the embedding space itself improved.

### Task A: Translation Retrieval

Definition:

Given a source-language sentence vector, retrieve the matching target-language sentence vector from a fixed candidate pool.

| Item | Setting |
| --- | --- |
| input | `source_lang`, `target_lang`, source `item_id` |
| candidate pool | all target-language test items in the same split |
| score | cosine similarity |
| metrics | Recall@1, Recall@5, MRR, median rank |
| directions | `eng->target`, `target->eng`, and target-target where overlap permits |

This is the cleanest translation-style task for an encoder-only model.

### Task B: Translation Pair Classification

Definition:

Classify whether two sentences in different languages express the same semantic item.

Features:

| Feature | Formula |
| --- | --- |
| cosine | `cos(e1, e2)` |
| abs diff | `abs(e1 - e2)` |
| product | `e1 * e2` |
| optional language ids | only for diagnostic, not main zero-shot result |

Classifiers:

| Classifier | Role |
| --- | --- |
| cosine threshold | no-train baseline |
| logistic regression | primary frozen-feature classifier |
| shallow MLP | ablation only |

Train on high-resource or train-split pairs. Evaluate on target10 held-out language pairs. Metrics: accuracy, macro F1, AUROC, AUPRC, pairwise MRR.

### Task C: Bible Topic / Taxi1500 Classification

Definition:

Use frozen sentence embeddings to classify verse/topic labels.

Preferred version:

| Train | Eval | Claim |
| --- | --- | --- |
| English Taxi1500 train | target10 Taxi1500 test | strongest classification claim |

Fallback version:

| Train | Eval | Claim |
| --- | --- | --- |
| English or high-resource fixed-label Bible train | target10 held-out Bible test | acceptable if labels are external and split-clean |

Model:

1. Extract frozen embeddings.
2. Train logistic regression or linear probe on train embeddings.
3. Select hyperparameters on dev only.
4. Evaluate target10 test once.

Metrics: accuracy, macro F1, per-language F1, class-balanced accuracy.

Do not use book/chapter labels as the main classification task. That task is too vulnerable to lexical/domain shortcuts and can only be a diagnostic sanity check.

### Task D: Few-Shot Target10 Classification

Definition:

If zero-shot classification is too sparse, use a tiny target-language train set and evaluate held-out target examples.

Settings:

| Shot | Use |
| --- | --- |
| 1-shot per class | stress test |
| 5-shot per class | low-resource practical setting |
| 10-shot per class | upper low-resource setting |

This is weaker than zero-shot transfer but useful for checking whether the embedding space is linearly usable in each low-resource language.

## Downstream Gate

`PASS_EMBEDDING_DOWNSTREAM_READY` requires:

1. Translation retrieval macro MRR improves over XLM-R-base.
2. Pair classification macro F1 or AUROC improves over XLM-R-base.
3. Classification macro F1 improves over XLM-R-base on the primary fixed-label task.
4. At least `7/10` target languages improve on the primary downstream metric.
5. `cop` and `syr` are explicitly reported.
6. Results are stable over model seeds `13/17/23` where candidate checkpoints exist.
7. High-resource control degradation remains within the no-collapse threshold.

If alignment improves but downstream tasks do not, the allowed claim is:

> The representation space becomes more cross-lingually aligned by retrieval/margin diagnostics, but the frozen embeddings do not yet produce broad target10 downstream gains.

## Artifact Plan

| Artifact | Path |
| --- | --- |
| item manifest | `10_embedding_alignment_downstream/parallel_item_manifest.tsv` |
| split manifest | `10_embedding_alignment_downstream/split_manifest.tsv` |
| embedding cache manifest | `10_embedding_alignment_downstream/embedding_cache_manifest.tsv` |
| alignment metrics | `10_embedding_alignment_downstream/alignment_scores.tsv` |
| language-pair retrieval | `10_embedding_alignment_downstream/retrieval_scores.tsv` |
| semantic margins | `10_embedding_alignment_downstream/semantic_margin_scores.tsv` |
| hubness report | `10_embedding_alignment_downstream/hubness_scores.tsv` |
| 2D map points | `10_embedding_alignment_downstream/map_points.tsv` |
| figure directory | `10_embedding_alignment_downstream/figures/` |
| downstream task manifest | `10_embedding_alignment_downstream/downstream_task_manifest.tsv` |
| pair classification results | `10_embedding_alignment_downstream/pair_classification_results.tsv` |
| topic classification results | `10_embedding_alignment_downstream/topic_classification_results.tsv` |
| few-shot results | `10_embedding_alignment_downstream/fewshot_classification_results.tsv` |
| final summary | `10_embedding_alignment_downstream/results.md` |

## Execution Order

1. Build `parallel_item_manifest.tsv`.
   - Include every target10 language with shared `item_id`s.
   - Record missing verses/sentences explicitly.

2. Freeze train/dev/test splits.
   - Prefer book/chapter-group split.
   - Mark any overlap and remove duplicate text leakage.

3. Extract embeddings.
   - XLM-R-base first.
   - Current replay-safe third_try checkpoints next.
   - Future positive-route checkpoints use the same script and manifest.

4. Run alignment scoring.
   - Compute cosine matrix.
   - Compute retrieval, margin, centroid, language silo, and hubness metrics.

5. Generate 2D maps.
   - Same item sample across models.
   - UMAP primary; t-SNE/PCA sensitivity.

6. Define downstream datasets.
   - Translation retrieval candidate pools.
   - Translation pair classification positives/negatives.
   - Taxi1500 or Bible topic classification labels.

7. Run frozen-feature downstream.
   - Logistic regression primary.
   - Cosine threshold baseline for pair classification.
   - Shallow MLP only as ablation.

8. Write gate summary.
   - If both alignment and downstream pass, this can support broad target10 embedding/model improvement.
   - If only alignment passes, keep it diagnostic.
   - If neither passes, return to tokenizer/init/training schedule redesign.

## Claim Boundary

Allowed if gates pass:

> The third_try candidate improves cross-lingual semantic alignment of target10 low-resource languages in XLM-R embedding space and improves frozen-embedding downstream transfer on translation retrieval/pair classification and topic classification.

Not allowed from this stage alone:

> The model performs free-form translation better.

> The model improves all downstream tasks.

> A visually better 2D map proves downstream improvement.

