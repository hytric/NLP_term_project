# v5 Presentation Presenter Script

작성 상태: execution draft, 2026-06-28 기준.

이 문서는 `ppt_content.md`를 실제 발표용 한국어 발화문으로 풀어 쓴 것이다. 숫자는
측정된 artifact에서 온 값만 사용하고, running 상태는 final result가 아니라 진행
상황으로 말한다. `pending_result_registry.md`의 `running`, `waiting checkpoint`,
`blocked-data`, `coverage-limited` 구분을 따른다.

발표 직전의 checkpoint 진행률과 Go/No-Go는 이 파일의 문장보다
`final_action_dashboard_ko.md`와
`bash scripts/run_v5_post_checkpoint_evals.sh status`를 우선한다.

## Slide 1. Title

오늘 발표할 내용은 Glot500 전체를 그대로 재학습했다는 주장이 아닙니다. 대신
Glot500의 핵심 실험 흐름을 계산 가능한 102개 language-script setting에서 재연하고,
vocabulary extension 이후 새 embedding row를 어떻게 초기화할지 비교하는 실험입니다.

설정은 XLM-R 학습에 포함된 것으로 볼 수 있는 Glot500 language-script 92개와,
Glot500 raw 안에 있지만 XLM-R seen이 아닌 target language-script 10개입니다. 이
controlled setting 안에서 reproduction과 novelty를 분리해서 보겠습니다.

## Slide 2. Motivation And Contributions

XLM-R 같은 multilingual model은 많은 언어를 지원하지만, 실제 품질은 균일하지
않습니다. 특히 low-resource 언어, 희귀 script, tokenizer coverage가 낮은 언어는
tokenization부터 representation까지 불리할 수 있습니다.

Glot500은 이런 문제를 더 많은 언어의 corpus, tokenizer 확장, continued pretraining으로
해결하려고 한 작업입니다. 여기서 저희 질문은 조금 더 좁습니다. 새 token을 vocabulary에
추가했을 때 그 embedding row를 그냥 random으로 둘 것인지, 아니면 기존 모델의 정보를
이용해 더 좋은 시작점으로 둘 수 있는지입니다.

그래서 기여는 세 가지입니다. 첫째, 92+10 controlled Glot500-style replay를 artifact와
audit 단위로 고정했습니다. 둘째, 새 vocabulary row initialization을 novelty 축으로
분리했습니다. 셋째, downstream task는 빠뜨리지 않고 PPPL, retrieval, classification,
tagging, Roundtrip을 coverage와 함께 끝까지 추적합니다.

## Slide 3. Reproduction Boundary

먼저 reproduction boundary를 분명히 하겠습니다. v5는 full 511-language Glot500
reproduction이 아닙니다. 이 표현은 쓰면 안 됩니다.

대신 v5는 Glot500-style pipeline reproduction입니다. 즉 corpus를 구성하고,
SentencePiece vocabulary를 확장하고, continued MLM pretraining을 수행하고, Glot500에서
사용한 metric family를 유지하는 구조를 102개 언어 설정에서 재연합니다.

그래서 발표와 보고서에서는 항상 controlled 102-language subset reproduction이라고
표현합니다. 이 경계가 있어야 결과 해석이 과장되지 않습니다.

## Slide 4. Target10 Selection

target10은 외부에서 임의로 가져온 언어가 아니라 Glot500 raw 안에서 다시 골랐습니다.
조건은 세 가지입니다. XLM-R seen이 아니고, `new_length`가 30,000 이상이고, local raw
directory가 실제로 존재해야 합니다.

슬라이드에는 scripts, regions, `new_length` range를 요약했습니다. 예를 들어 Arabic
script의 `acm_Arab`, Tibetan script의 `dzo_Tibt`, Ol Chiki script의 `sat_Olck`가 있고,
Latin script 안에서도 Europe, West Africa, Mesoamerica, Andean South America,
Polynesia가 함께 들어갑니다. 그래서 target10은 한 지역이나 한 문자권에 몰린 샘플이 아니라,
Glot500 내부에서 고른 diversity-controlled target set입니다.

