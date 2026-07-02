# 02 FVT Init

Main proposed initialization. Re-tokenize each new target token surface with the
source tokenizer and initialize from the mean of source subtoken embeddings.

Must explicitly handle:

- token identity row copy
- `<mask>` id remapping
- byte fallback rows
- LM head tying

## Next Step Gate

This main novelty method is eligible for `../04_zero_step_eval/`,
`../05_audit/`, and MLM training only after decomposition coverage is measured.

Pass line:

- every new token is assigned to one of: source-subtoken mean, fallback mean,
  byte row, special row, or skipped with reason.
- source tokenizer decomposition coverage is recorded for target10 and all new
  lexical rows.
- `<unk>` decompositions and empty decompositions are counted.
- checkpoint loads with the v5 tokenizer.
- `<mask>` remap, byte-row handling, and LM head tying are checked.

Required artifacts:

- checkpoint path note
- `init_report.json`
- decomposition coverage table
- fallback table
- row norm summary

If FVT coverage is unexpectedly poor for a script or language, route the case to
`../03_align/` or document it as a limitation before training.
