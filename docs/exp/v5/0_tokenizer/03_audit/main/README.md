# Main Tokenizer Audit

이 폴더는 full v5 tokenizer audit result를 보관한다.

Main report source:

- `results.md`
- `tokenization_metrics.tsv`
- `tokenization_comparison.tsv`
- `special_token_ids.tsv`
- `vocab_audit.json`

Promotion rule: tokenizer claims should use this `main` audit, not the
`pilot10k` audit. `dzo_Tibt` must remain a visible limitation.
