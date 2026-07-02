# v5 Tokenizer Stage

This stage covers the Glot500-internal target10 data scope, corpus merge,
tokenizer training, and tokenizer audits.

Subfolders:

- `00_data_scope/`: language selection and data inventory
- `01_merge/`: corpus merge commands and logs
- `02_tokenizer_train/`: SentencePiece/XLM-R tokenizer expansion logs
- `03_audit/`: vocab, special id, fertility, and `<unk>` audits
- `merge/`: current merge manifest/report artifacts
- `miscellaneous/`: selected language manifest, candidate pool, stats CSV

Canonical overview:

- `dataset_processing.md`
- `../TOKENIZER_EXTENSION_METHODS_KO.md`

## Stage Exit Line

Move to `../1_embedding/` only after all of the following are true:

- `00_data_scope/` has frozen the selected 92 seen + 10 target languages.
- `01_merge/` has a final merge report with missing language dirs `0`.
- `02_tokenizer_train/` has a usable extended tokenizer output path.
- `03_audit/` confirms vocab size, appended pieces, `<mask>` id, byte rows,
  fertility, and `<unk>` behavior.

Minimum artifact line:

```text
data_scope frozen + merge done + tokenizer trained + audit pass
```

If this line is not met, embedding initialization can be tested only as a smoke
run and should not be used for the main v5 claim.
