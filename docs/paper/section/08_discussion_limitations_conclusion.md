# 08 Discussion, Limitations, Conclusion Draft

## Discussion 방향

이 프로젝트의 장점은 큰 claim보다 실험 통제를 잘한 데 있다. 같은 tokenizer, corpus, objective, evaluation protocol에서 initialization만 바꿨으므로, 50K 결과가 method별로 다르면 그 차이를 initialization과 training dynamics의 상호작용으로 해석할 수 있다.

## 논의할 포인트

1. Tokenizer extension은 fragmentation을 줄였지만, 그것만으로 downstream improvement가 보장되지는 않는다.
2. Mean initialization은 안정적인 centroid baseline이지만 token surface 정보를 쓰지 않는다.
3. FVT는 source tokenizer decomposition을 통해 orthographic/subword 정보를 가져온다.
4. Weighted FVT는 더 긴 source subtoken에 더 큰 weight를 주는 local modification이다.
5. Family-aware mean은 surface decomposition 대신 family prior를 시험하는 exploratory method다.

## Limitations

- Target7은 모두 Latin script이므로 script-diverse 확장 결과가 아니다.
- Downstream coverage가 task마다 다르다.
- Text classification은 target direct evidence가 제한적일 수 있다.
- Step-4000 result는 early diagnostic이다.
- 50K result도 하나의 controlled local setup이므로 전체 Glot500 scale로 일반화하면 안 된다.
- Weighted FVT와 family-aware mean은 local experimental variants이며, 선행 연구의 standard method라고 과장하지 않는다.

## Conclusion 초안

본 보고서는 XLM-R 기반 multilingual encoder에 Glot500-style vocabulary extension을 적용하고, 새 vocabulary embedding row initialization이 50K-step MLM convergence와 downstream score에 미치는 영향을 비교했다. Target7 tokenization fertility는 감소했으며, 이후 method별 차이는 같은 tokenizer 위에서 embedding initialization과 continued pretraining dynamics가 만든 차이로 해석할 수 있다. 최종 claim은 50K five-way result의 tail/head/all table에 한정하며, Step-4000 결과는 FVT 계열이 강한 초기 신호를 보였다는 diagnostic evidence로만 사용한다.

