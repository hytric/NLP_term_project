# v5 Presentation Talk Track

Last updated: 2026-06-27

## Opening

오늘 발표의 핵심은 Glot500을 그대로 511개 언어 규모로 다시 학습했다는 주장이
아닙니다. 대신 Glot500의 중요한 구조인 corpus sampling, SentencePiece vocabulary
extension, continued MLM pretraining, 그리고 downstream metric family를 102개
language-script setting에서 재연합니다.

## Why This Is Still Faithful

재연의 단위는 scale이 아니라 실험 논리입니다. v5는 XLM-R에 있던 92개 Glot500
language-script와, Glot500 내부 raw에 존재하지만 XLM-R seen이 아닌 target10을
사용합니다. tokenizer는 Glot500-style append 방식을 따르고, MLM과 평가 metric
family도 Glot500의 구조를 유지합니다.

## Novelty

새로운 질문은 vocabulary를 늘린 뒤 새 embedding row를 어떻게 시작할지입니다.
random resize는 간단하지만 low-resource language에서는 새 row가 충분히 학습되기
전에 random 상태의 비용이 크게 남을 수 있습니다. FVT는 새 token surface를 기존
XLM-R tokenizer로 다시 분해하고, 그 source subtoken embedding 평균으로 새 row를
초기화합니다.

## What We Already Know

full merge와 main tokenizer는 완료되었습니다. tokenizer는 118,685개 token을
추가했고, 30개 audit language 중 29개에서 fertility가 좋아졌습니다. 단,
`dzo_Tibt`는 계속 악화되므로 성공 claim 안에 failure case로 넣어야 합니다.

zero-step 결과는 novelty를 강하게 지지합니다. target group에서 FVT weighted NLL은
8.785518이고, random은 18.411756입니다. 즉 continued training 전부터 embedding
initialization 차이가 명확히 보입니다.

## What Is Still Pending

main claim을 완성하려면 matched `v5_random`과 `v5_fvt` MLM checkpoint가 필요합니다.
현재 paired 10K run은 시작되어 있고, `v5_random`은 full-corpus preprocessing
barrier를 지나 Trainer optimization에 들어갔습니다. live snapshot은
`docs/exp/v5/3_evaluation/running_status.md`에서 생성하며, `v5_fvt`는 같은 설정으로
random 이후 실행됩니다. 이후 같은 budget의 checkpoint가 준비되면 PPPL과 downstream
metric을 실행합니다.

baseline/reference downstream rows도 local data가 있는 범위에서 측정되어
aggregation에 들어갔습니다. PPPL, Tatoeba, Bible retrieval, Taxi1500, NER,
POS, Roundtrip의 XLM-R/Glot500-base row가 현재 비교 기준입니다. Bible retrieval은 74개
available language-script 기준으로 XLM-R-base Top-10 0.381153,
Glot500-base Top-10 0.509356입니다. 단 target10 Bible coverage는 0/10이므로
target10 downstream claim으로 쓰지 않습니다. Roundtrip도 74개 available
language-script 기준으로 XLM-R-base accuracy 0.185300, Glot500-base accuracy
0.205189가 측정됐고, target10 coverage는 0/10입니다. XLM-R NER는 all F1 0.549858,
head F1 0.621207이고, v5-target actual intersection은 fur_Latn 하나라
0.459364로만 좁게 해석합니다. Glot500-base NER는 all F1 0.627108, head F1
0.645915, fur_Latn actual intersection 0.553191입니다. POS도 XLM-R-base와
Glot500-base가 모두 aggregation에 들어갔습니다. XLM-R-base POS는 all F1
0.481336, head F1 0.571446이고, Glot500-base POS는 all F1 0.567542, head
F1 0.573832입니다. POS는 local data에 `train-eng_Latn.tsv`가 없어
`TRAIN_LANGS=tur_Latn`으로 학습했다는 note가 붙습니다.

## Downstream Framing

Glot500 metric family는 모두 유지합니다. 다만 selected target10은 현재 downstream
task list에 거의 없기 때문에, target10 downstream improvement를 직접 주장하지
않습니다. target10은 tokenization, zero-step, after-MLM PPPL 중심으로 보고하고,
downstream은 available-language/head/all replay로 제시합니다.
이 경계는 `table_13_metric_fidelity_matrix.md`에 metric별로 정리되어 있어서,
발표 중 질문이 나오면 해당 표를 보여주면 됩니다.

## Closing

이 프로젝트의 장점은 실패와 제한을 숨기지 않는 데 있습니다. full-scale Glot500을
흉내 내는 것이 아니라, 작은 controlled setting에서 어떤 요소가 재현되고 어떤
요소가 새로운 contribution인지 분리합니다. 그래서 최종 report는 reproduction과
novelty를 동시에 말할 수 있습니다.

## If Results Are Mixed

최종 결과가 꼭 한 방향으로 깔끔하게 나오지 않아도 괜찮습니다. FVT가 PPPL에서는
좋고 downstream에서는 섞여 나오면, conclusion은 `intrinsic adaptation gain은
명확하지만 downstream transfer는 task coverage와 task type에 의존한다`로 갑니다.
FVT가 zero-step에서만 좋고 10K 후 random이 따라잡으면, contribution은
`초기화가 early adaptation을 바꾼다`는 diagnostic result로 정리합니다. 중요한 건
zero-step, after-MLM PPPL, downstream을 한 문장으로 뭉개지 않는 것입니다.
