# 09 Appendix And Artifact Map Draft

## 목적

보고서에 나온 모든 claim이 어느 파일, 코드, artifact에서 왔는지 추적 가능하게 만든다.

## Code Map

| Claim/Step | Artifact |
| --- | --- |
| Tokenizer training | `tokenization/train_v52_glot5007.sh`, `tokenization/run.py` |
| Corpus merge/sampling | `preprocessing/merge_files.py` |
| Initialization methods | `scripts/build_v5_initialized_checkpoint.py` |
| MLM training | `modeling/train_v52_glot5007_mlm.sh`, `modeling/run.py` |
| 50K loss plot | `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png` |
| Loss plot raw values | `docs/exp/v5.2/2_training/convergence_5way_loss_curve.tsv` |
| Step-4000 diagnostic table | `docs/exp/v5.2/3_evaluation/v52_final_downstream_table.tsv` |
| Final head/tail/all schema | `docs/exp/v5.2/3_evaluation/09_aggregation/main_head_tail_all.tsv` |
| Tokenization fertility | `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md` |
| Reference notes | `docs/paper/references.md` |

## Final Submission Checklist

- [ ] 50K checkpoints for all five methods are complete.
- [ ] Evaluation rows are regenerated for `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean`.
- [ ] Final table separates `tail`, `head`, and `all`.
- [ ] Coverage-free cells are marked `NA`.
- [ ] Step-4000 table is labeled early diagnostic.
- [ ] Loss plot caption explains title, axes, 1K point interval, 50K budget, markers, smoothing disclosure.
- [ ] Every table has source file path in notes or caption.
- [ ] PDF builds after updating numeric values.

