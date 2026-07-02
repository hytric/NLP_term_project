# v5 발표 방어 Q&A 한국어 카드

작성 상태: execution draft, 2026-06-28 기준.

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
Q&A header.

이 문서는 실제 발표 Q&A에서 바로 읽을 수 있는 짧은 한국어 답변 카드이다.
긴 근거와 영어 버전은 `defense_qa.md`를 사용하고, 숫자와 claim은
`final_claim_decision_tree.md`, `claim_promotion_matrix.md`,
`table_13_metric_fidelity_matrix.md`를 따른다.
질문 유형별 evidence와 금지 표현을 빠르게 확인할 때는
`novelty_defense_matrix_ko.md`를 같이 사용한다.

## 0. 압축 답변 카드

이 표는 시간이 부족한 Q&A에서 답변 길이를 조절하기 위한 카드이다. 10초 답변은
한 문장으로 먼저 말하고, 상대가 더 묻는 경우에만 30초 또는 60초 답변으로 늘린다.

| 질문 축 | 10초 답변 | 30초 답변 | 60초 답변 |
| --- | --- | --- | --- |
| Glot500 재연성 | full reproduction이 아니라 controlled 102-language Glot500-style replay이다. | 92 XLM-R-seen + target10 subset에서 corpus merge, SPM append, continued MLM, metric-family replay를 유지했다. | 511-language scale과 compute budget은 adapted이지만, tokenizer expansion, MLM objective, metric-family accounting, result-promotion guard는 retained이다. 그래서 정확한 claim은 full Glot500 reproduction이 아니라 controlled subset에서의 Glot500-style 재연이다. |
| novelty | novelty는 corpus가 아니라 appended vocabulary row initialization이다. | 같은 corpus/tokenizer/schedule에서 random resize와 source-token decomposition FVT를 비교한다. | target10 selection은 실험 scope이고, contribution은 vocabulary extension 이후 새 embedding row를 어떻게 시작할지에 있다. 현재 FVT는 zero-step target weighted NLL에서 random보다 9.626238 낮고, final method claim은 matched after-MLM/downstream rows 이후에만 연다. |
| downstream 충실성 | metric family는 모두 retained지만 target10 downstream improvement는 말하지 않는다. | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip을 모두 surface에 남겼고 measured/waiting/coverage-limited를 분리했다. | target10은 raw-text PPPL에는 10/10으로 들어가지만 retained downstream task families에서는 target10 coverage가 0/10이다. 따라서 downstream은 available-language replay로 보고하고, target10은 tokenization, zero-step, after-MLM PPPL 중심으로 해석한다. |
| claim lock | 결과 claim은 aggregation row와 decision tree가 열 때만 바꾼다. | live log, stdout, single-model row, dev score는 final claim source가 아니다. | checkpoint가 끝난 뒤 `run_v5_post_checkpoint_evals.sh status`, guarded `all`, `refresh_v5_reporting.py --with-plots` 순서로 갱신하고, `final_claim_decision_tree.md`와 `post_checkpoint_outcome_matrix_ko.md`가 같은 outcome을 가리킬 때만 slide 14와 conclusion을 바꾼다. |

## Q1. 이 실험은 Glot500을 완전히 재현한 것인가?

아니다. 정확한 표현은 `controlled 102-language Glot500-style replay`이다.
511개 언어 전체를 다시 학습한 것이 아니라, XLM-R seen 92개와 target10을 사용해
Glot500의 핵심 흐름인 corpus merge, SPM append, continued MLM, metric-family replay를
재연한 것이다.

더 엄밀하게는 `table_15_glot500_reproduction_fidelity.md` 기준으로 language scale과
compute budget은 adapted이고, tokenizer expansion, MLM objective, metric-family
accounting, result-promotion guard는 retained이다.

## Q2. 왜 92+10 구조인가?

92개는 현재 local Glot500 raw에서 확인 가능한 XLM-R seen language-script이고,
10개는 Glot500 raw 내부에서 XLM-R unseen, `new_length >= 30000`, local raw directory
존재, 지역/문자 다양성 기준으로 고른 target set이다. 즉 외부 corpus novelty가 아니라
통제된 Glot500-internal subset이다.

## Q3. novelty는 정확히 무엇인가?

novelty는 새 corpus가 아니라 vocabulary extension 이후 새 embedding row를 어떻게
초기화할지에 있다. main comparison은 Hugging Face random resize와 source-token
decomposition 기반 FVT initialization이다.

## Q4. V3/V4 tokenizer 차이는 어떻게 설명하나?

V4/V5는 Glot500-style SPM append 방식이다. V3의 add-token route는 Yamaguchi-style
vocabulary expansion ablation 또는 inspiration에 가깝다. 따라서 본 실험의 tokenizer
reproduction은 Glot500-style이고, Yamaguchi-style은 initialization novelty를 설명하는
관련 방법론 축으로 둔다.

