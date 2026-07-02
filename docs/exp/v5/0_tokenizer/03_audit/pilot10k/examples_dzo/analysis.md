# dzo_Tibt Pilot Tokenization Regression Analysis

작성일: 2026-06-26

## Finding

The pilot tokenizer regression for `dzo_Tibt` is not an `<unk>` or byte fallback
problem. It is mainly a segmentation-choice problem after appending new
SentencePiece rows.

Evidence from `500` sampled `dzo_Tibt` examples:

| Item | Value |
| --- | ---: |
| XLM-R tokens/word | 4.493663 |
| v5 pilot tokens/word | 8.874784 |
| delta tokens/word | +4.381121 |
| worse examples | 483 |
| better examples | 5 |
| same examples | 12 |
| v5 target tokens | 16,719 |
| v5 newly appended tokens | 13,949 |
| newly appended token share | 83.432% |
| v5 byte tokens | 3 |
| v5 unk tokens | 0 |

## Interpretation

The base XLM-R tokenizer already contains useful Tibetan pieces, often fairly
long chunks. The pilot v5 tokenizer keeps those base pieces, but the appended
auxiliary SentencePiece pieces have their own scores. For `dzo_Tibt`, many newly
appended shorter pieces appear to be selected instead of the older longer XLM-R
pieces, increasing token count even though the vocabulary was expanded.

This suggests a score-calibration risk in Glot500-style SPM append:

```text
Adding new pieces can make tokenization worse if new short pieces outcompete
existing useful pieces.
```

## Report Use

Use `dzo_Tibt` as a failure-analysis example:

- It proves why tokenizer audit must be language-specific, not only averaged.
- It separates tokenizer expansion effects from embedding initialization effects.
- It motivates the v5 rule that main claims require head/tail/target audit before
  downstream evaluation.

Do not treat the pilot `dzo_Tibt` result as final. The main tokenizer will use
the full corpus and target vocab setting, so this failure must be rechecked.
