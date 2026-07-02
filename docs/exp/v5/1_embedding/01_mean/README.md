# 01 Mean Init

Initialize target-only lexical rows with a source embedding mean vector.

Expected artifacts:

- checkpoint path note
- `init_report.json`
- fallback count
- zero-step MLM summary

## Next Step Gate

This ablation is eligible for `../04_zero_step_eval/` and `../05_audit/` only
after the mean-vector policy is fully specified.

Pass line:

- mean source is defined as source lexical rows, target-related rows, or global
  lexical rows.
- excluded rows such as special tokens and byte rows are documented.
- checkpoint loads with the v5 tokenizer.
- new lexical row count and fallback count are recorded.
- `<mask>` remap and LM head consistency are checked.

Required artifacts:

- checkpoint path note
- `init_report.json`
- mean-vector definition note
- fallback/count table

If this method is skipped for compute reasons, write that here and keep it out
of the minimum report matrix.
