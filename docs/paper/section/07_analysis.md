# 07 Representation Analysis

score 표만으로 보이지 않는 표현 공간 변화를 진단한다. 이 절의 plot은 official benchmark가 아니라 **representation geometry diagnostic**이며, centered cosine similarity를 중심으로 읽는다(raw cosine은 대부분 0.9 근처라 anisotropy 영향이 크다).

## 7.1 왜 centered cosine인가 / 어떤 데이터인가

Target7이 모두 Latin script이므로 "같은 문자라서 가까운가"와 "계통이 가까워서 가까운가"를 분리해서 봐야 한다. 그래서 최소 하나의 tail 언어를 포함하는 pair만 구성하고(head-head pair 제외), relation을 same-language / same-family / same-macro-family / same-script-only / different로 나눈다. sampled languages 38개, sentence points 3,708개, tail-anchored pair 11,956개.

## 7.2 Family/script similarity (FVT, 50K)

**Table 6. Relation bucket별 centered cosine (FVT, step 50K).**

| Relation type | Pairs | Mean centered cosine |
| --- | ---: | ---: |
| tail within language | 350 | **0.455** |
| tail–tail same family | 50 | 0.266 |
| tail–tail same macro-family | 100 | 0.146 |
| tail–tail different family | 900 | 0.074 |
| tail–head same family | 1,050 | 0.052 |
| tail–head diff family, same Latn script | 6,100 | −0.041 |
| tail–head diff family, diff script | 1,856 | −0.063 |

**해석.** 유사도가 `same language > same family > same macro-family > different family` 순으로 단조 감소한다. 같은 Latin script만 공유하는 경우(−0.041)보다 같은 family를 공유하는 경우(0.052, tail–head 기준)가 더 가깝다. 즉 이 공간에서는 script 효과도 일부 있지만 **family/typology 효과가 더 강한 설명력**을 가진다. tail끼리만 봐도 같은 순서가 나온다. Figures: `10_convergence_similarity/*/checkpoint-50000/family_similarity/family_pair_boxplot_...png`, `family_centroid_heatmap_...png`.

## 7.3 Step별 궤적: 구조는 10K 이전에 형성되고 이후 평탄하다 (10K→50K)

다섯 방법의 checkpoint를 step 10K~50K로 이어 보면(근거: `3_evaluation/11_inference/similarity_maps/similarity_10k50k_summary.tsv`, 5-way 전부 산출), **관측 구간에서 language/family geometry는 이미 형성되어 있고 거의 변하지 않는다.**

**Table 7. FVT의 relation bucket별 centered cosine, step 10K→50K.**

| Relation (fvt) | 10K | 30K | 50K |
| --- | ---: | ---: | ---: |
| tail within language | 0.458 | 0.454 | 0.455 |
| tail–tail same family | 0.274 | 0.264 | 0.266 |
| tail–tail same macro-family | 0.150 | 0.145 | 0.146 |
| tail–tail different family | 0.081 | 0.074 | 0.074 |

hierarchy(`same language > same family > macro > different`)는 10K에서 이미 완성돼 있고, 50K까지 격차가 더 벌어지지 않는다(오히려 미세하게 압축된다).

한편 **cross-lingual semantic alignment(같은 의미 src↔eng pair)는 소폭 개선 후 포화**한다: Tatoeba aligned 0.194→0.199(20K 포화), Bible aligned 0.060→0.072(40K 피크 후 정체), Roundtrip src–eng 0.038→0.049(40K 피크 후 정체). 반면 §6.2의 training loss와 §6.4의 PPPL은 50K까지 단조 감소한다.

**해석(정직한 경계).** 이 관측 구간에서 "step이 갈수록 표현이 점점 더 분리·개선된다"는 강한 주장은 성립하지 않는다. 언어·계통 구조는 우리가 snapshot을 가진 첫 지점(10K)에 이미 존재하며, 10K 이후 추가 학습 이득은 geometry cosine이 아니라 loss/PPPL 및 소폭의 alignment 개선으로 나타난다. 만약 "지역 먼저 → 계통 나중"의 단계적 창발이 있었다면 그것은 10K **이전** early phase에서 일어났을 가능성이 크며, 해당 구간의 geometry snapshot이 없어 본 보고서는 그 단계적 창발을 주장하지 않는다.

**Method 간 비교(step 40K).** relation bucket 값은 방법 간 차이가 작다. `family_mean`이 tail-within-language(0.486)와 tail–head same-family(0.064)에서 근소하게 높고, `random`은 tail–tail different-family(0.101)가 더 높아(= 서로 다른 계통이 덜 분리됨) geometry separation이 약간 나쁘다. FVT/weighted_fvt는 중간이다. 즉 geometry에서는 방법 간 격차가 크지 않으며, 초기화 효과는 geometry보다 loss/PPPL/retrieval(§6)에서 더 뚜렷하다.

