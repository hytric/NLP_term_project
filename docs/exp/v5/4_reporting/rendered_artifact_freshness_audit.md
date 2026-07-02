# v5 Rendered Artifact Freshness Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `rendered_artifact_freshness_ready`

This generated audit checks that shareable report/PPT handoff files
are not stale relative to their Markdown or intermediate rendered
sources. It guards against sharing an old PDF/PPTX after report or
deck source edits.

| Item | Status | Source | Artifact | Source mtime | Artifact mtime | Artifact bytes | Action |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| report_en_md_to_html | ready | 4_reporting/03_final_report/paper_draft.md | 4_reporting/03_final_report/paper_draft.html | 2026-06-28 10:54:09 | 2026-06-28 18:08:31 | 42091 | none |
| report_en_md_to_pdf | ready | 4_reporting/03_final_report/paper_draft.md | 4_reporting/03_final_report/paper_draft.pdf | 2026-06-28 10:54:09 | 2026-06-28 18:08:31 | 127722 | none |
| report_en_html_to_pdf | ready | 4_reporting/03_final_report/paper_draft.html | 4_reporting/03_final_report/paper_draft.pdf | 2026-06-28 18:08:31 | 2026-06-28 18:08:31 | 127722 | none |
| report_ko_md_to_html | ready | 4_reporting/03_final_report/paper_draft_ko.md | 4_reporting/03_final_report/paper_draft_ko.html | 2026-06-28 10:54:09 | 2026-06-28 18:08:31 | 30967 | none |
| report_ko_md_to_pdf | ready | 4_reporting/03_final_report/paper_draft_ko.md | 4_reporting/03_final_report/paper_draft_ko.pdf | 2026-06-28 10:54:09 | 2026-06-28 18:08:31 | 210539 | none |
| report_ko_html_to_pdf | ready | 4_reporting/03_final_report/paper_draft_ko.html | 4_reporting/03_final_report/paper_draft_ko.pdf | 2026-06-28 18:08:31 | 2026-06-28 18:08:31 | 210539 | none |
| deck_md_to_html | ready | 4_reporting/02_slides/final_deck_ko.md | 4_reporting/02_slides/v5_final_deck_ko.html | 2026-06-28 10:53:45 | 2026-06-28 18:08:30 | 16259 | none |
| deck_md_to_pptx | ready | 4_reporting/02_slides/final_deck_ko.md | 4_reporting/02_slides/v5_final_deck_ko.pptx | 2026-06-28 10:53:45 | 2026-06-28 18:08:30 | 30236 | none |
| deck_md_to_pdf | ready | 4_reporting/02_slides/final_deck_ko.md | 4_reporting/02_slides/v5_final_deck_ko.pdf | 2026-06-28 10:53:45 | 2026-06-28 18:08:30 | 80525 | none |
| deck_pptx_to_pdf | ready | 4_reporting/02_slides/v5_final_deck_ko.pptx | 4_reporting/02_slides/v5_final_deck_ko.pdf | 2026-06-28 18:08:30 | 2026-06-28 18:08:30 | 80525 | none |

Use:

- If this audit fails, rebuild the report/PPT artifacts before sharing the bundle.
- This is a freshness check only; rendering readability and overclaim guards are checked separately.
