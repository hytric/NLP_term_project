# v5 심사/발표 질문 대응 Crosswalk

작성 상태: execution draft.

이 문서는 최종 report/PPT를 보거나 발표를 듣는 사람이 물을 가능성이 높은
질문을 `짧은 답변`, `열 evidence`, `잠긴 claim`, `결과 이후 업데이트`로
연결한다. 목적은 좋은 프로젝트를 더 안전하게 말하는 것이다. 새 결과를 대신
만드는 문서가 아니며, 모든 숫자 claim은 aggregation, reporting tables, 또는
명시된 audit에서만 승격한다.

## 한 줄 판정

현재 v5는 **실행 준비가 된 controlled 102-language Glot500-style replay**이다.
다만 최종 method-result claim은 matched `v5_random`/`v5_fvt` 10K checkpoint,
post-checkpoint preflight, parsed metric rows가 모두 들어온 뒤에만 열린다.

## 핵심 답변 Matrix

| 질문 | 20초 답변 | 바로 열 evidence | 잠긴 claim | 결과 이후 업데이트 |
| --- | --- | --- | --- | --- |
| 실험 goal이 실제로 실행 가능한가? | 데이터, tokenizer, initialization, metric wrapper, report/PPT handoff는 준비되어 있고, 현재 남은 것은 matched FVT checkpoint와 post-checkpoint rows이다. | `execution_readiness_review_ko.md`, `goal_readiness.md`, `final_action_dashboard_ko.md` | final report/PPT complete | `run_v5_post_checkpoint_evals.sh status`가 `READY_TO_LAUNCH=yes`가 된 뒤 paired eval 실행 |
| Glot500을 완벽하게 재연한 것인가? | full 511-language 재연이 아니라, 92 seen + 10 target의 controlled subset에서 Glot500-style workflow를 재연한 것이다. | `00_tables/table_15_glot500_reproduction_fidelity.md`, `goal_readiness.md` | full 511-language reproduction | 최종 report/PPT에서도 `controlled subset replay` 표현 유지 |
| 왜 92+10인가? | XLM-R seen Glot500 92개와 Glot500 내부 raw 중 30K 이상, XLM-R unseen, 지역/문자 다양성을 가진 target10으로 scope를 고정했다. | `../Plan.md`, `00_tables/table_01_data_scope.md`, `../0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` | corpus novelty claim | target set 변경 금지; 변경 시 merge/tokenizer/eval 모두 재실행 |
| novelty가 정확히 무엇인가? | novelty는 언어 선택이 아니라 vocabulary extension 이후 새 embedding row initialization 비교이다. | `00_tables/table_03_initialization_zero_step.md`, `method_comparison_summary.md`, `comparison_materiality_audit.md` | after-MLM/downstream superiority before v5 rows | final method claim은 materiality audit와 decision tree를 따른다 |
| Glot500 method와 Yamaguchi method 차이는? | V5 main은 auxiliary SentencePiece piece를 append하는 Glot500-style이고, V3의 add-token 계열은 Yamaguchi-style framing으로 둔다. | `../Report.md`, `03_final_report/paper_draft.md`, `03_final_report/citation_source_map.md` | V3/V5를 같은 tokenizer method로 설명 | Related Work/Method에서 terminology 유지 |
| Glot500에서 측정한 metric을 모두 했나? | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip을 모두 retained metric family로 유지했고, measured/waiting/coverage-limited를 분리했다. | `metric_fidelity_audit.md`, `metric_execution_ledger.md`, `00_tables/table_13_metric_fidelity_matrix.md` | omitted metric family | v5 rows가 parsed되면 metric completion과 tables 갱신 |
| target10 downstream 0/10이면 downstream을 못 한 것 아닌가? | target10 raw-text PPPL은 10/10 가능하지만 retained downstream local task coverage는 현재 0/10이다. 그래서 downstream은 available-language Glot500 metric replay로 보고한다. | `00_tables/table_04_evaluation_coverage.md`, `metric_fidelity_audit.md`, `02_slides/defense_qa_ko.md` | target10 downstream improvement | target task data를 새로 materialize하지 않는 한 limitation 유지 |
| dzo_Tibt tokenizer regression은 치명적인가? | 좋은 failure case로 공개한다. tokenizer는 전체적으로 좋아졌지만 `dzo_Tibt`는 regression이 남아 있어 clean win이 아니라 documented-risk pass로 쓴다. | `00_tables/table_02_tokenizer_audit.md`, `03_final_report/claim_ledger.md`, `02_slides/defense_qa_ko.md` | every target improved | limitation/analysis에 계속 노출 |
| FVT zero-step이 좋으면 final conclusion인가? | 아니다. zero-step은 initialization novelty evidence이고, final method result는 after-MLM PPPL/downstream rows가 필요하다. | `method_comparison_summary.md`, `final_claim_decision_tree.md`, `final_goal_acceptance_rubric_ko.md` | FVT improves after-MLM/downstream | post-checkpoint rows 이후 decision tree로 결론 선택 |
| Glot500-base는 baseline인가? | `cis-lmu/glot500-base`는 external reference이며 equal-budget baseline이 아니다. Equal-budget 비교는 `v5_random` vs `v5_fvt`이다. | `03_final_report/claim_ledger.md`, `00_tables/table_15_glot500_reproduction_fidelity.md` | Glot500-base equal-budget baseline | report/PPT 표 caption에서 external reference 유지 |
| 지금 왜 평가를 바로 돌리지 않나? | paired comparison을 위해 `v5_random`과 `v5_fvt` 둘 다 wrapper-ready여야 하며, preflight가 ready-to-launch여야 한다. | `../3_evaluation/post_checkpoint_preflight.md`, `../3_evaluation/post_checkpoint_eval_queue.md`, `../2_training/mlm_progress_eta.md` | single-model final comparison | `READY_TO_LAUNCH=yes` 이후 long eval 실행 |
| 결과가 일부만 들어오면 어떻게 결론을 쓰나? | positive/negative 결론을 고르지 않고 `Incomplete Evaluation / Execution Draft` block을 사용한다. | `03_final_report/result_interpretation_blocks.md`, `final_evidence_packet_audit.md`, `final_claim_decision_tree.md` | partial row as final method claim | Final Evidence Packet이 닫히기 전에는 `measured but not promotable`로 유지 |
| 최종 report/PPT는 언제 complete인가? | matched checkpoints, parsed PPPL/downstream rows 또는 명시 blocker, materiality band, decision tree, report/PPT sync, release audit가 모두 닫힐 때이다. | `final_goal_acceptance_rubric_ko.md`, `objective_completion_audit.md`, `final_deliverable_audit.md` | current execution draft as final complete | `refresh_v5_reporting.py --with-plots` 이후 final freeze audit 확인 |

