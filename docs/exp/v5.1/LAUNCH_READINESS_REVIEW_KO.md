# v5.1 Launch Readiness Review

업데이트: 2026-06-28 18:37 KST

## 판정

```text
READY_TO_LAUNCH_FULL_TRAINING = launched_for_3K_matched_pair
READY_TO_LAUNCH_NEXT_GATE_WORK = yes
NEXT_GATE_WORK = monitor random MLM 3K, then FVT MLM 3K
EVAL_DATA_READY = yes
```

v5.1은 설계 방향이 좋고, v5의 downstream coverage 한계를 잘 드러낸다. 특히
target10을 downstream-aware하게 바꾼 결과, benchmark-covered XLM-R-unseen 언어가
엄격한 low-resource target set과 다르다는 점을 확인했다. 따라서 v5.1은 본 실험이
아니라 diagnostic/ablation으로 둔다.

## v5와 v5.1 사용 판정

```text
RECOMMENDATION = keep_v5_as_main_low_resource_experiment
KEEP_V5_1 = yes, but diagnostic/downstream-aware ablation only
```

v5를 버릴 필요가 없는 정도가 아니라, low-resource claim에는 v5가 더 적합하다.
이 프로젝트의 좋은 점은 v5에서 진짜 low-resource target10과 전체 파이프라인을 이미
확보했다는 것이다. 다만 v5 target10 downstream은 local task-list membership `8/10`이
있어도 local materialization repair 전에는 성능 향상 claim을 하지 않는다. v5.1은
"downstream-aware target을 고르면 대부분 mid/high-resource로 이동한다"는
limitation/ablation으로 설명한다.

## 요구사항별 증거

| 요구사항 | 현재 판정 | 증거 | 남은 일 |
| --- | --- | --- | --- |
| Glot500-style 92 seen + 10 target 제한 | pass | `README.md`, `strict_data_composition_by_language.md` | 없음 |
| target10이 XLM-R unseen인지 | pass | target10 `xlm_r_training_language=no` | 없음 |
| target10이 downstream을 고려했는지 | pass | Tatoeba 3, Bible 6, Roundtrip 6, NER 6 | POS/Taxi limitation 명시 |
| dev/test hold-out을 먼저 뺐는지 | pass | Arrow-verified split manifest/indices PASS | 없음 |
| train-only merge가 준비됐는지 | pass | 5% merge report PASS, line count 8,130,401 | 없음 |
| tokenizer 확장 비교가 준비됐는지 | pass | tokenizer audit failures 0 | 없음 |
| random vs FVT initialization novelty | running | random/FVT init reports pass; random 3K running | FVT 3K까지 완료 |
| held-out PPPL final metric | ready after checkpoint | PPPL guard + split-index support | checkpoint 이후 `PPPL_SPLIT=test` |
| downstream Glot500 metric families | ready after checkpoint | coverage summary + materialized Bible/Roundtrip + v5.1 wrapper | v5.1 checkpoint 이후 실행 |
| similarity / 2D map novelty | planned | `3_evaluation/08_embedding_similarity/README.md` | sentence embeddings/plots 생성 |
| report/PPT table source | pass for plan, pending for results | data composition table, runtime plan | results 삽입 후 refresh |

## Glot500 재연 충실도

현재 v5.1이 Glot500 방식을 더 잘 따라가는 부분:

- raw corpus를 language-script 단위로 `train/dev/test`로 분리한다.
- continued MLM에는 train만 넣는다.
- PPPL은 held-out `test`에서 계산하도록 계획한다.
- retrieval/tagging/alignment metric family를 Glot500의 7개 평가 축에 맞춘다.
- head/tail/all을 분리해 집계한다.

아직 Glot500-style final result claim을 막는 부분:

- MLM/evaluation이 v5.1 strict line에서는 아직 완료되지 않았다.

## Novelty 배치

v5.1 novelty는 다음 세 갈래로 잡는 것이 좋다.

| Novelty 축 | 실험 위치 | 방어 논리 |
| --- | --- | --- |
| embedding initialization | `random` vs `FVT` matched pair | vocab extension 때 새 token embedding 초기화가 downstream/PPPL에 주는 영향 |
| downstream-aware target selection | target10 재선정 | PPPL-only target이 아니라 retrieval/NER/roundtrip target evidence 확보 |
| sentence embedding similarity | `08_embedding_similarity` | 같은 의미/같은 언어/roundtrip 문장이 layer 8 embedding에서 어떻게 모이는지 시각화 |

claim boundary:

- POS와 Taxi1500은 target-side novelty로 주장하지 않는다. POS는 v5에 공식 membership
  1개가 있으나 materialization/eval repair 전에는 measured claim으로 승격하지 않는다.
- Bible/Roundtrip/NER/Tatoeba는 coverage가 있는 target subset에 대해서만 주장한다.
- v5 train-source PPPL은 diagnostic으로만 두고, final PPPL은 v5.1 held-out test를 사용한다.

## 다음 단계로 넘어가는 라인

### Gate 1: Split Evidence

통과 조건:

```text
strict split row count verification complete
or documented mismatch exception table accepted
```

현재 상태:

```text
pass
```

### Gate 2: 5% Train-Only Merge

통과 조건:

```text
5% merge report status PASS
actual_total_samples > 0
dev/test indices excluded
```

현재 상태:

```text
pass
```

### Gate 3: Tokenizer / Initializer

통과 조건:

```text
extended tokenizer exists
tokenizer audit failure = 0
random and FVT checkpoints pass mask remap and tied-head checks
```

현재 상태:

```text
pass
```

### Gate 4: Matched MLM Pair

통과 조건:

```text
v5_random and v5_fvt use same corpus, tokenizer, seed, batch, steps, schedule
3K checkpoints both complete
```

현재 상태:

```text
running_random_first
```

### Gate 5: Evaluation Data / Commands

통과 조건:

```text
coverage_summary exists
Bible/Roundtrip target materialization exists
post-checkpoint runner can print status
```

현재 상태:

```text
pass
```

증거:

```text
docs/exp/v5.1/3_evaluation/00_coverage/coverage_summary.tsv
docs/exp/v5.1/3_evaluation/03_retrieval_bible/materialization_summary.tsv
docs/exp/v5.1/3_evaluation/07_roundtrip_alignment/materialization_summary.tsv
scripts/run_v51_post_checkpoint_evals.sh
```

## 실행 판단

오늘 바로 할 수 있는 안전한 일:

1. running random 3K MLM을 모니터링한다.
2. 이어지는 FVT 3K MLM이 같은 corpus/tokenizer/batch/step으로 시작되는지 확인한다.
3. held-out PPPL과 downstream queue를 strict checkpoint 기준으로 실행한다.
4. similarity table/2D map을 생성한다.

지금 바로 하면 안 좋은 일:

- random/FVT를 서로 다른 corpus/step/batch로 학습시키는 것.
- v5 train-source PPPL을 v5.1 final PPPL처럼 쓰는 것.
- POS/Taxi1500에서 target10 improvement를 주장하는 것.
