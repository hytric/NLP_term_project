# Init MLM Probe Results

작성일: 2026-06-19

## Setup

- Task: masked language modeling continued training, same train/dev files as Stage05.
- Budget: `200` optimizer steps, seed `13`, LR `5e-5`, batch `4`, gradient accumulation `8`, max length `512`, MLM probability `0.15`.
- Compared initialization methods: `random`, `mean`, `fvt`, `align`, `focus`.
- Zero-step loss is kept only as a sanity baseline; the ranking below uses final dev MLM loss after training.
- Masking protocol: standard token-level MLM with `15%` selected non-special tokens and BERT-style `80/10/10` replacement; see `mlm_training_protocol.md`.

## Train/Eval Set

| Split | File | Raw lines | HF chunked samples | Role | Used in probe |
| --- | --- | ---: | ---: | --- | --- |
| train | `mlm_train_full_mixture.txt` | 966,152 | 136,039 | full MLM mixture | shuffled source for 200 optimizer steps |
| eval | `target10_dev.txt` | 6,521 | 701 | target10 low-resource dev | full dev evaluation |
| final_test | `target10_final_test.txt` | 9,804 | not used | target10 held-out final | not used in this ablation |

The train file is the full Stage01 MLM mixture, but this probe is not a full-epoch run. With batch `4` and gradient accumulation `8`, each optimizer step sees about `32` chunks, so `200` steps consume about `6,400` shuffled 512-token chunks from the 136,039-chunk train dataset. Trainer logs this as roughly epoch `0.05`.

Train mixture composition:

| Component | Lines | Role |
| --- | ---: | --- |
| target10 low-resource train | 52,016 | target-language adaptation signal |
| GlotCC eng/deu/jpn/kor replay | 800,000 | high-resource replay/control, 200,000 lines each |
| Bible eng/deu/jpn/kor control | 114,136 | domain-matched replay/control |
| total | 966,152 | `mlm_train_full_mixture.txt` |

Target10 low-resource split rows:

| ISO | Language | Script | Train rows | Dev rows | Final rows |
| --- | --- | --- | ---: | ---: | ---: |
| acu | Achuar-Shiwiar | Latin | 5,168 | 659 | 953 |
| ake | Akawaio | Latin | 5,178 | 673 | 1,003 |
| bsn | Barasana-Eduria | Latin | 5,063 | 629 | 959 |
| chr | Cherokee | Cherokee | 5,393 | 678 | 1,007 |
| cop | Coptic | Coptic | 5,388 | 678 | 1,003 |
| kbh | Camsa | Latin | 4,505 | 501 | 852 |
| nhg | Nahuatl Tetelcingo | Latin | 5,267 | 673 | 1,006 |
| oji | Ojibwa | Aboriginal Syllabics | 5,384 | 674 | 1,007 |
| syr | Syriac | Syriac | 5,376 | 678 | 1,007 |
| usp | Uspanteco | Latin | 5,294 | 678 | 1,007 |
| total | target10 | mixed | 52,016 | 6,521 | 9,804 |

## Result

| Rank | Init | Zero-step dev loss | Final dev loss | Drop | Delta vs fvt | Perplexity |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `fvt` | 7.925527 | 3.921798 | 4.003729 | 0.000000 | 50.491170 |
| 2 | `focus` | 16.760191 | 3.931313 | 12.828878 | 0.009515 | 50.973852 |
| 3 | `align` | 8.700895 | 4.060271 | 4.640624 | 0.138473 | 57.990012 |
| 4 | `random` | 17.998567 | 4.937548 | 13.061019 | 1.015750 | 139.427975 |
| 5 | `mean` | 10.910376 | 5.835072 | 5.075304 | 1.913274 | 342.089214 |

## Reading

This ablation answers the user's concern that initialization should not be judged immediately after row creation. All five variants are trained with the same masked-prediction objective and schedule before comparison.

Under this single-seed `200`-step budget, `fvt` has the best final dev MLM loss. The gap to `focus` is only `0.009515` loss, so this should be reported as a sensitivity result rather than a decisive final-method proof.

The same MLM dev split was also reused for a same-meaning encoder feature-similarity probe. Rows were reconstructed with verse ids from the v3.1 parallel item manifest, then evaluated over all 90 directed target10 language pairs. This is a semantic-feature diagnostic, not an MLM-loss metric.

Key feature-similarity result:

| Model | Phase | Same cosine | Macro margin | Macro R@1 | Macro MRR |
| --- | --- | ---: | ---: | ---: | ---: |
| `xlmr_base` | baseline | 0.986126 | -0.003000 | 0.006874 | 0.020418 |
| `mean_mlm200` | 200-step MLM | 0.996556 | -0.001656 | 0.005724 | 0.022055 |
| `random_mlm200` | 200-step MLM | 0.993669 | -0.002612 | 0.005793 | 0.021748 |
| `fvt_mlm200` | 200-step MLM | 0.990975 | -0.002530 | 0.004551 | 0.019034 |

Reading: `fvt` wins MLM dev loss, but not same-meaning feature retrieval. Absolute cosine is high for all models, while Recall@1/MRR remain weak. So MLM token prediction, absolute cosine, and semantic retrieval should be reported as separate diagnostics.

Interpretation rule:

- if `fvt` remains best after training, the claim is that subtoken-composition initialization gives a better adaptation starting point, not merely a lower zero-step loss;
- if another method catches up or wins, initialization is mostly washed out by MLM adaptation under this budget;
- if high zero-step methods improve but remain behind, report the result as sensitivity rather than a final method claim.

## Artifacts

- Configs: `docs/exp/v3.1/04_ablation/init_mlm_probe/configs/`
- MLM protocol: `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_training_protocol.md`
- Aggregated table: `docs/exp/v3.1/04_ablation/init_mlm_probe/init_mlm_probe_results.tsv`
- Same-meaning feature similarity: `docs/exp/v3.1/04_ablation/init_mlm_probe/feature_similarity_results.md`
- Checkpoints: `/home/axt/mnt2/jongha/v3_1/init_mlm_probe_200step/`
