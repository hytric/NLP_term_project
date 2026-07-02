# Experiment 2 Results: Embedding-Vector Downstream Tasks

작성일: 2026-06-18

Gate status: `PAIR_CLASSIFICATION_DONE_MIXED`

## Scope

This first downstream pass uses frozen encoder embeddings from the same Coptic-Syriac data lineage as Experiment 1 and Experiment 3.

Task:

> classify whether a cross-lingual sentence pair is the same Bible verse item.

The classifier sees only frozen embedding-derived features. The encoder is not fine-tuned.

## Data

Pair files:

| Direction | Pair file | Train pairs | Dev pairs | Final pairs |
| --- | --- | ---: | ---: | ---: |
| `cop -> syr` | `/home/axt/mnt2/jongha/v3_1/translation_pairs/cop_to_syr.tsv` | `5389` | `678` | `1006` |
| `syr -> cop` | `/home/axt/mnt2/jongha/v3_1/translation_pairs/syr_to_cop.tsv` | `5389` | `678` | `1006` |

For each split, the evaluation set contains:

- positive pairs: same `item_id`;
- shifted negatives: deterministic different target verse;
- hard negatives: nearest non-matching target verse under the evaluated model embedding.

This gives a positive rate of about `0.3333`. The hard-negative setting is intentionally stricter than a random-negative sanity check.

## Method

Script:

`modeling/run_v31_pair_classification.py`

Models:

| Model | Role |
| --- | --- |
| `xlm-roberta-base` | baseline |
| `fvt_replay_safe_lr1e5_seed13_step1000` | third_try candidate |
| `fvt_replay_safe_lr1e5_seed17_step1000` | third_try candidate |
| `fvt_replay_safe_lr1e5_seed23_step1000` | third_try candidate |

Classifiers:

| Classifier | Feature set | Selection |
| --- | --- | --- |
| cosine threshold | `cosine(e_src, e_tgt)` | threshold tuned on dev macro F1 |
| logistic regression | `cosine` | `C` selected on dev macro F1 |
| logistic regression | `abs(e_src - e_tgt) + e_src * e_tgt + cosine` | `C` selected on dev macro F1 |

Note: the full run emitted sklearn convergence warnings for some logistic-regression fits. Treat this as a diagnostic frozen-feature probe, not as a final tuned classifier benchmark.

## Main Result

The strongest and most interpretable downstream signal is the logistic-regression probe using `abs-diff + product + cosine` features.

Final-test summary:

| Direction | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

This supports a cautious downstream claim:

> With a frozen encoder and a shallow pair classifier, third_try embeddings separate same-verse Coptic-Syriac pairs from shifted/hard negatives better than XLM-R-base on the final split.

## Raw-Cosine Result

Raw cosine remains weak and inconsistent.

Final-test summary:

| Direction | Classifier | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | cosine threshold | `0.4000` | `0.4000` | `+0.0000` | `0.2588` | `0.2875` | `+0.0288` |
| `cop -> syr` | logistic on cosine | `0.6791` | `0.6422` | `-0.0370` | `0.7412` | `0.7125` | `-0.0288` |
| `syr -> cop` | cosine threshold | `0.3983` | `0.4677` | `+0.0694` | `0.3947` | `0.4805` | `+0.0857` |
| `syr -> cop` | logistic on cosine | `0.5463` | `0.4871` | `-0.0591` | `0.6053` | `0.5195` | `-0.0857` |

Interpretation:

- raw cosine alone does not give a stable pair-classification gain;
- same-item retrieval and raw cosine are still affected by anisotropy/hubness;
- the positive downstream signal appears when the probe can use pairwise difference/product structure.

## Artifacts

| Artifact | Path |
| --- | --- |
| raw pair-classification scores | `pair_classification_results.tsv` |
| mean/std summary | `pair_classification_metric_summary.tsv` |
| baseline-candidate deltas | `pair_classification_delta_summary.tsv` |
| embedding cache manifest | `pair_classification_cache_manifest.tsv` |
| downstream run manifest | `downstream_task_manifest.tsv` |
| train embedding cache | `/home/axt/mnt2/jongha/v3_1/embedding_downstream/pair_classification/*` |

## Claim Boundary

Allowed:

> third_try gives a positive frozen-feature pair-classification signal on Coptic-Syriac final-test pairs when evaluated with a shallow pairwise linear probe.

Not allowed yet:

> target10-wide downstream transfer is solved.

> raw cosine similarity alone proves robust semantic alignment.

> the representation is ready for high-quality generation.

## Next Evidence Needed

1. connect the completed CSLS/centered retrieval metrics to the pair-classification analysis;
2. extend pair classification beyond only Coptic-Syriac where target10 overlap permits;
3. add a fixed-label topic/classification probe if labels can be materialized without test leakage;
4. repeat the linear probe after any tokenizer/MLM ablation that changes the encoder.
