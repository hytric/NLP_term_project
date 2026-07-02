# v5 최종 Report/PPT Freeze Protocol

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 최종 보고서와 발표 자료를 언제 "freeze"라고 부를 수 있는지 정의한다.
현재 상태에서는 freeze 금지이다. matched `v5_random`/`v5_fvt` checkpoint와
post-checkpoint v5 metric rows가 아직 없기 때문이다.
발표 직전의 claim lock은 `presentation_readiness_checklist_ko.md`를 먼저 보고,
최종 freeze 여부는 이 문서와 `final_claim_freeze_audit.md`를 함께 확인한다.

## 1. Freeze 금지 조건

아래 조건 중 하나라도 참이면 최종 freeze를 하지 않는다.

| 금지 조건 | 확인 파일 | 조치 |
| --- | --- | --- |
| matched MLM checkpoint가 없다 | `finalization_gate_status.md` | 기다린 뒤 `bash scripts/run_v5_post_checkpoint_evals.sh status` |
| post-checkpoint preflight가 ready-to-launch가 아니다 | `../3_evaluation/post_checkpoint_preflight.md` | preflight verdict가 `post_checkpoint_preflight_ready_to_launch`가 될 때까지 긴 평가 금지 |
| `v5_random` 또는 `v5_fvt` after-MLM PPPL row가 없다 | `method_comparison_summary.md` | post-checkpoint PPPL 실행 |
| available downstream v5 row가 없다 | `3_evaluation/09_aggregation/main_head_tail_all.tsv` | post-checkpoint downstream 실행 |
| FVT-vs-random 차이의 materiality band가 확인되지 않았다 | `comparison_materiality_audit.md` | `tie_band`는 no clear separation, `small`은 cautious wording으로 고정 |
| final decision tree가 waiting 상태이다 | `final_claim_decision_tree.md` | conclusion을 conditional로 유지 |
| final claim freeze audit가 waiting 상태이다 | `final_claim_freeze_audit.md` | final method/downstream claim 잠금 |
| reporting package audit가 final-ready가 아니다 | `reporting_package_audit.md` | missing/stale/live guard 수정 |
| report/PPT 표면에 unguarded overclaim이 있다 | `surface_overclaim_audit.md` | high-risk claim을 guard 문맥으로 옮기거나 삭제 |
| 최종 smoke audit가 repair를 요구한다 | `final_submission_smoke_audit.md` | share artifact, rendered surface, release bundle, launch gate 중 실패 row 수정 |

## 2. Freeze 허용 조건

최종 freeze는 아래가 모두 만족될 때만 가능하다.

| Gate | Required state |
| --- | --- |
| selected checkpoints | `v5_random` and `v5_fvt` selected 10K checkpoints exist |
| post-checkpoint command guards | command consistency, parser contract, and preflight audits are ready |
| post-checkpoint preflight | `post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch` |
| after-MLM PPPL | aggregation has both v5 rows |
| comparison materiality | `comparison_materiality_audit.md` exists and final wording follows `tie_band`/`small`/`moderate`/`large` bands |
| downstream replay | runnable available-language v5 rows are parsed or explicitly blocked |
| Roundtrip | measured or retained as explicit pending/blocked status |
| claim decision | `final_claim_decision_tree.md` selects a non-pending outcome block |
| claim freeze | `final_claim_freeze_audit.md` is final-candidate or intentionally blocked with wording |
| table sync | `table_sync_audit.md` is ready |
| narrative | `narrative_quality_audit.md` is ready |
| overclaim guard | `surface_overclaim_audit.md` is `surface_overclaim_guard_ready` and `rendered_surface_scan_summary` is ready |
| final smoke | `final_submission_smoke_audit.md` is execution-draft-ready or final-candidate |
| references | `external_source_verification.md`, `citation_source_map.md`, `slide_citation_map.md` are ready |

## 3. Freeze 직전 실행 순서

matched checkpoints와 post-checkpoint preflight가 준비된 뒤 아래 순서를 그대로 따른다.
긴 evaluation을 수동으로 시작하는 직접 신호는 status output 마지막의
`READY_TO_LAUNCH=yes`이다. `READY_TO_LAUNCH=no`이면 두 번째 명령으로
넘어가지 않고 출력된 `NEXT_COMMAND`로 돌아간다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
# Continue only when the status output says READY_TO_LAUNCH=yes.
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

그 다음 verdict를 확인한다.

```bash
grep -n "Verdict" \
  docs/exp/v5/4_reporting/finalization_gate_status.md \
  docs/exp/v5/3_evaluation/post_checkpoint_command_consistency.md \
  docs/exp/v5/3_evaluation/post_checkpoint_parser_contract.md \
  docs/exp/v5/3_evaluation/post_checkpoint_preflight.md \
  docs/exp/v5/4_reporting/method_comparison_summary.md \
  docs/exp/v5/4_reporting/comparison_materiality_audit.md \
  docs/exp/v5/4_reporting/final_claim_decision_tree.md \
  docs/exp/v5/4_reporting/final_claim_freeze_audit.md \
  docs/exp/v5/4_reporting/table_sync_audit.md \
  docs/exp/v5/4_reporting/narrative_quality_audit.md \
  docs/exp/v5/4_reporting/surface_overclaim_audit.md \
  docs/exp/v5/4_reporting/reporting_package_audit.md \
  docs/exp/v5/4_reporting/final_submission_smoke_audit.md \
  docs/exp/v5/4_reporting/final_deliverable_audit.md
```

