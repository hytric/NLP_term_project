# Plot & Table Framework (per-section)

각 섹션(§00–§09) 위치별로 **어떤 표/그림이 들어가고, source·구성·caption·해석·claim 경계**가 무엇인지 정리한 틀이다. 모든 수치는 50K 기준(Step-4000 미사용). 표기: `[T]`=table, `[F]`=figure, `TO-GEN`=아직 생성 필요.

## 도식 규칙 (모든 figure 공통)

caption/본문은 최소한 다음에 답한다: (1) 무슨 실험 단계·비교 대상인가 (2) x축 단위(raw/exposure-aligned step, language, relation bucket) (3) y축 metric과 방향(↓/↑) (4) point/marker/color/box 의미 (5) 왜 이 step range인가 (6) 무엇을 주장하면 안 되는가(diagnostic vs final, coverage 한계).

색 규약(로스·궤적 공통, `scripts/plot_v52_convergence_loss.py`): random `#6f6f6f` · mean `#1f77b4` · fvt `#2ca02c` · weighted_fvt `#9467bd` · family_mean `#d62728`.

---

## §0 Abstract
- 표/그림 없음. 3대 관찰(fertility 27.75%↓, 50K loss FVT계열 최저·mean 최악, refinement가 plain FVT 추월)만 텍스트로.

## §1 Introduction
- `[F1] TO-GEN (optional)` **초기화 5방법 스펙트럼 도식**: 한 줄 위에 random→mean→FVT→weighted_FVT→family_mean을 "정보량↑" 축으로 배치. 개념 그림(손/matplotlib). 목적: 비교 축을 한눈에. 주장금지: 성능순서 아님(정보량/가정 순서일 뿐).

## §2 Related Work
- `[T2-1]` **Glot500 Table 3 참조**: task | head | tail | measure (Tatoeba 70/28/Top10, Bible 94/275/Top10, Text 90/264/F1, NER 89/75/F1, POS 63/28/F1, Roundtrip 85/288/Acc). Source: `docs/survey/2305.12182v2.pdf` Table 3. 용도: 우리 프로토콜이 Glot500과 동일함을 명시.
- `[T2-2]` **평가 프로토콜·레퍼런스 매핑**: task | dataset | fine-tune 여부 | metric | 인용. (§2.5 본문 표로 대체 가능.)

## §3 Data and Scope
- `[T1] Target7` (핵심): language_script | full name | family | region | new_length | Covered tasks. Source: `0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv`. Caption: "XLM-R-unseen tail 7개, 모두 Latn". 주장금지: script diversity 대표 아님.
- `[T2] Task coverage` (피드백 핵심): task | target 3언어 | 평가 규모 | 해석. Source: `1_data_scope/low_resource_task_fill_candidates.tsv`. 용도: "왜 이 언어, task별 3개" 정당화.
- `[T3] Corpus/sampling stats` (inline): source raw / MLM train total / seen / target7 / α=0.3 / scale. Source: `0_tokenizer/merge/*.report.json`, `v52_ppt_current_table.md`.

## §4 Method
- `[T4] 초기화 5방법 정의`: Method | 정의 | 직관/위치(hypothesis). Source: `scripts/build_v5_initialized_checkpoint.py`. (현재 §4.2 Table 3.)
- `[T5] Tokenizer 설정`: setting | value | 이유 (unigram/byte_fallback/char_coverage/input_sentence_size).
- `[T6] MLM hyperparameters`: base/objective/LR/Adam/schedule/wd/maxlen/α/batch/checkpoint/budget (§4.3). ⚠ effective batch 소스 충돌(96/384/36) 주석 유지.
- `[F2] TO-GEN (optional)` **FVT decomposition 개념도**: 새 token "＿bambara" → source XLM-R로 [▁bam][bara] 분해 → 두 subtoken embedding 평균 = 새 row 초기값. 목적: FVT 직관 시각화.

