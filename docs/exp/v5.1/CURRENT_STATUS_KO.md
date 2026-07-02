# v5.1 현재 상태

업데이트: 2026-06-28 21:56 KST

## 한 줄 결론

```text
READY_TO_LAUNCH_TRAINING = no
READY_TO_LAUNCH_MLM_3K = stopped_before_checkpoint
MLM_3K_STATUS = stopped_random_partial
PRIMARY_REASON = experiment was terminated before checkpoint-3000; random init stopped at 1869/3000
RECOMMENDED_FIRST_RUN = 5% corpus, SCALE=1.5, 3K steps pair
EVAL_DATA_READY = yes
```

v5.1은 v5의 좋은 실험 구조를 유지하면서, target10을 downstream-aware하게 다시
고른 diagnostic/ablation line이다. 방향은 좋고, split verification과 5% dry-run도
통과했고, 5% train-only corpus, tokenizer/audit, random/FVT initializer까지
완료했다. 현재 다음 실행 단위였던 3K MLM matched pair를 시작했고,
`random` initializer run은 `1869/3000` step에서 종료되었다. final checkpoint가
없으므로 Glot500-style held-out PPPL/downstream/similarity 결과는 생성되지 않았다.
종료 결과는 `EXPERIMENT_END_SUMMARY_KO.md`에 정리했다.

## v5 vs v5.1 판단

```text
FINAL_LINE = v5
V5_MAIN_CLAIM = genuine_low_resource_target10_intrinsic_proxy
V5_TARGET_DOWNSTREAM_CLAIM = no
V51_ROLE = downstream_aware_diagnostic_ablation
DO_NOT_USE_V5_TRAIN_PPPL_AS_FINAL_GLOT500_PPPL = true
```

v5.1은 downstream coverage를 만들기 위해 target10을 재선정했지만, 그 결과
`guj_Gujr`, `aze_Latn`, `fil_Latn`, `bos_Latn`처럼 mid/high-resource target이
포함됐다. 따라서 low-resource 논문의 본 실험은 v5로 둔다. 기존 v5의
train-source PPPL은 Glot500-style held-out PPPL로 과장하지 않고 intrinsic
diagnostic으로 표시한다. v5.1은 downstream benchmark가 붙는 XLM-R-unseen 언어가
엄격한 low-resource target set과 다르다는 limitation/diagnostic evidence로 둔다.

## 지금 완료된 것

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| target10 재선정 | done | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| 언어별 train/dev/test 계획 | done, verified | `0_tokenizer/00_data_scope/strict_split_manifest.tsv` |
| Arrow split verification | done | `0_tokenizer/00_data_scope/strict_split_verification_summary.md` |
| 언어별 데이터 구성 표 | done | `0_tokenizer/00_data_scope/strict_data_composition_by_language.md` |
| full-size dry-run | done | `0_tokenizer/merge/Glot500_v51_glot50010_xlmr100.report.json` |
| 5% strict dry-run | done | `0_tokenizer/merge/Glot500_v51_glot50010_xlmr100_strict_5pct.report.json` |
| 5% train-only merge | done | `/home/axt/mnt2/jongha/v5_1_glot50010/data/Glot500_v51_glot50010_xlmr100_strict_5pct.txt` |
| tokenizer train | done | `/home/axt/mnt2/jongha/v5_1_glot50010/tokenization/output_strict_5pct/Glot500_extended_spm` |
| tokenizer audit | done | `0_tokenizer/03_audit/strict_5pct/results.md` |
| random/FVT initializer | done | `/home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct` |
| Bible retrieval materialization | done | `3_evaluation/03_retrieval_bible/materialization_summary.tsv` |
| Roundtrip alignment materialization | done | `3_evaluation/07_roundtrip_alignment/materialization_summary.tsv` |
| raw/downstream dataset-size audit | done | `DATASET_SIZE_AUDIT_KO.md`, `3_evaluation/00_coverage/dataset_size_audit.tsv` |
| v5.1 eval wrappers | done | `scripts/run_v51_post_checkpoint_evals.sh` |
| similarity pair input | done | `3_evaluation/08_embedding_similarity/similarity_pairs.tsv` |
| report/PPT scaffold | done | `4_reporting/03_final_report/paper_draft_ko.md`, `4_reporting/02_slides/ppt_content_ko.md` |
| GPU/batch/ETA 계획 | done | `RUNTIME_AND_DATA_FRACTION_PLAN_KO.md` |
| live training setting/GPU status | done | `2_training/training_status.md`, `4_reporting/00_tables/table_02_training_status.md` |
| PPPL held-out policy | done | `../v5/MLM_HELDOUT_POLICY_KO.md`, `Plan.md` |

