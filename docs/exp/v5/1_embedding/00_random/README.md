# 00 Random Init

Baseline initialization. Use Hugging Face `resize_token_embeddings()` behavior
without custom row initialization.

Expected artifacts:

- checkpoint path note
- `init_report.json`
- row norm audit
- zero-step MLM summary

## Next Step Gate

This baseline is eligible for `../04_zero_step_eval/` and `../05_audit/` only
after the resized checkpoint is reproducible.

Pass line:

- checkpoint loads with the v5 tokenizer.
- model embedding size equals extended tokenizer vocab size.
- old/source rows are preserved where token identities match.
- new row count and random initialization seed are recorded.
- `<mask>` row location is recorded.
- input embedding and LM head status is recorded.

Required artifacts:

- checkpoint path note
- `init_report.json`
- produced-file list
- row norm summary

If this baseline fails, do not train other methods as final comparisons because
the main control condition is missing.
