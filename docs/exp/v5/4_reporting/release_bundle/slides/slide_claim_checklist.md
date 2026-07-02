# v5 Slide Claim Checklist

Last updated: 2026-06-28

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
checklist header.

Use this checklist before turning `ppt_content.md` into the final deck.

| Slide | Current status | Use now | Needs update before final |
| --- | --- | --- | --- |
| 1. Title | ready | controlled 102-language Glot500-style reproduction + initialization novelty | no |
| 2. Motivation And Contributions | ready | problem framing plus three bounded contributions: 92+10 replay, FVT initialization, metric-family fidelity | no |
| 3. Reproduction Boundary | ready | pattern reproduction, not 511-language full reproduction | no |
| 4. Target10 Selection | ready | selected 10 language-scripts with region/script/new_length summary and diversity criteria | no |
| 5. Corpus Construction | ready | 92,452,251 lines, 19G, 102/102 PASS | no |
| 6. Tokenizer Method | ready with caveat | 118,685 appended tokens, 29/30 improved, `dzo_Tibt` regression | no |
| 7. Novelty | ready | new embedding-row initialization policy comparison | no |
| 8. Initialization Audit | ready | identity row copy, `<mask>` remap, byte rows, LM-head tying | no |
| 9. Zero-Step Evidence | ready | zero-step initialization result and intrinsic-only interpretation | add after-MLM comparison only after parsed PPPL rows |
| 10. Training Setup | in progress | paired 10K run launched; use generated `running_status.md` and `mlm_progress_eta.md` for live state; v5-random ready, v5-FVT running/model file pending | replace status with checkpoint paths after completion |
| 11. Glot500 Metrics | ready with coverage caveat | required metric families and refreshed coverage/status table | update if task data or v5 rows change coverage |
| 12. Current Measured Rows | partially ready | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip baseline/reference rows plus v5-random diagnostic rows from `09_aggregation/`; v5-FVT rows wait for checkpoints | promote remaining v5-FVT rows only from measured outputs |
| 13. Coverage And Limitations | ready, refreshable | target10 downstream coverage boundary and scale limitation | refresh only if new task data appears |
| 14. Conclusion | partial | reproduction setup + zero-step novelty | choose final wording only from `post_checkpoint_outcome_matrix_ko.md` after measured rows and decision tree agree |
| 15. Backup Artifacts | ready | command and artifact map | update command logs/checkpoint paths after completion |

## Final Deck Rules

- Numeric claims must point to `../00_tables/`, `../01_figures/`, or
  `../../3_evaluation/`.
- Do not state target10 downstream improvement unless target10 task data exists
  and is evaluated.
- Keep `dzo_Tibt` as a visible failure case, not a footnote.
- Say `Glot500-base external reference`, not equal-budget baseline.
- Replace every unresolved result slot with either a measured value or an explicit blocker/status note.
- Slide 14 must follow `../post_checkpoint_outcome_matrix_ko.md` and
  `../final_claim_decision_tree.md`; never improvise final conclusion wording.
- Use `slide_citation_map.md` for citation placement; numeric claims still need
  local table/aggregation sources.
