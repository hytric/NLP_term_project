# Step 04 Results: Embedding Initialization

Status: COMPLETED

Run id: step04_init_20260610_225846

Completed date: 2026-06-10

Gate status: PASS

## Required Artifact Check

| Artifact | Path | Present? | Notes |
| --- | --- | --- | --- |
| score table | `score_table.tsv` | yes | selected 32k tokenizer x 5 init methods |
| file results | `file_results.tsv` | yes | docs and checkpoint paths recorded |
| init metrics | `embedding_init_metrics.tsv` | yes | shape/norm/fallback/loss metrics |
| zero-step MLM | `zero_step_mlm.tsv` | yes | 200 dev rows |
| nearest neighbors | `nearest_neighbors.md` | yes | approximate diagnostics |
| initialized checkpoints | `/home/axt/mnt2/jongha/second_try/checkpoints/04_embedding_init` | yes | saved outside workspace |

## Summary

Step 04 initialized the selected Step 03 tokenizer (`32000`) with all required methods: random, mean, fvt, align, and focus. `align` and `focus` are documented proxy implementations that use only second_try-local tokenizer evidence and no external bilingual lexicon.

| Metric | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| tokenizer | `/home/axt/mnt2/jongha/second_try/artifacts/03_vocab_extension/tokenizers/xlmr_target10_added_32000` |
| base vocab size | 250002 |
| merged vocab size | 279013 |
| new rows | 29011 |
| device | `cuda` |
| pass methods | random, mean, fvt, align, focus |

## Best Zero-Step Candidate

Best zero-step dev loss: `fvt` with loss `8.490678`.

## Gate Evidence

Evidence:

- `score_table.tsv` has no `TBD`, blank, or unchecked fields.
- input embedding and LM head shapes match tokenizer length for all methods.
- weight tying is preserved for all passing methods.
- zero-step MLM loss is recorded for every method.
- checkpoints are stored under `/home/axt/mnt2/jongha/second_try/checkpoints/04_embedding_init`.

Exit criteria:

- all required methods either pass or have documented implementation result: pass
- at least random, mean, and fvt pass: pass
- no missing/uninitialized rows: pass
- zero-step MLM loss is recorded: pass
- `results.md` has `Gate status: PASS`: pass

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE
