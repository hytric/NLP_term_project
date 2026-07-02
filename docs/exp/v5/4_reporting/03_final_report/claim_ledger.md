# v5 Claim Ledger

Last updated: 2026-06-28

This ledger separates claims that are already supported by measured artifacts
from claims that require matched MLM checkpoints and downstream evaluation.
Use this file before writing the final conclusion or slide summary.

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
claim ledger header.

## Claim Status Table

| Claim | Current status | Evidence | Safe wording now | Upgrade condition |
| --- | --- | --- | --- | --- |
| v5 reproduces the Glot500-style pipeline on a controlled subset | supported | data scope, full merge, tokenizer append, MLM launch, required metric folders | We reproduce the Glot500-style training/evaluation pattern on a controlled 102-language subset. | After all metrics run, say the pipeline was executed end-to-end on measured/available tasks. |
| v5 is a full Glot500 511-language reproduction | disallowed | v5 uses 92 seen + 10 target language-scripts | Do not use this claim. | Not applicable unless the full 511-language experiment is actually executed. |
| target10 selection is Glot500-internal and not arbitrary external data | supported | `glot50010_selected_manifest.tsv`, raw symlink root, merge manifest | The 10 targets are selected from Glot500 raw data with `new_length >= 30000` and diversity constraints. | None. |
| main corpus construction is complete | proven | merge report PASS, 92,452,251 actual samples, 0 missing dirs | The main 102-language corpus was merged successfully with no missing language directories. | None. |
| main tokenizer expansion is structurally valid | proven with documented risk | vocab audit, tokenizer audit, 0 structural failures | The tokenizer append run passed audits and improved fertility for 29/30 audited languages. | None, but keep the `dzo_Tibt` caveat. |
| tokenizer improves every target language | disallowed | `dzo_Tibt` worsens from 4.223938 to 5.552124 tokens/word | The tokenizer improves 9/10 target languages; `dzo_Tibt` is a documented regression. | Only if a repaired tokenizer removes this regression. |
| FVT initialization improves zero-step target MLM proxy over random | proven intrinsically | `1_embedding/04_zero_step_eval/main/summary.tsv` | Before continued MLM, FVT lowers target weighted NLL by 9.626238 versus random resize. | None for zero-step claim. |
| FVT improves after-MLM performance over random | pending | `v5_random` 10K checkpoint is ready; `v5_fvt` is still running/model-file pending, so the matched pair is incomplete | This is the main hypothesis for after-MLM evaluation, not a result yet. | Both `v5_random` and `v5_fvt` 10K checkpoints exist and are evaluated with the same scripts. |
| FVT improves downstream performance | pending | v5-random rows are partially measured, but matched v5-FVT downstream outputs are missing | Downstream transfer remains a paired-method hypothesis, not a result. | All required v5_random/v5_fvt metric rows have model outputs or explicit exclusions. |
| baseline/reference and partial v5-random evaluation are measured | supported with scope | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip rows for `xlmr_base`/`glot500_base` are parsed where local data exists; v5-random PPPL/Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip rows are parsed | Current baseline/reference and v5-random rows can be reported for measured metrics only. | Add paired method claims only after matched v5-FVT rows are parsed. |
| live dev scores are final downstream results | disallowed | Glot500-base NER/POS rows are promoted from final `test_results.txt`, not live dev F1; v5 method jobs still need final outputs | Mention live dev F1 only as progress, never as a final table row. | A non-empty completed `test_results.txt` or equivalent metric output is parsed by aggregation. |
| target10 downstream improves | disallowed for now | official task-list membership is partial, but local tail materialization needs repair | Target10 claims should focus on tokenization, zero-step, and after-MLM PPPL until Bible/NER/POS tail rows are repaired and evaluated. | Only if task data for target10 is materialized and evaluated. |
| Glot500 metric family is faithfully retained | supported | metric requirement docs, wrapper, aggregation skeleton | All Glot500 metric families are retained as required evaluation targets, with coverage/exclusion records. | After execution, say which metrics were measured and which remained blocked. |
| `cis-lmu/glot500-base` is an equal-budget baseline | disallowed | external model has different scale/training budget | Treat Glot500-base as an external reference model. | Not applicable without equal-budget retraining. |

## Report Conclusion Template

Current-safe conclusion:

```text
The v5 setup successfully reproduces the core Glot500-style workflow on a
controlled 102-language subset and isolates vocabulary-row initialization as a
measurable source of early adaptation quality. The strongest completed evidence
is intrinsic: FVT substantially improves zero-step target MLM proxy loss over
random resize while preserving source rows, `<mask>` behavior, byte-row
accounting, and LM-head tying. v5-random now has several available-language
post-checkpoint rows, but final after-MLM and downstream method claims remain
conditional on the matched `v5_fvt` checkpoint and paired task coverage.
```

Final-upgrade conclusion after downstream completion:

```text
After matched continued MLM training, we evaluate XLM-R-base, Glot500-base,
v5-random, and v5-FVT across the retained Glot500 metric families. Results show
whether the zero-step initialization advantage survives training and transfers
to available downstream tasks, while target10 downstream claims remain bounded
by documented task coverage.
```

## PPT Use

- Use proven claims for title, motivation, data, tokenizer, initialization, and
  current result slides.
- Use pending claims only as experiment plan or hypothesis.
- Put disallowed claims in limitations if they are useful for preventing
  overstatement.
- If a slide contains an unresolved result slot, it must point to the exact gate
  that will replace it.
