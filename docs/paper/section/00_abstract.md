# 00 Abstract Draft

## 한 문장 요약

XLM-R 기반 multilingual encoder를 Glot500-style vocabulary extension으로 low-resource tail language에 확장할 때, 새 vocabulary embedding row의 initialization 방식이 50K-step MLM 수렴과 downstream 성능에 어떤 영향을 주는지 controlled setup에서 비교한다.

## 포함해야 할 요소

- Base model: `xlm-roberta-base`.
- Data scope: 92 XLM-R-seen language-script + 7 XLM-R-unseen target language-script.
- Tokenizer: Glot500-style SentencePiece unigram append.
- Main methods: `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean`.
- Main evidence: 50K-step convergence run.
- Reporting groups: `tail`, `head`, `all`.
- Diagnostic only: Step-4000 random/mean/FVT table.

## Claim boundary

- 주장 가능: 같은 tokenizer/corpus/objective/evaluation protocol에서 initialization이 수렴 양상과 score에 영향을 주는지 검증한다.
- 주장 보류: 특정 method가 모든 task에서 항상 최고라는 식의 universal claim.
- 주의: 4K 결과는 수렴 결과가 아니라 초기 신호다.

## 초안 문장

본 보고서는 Glot500의 horizontal scaling 아이디어를 작은 재현 가능한 설정으로 가져와, XLM-R 기반 multilingual encoder를 low-resource tail language로 확장할 때 새 vocabulary embedding row의 초기화가 수렴과 downstream 성능에 미치는 영향을 분석한다. 실험은 92개의 XLM-R-seen language-script와 7개의 XLM-R-unseen target language-script를 사용하며, tokenizer는 Glot500과 같이 mixed corpus에서 SentencePiece unigram tokenizer를 학습하고 기존 XLM-R SentencePiece model 뒤에 새 piece를 append하는 방식으로 고정한다. 따라서 main ablation은 tokenizer가 아니라 새 token embedding initialization이다.

최종 보고서는 50K-step convergence run을 중심으로 다섯 초기화 방법의 training loss, pseudoperplexity, downstream scores를 tail/head/all group으로 정리한다. Step-4000 결과는 early diagnostic evidence로만 사용한다. 이 구분을 통해 본 보고서는 특정 initialization이 모든 task에서 항상 최고라고 주장하기보다, controlled setup에서 initialization choice가 low-resource vocabulary adaptation의 수렴과 평가 지표에 실질적인 영향을 주는지를 검증한다.

