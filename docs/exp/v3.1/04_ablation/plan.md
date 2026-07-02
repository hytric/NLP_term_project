# Ablation Placement Plan

작성일: 2026-06-18

## Purpose

`v3.1` ablations explain sensitivity. They do not replace the three main experiments.

Main experiments:

1. Experiment 1: semantic embedding alignment + 2D map.
2. Experiment 2: embedding-vector downstream tasks.
3. Experiment 3: simple decoder translation task.

Ablations are placed after the main metric definitions are frozen.

## Main vs Ablation Boundary

Main result requires:

- XLM-R-base baseline;
- target10 language set;
- fixed train/dev/test split;
- layer 8 mean-pooled embeddings by default;
- cosine retrieval/margin plus hubness diagnostics;
- frozen embedding downstream tasks;
- simple decoder translation with identical decoder setup across encoders;
- seed summary where candidate checkpoints have multiple seeds;
- explicit Coptic/Syriac rows.

Ablation only:

- layer choice other than layer 8;
- CLS pooling instead of mean pooling;
- UMAP vs t-SNE/PCA differences;
- CSLS vs cosine sensitivity;
- no-hard-negative pair construction;
- book/chapter classification;
- shallow MLP probe;
- encoder fine-tuning after frozen-feature probe;
- large encoder-decoder NMT generation;
- decoder architecture changes used only for the candidate but not XLM-R-base baseline;
- tokenizer/init/training variations inherited from v3.

## Ablation Matrix

| Axis | Main value | Ablation values | Question answered |
| --- | --- | --- | --- |
| embedding layer | layer 8 | last layer, last-4 average | Is alignment layer-dependent? |
| pooling | attention-mask mean | CLS | Is the signal a pooling artifact? |
| similarity | cosine | CSLS, dot product | Does hubness distort nearest neighbors? |
| negatives | hard negatives included | easy negatives only | Are gains semantic or topic shortcuts? |
| map method | UMAP | t-SNE, PCA | Is the 2D story stable? |
| candidate pool | full target-language test pool | reduced/balanced pool | Does retrieval depend on pool difficulty? |
| classifier | logistic regression | cosine threshold, shallow MLP | Is downstream gain linearly available? |
| decoder depth | 1-2 layer simple decoder | larger decoder, extra adapters | Is translation gain from encoder or decoder capacity? |
| encoder update | frozen encoder | top-layer unfreeze, LoRA | Does generation require encoder adaptation? |
| label task | Taxi1500/fixed-topic labels | book/chapter labels | Are classification gains task-real or shortcut-prone? |
| tokenizer | v3 selected append tokenizer | 32k/48k/script-balanced/byte fallback | Do tokenizer choices affect embedding alignment? |
| initialization | v3 `fvt` | mean, align, focus-like | Does new-token initialization affect semantic attachment? |
| training | replay-safe full MLM candidate | target-only, no-replay, LoRA, new-row-only repair | Does adaptation preserve multilingual space? |
| checkpoint | selected candidate | earlier checkpoints | Is alignment rescued by earlier stopping? |

## Completed Ablation: Init MLM Probe

The initial v3 table compared `random`, `mean`, `fvt`, `align`, and `focus` immediately after embedding-row creation. That zero-step comparison is only a sanity check.

For v3.1, all five initialization methods were trained with the same masked language modeling objective and the same 200-step Stage05 pilot budget before comparison.

| Rank | Init | Zero-step dev loss | Final dev loss | Delta vs fvt |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | 7.925527 | 3.921798 | 0.000000 |
| 2 | `focus` | 16.760191 | 3.931313 | 0.009515 |
| 3 | `align` | 8.700895 | 4.060271 | 0.138473 |
| 4 | `random` | 17.998567 | 4.937548 | 1.015750 |
| 5 | `mean` | 10.910376 | 5.835072 | 1.913274 |

Reading: `fvt` is still the best single-seed 200-step result, but the margin over `focus` is tiny. This should be reported as initialization sensitivity after MLM adaptation, not as decisive proof that the initialization method alone determines downstream quality.

Artifacts:

- `docs/exp/v3.1/04_ablation/init_mlm_probe/results.md`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/init_mlm_probe_results.tsv`
- `/home/axt/mnt2/jongha/v3_1/init_mlm_probe_200step/`

### MLM Dev Feature-Similarity Probe

The same MLM dev set can be reused for encoder output feature similarity because the manifest preserves the shared verse `item_id`. The plain `target10_dev.txt` has only text, but `docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv` reconstructs language, script, and same-meaning ids.

The completed probe uses:

- split: target10 MLM dev;
- languages: all 10 target languages;
- rows: 6,521 unique dev rows;
- pairs: 90 directed target10 language pairs;
- representation: last hidden state, attention-mask mean pooling, L2 normalization;
- metrics: same cosine, hard-negative margin, Recall@1/5, MRR, hubness.

Summary:

| Model | Phase | Same cosine | Macro margin | Macro R@1 | Macro MRR |
| --- | --- | ---: | ---: | ---: | ---: |
| `xlmr_base` | baseline | 0.986126 | -0.003000 | 0.006874 | 0.020418 |
| `mean_mlm200` | 200-step MLM | 0.996556 | -0.001656 | 0.005724 | 0.022055 |
| `random_mlm200` | 200-step MLM | 0.993669 | -0.002612 | 0.005793 | 0.021748 |
| `fvt_mlm200` | 200-step MLM | 0.990975 | -0.002530 | 0.004551 | 0.019034 |

Reading: `fvt` wins the MLM-loss ablation, but it does not win the same-meaning encoder feature retrieval probe. This is useful negative evidence: MLM loss and semantic feature alignment must be evaluated separately.

Artifacts:

- `docs/exp/v3.1/04_ablation/init_mlm_probe/feature_similarity_results.md`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_summary.tsv`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_pair_scores.tsv`

## Placement In Report

Recommended report order:

1. Main method and data.
2. Experiment 1 main alignment result.
3. Experiment 2 main downstream result.
4. Experiment 3 simple decoder translation result.
5. Ablation section:
   - representation extraction ablations;
   - retrieval/pair construction ablations;
   - downstream classifier ablations;
   - decoder depth/freeze/unfreeze ablations;
   - inherited tokenizer/init/training ablations from v3.
6. Error analysis:
   - language silos;
   - high-resource hubs;
   - Coptic/Syriac specific failures;
   - nearest-neighbor examples.

## Reusing V3 Ablations

Carry forward these v3 findings as background/ablation, not main evidence:

| V3 axis | V3 reading | V3.1 use |
| --- | --- | --- |
| vocab size | 48k improved average tokenization but not model quality | motivate tokenizer sensitivity ablation |
| byte fallback | tokenizer metric improvement but implementation mismatch | keep as tokenizer ablation only |
| init method | `fvt` best zero-step/pilot choice | compare alignment across init methods if checkpoints exist |
| replay/control | high-resource control failed in v3 | keep high-resource hub/control diagnostics mandatory |
| appended-token learning | tokenizer gains did not become model gains | check whether semantic alignment is the missing bridge |
| free-form translation | prior NMT collapsed or retrieval-dominated | reintroduce only as simple-decoder final task with strict baselines |

## Gate

`PASS_ABLATION_PACKAGE_READY` requires:

1. Every ablation has a clear main-axis contrast.
2. No ablation is promoted to main claim without satisfying the main gates.
3. Shortcut-prone tasks are labeled diagnostic.
4. Negative ablations are reported, not hidden.
5. Coptic/Syriac deviations are explicit.
