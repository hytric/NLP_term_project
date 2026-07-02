# Step 07 Plan: Translation Benchmark

## Goal

Add a translation benchmark after encoder-only downstream evaluation and reach at least 80% of the high-resource reference score.

## Inputs

- Step 06 `Gate status: PASS` or `PASS_NEGATIVE_RESULT`
- Selected adapted encoder/checkpoint from Step 05
- Downstream evidence from Step 06
- Translation data manifests from Step 01 or branch-specific data manifests

## Required Work

1. Define the high-resource reference dataset and score.
2. Define the target low-resource translation dataset and split.
3. Choose translation setup:
    - encoder + lightweight decoder
    - retrieval-augmented translation
    - external high-resource teacher/pivot baseline
    - branch-specific alternative if needed
4. Run high-resource reference baseline.
5. Run target translation experiment.
6. Compare target score against `0.8 * high_resource_reference_score`.
7. Save large checkpoints/logs under `/home/axt/mnt2/jongha/second_try`.
8. Document all failed attempts and branch attempts.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `translation_data_manifest.tsv`
- `translation_results.tsv`
- `high_resource_reference.md`
- `sample_translations.md`
- `failure_cases.md`
- `file_results.tsv`

## Score Table Contract

Every score cell must be filled. If a metric is unavailable, write `NOT_APPLICABLE` and explain in `results.md`. No `TBD` is allowed before exit.

## Metrics

- chrF++
- BLEU
- exact copy rate
- output script validity
- generation length
- high-resource reference ratio

## Exit Criteria

- High-resource reference score is defined and measured.
- Target translation score is measured.
- `target_score / high_resource_reference_score >= 0.80` for the primary metric.
- Sample translations and failure cases are documented.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If target translation is below 80%:

1. Record `Gate status: FAIL`.
2. Identify whether failure is data, tokenizer, model, decoder, or evaluation related.
3. If a known earlier step can fix it, return to that step.
4. If no existing guideline applies, create a branch under `docs/exp/second_try/branches/{branch_id}` and `/home/axt/mnt2/jongha/second_try/branches/{branch_id}`.
5. The branch must define a new goal, plan, score table, and return decision before more experiments continue.
