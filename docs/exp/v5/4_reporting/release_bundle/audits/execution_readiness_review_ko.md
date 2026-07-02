# v5 Execution Readiness Review Korean

Last checked: 2026-06-28 18:08 KST

Verdict: `execution_readiness_needs_repair`

이 문서는 실제 goal 실행 준비 상태를 보고서/PPT 작성 관점에서
짧게 판정한다. 최종 결과 완료 여부가 아니라, 현재 다음 단계로
넘어갈 수 있는 선이 명확한지를 점검한다.

## 한 줄 판정

실험 설계, novelty, metric-family fidelity, report/PPT 조립선은 준비되어 있다.
다만 최종 method claim은 matched `v5_random`/`v5_fvt` checkpoint와
post-checkpoint PPPL/downstream 결과가 aggregation에 들어간 뒤에만 열린다.

## 지금 실행 가능 여부

- 가능: `refresh_v5_reporting.py`, `run_v5_post_checkpoint_evals.sh status`,
  `watch_v5_mlm_handoff.sh`로 상태를 갱신하고 감시한다.
- 금지: `READY_TO_LAUNCH=yes` 전에는 긴 post-checkpoint evaluation,
  final report/PPT freeze, after-MLM/downstream superiority claim을 실행하지 않는다.
- GO 신호: `v5_random`과 `v5_fvt`가 모두 `ready_for_wrapper=yes`이고
  `post_checkpoint_preflight_ready_to_launch`가 확인되는 순간이다.

## 준비도 Matrix

| 영역 | 상태 | 근거 | 다음 라인 |
| --- | --- | --- | --- |
| 실험 범위 | ready | merge=PASS; seen=92; target=10; lines=92452251; missing_dirs=0 | 102-language controlled scope를 유지한다. |
| Glot500-style tokenizer | ready_with_caveat | target_len=368687; appended=118685; fertility_improved=29/30; dzo_Tibt_regression=visible | 보고서/PPT에는 `dzo_Tibt` regression을 limitation으로 유지한다. |
| novelty 배치 | ready | fvt_rows=118427; mask_diff=0.0; lm_head_tied=True; zero_step_target_delta=-9.626238 | novelty는 appended-row initialization으로 고정하고, after-MLM 주장은 checkpoint 이후에만 연다. |
| 학습 parity | needs_review | training_parity=training_parity_ready | `v5_random`과 `v5_fvt`가 initialization만 다르다는 비교선을 유지한다. |
| 현재 MLM 실행 | running_waiting_checkpoint | mlm_progress=mlm_progress_ready_for_post_checkpoint_status; loss_snapshot=training_loss_snapshot_ready; live_health=live_training_health_ready_for_post_checkpoint_status; storage=storage_readiness_ready_current; paired_transition=paired_launcher_transition_matched_ready | `mlm_progress_eta.md`를 보며 기다리고, wrapper-ready 및 preflight ready-to-launch 전에는 post-checkpoint 평가를 실행하지 않는다. |
| 실제 long-eval launch gate | go_ready_to_launch | v5_random_wrapper=yes; v5_fvt_wrapper=yes; post_checkpoint_preflight=post_checkpoint_preflight_ready_to_launch; live_progress_source=2_training/mlm_progress_eta.md; launch_status_source=bash scripts/run_v5_post_checkpoint_evals.sh status | one-shot launcher로 remaining v5 rows, refresh, final evidence packet audit를 이어서 실행한다. |
| Glot500 metric fidelity | needs_review | metric_fidelity=metric_fidelity_needs_repair; metrics=pseudoperplexity=partial; retrieval_tatoeba=measured; retrieval_bible=measured; text_classification=measured; ner=partial; pos=partial; roundtrip_alignment=partial | 모든 Glot500 metric family를 유지하고, v5 rows는 checkpoint 이후 aggregation에서만 승격한다. |
| 최종 결과 gate | pending_results | matched=ready; pppl=pending; downstream=pending; execution_plan=post_checkpoint_execution_plan_ready_to_launch | 두 checkpoint가 wrapper-ready이고 post-checkpoint preflight가 ready-to-launch가 된 뒤 현재 measured row를 보존하려면 `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`을 실행한다. |
| 보고서/PPT 조립 | needs_review | section_slide_sync=section_slide_sync_ready; claim_trace=claim_evidence_trace_needs_repair; claim_freeze=claim_freeze_needs_update | 실행 draft는 사용 가능하나, 최종 결론은 decision tree가 열릴 때까지 잠근다. |

## Glot500 재연 가능성 판단

- `완전한 511-language Glot500 reproduction`이라고 쓰면 안 된다.
- 현재 허용되는 표현은 `controlled 102-language Glot500-style replay`이다.
- 이 제한된 범위 안에서는 data scope, tokenizer expansion, initialization audit,
  continued-MLM parity contract, metric-family mapping, aggregation, report/PPT
  claim locks가 모두 문서화되어 재연선이 명확하다.
- downstream은 Glot500 metric family를 유지하되, PPPL은 target10 10/10이고
  retained downstream task families는 target10 0/10이므로 available-language
  결과와 coverage limitation을 분리해서 쓴다.

## Novelty 배치 판단

- novelty는 target10 선택 자체가 아니라 `vocabulary extension 후 새 embedding row
  initialization`이다.
- FVT는 source-token decomposition을 이용해 appended row를 초기화하는 주 방법이고,
  random resize는 같은 tokenizer/corpus/schedule을 쓰는 대조군이다.
- zero-step evidence는 이미 report/PPT에 넣을 수 있지만, after-MLM 및 downstream
  개선 주장은 아직 잠겨 있다.

## 다음 실행선

현재 대기/감시 명령:

```bash
python3 scripts/refresh_v5_reporting.py
bash scripts/run_v5_post_checkpoint_evals.sh status
POLL_SECONDS=300 bash scripts/watch_v5_mlm_handoff.sh
```

감시 명령은 사용자 관리 shell 또는 tmux 같은 persistent session에서 실행한다.
transient non-interactive launcher의 background watcher 지속성은 가정하지 않는다.

`status`에서 두 v5 model 모두 `ready_for_wrapper=yes`이고
`post_checkpoint_preflight.md`가 `post_checkpoint_preflight_ready_to_launch`를
보고한 뒤에만 아래 긴 평가 명령을 실행한다.

```bash
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

canonical full rerun이 필요할 때의 기본형은
`WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`이다.

즉, status 확인과 long-run 실행은 같은 단계가 아니라 gate 전/후 단계이다.
