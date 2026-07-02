# v5 Target10 재선정 실행 소요시간 계산

작성 시각: 2026-06-28 16:29 KST  
마감 기준: 2026-06-29 오전, 보수적으로 2026-06-29 12:00 KST  
남은 시간: 약 19시간 30분

## 결론

내일 오전까지 `target10 재선정 + merge + tokenizer + random/FVT 10K MLM 재학습 + Glot500 metric 전체 재평가`를 끝내는 것은 불가능하다.

현재 로그 기준으로 10K MLM만 한 조건당 약 19.3시간이 걸린다. 즉, 재선정 후 `v5_fvt` 한 조건만 다시 학습해도 평가와 보고서 정리 전 단계에서 이미 마감선을 넘는다.

내일 오전 제출을 목표로 하면 다음 경로가 현실적이다.

1. 현재 v5 실험을 완주한다.
2. 완료된 `v5_random`과 `v5_fvt` 10K checkpoint를 비교한다.
3. target10 downstream coverage 문제는 명시적 limitation으로 보고한다.
4. downstream-aware target10 재선정안은 `v5.1 corrected design`으로 문서화한다.

이 프로젝트는 이미 로그, coverage, method comparison, reporting gate가 촘촘히 쌓여 있어서 마감 대응은 충분히 가능하다. 다만 지금 시점에서 새 target10으로 본실험을 갈아엎는 것은 계산상 맞지 않는다.

## 기존 v5 실측 소요시간

| 단계 | 근거 | 실측 소요 |
| --- | --- | ---: |
| full merge | `full_merge_20260626_230847.log`, 23:08:47 -> 00:06:36 | 0:57:49 |
| tokenizer train | `train_v5_tokenizer_20260627_000941.log`, 00:09:41 -> 00:33:26 | 0:23:45 |
| `v5_random` 10K MLM | `train_results.json` `train_runtime=69401.3008` | 19:16:41 |
| `v5_fvt` 10K MLM | `train_results.json` `train_runtime=69436.5034` | 19:17:16 |
| random+FVT 10K MLM 순차 실행 | 위 두 학습 합계 | 38:33:58 |
| v5 모델 1개 전체 평가 | `v5_random` PPPL/Tatoeba/Bible/Taxi/NER/POS/Roundtrip 로그 합계 | 4:41:00 |
| XLM-R + Glot500 baseline 전체 평가 | baseline 로그 합계 | 9:11:13 |

## 재선정 후 full rerun 계산

`downstream-aware target10`으로 새 v5.1을 만들 경우 최소 재실행 범위는 다음과 같다.

| 재실행 항목 | 예상/실측 기준 | 시간 |
| --- | --- | ---: |
| target manifest/stats/symlink 수정 | 추정 | 0:10-0:30 |
| full merge | 실측 | 0:57:49 |
| tokenizer train | 실측 | 0:23:45 |
| embedding init + audit + zero-step | 추정, zero-step 자체는 1분 미만 | 0:30-1:00 |
| `v5_random` 10K MLM | 실측 | 19:16:41 |
| `v5_fvt` 10K MLM | 실측 | 19:17:16 |
| baseline 재평가 | 실측 합계 | 9:11:13 |
| random/FVT post-checkpoint 평가 | 실측 1모델 4:41:00 x 2 | 9:22:00 |
| aggregation/report patch | 추정 | 1:00-3:00 |

계산 결과:

| 시나리오 | 예상 wall-clock |
| --- | ---: |
| full 재선정 리런, 순차 실행 | 약 60-65시간 |
| full 재선정 리런, random/FVT 학습만 2 GPU 병렬화 성공 | 약 40-45시간 |
| 재선정 후 FVT 한 조건만 학습+평가 | 최소 25-27시간 |
| 재선정 후 tokenizer/zero-step까지만 실행 | 약 2-4시간 |

따라서 2026-06-29 오전 마감에는 full 재선정 리런도, 단일 조건 재학습도 맞지 않는다.

## 내일 오전 제출용 권장 플랜

현재 `v5_random`과 `v5_fvt` 10K MLM checkpoint는 모두 준비된 상태다. 남은 핵심 작업은 `v5_fvt` post-checkpoint 평가와 보고서 반영이다.

| 작업 | 예상 시간 | 마감 적합성 |
| --- | ---: | --- |
| `v5_fvt` PPPL/Tatoeba/Bible/Taxi/NER/POS/Roundtrip 평가 | 약 4:41, 여유 포함 5-6시간 | 가능 |
| aggregation refresh + 결과표 확인 | 0:30-1:00 | 가능 |
| report/PPT claim patch | 1:00-2:00 | 가능 |
| final package smoke check | 0:30 | 가능 |

권장 실행선:

```text
현재 v5를 main experiment로 마무리한다.
target10은 공식 task-list membership이 일부 있으나, 기존 로컬 materialization이
tail flag를 undercount했으므로 repair 전까지 measured downstream claim은 보류한다.
downstream-aware target10 재선정은 v5.1 follow-up design으로 분리한다.
```

이렇게 하면 내일 오전까지 제출 가능한 결과물은 다음과 같이 정리된다.

| 결과물 | 상태 |
| --- | --- |
| Glot500-style tokenizer expansion 재연 | 완료 |
| random vs FVT embedding initialization 비교 | 완료 가능 |
| 10K continued MLM random/FVT paired checkpoint | 완료 |
| Glot500 metric 전체 family 실행 | `v5_fvt` 평가만 마치면 완료 |
| target10 downstream claim | 직접 claim 금지, coverage limitation으로 보고 |
| v5.1 재선정안 | 설계/근거 문서로 포함 |

## 의사결정

오늘 결정해야 할 라인은 하나다.

```text
마감 우선이면 current v5를 완주한다.
target downstream direct evidence가 절대 필요하면 마감을 연장하고 v5.1 full rerun으로 간다.
```

현재 남은 시간 기준 추천은 전자다.
