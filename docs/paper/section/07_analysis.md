# 07 Analysis Draft

## 목적

score table만으로 보이지 않는 representation 변화를 설명한다. 단, analysis plot은 official benchmark score가 아니라 diagnostic evidence임을 분명히 한다.

## 분석 질문

1. FVT 초기화는 target language sentence representation을 더 안정적인 공간에 놓는가?
2. 같은 language/family pair의 centered cosine similarity가 다른 relation보다 높게 나타나는가?
3. 50K training 이후 초기화 차이가 representation geometry에 남는가, 아니면 MLM training이 차이를 지우는가?

## 현재 사용 가능한 figure

- `docs/exp/v5.2/3_evaluation/09_family_similarity/family_pair_boxplot_v52_fvt_step4000.png`
- `docs/exp/v5.2/3_evaluation/09_family_similarity/family_centroid_map_v52_fvt_step4000.png`

## Figure 설명 기준

### Family pair boxplot

- X-axis: relation bucket, 예: same language, same family, different family.
- Y-axis: centered cosine similarity.
- Box: relation bucket별 distribution.
- 해석: 같은 language 또는 같은 family pair가 더 높은 similarity를 보이는지 확인한다.
- 주의: Step-4000 FVT snapshot이므로 final 50K five-way claim이 아니다.

### Family centroid map

- Point: language/family centroid.
- Distance: embedding space의 relative geometry를 2D projection으로 표현.
- 해석: family별 grouping이 시각적으로 나타나는지 확인한다.
- 주의: 2D projection은 distortion이 있으므로 numeric score보다 보조적이다.

## 50K 결과가 나오면 추가할 분석

- 각 method의 final checkpoint에서 같은 plot을 다시 생성한다.
- random/mean/FVT/weighted FVT/family-aware mean 사이에 family geometry가 어떻게 달라지는지 비교한다.
- 만약 weighted FVT가 loss는 좋지만 downstream이 약하면, representation geometry가 lexical/subtoken prior와 어떻게 다른지 확인한다.

## 금지할 과장

- 2D plot만 보고 semantic alignment가 완성됐다고 주장하지 않는다.
- centered cosine diagnostic을 Glot500 official metric처럼 쓰지 않는다.
- target7 전체 언어 family 구조에 대한 강한 typological 결론을 내리지 않는다.

