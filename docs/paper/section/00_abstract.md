# 00 Abstract

## 한 줄 요약

XLM-R 기반 multilingual encoder를 Glot500-style vocabulary extension으로 low-resource tail language에 확장할 때, 새 vocabulary embedding row를 어떻게 초기화하느냐가 continued MLM pretraining의 수렴과 downstream transfer에 실질적 영향을 준다는 것을 controlled ablation으로 보인다.

## Abstract (본문)

Multilingual masked language model인 XLM-R은 100여 개 언어를 커버하지만, 학습에 포함되지 않은 tail language에서는 subword가 과도하게 잘게 쪼개지고(over-fragmentation) 표현이 정렬되지 않는 문제가 남는다. Glot500은 mixed corpus로 SentencePiece unigram tokenizer를 다시 학습해 vocabulary를 확장하고, 확장된 모델을 MLM으로 continued pretraining하여 이 문제를 완화했다. 그러나 vocabulary를 확장하면 embedding matrix 뒤에 기존에 없던 새 token row가 추가되는데, 이 row를 **어떤 벡터로 시작할지**는 별도의 modeling 선택으로 남아 있고 체계적으로 비교된 적이 드물다.

본 보고서는 이 선택 하나만 통제 변인으로 두고 비교한다. Base model은 `xlm-roberta-base`, 데이터는 92개 XLM-R-seen replay language-script와 7개 XLM-R-unseen target language-script(Target7)이며, tokenizer는 Glot500 방식의 SentencePiece unigram append로 **고정**한다. 그 위에서 새 token embedding row 초기화만 `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean`의 다섯 가지로 바꾸어, 동일한 corpus·objective·schedule·evaluation protocol 아래 continued MLM pretraining을 수행한다.

모든 결과는 50K-step 수렴 checkpoint를 기준으로 보고한다. 주요 관찰은 세 가지다. 첫째, 확장 tokenizer는 Target7의 tokens/word를 2.204에서 1.592로 약 27.75% 낮춰 fragmentation을 실제로 줄인다. 둘째, 같은 tokenizer를 공유함에도 초기화에 따라 수렴 loss가 갈린다. 최종 MLM loss는 `weighted FVT`(2.73), `FVT`(2.76)가 가장 낮고 `random`(3.12), `mean`(3.27)이 가장 높으며, 특히 `mean`은 `random`보다도 나쁘다 — source subtoken을 재조합하는 FVT 계열 prior는 지속적 optimization 이득을 주지만 단순 centroid(`mean`)는 그렇지 않다. 셋째, 50K downstream에서 우리가 추가한 두 refinement(`weighted FVT`, `family-aware mean`)가 target pseudoperplexity·Tatoeba retrieval·NER·roundtrip alignment에서 최고이며 — 특히 `family-aware mean`은 NER에서 full Glot500-m을 능가한다 — 학습 초반엔 plain `FVT`가 앞서다가 수렴 구간에서 이 refinement에 추월당한다.

claim은 controlled setup 안으로 제한한다. 특정 초기화가 모든 task에서 항상 최고라고 주장하지 않으며, Target7이 모두 Latin script이므로 script 다양성 결론도 내리지 않는다. 본 보고서의 기여는 새 아키텍처가 아니라, low-resource vocabulary adaptation에서 흔히 임의로 정해지는 embedding initialization이 통제된 조건에서도 수렴과 평가 지표를 바꾸며, FVT를 정교화한 초기화가 종합적으로 가장 유리함을 재현 가능하게 문서화한 데 있다.

## Claim boundary

- 주장 가능: 동일 tokenizer/corpus/objective/protocol에서 initialization이 50K 수렴 양상과 지표를 바꾸며, FVT 계열 refinement가 종합적으로 유리하다.
- 주장 보류: 특정 method가 모든 task에서 항상 최고라는 universal claim.
- 주의: Target7은 script diversity를 대표하지 않음. Bible retrieval은 floor, Text는 head/EN-only.