따라서 novelty는 corpus를 새로 만들었다는 데 있지 않습니다. Glot500 내부 데이터에서
controlled target set을 만들고, 그 위에서 vocabulary expansion과 initialization을
비교하는 데 있습니다.

## Slide 5. Corpus Construction

full merge는 완료되었습니다. 총 102개 language-script이고, planned sample 수와 실제
sample 수가 모두 92,452,251로 일치합니다. 파일 크기는 약 19G이고, missing language
directory는 0개입니다.

이 점이 중요합니다. 이후 tokenizer, initialization, MLM, downstream 평가가 모두 같은
data scope 위에서 돌아가기 때문입니다. data scope가 흔들리면 reproduction claim도
흔들리는데, v5에서는 manifest와 merge report로 이 부분을 고정했습니다.

## Slide 6. Tokenizer Method

tokenizer는 Glot500-style SentencePiece append 방식을 사용했습니다. auxiliary SPM을
학습하고, 기존 XLM-R SPM에 없는 piece를 뒤에 붙이는 방식입니다.

이 방식은 V3에서 했던 add_tokens 계열 방법과 다릅니다. add_tokens 방식은 기존 id를
보존하기 쉽지만, Glot500 reproduction에는 SentencePiece append가 더 가깝습니다. 다만
append 방식에서는 `<mask>` 같은 special token id가 움직일 수 있습니다.

실제로 main tokenizer에서 vocab size는 250,002에서 368,687로 늘었고, 118,685개의 token이
추가되었습니다. `<mask>`는 250001에서 368686으로 이동했습니다.

audit 결과는 대체로 좋습니다. 30개 audit language 중 29개, 즉 29/30에서 tokens per
word가 개선됐고, target10에서는 9/10이 개선됐습니다. 다만 `dzo_Tibt`는 4.223938에서
5.552124 tokens/word로 악화되었습니다. 이 failure case는 숨기지 않고 main limitation으로
가져갑니다.

## Slide 7. Novelty: Initialization Question

이 실험의 novelty는 새 corpus가 아니라 새 vocabulary row initialization입니다. 새 token이
생겼을 때 embedding row를 어떻게 시작할지가 질문입니다.

비교하는 방법은 세 가지입니다. `random`은 Hugging Face resize의 기본 random
초기화입니다. `mean`은 source/global mean vector를 쓰는 안정적인 baseline입니다. `fvt`는
새 token surface를 기존 XLM-R tokenizer로 다시 tokenize하고, 그 source subtoken embedding을
평균내서 새 row를 초기화합니다.

직관은 간단합니다. 새 token이 완전히 낯선 symbol이 아니라면, 기존 tokenizer가 그 surface를
여러 subpiece로 분해할 수 있습니다. 그 subpiece embedding 평균이 random보다 더 좋은
시작점일 수 있다는 것입니다.

## Slide 8. Initialization Audit

initialization 비교는 correctness audit이 없으면 의미가 없습니다. 특히 SPM append에서는
id prefix가 그대로 source row를 의미한다고 가정하면 안 됩니다.

그래서 v5에서는 source row를 token identity 기준으로 복사했습니다. `<mask>` row는 source
id 250001에서 target id 368686으로 명시적으로 remap했습니다. byte fallback row와 lexical
fallback row도 따로 기록했습니다. input embedding과 LM head tying도 확인했습니다.

main FVT에서는 source identity row 250,002개를 복사했고, 새 row 118,685개 중 118,427개를
FVT로 초기화했습니다. byte row는 256개, lexical fallback은 2개입니다. `<mask>` diff는
0.0이고 LM head tied도 true입니다.

## Slide 9. Zero-Step Evidence

