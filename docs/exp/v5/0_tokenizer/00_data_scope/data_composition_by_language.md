# v5 Language-Level Data Composition

Last checked: 2026-06-28

이 문서는 v5 실험의 언어별 데이터 구성을 정리한다. 핵심 범위는
`92` XLM-R 학습 포함 언어와 `10` Glot500-internal target 언어의 controlled
`102` language-script subset이다.

언어 소스와 task coverage overlap 해석은 `../../LANGUAGE_SOURCE_OVERLAP_KO.md`를
먼저 본다.

## Counting Rule

- `mlm_train_samples`: full merged corpus에 실제 들어간 continued-MLM train row 수이다.
- `mlm_valid_samples`와 `mlm_test_samples`: 현재 v5 MLM corpus에는 별도 held-out
  split을 만들지 않았으므로 `0`으로 기록한다.
- PPPL은 raw text availability를 기록한다.
- Tatoeba/Bible/Roundtrip은 train/dev split이 아니라 retrieval/alignment evaluation
  pair 또는 JSONL row 수를 test-style count로 기록한다.
- NER/POS는 TSV의 blank-line separated sequence blocks를 sentence count로 기록한다.
- Taxi1500은 row count를 train/dev/test example count로 기록한다.
- `xlm_r_training_language=yes`는 v5의 92 seen/head side, `no`는 selected target10 side와 일치한다.
- `has_*` 컬럼은 final coverage gate이다. 로컬 파일 count가 0보다 커도 upstream
  flag가 0이면 final claim에서는 coverage-limited row로 취급한다. 예: `fur_Latn`
  NER 파일은 존재하지만 `coverage_ner.tsv`의 upstream flag가 `0`이므로 target10-wide
  downstream claim으로 승격하지 않는다.

## Summary

| Item | Value |
| --- | ---: |
| total language-scripts | 102 |
| seen/head language-scripts | 92 |
| target language-scripts | 10 |
| XLM-R training language yes | 92 |
| XLM-R training language no | 10 |
| total source sentences, new_length | 1025998855 |
| total MLM train samples | 92452251 |
| PPPL raw-text languages | 102 |
| Tatoeba retrieval languages | 63 |
| Bible retrieval languages | 74 |
| Roundtrip alignment languages | 74 |
| Taxi1500 languages | 1 |
| NER languages | 78 |
| POS languages | 58 |

## Target10 Detailed Table

| language_script | script | xlm_r_training_language | source_sentences_new_length | mlm_train_samples | pppl_has_raw_text | has_tatoeba | tatoeba_test_pairs | has_bible | bible_test_pairs | has_roundtrip | roundtrip_test_rows | has_ner | ner_train_sentences | ner_valid_sentences | ner_test_sentences | has_pos | pos_train_sentences | pos_valid_sentences | pos_test_sentences | region_or_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fur_Latn | Latn | no | 30052 | 901560 | yes | no | 0 | no | 0 | no | 0 | no | 100 | 100 | 100 | no | 0 | 0 | 0 | Europe |
| krc_Cyrl | Cyrl | no | 30353 | 904259 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | North Caucasus |
| acm_Arab | Arab | no | 44505 | 1014273 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | West Asia |
| dzo_Tibt | Tibt | no | 52732 | 1067222 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | Himalaya |
| sat_Olck | Olck | no | 39614 | 979461 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | South Asia |
| mad_Latn | Latn | no | 38993 | 974829 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | Southeast Asia |
| bam_Latn | Latn | no | 32150 | 919998 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | West Africa |
| kjb_Latn | Latn | no | 31471 | 914125 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | Mesoamerica |
| quw_Latn | Latn | no | 33449 | 930995 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | Andean South America |
| rap_Latn | Latn | no | 30102 | 902009 | yes | no | 0 | no | 0 | no | 0 | no | 0 | 0 | 0 | no | 0 | 0 | 0 | Polynesia |

## 102-Language Compact Table

