# v5 Post-Checkpoint Trigger Card

작성 상태: 실행 handoff 카드. 숫자 결과표가 아니라, `v5_fvt` 10K 완료 직후
어떤 순서로 평가와 report/PPT 갱신을 시작할지 고정하는 문서이다.

## 1. 먼저 열 파일

```text
docs/exp/v5/4_reporting/final_action_dashboard_ko.md
docs/exp/v5/3_evaluation/post_checkpoint_execution_plan.md
docs/exp/v5/4_reporting/final_result_update_checklist_ko.md
```

## 2. 절대 Go/No-Go

긴 평가를 시작하기 전에 반드시 아래 명령을 먼저 실행한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
```

Go 조건:

- `v5_random` `ready_for_wrapper=yes`
- `v5_fvt` `ready_for_wrapper=yes`
- `post_checkpoint_preflight_ready_to_launch`
- `post_checkpoint_command_consistency_ready`
- parser contract가 waiting-model 이외의 command/path 문제를 보고하지 않음

No-Go 조건:

- `v5_fvt`가 `dir_exists_no_model_file`, `waiting_model`, 또는
  `ready_for_wrapper=no`
- queue에서 실행할 metric command가 `none`
- selected checkpoint manifest에 model file, trainer state, global step 중
  하나라도 비어 있음

No-Go일 때는 평가를 시작하지 않고 아래 watcher만 둔다.

```bash
POLL_SECONDS=300 RUN_ALL=0 bash scripts/watch_v5_mlm_handoff.sh
```

Watcher 자체를 먼저 점검하려면 아래 smoke test를 한 번만 실행한다. `v5_fvt`가
아직 준비되지 않은 상태에서는 exit code `2`가 정상이며, 이 명령은 긴 평가를
실행하지 않는다.

```bash
MAX_POLLS=1 POLL_SECONDS=1 RUN_ALL=0 bash scripts/watch_v5_mlm_handoff.sh
```

긴 평가 wrapper 자체의 No-Go 동작을 점검하려면 아래 smoke test를 사용한다.
`v5_fvt`가 아직 준비되지 않은 상태에서는 exit code `1`과
`Matched v5 checkpoints are not ready yet.` 메시지가 정상이며, PPPL 계산은
시작되지 않는다.

```bash
WITH_PLOTS=0 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
```

## 3. Ready가 되면 실행

권장 one-shot 경로는 아래 명령이다. 이 실행기는 내부에서 status를 다시 확인하고,
`READY_TO_LAUNCH=yes`가 아니면 평가를 거부한다. Ready이면 paired evaluation,
reporting refresh, Final Evidence Packet audit까지 이어서 수행한다.
`READY_TO_LAUNCH=no`이면 평가를 시작하지 말고 status output의 `NEXT_COMMAND`로
돌아간다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_ready_to_final_package.sh
```

현재 큐처럼 일부 metric/model 행이 이미 `measured`로 집계된 상태라면,
한 번에 전체 paired pass를 재개하되 중복 실행을 건너뛴다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

GPU `0` 또는 `1`이 바쁘면 `nvidia-smi`로 빈 물리 GPU id를 확인하고
`GPU_RANDOM`, `GPU_FVT`만 바꾼다.

의도적으로 모든 post-checkpoint row를 재측정할 때만 아래 canonical full rerun을
사용한다.

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

길게 나눠야 할 때만 아래 순서를 쓴다.

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
python3 scripts/refresh_v5_reporting.py --with-plots
```

## 4. 결과 도착 직후 확인

결과 숫자는 stdout이나 live log에서 복사하지 않는다. 반드시 refresh 후 아래
파일을 본다.

```text
docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv
docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv
docs/exp/v5/3_evaluation/09_aggregation/v5_target_subset.tsv
docs/exp/v5/4_reporting/method_comparison_summary.md
docs/exp/v5/4_reporting/claim_promotion_matrix.md
docs/exp/v5/4_reporting/final_claim_decision_tree.md
```

## 5. Claim Unlock Line

| Evidence | Unlocks | Still locked |
| --- | --- | --- |
| both selected checkpoints ready | paired evaluation may start | method improvement claim |
| parsed `v5_random`/`v5_fvt` PPPL rows | after-MLM intrinsic FVT-vs-random claim may unlock | downstream improvement |
| parsed available downstream rows | available-language downstream comparison may unlock | target10 downstream improvement if coverage is still `0/10` |
| final decision tree selects an outcome | slide 14/report conclusion wording | full 511-language reproduction claim |

## 6. Report/PPT Patch Order

1. `python3 scripts/refresh_v5_reporting.py --with-plots`
2. Check `method_comparison_summary.md`, `claim_promotion_matrix.md`, and
   `final_claim_decision_tree.md`.
3. Update report text from `03_final_report/result_interpretation_blocks.md`
   only.
4. Update PPT in this order: slide 11 status/coverage, slide 12 result values,
   slide 14 conclusion.
5. Run `python3 scripts/refresh_v5_reporting.py --with-plots` again.
6. Check `reporting_package_audit.md`, `final_claim_freeze_audit.md`,
   `final_deliverable_audit.md`, and `release_bundle_audit.md`.

## 7. One-Line Rule

```text
Checkpoint readiness unlocks evaluation; parsed aggregation rows unlock claims.
```