zero-step 결과가 핵심입니다. target weighted NLL에서 random은 18.411756, mean은 11.953142,
FVT는 8.785518입니다. FVT는 random보다 9.626238 낮고, mean보다도 3.167624 낮습니다. 이
결과가 현재 novelty를 가장 강하게 지지합니다. `method_comparison_summary.md` 기준으로
FVT는 random 대비 weighted NLL을 target에서 52.28%, head에서 48.65%, 전체 zero-step
row에서 51.31% 낮춥니다.

## Slide 10. Training Setup

이제 이 zero-step advantage가 continued MLM 이후에도 유지되는지가 main experiment입니다.
이를 위해 `v5_random`과 `v5_fvt`는 같은 corpus, 같은 tokenizer, 같은 schedule, 같은 10K
checkpoint rule로 학습해야 합니다.

현재 paired launcher는 예상한 transition에 들어갔습니다. `v5_random_mlm_10k`는 10K
selected checkpoint를 만들었고, 같은 설정의 `v5_fvt_mlm_10k`가 실행 중입니다. live snapshot은
`docs/exp/v5/3_evaluation/running_status.md`와
`docs/exp/v5/2_training/mlm_progress_eta.md`에서 확인합니다. 발표에서는 pair 전체가 아직
완성되지 않았고 post-checkpoint 평가가 잠겨 있다는 gate만 말합니다. 이 live progress는 품질
결과가 아니라 운영 상태입니다. 따라서 step 수나 ETA가 좋아 보여도 final result table에는 넣지
않습니다.

## Slide 11. Glot500 Metrics

evaluation은 Glot500에서 사용한 metric family를 모두 유지합니다. 슬라이드의 coverage
summary는 metric별 local coverage, target10 coverage, v5 method row 상태를 압축해서 보여줍니다.
PPPL은 102/102 전체와 target10 10/10에 들어가고, Tatoeba는 63/102, Bible과 Roundtrip은
각각 74/102, NER는 materialization audit 기준 78/102, POS는 58/102입니다. Taxi1500은
local split 기준 1/102라서 가장 좁은 evidence로 표시합니다. 이 주장은
`table_13_metric_fidelity_matrix.md`에서 metric별로 확인할 수 있게 정리했습니다.
각 metric이 measured인지, v5 checkpoint를 기다리는지, coverage-limited인지,
blocked-data인지 같은 표면에서 보여줍니다.

중요한 점은 coverage입니다. target10은 raw text가 있으므로 PPPL에는 10/10으로 들어갑니다.
하지만 현재 downstream task data에서는 target10 coverage가 거의 없습니다. Tatoeba, NER,
POS, Bible, roundtrip에서 target10 local coverage는 현재 0/10입니다.
단, NER output에는 `fur_Latn` 하나의 actual evaluated intersection이 있습니다. 이것은
단일 target-language row로 보고하되, materialized target10 coverage나 target10-wide
downstream evidence로 승격하지 않습니다.

그래서 downstream 결과를 말할 때 target10 improvement라고 말하지 않습니다. 대신
available-language, head, all 기준으로 Glot500 metric replay를 보고하고, target10은
tokenization, zero-step, after-MLM PPPL 중심으로 해석합니다.

## Slide 12. Current Measured Rows

현재 final table에 넣을 수 있는 measured baseline/reference 결과가 있습니다.

PPPL에서 XLM-R-base는 target 61.980216, head 8.117338, all 9.986271입니다. Glot500-base는
target 15.102934, head 10.213100, all 10.640353입니다. 이 결과는 Glot500-base가 target
raw-text PPPL에서 강하다는 reference scale을 보여줍니다.

Tatoeba retrieval에서는 XLM-R-base가 head 0.656309, all available 0.566067이고,
Glot500-base는 head 0.743755, all available 0.706649입니다. v5-random도 측정되어
head 0.700285, all available 0.610353입니다. Taxi1500에서는 XLM-R-base
macro-F1이 0.592876이고 Glot500-base macro-F1이 0.743338이며, v5-random은
0.702956입니다.

