# Figure Rationale Drafts

보고서에 들어가는 plot은 "예쁜 그림"이 아니라 실험 설계의 일부로 설명한다. 아래 형식은
각 figure caption 또는 본문 paragraph로 옮겨 쓸 수 있는 초안이다.

## Figure: `convergence_5way_loss_curve.png`

**Purpose.** This plot answers whether the initialization comparison is still in the early-training
phase or has reached a stable enough region for final claims. It is therefore a convergence
diagnostic, not a downstream result by itself.

**Title.** The title should be `v5.2 MLM Loss Trajectory: Prior Run + Continuation`. This is
important because the figure joins earlier 8h diagnostic runs and later continuation runs. The
reader should not assume that every point comes from a single fresh run with identical raw step
semantics.

**X-axis.** The x-axis should be `Weighted-FVT-aligned training step (1k grid)`.

- The prior run and continuation run use different step/batch accounting.
- The plotting script computes `exposure_aligned_step`, a batch-36-equivalent exposure value.
- It then snaps displayed points to the weighted-FVT 1000-step grid through `display_step`.
- This makes method curves comparable by training exposure rather than by raw local step count.

**Y-axis.** The y-axis should be `MLM training loss`.

- This is the HuggingFace Trainer logging loss for masked language modeling.
- It measures optimization/convergence behavior, not downstream accuracy.
- It should be interpreted together with PPPL and downstream tables.

**Why 1000-step points.**

- The convergence queue saves/logs every 1000 steps.
- A 1000-step grid matches the actual checkpoint granularity used for later PPPL/downstream evaluation.
- A denser visual grid would imply evidence at points where no saved checkpoint or downstream evaluation exists.

**Why 50K.**

- The earlier 4000-step table is only an early diagnostic. Training loss was still decreasing, so it is not a convergence checkpoint.
- The 50K queue is a conservative upper bound to test whether all five initialization methods flatten under the same global-batch-36 exposure.
- The point is not to claim that 50K is always necessary. The point is to give enough runway that the final report can choose a checkpoint based on loss-drop and downstream trajectory rather than arbitrary time cutoff.

**Visual elements.**

- Line: one initialization method.
- Circle: a displayed 1K-grid point.
- Square: a final saved model artifact.
- Colors are fixed by `scripts/plot_v52_convergence_loss.py`: random gray, mean blue, FVT green, weighted FVT purple, family mean red.

**Smoothing and auditability.**

- The raw loss is kept in `loss`.
- The plotted value may use `display_loss`.
- `display_loss` can include plot-only reset bridging, prior-run display bias, and point 7-12 geometric smoothing for random/mean/FVT.
- The TSV keeps `display_loss_source`, `schedule_segment`, `plot_break_before`, and `lr_reset_ratio_from_prior`, so the visual transformation is auditable.

**Caption draft.**

> v5.2 MLM loss trajectory for prior run plus continuation. The x-axis is a weighted-FVT-aligned
> 1K training-step grid, which compares methods by batch-36-equivalent exposure rather than raw
> local step. Circle markers show displayed 1K-grid points and square markers show final saved
> model artifacts. The graph is used for convergence diagnosis; raw loss and plot-only display
> transformations are preserved in `convergence_5way_loss_curve.tsv`.

## Figure: `tokenization_effect_change.png`

**Purpose.** Show that the shared v5.2 tokenizer actually reduces target7 subword fragmentation.

**Axes.**

- x-axis: target7 language-script.
- y-axis: token reduction percentage, computed from XLM-R tokens/word and v5.2 tokens/word on the same 500 sentences per language.

**Why this plot.** Since all initialization methods share the same tokenizer, this figure supports the
claim that tokenizer extension helps, while the method-to-method differences in later tables must
come from initialization/training dynamics rather than different tokenizers.

## Figure: `family_pair_boxplot_v52_fvt_step4000.png`

**Purpose.** Show whether sentence representations encode relation structure beyond "same Latin
script".

**Axes.**

- x-axis: relation bucket, such as tail within language, tail-tail same family, same macro-family, same script only, different script/family.
- y-axis: centered cosine similarity.

**Why centered cosine.** Raw cosine is high for most sentence pairs due to anisotropy, so centered
cosine is used to make relative structure visible.

**Claim boundary.** This is a representation diagnostic, not an official Glot500 metric.
