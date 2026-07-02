# Final Submission Checklist

작성일: 2026-06-04

## Must Have

- [x] Final objective documented.
- [x] Target10 language set documented.
- [x] GPU policy documented.
- [x] Data split documented.
- [x] Tokenization audit table.
- [x] Vocabulary extension metrics.
- [x] Embedding initialization metrics.
- [x] MLM checkpoint selection.
- [x] Direct NMT baseline results.
- [x] Retrieval baseline results.
- [x] Pivot/back-translation gate result.
- [x] Final metric table draft.
- [x] Qualitative analysis draft with 20 inspected examples.
- [x] Error taxonomy draft.
- [x] Reproducibility checklist draft.
- [x] Command examples draft.
- [x] Claim-to-evidence map draft.
- [x] Experiment manifest draft.
- [x] Source-grounding diagnostic gate documented.
- [x] Release audit folder and artifact inventory drafted.

## Still Needed Before Final Paper

- [x] Convert current notes into a coherent paper narrative draft.
- [x] Add citations and related-work discussion with actual bibliographic sources.
- [x] Add figures or compact tables for tokenization reductions.
- [x] Decide whether to run one stronger source-grounding experiment.
- [x] Write final limitations section.
- [ ] Clean untracked/modified workspace state before public GitHub release.
- [ ] Confirm data licenses and redistribution limits with source-specific license text.

## Release Risks

- `docs/`, `scripts/`, and several support files are currently untracked.
- Existing tracked modifications in `modeling/*.py` and `evaluation/download_data/download_data.sh` should be reviewed before commit.
- Large artifacts should stay on `/disk1` or be ignored; do not push checkpoints.
- Root `main.zip` is now ignored and should be removed or kept outside release history.
- Local license evidence now covers `bible-corpus` and `UD_Coptic-Scriptorium`, but every raw source still needs a source-by-source redistribution decision.