NER에서는 XLM-R-base all F1이 0.549858이고 Glot500-base all F1이 0.627108입니다.
v5-random NER도 측정되어 all F1 0.544628, head F1 0.608020입니다. `fur_Latn`
하나의 actual target intersection도 있지만, 이것은 target10-wide evidence로
말하지 않습니다. POS에서는 XLM-R-base all F1이 0.481336이고 Glot500-base all F1이
0.567542이며, v5-random all F1은 0.481102입니다. head 기준으로는 v5-random POS가
0.587430으로 XLM-R-base 0.571446과 Glot500-base 0.573832보다 높습니다. local POS에는
`train-eng_Latn.tsv`가 없어서 `TRAIN_LANGS=tur_Latn` 조건으로 해석해야 한다는 caveat를
같이 말합니다.

Bible retrieval에서는 available language-script 74개 기준으로 XLM-R-base Top-10이
0.381153이고, Glot500-base Top-10이 0.509356이며, v5-random Top-10은
0.328019입니다. target10 Bible coverage는 여전히 0/10이므로 target10 downstream
claim으로 쓰지는 않고, available-language reference로 해석합니다.

Roundtrip alignment도 같은 74개 available language-script 기준으로 측정됐습니다.
XLM-R-base accuracy는 0.185300이고, Glot500-base accuracy는 0.205189이며,
v5-random accuracy는 0.190300입니다. 이것도 target10 downstream evidence가 아니라
available-language row로 둡니다.

이 시점의 핵심 해석은 v5-random이 method win이 아니라 diagnostic row라는 점입니다.
target10 PPPL에서는 XLM-R보다 좋아졌지만 Glot500-base reference에는 아직 못 미치고,
downstream은 metric별로 좋고 나쁨이 섞여 있습니다. 그래서 아직 비어 있는 것은
v5-FVT의 after-MLM PPPL/downstream rows이며, 이 부분은 matched checkpoint가 생긴 뒤
같은 wrapper로 평가해서 채웁니다.

## Slide 13. Coverage And Limitations

제한점은 명확합니다. 첫째, full 511-language Glot500 reproduction이 아닙니다. 둘째,
target10 downstream coverage가 현재 PPPL 외에는 거의 없습니다. 셋째, Glot500-base는
external reference이지 equal-compute baseline이 아닙니다.

또한 tokenizer가 모든 target에서 좋아진 것도 아닙니다. `dzo_Tibt`는 계속 악화됐고, 이 case는
오히려 중요한 분석 포인트입니다. 새 piece를 많이 추가하는 것이 항상 좋은 segmentation을
보장하지는 않는다는 뜻입니다.

따라서 최종 보고서에서는 성공한 결과와 실패한 결과를 함께 보여줍니다. 이 점이 v5의 신뢰도를
높입니다.
특히 Slide 13에서는 `table_09_blocked_metric_notes.md`와
`table_13_metric_fidelity_matrix.md`를 같이 사용해서, 누락이 아니라 명시적
coverage/blocker accounting임을 보여줍니다.

## Slide 14. Conclusion

현재까지의 결론은 세 가지입니다.

첫째, v5는 controlled 102-language setting에서 Glot500-style workflow를 재연할 수 있는
상태까지 왔습니다. data scope, full merge, tokenizer, initialization audit, zero-step
evaluation이 완료되었습니다.

둘째, novelty는 분명합니다. 새 embedding row를 random으로 두는 것보다 source-token
decomposition으로 초기화하는 것이 zero-step target MLM proxy에서 크게 좋습니다.

셋째, final downstream conclusion은 아직 보류입니다. matched `v5_random`과 `v5_fvt`
checkpoint가 생성되고, Glot500 metric family가 parse된 뒤에만 최종 claim으로 올립니다.
이 결론 잠금은 `final_claim_decision_tree.md`와 `final_claim_freeze_audit.md`에서
같이 확인합니다. 결과가 들어온 뒤 실제 report/PPT 수정은
`post_result_patch_plan_ko.md`의 `ready_for_patch` row만 따라갑니다. 그래서 현재
발표에서는 "FVT가 zero-step에서 좋다"까지는 강하게 말하고, "after-MLM이나
downstream에서도 좋다"는 말은 결과가 들어올 때까지 하지 않습니다.

