# Experiment 1 Results: Embedding Alignment

작성일: 2026-06-18

Gate status: `ALIGNMENT_DECODER_LINK_CSLS_DONE_WEAK_RETRIEVAL`

## Summary

The `v3.1` parallel item manifest was materialized from the same v3/v1 Bible split lineage used by `docs/exp/v3`. Encoder embedding alignment was then evaluated on the same Coptic-Syriac dev/final splits used by the decoder experiment.

| Item | Count |
| --- | ---: |
| all parallel rows | `217689` |
| target10 rows | `93297` |
| high-resource rows | `124392` |
| translation pair files | `22` |

## Split Evidence

The generated split manifest is:

`docs/exp/v3.1/01_embedding_alignment/split_manifest.tsv`

Key shared target10 overlap:

| Split | Shared item count |
| --- | ---: |
| train | `3029` |
| dev | `456` |
| final_test | `782` |
| burned_excluded | `625` |

## Command

```bash
python3 preprocessing/build_v31_parallel_items.py
```

Alignment/decoder-link command:

```bash
CUDA_VISIBLE_DEVICES=2 python3 modeling/run_v31_embedding_alignment.py \
  --batch-size 16 \
  --max-length 256

python3 modeling/aggregate_v31_alignment_results.py
python3 modeling/build_v31_alignment_maps.py --split final_test
python3 modeling/run_v31_csls_alignment.py \
  --directions 'cop->syr' 'syr->cop' \
  --splits dev final_test
```

## Models Evaluated

| Model | Role |
| --- | --- |
| `xlm-roberta-base` | baseline |
| `fvt_replay_safe_lr1e5_seed13_step1000` | third_try candidate |
| `fvt_replay_safe_lr1e5_seed17_step1000` | third_try candidate |
| `fvt_replay_safe_lr1e5_seed23_step1000` | third_try candidate |

Pooling:

- last hidden state;
- mean pooling over non-padding tokens;
- L2 normalization;
- exact item-id retrieval over the paired split.

## Decoder-Link Summary

The candidate improves decoder chrF++ and also improves retrieval/margin metrics, but absolute retrieval remains very weak.

| Direction | Split | Decoder chrF++ Delta | MRR Delta | Recall@1 Delta | Margin Delta | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `cop -> syr` | final_test | `+2.2667` | `+0.0031` | `+0.0017` | `+0.0023` | weak alignment gain |
| `syr -> cop` | final_test | `+3.4949` | `+0.0075` | `+0.0013` | `+0.0009` | weak alignment gain |

Final-test absolute retrieval:

| Direction | Model | Recall@1 | Recall@5 | MRR | Hubness@10 max rate |
| --- | --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | XLM-R-base | `0.0010` | `0.0050` | `0.0079` | `1.0000` |
| `cop -> syr` | third_try mean | `0.0027` | `0.0086` | `0.0111` | `0.9848` |
| `syr -> cop` | XLM-R-base | `0.0020` | `0.0070` | `0.0090` | `0.9821` |
| `syr -> cop` | third_try mean | `0.0033` | `0.0116` | `0.0164` | `0.6478` |

## Interpretation

The alignment result supports a cautious decoder-link claim:

> third_try replay-safe checkpoints improve both simple-decoder chrF++ and same-item embedding retrieval/margin relative to XLM-R-base on the Coptic-Syriac final split.

However, it does not support a strong semantic-transfer claim yet:

- Recall@1 remains below `0.4%` for all final-test candidate directions.
- `cop -> syr` hubness remains extreme; one or a few target points still dominate top-10 retrieval.
- aligned cosine is very high for all models, suggesting anisotropy; raw cosine alone is not enough.
- decoder outputs remain repetitive, so part of the chrF++ gain may come from tokenizer/script recovery rather than sentence-level semantic translation.

The right paper framing is:

> append-only low-resource adaptation gives a measurable weak alignment signal and prevents target-script collapse in a simple decoder probe, but stronger retrieval/CSLS and generation diagnostics are required before claiming robust semantic translation.

## CSLS and Centered Retrieval

Raw cosine has severe anisotropy and hubness, so the same cached embeddings were re-scored with centered cosine and CSLS.

Script:

`modeling/run_v31_csls_alignment.py`

Score types:

| Score type | Meaning |
| --- | --- |
| `raw_cosine` | original L2-normalized dot product |
| `centered_cosine` | subtract side centroid, then L2-normalize |
| `csls_k10` | CSLS with `k=10` on raw normalized embeddings |
| `centered_csls_k10` | CSLS with `k=10` after centering |

