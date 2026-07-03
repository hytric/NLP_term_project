# 08 Discussion, Limitations, Conclusion

## 8.1 Discussion

이 프로젝트의 강점은 큰 주장보다 **통제의 엄격함**에 있다. tokenizer·corpus·objective·evaluation을 고정하고 initialization만 바꿨으므로, 관찰된 차이를 initialization과 training dynamics의 상호작용으로 귀속할 수 있다.

1. **Tokenizer extension ≠ downstream 보장.** 확장 tokenizer는 fragmentation을 확실히 줄이지만(§6.1), 같은 tokenizer를 쓰는 초기화 variant 사이에서도 loss·downstream 차이가 유지된다(§6.2–6.3). 따라서 novelty는 tokenizer 확장 자체가 아니라 **확장된 vocabulary row를 어떻게 초기화하느냐**에 있다.
2. **왜 FVT 계열이 이기는가.** FVT는 새 token을 source subtoken 조합으로 설명하여 형태·철자 정보를 재사용한다. 이는 random의 무정보 시작이나 mean의 단일 centroid보다 언어적으로 의미 있는 출발점을 준다. 50K loss(§6.2)와 target PPPL·Tatoeba(§6.3)가 같은 방향을 가리키므로, 이 이득은 초기 우연이 아니라 수렴까지 지속된다.
3. **왜 refinement가 plain FVT를 추월하는가(핵심).** plain `fvt`는 균등 subtoken 평균이라 좋은 출발점을 주지만 표현력이 제한돼 조기 포화한다. `weighted_fvt`(길이 가중)와 `family_mean`(계통 prior)은 10K엔 더 나쁘지만 수렴 구간에서 계속 개선돼 50K에 추월한다(§6.4). 즉 정교한 prior의 이득은 학습 초반이 아니라 **수렴 시점**에 드러난다 — 짧은 진단만으로 초기화를 평가하면 잘못된 결론에 이를 수 있다는 함의를 준다.
4. **왜 mean이 최악인가.** mean은 모든 새 token을 embedding 중심 한 점 근처에서 출발시켜, 서로 다른 token을 구분하는 초기 분리를 오히려 방해한다. 결과적으로 random보다도 나쁘다(§6.2). "안정적 centroid"라는 직관이 여기서는 통하지 않는다.
5. **Family prior의 위치.** `family_mean`은 target PPPL·Tatoeba·NER에서 최고이고 NER에선 full Glot500-m까지 능가하지만, 전체 corpus loss는 3위다(§6.2–6.3). 계통 prior가 **target 언어에 특화**되나 head 일반화에는 덜 유리하다는 해석과 일치한다.
6. **PPPL과 downstream의 관계.** 초기화 순위는 PPPL과 retrieval에서 대체로 일관되지만(FVT 계열 상위), Bible은 floor라 무정보하고 Text(head/EN)는 분산이 커 방향이 다르다. intrinsic MLM fit 개선이 모든 downstream으로 선형 전이되지는 않는다.

## 8.2 Limitations

- **Script 편중.** Target7은 모두 Latin script라 script diversity 결론을 내릴 수 없다.
- **Coverage 불균형.** task마다 target coverage가 다르다. NER은 언어당 100문장 subset, Bible retrieval은 50K에서도 ~0.8로 floor(§6.3), Text classification은 target test set이 없어 English/head-only다.
- **Downstream coverage subset.** 본 보고서는 PPPL·Tatoeba·Bible·Roundtrip·Text·NER과 수렴 loss로 보고한다. 계산 비용이 큰 일부 sequence-labeling 평가는 5개 초기화 전부에 대해 완주하지 못해 제외했으며, 이는 방법론 문제가 아니라 compute/time 제약이다(future work).
- **수렴 단정 불가.** 50K에서 loss는 평탄화됐으나 완전 수렴이라 단정하지 않는다. 절대 성능은 full-scale Glot500(예: PPPL 7.7, Tatoeba 45.7)에 못 미친다(50K vs 480K, 축소 budget 한계). 본 실험의 관심사는 초기화 방법 사이의 비교다.
- **Local variants.** `weighted_fvt`, `family_mean`은 표준 방법이 아니라 이 실험의 local variant다.
- **Seed variance.** 단일 run 설정이라 seed 분산은 충분히 평가되지 않았다.

## 8.3 Conclusion

본 보고서는 `xlm-roberta-base`에 Glot500-style vocabulary extension을 적용하고, 새 vocabulary embedding row 초기화를 다섯 방법으로 50K-step까지 통제 비교했다. (1) 확장 tokenizer는 Target7 fragmentation을 27.75% 줄였다. (2) 같은 tokenizer·corpus 위에서도 초기화에 따라 50K 수렴 loss가 갈렸으며, FVT 계열이 가장 낮고 mean이 random보다도 높았다. (3) 50K downstream에서 우리가 추가한 refinement(`weighted_fvt`, `family_mean`)가 target PPPL·Tatoeba·NER·Roundtrip에서 최고였고 — `family_mean`은 NER에서 full Glot500-m까지 능가했다 — 학습 초반 앞서던 plain FVT를 수렴 구간에서 추월했다. (4) 문장 표현 공간에서는 script보다 language/family 구조가 더 강하게 나타났으며, 이 구조는 학습 조기에 형성되어 이후 평탄했다.

결론은 controlled setup 안으로 제한한다: **low-resource vocabulary adaptation에서 embedding initialization은 흔히 임의로 정해지지만, 통제된 조건에서도 50K 수렴과 평가 지표를 실제로 바꾼다. source subtoken을 재사용하는 FVT 계열이 random·mean보다 지속적으로 유리하며, 그중 이를 정교화한 `weighted_fvt`가 종합적으로 가장 균형 잡힌 선택이다.** 향후 과제는 더 넓은 script/language coverage, 다중 seed, 그리고 target 언어 downstream coverage 확대다.
