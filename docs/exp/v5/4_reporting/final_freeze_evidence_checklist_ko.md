# v5 최종 Freeze Evidence Checklist

작성 상태: execution draft.

이 문서는 final report/PPT를 실제로 `freeze`라고 부르기 직전에 보는 한 장짜리
증거 체크리스트이다. 자세한 규칙은 `final_freeze_protocol_ko.md`에 있고, 이
문서는 빠른 최종 확인용이다.

## 현재 판정

현재는 final freeze가 아니다. `v5_fvt` matched checkpoint와 parsed
post-checkpoint v5 rows가 아직 필요하다. 지금 가능한 공유 상태는
`execution-draft ready`이다.

## Freeze Evidence Matrix

| Evidence | Final-ready 조건 | 현재 대기 중이면 유지할 표현 |
| --- | --- | --- |
| `selected_checkpoint_manifest.md` | `v5_random`과 `v5_fvt` selected 10K checkpoint, model file, trainer state, global step이 모두 기록됨 | matched checkpoint pending |
| `post_checkpoint_preflight.md` | `post_checkpoint_preflight_ready_to_launch` 이후 평가가 실행됨 | long eval locked |
| `post_checkpoint_provenance_audit.md` | v5 rows마다 source file, `run_meta.tsv`, command log가 남음 | provenance waiting models |
| `3_evaluation/09_aggregation/main_head_tail_all.tsv` | PPPL과 available downstream의 `v5_random`/`v5_fvt` paired rows가 parsed됨 | v5-random diagnostic rows ready; v5-FVT rows waiting checkpoint |
| `3_evaluation/09_aggregation/v5_target_subset.tsv` | target10 PPPL paired rows가 parsed됨 | target10 intrinsic after-MLM pending |
| `method_comparison_summary.md` | zero-step, after-MLM PPPL, available downstream 비교가 paired evidence로 정리됨 | zero-step ready, after-MLM pending |
| `comparison_materiality_audit.md` | final comparison row마다 `tie_band`/`small`/`moderate`/`large` band가 있음 | materiality waiting results |
| `final_claim_decision_tree.md` | waiting이 아닌 final outcome 하나를 선택함 | decision tree waiting for results |
| `post_checkpoint_outcome_matrix_ko.md` | 선택된 outcome의 한국어 report/PPT 결론 문장이 정해짐 | outcome pending |
| `final_claim_freeze_audit.md` | final-candidate 또는 명시적으로 accepted-blocked wording을 보고함 | claim freeze waiting for results |
| `table_sync_audit.md` | aggregation 숫자가 reporting tables/report/PPT source에 동기화됨 | current baseline/reference and v5-random rows ready; paired FVT rows pending |
| `surface_overclaim_audit.md` | report/PPT rendered surfaces에서 unguarded high-risk claim이 0임 | guard ready, final result pending |
| `rendered_artifact_freshness_audit.md` | report PDF, Korean report PDF, PPTX, deck PDF/HTML이 최신 source보다 낡지 않음 | execution draft freshness ready |
| `release_bundle_audit.md` | final handoff bundle이 readable이고 status가 final-candidate 또는 caveat를 명시함 | execution draft bundle ready |
| `final_submission_smoke_audit.md` | launch gate, rendered freshness, overclaim, release bundle, deliverable state가 서로 일치함 | final smoke execution draft ready |

## Freeze 전 5분 명령

final candidate를 만들기 직전 아래 순서로만 확인한다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
# Continue only when the status output says READY_TO_LAUNCH=yes.
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
grep -n "Verdict:" \
  docs/exp/v5/4_reporting/final_claim_decision_tree.md \
  docs/exp/v5/4_reporting/final_claim_freeze_audit.md \
  docs/exp/v5/4_reporting/final_deliverable_audit.md \
  docs/exp/v5/4_reporting/final_submission_smoke_audit.md \
docs/exp/v5/4_reporting/release_bundle_audit.md
```

`READY_TO_LAUNCH=no`이면 두 번째 명령으로 넘어가지 않고
`NEXT_COMMAND`에 표시된 watcher/status 명령으로 돌아간다.

## Freeze 금지 문장

아래 문장이 report/PPT의 positive claim으로 남아 있으면 freeze하지 않는다.

- `full 511-language Glot500 reproduction`
- `target10 downstream improves`
- `Glot500-base equal-budget baseline`
- `FVT improves downstream performance` without parsed v5 downstream rows
- `FVT improves after-MLM PPPL` without paired PPPL rows and materiality band

## Freeze 가능 문장

모든 final-ready 조건이 닫힌 뒤에만 아래 형태로 쓴다.

```text
The final report/PPT package is frozen from parsed aggregation rows,
explicit pending/blocker accounting, clean claim gates, synchronized tables,
and source-checked report/PPT prose.
```

현재는 아래 문장을 사용한다.

```text
The report/PPT package is execution-draft ready and waits for matched
v5_random/v5_fvt checkpoints plus parsed post-checkpoint metrics.
```
