# v5 Post-Checkpoint Evaluation Recovery Runbook

작성 상태: execution draft, 2026-06-27 기준.

이 문서는 matched `v5_random`/`v5_fvt` checkpoint가 준비된 뒤, PPPL과
Glot500-required downstream evaluation을 실행하다가 일부 metric이 오래 걸리거나 실패할
때 사용하는 복구 절차이다. 최종 report/PPT claim은 이 문서가 아니라
`09_aggregation/`, `finalization_gate_status.md`, `final_claim_decision_tree.md`,
`final_claim_freeze_audit.md`가 허용한 값만 사용한다.

## 1. 시작 전 확인

먼저 model matrix와 checkpoint manifest를 갱신한다.

```bash
python3 scripts/refresh_v5_reporting.py
bash scripts/run_v5_post_checkpoint_evals.sh status
sed -n '1,90p' docs/exp/v5/2_training/paired_launcher_transition.md
```

`model_matrix.tsv`에서 두 row가 모두 아래 상태여야 한다.

```text
v5_random ready_for_wrapper=yes
v5_fvt    ready_for_wrapper=yes
```

둘 중 하나라도 `no`이면 evaluation을 시작하지 않는다. 이 상태에서는
`post_checkpoint_eval_queue.md`가 `waiting_model` row를 유지해야 정상이다.
`../2_training/paired_launcher_transition.md`가 `random_running_fvt_waiting`이면 이것도 정상
대기 상태이다. 이 verdict는 launcher health 증거일 뿐이고, FVT 결과나 downstream
claim을 열어주지는 않는다.

## 2. 권장 실행 순서

최종 pass는 아래 한 줄을 우선 사용한다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

이 wrapper는 다음 순서로 움직인다.

1. PPPL `v5_random`
2. PPPL `v5_fvt`
3. Tatoeba retrieval pair
4. Bible retrieval pair
5. Taxi1500 text classification pair
6. NER pair
7. POS pair
8. Roundtrip alignment pair
9. metric family마다 reporting refresh

PPPL을 먼저 실행하는 이유는 target10 raw-text coverage가 `10/10`이고, novelty claim의
after-MLM intrinsic evidence가 여기서 결정되기 때문이다.

## 3. 긴 실행을 나누는 방법

machine time이나 GPU queue 때문에 한 번에 `all`을 돌리기 어렵다면 아래처럼 나눈다.

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

tagging만 다시 돌릴 때:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh tagging
```

Bible만 다시 돌릴 때:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh bible
```

Roundtrip만 다시 돌릴 때:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh roundtrip
```

항상 paired wrapper를 먼저 사용한다. 개별 metric command는 복구/디버깅에서만 사용한다.

## 4. 개별 metric 복구 명령

PPPL 한쪽만 실패했을 때:

```bash
MAX_EXAMPLES_PER_LANGUAGE=100 MAX_LENGTH=128 MASK_BATCH_SIZE=64 \
  bash scripts/run_v5_eval_metric.sh pppl v5_random 0

MAX_EXAMPLES_PER_LANGUAGE=100 MAX_LENGTH=128 MASK_BATCH_SIZE=64 \
  bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

retrieval 한쪽만 실패했을 때:

```bash
bash scripts/run_v5_eval_metric.sh retrieval_tatoeba v5_random 0
bash scripts/run_v5_eval_metric.sh retrieval_tatoeba v5_fvt 1

bash scripts/run_v5_eval_metric.sh retrieval_bible v5_random 0
bash scripts/run_v5_eval_metric.sh retrieval_bible v5_fvt 1
```

Taxi1500 한쪽만 실패했을 때:

```bash
bash scripts/run_v5_eval_metric.sh text_classification v5_random 0
bash scripts/run_v5_eval_metric.sh text_classification v5_fvt 1
```

tagging 한쪽만 실패했을 때:

```bash
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner v5_random 0
TRAIN_LANGS=eng_Latn bash scripts/run_v5_eval_metric.sh ner v5_fvt 1

TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos v5_random 0
TRAIN_LANGS=tur_Latn bash scripts/run_v5_eval_metric.sh pos v5_fvt 1
```

Roundtrip 한쪽만 실패했을 때:

```bash
bash scripts/run_v5_eval_metric.sh roundtrip_alignment v5_random 0
bash scripts/run_v5_eval_metric.sh roundtrip_alignment v5_fvt 1
```

개별 복구 후에는 반드시 reporting refresh를 실행한다.

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

## 5. 실패 유형별 판단

| Symptom | Likely cause | Action | Claim handling |
| --- | --- | --- | --- |
| wrapper exits before running | one or both v5 models or the preflight gate is not ready | rerun `status`; wait for `ready_for_wrapper=yes` and `post_checkpoint_preflight_ready_to_launch` | keep `waiting checkpoint` |
| paired transition says random running / FVT waiting | first model is still training under the paired launcher | keep watching `../2_training/mlm_progress_eta.md` and `../2_training/paired_launcher_transition.md` | no result claim; operational status only |
| one model row completes, pair model fails | transient eval/GPU failure | rerun failed metric/model with individual command, then refresh | do not compare until both rows parse |
| PPPL out of memory | mask batch or max length too high | lower `MASK_BATCH_SIZE` or `MAX_LENGTH`, record env in command log | only use row if both methods use comparable settings |
| tagging train file missing | local train-language coverage gap | use documented `TRAIN_LANGS` fallback only if already accepted | keep caveat in report/PPT |
| Roundtrip command exits | evaluator/runtime failure after materialization | keep `pending` or explicit failed-run note; do not force measured claim | limitation row |
| aggregation does not update | parser did not find completed output | inspect metric folder README/logs and rerun `scripts/aggregate_v5_metrics.py` | no promotion until aggregation row exists |

## 6. Promotion Rules

Final report/PPT values are promoted only through aggregation.

Use as final evidence:

```text
3_evaluation/09_aggregation/main_head_tail_all.tsv
3_evaluation/09_aggregation/v5_target_subset.tsv
3_evaluation/09_aggregation/metric_completion.tsv
4_reporting/current_result_snapshot.md
4_reporting/method_comparison_summary.md
```

Do not use as final evidence:

```text
live training steps
paired launcher transition verdict
storage readiness verdict
partial logs
dev F1
stdout values not parsed by aggregation
single-method metric rows when the pair is missing
```

## 7. After Recovery

After any rerun or recovery action:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Then check:

```text
post_checkpoint_eval_queue.md
09_aggregation/metric_completion.tsv
../4_reporting/finalization_gate_status.md
../4_reporting/method_comparison_summary.md
../4_reporting/final_claim_decision_tree.md
../4_reporting/result_promotion_readiness_audit.md
../4_reporting/final_claim_freeze_audit.md
../4_reporting/reporting_package_audit.md
```

The report/PPT conclusion may change only after the decision tree changes from
`decision_tree_waiting_for_results` to a result-ready or review-needed outcome.

## 8. Final Safe Fallback

If a required downstream metric remains unavailable after reasonable recovery,
do not delete it from the protocol. Keep the metric in one of these states:

- measured;
- waiting model;
- coverage-limited;
- blocked-data.

This is especially important for Roundtrip alignment. It remains a required
Glot500 metric family. In the current v5 package, available-language baseline
and reference rows are materialized and measured; the remaining gap is the
matched `v5_random`/`v5_fvt` checkpoint rows, with target10 coverage still
`0/10`. Keep that as `waiting model` or `coverage-limited`, not as a silent
omission.
