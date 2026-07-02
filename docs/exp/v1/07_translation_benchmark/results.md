# Step 07 Results: Translation Benchmark

Status: COMPLETED_WITH_EXPLORATORY_BRANCH

Run id: step07_translation_20260610_231227

Completed date: 2026-06-10

Gate status: PASS_NEGATIVE_RESULT_AFTER_STEP09

Post-audit note: Step 09 reran the translation check with method-matched high-resource and target retrieval methods. That audit supersedes the Branch 001 pass for top-tier translation claims.

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | reference, original target, and branch-merged target rows filled |
| file results | `file_results.tsv` | yes | per-output file status recorded |
| data manifest | `translation_data_manifest.tsv` | yes | high-resource and target datasets |
| translation results | `translation_results.tsv` | yes | chrF++/BLEU/copy/script metrics |
| high-resource reference | `high_resource_reference.md` | yes | reference score defined |
| sample translations | `sample_translations.md` | yes | original failed target pair samples |
| branch samples | `branch_sentence_embedding_samples.md` | yes | exploratory branch examples |
| failure cases | `failure_cases.md` | yes | original failure and branch audit notes |

## Summary

Step 07 used a retrieval-augmented verse translation proxy. The source encoder retrieves a target-language verse from candidate target verses, then the retrieved target text is scored against the gold aligned verse.

The original selected adapted-encoder retrieval row failed. Following the documented branch rule, Branch 001 retried no-leakage multilingual sentence-embedding retrieval. The branch selected `sentence-transformers/LaBSE`, `csls`, and `kbh->nhg` on the dev split, then evaluated that exact setting once on held-out John test. Step 09 later showed that this branch was a mixed-method shortcut for the 80% claim because the high-resource reference used XLM-R retrieval while the target branch used LaBSE+CSLS.

## High-Resource Reference

High-resource reference: Spanish -> English, chrF++ `61.959906`.

## 80 Percent Check

Original target pair: `usp->kbh`.

Original target chrF++: `31.613700`.

Required threshold: `49.567925`.

Original ratio: `0.510228`.

Branch exploratory target pair: `kbh->nhg`.

Branch exploratory target chrF++: `64.434500`.

Branch mixed-method ratio: `1.039939`.

Step 09 selected adapted XLM-R method-matched ratio: `0.638034`.

Step 09 LaBSE+CSLS method-matched ratio: `0.567179`.

Gate: `PASS_NEGATIVE_RESULT_AFTER_STEP09`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- high-resource reference score is measured.
- original target translation score is measured.
- branch target translation score is measured, but it is now marked exploratory because it used a mixed-method high-resource comparison.
- Step 09 method-matched validation fails the 80% threshold for both the selected adapted XLM-R encoder and the LaBSE+CSLS upper bound.
- sample translations, branch samples, and failure cases are documented.

## Failure Return

Failed gate: method_matched_translation_80_percent

Observed evidence: selected_adapted_xlmr_cosine ratio=`0.638034 < 0.800000`; labse_csls_upper_bound ratio=`0.567179 < 0.800000`

Return-to step: `05_mlm_adaptation` / `06_downstream_tasks` / `07_translation_benchmark`

Required fix or branch id: run a new branch with stronger adaptation controls, dev-only branch selection, and a fresh held-out method-matched translation retrieval or generation test.