Final-test summary:

| Direction | Score type | Baseline MRR | Candidate MRR | Delta | Baseline hubness@10 max | Candidate hubness@10 max | Delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `raw_cosine` | `0.0079` | `0.0111` | `+0.0031` | `1.0000` | `0.9848` | `-0.0152` |
| `cop -> syr` | `csls_k10` | `0.0078` | `0.0133` | `+0.0055` | `0.9970` | `0.9032` | `-0.0938` |
| `cop -> syr` | `centered_csls_k10` | `0.0099` | `0.0219` | `+0.0120` | `0.3151` | `0.1057` | `-0.2094` |
| `syr -> cop` | `raw_cosine` | `0.0090` | `0.0164` | `+0.0075` | `0.9821` | `0.6478` | `-0.3343` |
| `syr -> cop` | `csls_k10` | `0.0087` | `0.0222` | `+0.0136` | `0.8588` | `0.4278` | `-0.4311` |
| `syr -> cop` | `centered_csls_k10` | `0.0124` | `0.0220` | `+0.0096` | `0.1730` | `0.0418` | `-0.1312` |

Interpretation:

- CSLS/centering reduces hubness substantially, especially for `syr -> cop`.
- Candidate MRR remains higher than XLM-R-base after hubness correction.
- `centered_csls_k10` gives the cleanest hubness profile, but Recall@1 remains below `1%`.
- Therefore CSLS strengthens the weak-alignment diagnostic, but still does not justify a strong semantic retrieval claim.

## 2D Map

PCA map points were generated for the final-test split:

| Artifact | Path |
| --- | --- |
| map points | `docs/exp/v3.1/01_embedding_alignment/map_points.tsv` |
| figure manifest | `docs/exp/v3.1/01_embedding_alignment/map_figure_manifest.tsv` |
| figures | `docs/exp/v3.1/01_embedding_alignment/figures/*.png` |

The PCA maps are qualitative diagnostics only. They should be discussed with retrieval, margin, and hubness metrics because visually close clusters can still have poor exact item retrieval.

Visual inspection note:

- `xlmr_base_cop_to_syr_final_test_pca.png` and `fvt_seed17_cop_to_syr_final_test_pca.png` are nonblank and render correctly.
- Both show strong source/target separation in PCA space.
- Therefore the current 2D maps do not support a strong "languages are mixed in one semantic manifold" claim.
- The maps are consistent with the quantitative reading: weak retrieval/margin improvement, but language/script silo remains.

## Artifacts

| Artifact | Path |
| --- | --- |
| parallel item manifest | `docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv` |
| split summary | `docs/exp/v3.1/01_embedding_alignment/split_manifest.tsv` |
| translation manifest | `docs/exp/v3.1/03_decoder_translation/translation_data_manifest.tsv` |
| pair files | `/home/axt/mnt2/jongha/v3_1/translation_pairs/*.tsv` |
| embedding cache manifest | `docs/exp/v3.1/01_embedding_alignment/embedding_cache_manifest.tsv` |
| alignment scores | `docs/exp/v3.1/01_embedding_alignment/alignment_scores.tsv` |
| retrieval scores | `docs/exp/v3.1/01_embedding_alignment/retrieval_scores.tsv` |
| semantic margin scores | `docs/exp/v3.1/01_embedding_alignment/semantic_margin_scores.tsv` |
| hubness scores | `docs/exp/v3.1/01_embedding_alignment/hubness_scores.tsv` |
| decoder/alignment join | `docs/exp/v3.1/01_embedding_alignment/decoder_alignment_join.tsv` |
| decoder/alignment deltas | `docs/exp/v3.1/01_embedding_alignment/decoder_alignment_delta_summary.tsv` |
| CSLS/centered retrieval scores | `docs/exp/v3.1/01_embedding_alignment/csls_retrieval_scores.tsv` |
| CSLS/centered metric summary | `docs/exp/v3.1/01_embedding_alignment/csls_retrieval_metric_summary.tsv` |
| CSLS decoder/alignment deltas | `docs/exp/v3.1/01_embedding_alignment/csls_decoder_alignment_delta_summary.tsv` |
| PCA map points | `docs/exp/v3.1/01_embedding_alignment/map_points.tsv` |
| PCA figures | `docs/exp/v3.1/01_embedding_alignment/figures/*.png` |

## Next Gate

Required next outputs:

1. target10-wide alignment beyond only Coptic-Syriac;
2. link CSLS/centered metrics into Experiment 2 downstream probes;
3. add generation-specific repetition/EOS diagnostics before making translation-quality claims.
