# Plan: Final Goal

Status: active

## Final Objective

Build a multilingual adaptation pilot that adds about 10 low-resource languages to a Glot500-style model, then evaluate Coptic <-> Syriac translation as the main downstream case. Vocabulary extension and embedding initialization remain the core experimental contribution. Submit a reproducible term-paper package by 2026-07-03.

## Paper Thesis

The central bottleneck in low-resource multilingual extension is representational failure: existing multilingual tokenizers overfragment unsupported scripts or underrepresented orthographies, and randomly initialized new embeddings are unstable under low-resource adaptation. A controlled 10-language tokenizer-extension pipeline with careful embedding initialization can improve representation quality and support better Coptic-Syriac pivot-based NMT.

## Success Criteria

- A 10-language target set is defined and extracted.
- Joint 10-language tokenizer/adaptation artifacts exist.
- Coptic -> Syriac and Syriac -> Coptic translation outputs exist.
- Held-out evaluation reports BLEU and chrF++.
- At least 20 qualitative examples are analyzed.
- Tokenization audit proves or falsifies the overfragmentation hypothesis.
- Vocabulary extension is compared against no-extension baseline.
- Embedding initialization has at least two conditions, preferably Random, Mean, and Align.
- Final report explains design choices, data, training pipeline, results, ablations, and limitations.
- Code and commands are documented well enough to rerun the main experiments.

## Milestones

| Date | Deliverable |
| --- | --- |
| 2026-06-12 | Progress report with survey, data plan, tokenizer audit plan or early numbers |
| 2026-06-19 | Final presentation with at least one completed ablation or baseline result |
| 2026-07-03 | Term paper and GitHub reproducibility package |

## Primary Experiments

1. 10-language data inventory and held-out split construction.
2. Tokenization audit for Glot500, XLM-R, NLLB, and new tokenizer.
3. Joint 10-language SentencePiece unigram vocabulary extension.
4. New embedding initialization comparison: Random vs Mean vs Align.
5. Continued MLM pretraining: target-only vs mixed sampling.
6. NMT baselines: no-extension, vocab-extension, multitask pivot.
7. Pivot and back-translation augmentation.
8. Final quantitative and qualitative analysis.

## Decision Rule

If time becomes tight, prioritize the minimum viable paper:

1. data and split
2. tokenizer audit
3. 10-language vocab extension
4. Random vs Mean initialization
5. one bidirectional NMT baseline
6. BLEU/chrF++ and qualitative analysis

Align initialization and back-translation are high-value but can be downgraded if implementation time blocks the core result.
