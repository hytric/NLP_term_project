# Progress Report Draft

작성일: 2026-06-04

## Title

Target10 Low-Resource Multilingual Adaptation with Coptic/Syriac Translation Diagnostics

## One-Sentence Summary

We extend a Glot500-style model to 10 low-resource languages, show that tokenizer extension and mean embedding initialization improve representation-side readiness, and find that downstream Coptic/Syriac generation still requires stronger source-grounding than the current direct, pivot, or retrieval-augmented neural setups provide.

## Project Scope

Target10 languages:

- Coptic
- Syriac
- Cherokee
- Ojibwa
- Barasana-Eduria
- Uspanteco
- Nahuatl (Tetelcingo)
- Akawaio
- Camsa
- Achuar-Shiwiar

Downstream case study:

- Coptic/Syriac translation and pivot/retrieval diagnostics.

## Completed Evidence

### Data

- Bible-derived target10 pilot data was prepared.
- Each target language has train/dev/test split counts documented.
- Shared 10-language verse overlap: 4,892.

### Tokenization

The merged target10 tokenizer substantially reduces Glot500 overfragmentation:

| Language | Glot500 tokens/word | Merged target10 tokens/word | Reduction |
| --- | ---: | ---: | ---: |
| Syriac | 5.089 | 1.601 | 68.5% |
| Coptic | 5.274 | 1.779 | 66.3% |
| Cherokee | 5.254 | 2.001 | 61.9% |
| Ojibwa | 5.021 | 2.205 | 56.1% |

Figure artifact:

- `docs/exp/2026-06-03_08_evaluation_analysis/figures/target10_tokenization_reduction.png`

### Embedding Initialization And MLM

Mean initialization is the selected representation checkpoint:

| Init | Stable eval loss | Stable perplexity | Decision |
| --- | ---: | ---: | --- |
| Random | 7.0169 | 1,115.29 | ablation/control |
| Mean | 5.8343 | 341.84 | selected |

Active adapted encoder candidate:

- `docs/exp/2026-06-03_05_mlm_adaptation/pilot10k_mean`

### NMT And Retrieval

Direct NMT runs complete but are not usable translations:

- Coptic -> Syriac full1epoch: chrF++ 5.7982.
- Syriac -> Coptic full1epoch: chrF++ 9.9340, but max-length repetitive output.

Retrieval is much stronger as a baseline:

- English -> Coptic retrieval: chrF++ 22.3584.
- Syriac -> Coptic retrieval: chrF++ 22.2083.
- English -> Coptic top8 oracle: chrF++ 28.3327.
- Top8 feature reranker: chrF++ 24.5921.

Neural retrieval augmentation is promising but copy-heavy:

- Normal retrieval + Coptic autoencoding: chrF++ 19.6952 on 64-example slice.
- Feature-selected top8 hint: chrF++ 19.9182 on the same slice.
- Wrong-retrieval/source-only controls show the model follows the retrieved hint more than the English source.

Source-candidate diagnostics now support the next selection objective:

- 10A CPU diagnostic rows: 879.
- Sentence-level top1 candidate mean chrF++: 22.7410.
- Sentence-level feature-selected mean chrF++: 24.7724.
- Sentence-level oracle@8 mean chrF++: 28.9181.
- Oracle is not rank 1 for 663/879 examples.
- Feature-selected rank matches oracle rank for 298/879 examples.

10B CPU-only candidate decision selector:

- Selected model by validation OOF: gradient boosting.
- Test corpus chrF++: 24.6862.
- Top1 retrieval corpus chrF++: 22.5362.
- Existing feature reranker corpus chrF++: 24.5921.
- Oracle@8 corpus chrF++: 28.3327.
- Reading: candidate selection is worth keeping, but the small gain and remaining oracle gap argue for pairwise/listwise reranking before a GPU edit model.

10B pairwise selector follow-up:

- Selected model: logistic regression over candidate-pair feature differences.
- Test corpus chrF++: 24.7438.
- This is the current best CPU retrieval selector, but still well below oracle@8.

10C pairwise-selected retrieval-editing gate:

- Model: `google/byt5-small`.
- GPU: physical GPU 3 only.
- Budget: 512 train examples, 120 steps, fp32, no saved model.
- 64-test slice test chrF++: 18.3574.
- Pairwise-selected retrieval candidate on the same slice: 26.6235 chrF++.
- Prediction-vs-retrieved chrF++: 52.6372.
- Exact prediction=retrieved copy: 0/64, but retrieved contains prediction: 17/64.
- Reading: exact copying is reduced, but the model is still retrieval-dominated and underperforms the candidate evidence. Treat this as a negative neural editing gate.
- Same-checkpoint controls are complete:
  - correct pairwise source+retrieval: chrF++ 18.3574
  - source-only: chrF++ 0.2729
  - retrieved-only: chrF++ 18.6220
  - wrong-shift1: chrF++ 12.8253
  - feature-selected top8: chrF++ 19.1558
- Reading: retrieved-only slightly beats correct source+retrieval, while source-only collapses. Wrong retrieval hurts, so the model is retrieval-sensitive but not source-grounded enough.

### Pivot/Back-Translation Gate

Greek pivot gate fails:

| Direction | Test BLEU | Test chrF++ | Gen len | Judgment |
| --- | ---: | ---: | ---: | --- |
| Syriac -> Greek | 0.0000 | 3.5930 | 127.0 | Greek-script repetition |
| Greek -> Coptic | 0.0000 | 0.0000 | 127.0 | no Coptic output |

Decision:

- Do not generate back-translation data from these checkpoints.

## Main Findings

1. Target10 vocabulary extension solves a real tokenizer bottleneck.
2. Mean embedding initialization gives a better MLM adaptation starting point than Random.
3. Direct Coptic/Syriac neural NMT is currently collapsed.
4. Retrieval baselines are strong and must be included in the paper.
5. Retrieval-augmented neural models improve surface overlap but are copy-heavy.
6. Pairwise retrieval selection is the best current retrieval-side improvement, but same-checkpoint 10C controls show the neural edit gate is negative.
7. Small ByT5 pivot/back-translation gates fail, especially for Greek -> Coptic target-script transfer.

## Current Limitation

The representation-side pipeline is stronger than the generation-side pipeline.
The next modeling improvement should explicitly reward source grounding or candidate editing rather than simply training longer on the same direct/pivot objective.

## Next Work

Near-term:

- Finish report/presentation packaging.
- Keep all GPU experiments on physical GPU 3 only.
- If modeling continues, run only a small 10C retrieval-editing pilot with explicit copy/source controls.
- 10C controls are complete; treat neural retrieval editing as failure analysis and do not scale this objective without a stronger source-grounding design.
- Finalize data source and license citations before public release.

Do not prioritize:

- scaling direct NMT runs that already collapse;
- generating synthetic back-translation from the failed Greek pivot gate;
- claiming neural retrieval augmentation as solved translation.
