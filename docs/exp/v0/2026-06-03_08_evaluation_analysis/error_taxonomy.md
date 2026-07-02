# Error Taxonomy

작성일: 2026-06-04

## E1. Formulaic Target Fragment Collapse

Definition:

- The model outputs a short, high-frequency target-language fragment for many unrelated sources.

Seen in:

- Direct Syriac -> Coptic 300-step control.

Evidence:

- 64 predictions have only 3 unique strings.
- Repeated fragment family: `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ...`.

Interpretation:

- The decoder learns target-script fluency fragments but not verse-specific translation.

## E2. Maximum-Length Repetition

Definition:

- Generation reaches the configured cap and repeats phrase-like material.

Seen in:

- Full Syriac -> Coptic.
- ByT5 pivot and retrieval-augmented diagnostics.
- Greek pivot gate.

Evidence:

- Greek pivot gate has `test_gen_len=127.0` with target cap 128.
- Earlier full Syriac -> Coptic had `test_gen_len=96.0`.

Interpretation:

- Lowering the cap can make output shorter, but does not teach EOS or source grounding.

## E3. Target-Script Failure

Definition:

- Output remains in the source or pivot script instead of the required target script.

Seen in:

- Greek -> Coptic gate.
- Earlier ByT5 English -> Coptic plain second-leg diagnostic.

Evidence:

- Greek -> Coptic gate: 0/32 predictions contain Coptic characters; all inspected predictions are Greek-script.

Interpretation:

- Back-translation should not be generated from this path.

## E4. Retrieval Copy Dependence

Definition:

- The model output is close to the retrieved Coptic hint, and source-only evaluation collapses.

Seen in:

- Retrieval-augmented ByT5 + Coptic autoencoding.
- Feature-selected top8 hint evaluation.
- Retrieved-only, wrong-retrieval, and source-only controls.

Evidence:

- Normal retrieval + Coptic autoencoding: `test_chrfpp=19.6952`, but 17/64 exact retrieved copies.
- Retrieved-only control nearly matches source+retrieval.
- Wrong-retrieval evaluation follows the wrong hint and drops gold chrF++.
- Source-only evaluation collapses.

Interpretation:

- Retrieval is a strong baseline and useful signal, but current neural generation is not independent source-conditioned translation.

## E5. Metric Inflation From Surface Overlap

Definition:

- BLEU/chrF++ improve because generated strings contain common or copied target-language fragments, not because adequacy improves.

Seen in:

- Full Syriac -> Coptic.
- Multi-source-to-Coptic 300-step.
- Retrieval-augmented copy-heavy runs.

Evidence:

- Multi-source 300-step produced high chrF++ but max-length repetition.
- Direct 300-step improved chrF++ but retained formulaic collapse.

Interpretation:

- chrF++ should be paired with diversity, generation length, source-only controls, wrong-retrieval controls, and qualitative examples.

## E6. Undertrained Empty Output

Definition:

- The model emits empty or near-empty strings after unstable prompting or insufficient training exposure.

Seen in:

- Bracket-style source/target tags.
- Undertrained multi-source-to-Coptic 100-step.
- Some English -> Coptic pivot second-leg settings.

Evidence:

- Bracket tag runs score 0.0 and produce empty/punctuation-like output.

Interpretation:

- Bracket-style tags should not be scaled in the current encoder-decoder setup.

## Recommended Evaluation Checklist

For every future translation run, report:

- BLEU and chrF++.
- Mean generation length and cap-hit count.
- Unique prediction count.
- Target-script line count.
- For retrieval runs: exact retrieved-copy count and prediction-vs-retrieved chrF++.
- At least 10 qualitative examples per direction.

This prevents a run from looking successful only because it copies a retrieved candidate or repeats target-language boilerplate.
