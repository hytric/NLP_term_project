# Plot and Table Plan for Term Report

이 문서는 `docs/paper/tex/main.tex`에 넣을 표/그림과 claim boundary를 따로 정리한 것이다.

## Feedback 반영 체크

| Feedback | 반영 위치 | 상태 |
| --- | --- | --- |
| 제목을 XLM 기반으로 변경 | `tex/main.tex` title | 반영 |
| initialization 방법론 비교 및 수렴 정도 비교 | `sections/04_method.tex`, `sections/06_results.tex`, `convergence_5way_loss_curve.png` | 초안 반영 |
| downstream task 정당성 확보 | `sections/03_data.tex`, `tables/table_task_coverage.tex` | 반영 |
| 언어 선택 이유 명시 | `sections/03_data.tex`, `tables/table_target7.tex` | 반영 |
| task별 3개 언어 table | `tables/table_task_coverage.tex` | 반영 |
| training sampling strategy 확인 | `sections/03_data.tex`, `preprocessing/merge_files.py` 근거 | 반영 |
| embedding initialization 2개 추가 | `tables/table_initialization_methods.tex`에 weighted FVT, family-aware mean 포함 | 반영, numeric main table은 50K five-way |
| head/tail/all 최종 table | `tables/table_head_tail_all_draft.tex` | draft grid 작성, 최종값 갱신 필요 |
| 4K-step 이하 PPPL 감소 추세 | `tables/table_pppl_trajectory.tex` | 반영 |
| 실제 loss graph 추가 | `sections/06_results.tex`, `convergence_5way_loss_curve.png` | 반영 |
| sentence representation space 설명 | `sections/07_analysis.tex` | 반영 |
| step별 clustering 변화 plot | `figure_rationale.md`에 설명 기준 작성, plot artifact 확정 후 본문 삽입 | 대기 |
| 38개 언어 subset 2D PCA 유지 | `sections/07_analysis.tex`, family map figure | 반영 |

## Tables

| Table | Source | Current file |
| --- | --- | --- |
| Glot500 original head/tail/all baseline | `docs/survey/2305.12182v2.pdf`, Table 4 | `tex/tables/table_glot500_reference.tex` |
| Target7 selection | `docs/exp/v5.2/0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv` | `tex/tables/table_target7.tex` |
| Task coverage / target language justification | `docs/exp/v5.2/1_data_scope/low_resource_task_fill_candidates_ko.md` | `tex/tables/table_task_coverage.tex` |
| Initialization methods | `scripts/build_v5_initialized_checkpoint.py` | `tex/tables/table_initialization_methods.tex` |
| Step-4000 random/mean/FVT early diagnostic | `docs/exp/v5.2/3_evaluation/v52_final_downstream_table.tsv` | `tex/tables/table_ablation_results.tex` |
| PPPL trajectory | `docs/exp/v5.2/3_evaluation/v52_checkpoint_score_table.tsv` | `tex/tables/table_pppl_trajectory.tex` |
| Final 50K five-way head/tail/all grid | `docs/exp/v5.2/3_evaluation/09_aggregation/main_head_tail_all.tsv` regenerated after 50K evaluation | `tex/tables/table_head_tail_all_draft.tex` |
| Reproducibility map | codebase paths | `tex/tables/table_repro_map.tex` |

## Figures

| Figure | Source file | Use |
| --- | --- | --- |
| Tokenization fertility reduction | `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/tokenization_effect_change.png` | Shows tokenizer extension reduces target fragmentation |
| 5-way convergence loss curve | `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png` | Shows training loss by initialization method |
| Family pair boxplot | `docs/exp/v5.2/3_evaluation/09_family_similarity/family_pair_boxplot_v52_fvt_step4000.png` | Shows relation-type similarity ordering |
| Family centroid map | `docs/exp/v5.2/3_evaluation/09_family_similarity/family_centroid_map_v52_fvt_step4000.png` | Shows language/family geometry |
| Novelty summary | `docs/exp/v5.2/4_reporting/v52_novelty_summary.png` | Optional summary figure for final version |

## Figure Explanation Standard

각 plot은 본문 또는 caption에서 최소한 아래 질문에 답해야 한다.

| Question | Required answer |
| --- | --- |
| Why this title? | 제목이 어떤 실험 단계와 비교 대상을 가리키는지 설명한다. |
| Why this x-axis? | x축 단위가 raw step, aligned step, epoch, language, metric 중 무엇이며 왜 선택했는지 설명한다. |
| Why this y-axis? | y축 metric이 무엇을 측정하고, 낮을수록/높을수록 좋은지 설명한다. |
| Why these points? | checkpoint/save/eval 간격, sampling 간격, smoothing 여부를 설명한다. |
| Why this time/step range? | 4K, 8K, 20K, 50K 등 cutoff가 실험 판단에서 어떤 의미인지 설명한다. |
| What does each visual element mean? | color, marker, line, error bar, boxplot bucket, highlighted language를 설명한다. |
| What should not be claimed? | diagnostic plot인지 final metric인지, coverage limitation이 있는지 명시한다. |

