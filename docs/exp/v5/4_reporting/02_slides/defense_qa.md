# v5 Presentation Defense Q&A

Last updated: 2026-06-28

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
Q&A header.

Use this document to answer likely questions without overstating the current
evidence.

## Q1. Is this a full Glot500 reproduction?

No. The safe wording is:

```text
controlled 102-language Glot500-style reproduction
```

The experiment preserves the Glot500-style workflow: corpus merge, SentencePiece
append, continued MLM, and retained metric families. It does not reproduce the
full 511-language scale.

## Q2. Why use only 92 seen languages?

The 92 head language-scripts are the local XLM-R-seen Glot500 language-scripts
available in the current raw data. The missing XLM-R seen candidates are listed
in the report. This makes the data scope reproducible and avoids silently
mixing unavailable or unverifiable sources.

## Q3. Why these 10 target languages?

They are selected from Glot500 raw data, not from an external corpus. The
selection constraints are:

- `XLM-R != True`
- `new_length >= 30000`
- local raw directory exists
- regional/script/family diversity

This means the target10 is a controlled Glot500-internal tail set.

## Q4. What is the novelty?

The novelty is vocabulary-row initialization after SentencePiece extension.
The main comparison is:

```text
random resize vs source-token decomposition initialization
```

The strongest completed evidence is zero-step target MLM proxy: FVT lowers
target weighted NLL by `9.626238` versus random resize.

## Q5. Is zero-step enough to claim downstream improvement?

No. Zero-step supports the initialization hypothesis, but downstream improvement
requires matched after-MLM checkpoints and downstream evaluation. The final
claim remains pending until `v5_random` and `v5_fvt` are trained and evaluated
under the same budget.

## Q6. Why not claim target10 downstream improvement?

Current downstream task coverage for target10 is `0/10` outside raw-text PPPL.
Therefore target10 claims should be about:

- tokenization
- zero-step MLM proxy
- after-MLM PPPL once checkpoints exist

Downstream metrics should be reported as available-language/head/all replay.

## Q7. Why include Glot500-base if it is not equal-budget?

Glot500-base is useful as an external reference model. It should not be
described as an equal-compute or equal-data baseline. The equal-budget
comparison for the novelty is `v5_random` vs `v5_fvt`.

## Q8. What does the `dzo_Tibt` regression mean?

It is a real tokenizer failure case. The main tokenizer improves 9/10 target
languages but worsens `dzo_Tibt` from `4.223938` to `5.552124` tokens/word.
The issue is not `<unk>` or byte fallback. It appears related to newly appended
Tibetan pieces changing segmentation behavior.

Safe answer:

```text
The tokenizer expansion is structurally valid and broadly improves fertility,
but not uniformly. dzo_Tibt is retained as a visible limitation and repair
target.
```

## Q9. Why is POS trained with Turkish?

The local POS materialization has no `train-eng_Latn.tsv`. The v5 POS baseline
therefore uses `TRAIN_LANGS=tur_Latn`, which is explicitly documented. This is
a local-data deviation from an English-train setup and should be preserved in
the report.

## Q10. Can running dev F1 be cited?

Only as live progress. It is not a final result row. A created-but-empty
`test_results.txt` also does not count as a final result row.

Final tagging rows require:

```text
non-empty completed test_results.txt parsed by scripts/aggregate_v5_metrics.py
```

Current example:

```text
Glot500-base NER reached step-3000 dev F1 0.830725 during training, but this is
only a progress signal. The value that can be used in the result table is the
completed test file parsed by aggregation: all F1 0.627108 and head F1
0.645915.
```

The same rule is now satisfied for Glot500-base POS: the completed
`test_results.txt` is parsed by aggregation, so all F1 `0.567542` and head F1
`0.573832` can be used with the `TRAIN_LANGS=tur_Latn` caveat.

It is also satisfied for v5-random NER: the completed `test_results.txt` has
`164` language rows and is parsed by aggregation, so all F1 `0.544628`, head F1
`0.608020`, and the one-language v5-target actual-intersection F1 `0.560554`
can be used with the `fur_Latn` caveat.

It is also satisfied for v5-random POS: the completed `test_results.txt` is
parsed by aggregation, so all F1 `0.481102` and head F1 `0.587430` can be used
with the same `TRAIN_LANGS=tur_Latn` caveat.

## Q11. What remains before final report completion?

The main remaining gates are:

- matched `v5_random` and `v5_fvt` checkpoints
- after-MLM PPPL for both v5 models
- available downstream replay for remaining v5 models/rows
- Bible row for `v5_fvt` after checkpoints and preflight
- Roundtrip row for `v5_fvt` after checkpoints and preflight
- POS row for `v5_fvt`

These gates are tracked in:

```text
docs/exp/v5/4_reporting/final_package_checklist.md
```

The short contribution wording is tracked in:

```text
docs/exp/v5/4_reporting/03_final_report/contribution_summary.md
```

## Q12. What is the one-sentence current conclusion?

Current-safe conclusion:

```text
v5 faithfully sets up and executes the Glot500-style workflow on a controlled
102-language subset, and the strongest completed evidence shows that
source-token decomposition initialization greatly improves zero-step target MLM
proxy over random resize; several v5-random available-language downstream rows
are now measured, but final method claims are still pending the matched v5-FVT
checkpoint and parsed paired task results.
```

