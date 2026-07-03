# 06 Results

결과는 **세 층위**로 제시한다. (§6.1) 전체 경향성 + best-result 요약, (§6.2) head/tail/all 중심 main table, (§6.3) step별 세부 지표 궤적. 모든 수치는 **50K-step 기준**(Step-4000 미사용). 원자료(step별·언어별 full table, 모든 plot)는 **§9 Appendix**에 전부 첨부한다.

---

## 6.1 Overview — 전체 경향성과 best result

**한 문장 경향.** 같은 tokenizer·corpus에서 초기화만 바꿔도 결과가 갈린다. **FVT 계열(`fvt`/`weighted_fvt`/`family_mean`)이 `random`·`mean`을 사실상 모든 지표에서 앞서고, 우리가 추가한 refinement(`weighted_fvt`·`family_mean`)가 수렴(50K) 시점에 plain `fvt`를 추월**한다. `mean`은 loss·PPPL에서 `random`보다도 나쁘다.

**Table 4. Best-result 요약 (50K, 완료 지표).** 지표별 ablation 최고 method·값, `random` 대비, Glot500-m 참조.

| Metric (group) | dir | best init | best | random | Glot500-m |
| --- | :---: | --- | ---: | ---: | ---: |
| MLM loss (all) | ↓ | **weighted_fvt** | 2.73 | 3.12 | – |
| PPPL (tail) | ↓ | **family_mean** | 12.3 | 20.2 | 7.7 |
| Tatoeba (tail) | ↑ | **family_mean** | 36.1 | 33.4 | 45.7 |
| Roundtrip (tail) | ↑ | **weighted_fvt** | 3.4 | 2.7 | 5.4 |
| NER (tail) | ↑ | **family_mean** | **55.8** | 48.2 | 52.6 |
| Text (head/EN) | ↑ | fvt | 77.4 | 72.6 | 74.3 |
| Bible (tail) | ↑ | (floor) | ~0.9 | 0.8 | 14.7 |

Bible은 floor(§6.4). 전체 상세는 §9.

**세 줄 요약.**
1. refinement(weighted_fvt/family_mean)가 **PPPL·Tatoeba·NER·Roundtrip·loss**에서 최고 — 수렴 시점 우위. 특히 **`family_mean`은 NER(55.8)에서 full Glot500-m(52.6)·XLM-R-L(53.9)까지 능가**한다.
2. `random`/`mean`은 전 지표 하위, `mean`은 loss·PPPL 최악.
3. Bible은 task 난이도로 floor(초기화 무관)라 비교에서 제외.

---

## 6.2 Main result — head/tail/all

### 6.2-a 완료 지표 5-way table (main)

값 = 50K checkpoint. retrieval/roundtrip/text ×100, PPPL raw. 근거: `11_inference/downstream_head_tail_all.tsv`.

| Model / Method | PPPL ↓ | Tatoeba ↑ | Bible ↑ | NER ↑ | Roundtrip ↑ | Text(EN) ↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XLM-R-B (ref) | 98.2 | 20.5 | 0.5 | 45.7 | 2.4 | 59.3 |
| XLM-R-L (ref) | 63.7 | 12.8 | 0.4 | 53.9 | 2.7 | 72.9 |
| Glot500-m (ref) | 7.7 | 45.7 | 14.7 | 52.6 | 5.4 | 74.3 |
| random | 20.2 | 33.4 | 0.8 | 48.2 | 2.7 | 72.6 |
| mean | 23.0 | 33.2 | 0.8 | 49.2 | 2.7 | 68.2 |
| fvt | 16.3 | 34.4 | 0.8 | 51.3 | 3.2 | **77.4** |
| **weighted_fvt** | 13.9 | 35.8 | **0.9** | 50.6 | **3.4** | 74.9 |
| **family_mean** | **12.3** | **36.1** | 0.8 | **55.8** | 3.2 | 74.2 |

**Group 주의(coverage).** 본 실험 지표는 대부분 **tail(target7)** 전용이다: PPPL·Tatoeba·Bible·Roundtrip·NER = tail. **Text = head(English)만**(PBC 부재). 나머지 지표의 head/all은 미측정(NA)이며 이는 설계상 target-focused 평가이기 때문이다.