여기서 말하는 Yamaguchi-style의 문헌 출처는 Yamaguchi, Villavicencio, Aletras의
Computational Linguistics 2026 논문 "How Can We Effectively Expand the Vocabulary
of LLMs with 0.01GB of Target Language Text?"이다. v5는 이 논문을 low-resource
vocabulary expansion 및 new-token initialization motivation으로 인용하지만, 실행된
main tokenizer는 Glot500-style SentencePiece append라고 분리해서 말한다.

## Q5. zero-step 결과만으로 final method claim이 가능한가?

아니다. zero-step은 initialization이 early behavior에 영향을 준다는 intrinsic evidence이다.
after-MLM PPPL과 downstream improvement는 matched `v5_random`/`v5_fvt` 10K checkpoint와
aggregation row가 생긴 뒤에만 claim으로 승격한다.

## Q6. 현재 안전하게 말할 수 있는 결론은 무엇인가?

현재 안전한 결론은 setup fidelity와 zero-step novelty이다. v5는 controlled 102-language
setting에서 Glot500-style workflow를 재연할 준비를 갖췄고, FVT는 target weighted NLL에서
random보다 9.626238 낮은 zero-step 결과를 보였다.

## Q7. target10 downstream improvement를 왜 말하지 않나?

target10은 raw-text PPPL에는 10/10으로 들어가지만, 현재 materialized retained
downstream task coverage는 target10 0/10이다. 따라서 target10 claim은 tokenization, zero-step, after-MLM
PPPL 중심으로 제한하고, downstream은 available-language/head/all replay로 보고한다.

## Q8. Glot500-base는 baseline인가?

Glot500-base는 external reference이다. equal-budget baseline이라고 말하면 안 된다.
본 연구의 equal-budget method comparison은 같은 corpus, tokenizer, schedule, checkpoint
rule을 공유하는 `v5_random`과 `v5_fvt`이다.

## Q9. `dzo_Tibt` tokenizer regression은 어떻게 방어하나?

숨기지 않는 것이 맞다. main tokenizer는 29/30 audited languages와 9/10 target languages에서
fertility를 개선했지만, `dzo_Tibt`는 4.223938에서 5.552124 tokens/word로 악화됐다. 이는
SPM append가 모든 script에서 항상 좋은 segmentation을 보장하지 않는다는 중요한 limitation이다.

## Q10. Glot500 metric을 모두 이행했나?

metric family는 모두 retained이다. PPPL, Tatoeba, Bible, text classification, NER, POS,
Roundtrip을 모두 evaluation surface에 남겼고, 현재 측정 가능 row와 coverage-limited row,
blocked-data row를 분리해 기록한다. 성능 claim은 measured row에만 붙인다.
현재 v5-random은 PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip row가
aggregation에 들어갔다. 다만 paired method claim은 v5-FVT row가 들어온 뒤에만 연다.

## Q11. Roundtrip은 지금 어떻게 보고하나?

Bible-derived parallel input과 v5 batch runner가 준비되어 coverage가 `74/102`까지
열렸고, XLM-R accuracy `0.185300`, Glot500-base accuracy `0.205189`가 측정됐다.
v5-random accuracy도 `0.190300`으로 측정됐다. 남은 것은 v5-FVT row이며, 이것은
matched checkpoint 이후 실행한다. target10 coverage는 여전히 `0/10`이라 target10
downstream claim에는 쓰지 않는다.

## Q12. POS에서 Turkish train caveat는 왜 중요한가?

local POS에는 `train-eng_Latn.tsv`가 없어서 `TRAIN_LANGS=tur_Latn`으로 학습한 row가 있다.
따라서 POS 결과를 읽을 때는 이 local train-language caveat를 같이 말해야 한다.

## Q13. checkpoint가 끝나면 바로 무엇을 하나?

먼저 `bash scripts/run_v5_post_checkpoint_evals.sh status`를 실행해 두 v5 model이
`ready_for_wrapper=yes`이고 `post_checkpoint_preflight.md` verdict가
`post_checkpoint_preflight_ready_to_launch`인지 확인한다. 그 다음
`SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`을 실행하고,
`python3 scripts/refresh_v5_reporting.py --with-plots`로 aggregation, tables, figures,
claim gates를 갱신한다.
실행 환경, GPU 배정, 출력/log 위치, claim 승격 규칙은
`../../3_evaluation/post_checkpoint_execution_plan.md`를 따른다.

## Q14. FVT가 after-MLM에서 random을 이기지 못하면 실패인가?

아니다. 그 경우 결론은 "FVT가 더 좋은 starting point를 만들지만, 10K MLM update가 그 차이를
줄이거나 지울 수 있다"가 된다. 즉 positive claim은 낮추되, initialization이 early adaptation에
영향을 준다는 diagnostic contribution은 남는다.

## Q15. 최종 발표에서 절대 피해야 할 표현은?

