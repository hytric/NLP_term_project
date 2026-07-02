# Table 2. Tokenizer Audit

Last updated: 2026-06-27

Caption draft:

```text
The v5 tokenizer follows the Glot500-style SentencePiece append procedure. The
main full-corpus tokenizer appends 118,685 novel token strings to XLM-R and
passes structural audits, while dzo_Tibt remains a documented fertility-risk
case.
```

| Audit item | Value |
| --- | ---: |
| base HF tokenizer length | 250,002 |
| v5 extended tokenizer length | 368,687 |
| appended novel token strings | 118,685 |
| byte fallback tokens | 256 |
| source `<mask>` id | 250,001 |
| target `<mask>` id | 368,686 |
| audited languages | 30 |
| audit failures | 0 |
| languages with lower tokens/word | 29 / 30 |
| target10 improved | 9 / 10 |
| target10 average tokens/word delta | -0.390862 |
| target10 average delta excluding `dzo_Tibt` | -0.581867 |
| `dzo_Tibt` base tokens/word | 4.223938 |
| `dzo_Tibt` v5 tokens/word | 5.552124 |

Interpretation note:

`dzo_Tibt` is not an `<unk>` or byte-fallback failure. The example analysis
shows `0` target byte tokens, `0` target `<unk>` tokens, and high newly appended
piece share. The likely issue is SPM score calibration among appended Tibetan
pieces.

Source artifacts:

- `docs/exp/v5/0_tokenizer/03_audit/main/results.md`
- `docs/exp/v5/0_tokenizer/03_audit/main/tokenization_comparison.tsv`
- `docs/exp/v5/0_tokenizer/03_audit/main/examples_dzo/summary.tsv`