| language_script | group | xlm_r_training_language | source_sentences_new_length | mlm_train_samples | pppl_has_raw_text | has_tatoeba | has_bible | has_ner | has_pos | has_roundtrip | has_taxi1500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lao_Laoo | seen92 | yes | 66966 | 901560 | yes | no | no | no | no | no | no |
| mya_Mymr | seen92 | yes | 945180 | 901560 | yes | no | yes | yes | no | yes | no |
| ara_Arab | seen92 | yes | 24524122 | 901560 | yes | yes | no | yes | yes | no | no |
| mar_Deva | seen92 | yes | 28748897 | 901560 | yes | yes | yes | yes | yes | yes | no |
| hau_Latn | seen92 | yes | 4368483 | 901560 | yes | no | yes | no | no | yes | no |
| uzb_Latn | seen92 | yes | 3223485 | 901560 | yes | no | yes | yes | no | yes | no |
| slv_Latn | seen92 | yes | 15719210 | 901560 | yes | yes | yes | yes | yes | yes | no |
| fin_Latn | seen92 | yes | 16730388 | 901560 | yes | yes | yes | yes | yes | yes | no |
| hun_Latn | seen92 | yes | 18800025 | 901560 | yes | yes | yes | yes | yes | yes | no |
| cmn_Hani | seen92 | yes | 80745 | 901560 | yes | yes | yes | no | no | yes | no |
| est_Latn | seen92 | yes | 13600579 | 901560 | yes | yes | no | yes | yes | no | no |
| bre_Latn | seen92 | yes | 748954 | 901560 | yes | yes | yes | yes | yes | yes | no |
| hrv_Latn | seen92 | yes | 17882932 | 901560 | yes | yes | yes | yes | yes | yes | no |
| jav_Latn | seen92 | yes | 516833 | 901560 | yes | no | yes | yes | yes | yes | no |
| ron_Latn | seen92 | yes | 19190217 | 901560 | yes | yes | yes | yes | yes | yes | no |
| ell_Grek | seen92 | yes | 22033282 | 901560 | yes | yes | yes | yes | yes | yes | no |
| nor_Latn | seen92 | yes | 14576191 | 901560 | yes | no | no | yes | yes | no | no |
| slk_Latn | seen92 | yes | 14633631 | 901560 | yes | yes | yes | yes | yes | yes | no |
| vie_Latn | seen92 | yes | 15697827 | 901560 | yes | yes | yes | yes | yes | yes | no |
| amh_Ethi | seen92 | yes | 2862985 | 901560 | yes | yes | yes | yes | yes | yes | no |
| epo_Latn | seen92 | yes | 8737198 | 901560 | yes | yes | yes | yes | no | yes | no |
| bel_Cyrl | seen92 | yes | 5319675 | 901560 | yes | yes | yes | yes | yes | yes | no |
| xho_Latn | seen92 | yes | 1262364 | 901560 | yes | yes | yes | no | no | yes | no |
| hin_Deva | seen92 | yes | 7046700 | 901560 | yes | yes | yes | yes | yes | yes | no |
| tam_Taml | seen92 | yes | 3388255 | 901560 | yes | yes | yes | yes | yes | yes | no |
| mon_Cyrl | seen92 | yes | 4616960 | 901560 | yes | yes | no | yes | no | no | no |
| ces_Latn | seen92 | yes | 20376340 | 901560 | yes | yes | yes | yes | yes | yes | no |
| san_Deva | seen92 | yes | 165616 | 901560 | yes | no | yes | yes | yes | yes | no |
| hye_Armn | seen92 | yes | 1463123 | 901560 | yes | yes | yes | yes | yes | yes | no |
| pus_Arab | seen92 | yes | 731992 | 901560 | yes | no | no | yes | no | no | no |
| som_Arab | seen92 | yes | 14199 | 901560 | yes | no | no | no | no | no | no |
| kan_Knda | seen92 | yes | 41836495 | 901560 | yes | no | yes | yes | no | yes | no |
| isl_Latn | seen92 | yes | 19547941 | 901560 | yes | yes | yes | yes | yes | yes | no |
| ori_Orya | seen92 | yes | 410827 | 901560 | yes | no | no | yes | no | no | no |
| afr_Latn | seen92 | yes | 5157787 | 901560 | yes | yes | yes | yes | yes | yes | no |
| deu_Latn | seen92 | yes | 31015993 | 901560 | yes | yes | yes | yes | yes | yes | no |
| urd_Arab | seen92 | yes | 6009594 | 901560 | yes | yes | yes | yes | yes | yes | no |
| bul_Cyrl | seen92 | yes | 21823004 | 901560 | yes | yes | yes | yes | yes | yes | no |
| tgl_Latn | seen92 | yes | 7411064 | 901560 | yes | yes | yes | yes | yes | yes | no |
| eus_Latn | seen92 | yes | 12775959 | 901560 | yes | yes | yes | yes | yes | yes | no |
| pol_Latn | seen92 | yes | 19339945 | 901560 | yes | yes | yes | yes | yes | yes | no |
| lat_Latn | seen92 | yes | 1179913 | 901560 | yes | yes | yes | yes | yes | yes | no |
| tur_Latn | seen92 | yes | 29184662 | 901560 | yes | yes | yes | yes | yes | yes | no |
| fra_Latn | seen92 | yes | 39197581 | 901560 | yes | yes | yes | yes | yes | yes | no |
| cat_Latn | seen92 | yes | 8648271 | 901560 | yes | yes | yes | yes | yes | yes | no |
| uig_Arab | seen92 | yes | 307302 | 901560 | yes | yes | yes | yes | yes | yes | no |
| arb_Arab | seen92 | yes | 159884 | 901560 | yes | no | yes | no | no | yes | no |
| sqi_Latn | seen92 | yes | 5526836 | 901560 | yes | yes | yes | yes | yes | yes | no |
| sin_Sinh | seen92 | yes | 7293178 | 901560 | yes | no | yes | yes | yes | yes | no |
| msa_Latn | seen92 | yes | 3929084 | 901560 | yes | no | no | yes | no | no | no |
| swh_Latn | seen92 | yes | 95776 | 901560 | yes | yes | yes | no | no | yes | no |
| kor_Hang | seen92 | yes | 6468444 | 901560 | yes | yes | yes | yes | yes | yes | no |
| ukr_Cyrl | seen92 | yes | 7462046 | 901560 | yes | yes | yes | yes | yes | yes | no |
| kir_Cyrl | seen92 | yes | 1397566 | 901560 | yes | no | yes | yes | no | yes | no |
| yid_Hebr | seen92 | yes | 220214 | 901560 | yes | yes | no | yes | no | no | no |
| heb_Hebr | seen92 | yes | 18128962 | 901560 | yes | yes | yes | yes | yes | yes | no |
| nld_Latn | seen92 | yes | 25061426 | 901560 | yes | yes | yes | yes | yes | yes | no |
| fry_Latn | seen92 | yes | 957422 | 901560 | yes | yes | yes | yes | no | yes | no |
| azb_Arab | seen92 | yes | 33758 | 901560 | yes | no | yes | no | no | yes | no |
| glg_Latn | seen92 | yes | 17852274 | 901560 | yes | yes | no | yes | yes | no | no |
| fas_Arab | seen92 | yes | 18277593 | 901560 | yes | no | no | yes | yes | no | no |
| eng_Latn | seen92 | yes | 36122761 | 901560 | yes | no | no | yes | yes | no | yes |
| mkd_Cyrl | seen92 | yes | 14717004 | 901560 | yes | yes | yes | yes | no | yes | no |
| ind_Latn | seen92 | yes | 23018106 | 901560 | yes | yes | yes | yes | yes | yes | no |
| por_Latn | seen92 | yes | 27824391 | 901560 | yes | yes | yes | yes | yes | yes | no |
| spa_Latn | seen92 | yes | 37286756 | 901560 | yes | yes | yes | yes | yes | yes | no |
| dan_Latn | seen92 | yes | 19174573 | 901560 | yes | yes | yes | yes | yes | yes | no |
| khm_Khmr | seen92 | yes | 590429 | 901560 | yes | yes | yes | yes | no | yes | no |
| gla_Latn | seen92 | yes | 152563 | 901560 | yes | yes | yes | yes | yes | yes | no |
| uig_Latn | seen92 | yes | 9637 | 901560 | yes | no | yes | no | no | yes | no |
| kat_Geor | seen92 | yes | 1004297 | 901560 | yes | yes | yes | yes | no | yes | no |
| mlg_Latn | seen92 | yes | 3715802 | 901560 | yes | no | no | yes | no | no | no |
| snd_Arab | seen92 | yes | 488730 | 901560 | yes | no | yes | yes | no | yes | no |
| ita_Latn | seen92 | yes | 23539857 | 901560 | yes | yes | yes | yes | yes | yes | no |
| hau_Arab | seen92 | yes | 9593 | 901560 | yes | no | no | no | no | no | no |
| cym_Latn | seen92 | yes | 1244783 | 901560 | yes | yes | yes | yes | yes | yes | no |
| srp_Latn | seen92 | yes | 18371769 | 901560 | yes | yes | yes | no | yes | yes | no |
| zho_Hani | seen92 | yes | 24143786 | 901560 | yes | no | no | yes | yes | no | no |
| tha_Thai | seen92 | yes | 7735209 | 901560 | yes | yes | yes | yes | yes | yes | no |
| swe_Latn | seen92 | yes | 20725883 | 901560 | yes | yes | yes | yes | yes | yes | no |
| pan_Guru | seen92 | yes | 29052537 | 901560 | yes | no | yes | yes | no | yes | no |
| prs_Arab | seen92 | yes | 26823 | 901560 | yes | no | yes | no | no | yes | no |
| pes_Arab | seen92 | yes | 57511 | 901560 | yes | yes | yes | no | no | yes | no |
| san_Latn | seen92 | yes | 25742 | 901560 | yes | no | yes | no | no | yes | no |
| kaz_Cyrl | seen92 | yes | 12378727 | 901560 | yes | yes | yes | yes | yes | yes | no |
| kur_Latn | seen92 | yes | 407169 | 901560 | yes | yes | no | yes | no | no | no |
| mal_Mlym | seen92 | yes | 48098273 | 901560 | yes | yes | yes | yes | yes | yes | no |
| nep_Deva | seen92 | yes | 1317291 | 901560 | yes | no | yes | yes | no | yes | no |
| gle_Latn | seen92 | yes | 7225513 | 901560 | yes | yes | yes | yes | yes | yes | no |
| swa_Latn | seen92 | yes | 5989369 | 901560 | yes | no | no | yes | no | no | no |
| som_Latn | seen92 | yes | 3916769 | 901560 | yes | no | yes | yes | no | yes | no |
| lit_Latn | seen92 | yes | 12479626 | 901560 | yes | yes | yes | yes | yes | yes | no |
| fur_Latn | target10 | no | 30052 | 901560 | yes | no | no | no | no | no | no |
| krc_Cyrl | target10 | no | 30353 | 904259 | yes | no | no | no | no | no | no |
| acm_Arab | target10 | no | 44505 | 1014273 | yes | no | no | no | no | no | no |
| dzo_Tibt | target10 | no | 52732 | 1067222 | yes | no | no | no | no | no | no |
| sat_Olck | target10 | no | 39614 | 979461 | yes | no | no | no | no | no | no |
| mad_Latn | target10 | no | 38993 | 974829 | yes | no | no | no | no | no | no |
| bam_Latn | target10 | no | 32150 | 919998 | yes | no | no | no | no | no | no |
| kjb_Latn | target10 | no | 31471 | 914125 | yes | no | no | no | no | no | no |
| quw_Latn | target10 | no | 33449 | 930995 | yes | no | no | no | no | no | no |
| rap_Latn | target10 | no | 30102 | 902009 | yes | no | no | no | no | no | no |

