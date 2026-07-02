# 발표 삽입용: 해결책 제안

## 왜 해결책이 필요한가

Step17에서 실패 원인을 appended-token prediction으로 좁혔다. 그래서 발표에서는 "실패를 찾았다"에서 끝나면 약하다. 바로 다음 슬라이드에서 "그럼 어떤 처방이 맞는가"를 제시해야 한다.

## 발표용 핵심 문장

> The failure suggests that appended tokens should not be learned only from ordinary MLM masks. They need teacher-guided supervision from the original XLM-R subtoken decomposition, while base-token behavior is preserved with KL/replay during curriculum training.

## 제안 해결책

1. Original XLM-R subtoken teacher로 appended token span을 supervision한다.
2. Added-token mask/loss를 curriculum으로 점진적으로 키운다.
3. Base-token KL 또는 replay loss로 old-token behavior를 보존한다.
4. 필요하면 non-final target text를 추가해 rare appended token coverage를 늘린다.
5. 이 모든 방법도 Step15/16-style original control을 통과해야 positive claim으로 인정한다.

## 슬라이드 한 장 구성

```text
Diagnosis:
  added tokens = 50.456741% of tokens
  added loss share = 74.269955%
  added/base loss ratio = 2.835906

Failed simple fixes:
  weighting -> added improves but all-token worsens
  new-row-only -> base preserved but added does not improve
  longer 8k MLM -> original improves faster

Proposed remedy:
  subtoken-teacher distillation
  + curriculum added-token MLM
  + base KL/replay preservation

Required gate:
  added/base/all pass in 3/3 seeds
  word/char normalized ratio <= 1.100000
```

## 주의 문장

- "이 방법이 해결했다"라고 말하지 않는다.
- "진단이 가리키는 다음 방법"이라고 말한다.
- "positive claim은 이 protocol을 통과해야 열린다"라고 말한다.