**해석.** (1) 다섯 초기화 모두 PPPL·Tatoeba·NER에서 XLM-R-B를 크게 능가(NER 48~56 vs 45.7). (2) **`family_mean`이 PPPL·Tatoeba·NER 세 target 지표 모두 최고**이고, **NER(55.8)에서는 full Glot500-m(52.6)·XLM-R-L(53.9)까지 능가** — 50K 축소 모델이 계통 prior만으로 target 개체명 인식에서 baseline을 넘는다. (3) `weighted_fvt`는 Roundtrip 최고, `fvt`는 Text(head) 최고. (4) `random`/`mean`은 전 지표 하위. retrieval/PPPL 절대값이 Glot500-m에 못 미치는 것은 축소 budget(50K vs 480K) 때문이며 관심사는 **초기화 비교**다.

---

## 6.3 Step별 세부 지표 궤적 (경향성)

### 6.3-a MLM loss 수렴 (main figure)

Figure: `Plot/loss/convergence_5way_loss_curve.png`. x=exposure-aligned step(1K grid), y=MLM loss(↓), line=method(색 규약 §plot_table_plan). **50K 최종 loss:** weighted_fvt 2.73 < fvt 2.76 < family_mean 2.91 < random 3.12 < mean 3.27. FVT 계열 최저, mean 최악. 상세 도식 규칙·smoothing disclosure는 §9 A.4.

### 6.3-b 10K→50K downstream 궤적 (crossover)

**Table 5. PPPL·Tatoeba·Roundtrip 궤적(tail).** 전체 step표(Bible·Text·NER 포함)는 §9 A.2.

| Method | PPPL 10K→50K | Tatoeba 10K→50K | Roundtrip 10K→50K |
| --- | ---: | ---: | ---: |
| fvt | 21.2 → 16.3 | 33.9 → 34.4 | 3.02 → 3.22 |
| weighted_fvt | 26.9 → 13.9 | 30.4 → 35.8 | 2.85 → 3.38 |
| family_mean | 34.2 → 12.3 | 30.7 → 36.1 | 2.61 → 3.16 |
| random | 28.4 → 20.2 | 33.0 → 33.4 | 2.61 → 2.67 |
| mean | 32.5 → 23.0 | 31.7 → 33.2 | 2.68 → 2.72 |

**경향성(핵심 novelty).** plain `fvt`는 10K에 이미 최고로 출발하나 **조기 포화**(이후 거의 정체). `weighted_fvt`·`family_mean`은 10K에 더 나쁘게 출발하지만 **계속 개선되어 30~50K에서 fvt를 추월**한다. `random`·`mean`은 전 구간 하위. → "정교한 초기화 prior의 이득은 학습 초반이 아니라 **수렴 구간**에 드러난다." 이 crossover는 §6.3-a loss와 방향 일치. Figure(권장, TO-GEN): PPPL·Tatoeba crossover line plot(§9 A.4).

---

## 6.4 Task별 주의점 (요약)

- **Bible = floor.** 다섯 방법 모두 ~0.8(Glot500-m 14.7)로 붙는다. 원인은 초기화가 아니라 task 난이도(후보 pool ~7–8천 절, 짧고 균질). 초기화 비교엔 무정보. 상세 §9 A.5. → **pivot을 관련 Latin 언어로 바꾸는 추가 실험**(dtp→ind 등)은 별도 spec: `03_retrieval_bible/RELATED_PIVOT_PROMPT.md`.
- **Text = head/EN-only.** target test(PBC) 부재로 English만. 참고용. epoch 분산 큼.
- **PPPL 절대 비교는 지시적.** baseline PPPL(98.2/63.7/7.7)은 pool이 다를 수 있음. retrieval/roundtrip은 고정 eval set이라 직접 비교.

## 6.5 Tokenizer fertility (요약)

확장 tokenizer가 Target7 tokens/word를 2.204 → 1.592로 **−27.75%**. 언어별 12.4~34.9%. Figure `0_tokenizer/03_tokenization_effect/tokenization_effect_change.png`(§9 A.4). **경계:** 모든 초기화가 같은 tokenizer를 쓰므로 method 차이는 fertility로 설명되지 않는다.

## 6.6 Result summary

1. 확장 tokenizer가 fragmentation을 27.75% 줄였다.
2. 50K 수렴 loss는 FVT 계열 최저·mean 최악 → 초기화가 수렴에 지속 영향.
3. downstream(PPPL·Tatoeba·NER·Roundtrip)에서 refinement가 최고이며 **plain FVT를 추월**(crossover). **`family_mean`은 NER에서 Glot500-m까지 능가**.
4. Bible은 floor(task 난이도), Text는 head/EN-only.