## 발표 중 안전한 표현

```text
우리는 Glot500 전체 511개 언어를 재학습한 것이 아니라, XLM-R seen 92개와
Glot500 내부 target 10개로 controlled subset을 만들고 Glot500-style tokenizer
expansion, continued MLM, metric-family replay를 재연했습니다.
Novelty는 corpus가 아니라 vocabulary extension 이후 새 embedding row를 어떻게
초기화할 것인가에 있습니다. 현재 zero-step evidence는 확보했고, after-MLM 및
downstream method claim은 matched checkpoint와 parsed metric row 이후에만
승격합니다.
```

## 절대 피할 표현

- `full Glot500 reproduction`
- `target10 downstream improves`
- `FVT improves downstream performance` before parsed v5 rows
- `Glot500-base baseline` without `external reference`
- live training progress as a model-quality result
- single `v5_random` or `v5_fvt` row as a paired comparison

## 결과가 도착한 뒤 이 문서를 업데이트하는 규칙

1. `bash scripts/run_v5_post_checkpoint_evals.sh status`에서
   `READY_TO_LAUNCH=yes`를 확인한다.
2. `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`
   실행 후 `python3 scripts/refresh_v5_reporting.py --with-plots`를 실행한다.
3. `method_comparison_summary.md`, `comparison_materiality_audit.md`,
   `final_claim_decision_tree.md`를 확인한다.
4. Final Evidence Packet이 닫히지 않았으면
   `03_final_report/result_interpretation_blocks.md`의
   `Incomplete Evaluation / Execution Draft` block을 유지한다.
5. 위 matrix에서 `잠긴 claim`이 실제로 열렸는지 파일 단위로 고친다.
6. `final_claim_freeze_audit.md`, `surface_overclaim_audit.md`,
   `final_submission_smoke_audit.md`, `release_bundle_audit.md`를 다시 확인한다.