## 데이터 구성 핵심 숫자

| 범위 | total | seen/head | target/tail |
| --- | ---: | ---: | ---: |
| PPPL / raw text | 102 | 92 | 10 |
| Tatoeba retrieval | 66 | 63 | 3 |
| Bible retrieval | 80 | 74 | 6 |
| Roundtrip alignment | 80 | 74 | 6 |
| NER | 84 | 78 | 6 |
| POS nominal coverage | 58 | 58 | 0 |
| POS countable local split files | 9 | 9 | 0 |
| Taxi1500 | 1 | 1 | 0 |

Target10은 모두 XLM-R 학습 언어가 아니며, 각 언어는 현재 계획상
대부분 `train = source - 2000`, `dev = 1000`, `test = 1000`으로 잡혀 있다.
단, `azb_Arab`, `uig_Latn`, `san_Latn`은 실제 Arrow row count가 작아
`small_policy=shrink` 예외를 적용했다.

실제 train/dev/test 및 downstream pair/sample 수는 `DATASET_SIZE_AUDIT_KO.md`에
정리했다. POS는 task-list 기준 nominal coverage와 현재 로컬 materialized split
파일 수가 다르므로, 최종 보고에서는 countable local split 기준을 함께 명시한다.

## Strict Split Verification

| 항목 | 값 |
| --- | ---: |
| verified language-scripts | 102 |
| status | PASS |
| Arrow source examples | 1,169,433,406 |
| Arrow train examples | 1,169,231,705 |
| Arrow dev examples | 100,850 |
| Arrow test examples | 100,851 |
| shrink exception rows | 3 |

보존 파일:

```text
strict_split_manifest.stats_plan.tsv
strict_split_indices.stats_plan.jsonl
```

## 5% Merge 결과

| 항목 | 값 |
| --- | ---: |
| scale | 1.5 |
| planned seen samples | 5,466,732 |
| planned target samples | 2,663,669 |
| planned total samples | 8,130,401 |
| actual total samples | 8,130,401 |
| actual line count | 8,130,401 |
| output size | 1.7G |
| status | PASS |

Output:

```text
/home/axt/mnt2/jongha/v5_1_glot50010/data/Glot500_v51_glot50010_xlmr100_strict_5pct.txt
```

## Tokenizer 결과

| 항목 | 값 |
| --- | ---: |
| tokenizer dir | `/home/axt/mnt2/jongha/v5_1_glot50010/tokenization/output_strict_5pct/Glot500_extended_spm` |
| audited languages | 102 |
| audit failures | 0 |
| base vocab size | 250,002 |
| target vocab size | 370,051 |
| novel tokens | 120,049 |
| byte tokens | 256 |
| base `<mask>` id | 250,001 |
| target `<mask>` id | 370,050 |
| mean delta tokens/word | -0.194897 |

## Initializer 결과

| 항목 | random | FVT |
| --- | ---: | ---: |
| output dir | `/home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct/v5_random` | `/home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct/v5_fvt` |
| target embedding rows | 370,051 | 370,051 |
| new token rows | 120,049 | 120,049 |
| random initialized | 120,049 | 0 |
| FVT initialized | 0 | 119,792 |
| global mean rows | 0 | 257 |
| `<mask>` remap diff | 0.0 | 0.0 |
| LM head tied | true | true |

## 아직 막고 있는 Gate

| Gate | 상태 | 다음 조치 |
| --- | --- | --- |
| strict split verification | done | Arrow count verification PASS |
| 5% train-only merge | done | report PASS, line count matched |
| tokenizer train | done | audit failures 0 |
| random/FVT initializer | done | mask remap diff 0.0, LM head tied |
| random/FVT MLM 3K pair | stopped before final checkpoint | random partial run, `1869/3000`; FVT not started |
| held-out PPPL | ready after checkpoint | `PPPL_SPLIT=test`, split indices ready |
| downstream | ready after checkpoint | Tatoeba/Bible/NER/Roundtrip target subset available |
| similarity | input ready, embedding pending | 22,600 pair input ready; checkpoint 필요 |

## 현재 MLM 실행

