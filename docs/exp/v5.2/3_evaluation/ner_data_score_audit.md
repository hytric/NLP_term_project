# v5.2 NER Data And Score Audit

## Verdict

NER outputs are not obviously corrupted: every reported model has 3 target
language blocks, prediction lengths match gold token counts, and all baselines
and ablations use the same target test files.

The main issue is evidential strength. The local PAN-X/NER target data for
`csb_Latn`, `lij_Latn`, and `fur_Latn` contains only 100 test sentences per
language. Therefore NER can be reported as a small target-subset diagnostic,
but it should not be framed as strong Table 3-scale downstream evidence.

## Score Check

Scores are macro averages over the three target languages.

| Model | `csb_Latn` | `lij_Latn` | `fur_Latn` | Macro F1 |
| --- | ---: | ---: | ---: | ---: |
| XLM-R-B | 56.2 | 34.7 | 46.0 | 45.7 |
| XLM-R-L | 58.5 | 47.1 | 55.9 | 53.9 |
| Glot500-m | 59.0 | 42.1 | 56.8 | 52.6 |
| random | 41.5 | 29.5 | 42.1 | 37.7 |
| mean | 45.9 | 30.6 | 45.0 | 40.5 |
| fvt | 52.6 | 38.4 | 54.3 | 48.4 |

Interpretation: `fvt` is better than `random` and `mean` on all three target
languages, but it does not beat `XLM-R-L` or `Glot500-m` on this NER subset.

## Data Check

| Split | Sentences | Tokens | Entity tokens | Entity spans |
| --- | ---: | ---: | ---: | ---: |
| English train | 20,000 | 160,394 | 79,032 | 27,931 |
| English dev | 10,000 | 80,536 | 39,661 | 14,146 |
| `csb_Latn` test | 100 | 953 | 224 | 122 |
| `lij_Latn` test | 100 | 1,021 | 205 | 111 |
| `fur_Latn` test | 100 | 1,154 | 203 | 110 |
| Target test total | 300 | 3,128 | 632 | 343 |

The source English train/dev data is much larger and has a higher entity-token
ratio than the target tests. This can make target transfer scores noisy.

## Sanity Checks

| Check | Result |
| --- | --- |
| Models with non-empty NER `test_results.txt` | 6/6 |
| Language blocks per model | 3/3: `csb_Latn`, `lij_Latn`, `fur_Latn` |
| Prediction length vs gold token count | matches for all three target languages |
| Shared target test files across baselines/ablations | same SHA for each language |
| random/mean/fvt tokenizer cache compatibility | same SentencePiece SHA |

## Reporting Rule

Use NER as:

```text
Small target-subset transfer diagnostic: FVT improves over random/mean, but
the 300-sentence target test set is too small for a strong downstream claim.
```

Do not use NER as:

```text
FVT beats full Glot500/XLM-R baselines on NER.
```
