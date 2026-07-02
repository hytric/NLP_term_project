# v5 Pending Result Registry

Last updated: 2026-06-28

This file keeps unresolved report/slide entries explicit. A pending entry is
acceptable in an execution draft only when its gate and claim impact are clear.

Live MLM progress, storage readiness, and paired launcher transition status are
operational evidence, not model-quality evidence. Use
`../2_training/mlm_progress_eta.md`, `../2_training/live_training_health.md`,
`../2_training/storage_readiness.md`, and
`../2_training/paired_launcher_transition.md` to explain whether the paired run
is still waiting, running, or wrapper-ready, but promote only parsed aggregation
rows into result tables.

## Status Labels

| Label | Meaning | Allowed in final package? |
| --- | --- | --- |
| `measured` | Parsed by `scripts/aggregate_v5_metrics.py` from a completed raw output | yes |
| `waiting checkpoint` | The metric needs a matched v5 checkpoint that does not exist yet | no, replace after evaluation |
| `running` | A job is active, but final metric output is not complete or parsed | no, live status only |
| `blocked-data` | The metric family is retained, but local data or runner artifacts are missing | yes, as a limitation row |
| `coverage-limited` | The task has data, but not for the selected target10 subset | yes, with coverage note |

## Current Pending And Blocked Rows

| Area | Current status | Gate to promote | Claim impact |
| --- | --- | --- | --- |
| `v5_random` 10K MLM | selected 10K checkpoint exists; wrapper-ready; PPPL/downstream diagnostic rows parsed | none | diagnostic random baseline for the paired method comparison |
| `v5_fvt` 10K MLM | running; not wrapper-ready | selected checkpoint and model files exist | unlocks matched FVT-vs-random evaluation |
| after-MLM PPPL for v5 models | `v5_random` measured; `v5_fvt` waiting checkpoint | PPPL output parsed for both `v5_random` and `v5_fvt` | intrinsic after-training comparison |
| Tatoeba for v5 models | `v5_random` measured; `v5_fvt` waiting checkpoint; target10 coverage `0/10` | retrieval output parsed for both v5 models | available-language retrieval comparison only |
| Taxi1500 for v5 models | `v5_random` measured; `v5_fvt` waiting checkpoint; local data is English-only | classification output parsed for both v5 models | limited text-classification comparison |
| Glot500-base POS | measured with `TRAIN_LANGS=tur_Latn` caveat | completed non-empty `test_results.txt` parsed after evaluator exit | external reference tagging row is available |
| v5 NER/POS | `v5_random` measured; `v5_fvt` waiting checkpoint; target10 materialized coverage `0/10` | final tagging outputs parsed for both v5 checkpoints | available-language tagging comparison only |
| Bible retrieval | XLM-R/Glot500-base/v5-random measured, v5-FVT waiting checkpoint, coverage `74/102`, target10 `0/10` | retrieval output parsed for both v5 checkpoints | available-language Bible retrieval comparison only |
| Roundtrip alignment | XLM-R/Glot500-base/v5-random measured, v5-FVT waiting checkpoint, coverage `74/102`, target10 `0/10` | parsed rows for `v5_random` and `v5_fvt` after matched checkpoints | retained metric; diagnostic v5-random row available, no v5 method claim yet |

## Supporting Promotion Gates

These rows are not metric results, but they must stay synchronized before a
new result is promoted into the report or slides.

| Gate | Current status | Sync trigger | Claim impact |
| --- | --- | --- | --- |
| selected checkpoint manifest | generated; waiting for matched v5 checkpoints | any model path, model file, or `trainer_state.json` change | prevents hand-picked checkpoint claims |
| MLM progress ETA | generated; random ready and FVT running until the launcher finishes | live log/progress-bar changes | operational waiting evidence only; never a result claim |
| live training health | generated; process/GPU/log checks stay clean while waiting | process, GPU, or critical log-pattern changes | confirms wait/run health only; never a result claim |
| storage readiness | generated; output paths and free-space checks stay ready | checkpoint save, cache cleanup, or evaluation output changes | prevents avoidable write failures; never a result claim |
| paired launcher transition | generated; random ready and FVT running under the paired launcher | launcher process, random/FVT log, or wrapper-ready status changes | confirms random-to-FVT handoff health only; never a result claim |
| visual evidence package | generated for current setup and coverage artifacts | tokenizer audit, zero-step summary, or coverage source data changes | keeps figure captions and slide assets source-tracked |
| metric fidelity matrix | ready for current coverage and blockers | any metric coverage, blocked-data, or measured-model status change | defends the claim that Glot500 metric families were retained |
| report-slide crosswalk | ready for current report and deck sections | any promoted result, figure, table, or limitation wording change | keeps report and PPT from drifting |
| citation maps | ready for current related-work and slide claim boundaries | any cited background, method lineage, or slide citation wording change | separates literature support from local v5 numeric evidence |

## Replacement Rule

```text
live log/dev score -> running status only
launcher/storage health -> operational gate only
completed raw metric file -> aggregate -> measured table value
missing local data/runner -> blocked-data limitation row
target subset absent from task -> coverage-limited note
```

The final deck/report can keep `blocked-data` and `coverage-limited` entries,
but it should not keep unresolved result slots, `running`, or `waiting
checkpoint` entries as if they were results.