## §5 Experiment Protocol
- `[T7] 평가항목 요약`: 평가 항목 | 무엇을 평가 | 해석(↓/↑) (7 tasks). (현재 §5.4 개요 표.)
- `[T8] Downstream fine-tuning/eval 하이퍼파라미터` (핵심): task | fine-tune | epochs | LR | batch(eff) | max len | optimizer/schedule | metric. (현재 §5.6.) 주석: Glot500 recipe 일치(LR 2e-5, Text batch 16).
- `[F3] TO-GEN (강추)` **Zero-shot transfer 흐름도**: English 문장→공유 tokenizer→공유 encoder→[task head 학습]  ‖  tail 문장→같은 encoder→같은 head(고정)→예측. 목적: "English와 tail이 공유 표현으로 연결"을 시각화(질문 대응). 주장금지: head가 번역하는 것 아님.

## §6 Results

### 6.1 Tokenizer fertility
- `[F4] 언어별 fertility 감소 bar`. Source: `0_tokenizer/03_tokenization_effect/tokenization_effect_change.png`. x=7 target 언어, y=tokens/word(XLM-R vs v5.2) 또는 reduction%. Caption: 평균 2.204→1.592(−27.75%). 주장금지: fertility가 method 차이를 설명하지 않음(tokenizer 공유).
- `[T9] fertility 표`: scope/언어 | XLM-R tok/word | v5.2 tok/word | reduction%.

### 6.2 50K convergence loss (main figure)
- `[F5] 5-way loss curve` (핵심). Source: `Plot/loss/convergence_5way_loss_curve.png` (raw `.tsv`). x=exposure-aligned step(1K grid), y=MLM training loss(↓). line=method, ○=1K point, ■=final. 상세 caption은 아래 "F5 상세" 참조.
- `[T10] 50K 최종 loss 순위`: method | 최종 loss | 순위 (weighted_fvt 2.73 … mean 3.27).

### 6.3 50K five-way downstream (main table)
- `[T11] 50K downstream 비교` (가장 중요): model/method(baseline 3 + init 5) × {PPPL↓, Tatoeba↑, Bible↑, Roundtrip↑, Text(EN)↑}. 열별 best 굵게. Source: `11_inference/downstream_head_tail_all.tsv`. 주석: Text head/EN-only, Bible floor, PPPL baseline pool 주의.
- `[T12] NER`: 5-way 50K 완료(family_mean 55.8 최고, Glot500-m 능가) + baseline. POS는 미보고.
- `[F6] TO-GEN (optional)` **downstream bar (method×metric)**: PPPL/Tatoeba/Roundtrip를 method별 그룹 bar로. baseline은 점선 reference. 목적: 표를 시각화.

### 6.4 10K→50K 궤적 (crossover, 핵심 novelty)
- `[T13] 궤적 표`: method × {PPPL 10/30/50K, Tatoeba 10/30/50K}. (현재 Table 6.)
- `[F7] TO-GEN (강추)` **궤적 line plot**: 좌 y=PPPL(↓)·우 y=Tatoeba(↑), x=step 10K–50K, 5 line(색 규약). 강조: fvt 조기 포화 vs weighted_fvt/family_mean 지속 개선·추월(crossover 지점 표시). Source data: `downstream_head_tail_all.tsv`(step별). 목적: "정교한 prior 이득은 수렴 구간에 드러남"을 한 장으로.

