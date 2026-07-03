# v5.2 Glot500-Style Target7 Run

작성일: 2026-06-28

v5.2는 보고용 framing이 아니라 실제 재시작 실험이다. 핵심은 Glot500 논문 실험 흐름을
따르되, target을 `XLM-R-unseen tail + downstream 가능한 최소 corpus band`의 7개 언어로
고정하는 것이다.

## Current Decision

```text
MAIN_EXPERIMENT = v5.2
CORPUS = 92 XLM-R-seen replay + 7 XLM-R-unseen target
TARGET_SET = dtp_Latn, xav_Latn, bam_Latn, csb_Latn, ile_Latn, lij_Latn, fur_Latn
TOKENIZER = Glot500-style SentencePiece unigram + XLM-R SPM append
MAIN_AXIS = new-token embedding initialization
INIT_METHODS = random, mean, fvt, weighted_fvt, family_mean
YAMAGUCHI = appendix/additional experiment, not main
CHECKPOINT_EVAL = 8h run, about 5-8 checkpoints, update downstream table per checkpoint
```

## Key Files

| File | Role |
| --- | --- |
| `RUNBOOK_KO.md` | 실제 실행 순서와 command |
| `EXPERIMENT_DESIGN_KO.md` | 확정된 실험 설계 |
| `GOAL_COMMAND_KO.md` | Codex goal로 걸 명령어 문안 |
| `ppt_guide.md` | 발표 개요 작성용 rough guide |
| `0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv` | 확정 target7 manifest |
| `1_data_scope/low_resource_task_fill_candidates.tsv` | task별 target 후보와 상태 |
| `3_evaluation/incremental_table_tracker.tsv` | checkpoint별 table 갱신 tracker |

## Prepared State

현재 준비된 것:

- target7 selection strategy added to `preprocessing/prepare_v5_glot50010_merge_inputs.py`
- v5.2 prepare/merge/tokenizer/initializer/training wrappers added
- `92/92` XLM-R-seen raw links and `7/7` target raw links validated
- target manifest written under `docs/exp/v5.2/0_tokenizer/miscellaneous/`

다음 실제 heavy step은 corpus merge다.