## 7.4 2D embedding map 해석

38개 언어 subset의 문장 임베딩 평균(centroid)을 2D PCA로 시각화한다(§A.4 추출 방식). 색은 language family, 삼각형(▲)은 tail 언어, 원(●)은 head/reference 언어를 나타낸다. Figures: `.../embedding_similarity/embedding_map_2d.png`, `family_point_map_tail_by_language_...png`, `family_centroid_map_...png`.

**무엇이 보이는가.**
- **계통 clustering.** 같은 family 언어들이 대체로 인접한다. Slavic(`csb`+`ces/hrv/pol/slk/slv`), Romance(`fur`,`lij`+`cat/fra/ita/por/ron`), Austronesian(`dtp`+`ind/jav/msa/tgl`)이 각각 국소 군집을 이룬다. 이는 §7.2의 "same family > same script" 순서와 시각적으로 일치한다.
- **잘 분리되는 tail.** `dtp`(Austronesian), `bam`(Mande), `xav`(Macro-Je)는 주변 head가 적어 비교적 뚜렷이 떨어진 위치에 놓인다.
- **겹치는 tail.** `csb`,`fur`,`ile`,`lij`는 유럽권 Latin 언어(Slavic/Romance/Constructed)라 서로, 그리고 인접 head와 많이 겹친다 — script·지리 근접성 때문이다.
- **tail이 대응 family 쪽으로 끌린다.** 각 tail centroid는 무작위가 아니라 자기 계통 head 군집 방향에 자리한다. 이는 vocabulary extension + continued pretraining이 새 언어를 관련 head 언어의 표현 이웃으로 끌어온다는 Glot500의 "related-language help" 관찰과 부합한다.

**주의.** centroid map은 sentence-level point보다 잘 분리되며, point-level에서는 완전한 cluster separation이 아니다. 따라서 "완벽히 분리된다"가 아니라 "tail language identity와 family 구조가 관찰된다"로 읽는다. 2D는 768차원의 projection이라 거리 왜곡이 있으므로 numeric score(§6)보다 보조적이다.

## 7.5 종합: 어떤 초기화가 가장 좋은가

세 관점에서 "best model"을 정리한다(근거 §6.2–6.4).

| 관점 | 지표 | 최고 method | 2위 |
| --- | --- | --- | --- |
| **MLM 학습 자체** | 50K training loss (전체 corpus) | **weighted_fvt** (2.73) | fvt (2.76) |
| **MLM intrinsic (target)** | 50K target PPPL | **family_mean** (12.3) | weighted_fvt (13.9) |
| **Downstream (retrieval)** | Tatoeba Acc10 | **family_mean** (36.1) | weighted_fvt (35.8) |
| **Downstream (sequence labeling)** | NER F1 | **family_mean** (55.8) | fvt (51.3) |
| **Downstream (alignment)** | Roundtrip Acc | **weighted_fvt** (3.4) | fvt (3.2) |

(NER family_mean 55.8은 Glot500-m 52.6·XLM-R-L 53.9까지 능가.)

**종합적으로 가장 이상적인 모델.** `random`·`mean`은 모든 축에서 하위이고(특히 `mean`은 loss 최악), 개선은 전부 **FVT 계열**에서 나온다. 그중에서도:
- **`family_mean`이 target downstream의 최강자**다: target PPPL·Tatoeba·NER 세 지표 모두 최고이며, **NER에서는 full Glot500-m까지 능가**한다. 계통 prior가 target 언어 표현에 특히 유리하다는 해석과 일치. 다만 전체 corpus loss는 3위다(head 일반화보다 target 특화).
- **`weighted_fvt`가 가장 균형 잡힌 default**다: training loss 최저·Roundtrip 최고에 PPPL·Tatoeba·NER 상위권으로 모든 축에서 안정적이다.
- **plain `fvt`는 "빠른 출발, 조기 포화"**: 초반(≤10K)엔 최고지만 수렴 시점엔 두 refinement에 추월당한다.

결론적으로, low-resource vocabulary adaptation에서 새 embedding row는 무정보(`random`)나 전역 centroid(`mean`)가 아니라 **source subtoken/계통 정보를 재사용하는 FVT 계열로 초기화하는 것이 유리하다. target 성능이 목표면 `family_mean`(NER에서 Glot500-m 능가), 전반적 균형이 목표면 `weighted_fvt`가 최선이다.**

## 금지할 과장

- 2D projection만으로 semantic alignment가 완성됐다고 하지 않는다(distortion 존재).
- centered cosine diagnostic을 Glot500 official metric처럼 쓰지 않는다.
- 38개 subset 결과를 Target7 전체 계통에 대한 강한 typological 결론으로 확대하지 않는다.
