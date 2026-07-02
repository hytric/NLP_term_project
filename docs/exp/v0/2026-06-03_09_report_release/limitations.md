# Limitations

작성일: 2026-06-04

## L1. Domain Limitation

Most experiments use Bible-derived aligned text.

Impact:

- The data is useful for controlled verse-level comparison.
- However, religious formulae and repeated phrasing can inflate overlap metrics.
- Results should not be generalized to broad-domain Coptic/Syriac translation.

## L2. Translation Quality Is Not Solved

The project has a successful representation-side pipeline, but not a final usable neural translator.

Evidence:

- Direct Coptic/Syriac NMT outputs are repetitive.
- Greek pivot back-translation gate fails target-script transfer.
- Retrieval-augmented models are copy-heavy.

Claim wording:

- Say "diagnostic", "pilot", "case study", and "preliminary evidence".
- Do not claim "state-of-the-art translation" or "solved Coptic/Syriac NMT".

## L3. chrF++ Can Be Misleading

chrF++ is useful for low-resource string overlap, but it can reward:

- repeated high-frequency Coptic fragments;
- retrieved target copying;
- long max-length target-script output.

Mitigation used:

- unique prediction counts;
- generation length;
- target-script checks;
- wrong-retrieval controls;
- source-only controls;
- qualitative examples.

## L4. Retrieval Is Strong But Not Translation

Character n-gram retrieval is a strong baseline and produces valid Coptic sentences.

But:

- It borrows a train-set target from a similar source verse.
- It may be semantically adjacent rather than exactly correct.
- It should be framed as a non-neural reference, not as generative translation.

## L5. Retrieval-Augmented Neural Models Are Copy-Heavy

The best neural retrieval-augmented run is not source-only translation.

Evidence:

- Same-checkpoint 10C correct source+retrieval reaches chrF++ 18.3574.
- Retrieved-only reaches chrF++ 18.6220, slightly above correct source+retrieval.
- Wrong-shift1 drops to chrF++ 12.8253 but still follows the wrong hint closely.
- Source-only collapses to chrF++ 0.2729.

Interpretation:

- Retrieval can provide useful Coptic lexical material.
- The current objective does not force the model to correct the hint from the English source.

## L6. Back-Translation Not Yet Viable

The Greek pivot gate fails:

- Syriac -> Greek emits Greek-script repetition.
- Greek -> Coptic emits Greek, not Coptic.

Decision:

- Do not scale synthetic back-translation from these checkpoints.
- Future back-translation needs a stronger model or a target-script/source-grounded objective.

## L7. Model And Compute Scope

Most neural runs are deliberately small diagnostics.

Reasons:

- Avoid large checkpoint artifacts.
- Keep experiments reproducible on one A6000.
- Quickly detect collapse before scaling.

Consequence:

- Some negative results may improve with larger models or better training recipes.
- But repeated collapse across direct, pivot, and retrieval controls suggests the issue is not only insufficient steps.

## L8. Data Licensing And Release

The repo should avoid redistributing large corpora or model checkpoints without checking licenses.

Release-safe direction:

- Keep generated metrics, scripts, and documentation.
- Provide data preparation instructions.
- Keep large local artifacts on `/disk1` or ignored paths.

## L9. Target10 Scope

The project adds exactly the current target10 low-resource set.

It does not claim:

- coverage of all low-resource languages;
- universal script adaptation;
- final translation quality for all ten languages.

The 10-language scope is a controlled pilot, not a broad multilingual benchmark.