### Slide 14 Post-Checkpoint Replacement

checkpoint 이후에는 `post_result_patch_plan_ko.md`가 허용한 파일-level 수정 범위 안에서
`post_checkpoint_outcome_matrix_ko.md`와 `final_claim_decision_tree.md`가 고른 outcome만
사용합니다. 아래 문장은 slide 14의 마지막 30초를 교체하는 용도입니다.

Bounded positive outcome:

```text
최종 결과에서는 FVT가 PPPL에서 random resize보다 유리했고, available-language
downstream row 다수에서도 같은 방향의 evidence가 나왔습니다. 그래서 결론은
강하지만 제한된 positive claim입니다. 새 vocabulary row initialization은 도움이 될 수
있지만, target10 downstream coverage가 거의 없기 때문에 target10 transfer claim은
여전히 제한합니다.
```

Intrinsic positive, downstream mixed outcome:

```text
FVT는 PPPL에서는 분명히 유리했지만 downstream 결과는 task별로 섞였습니다. 그래서
이 연구의 가장 강한 결론은 intrinsic adaptation 개선입니다. downstream은 실패나
성공으로 단순화하지 않고, available-language와 coverage 조건 안에서 해석합니다.
```

Early-only diagnostic outcome:

```text
FVT는 zero-step에서는 매우 좋은 시작점을 만들었지만, matched continued MLM 이후에는
그 우위가 유지되지 않았습니다. 따라서 결론은 superiority가 아니라 diagnostic evidence입니다.
새 embedding row initialization이 early adaptation을 바꾼다는 점은 보였고, 그 효과를
끝까지 보존하려면 추가 조건이 필요합니다.
```

Negative final comparison outcome:

```text
최종 비교에서는 FVT가 random resize를 넘어서지 못했습니다. 하지만 이 결과는 실패로만
볼 수 없습니다. 같은 tokenizer, corpus, budget에서 decomposition initialization이 항상
final gain을 보장하지 않는다는 controlled negative result이고, 다음 연구에서는 row update
전략이나 training objective를 더 봐야 한다는 방향을 줍니다.
```

Incomplete evaluation outcome:

```text
아직 matched checkpoint나 post-checkpoint metric row가 완결되지 않았기 때문에, final
method claim은 잠급니다. 현재 확정 가능한 결론은 controlled Glot500-style replay,
tokenizer/initialization audit, 그리고 zero-step FVT advantage입니다.
```

## Slide 15. Backup: Execution Artifacts

재현성을 위해 모든 주요 artifact를 문서화했습니다. plan은 `Plan.md`, 현재 상태와 폴더 구조는
`README.md`, report draft는 `Report.md`와 `paper_draft.md`에 있습니다.

metric 실행은 `scripts/run_v5_eval_metric.sh`를 사용합니다. 이 wrapper는 model key, model
path, tokenizer path, GPU, output root를 metadata로 남기기 때문에, inherited evaluation
script를 직접 실행하는 것보다 final report에 적합합니다.

현재 실행 큐와 다음 실행 순서는 `execution_queue.md`, `next_runbook.md`,
`post_checkpoint_eval_queue.md`, `post_checkpoint_execution_plan.md`에 정리되어 있습니다.
queue는 metric/model row 상태를 보여주고, execution plan은 실제 launch env, log/output
위치, claim 승격 규칙을 보여줍니다. 최종 목표 기준의 완료 여부는
`objective_completion_audit.md`와 `final_claim_freeze_audit.md`에서 확인합니다. 따라서
job이 끝나면 바로 aggregation, figure, readiness audit, report/PPT 업데이트 순서로
이어갈 수 있습니다.
