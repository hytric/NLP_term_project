# v5 제출/발표 파일 색인

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 최종 report/PPT 패키지에서 실제로 열어볼 파일을 빠르게 고르기 위한
한국어 색인이다. 현재 패키지는 `EXECUTION_DRAFT_NOT_FINAL`이며, matched
`v5_random`/`v5_fvt` checkpoint와 post-checkpoint evaluation row가 들어오기 전까지
after-MLM/downstream method claim은 잠겨 있다.

## 바로 제출/공유할 파일

| 목적 | 파일 | 현재 용도 |
| --- | --- | --- |
| 한국어 논문형 보고서 PDF | `03_final_report/paper_draft_ko.pdf` | 보고서 공유용 execution draft |
| 영어 논문형 보고서 PDF | `03_final_report/paper_draft.pdf` | 영어 report 검토용 execution draft |
| PPTX 발표 자료 | `02_slides/v5_final_deck_ko.pptx` | 실제 PowerPoint 발표용 deck |
| 발표 PDF | `02_slides/v5_final_deck_ko.pdf` | 리뷰/공유용 deck export |
| 브라우저 발표 자료 | `02_slides/v5_final_deck_ko.html` | 브라우저 리허설/발표용 |
| 발표 대본 | `02_slides/presenter_script_ko.md` | 슬라이드별 한국어 발화문 |
| 리허설 플랜 | `02_slides/rehearsal_plan_ko.md` | 5/8/12/15분 발표 운영과 checkpoint 상태별 closing line |
| Q&A 카드 | `02_slides/defense_qa_ko.md` | 발표 질문 방어용 |
| 심사 질문 crosswalk | `reviewer_response_crosswalk_ko.md` | 질문별 답변, evidence, claim lock 연결 |
| 결과 지연 대응 | `result_delay_contingency_ko.md` | 결과가 늦을 때 execution draft로 공유 가능한 범위와 금지 claim |
| 최종 freeze evidence | `final_freeze_evidence_checklist_ko.md` | final이라고 부르기 전 증거 파일 최종 확인 |
| 참고문헌/근거 경계 | `03_final_report/references.bib` | 보고서 인용 bib source |
| 인용 source map | `03_final_report/citation_source_map.md` | 보고서 claim별 외부/내부 source 위치 확인 |
| 외부 source 검증 | `03_final_report/external_source_verification.md` | ACL Anthology 등 외부 reference 재확인 기록 |
| 슬라이드 인용 map | `02_slides/slide_citation_map.md` | 발표 deck의 slide별 source 연결 |
| 발표 직전 체크리스트 | `presentation_readiness_checklist_ko.md` | 발표 5분 전 claim lock과 열 파일 순서 확인 |
| 한 페이지 요약 | `one_page_summary_ko.md` | 발표 직전 60초 체크와 핵심 주장 요약 |

## 먼저 열 파일 순서

1. `presentation_readiness_checklist_ko.md`
2. `one_page_summary_ko.md`
3. `02_slides/rehearsal_plan_ko.md`
4. `reviewer_response_crosswalk_ko.md`
5. `result_delay_contingency_ko.md`
6. `final_freeze_evidence_checklist_ko.md`
7. `final_action_dashboard_ko.md`
8. `post_checkpoint_trigger_card_ko.md`
9. `final_handoff_runbook.md`
10. `final_claim_decision_tree.md`
11. `final_package_checklist.md`
12. `00_tables/source_map.md`
13. `03_final_report/citation_source_map.md`
14. `03_final_report/external_source_verification.md`
15. `03_final_report/references.bib`
16. `02_slides/slide_citation_map.md`
17. `02_slides/v5_final_deck_ko.pptx`
18. `03_final_report/paper_draft_ko.pdf`

이 순서는 발표 직전에 gate를 먼저 확인하고, 그 다음 실제 deck/report를 여는
흐름이다.

## 결과가 들어온 뒤 먼저 고칠 파일

| 새 evidence | 먼저 고칠 파일 | 그 다음 |
| --- | --- | --- |
| selected checkpoints | `../2_training/05_checkpoint_selection/selected_checkpoint_manifest.md` | slide 10, reproducibility appendix |
| post-checkpoint Go/No-Go | `post_checkpoint_trigger_card_ko.md` | long paired eval 실행 전 확인 |
| after-MLM PPPL | `00_tables/table_06_pppl_partial.md` | report result/analysis, slide 11 status, slide 12 result values, slide 14 conclusion |
| downstream rows | metric별 `00_tables/table_*.md` | slide 11 status, slide 12 result values, downstream result paragraph |
| final conclusion outcome | `final_claim_decision_tree.md` | `result_interpretation_blocks.md`, slide 14, conclusion |
| final package rebuild | `release_manifest.md`, `release_bundle/README.md` | final audit 확인 |

## 말하면 안 되는 것

- full 511-language Glot500 reproduction.
- FVT after-MLM/downstream improvement before parsed v5 rows.
- target10 downstream improvement before partial official target task membership is materialized/evaluated.
- Glot500-base as an equal-budget baseline.
- live training progress as a result.

## 현재 안전한 닫는 문장

```text
현재까지는 92+10 controlled subset에서 Glot500-style workflow와 metric-family
accounting을 재연했고, vocabulary extension 이후 FVT initialization이 zero-step
target MLM proxy에서 random resize보다 좋은 시작점을 만든다는 evidence를 확보했다.
최종 after-MLM/downstream method claim은 matched checkpoint와 parsed metric row 이후에만
열겠다.
```

## Release Bundle 안의 위치

이 파일은 bundle을 만들면 아래 위치에 복사된다.

```text
release_bundle/handoff/submission_file_index_ko.md
```

같은 bundle 안에서 최종 패키지 체크와 evidence map은 아래 파일로 바로 이어진다.

```text
release_bundle/handoff/final_package_checklist.md
release_bundle/handoff/reviewer_response_crosswalk_ko.md
release_bundle/handoff/result_delay_contingency_ko.md
release_bundle/handoff/final_freeze_evidence_checklist_ko.md
release_bundle/handoff/source_map.md
release_bundle/reports/references.bib
release_bundle/reports/citation_source_map.md
release_bundle/reports/external_source_verification.md
release_bundle/slides/slide_citation_map.md
release_bundle/tables/table_13_metric_fidelity_matrix.md
release_bundle/tables/table_15_glot500_reproduction_fidelity.md
```
