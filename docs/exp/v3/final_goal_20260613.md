# Third Try Final Goal

작성일: 2026-06-13

## 최종 목표

`third_try`의 최종 목표는 Glot500 피드백을 따라 **XLM-R-base의 기존 vocabulary id를 보존한 append-only vocabulary extension**을 만들고, **target10 low-resource + high-resource replay/control mixture**로 full-model MLM continued pretraining을 수행한 뒤, **target10 downstream/model evidence가 XLM-R-base보다 좋아지는지** 검증하는 것이다.

기존에 수행했던 `first_try`, `second_try`, short pilot, fallback 비교, checkpoint 선택 실험은 main success claim이 아니라 **ablation/failure analysis**로 배치한다.

## 성공 조건

Positive model claim은 아래 조건을 모두 만족할 때만 허용한다.

1. Base model은 `xlm-roberta-base`다.
2. 기존 XLM-R token id와 special token id는 변하지 않는다.
3. 새 vocabulary는 append-only로 추가된다.
4. Training mixture는 target10 low-resource와 high-resource replay/control을 함께 포함한다.
5. Training은 adapter/LoRA가 아니라 full-model MLM continued pretraining이다.
6. Model-dependent 비교는 최소 3개 seed에서 반복된다.
7. Coptic과 Syriac은 target10 main evidence에 포함된다.
8. Target10 downstream 또는 엄격한 proxy-downstream evidence가 seed-stable하게 XLM-R-base보다 좋아진다.
9. High-resource control에서 큰 degradation이 없어야 한다.

## 현재 판정

현재 evidence는 positive model claim을 통과하지 못한다.

- Replay-safe 1000-step retry는 200-step pilot보다 낫다.
- Coptic POS token accuracy는 3/3 seed에서 약하게 개선된다.
- 그러나 target10 MLM proxy 평균은 여전히 XLM-R-base보다 나쁘다.
- Syriac은 local supervised downstream evidence가 없고 proxy-only 상태다.
- High-resource control은 replay-safe retry 후에도 no-large-collapse threshold를 통과한 언어가 `0/4`개다.

따라서 현재 최종 목표의 종료 형태는 다음으로 고정한다.

`DIAGNOSTIC_NEGATIVE_REPORT_READY`

허용되는 최종 주장은 다음과 같다.

> XLM-R-base append-only vocabulary extension은 target10 평균 tokenizer fragmentation을 줄였지만, 현재 compute-bounded Glot500-style continued-pretraining pilot/retry에서는 그 개선이 broad target10 downstream/model improvement로 이어지지 않았다. High-resource control도 악화되므로, 현재 결과는 positive model success가 아니라 vocab size, initialization, fallback, replay, appended-token learning에 대한 diagnostic negative 및 ablation evidence로 보고해야 한다.

## Positive Claim을 다시 목표로 할 때

Positive route로 재시작하려면 Stage 05로 돌아간다.

필수 수정:

1. replay/control sampling 또는 learning schedule을 더 강하게 재설계한다.
2. 3개 이상 seed를 유지한다.
3. high-resource control no-collapse를 먼저 통과시킨다.
4. target10 downstream coverage를 넓힌다.
5. Syriac에 대해 encoder-only, leakage-safe supervised/proxy-downstream task를 추가한다.
6. `first_try`와 `second_try`는 계속 ablation/failure analysis로만 사용한다.
