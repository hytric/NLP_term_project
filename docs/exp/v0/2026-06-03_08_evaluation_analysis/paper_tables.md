# Paper Tables Draft

작성일: 2026-06-04

## Table 1. Target10 Language Set

| ISO | Language | Script | Train verses | Dev verses | Test verses |
| --- | --- | --- | ---: | ---: | ---: |
| `cop` | Coptic | Coptic | 6,400 | 678 | 879 |
| `syr` | Syriac | Syriac | 6,397 | 678 | 879 |
| `chr` | Cherokee | Cherokee | 6,400 | 678 | 879 |
| `oji` | Ojibwa | Aboriginal Syllabics | 6,391 | 674 | 878 |
| `bsn` | Barasana-Eduria | Latin | 6,062 | 629 | 857 |
| `usp` | Uspanteco | Latin | 6,334 | 678 | 878 |
| `nhg` | Nahuatl (Tetelcingo) | Latin | 6,279 | 673 | 870 |
| `ake` | Akawaio | Latin | 6,182 | 673 | 879 |
| `kbh` | Camsa | Latin | 5,363 | 501 | 657 |
| `acu` | Achuar-Shiwiar | Latin | 6,123 | 659 | 864 |

Shared verse overlap across all 10 languages: 4,892.

## Table 2. Tokenization Bottleneck And Target10 Improvement

| ISO | Script | Glot500 tokens/word | Merged target10 tokens/word | Reduction |
| --- | --- | ---: | ---: | ---: |
| `syr` | Syriac | 5.089 | 1.601 | 68.5% |
| `cop` | Coptic | 5.274 | 1.779 | 66.3% |
| `chr` | Cherokee | 5.254 | 2.001 | 61.9% |
| `oji` | Aboriginal Syllabics | 5.021 | 2.205 | 56.1% |

Interpretation:

- The largest gains are in the non-Latin scripts that were most overfragmented by Glot500.
- NLLB has a different failure mode: it often maps these scripts to `<unk>` rather than merely overfragmenting them.
- A paper-ready visualization is available in `paper_figures.md`.

## Table 3. Target10 MLM Initialization Ablation

| Init | Train samples | Steps | Train loss | Stable eval loss | Stable perplexity | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Random | 10,000 | 5,000 | 7.3639 | 7.0169 | 1,115.29 | keep as ablation |
| Mean | 10,000 | 5,000 | 6.2236 | 5.8343 | 341.84 | selected for NMT |

Interpretation:

- Mean initialization is the stronger downstream candidate after the stable fp32, batch-16 re-evaluation.
- The built-in batch-2 eval produced NaN for both 10k checkpoints, so the stable re-eval is the decision metric.

## Table 4. Translation And Retrieval Evidence

| Family | Condition | Scope | BLEU | chrF++ | Main reading |
| --- | --- | --- | ---: | ---: | --- |
| Direct NMT | Coptic -> Syriac, Mean full1epoch | full test | 0.0139 | 5.7982 | runs end-to-end but repetitive |
| Direct NMT | Syriac -> Coptic, Mean full1epoch | full test | 0.0181 | 9.9340 | high overlap from max-length Coptic repetition |
| Direct NMT control | Syriac -> Coptic, 512 train, 300 steps | 64-test slice | 0.1230 | 8.7360 | short formulaic fragments |
| Retrieval baseline | English -> Coptic char 3-5gram | full test | 3.7415 | 22.3584 | strong non-neural reference |
| Retrieval baseline | Syriac -> Coptic char 3-5gram | full test | 3.7434 | 22.2083 | strong non-neural reference |
| Top8 oracle | English -> Coptic | full test | n/a | 28.3327 | reranking headroom |
| Feature reranker | Gradient boosting over top8 | full test | n/a | 24.5921 | first deployable selector above top1 |
| Candidate decision selector | 10B validation-selected gradient boosting | full test | 3.4576 | 24.6862 | small selector gain; still below oracle |
| Pairwise candidate selector | 10B logistic pairwise selector | full test | 3.0602 | 24.7438 | current best CPU selector; still below oracle |
| Neural retrieval | ByT5 retrieval + Coptic autoencoding | 64-test slice | 3.5392 | 19.6952 | high but copy-heavy |
| Neural retrieval | Feature-selected top8 hint eval | 64-test slice | 3.2145 | 19.9182 | small gain, copy not solved |
| Greek pivot gate | Syriac -> Greek ByT5 | 32-test slice | 0.0000 | 3.5930 | Greek-script repetition |
| Greek pivot gate | Greek -> Coptic ByT5 | 32-test slice | 0.0000 | 0.0000 | no Coptic output |

## Current Paper Claim Strength

Strong claims:

- Target10 tokenizer extension substantially reduces overfragmentation for unsupported/underrepresented scripts.
- Mean embedding initialization is more stable than Random in the 10k MLM pilot.
- Direct low-resource Coptic/Syriac generation remains collapsed under the current small seq2seq setups.
- Retrieval is a strong baseline and must be included to avoid overstating neural results.
- CPU-only candidate selection improves retrieval slightly, with pairwise selection the current best CPU selector, but oracle headroom remains.

Weaker claims:

- Retrieval-augmented neural generation improves overlap but is copy-heavy.
- Source-grounded retrieval editing is promising but not solved by candidate selection alone.
- Pivot/back-translation is not yet viable under the small ByT5 gate.

Do not claim yet:

- Back-translation improves Coptic/Syriac translation.
- The neural model beats retrieval as a source-grounded translator.
- Random-vs-Mean downstream NMT has been cleanly decided; current decoders are too collapsed for that ablation to be meaningful.
