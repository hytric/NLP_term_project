# Experiment 2 Plan: Downstream Tasks From Embedding Vectors

작성일: 2026-06-18

## Goal

Define downstream tasks directly on encoder embedding vectors and test whether third_try/v3.1 embeddings are more useful than XLM-R-base.

The first pass uses frozen embeddings only. This avoids hiding representation failure behind encoder fine-tuning.

## Inputs From Experiment 1

| Input | Use |
| --- | --- |
| cached embeddings | frozen features |
| split manifest | train/dev/test discipline |
| language-pair retrieval matrix | translation retrieval candidate pools |
| positive/hard-negative pair manifest | pair classification |
| topic/class labels | classification probe |

## Task A: Translation Retrieval

Definition:

Given a source sentence vector, retrieve the aligned target sentence from a fixed target-language candidate pool.

| Field | Setting |
| --- | --- |
| directions | `eng->target`, `target->eng`, target-target when overlap permits |
| score | cosine; CSLS sensitivity if hubness is high |
| candidate pool | all target-language test items |
| metrics | Recall@1, Recall@5, MRR, median rank |
| model training | none |

This is the main translation-style task for an encoder-only model.

## Task B: Translation Pair Classification

Definition:

Classify whether a pair of sentences in different languages has the same semantic `item_id`.

Features:

| Feature | Formula |
| --- | --- |
| cosine | `cos(e1, e2)` |
| absolute difference | `abs(e1 - e2)` |
| elementwise product | `e1 * e2` |

Classifiers:

| Classifier | Role |
| --- | --- |
| cosine threshold | no-train baseline |
| logistic regression | primary frozen-feature classifier |
| shallow MLP | ablation only |

Train/eval:

- train on train split pairs;
- tune threshold / regularization on dev;
- evaluate target10 test once.

Metrics:

- macro F1;
- AUROC;
- AUPRC;
- accuracy;
- language-pair breakdown.

## Task C: Topic / Taxi1500-Style Classification

Preferred:

| Train | Eval |
| --- | --- |
| English Taxi1500 train | target10 Taxi1500 test |

Fallback:

| Train | Eval |
| --- | --- |
| English/high-resource fixed-label Bible train | target10 held-out Bible test |

Model:

1. Freeze embeddings.
2. Train logistic regression or linear probe.
3. Select hyperparameters on dev.
4. Evaluate target10 test once.

Metrics:

- macro F1;
- class-balanced accuracy;
- per-language F1;
- per-class confusion.

Blocked as main:

- book/chapter prediction;
- labels derived from target test text;
- classifier selected on final test.

## Task D: Few-Shot Target10 Probe

If zero-shot classification is infeasible:

| Setting | Meaning |
| --- | --- |
| 1-shot per class | stress test |
| 5-shot per class | low-resource practical setting |
| 10-shot per class | upper low-resource setting |

Few-shot is not as strong as zero-shot classification. It belongs in the main text only if clearly labeled as few-shot frozen-feature transfer.

## Gate

`PASS_EMBEDDING_DOWNSTREAM_READY` requires:

1. Translation retrieval macro MRR improves over XLM-R-base.
2. Pair classification macro F1 or AUROC improves over XLM-R-base.
3. Topic/classification macro F1 improves over XLM-R-base on the primary fixed-label task.
4. At least `7/10` target languages improve on the primary downstream metric.
5. `cop` and `syr` are explicitly reported.
6. Model-seed variance is recorded where candidate checkpoints exist.
7. High-resource control degradation remains within the v3 no-collapse threshold.

Failure labels:

| Label | Meaning |
| --- | --- |
| `PASS_ALIGNMENT_ONLY` | Experiment 1 improves but downstream fails |
| `FAIL_TRANSFER` | frozen embeddings do not help classification/retrieval |
| `FAIL_LABEL_COVERAGE` | target10 classification labels unavailable |
| `FAIL_SEED_STABILITY` | one seed improves but 3-seed summary does not |

## Outputs

| Artifact | Path |
| --- | --- |
| task manifest | `downstream_task_manifest.tsv` |
| retrieval results | `retrieval_downstream_results.tsv` |
| pair classification results | `pair_classification_results.tsv` |
| topic classification results | `topic_classification_results.tsv` |
| few-shot results | `fewshot_classification_results.tsv` |
| qualitative examples | `nearest_neighbor_examples.md`, `classification_errors.md` |
| summary | `results.md` |

