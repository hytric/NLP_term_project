# Final Presentation Outline

작성일: 2026-06-04

## Slide 1. Problem

- Multilingual pretrained models still fail on unsupported or underrepresented scripts.
- Low-resource adaptation needs both representation-side and generation-side evidence.

## Slide 2. Target10 Setup

- 10 low-resource languages from Bible data.
- Coptic/Syriac as downstream translation case.
- Shared verse overlap: 4,892.

## Slide 3. Tokenizer Bottleneck

- Glot500 overfragments Coptic, Syriac, Cherokee, Ojibwa.
- NLLB often uses `<unk>` for unsupported scripts.

## Slide 4. Vocabulary Extension

- Train target10 SentencePiece unigram 16k.
- Merge into Glot500 tokenizer.
- Main result: Syriac/Coptic tokens per word drop by about two thirds.

## Slide 5. Embedding Initialization

- Random vs Mean initialization.
- Mean wins stable 10k MLM re-evaluation: eval loss 5.8343 vs 7.0169.

## Slide 6. Direct NMT Baselines

- Coptic -> Syriac and Syriac -> Coptic run end-to-end.
- BLEU remains near zero.
- chrF++ improves but outputs are repetitive.

## Slide 7. Retrieval Baselines

- Character n-gram retrieval is much stronger than direct neural NMT.
- English -> Coptic retrieval: chrF++ 22.3584.
- Syriac -> Coptic retrieval: chrF++ 22.2083.

## Slide 8. Reranking And Retrieval-Augmented Neural Runs

- Top8 oracle shows headroom: 28.3327 chrF++.
- Feature reranker reaches 24.5921.
- Neural retrieval-augmented run reaches around 19.7-19.9 on the 64-slice, but is copy-heavy.

## Slide 9. Pivot/Back-Translation Gate

- Greek pivot gate fails.
- Syriac -> Greek emits Greek-script repetition.
- Greek -> Coptic emits no Coptic.
- Back-translation should not be scaled from this gate.

## Slide 10. Qualitative Failure Modes

- Formulaic Coptic fragments.
- Max-length repetition.
- Target-script failure.
- Retrieval copy dependence.
- Metric inflation from surface overlap.

## Slide 11. Conclusion

- Representation-side adaptation is promising and measurable.
- Generation-side translation remains unsolved.
- Retrieval is a necessary baseline and useful input signal, but not final translation.

## Slide 12. Next Steps

- Stronger source-grounding objective.
- Retrieval-editing or delta-generation setup.
- Better candidate selection plus copy-aware evaluation.
- Avoid scaling failed pivot/back-translation checkpoints.
