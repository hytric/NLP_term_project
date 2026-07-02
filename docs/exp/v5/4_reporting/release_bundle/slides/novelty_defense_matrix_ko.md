# v5 Novelty/Reproduction Defense Matrix

작성 상태: execution draft, 2026-06-28 기준.

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
defense matrix header.

이 파일은 발표 Q&A에서 가장 공격받기 쉬운 세 축, 즉 `Glot500 재연성`,
`novelty`, `downstream coverage`를 빠르게 방어하기 위한 한국어 매트릭스이다.
숫자와 claim은 항상 `claim_promotion_matrix.md`, `final_claim_decision_tree.md`,
`metric_fidelity_audit.md`, `3_evaluation/09_aggregation/`을 따른다.

## 1. 핵심 방어선

| 공격 질문 | 짧은 답변 | Evidence | 반드시 붙일 caveat | 금지 표현 |
| --- | --- | --- | --- | --- |
| 이게 Glot500 재현인가? | full 재현이 아니라 controlled 102-language Glot500-style replay이다. | `table_15_glot500_reproduction_fidelity.md`, `goal_readiness.md` | 511-language scale과 compute budget은 adapted | full Glot500 reproduction |
| 왜 92+10인가? | XLM-R seen 92개와 Glot500-internal target10으로 통제된 subset을 만든 것이다. | `glot50010_selected_manifest.tsv`, merge report | target10은 external corpus novelty가 아님 | arbitrary external data |
| novelty가 corpus 선택뿐 아닌가? | novelty는 appended vocabulary row initialization이다. | `table_03_initialization_zero_step.md`, init reports | target10 selection은 실험 scope, novelty는 init method | new corpus contribution |
| FVT가 정확히 뭔가? | 새 token surface를 source tokenizer로 분해하고 source subtoken embedding 평균으로 초기화한다. | FVT init report, zero-step summary | lexical fallback 2개와 byte row accounting을 같이 말함 | magic semantic initialization |
| Yamaguchi-style은 어떤 논문인가? | Yamaguchi, Villavicencio, Aletras의 CL 2026 low-resource vocabulary expansion 논문이다. | `citation_source_map.md`, `external_source_verification.md` | v5는 inspiration으로 인용하고 tokenizer는 Glot500-style append임 | v5 tokenizer is Yamaguchi method |
| zero-step만으로 충분한가? | zero-step은 intrinsic early evidence이고, final method claim은 after-MLM 이후에만 열린다. | `method_comparison_summary.md`, `claim_promotion_matrix.md` | PPPL/downstream은 checkpoint 이후 | final improvement proven |
| tokenizer가 다 좋아졌나? | 구조 audit은 통과했고 29/30이 개선됐지만 `dzo_Tibt`는 악화됐다. | `table_02_tokenizer_audit.md` | `dzo_Tibt` regression을 limitation으로 유지 | improves every language |
| downstream도 target10에서 좋아졌나? | 아직 말하지 않는다. PPPL은 target10 10/10이지만 retained downstream task families는 target10 0/10이다. | coverage summary, `table_04_evaluation_coverage.md` | target10은 PPPL 중심으로 해석 | target10 downstream improves |
| Glot500 metric을 빼먹은 것 아닌가? | metric family는 모두 retained이고 measured/waiting/coverage-limited를 분리했다. | `metric_fidelity_audit.md`, `table_13_metric_fidelity_matrix.md` | performance claim은 measured row에만 | all metrics fully measured |
| Glot500-base와 비교하면 공정한가? | Glot500-base는 external reference이고 equal-budget baseline이 아니다. | `claim_ledger.md` | method comparison은 `v5_random` vs `v5_fvt` | equal-budget baseline |
| v5-random 결과가 섞이면 novelty가 약한가? | 아니다. v5-random은 diagnostic lower-bound이고 최종 검정은 matched v5-FVT row이다. | `main_head_tail_all.tsv`, `result_promotion_readiness_audit.md` | v5-random은 method win이 아니라 sanity row | v5 already wins |
| FVT가 최종적으로 지면 실패인가? | 실패가 아니라 early initialization advantage가 training에서 희석된 결과로 해석한다. | `result_interpretation_blocks.md` | final claim은 decision tree outcome에 맞춤 | method disproven |

## 2. 발표 중 즉시 쓸 문장

### Reproduction Boundary

```text
이 실험은 Glot500 전체 511개 언어를 다시 학습한 것이 아닙니다. 대신 Glot500의
핵심 절차인 corpus merge, SentencePiece append, continued MLM, metric-family replay를
92+10 controlled subset에서 재연한 것입니다.
```

