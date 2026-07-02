# v5 Section-Slide Sync Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `section_slide_sync_ready`

This generated audit checks that the manuscript completion matrix, slide
completion matrix, report-slide crosswalk, final deck, presenter script,
and conclusion-selection contract describe the same final report/PPT
handoff. It does not claim pending v5 results already exist.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| required sync artifacts | ready | all manuscript/slide sync artifacts exist | none |
| manuscript_section_coverage | ready | sections=15 | none |
| slide_matrix_coverage | ready | slides=15 | none |
| report_slide_crosswalk_coverage | ready | slides_covered=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 | none |
| claim_gate_consistency | ready | manuscript, slide matrix, and crosswalk mention the core pending/disallowed gates | none |
| deck_script_conclusion_sync | ready | final deck and presenter script share conclusion-gate references | none |
| conclusion_contract_dependency | ready | conclusion_selection_contract=conclusion_selection_contract_ready_waiting_results | none |

Use:

- Keep this audit ready before assembling the final report/PPT.
- If a section or slide changes after final metrics arrive, rerun
  `python3 scripts/refresh_v5_reporting.py` before freezing claims.
