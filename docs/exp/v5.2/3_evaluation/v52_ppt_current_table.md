# v5.2 Current PPT Table

Generated during the accelerated downstream pass.

`align` is excluded from the main ablation because it collapsed to the same artifact as `fvt`.

## Dataset And Evaluation Size

| Split / task | Scope | Count |
| --- | --- | ---: |
| MLM train seen/head | 92 XLM-R-seen replay languages | 4,147,176 samples |
| MLM train target7 | 7 XLM-R-unseen tail targets | 335,083 samples |
| MLM train total | 99 language-script units | 4,482,259 samples |
| PPPL target pool | Target7, 100 samples per language | 700 samples |
| Tatoeba retrieval | `dtp`, `ile`, `csb` | 2,253 sentence pairs |
| Bible retrieval | `dtp`, `xav`, `bam` | 23,238 verse pairs |
| Roundtrip alignment | `dtp`, `xav`, `bam` | 22,669 samples |
| NER | `csb`, `lij`, `fur` | 300 test sentences |
| POS target subset | `xav`, `bam`, `lij` | 1,342 test sentences / 20,286 tokens |
| POS full scoring set | Table 3 POS 91 languages | 200,200 test sentences / 3,336,371 tokens |

PPPL note: the target pool is 700 samples, while the accelerated scored run
currently reported in the table used 140 sentences and 5,196 masked tokens.

| Model / Method | PPPL ↓ | Tatoeba Acc10 ↑ | Bible Acc10 ↑ | Text macro-F1 ↑ | NER F1 ↑ | POS F1 ↑ | Roundtrip Acc ↑ | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| XLM-R-B | 98.2 | 20.5 | 0.5 | 59.3 | 45.7 | 53.9 | 2.4 | baseline complete |
| XLM-R-L | 63.7 | 12.8 | 0.4 | 72.9 | 53.9 | 54.4 | 2.7 | baseline complete |
| Glot500-m | 7.7 | 45.7 | 14.7 | 74.3 | 52.6 | 59.5 | 5.4 | baseline complete |
| random | 119.6 | 24.9 | 0.6 | 69.7 | 37.7 | 50.7 | 1.9 | current |
| mean | 128.3 | 24.6 | 0.6 | 77.8 | 40.5 | 50.7 | 2.2 | current |
| fvt | 58.0 | 28.3 | 0.6 | 71.3 | 48.4 | 51.9 | 2.6 | current |

## Notes

- Current ablation table is now complete for random/mean/fvt.
- Scale follows the Glot500 paper table style: PPPL is raw; all other task metrics are reported as score x 100.
- `XLM-R-B` PPPL/Tatoeba/Bible/Text/NER/POS/Roundtrip baselines are filled.
- `XLM-R-L` PPPL/Tatoeba/Bible/Text/NER/POS/Roundtrip baselines are filled.
- `Glot500-m` PPPL/Tatoeba/Bible/Text/NER/POS/Roundtrip baselines are filled.
- NER is a small target-subset diagnostic: `csb_Latn`, `lij_Latn`, and
  `fur_Latn` have only 100 test sentences each. FVT beats random/mean on this
  subset, but it does not beat `XLM-R-L` or `Glot500-m`.
- Roundtrip alignment is recomputed on the full materialized target files:
  `dtp_Latn` 7,393 samples, `xav_Latn` 7,393 samples, and `bam_Latn` 7,883
  samples. The earlier 300-sample row is retained only in the backup artifacts.
- POS values are now recomputed on the recovered Table 3 POS split: 91/91
  languages, with 63/63 head and 28/28 tail covered.
- The recovered POS source is
  `/home/axt/mnt2/jongha/v5_glot50010/eval_data_download/udpos-redownload-20260628_212333/pos_rebuilt/`.
  It contains 134 `test-*.tsv` files and covers all 91 Table 3 POS languages
  from `evaluation/tagging/pos_lang_list.txt`, including all 28 tail languages.

## POS Breakdown

| Model / Method | All 91 | Head 63 | Tail 28 |
| --- | ---: | ---: | ---: |
| XLM-R-B | 53.9 | 61.8 | 36.2 |
| XLM-R-L | 54.4 | 62.0 | 37.2 |
| Glot500-m | 59.5 | 63.7 | 50.2 |
| random | 50.7 | 58.5 | 33.2 |
| mean | 50.7 | 58.4 | 33.5 |
| fvt | 51.9 | 59.8 | 34.0 |
