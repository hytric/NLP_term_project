# Plan: Data And Splits

Status: initial target10 extraction complete

## Goal

Collect, normalize, and split the 10-language low-resource pilot data so every later experiment has clean inputs and no evaluation leakage. Keep Coptic/Syriac as the main downstream translation case.

## Research Questions

- Can we collect enough text across about 10 low-resource languages to justify Glot500-style adaptation?
- Is there enough verse-level overlap to build a 500-1000 sentence Coptic-Syriac held-out test set?
- Which target languages create the strongest tokenizer failure modes?
- Which data can be redistributed, and which can only be used for local training?

## Candidate Sources

- Coptic Scriptorium corpora
- UD Coptic Scriptorium
- Multilingual Bible Parallel Corpus
- Sahidica / Coptic Bible sources
- SEDRA / Beth Mardutho
- Comprehensive Aramaic Lexicon
- Tatoeba and OPUS-style small parallel sources

## Planned Work

1. Download or stage public data sources.
2. Record URL, license, access date, and redistribution status.
3. Extract raw text while preserving original files.
4. Normalize into NFC text in separate processed files.
5. Verify script blocks:
   - Coptic: U+2C80-U+2CFF
   - Syriac: U+0700-U+074F
6. Build verse-aligned table for all target10 languages.
7. Create train/dev/test split.
8. Reserve final Bible evaluation set before any training.

## Outputs

- `data_inventory.tsv`
- `source_licenses.md`
- `split_manifest.tsv`
- `target_languages.tsv`
- `target10_bible_verses.tsv`
- `target10_stats.tsv`
- `target10_train_for_tokenizer.txt`

## Metrics

- sentence count per source
- token count per source
- percentage target-script characters
- number of overlapping target10 verse IDs
- held-out evaluation size

## Success Gate

This phase passes when:

- final held-out examples are identified and excluded from all training
- all 10 target languages have tokenizer-audit samples
- Coptic/Syriac held-out overlap is available for downstream translation
- licenses are documented for every source used in training or reporting

## Risks

- Bible alignment may be verse-level rather than sentence-level.
- Syriac sources may not be redistributable.
- Coptic sources may include duplicate witnesses or dialect variants.
