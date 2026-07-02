# 03 Final Report

Use this folder for the final polished report package. The living draft remains
at `../../Report.md`.

Current prose draft:

- `report_sections_draft.md`
- `paper_draft.md`
- `paper_draft.html`
- `paper_draft.pdf`
- `paper_draft_ko.md`
- `paper_draft_ko.html`
- `paper_draft_ko.pdf`
- `references.bib`
- `citation_source_map.md`
- `external_source_verification.md`
- `contribution_summary.md`
- `claim_ledger.md`
- `manuscript_completion_matrix.md`
- `paper_build_spec.md`
- `reproducibility_appendix.md`
- `result_interpretation_blocks.md`

## Next Step Gate

The final report is ready only after it is synchronized with all measured
artifacts.

Pass line:

- `../../Report.md` has no unresolved result slot for completed metrics.
- every result table points to `../00_tables/` or `../../3_evaluation/09_aggregation/`.
- every figure points to `../01_figures/`.
- limitations include missing coverage, failed runs, and skipped ablations.
- conclusion distinguishes reproduction result from initialization novelty.

Required artifacts:

- final report markdown or PDF path
- generated HTML report artifacts for browser review and print/PDF export
- generated PDF report artifacts for submission/review handoff
- Korean paper-style report draft for presentation/report writing
- source table/figure map
- metric completion checklist link
- final limitation note
- BibTeX references for cited papers and code artifacts
- citation source map for claim-to-reference boundaries
- primary-source verification note for bibliography and method-lineage claims
- reproducibility appendix with command and artifact paths
- result interpretation blocks for positive, mixed, and negative outcomes
- manuscript completion matrix with section-level gates
- paper build spec for final report assembly

If a metric remains blocked, the report can still be final only if the blocker
and its effect on claims are written explicitly.

Build browser/print report artifacts with:

```bash
python3 scripts/build_v5_report_html.py
```

Build PDF report artifacts with:

```bash
bash scripts/build_v5_report_pdf.sh
```