## Detailed Example: `convergence_5way_loss_curve.png`

**Title:** `v5.2 MLM Loss Trajectory: Prior Run + Continuation`

- 제목에 `Prior Run + Continuation`을 넣는 이유는 이 그림이 하나의 fresh run만 그린 것이 아니기 때문이다.
- `random`, `mean`, `fvt`는 이전 8h run checkpoint에서 이어붙인 continuation segment가 있고, plot script는 prior run의 `trainer_state.json` loss log를 읽어 continuation과 같은 grid에 맞춘다.
- 따라서 제목에서 continuation 구조를 숨기면 독자가 step을 단순 raw local step으로 오해할 수 있다.

**X-axis:** `Weighted-FVT-aligned training step (1k grid)`

- prior phase와 continuation phase의 effective batch accounting이 다르다.
- plot script는 `exposure_aligned_step`으로 effective examples를 batch-36-equivalent step으로 바꾼다.
- 그 다음 `display_step`을 weighted-FVT 기준 1000-step grid에 snap한다.
- 그래서 x축은 raw local step이 아니라 exposure-aligned step이다.

**Y-axis:** `MLM training loss`

- y값은 HuggingFace Trainer가 logging한 MLM training loss다.
- 이 값은 수렴성 판단을 위한 intrinsic signal이다.
- downstream 성능을 직접 의미하지 않으므로 final claim에서는 PPPL/downstream table과 함께 해석해야 한다.

**Why 1000-step points?**

- v5.2 convergence queue의 save/log interval이 1000 step이다.
- downstream과 PPPL checkpoint evaluation도 checkpoint 단위로 붙기 때문에 1000-step grid가 가장 추적 가능하다.
- 더 촘촘한 점을 그리면 logging noise가 늘고, 실제 saved checkpoint/evaluation 근거가 없는 중간값처럼 보일 수 있다.

**Why 50K?**

- 4000-step table은 early diagnostic으로만 쓴다. `docs/exp/v5.2/4_reporting/convergence_recommendation_ko.md`는 4000 step에서 PPPL 개선이 둔화됐지만 training loss는 계속 내려가므로 convergence로 볼 수 없다고 적는다.
- 8K/12K도 loss가 계속 내려가면 final performance claim을 유보해야 한다.
- 그래서 50K queue는 모든 initialization method를 같은 global batch 36 조건에서 충분히 길게 돌려 flattening 여부를 확인하기 위한 conservative upper bound다.
- 50K가 “반드시 필요한 step”이라는 뜻은 아니고, loss-drop summary가 안정적으로 plateau를 보이면 final report는 그 이전 checkpoint를 선택할 수 있다.

**Visual elements**

- Line: initialization method별 loss trajectory.
- Circle marker: displayed 1K-grid point.
- Square marker: final saved model.
- Colors from `scripts/plot_v52_convergence_loss.py`:
  - random `#6f6f6f`
  - mean `#1f77b4`
  - fvt `#2ca02c`
  - weighted_fvt `#9467bd`
  - family_mean `#d62728`

**Important disclosure**

- 이 plot은 raw loss와 display loss가 구분된다.
- Raw `loss`는 `docs/exp/v5.2/2_training/convergence_5way_loss_curve.tsv`에 보존된다.
- `display_loss`는 prior/continuation boundary를 보기 좋게 잇기 위한 plot-only reset bridge, prior bias, random/mean/FVT point 7-12 smoothing을 포함할 수 있다.
- 보고서에는 반드시 “plot-only smoothing이며 raw values are preserved”라고 적는다.

## Remaining Work Before Final Submission

1. Regenerate the 50K five-way aggregation after all convergence/evaluation jobs are complete.
2. Fill `head`, `tail`, and `all` final reporting table from the regenerated `main_head_tail_all.tsv` schema.
3. Keep `random`, `mean`, `fvt`, `weighted_fvt`, and `family_mean` as main rows; move only unsupported diagnostic analyses to the appendix.
4. Add step-by-step representation trajectory plots if `scripts/plot_v52_embedding_manifold_trajectory.py` outputs are finalized.
5. Verify PPPL split wording: do not call diagnostic PPPL a Glot500 held-out test unless strict held-out files are used.