## Full Machine-Readable Table

Full per-language counts are available here:

```text
docs/exp/v5/0_tokenizer/00_data_scope/data_composition_by_language.tsv
```

Important full-table columns include:

- `source_sentences_new_length`, `source_sentences_original`
- `mlm_train_samples`, `mlm_valid_samples`, `mlm_test_samples`
- `tatoeba_test_pairs`, `bible_test_pairs`, `roundtrip_test_rows`
- `taxi_train_rows`, `taxi_valid_rows`, `taxi_test_rows`
- `ner_train_sentences`, `ner_valid_sentences`, `ner_test_sentences`
- `pos_train_sentences`, `pos_valid_sentences`, `pos_test_sentences`
- task inclusion flags: `has_tatoeba`, `has_bible`, `has_roundtrip`,
  `has_taxi1500`, `has_ner`, `has_pos`

## Reporting Notes

- For report/PPT tables, use `mlm_train_samples` when discussing continued-MLM
  data balance.
- Use task-specific counts only for downstream coverage claims.
- Do not describe missing target10 downstream task rows as model failures; they
  are task coverage limitations.
- If a target language has local task files but the corresponding `has_*` gate is
  `no`, report it as an actual local intersection only; do not generalize it to
  target10-wide downstream coverage.
- Glot500-base remains an external/reference checkpoint, not an equal-budget
  v5 baseline.
