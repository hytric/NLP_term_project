# v5.1 Downstream-Aware Target10 Rerun

작성일: 2026-06-28

v5.1은 v5의 tokenizer/MLM/embedding-initialization pipeline을 유지하되,
target10을 downstream coverage가 있는 언어 중심으로 다시 고르고, PPPL을
Glot500처럼 held-out test set에서 측정하도록 고치는 downstream-aware diagnostic
rerun이다.

기존 v5는 target10이 PPPL/raw-text에는 모두 있었고, 현재 repo에서 확인 가능한 local task-list
기준으로는 `8/10`에 일부 downstream membership이 있다. 다만 기존 로컬
coverage/materialization 산출물은 task list의 `0/1` 컬럼을 availability로 오해해
tail task를 undercount했다. v5.1은 이 약점을 보완하려던 downstream-aware diagnostic
rerun이지만, 그 과정에서 target이 mid/high-resource로 이동한다는 limitation도 함께
보여준다.
또한 기존 v5 PPPL은 local raw `train` split에서 나온 train-source diagnostic이므로,
v5.1에서는 language별 `train/dev/test`를 먼저 고정하고 held-out `test`에서 PPPL을
계산한다.

## Current Decision

Decision after checking the Glot500 paper/eval policy and the corpus-size
distribution of v5.1 target10:

```text
USE_AS_FINAL_EXPERIMENT = v5
V5_MAIN_CLAIM = genuine low-resource XLM-R-unseen target10
TARGET_DOWNSTREAM_CLAIM = no
USE_V5_1_AS = downstream-aware diagnostic / ablation
REASON = v5.1 target downstream coverage comes mostly from mid/high-resource XLM-R-unseen languages
```

The v5 artifacts are the main line because they best support the genuinely
low-resource target claim. v5.1 remains useful and this project is in a strong
position because v5.1 shows an important limitation: benchmark-covered
XLM-R-unseen target languages are generally not the same as strict
corpus-size low-resource targets. The final report should not claim v5 target10
downstream improvement; downstream metrics are available-language replay or
v5.1 diagnostic evidence.

먼저 볼 문서:

| File | Role |
| --- | --- |
| `EXPERIMENT_END_SUMMARY_KO.md` | 실험 종료 시점의 실제 결과, 가능한 주장/불가능한 주장 |
| `../v5.2/README.md` | 최종 보고용 framing: v5 main, v5.1 diagnostic |
| `CURRENT_STATUS_KO.md` | 지금 어디까지 왔는지 보는 live dashboard |
| `LAUNCH_READINESS_REVIEW_KO.md` | Glot500 재연 가능성, novelty, gate 판정 |
| `STRICT_RERUN_CHECKLIST_KO.md` | 새 strict rerun의 지속 업데이트 체크리스트 |
| `RUNTIME_AND_DATA_FRACTION_PLAN_KO.md` | 데이터 비율, GPU/batch, 단계별 ETA |
| `DATASET_SIZE_AUDIT_KO.md` | raw/downstream train-dev-test 데이터 양 audit |
| `Plan.md` | 실행 단계와 gate |
| `0_tokenizer/00_data_scope/strict_data_composition_by_language.md` | 언어별 train/dev/test, XLM-R, downstream overlap 표 |

| Item | v5 | v5.1 |
| --- | ---: | ---: |
| language-script total | 102 | 102 |
| XLM-R-seen/head | 92 | 92 |
| target/tail | 10 | 10 |
| target with local task-list membership | 8/10 | 8/10 |
| target with Bible retrieval | 7/10 | 6/10 |
| target with Roundtrip alignment | 0/10 | 6/10 |
| target with NER | 1/10 | 6/10 |
| target with Tatoeba | 0/10 | 3/10 |
| target with POS | 1/10 | 0/10 |
| measured target downstream claim | pending repair | diagnostic |
| PPPL split discipline | train-source diagnostic | held-out test |

## Selected Target10

| language_script | role | downstream coverage |
| --- | --- | --- |
| `guj_Gujr` | target downstream | Bible, Roundtrip, NER |
| `asm_Beng` | target downstream | Bible, Roundtrip, NER |
| `srp_Cyrl` | target downstream | Bible, Roundtrip, NER |
| `sun_Latn` | target downstream | Bible, Roundtrip, NER |
| `zsm_Latn` | target downstream | Tatoeba, Bible, Roundtrip |
| `aze_Latn` | target downstream | Tatoeba, NER |
| `fil_Latn` | target downstream | Bible, Roundtrip |
| `bos_Latn` | target downstream | Tatoeba, NER |
| `dzo_Tibt` | script diversity anchor | PPPL only |
| `sat_Olck` | script diversity anchor | PPPL only |

## Active Paths

