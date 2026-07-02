# 02 Slides

Use this folder for slide outlines, exported figures, and final deck assets.

Current slide content draft:

- `ppt_content.md`
- `final_deck_ko.md`
- `v5_final_deck_ko.html`
- `v5_final_deck_ko.pptx`
- `v5_final_deck_ko.pdf`
- `talk_track.md`
- `presenter_script_ko.md`
- `rehearsal_plan_ko.md`
- `defense_qa.md`
- `defense_qa_ko.md`
- `novelty_defense_matrix_ko.md`
- `slide_claim_checklist.md`
- `slide_completion_matrix.md`
- `deck_build_spec.md`

## Next Step Gate

Move to final presentation only after the slide story matches the measured
report results.

Pass line:

- slide outline covers motivation, data, method, experiments, results,
  limitations, and conclusion.
- every numeric claim points to `../00_tables/` or `../../3_evaluation/`.
- every figure points to `../01_figures/`.
- incomplete metrics are labeled draft or blocked.
- final conclusion does not overstate unsupported results.
- outcome wording follows `../03_final_report/result_interpretation_blocks.md`.
- final Korean conclusion wording also follows
  `../post_checkpoint_outcome_matrix_ko.md`.

Required artifacts:

- slide outline or deck file
- table/figure source map
- speaker-note draft when needed
- rehearsal timing plan
- slide citation map
- Korean Q&A defense card
- Korean 10/30/60-second compressed answer cards inside `defense_qa_ko.md`
- novelty/reproduction defense matrix
- final checklist
- slide completion matrix
- deck build spec for actual PPT assembly
- generated HTML deck for rehearsal and browser-based presentation
- generated PPTX deck for actual presentation handoff
- generated PDF deck for review/sharing
- outcome-conditioned talk blocks for mixed or negative results
- Korean post-checkpoint outcome matrix for slide 14 conclusion replacement
- final claim decision tree for selecting slide 14 conclusion wording

If results change, update slides after updating tables and figures.

Build the browser-presentable deck with:

```bash
python3 scripts/build_v5_slide_html.py
```

Build the PowerPoint deck with:

```bash
python3 scripts/build_v5_slide_pptx.py
```

Build the PDF deck with:

```bash
bash scripts/build_v5_slide_pdf.sh
```
