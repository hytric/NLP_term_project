# PPPL v5_random Output

이 폴더는 `v5_random_mlm_10k` continued-MLM checkpoint의 PPPL run output을 보관한다.

Key files:

- `summary.tsv`: group-level weighted PPPL and weighted mean NLL for all, head, and v5 target groups.
- `scores.tsv`: language-script-level PPPL rows.
- `results.md`: human-readable PPPL summary.
- `run_meta.tsv`: model, tokenizer, GPU, and output-root provenance.
- `command_logs/`: execution log for the measured run.

Promotion rule: final tables should use values after aggregation into
`../../09_aggregation/`, not hand-copied raw files. This row is measured
evidence for the random-initialized checkpoint only; FVT-vs-random method
claims remain locked until the matched `v5_fvt` PPPL row is also parsed.
