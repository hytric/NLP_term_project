# v5.2 Tokenization Effect

This audit compares `xlm-roberta-base` tokenization with the local v5.2 extended tokenizer on the same target7 raw sentences.

## Setup

- base tokenizer length: `250002`
- v5.2 tokenizer length: `366666`
- appended/novel token strings: `116664`
- samples per language: `500`

## Aggregate Result

| Scope | Sentences | Base TPW | v5.2 TPW | Token reduction | Base chars/token | v5.2 chars/token | New-token share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| target7 | 3500 | 2.204134 | 1.592392 | 27.754280% | 2.074479 | 2.871421 | 28.392427% |

## By Language

| Language | Name | Sentences | Base TPW | v5.2 TPW | Token reduction | New-token share | Better | Same | Worse |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bam_Latn | Bambara | 500 | 2.248034 | 1.513428 | 32.677703% | 32.346790% | 496 | 3 | 1 |
| csb_Latn | Kashubian | 500 | 2.934551 | 1.945100 | 33.717290% | 34.388850% | 488 | 12 | 0 |
| dtp_Latn | Kadazan Dusun | 500 | 1.975990 | 1.496198 | 24.281085% | 34.394223% | 489 | 11 | 0 |
| fur_Latn | Friulian | 500 | 1.824645 | 1.453669 | 20.331393% | 23.974143% | 485 | 15 | 0 |
| ile_Latn | Interlingue | 500 | 1.544606 | 1.352672 | 12.426036% | 14.416863% | 443 | 57 | 0 |
| lij_Latn | Ligurian | 500 | 2.195411 | 1.824073 | 16.914278% | 19.795870% | 480 | 20 | 0 |
| xav_Latn | Xavánte | 500 | 2.398465 | 1.561237 | 34.906811% | 34.478046% | 500 | 0 | 0 |

## Interpretation

- Positive token reduction means the extended tokenizer uses fewer subwords per word than XLM-R.
- This confirms a tokenizer-side fertility improvement for the target7 raw corpus.
- However, all v5.2 ablation models use the same extended tokenizer. Therefore differences among `random`, `mean`, and `fvt` cannot be explained by tokenizer extension alone.
- The tokenizer effect should be presented as a necessary preprocessing improvement, while the novelty claim should focus on embedding initialization after vocab extension.

## Outputs

- `tokenization_effect_summary.tsv`
- `tokenization_effect_examples.tsv`
- `tokenization_effect_change.png`
