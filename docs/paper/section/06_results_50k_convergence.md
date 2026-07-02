# 06 Results: 50K Convergence Draft

## 목적

50K-step convergence 결과를 중심으로 보고한다. 이 section은 숫자가 들어오면 바로 채울 수 있게 표 구조와 해석 문장을 미리 고정한다.

## 6.1 Tokenizer Fertility

### 현재 숫자

- XLM-R tokenizer target7 tokens/word: 2.204.
- v5.2 extended tokenizer target7 tokens/word: 1.592.
- Average reduction: 27.75%.

### 해석

Tokenizer extension은 target7의 subword fragmentation을 줄였다. 다만 모든 initialization method가 같은 extended tokenizer를 쓰므로, method 간 차이는 tokenizer fertility 때문이 아니라 embedding initialization과 이후 MLM training dynamics에서 온다.

### Figure

- Source: `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/tokenization_effect_change.png`.
- Caption에서 쓸 말: target7에서 tokenization fertility가 감소했으며, tokenizer는 모든 initialization variant에서 고정되어 있다.

## 6.2 50K Five-Way Main Result

### 채울 표

Source schema:

- `docs/exp/v5.2/3_evaluation/09_aggregation/main_head_tail_all.tsv`

Final columns:

| Metric | Group | Score | Random | Mean | FVT | Weighted FVT | Family-aware mean | Best | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PPPL | tail | lower | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| PPPL | head | lower | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| PPPL | all | lower | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| Tatoeba | tail | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| Tatoeba | head | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| Tatoeba | all | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| NER | tail | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| NER | head | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |
| NER | all | higher | TBD | TBD | TBD | TBD | TBD | TBD | n languages |

### 결과 해석 템플릿

50K-step final checkpoint에서 `[METHOD]`는 `[METRIC/GROUP]`에서 가장 좋은 score를 보였다. 이 결과는 early Step-4000 diagnostic의 `[consistent/inconsistent]`한 연장선이다. 다만 `[TASK]`에서는 `[OTHER METHOD]`가 더 높으므로, initialization effect는 task family와 language group에 따라 다르게 나타난다.

## 6.3 Convergence Loss Plot

### Figure

- Source PNG: `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png`.
- Source TSV: `docs/exp/v5.2/2_training/convergence_5way_loss_curve.tsv`.
- Script: `scripts/plot_v52_convergence_loss.py`.

### 제목 설명

Title: `v5.2 MLM Loss Trajectory: Prior Run + Continuation`

이 제목은 figure가 단일 fresh run만 보여주는 것이 아니라 prior diagnostic run과 continuation segment를 연결한 그림임을 밝힌다. 제목에서 continuation 구조를 숨기면 독자가 x축 step을 단순 raw local step으로 오해할 수 있다.

### X-axis 설명

X-axis: `Weighted-FVT-aligned training step (1K grid)`

prior phase와 continuation phase의 effective batch accounting이 다르므로 raw step을 그대로 비교하지 않는다. Plot script는 exposure를 batch-36-equivalent step으로 맞춘 뒤 weighted-FVT 기준 1000-step grid에 snap한다. 따라서 x축은 raw local step이 아니라 exposure-aligned training step이다.

### Y-axis 설명

Y-axis: `MLM training loss`

이 값은 HuggingFace Trainer logging loss이며, convergence diagnosis를 위한 intrinsic signal이다. Downstream score를 직접 의미하지 않으므로 final table과 함께 해석해야 한다.

### Point interval 설명

Point는 1000 aligned steps마다 표시한다. v5.2 convergence queue의 save/log interval이 1000 step이고, PPPL/downstream checkpoint evaluation도 checkpoint 단위로 붙기 때문이다. 더 촘촘한 점을 그리면 실제 saved checkpoint 근거가 없는 중간값처럼 보일 수 있다.

### 왜 50K인가

Step-4000에서는 PPPL 개선이 둔화된 신호가 있었지만 training loss는 계속 감소했으므로 convergence라고 말하기 어렵다. 50K queue는 모든 initialization method를 같은 global exposure 조건에서 충분히 길게 돌려 loss flattening과 downstream trajectory를 확인하기 위한 conservative budget이다. 50K가 반드시 최적 step이라는 뜻은 아니며, final claim을 세우기 위한 충분한 관찰 구간이다.

### Visual elements

- Line: initialization method별 loss trajectory.
- Circle marker: displayed 1K-grid point.
- Square marker: final saved model.
- Color mapping:
  - `random`: gray.
  - `mean`: blue.
  - `FVT`: green.
  - `weighted_fvt`: purple.
  - `family_mean`: red.

### Smoothing disclosure

Graph는 prior/continuation boundary 근처를 읽기 쉽게 하기 위한 plot-only smoothing/bridging을 포함할 수 있다. Raw values는 TSV에 보존되며, 보고서에는 `loss`, `display_loss`, `display_loss_source`가 분리되어 있다고 명시한다.

## 6.4 Step-4000 Early Diagnostic

기존 Step-4000 random/mean/FVT table은 early diagnostic으로 유지한다.

### 해석 문장

Step-4000 diagnostic에서 FVT는 PPPL, retrieval/alignment, sequence labeling 계열에서 강한 초기 신호를 보였다. 그러나 이 표는 convergence result가 아니며, weighted FVT와 family-aware mean이 포함되지 않았으므로 final claim에는 50K five-way result를 사용한다.

