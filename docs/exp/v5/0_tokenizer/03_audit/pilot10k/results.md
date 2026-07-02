# v5 Tokenizer Audit Results

- target tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/pilot10k_output/Glot500_extended_spm`
- audited languages: `30`
- failures: `0`
- base len: `250002`
- target len: `257593`
- novel token count by string: `7591`
- target byte token count: `256`
- base `<mask>` id: `250001`
- target `<mask>` id: `257592`

Artifacts:

- `vocab_audit.json`
- `special_token_ids.tsv`
- `tokenization_metrics.tsv`
- `tokenization_comparison.tsv`

Additional pilot finding:

- `9/10` target languages reduced tokens/word.
- `dzo_Tibt` regressed from `4.223938` to `8.859717` tokens/word in the
  200-sentence audit.
- A separate 500-example `dzo_Tibt` analysis shows this is not byte fallback or
  `<unk>` behavior: v5 byte tokens `3`, v5 unk tokens `0`.
- In that 500-example analysis, `83.432%` of v5 `dzo_Tibt` tokens are newly
  appended pieces, suggesting appended short SPM pieces outcompete useful
  original XLM-R Tibetan pieces.

See:

- `examples_dzo/analysis.md`
- `examples_dzo/examples.md`
- `examples_target10/summary.tsv`