| Artifact | Path |
| --- | --- |
| docs root | `docs/exp/v5.1` |
| raw symlink root | `/home/axt/mnt2/jongha/v5_1_glot50010/raw` |
| data/output root | `/home/axt/mnt2/jongha/v5_1_glot50010` |
| stats csv | `0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv` |
| target manifest | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| strict split table | `0_tokenizer/00_data_scope/strict_data_composition_by_language.md` |
| merge report | `0_tokenizer/merge/Glot500_v51_glot50010_xlmr100.report.json` |

## Dry-Run Status

The v5.1 merge dry-run passed.

| Check | Value |
| --- | ---: |
| raw symlink count | 102 |
| missing language dirs | 0 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 145,832,137 |
| planned seen samples | 109,334,640 |
| planned target samples | 53,273,459 |
| planned total samples | 162,608,099 |

v5.1 is larger than v5 because the downstream-covered target languages are much
higher resource. Expect full merge output and MLM preprocessing to be larger.

Recommended first strict run:

```text
DATA_FRACTION=5%
SCALE=1.5
EXPECTED_LINES=8,130,401
EXPECTED_TEXT_SIZE=~1.67G
GPU_PLAN=4x A6000 if available, effective batch 384
```

Current execution note:

```text
MLM_3K_STATUS=running_random_first
RUN=v51_strict5pct_random_mlm_3k
LATEST_STEP=1869/3000 at 2026-06-28 21:56 KST
LATEST_LOSS=4.0544 at step 1800
RANDOM_ETA=2026-06-29 00:28 KST
GPU_PLAN_USED=0,1,3
LAUNCHER_PID=2985609
EVAL_DATA_READY=yes
CHECKPOINT_STATUS=pending checkpoint-3000
```

Live evidence:

| Artifact | Path |
| --- | --- |
| one-command live refresh | `bash scripts/refresh_v51_live_status.sh` |
| training status | `2_training/training_status.md` |
| report table | `4_reporting/00_tables/table_02_training_status.md` |
| current dashboard | `CURRENT_STATUS_KO.md` |
| handoff watcher | `scripts/watch_v51_mlm_handoff.sh` |
| watcher smoke log | `2_training/watch_logs/watch_v51_mlm_handoff_20260628_193054.log` |

## Evaluation Readiness

v5.1 evaluation data and wrappers are prepared. The remaining blocker is
checkpoint availability, not data layout. As of `2026-06-28 21:56 KST`,
`v51_random` is still training and no checkpoint model file has been written.

| Artifact | Path |
| --- | --- |
| evaluation README | `3_evaluation/README.md` |
| checkpoint runbook | `3_evaluation/POST_CHECKPOINT_EVAL_RUNBOOK_KO.md` |
| coverage summary | `3_evaluation/00_coverage/coverage_summary.tsv` |
| model matrix | `3_evaluation/model_matrix.tsv` |
| eval wrapper | `scripts/run_v51_post_checkpoint_evals.sh` |

Current target-side coverage:

| Metric | Target10 available |
| --- | ---: |
| PPPL | 10 / 10 |
| Tatoeba retrieval | 3 / 10 |
| Bible retrieval | 6 / 10 |
| NER | 6 / 10 |
| Roundtrip alignment | 6 / 10 |
| POS | 0 / 10 |
| Taxi1500 | 0 / 10 |

## Main Claim Boundary

v5.1 can support a stronger target-side evaluation claim than v5:

```text
The corrected target10 includes direct downstream coverage for 8/10 target
languages, enabling target-subset analysis for Bible/Roundtrip/NER/Tatoeba
where data exists.
```

Still do not claim full target10 downstream coverage. POS and Taxi1500 target
coverage remain unavailable.

## Held-Out PPPL Correction

v5.1의 PPPL exit line은 v5와 다르다.

```text
merge/tokenizer/MLM input = train-only
PPPL input = held-out dev/test
```

필수 규칙:

- 각 language-script에서 dev `1000`, test `1000` 문장을 먼저 제외한다.
- tokenizer training corpus에도 dev/test 문장을 넣지 않는다.
- continued MLM pretraining에는 train-only corpus만 사용한다.
- PPPL command는 `PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test`로 실행한다.
- 기존 v5 `PPPL_SPLIT=train` 값과 v5.1 held-out PPPL 값을 같은 이름으로 섞지 않는다.

Current split planning artifacts:

```text
0_tokenizer/00_data_scope/strict_split_manifest.tsv
0_tokenizer/00_data_scope/strict_split_indices.jsonl
0_tokenizer/00_data_scope/strict_split_verification_summary.md
```

These are now Arrow-verified artifacts with status `PASS`. The previous
stats-based planning files are preserved as `*.stats_plan.*`.
