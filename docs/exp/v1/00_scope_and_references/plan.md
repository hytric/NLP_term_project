# Step 00 Plan: Scope And References

## Goal

Freeze the second_try scope and map every reference-derived method decision before implementation begins.

## Inputs

- `../idea.md`
- `../questions.md`
- `../reference_summaries/`
- `../reference_summary.md`
- `../downstream_tasks.md`
- `../step_index.md`

## Required Work

1. Confirm that the base model is `xlm-roberta-base`.
2. Confirm encoder-only downstream tasks and no translation.
3. Confirm the exact target language list.
4. Confirm tokenizer method: SentencePiece unigram.
5. Confirm vocab size grid: 8k, 16k, 32k.
6. Confirm init method list: random, mean, fvt, align, focus.
7. Confirm downstream tasks and diagnostic-only language identification.
8. Record all unresolved decisions or explicitly assign defaults.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `scope_decisions.tsv`
- `reference_trace.md`

## Score Table Contract

`score_table.tsv` must have no `TBD` before exit. Every row must identify whether the scope item is confirmed, defaulted, or blocked.

## Exit Criteria

- `scope_decisions.tsv` exists.
- `reference_trace.md` maps each major method decision to a second_try reference summary.
- All score table fields are filled.
- `results.md` has `Gate status: PASS`.

## Failure Return

If scope conflicts remain, do not proceed to Step 01. Resolve the conflict in `questions.md`, then rerun Step 00.
