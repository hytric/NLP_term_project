# v5 Deck Build Spec

Last updated: 2026-06-28

This file turns `ppt_content.md` into an assembly-oriented PPT checklist.
Use it with `slide_asset_manifest.md`, `slide_citation_map.md`,
`rehearsal_plan_ko.md`, `../03_final_report/result_interpretation_blocks.md`,
`../post_checkpoint_outcome_matrix_ko.md`, and
`../final_claim_decision_tree.md`. Numeric
claims still come from `3_evaluation/09_aggregation/` and
`4_reporting/00_tables/`.

The browser-presentable deck is generated from `final_deck_ko.md`:

```bash
python3 scripts/build_v5_slide_html.py
```

The PowerPoint handoff deck is also generated from `final_deck_ko.md`:

```bash
python3 scripts/build_v5_slide_pptx.py
```

The PDF review deck is generated from the PPTX handoff deck:

```bash
bash scripts/build_v5_slide_pdf.sh
```

Output:

```text
docs/exp/v5/4_reporting/02_slides/v5_final_deck_ko.html
docs/exp/v5/4_reporting/02_slides/v5_final_deck_ko.pptx
docs/exp/v5/4_reporting/02_slides/v5_final_deck_ko.pdf
```

## Deck Rule

The deck should feel like an experiment report, not a proposal deck.
Use measured values, explicit gates, and blocked-data notes. Do not use live
training steps as result claims.

## Slide Specs

| Slide | Layout | Primary content | Visual/source | Speaker emphasis | Final gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | title | Controlled 102-language Glot500-style replay with vocabulary-extension initialization | title only | Scope is controlled subset, not full Glot500 | scope unchanged |
| 2 | compact motivation + contribution triad | uneven multilingual coverage; 92+10 replay; FVT initialization; metric-family fidelity | report contribution summary | Problem, contribution, and claim gate are introduced together | none |
| 3 | compact comparison | Glot500 full scale vs v5 controlled replay | table_15 fidelity matrix | We keep experimental logic, not 511-language scale | boundary wording locked |
| 4 | compact target summary | target10 codes, region/script diversity, row threshold | `glot50010_selected_manifest.tsv` | Targets are Glot500-internal and diverse | target set unchanged |
| 5 | corpus snapshot | 92 seen, 10 target, 92,452,251 merged lines, 0 missing dirs | `table_01_data_scope.md` | Data scope is frozen and reproducible | merge unchanged |
| 6 | figure + caveat | tokenizer fertility improvement and `dzo_Tibt` regression | `figure_02_tokenizer_fertility_delta.png` | 29/30 improves; failure case stays visible | tokenizer unchanged |
| 7 | method bullets | random, mean, FVT, align roles | initialization audit reports | Novelty is initialization of appended rows | none |
| 8 | correctness audit | identity copy, `<mask>`, byte rows, LM head | FVT init report | Correctness gates protect the comparison | none |
| 9 | zero-step evidence | random/mean/FVT target weighted NLL and intrinsic-only caveat | `figure_03_zero_step_initialization.png`; `table_03_initialization_zero_step.md` | FVT zero-step target NLL is strongly lower | matched PPPL rows |
| 10 | training status | paired 10K random -> FVT run; checkpoint selection rule | `table_05_training_status.md`; `running_status.md` | This is progress, not a result row | matched checkpoints |
| 11 | metric-family coverage/status | all Glot500 metric families retained; coverage boundaries | `figure_05_evaluation_coverage.png`; `current_result_snapshot.md` | Missing coverage is reported, not hidden | coverage changes |
| 12 | current measured rows | PPPL/Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip baseline/reference rows plus v5-random diagnostic rows; v5-FVT rows gated | `current_result_snapshot.md`; tables 06-14 | Baseline/reference and v5-random rows measured; FVT method rows wait | paired v5-FVT outputs parsed |
| 13 | limitations | target10 downstream coverage, Bible/Roundtrip v5 checkpoint gaps, external Glot500-base | coverage/blocker tables | Limitations are part of fidelity | blockers change |
| 14 | conclusion | setup fidelity + zero-step novelty + remaining method gate | `claim_ledger.md`; `result_interpretation_blocks.md` Korean final conclusion choices; `post_checkpoint_outcome_matrix_ko.md`; `final_claim_decision_tree.md` | Current-safe conclusion only | decision tree selects final outcome block |
| 15 | backup artifacts | commands, paths, audits, post-checkpoint runner | `source_map.md`; `post_checkpoint_eval_queue.md`; `post_checkpoint_execution_plan.md` | Everything is traceable to files | add final logs |

