# Results: Target10 Tokenization Audit

작성일: 2026-06-03

## Setup

Samples:

- 10 target languages
- 500 train verses per language

Tokenizers:

- `xlm-roberta-base`
- `cis-lmu/glot500-base`
- `facebook/nllb-200-distilled-600M`

Output:

- `target10_tokenization_metrics.tsv`


> 10개 언어 Bible train split에서 언어당 500개 verse를 뽑고, 같은 문장을 여러 tokenizer로 tokenize해서 비교

## Key Finding

The tokenizer bottleneck is real, but it differs by model.

- Glot500 is very poor for Coptic, Syriac, Cherokee, and Ojibwa in this Bible corpus.
- NLLB has a serious UNK problem for Coptic, Syriac, Cherokee, and Ojibwa.
- XLM-R handles Coptic/Cherokee/Ojibwa better than expected, but Syriac is heavily character-level.

## Most Important Numbers

| Tokenizer | Language | Script | tokens/word | single-char % | UNK % |
| --- | --- | --- | ---: | ---: | ---: |
| Glot500 | Syriac | Syriac | 5.089 | 80.3 | 0.0 |
| Glot500 | Coptic | Coptic | 5.274 | 67.7 | 0.0 |
| Glot500 | Cherokee | Cherokee | 5.254 | 77.2 | 0.0 |
| Glot500 | Ojibwa | Aboriginal Syllabics | 5.021 | 87.0 | 0.0 |
| NLLB | Syriac | Syriac | 2.000 | 0.0 | 50.0 |
| NLLB | Coptic | Coptic | 2.059 | 2.8 | 48.6 |
| NLLB | Cherokee | Cherokee | 2.227 | 10.2 | 45.0 |
| NLLB | Ojibwa | Aboriginal Syllabics | 2.105 | 5.8 | 47.2 |
| XLM-R | Syriac | Syriac | 4.785 | 73.8 | 0.0 |

## Interpretation

For the paper, this gives two distinct failure modes:

1. Character fragmentation: Glot500 and XLM-R produce many single-character tokens, especially for Syriac and non-Latin scripts.
2. Unknown-token collapse: NLLB has lower token counts for some scripts, but only because many characters collapse into `<unk>`.

This strongly supports vocabulary extension as the next experiment.

## Caveat

Some verses exceed model max sequence length after tokenization.
For model training, max-length filtering or chunking is mandatory.
