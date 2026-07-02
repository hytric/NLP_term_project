# Data Inventory

작성일: 2026-06-03

이 문서는 과제 가이드라인과 현재 확인 가능한 원자료/공식 페이지를 바탕으로 만든 예비 데이터 인벤토리이다.
라이선스와 재배포 가능성은 반드시 다운로드 전후로 다시 확인한다.

## 1. Priority Sources

| Priority | Source | Language | Type | Current evidence | Expected use | Main risk | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | Coptic Scriptorium corpora | Coptic | monolingual, annotated, some translated | Public GitHub corpora; most documents CC-BY 3.0/4.0 except Sahidica-specific material | tokenizer training, MLM adaptation, qualitative examples | duplicate witnesses, TEI/TT parsing, Sahidica license exception | Clone/download release and count unique sentences |
| P0 | UD Coptic Scriptorium | Coptic | manually annotated treebank | Total listed tokens: 58,974; license CC BY 4.0; includes Bible, Shenoute, Besa, saints' lives | tokenizer audit sample, normalization test, small evaluation diagnostics | token-level corpus, not direct MT parallel | Download CoNLL-U and extract surface sentences |
| P0 | Multilingual Bible Parallel Corpus | Coptic, Syriac, Greek, English | parallel Bible | Coptic and Syriac entries both listed as New Testament; Greek and English available | Coptic/Syriac/Greek/English verse-level pivot baseline and evaluation candidate | verse alignment may be coarse; license/source constraints need checking | Download XML and inspect verse IDs |
| P0 | SEDRA / Beth Mardutho | Syriac | lexical/literary database | SEDRA reports roots, lexemes, words and Syriac linguistic database scope | Syriac vocabulary coverage, lexicon-assisted normalization, possible monolingual text leads | access and redistribution constraints | Check library/API/export path |
| P0 | Comprehensive Aramaic Lexicon | Syriac/Aramaic | text base, lexically parsed words | CAL describes Aramaic texts from 9th c. BCE to 13th c. CE, approx. 3M lexically parsed words | Syriac monolingual data, lexical analysis | dialect mixture, web extraction, licensing | Inspect Syriac text pages and terms |
| P1 | Sahidica | Coptic | Coptic New Testament | Coptic Scriptorium notes Sahidica-specific license; Biblical-data hosts Sahidic NT PDF | Coptic Bible parallel candidate | academic-use-only or limited license | Verify exact license before use |
| P1 | Coptic Scriptorium Sahidic OT | Coptic | Old Testament texts | Coptic Scriptorium page indicates CC BY-SA 4.0 for Sahidic OT from Göttingen project | Coptic biblical evaluation/pivot data | OT coverage may be partial | Download and inspect book coverage |
| P1 | Tatoeba | Syriac, possibly Coptic-related via translations | short parallel sentences | Tatoeba download page lists Syriac among languages | small sanity-check parallel examples | likely tiny and modern/simple domain | Query downloads for `syc`/Syriac |
| P2 | Patristic editions and CSCO/Patrologia | Coptic, Syriac, Greek | scholarly editions/translations | Survey points to patristic literature as important source | future paper extension beyond Bible domain | copyright/OCR/alignment workload | Keep as stretch goal |

## 2. Source Notes

### Coptic Scriptorium

Why it matters:

- It is the strongest Coptic-first source for annotated, machine-readable text.
- It can support tokenizer audit, normalization, sentence extraction, and linguistic error analysis.
- The public corpora repository warns about duplicate material and parallel witnesses, which matters for train/dev/test leakage.

Immediate checks:

- Count documents, raw tokens, bound groups, and sentence-like units.
- Filter `redundant="yes"` where quantitative experiments would double-count similar witnesses.
- Separate Sahidica-derived texts from normal CC-BY material.

### UD Coptic Scriptorium

Why it matters:

- It is smaller than the full corpora but manually curated.
- It gives a clean first sample for tokenization diagnostics.
- It includes genre variety: Bible, fiction, nonfiction, saints' lives, Shenoute/Besa material.

Immediate checks:

- Extract sentence text from CoNLL-U.
- Compare raw orthographic tokens vs multi-word token expansion.
- Use it as the first tokenizer audit fixture before larger crawling.

### Bible Parallel Corpus

Why it matters:

- It gives Coptic, Syriac, Greek, and English in one verse-indexed framework.
- It is the easiest route to a first pivot baseline: Coptic -> Greek/English -> Syriac.
- It can seed a held-out evaluation set if splits are made by book/chapter/verse and leakage is controlled.

Immediate checks:

- Confirm language codes: `cop` for Coptic, `arc` or source-specific Syriac entry.
- Verify whether Coptic and Syriac verse IDs overlap enough for 500-1000 test examples.
- Split by book or chapter to avoid near-duplicate verse leakage.

### Syriac Sources

SEDRA and CAL should be treated as complementary:

- SEDRA looks stronger for lexeme/word-level Syriac linguistic resources.
- CAL looks stronger for broad Aramaic/Syriac text coverage.
- Both need careful access, licensing, and dialect filtering before use as training data.

Immediate checks:

- Identify whether Classical Syriac text can be downloaded in plain Unicode Syriac script.
- Separate Syriac from other Aramaic dialects.
- Determine whether data is usable only for analysis or also for model training.

## 3. First Download Plan

1. Download UD Coptic Scriptorium.
2. Download Coptic Scriptorium corpora release.
3. Download Bible Parallel Corpus.
4. Extract 100 sentences per language for tokenizer audit.
5. Extract verse-aligned Coptic/Syriac/Greek/English table.
6. Record license/source metadata per file before training.

## 4. Data Split Rules

- Never mix the final 500-1000 Bible evaluation verses into tokenizer training, MLM adaptation, NMT training, or synthetic data generation.
- Prefer book-level or chapter-level split for Bible data, not random verse split.
- Keep Coptic dialect labels when available, especially Sahidic vs Bohairic.
- Keep Syriac dialect/source labels when available.
- Preserve original Unicode text and store normalized text separately.

## 5. Open Data Questions

- How many Coptic sentences remain after duplicate witness filtering?
- How many Syriac sentences can be downloaded legally in Unicode plain text?
- Does Bible Parallel Corpus provide enough direct Coptic-Syriac verse overlap?
- Should Bible test set be Gospel-only for alignment quality, or mixed books for robustness?
- Are Greek/English pivot texts close enough to Coptic/Syriac witnesses to avoid misleading synthetic pairs?

## 6. Evidence Links

- Coptic Scriptorium corpora: https://github.com/CopticScriptorium/corpora
- UD Coptic Scriptorium: https://github.com/UniversalDependencies/UD_Coptic-Scriptorium
- Coptic Scriptorium data browser: https://data.copticscriptorium.org/
- Multilingual Bible Parallel Corpus: https://christos-c.com/bible/
- Bible corpus GitHub: https://github.com/christos-c/bible-corpus
- SEDRA: https://sedra.bethmardutho.org/about/sedra
- CAL: https://cal.huc.edu/main_index.html
- Tatoeba downloads: https://tatoeba.org/en/downloads
