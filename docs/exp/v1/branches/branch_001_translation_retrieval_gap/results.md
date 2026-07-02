# Branch Results

Status: EXPLORATORY_SUPERSEDED_BY_STEP09

Run id: branch001_sentence_embedding_20260610_234706

Gate status: PASS_NEGATIVE_RESULT_AFTER_STEP09

Post-audit note: Step 09 reran the branch idea with method-matched high-resource and target retrieval. The LaBSE+CSLS method-matched ratio is `0.567179`, below the `0.800000` threshold.

## Summary

Retried translation branch with multilingual sentence-embedding retrieval. The selected setting was chosen on dev only:

- model: `sentence-transformers/LaBSE`
- scoring: `csls`
- pair: `kbh->nhg`

Test chrF++: `64.434500`.

Required chrF++: `49.567925`.

Mixed-method ratio: `1.039939`.

Step 09 method-matched LaBSE+CSLS ratio: `0.567179`.

Retrieval accuracy: `0.520000`.

Artifact directory: `/home/axt/mnt2/jongha/second_try/branches/branch_001_translation_retrieval_gap/sentence_embedding/branch001_sentence_embedding_20260610_234706`.

Runtime minutes: `1.678`.

## Failure Return

Failed gate: method_matched_translation_80_percent

Observed evidence: Step 09 LaBSE+CSLS ratio `0.567179 < 0.800000`

Return-to step: 07_translation_benchmark

Required fix: run a method-matched branch with dev-only selection and fresh held-out evaluation before merging into final claims
