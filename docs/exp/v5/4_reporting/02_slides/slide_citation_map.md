# v5 Slide Citation Map

Last updated: 2026-06-28

Use this file when assembling the final PPT or answering defense questions. It
maps each slide to citation support and local evidence. Citations justify
background and method lineage; local artifacts prove v5 results.

| Slide | Claim type | Citation support | Local evidence source | Boundary |
| ---: | --- | --- | --- | --- |
| 1 | title and scope | `imanigooghari-etal-2023-glot500` | `03_final_report/claim_ledger.md`; `03_final_report/paper_draft.md` | controlled subset replay, not full Glot500 |
| 2 | motivation and contribution framing | `imanigooghari-etal-2023-glot500`; `yamaguchi-etal-2026-effectively` | `03_final_report/contribution_summary.md` | citations motivate the problem; v5 contribution claims start from local audits |
| 3 | reproduction boundary | `imanigooghari-etal-2023-glot500`; `glot500-code` | `goal_readiness.md`; `03_final_report/claim_ledger.md` | reproduce pattern, not 511-language scale |
| 4 | target10 design | none required beyond Glot500 data lineage | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`; `Report.md` | target set is local v5 design |
| 5 | corpus construction | `imanigooghari-etal-2023-glot500`; `glot500-code` | `0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`; `table_01_data_scope.md` | local merge report proves v5 counts |
| 6 | tokenizer method | `imanigooghari-etal-2023-glot500`; `yamaguchi-etal-2026-effectively` | tokenizer audit JSON/TSV; `table_02_tokenizer_audit.md` | v5 main tokenizer is Glot500-style append; Yamaguchi is contrast |
| 7 | novelty framing | `yamaguchi-etal-2026-effectively`; `lowres-cve-code` | `contribution_summary.md`; `table_03_initialization_zero_step.md` | novelty is v5 initialization comparison, not a new corpus |
| 8 | initialization audit | none required for measured audit facts | FVT init report | local audit files prove row-copy, mask remap, byte accounting, and LM-head tying |
| 9 | zero-step evidence | `yamaguchi-etal-2026-effectively` for motivation | zero-step summary; `table_03_initialization_zero_step.md`; `method_comparison_summary.md` | zero-step does not imply after-MLM or downstream improvement |
| 10 | training setup | none required for live status | `running_status.md`; `selected_checkpoint_manifest.md`; `table_05_training_status.md` | live steps are progress, not result claims |
| 11 | Glot500 metrics | `imanigooghari-etal-2023-glot500`; `glot500-code` | `metric_mapping.md`; coverage summary; `table_13_metric_fidelity_matrix.md`; `current_result_snapshot.md` | metric-family retention is supported; coverage is local |
| 12 | current measured rows | none required for numeric values | `09_aggregation/`; tables 06-14; `current_result_snapshot.md` | numeric claims come only from parsed artifacts; v5-random is diagnostic until v5-FVT paired rows exist |
| 13 | limitations | `imanigooghari-etal-2023-glot500` for original scale | coverage summary; blocker notes; `claim_ledger.md` | limitations are local execution boundaries |
| 14 | conclusion | citation support inherited from prior slides | `claim_ledger.md`; `result_interpretation_blocks.md` | choose final wording only after v5 rows parse |
| 15 | backup artifacts | `references.bib`; `citation_source_map.md` | `source_map.md`; selected checkpoint manifest; post-checkpoint queue; post-checkpoint execution plan | cite papers for lineage, local files for reproducibility |

## Citation Rules For Slides

- Put citations in small footer text only on slides that discuss background,
  method lineage, or reproduction target.
- Do not cite a paper as proof of a v5 number; use tables, figures, or
  aggregation files for measured values.
- Use `Glot500-style controlled subset replay` on title/boundary slides.
- Use `Yamaguchi-style inspiration/contrast` for the add-token route and
  low-resource vocabulary-expansion motivation.
- Keep `citation_source_map.md` as the paper-level source and this file as the
  slide-level source.