### Novelty Boundary

```text
새 언어를 고른 것 자체가 novelty는 아닙니다. novelty는 vocabulary extension 이후
새로 생긴 embedding row를 random으로 둘지, source tokenizer decomposition을 이용해
더 정보 있는 시작점으로 둘지 비교하는 데 있습니다.
```

### Downstream Boundary

```text
target10은 raw-text PPPL에는 들어가지만 현재 local downstream task coverage는 대부분
0/10입니다. 그래서 target10 claim은 tokenization, zero-step, after-MLM PPPL로 제한하고,
downstream은 available-language/head/all replay로 보고합니다.
```

### Negative-Result Boundary

```text
만약 FVT가 after-MLM에서 random보다 좋지 않다면, 결론은 초기화가 전혀 의미 없다는
것이 아니라 10K MLM update 이후 초기화 차이가 줄어들 수 있다는 것입니다. 이 경우에도
zero-step result는 early adaptation evidence로 남습니다.
```

### v5-Random Diagnostic Boundary

```text
v5-random은 최종 method claim이 아니라 diagnostic lower-bound입니다. 일부
available-language metric에서는 XLM-R보다 낫고 일부에서는 약하므로, 결론은 v5가 이미
이겼다는 것이 아니라 matched FVT checkpoint가 결정적 검정이라는 것입니다.
```

## 3. Novelty Claim Strength Ladder

novelty 질문을 받을 때는 아래 단계 중 현재 gate가 닫힌 단계까지만 말한다.
강한 claim을 빨리 말하는 것보다, 어느 evidence layer까지 열렸는지 분리하는 것이
이 실험의 장점이다.

| Level | 현재 상태 | 허용 claim | 필요한 evidence | 금지되는 확장 |
| --- | --- | --- | --- | --- |
| 0. setup novelty | ready | Glot500-style replay 위에 embedding-row initialization 질문을 분리했다 | target10 manifest, tokenizer append audit, init audit | corpus 선택 자체를 novelty라고 말하기 |
| 1. zero-step intrinsic novelty | ready | FVT가 random resize보다 zero-step target MLM proxy에서 훨씬 좋은 시작점이다 | `method_comparison_summary.md`, `table_03_initialization_zero_step.md` | after-MLM 또는 downstream superiority로 확장 |
| 2. after-MLM intrinsic novelty | locked | matched continued MLM 이후에도 PPPL에서 FVT가 유리한지 검정한다 | paired `v5_random`/`v5_fvt` PPPL rows, materiality audit | single-model row나 live log로 method win 주장 |
| 3. available downstream transfer | locked | available-language downstream metric family에서 FVT 효과가 유지되는지 본다 | paired downstream rows, majority/tie rule, decision tree | target10 downstream improvement로 일반화 |
| 4. target10 downstream transfer | locked/disallowed now | target10 downstream coverage가 생긴 경우에만 별도 보조 claim 가능 | target10 task coverage and measured rows | 현재 0/10 coverage에서 개선/악화 주장 |

즉 현재 발표의 novelty 결론은 `Level 1`까지가 확정이고, `Level 2-3`은
matched checkpoint와 aggregation 이후에만 열린다. `Level 4`는 새 downstream
coverage가 생기지 않는 한 열지 않는다.

## 4. Q&A에서 열 파일

| 상황 | 먼저 열 파일 | 보조 파일 |
| --- | --- | --- |
| 재연성 질문 | `00_tables/table_15_glot500_reproduction_fidelity.md` | `goal_readiness.md` |
| novelty 질문 | `00_tables/table_03_initialization_zero_step.md` | `method_comparison_summary.md` |
| claim 가능성 질문 | `claim_promotion_matrix.md` | `final_claim_freeze_audit.md` |
| downstream coverage 질문 | `00_tables/table_04_evaluation_coverage.md` | `3_evaluation/00_coverage/coverage_summary.tsv` |
| Roundtrip/Bible 질문 | `metric_fidelity_audit.md` | `00_tables/table_12_bible_partial.md`, `00_tables/table_14_roundtrip_partial.md` |
| 최종 결론 질문 | `final_claim_decision_tree.md` | `post_checkpoint_outcome_matrix_ko.md`, `03_final_report/result_interpretation_blocks.md` |

## 5. Final Claim Upgrade Rule

최종 발표의 conclusion은 아래 순서가 끝난 뒤에만 바꾼다.

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

그 뒤 `final_claim_decision_tree.md`가 선택한 outcome만 사용한다.
live training progress, partial stdout, 단일 모델 row는 final claim으로 쓰지 않는다.