- `full Glot500 reproduction`
- `target10 downstream improvement`
- `Glot500-base equal-budget baseline`
- `FVT improves downstream` without parsed v5 rows
- live training step이나 dev score를 final result처럼 말하는 표현

## Q16. novelty가 너무 작은 것 아닌가?

작지 않다. 이 실험의 novelty는 새 model architecture가 아니라, Glot500-style
vocabulary expansion 이후 새 embedding row를 어떻게 초기화할지에 대한 controlled
method comparison이다. 특히 `v5_random`과 `v5_fvt`가 같은 corpus, tokenizer, schedule,
checkpoint rule을 공유하도록 고정했기 때문에, 차이가 나면 initialization policy의 효과로
해석할 수 있다.

현재는 zero-step target weighted NLL에서 FVT가 random보다 9.626238 낮다는 intrinsic
evidence가 있고, final method claim은 after-MLM PPPL과 downstream row가 들어온 뒤에만
연다. 즉 novelty를 크게 포장하지 않고, 검증 가능한 좁은 질문으로 만든 것이 장점이다.

## Q17. target10 downstream coverage를 어떻게 해석해야 하는가?

충실히 이행한 것이다. 단, claim scope가 다르다. Glot500 metric family를 빼지 않고
PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip을 모두 retained surface로 유지했다.
정정된 기준으로는 v5 target10 중 `8/10`이 공식 Glot500 task list에 일부 membership을
가진다. 다만 기존 local materialization/coverage 파일이 task-list `0/1` flag를
availability로 오해해 tail task를 undercount했으므로, target10 downstream improvement는
repair 전까지 말하지 않는다.

대신 downstream은 available-language/head/all replay로 보고하고, target10은 raw-text PPPL,
tokenization, zero-step, after-MLM PPPL 중심으로 해석한다. 이 구분이 없으면 coverage
gap을 성능 결과로 착각하게 되므로, v5에서는 measured, waiting, coverage-limited를 분리해
보고한다.

## Q18. v5-random 결과가 섞여 있는데 novelty가 약해지는 것 아닌가?

아니다. v5-random은 method win이 아니라 diagnostic lower-bound row이다. target10 PPPL에서는
XLM-R보다 좋아졌지만 Glot500-base reference에는 아직 못 미치고, downstream은 metric별로
섞인다. 예를 들어 Tatoeba와 Taxi1500에서는 XLM-R보다 높지만 Glot500-base보다 낮고,
Bible retrieval에서는 두 reference보다 낮다. POS는 all 기준으로 XLM-R과 거의 같지만,
head 기준으로는 XLM-R과 Glot500-base보다 높다.

이 혼합 결과는 설계를 약하게 만드는 것이 아니라, matched `v5_fvt` test가 왜 필요한지
보여준다. random resize + 10K MLM만으로는 안정적인 method claim이 되지 않으므로,
같은 corpus/tokenizer/schedule에서 FVT가 이 random checkpoint를 넘는지 확인하는 것이
최종 novelty 검정이다.

## Q19. 결과가 일부만 들어오면 결론은 어떻게 하나?

일부 metric row만 있거나, provenance/Final Evidence Packet이 닫히지 않으면 최종 결론을
positive나 negative로 고르지 않는다. 이 경우 공식 결론은 `Incomplete Evaluation /
Execution Draft`이다. 즉 setup fidelity, Glot500 metric-family replay protocol,
zero-step FVT initialization advantage까지만 확정하고, after-MLM PPPL 및 downstream
superiority claim은 잠근다.

이 답변은 실패 방어가 아니라 claim hygiene이다. 좋은 숫자가 일부 보여도 paired
`v5_random`/`v5_fvt` row, provenance, materiality band, decision tree, final freeze audit가
같은 refresh에서 닫히지 않으면 `measured but not promotable`로 남긴다. 사용할 문장은
`../03_final_report/result_interpretation_blocks.md`의 `Incomplete Evaluation / Execution Draft`
블록에서만 가져온다.

## 바로 열 파일

| 상황 | 파일 |
| --- | --- |
| claim 가능/불가능 판단 | `../claim_promotion_matrix.md` |
| 최종 결론 문구 선택 | `../final_claim_decision_tree.md`, `../post_checkpoint_outcome_matrix_ko.md` |
| 일부 결과/불완전 평가 결론 | `../03_final_report/result_interpretation_blocks.md` |
| metric family fidelity 방어 | `../00_tables/table_13_metric_fidelity_matrix.md` |
| metric별 measured/waiting 상태 | `../metric_execution_ledger.md` |
| target10/downstream coverage 질문 | `../../3_evaluation/00_coverage/coverage_summary.tsv` |
| post-checkpoint 실행선 | `../../3_evaluation/post_checkpoint_execution_plan.md` |
| post-checkpoint row 상태 | `../../3_evaluation/post_checkpoint_eval_queue.md` |
| full Q&A | `defense_qa.md` |