## Q13. How do we defend Bible/Roundtrip metric gaps?

Do not remove them from the protocol. The safe answer is:

```text
We retained every Glot500 metric family in the v5 evaluation design. Bible
retrieval is now materialized for 74 available language-scripts, and the
XLM-R-base / Glot500-base / v5-random rows are measured. The remaining Bible
gap is the `v5_fvt` row, which waits for the matched checkpoint. Roundtrip
alignment also has materialized inputs, a v5 batch runner, and measured
XLM-R-base / Glot500-base / v5-random rows over 74 available language-scripts.
The remaining Roundtrip gap is likewise the `v5_fvt` row after the matched
checkpoint.
```

Point to `00_tables/table_13_metric_fidelity_matrix.md` if asked for the
metric-by-metric evidence. It records each required family, the runner, current
baseline/reference status, v5 method status, coverage boundary, and final claim
rule.

This is weaker than measuring the metrics, but stronger than hiding them. It
shows that the experiment is faithful to Glot500's metric surface and honest
about local data limits.

## Q14. What exactly happens when the v5 checkpoints finish?

First, refresh and inspect the generated model matrix:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

This command must show both `v5_random` and `v5_fvt` as
`ready_for_wrapper=yes`, and `post_checkpoint_preflight.md` must report
`post_checkpoint_preflight_ready_to_launch`. Then run the paired
post-checkpoint evaluation wrapper:

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

The wrapper runs PPPL first and then the available downstream replay. Use the
canonical full rerun without `SKIP_MEASURED=1` only when intentional
remeasurement is needed. If machine time or debugging constraints make that too
large, run the same wrapper in phases:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

The wrapper refuses to run before both matched checkpoints and post-checkpoint
preflight are ready. Final
report and slide values still come only from `3_evaluation/09_aggregation/`
after `scripts/refresh_v5_reporting.py` promotes completed outputs.
The exact launch environment, output/log locations, and promotion rule are
recorded in:

```text
docs/exp/v5/3_evaluation/post_checkpoint_execution_plan.md
```

## Q15. What if FVT does not beat random after MLM?

That is still a useful result. The safe answer is:

```text
The zero-step result proves that initialization changes early behavior. If
random catches up after matched MLM, the conclusion becomes diagnostic rather
than positive: FVT gives a better starting point, but the fixed 10K MLM budget
can reduce or erase the initialization gap.
```

Do not reinterpret a negative or mixed final result as a hidden downstream win.
Use `result_interpretation_blocks.md` and choose the block that matches parsed
PPPL and downstream evidence.

## Q16. How do we avoid cherry-picking checkpoints?

The checkpoint-selection surface is generated before downstream scores are
inspected:

```text
docs/exp/v5/2_training/05_checkpoint_selection/selected_checkpoint_manifest.md
```

The main rule is fixed:

```text
Use v5_random and v5_fvt only when both rows are selected 10K checkpoints from
the paired full-corpus run.
```

If one side fails or stops early, the comparison is not silently repaired by
choosing a more favorable checkpoint. It must be rerun or downgraded to an
incomplete/exploratory result.

## Q17. How is this still Glot500-faithful if some downstream target10 rows are missing?

Faithfulness here means retaining the Glot500 evaluation surface and reporting
coverage honestly, not forcing unavailable target task rows. The answer is:

```text
We keep every Glot500 metric family in the protocol. When a task lacks selected
target10 data, the row is reported as coverage-limited rather than omitted or
converted into a negative target10 result.
```

This is why PPPL can support target10 method claims, while Tatoeba/Bible/NER/POS
currently support available-language/head/all replay claims.

## Q18. What if only part of the post-checkpoint evidence arrives?

Do not choose a positive or negative final conclusion from partial evidence.
If one selected checkpoint, paired metric row, provenance trail, materiality
band, decision-tree outcome, or final freeze audit is missing, the official
outcome is:

```text
Incomplete Evaluation / Execution Draft
```

The safe answer is:

```text
The controlled setup, tokenizer expansion, initialization audits, and Glot500
metric-family replay protocol are complete enough to support setup fidelity
and zero-step initialization evidence. However, final after-MLM and downstream
superiority claims require the full Final Evidence Packet. Until that packet
closes, any measured partial row remains measured but not promotable.
```

Use the `Incomplete Evaluation / Execution Draft` block in
`../03_final_report/result_interpretation_blocks.md` for report and slide
wording. Do not improvise a stronger conclusion from a good-looking single
metric, stdout line, live log, or one-sided v5 row.

## Q18. Do the mixed v5-random results weaken the novelty claim?

No. The v5-random rows are diagnostic lower-bound rows, not the final method
claim. v5-random improves target10 PPPL relative to XLM-R but remains behind
the Glot500-base reference; available-language downstream behavior is mixed
across metrics. That mixed profile is exactly why the matched FVT test matters:
random resize plus a short 10K MLM budget is not itself a stable vocabulary
extension method claim. The final novelty test is whether source-token
decomposition initialization improves over that random checkpoint under the
same corpus, tokenizer, schedule, and checkpoint rule.