발표/제출 직전에는 위 verdict 확인 전에 아래 파일을 먼저 연다.

```text
docs/exp/v5/4_reporting/presentation_readiness_checklist_ko.md
docs/exp/v5/4_reporting/final_action_dashboard_ko.md
docs/exp/v5/4_reporting/submission_file_index_ko.md
```

## 4. Report Freeze Checklist

| Section | 확인할 것 |
| --- | --- |
| Abstract | `Final Abstract Update Choices` 중 final decision tree outcome과 같은 block을 사용했는지 |
| Related work | Glot500과 Yamaguchi-style 역할이 섞이지 않았는지 |
| Data | 92+10 controlled subset wording이 유지되는지 |
| Tokenizer | `dzo_Tibt` regression이 visible limitation으로 남아 있는지 |
| Initialization | zero-step claim과 after-MLM claim이 분리되어 있는지 |
| Results | 모든 숫자가 `00_tables/` 또는 `09_aggregation/`에서 온 것인지 |
| Result materiality | `comparison_materiality_audit.md`의 `tie_band`/`small`/`moderate`/`large` band에 맞춰 문장 강도가 제한되는지 |
| Result source hygiene | live log/stdout/single-model row가 report/PPT claim source로 쓰이지 않았는지 |
| Overclaim hygiene | `surface_overclaim_audit.md`가 `surface_overclaim_guard_ready`이고 rendered report/PPT의 `rendered_surface_scan_summary`가 `unguarded=0`인지 |
| Downstream | target10 downstream improvement를 말하지 않는지 |
| Limitations | Bible/Roundtrip v5 pending status와 coverage limit이 사라지지 않았는지 |
| Conclusion | `result_interpretation_blocks.md`의 `Korean Final Conclusion Choices`와 `post_checkpoint_outcome_matrix_ko.md`에서 decision tree outcome과 일치하는 block만 사용했는지 |

## 5. PPT Freeze Checklist

| Slide | 확인할 것 |
| --- | --- |
| 3 | full Glot500 reproduction처럼 들리지 않는지 |
| 6 | tokenizer gain과 `dzo_Tibt` caveat가 같이 보이는지 |
| 8-9 | FVT novelty가 zero-step evidence로 정확히 위치하는지 |
| 10 | Glot500 metric family가 모두 retained로 표현되는지 |
| 11-12 | v5 rows가 pending인지 measured인지 최신 상태인지 |
| 13 | target10 downstream coverage limitation이 살아 있는지 |
| 14 | final conclusion이 decision tree, `post_checkpoint_outcome_matrix_ko.md`, `comparison_materiality_audit.md`와 일치하는지 |
| Backup/Q&A | `defense_qa.md`와 `defense_qa_ko.md`가 최신 claim lock을 따르는지 |

## 6. Outcome별 최종 결론 선택

| Outcome | 사용할 문서 |
| --- | --- |
| FVT wins PPPL and most available downstream rows | `post_checkpoint_outcome_matrix_ko.md`의 bounded positive row와 `result_interpretation_blocks.md`의 `Final Abstract Update Choices`/`Korean Final Conclusion Choices` 중 `FVT Wins PPPL And Most Available Downstream Rows` |
| FVT wins PPPL but downstream is mixed | `post_checkpoint_outcome_matrix_ko.md`의 intrinsic positive, downstream mixed row와 `Final Abstract Update Choices`/`Korean Final Conclusion Choices` 중 `FVT Wins PPPL But Downstream Is Mixed` |
| FVT wins zero-step only | `post_checkpoint_outcome_matrix_ko.md`의 early-only diagnostic row와 `Final Abstract Update Choices`/`Korean Final Conclusion Choices` 중 `FVT Wins Zero-Step Only` |
| random catches or beats FVT after MLM | `post_checkpoint_outcome_matrix_ko.md`의 negative final comparison row와 `Final Abstract Update Choices`/`Korean Final Conclusion Choices` 중 `Random Catches Or Beats FVT After MLM` |
| target10 official membership is not materialized/evaluated | `post_checkpoint_outcome_matrix_ko.md`의 coverage 방어 원칙과 target10 downstream claim block |

임의로 더 강한 표현을 만들지 않는다.

## 7. 제출 직전 금지 표현 검색

freeze 직전에 아래 표현이 final report/PPT에서 positive claim으로 남아 있지 않은지
확인한다.

```bash
grep -R -n -E \
  "full Glot500 reproduction|511-language.*complete|target10 downstream improves|equal-budget baseline|FVT improves downstream" \
  docs/exp/v5/Report.md \
  docs/exp/v5/4_reporting/03_final_report \
  docs/exp/v5/4_reporting/02_slides
```

검색 결과가 나오더라도 limitation, forbidden-claim, Q&A 방어 문맥이면 허용된다.
positive claim이면 수정한다.

## 8. Freeze 판정 문장

최종 freeze가 가능할 때만 아래 문장을 사용할 수 있다.

```text
The final report/PPT package is frozen from parsed aggregation rows,
explicit pending/blocker accounting, clean claim gates, synchronized tables,
and source-checked report/PPT prose.
```

현재는 이 문장을 사용하지 않는다. 현재 문장은 다음과 같다.

```text
The report/PPT package is execution-draft ready and waits for matched
v5_random/v5_fvt checkpoints plus parsed post-checkpoint metrics.
```
