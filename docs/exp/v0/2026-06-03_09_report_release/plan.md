# Plan: Report And Release

Status: report, presentation, term-paper outline, related-work notes, reproducibility, command examples, license notes, limitations, claim map, and experiment manifest drafted

## Goal

Package the project into a progress report, final presentation, term paper, and reproducible GitHub-ready codebase.

## Deliverables

- 2026-06-12 progress report
- 2026-06-19 final presentation
- 2026-07-03 term paper
- GitHub reproducibility instructions

## Planned Work

1. Convert survey and plan documents into progress report slides.
2. Update experiment tables with real results.
3. Write final paper sections:
   - Introduction
   - Related Work
   - Data
   - Method
   - Experiments
   - Results
   - Discussion
   - Conclusion
4. Write reproducibility docs.
5. Check that all scripts have command examples.
6. Confirm license notes for data.
7. Create final limitations section.

## Paper Claim Checklist

- Coptic/Syriac are unsupported or poorly tokenized by existing models.
- Vocabulary extension improves tokenizer metrics.
- Embedding initialization affects adaptation stability.
- Pivot/multitask/back-translation affects NMT quality.
- chrF++ and qualitative examples support conclusions even if BLEU is low.

## Outputs

- `progress_report.md`
- `final_presentation_outline.md`
- `term_paper_outline.md`
- `related_work_notes.md`
- `reproducibility_checklist.md`
- `final_submission_checklist.md`

## Success Gate

This phase passes when:

- paper claims map to evidence files
- commands are reproducible
- final report and GitHub link are ready for submission

## Decision Rule

Do not claim a novelty as proven unless it has a controlled comparison. Use "case study", "analysis", or "preliminary evidence" for weaker results.