## Build Artifacts

| Artifact | Source | Purpose | Final gate |
| --- | --- | --- | --- |
| `final_deck_ko.md` | manually maintained slide source | canonical slide text and claim boundaries | update after result insertion |
| `v5_final_deck_ko.html` | `scripts/build_v5_slide_html.py` from `final_deck_ko.md` | browser-based rehearsal/presentation deck with keyboard navigation | regenerate after slide source changes |
| `v5_final_deck_ko.pptx` | `scripts/build_v5_slide_pptx.py` from `final_deck_ko.md` | actual PowerPoint handoff deck generated without extra Python dependencies | regenerate after slide source changes |
| `v5_final_deck_ko.pdf` | `scripts/build_v5_slide_pdf.sh` from `v5_final_deck_ko.pptx` | shareable/reviewable deck export | regenerate after slide source changes |
| `presenter_script_ko.md` | slide content and talk track | spoken presentation script | update after slide 11/12/14 changes |

## Must-Show Numbers

| Claim | Number | Source |
| --- | ---: | --- |
| merged corpus lines | 92,452,251 | `table_01_data_scope.md` |
| extended HF tokens | 368,687 | `table_02_tokenizer_audit.md` |
| appended token strings | 118,685 | `table_02_tokenizer_audit.md` |
| tokenizer audit improved | 29/30 | `table_02_tokenizer_audit.md` |
| target10 improved | 9/10 | `table_02_tokenizer_audit.md` |
| `dzo_Tibt` source -> v5 tokens/word | 4.223938 -> 5.552124 | `table_02_tokenizer_audit.md` |
| zero-step target NLL random | 18.411756 | `table_03_initialization_zero_step.md` |
| zero-step target NLL FVT | 8.785518 | `table_03_initialization_zero_step.md` |
| FVT - random target NLL | -9.626238 | `table_03_initialization_zero_step.md` |
| XLM-R target PPPL | 61.980216 | `table_06_pppl_partial.md` |
| Glot500-base target PPPL | 15.102934 | `table_06_pppl_partial.md` |
| v5-random target PPPL | 39.222875 | `table_06_pppl_partial.md` |
| v5-random Tatoeba all Top-10 | 0.610353 | `table_07_tatoeba_partial.md` |
| XLM-R Bible Top-10 | 0.381153 | `table_12_bible_partial.md` |
| Glot500-base Bible Top-10 | 0.509356 | `table_12_bible_partial.md` |
| v5-random Bible Top-10 | 0.328019 | `table_12_bible_partial.md` |
| XLM-R Roundtrip accuracy | 0.185300 | `table_14_roundtrip_partial.md` |
| Glot500-base Roundtrip accuracy | 0.205189 | `table_14_roundtrip_partial.md` |
| v5-random Roundtrip accuracy | 0.190300 | `table_14_roundtrip_partial.md` |
| Glot500-base NER all F1 | 0.627108 | `table_10_ner_partial.md` |
| Glot500-base POS all F1 | 0.567542 | `table_11_pos_partial.md` |

## Do Not Put On Slides

- Full 511-language reproduction claim.
- Target10 downstream improvement claim.
- FVT after-MLM or downstream improvement before matched checkpoints are parsed.
- Glot500-base as an equal-budget baseline.
- Live training step as a result row.
- NER/POS dev F1 as final tagging result.
- Citations as proof of local v5 numbers; cite papers for background/method
  lineage and use local artifacts for results.

## Post-Checkpoint Slide Update

After `v5_random` and `v5_fvt` are `ready_for_wrapper=yes` and
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
```

Use split phases only when staging long jobs:

```bash
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream
```

Then update in this order:

1. `2_training/05_checkpoint_selection/selected_checkpoint_manifest.md`
2. `00_tables/table_06_pppl_partial.md`
3. relevant downstream tables 07, 08, 10, 11, 12
4. `00_tables/table_13_metric_fidelity_matrix.md` if coverage or blocker status changed
5. `01_figures/generated/figure_manifest.tsv` and `captions.md` if figure sources changed
6. `final_claim_decision_tree.md` to select the slide 14 outcome wording,
   `post_checkpoint_outcome_matrix_ko.md` to confirm the outcome family, and
   `result_interpretation_blocks.md` `Korean Final Conclusion Choices` to copy
   the matching Korean line
7. `ppt_content.md` slides 11-14
8. `presenter_script_ko.md`
9. `slide_claim_checklist.md`
10. `slide_asset_manifest.md`
11. `slide_citation_map.md` if slide citation boundaries changed
12. `report_slide_crosswalk.md`
