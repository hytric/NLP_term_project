# 09 Appendix

본문(§6)은 best-result와 경향성만 보였다. 여기에는 **전체 원자료(step별·언어별 full table)와 모든 plot, 재현 근거**를 정리한다.

- A.1 완료 50K downstream full table
- A.2 step별 full 궤적 table (모든 지표·모든 method)
- A.3 언어별 breakdown
- A.4 Plot gallery (모든 그림)
- A.5 50K loss / hyperparameters / init audit
- A.6 Artifact & code map
- A.7 Bible floor 상세 + related-pivot 추가 실험
- A.8 Claim boundary checklist

---

## A.1 완료 50K downstream full table

값 = 50K checkpoint. retrieval/roundtrip/text ×100, PPPL raw. Source: `docs/exp/v5.2/3_evaluation/11_inference/downstream_head_tail_all.tsv`.

| Method | PPPL ↓ | Tatoeba ↑ | Bible ↑ | Roundtrip ↑ | Text(EN) ↑ | NER ↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| XLM-R-B | 98.2 | 20.5 | 0.5 | 2.4 | 59.3 | 45.7 |
| XLM-R-L | 63.7 | 12.8 | 0.4 | 2.7 | 72.9 | 53.9 |
| Glot500-m | 7.7 | 45.7 | 14.7 | 5.4 | 74.3 | 52.6 |
| random | 20.2 | 33.4 | 0.8 | 2.7 | 72.6 | 48.2 |
| mean | 23.0 | 33.2 | 0.8 | 2.7 | 68.2 | 49.2 |
| fvt | 16.3 | 34.4 | 0.8 | 3.2 | 77.4 | 51.3 |
| weighted_fvt | 13.9 | 35.8 | 0.9 | 3.4 | 74.9 | 50.6 |
| family_mean | 12.3 | 36.1 | 0.8 | 3.2 | 74.2 | **55.8** |

NER은 5-way 50K 완료(tail=all, target-only).

## A.2 step별 full 궤적 (10K→50K)

### A.2-1 PPPL (tail, ↓)
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 28.43 | 20.95 | 20.36 | 20.20 | 20.17 |
| mean | 32.52 | 23.97 | 23.29 | 23.04 | 23.02 |
| fvt | 21.19 | 16.96 | 16.53 | 16.41 | 16.34 |
| weighted_fvt | 26.86 | 18.56 | 16.09 | 14.66 | 13.89 |
| family_mean | 34.25 | 20.40 | 14.84 | 12.86 | 12.26 |

### A.2-2 Tatoeba (tail, Acc10 ↑)
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.330 | 0.328 | 0.332 | 0.332 | 0.334 |
| mean | 0.317 | 0.330 | 0.328 | 0.330 | 0.332 |
| fvt | 0.339 | 0.344 | 0.343 | 0.343 | 0.344 |
| weighted_fvt | 0.304 | 0.348 | 0.354 | 0.351 | 0.358 |
| family_mean | 0.307 | 0.328 | 0.355 | 0.358 | 0.361 |

### A.2-3 Roundtrip (tail, Acc ↑)
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.0261 | 0.0266 | 0.0269 | 0.0269 | 0.0267 |
| mean | 0.0268 | 0.0268 | 0.0273 | 0.0274 | 0.0272 |
| fvt | 0.0302 | 0.0328 | 0.0324 | 0.0320 | 0.0322 |
| weighted_fvt | 0.0285 | 0.0324 | 0.0333 | 0.0333 | 0.0338 |
| family_mean | 0.0261 | 0.0274 | 0.0309 | 0.0327 | 0.0316 |

### A.2-4 Bible (tail, Acc10 ↑) — floor
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.0076 | 0.0079 | 0.0078 | 0.0079 | 0.0079 |
| mean | 0.0078 | 0.0078 | 0.0076 | 0.0077 | 0.0078 |
| fvt | 0.0078 | 0.0083 | 0.0083 | 0.0083 | 0.0084 |
| weighted_fvt | 0.0073 | 0.0086 | 0.0090 | 0.0083 | 0.0089 |
| family_mean | 0.0062 | 0.0070 | 0.0073 | 0.0071 | 0.0075 |

### A.2-5 NER (tail, F1 ↑) — 5-way 50K 완료
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.447 | 0.466 | 0.464 | 0.470 | 0.482 |
| mean | 0.473 | 0.488 | 0.511 | 0.503 | 0.492 |
| fvt | 0.494 | 0.515 | – | – | 0.513 |
| weighted_fvt | – | – | – | – | 0.506 |
| family_mean | – | – | – | – | **0.558** |

NER F1은 20~30K에서 정점 후 평탄(mean 30K 0.511 정점, fvt 20K 0.515). 50K 최종은 `family_mean` 0.558이 최고로 Glot500-m(0.526)·XLM-R-L(0.539) 능가.

### A.2-6 Text (head/EN, macro-F1 ↑) — 불균등 coverage, 참고용
| Method | 10K | 20K | 30K | 40K | 50K |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.669 | 0.684 | 0.682 | 0.771 | 0.726 |
| mean | 0.787 | 0.682 | 0.719 | 0.788 | 0.682 |
| fvt | 0.724 | 0.797 | – | – | 0.774 |
| weighted_fvt | – | – | – | – | 0.749 |
| family_mean | – | – | – | – | 0.742 |

### A.2-7 MLM loss (all, ↓) — 요약(전체는 TSV)
50K 최종: weighted_fvt 2.7254 · fvt 2.7571 · family_mean 2.9140 · random 3.1150 · mean 3.2716. 전체 1K-grid: `Plot/loss/convergence_5way_loss_curve.tsv`.