## §7 Representation Analysis
- `[T14] relation bucket similarity (50K)`: relation type | pairs | mean centered cosine(단조감소). Source: `11_inference/similarity_maps/similarity_10k50k_summary.tsv`(fvt step50000).
- `[F8] family pair boxplot`. Source: `10_convergence_similarity/fvt/checkpoint-50000/family_similarity/family_pair_boxplot_*.png`(없으면 09_family_similarity step4000). x=relation bucket, y=centered cosine. 주장금지: raw cosine 아님(anisotropy).
- `[F9] family centroid heatmap`. Source: 같은 폴더 `family_centroid_heatmap_*.png`. 언어 centroid 간 유사도 matrix.
- `[F10] 2D embedding map` (피드백 유지): Source: `10_convergence_similarity/fvt/checkpoint-50000/embedding_similarity/embedding_map_2d.png` 또는 `family_point_map_*`. ▲=tail, ●=head, 색=family. 해석: 계통 clustering·잘분리 tail(dtp/bam/xav)·겹침 tail(csb/fur/ile/lij). 주장금지: 완전 분리 아님, 2D distortion.
- `[F11] TO-GEN (optional)` **step별 similarity 궤적**: x=10K–50K, y=centered cosine, line=relation bucket(within-lang/same-family/…) + aligned-pair. 강조: family 구조 조기형성·평탄, aligned(src-eng)만 40K까지 소폭↑. 목적: §7.3 정직한 관찰 시각화.
- `[T15] best-model 종합`: 관점(MLM loss/target PPPL/Tatoeba/Roundtrip/NER) | 최고 method | 2위. (현재 §7.5.)

## §8 Discussion/Limitations/Conclusion
- 표/그림 없음.

## §9 Appendix
- `[TA1] Initialization audit`: source/target len, new rows, mask remap, lm-head tied.
- `[TA2] Artifact/code map`: pipeline·result 경로.
- `[TA3] 언어별 breakdown`: Tatoeba/NER/Roundtrip per-language. Source: `11_inference/downstream_language_scores.tsv`, `v52_final_downstream_language_breakdown.tsv`.
- `[TA4] 완성 5-way downstream`: NER 포함 최종본(POS 제외).

---

## F5 상세 (5-way loss curve)
- **Title** `v5.2 MLM Loss Trajectory: Prior Run + Continuation` — 단일 fresh run이 아니라 prior 8h run + continuation을 이어붙였음을 명시.
- **X** `Exposure-aligned training step (1K grid)` — prior/continuation의 effective batch 회계가 달라 raw step 아님; exposure를 batch-equivalent step으로 맞춰 1K grid에 snap.
- **Y** `MLM training loss` (↓) — HF Trainer logging loss, intrinsic 신호. downstream을 직접 의미하지 않으므로 표와 함께 해석.
- **Points** 1K 간격 = save/log/eval granularity. 더 촘촘하면 근거 없는 중간값처럼 보임.
- **Why 50K** 4K/8K는 loss가 계속 내려가 수렴 단정 불가 → 동일 exposure로 충분히 길게 돌린 conservative budget. 50K가 "필수 step"은 아님.
- **Elements** line=method, ○=1K point, ■=final saved. 색=색 규약.
- **Disclosure** raw `loss`는 TSV에 보존; `display_loss`는 prior/continuation 경계 bridge·smoothing 포함 가능 → "plot-only smoothing, raw preserved" 명시.

## 생성 대기(TO-GEN) 요약
| ID | 그림 | source data | 우선순위 |
| --- | --- | --- | --- |
| F7 | 10K–50K PPPL·Tatoeba crossover line | `downstream_head_tail_all.tsv` | 높음(novelty) |
| F3 | zero-shot transfer 흐름도 | 개념도 | 높음(설명력) |
| F11 | step별 similarity 궤적 | `similarity_10k50k_summary.tsv` | 중 |
| F6 | downstream method×metric bar | `downstream_head_tail_all.tsv` | 중 |
| F1/F2 | init 스펙트럼·FVT 분해 개념도 | 개념도 | 낮음(optional) |

## 최종 제출 전 남은 일
1. (완료) NER 5-way 50K 반영. POS는 미보고(제외).
2. `[F7]`(crossover) 생성 — 본 보고서 novelty를 가장 잘 보여주는 그림.
3. 50K geometry 그림(F8–F10)을 checkpoint-50000 산출물로 교체(없으면 step4000 유지 + 라벨).
4. PPPL split 문구: diagnostic PPPL을 Glot500 held-out으로 부르지 않기.