| 항목 | 값 |
| --- | --- |
| launcher PID | none |
| active run | `v51_strict5pct_random_mlm_3k` |
| GPUs | `CUDA_VISIBLE_DEVICES=0,1,3` |
| NPROC | `3` |
| per-device batch | `8` |
| grad accumulation | `16` |
| effective batch | `384` |
| max steps | `3000` |
| optimizer | `AdamW` |
| initial LR | `5e-5` |
| latest checked step | `1869 / 3000` |
| progress | `62.30%` |
| latest logged loss | `4.0544` at step 1800 |
| latest logged LR | `2.01e-05` at step 1800 |
| ETA | n/a, experiment stopped |
| checkpoint status | no model file; final eval not runnable |
| live status doc | `2_training/training_status.md` |
| reporting table | `4_reporting/00_tables/table_02_training_status.md` |
| launch log | `/home/axt/mnt2/jongha/v5_1_glot50010/runs/logs/launch_v51_strict5pct_mlm3k_20260628_1825.log` |
| train log | `/home/axt/mnt2/jongha/v5_1_glot50010/runs/logs/train_v5_v51_strict5pct_random_mlm_3k_20260628_182508.log` |
| output dir | `/home/axt/mnt2/jongha/v5_1_glot50010/runs/v51_strict5pct_random_mlm_3k` |

종료 확인 기준으로 training loop는 더 이상 실행 중이 아니며, random run은 `3000` step 중
`1869` step까지 진행한 뒤 멈췄다. optimizer는 plain Adam이 아니라 Hugging Face
Trainer의 `AdamW`이며, LR은 `5e-5` 시작값에서 scheduler에 따라 감소 중이다.
현재 v5.1 MLM/eval 프로세스는 남아 있지 않다. checkpoint 파일은 없으므로 PPPL,
downstream, similarity 결과는 final metric으로 생성되지 않았다.

## 평가 준비 상태

| 항목 | 상태 | 경로 |
| --- | --- | --- |
| eval data root | ready | `/home/axt/mnt2/jongha/v5_1_glot50010/eval_data_download` |
| eval model matrix | ready, but v5.1 checkpoints missing | `3_evaluation/model_matrix.tsv` |
| coverage summary | ready | `3_evaluation/00_coverage/coverage_summary.tsv` |
| post-checkpoint runbook | ready | `3_evaluation/POST_CHECKPOINT_EVAL_RUNBOOK_KO.md` |
| execution wrapper | ready | `scripts/run_v51_post_checkpoint_evals.sh` |
| similarity runner | ready | `scripts/run_v51_similarity.sh` |
| handoff watcher | smoke-tested, stopped before checkpoint | `scripts/watch_v51_mlm_handoff.sh`, `2_training/watch_logs/watch_v51_mlm_handoff_20260628_201638.log` |

Post-checkpoint 핵심 명령:

```bash
bash scripts/run_v51_post_checkpoint_evals.sh status
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh pppl
GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh downstream
GPU=0 MODEL_KEYS=v51_random,v51_fvt bash scripts/run_v51_similarity.sh
```

## 지금부터 ETA

| 단계 | 예상 시간 | 마감 관점 |
| --- | ---: | --- |
| random MLM 3K, 3 GPUs | stopped before checkpoint | final checkpoint 없음 |
| FVT MLM 3K, 3 GPUs | not started | matched comparison 불가 |
| held-out PPPL + downstream + similarity | not run | checkpoint 부재 |
| report/PPT refresh | done for partial trace/scaffold | final metric 없음 |

내일 오전까지 완주를 노리려면 v5.1은 `5% + 3K`를 first strict line으로 두고,
기존 v5 결과는 fallback/report scaffold로 계속 유지하는 전략이 가장 현실적이다.

## 기존 v5 fallback 실행 상태

v5.1 strict correction이 마감 전 완주하지 못할 수 있으므로, 기존 v5 결과는 발표
fallback evidence로 계속 살린다.

| 항목 | 상태 |
| --- | --- |
| running job | `bash scripts/run_v5_post_checkpoint_evals.sh downstream` |
| PID | `2966371` |
| current metric | `retrieval_bible:v5_fvt` running |
| log | `/home/axt/mnt2/jongha/v5_glot50010/runs/finalization_logs/downstream_v5_fvt_resume_20260628_173303.log` |
| current GPU snapshot | GPU 2 active, about 99% utilization |
| final metric rule | only use `docs/exp/v5/3_evaluation/09_aggregation/` after parser reads completed result files |

## 바로 다음 실행 단위

1. random 3K run이 끝나는지 확인한다.
2. launcher가 이어서 FVT 3K run을 시작하는지 확인한다.
3. checkpoint 완료 후 held-out PPPL과 downstream/similarity queue를 실행한다.
4. 장시간 대기는 `scripts/watch_v51_mlm_handoff.sh`로 checkpoint pair readiness를 감시한다.
5. `strict_data_composition_by_language.md`와 verification summary를 report/PPT 데이터 구성 표 출처로 사용한다.