## A.3 언어별 breakdown
per-language 점수(Tatoeba 3언어, Bible 3언어, NER 3언어, Roundtrip 3언어). Source: `11_inference/downstream_language_scores.tsv`, `v52_final_downstream_language_breakdown.tsv`. (표는 생성물에서 자동 렌더; 최종본에 삽입.)

## A.4 Plot gallery (모든 그림)

| # | Figure | Source | 설명 |
| --- | --- | --- | --- |
| P1 | Tokenizer fertility bar | `0_tokenizer/03_tokenization_effect/tokenization_effect_change.png` | 언어별 tokens/word 감소(−27.75%) |
| P2 | 5-way MLM loss curve | `Plot/loss/convergence_5way_loss_curve.png` | exposure-aligned step vs loss, 5 method |
| P3 | (TO-GEN) PPPL·Tatoeba crossover | `downstream_head_tail_all.tsv` | 10K–50K refinement 추월 |
| P4 | (TO-GEN) downstream method×metric bar | 〃 | 50K best 시각화 |
| P5 | family pair boxplot | `10_convergence_similarity/fvt/checkpoint-50000/family_similarity/family_pair_boxplot_*.png` | relation별 centered cosine |
| P6 | family centroid heatmap | 〃 `family_centroid_heatmap_*.png` | 언어 centroid 유사도 |
| P7 | 2D embedding map | 〃 `embedding_similarity/embedding_map_2d.png`, `family_point_map_*` | ▲tail/●head, 색=family |
| P8 | (TO-GEN) step별 similarity 궤적 | `similarity_10k50k_summary.tsv` | family 조기형성·평탄, aligned 소폭↑ |

**P2 도식 규칙(상세).** Title `MLM Loss: Prior + Continuation`. x=exposure-aligned step(1K grid, raw 아님). y=HF Trainer MLM loss(↓, intrinsic). ○=1K point, ■=final saved. 색: random `#6f6f6f`·mean `#1f77b4`·fvt `#2ca02c`·weighted_fvt `#9467bd`·family_mean `#d62728`. **Disclosure:** raw `loss`는 TSV 보존, `display_loss`는 prior/continuation 경계 bridge·smoothing 포함 가능("plot-only smoothing" 명시). Why 50K: 4K/8K는 loss 계속 하강 → 수렴 단정 불가, conservative budget.

## A.5 50K loss / hyperparameters / init audit

- **50K 최종 loss**: A.2-7.
- **MLM hyperparameters**: §4.3 (LR 5e-5, Adam 0.9/0.999·ε1e-8, linear/warmup0, wd0, maxlen512, α0.3, ckpt 1000, 50K). effective batch 소스 충돌(96/384/36) 주석.
- **Downstream fine-tune hyperparameters**: §5.6 (NER 10ep·2e-5·bs8×4·maxlen256; Text 30ep·2e-5·bs16; retrieval/roundtrip/PPPL frozen).
- **Init audit**: source len 250,002 · target 366,666 · new rows 116,664 · `<mask>` 250001→366665(diff 0.0) · LM head tied.

## A.6 Artifact & code map

| 단계 | 코드 |
| --- | --- |
| corpus merge + sampling(α0.3) | `preprocessing/merge_files.py`, `merge_files.sh` |
| tokenizer 확장(SPM append) | `tokenization/run.py`, `train_v52_glot5007.sh` |
| init 5-way | `scripts/build_v5_initialized_checkpoint.py`, `4_reporting/v52_initializer_core_code.py` |
| continued MLM | `modeling/run.py`, `train_v52_glot5007_mlm.sh` |
| retrieval/NER/roundtrip/text eval | `evaluation/{retrieval,tagging,round-trip,text_classification}/*` |

| 내용 | 경로 |
| --- | --- |
| 50K downstream | `3_evaluation/11_inference/downstream_head_tail_all.tsv` |
| loss curve+TSV | `Plot/loss/convergence_5way_loss_curve.{png,tsv}` |
| baseline(XLM-R-B/L, Glot500-m) 비교 | `3_evaluation/v52_ppt_current_table.md` |
| similarity 10K–50K·2D map | `3_evaluation/11_inference/similarity_maps/`, `10_convergence_similarity/` |
| fertility | `0_tokenizer/03_tokenization_effect/results_ko.md` |

## A.7 Bible floor 상세 + related-pivot 추가 실험

- **floor 원인**: English pivot, 후보 pool 언어당 ~7–8천 절(Tatoeba의 10배), 짧고 균질한 절 → 우연상한 낮음, 50K로 verse 정밀정렬 미달. 다섯 방법 공통 실패라 초기화 무정보(§6.4).
- **추가 실험 spec**: pivot을 관련 Latin 언어로(dtp→ind, xav→por, bam→fra) 교체해 related-language-help·robustness 확인. 전체 가이드·명령: `docs/exp/v5.2/3_evaluation/03_retrieval_bible/RELATED_PIVOT_PROMPT.md`. skeleton 표: §6.4 참조.

## A.8 Claim boundary checklist

- [ ] 모든 수치가 50K 기준인가(Step-4000 미사용)?
- [ ] 모든 수치에 source artifact가 붙었는가?
- [ ] ↓/↑ metric 방향이 표시됐는가?
- [ ] coverage 없음=`NA`, 미완=`pending`으로 구분했는가?
- [ ] Target7 Latin-script 한계를 명시했는가?
- [ ] 모든 row가 뒷받침할 때만 best claim을 했는가?
- [ ] Bible floor / Text head-only를 격리했는가?
