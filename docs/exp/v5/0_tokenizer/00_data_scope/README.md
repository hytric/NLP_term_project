# 00 Data Scope

Use this folder for language selection, head/tail definitions, corpus inventory,
and data availability notes.

Current canonical files outside this folder:

- `../miscellaneous/glot50010_selected_manifest.tsv`
- `../miscellaneous/glot500_candidate_pool_min30k.tsv`
- `../miscellaneous/languages_stats_glot50010_xlmr100.csv`
- `../../LANGUAGE_SOURCE_OVERLAP_KO.md`
- `../../TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md`

Source/overlap note: `XLM-R=True` is a membership label for the seen/head side;
the actual v5 raw text used for tokenizer/MLM/PPPL is the local Glot500 raw-text
subset containing all `102` language-scripts.

Downstream correction: the current target10 has `0/10` direct coverage for
Tatoeba/Bible/Roundtrip/Taxi1500/NER/POS. If target-language downstream evidence
is required, use `target_candidate_task_overlap.tsv` to choose a
downstream-aware target set before merge/tokenizer/training.

## Next Step Gate

Move to `../01_merge/` only after this data scope is frozen.

Pass line:

- selected language count is fixed at `92 seen + 10 target`.
- every target language has `XLM-R != True`, `new_length >= 30000`, and an
  existing raw directory.
- region/script/family diversity rationale is written.
- excluded XLM-R seen languages and missing raw directories are documented.
- raw symlink root contains exactly `102` language-script entries.

Required artifacts:

- selected target manifest
- candidate pool
- stats CSV
- data-processing note with selection rationale

If any language is replaced after this gate, return here and regenerate merge
inputs before continuing.
