# v5.1 Strict Data Composition

Last checked: 2026-06-28 17:53 KST

이 문서는 v5.1 strict rerun의 언어별 데이터 구성을 정리한다. v5.1은 Glot500
raw text subset `102`개 language-script를 유지하되, `92`개 XLM-R 학습 포함
언어와 downstream-aware target10을 분리한다.

## Split Rule

- Glot500 방식에 맞춰 각 language-script에서 dev `1000`, test `1000`을 먼저
  제외하고, merge/tokenizer/continued MLM은 train만 사용한다.
- 현재 기본 split manifest는 `count_source=arrow` verified output이며 status는
  `PASS`다. 이전 stats-based planning file은 `*.stats_plan.*`로 보존한다.
- 실제 Arrow row count가 작은 `azb_Arab`, `uig_Latn`, `san_Latn`에는
  `small_policy=shrink`를 적용한다.
- `dev_examples`와 `test_examples`는 PPPL/MLM evaluation 후보 hold-out이다.
  train-source PPPL과 섞지 않는다.

## Summary

| Item | Value |
| --- | ---: |
| total language-scripts | 102 |
| seen/head language-scripts | 92 |
| target/tail language-scripts | 10 |
| XLM-R training language yes | 92 |
| XLM-R training language no | 10 |
| source examples | 1169433406 |
| train examples after hold-out | 1169231705 |
| dev examples | 100850 |
| test examples | 100851 |
| PLAN_UNVERIFIED rows | 0 |

## Dataset / Task Overlap

| dataset_or_metric | total | seen92 | target10 |
| --- | --- | --- | --- |
| pppl | 102 | 92 | 10 |
| tatoeba | 66 | 63 | 3 |
| bible | 80 | 74 | 6 |
| roundtrip | 80 | 74 | 6 |
| taxi1500 | 1 | 1 | 0 |
| ner | 84 | 78 | 6 |
| pos | 58 | 58 | 0 |

Interpretation:

- PPPL/MLM raw-text coverage is `102 = seen92 92 + target10 10`.
- v5.1 target10 flags are parsed from
  `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`, because v5 old
  coverage files used a different target10.
- v5.1 target10 has downstream coverage for Bible/Roundtrip/NER/Tatoeba where
  local task data exists.
- POS and Taxi1500 still have `0/10` target10 coverage, so those metrics are
  all/head replay evidence, not target-side novelty evidence.

## Target10 Train/Dev/Test And Task Coverage

| language_script | region | xlm_r_training_language | source_examples | train_examples | dev_examples | test_examples | has_pppl | has_tatoeba | has_bible | has_roundtrip | has_ner | has_pos | has_taxi1500 | split_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| guj_Gujr | South Asia | no | 45738247 | 45736247 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| asm_Beng | South Asia | no | 1876644 | 1874644 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| srp_Cyrl | Southeast Europe | no | 3863064 | 3861064 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| sun_Latn | Southeast Asia | no | 2546902 | 2544902 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| zsm_Latn | Southeast Asia | no | 849033 | 847033 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| aze_Latn | Caucasus/West Asia | no | 46292511 | 46290511 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| fil_Latn | Southeast Asia | no | 33484266 | 33482266 | 1000 | 1000 | yes | no | yes | yes | no | no | no | PASS |
| bos_Latn | Southeast Europe | no | 11012783 | 11010783 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| dzo_Tibt | Himalaya | no | 44100 | 42100 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |
| sat_Olck | South Asia | no | 37581 | 35581 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |

## 102-Language Compact Table

| rank | language_script | group | xlm_r_training_language | train_examples | dev_examples | test_examples | has_pppl | has_tatoeba | has_bible | has_roundtrip | has_ner | has_pos | has_taxi1500 | split_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | lao_Laoo | seen92 | yes | 54337 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |
| 2 | mya_Mymr | seen92 | yes | 909018 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 3 | ara_Arab | seen92 | yes | 24519525 | 1000 | 1000 | yes | yes | no | no | yes | yes | no | PASS |
| 4 | mar_Deva | seen92 | yes | 28747662 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 5 | hau_Latn | seen92 | yes | 4359657 | 1000 | 1000 | yes | no | yes | yes | no | no | no | PASS |
| 6 | uzb_Latn | seen92 | yes | 3180187 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 7 | slv_Latn | seen92 | yes | 15716268 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 8 | fin_Latn | seen92 | yes | 16727345 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 9 | hun_Latn | seen92 | yes | 18796712 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 10 | cmn_Hani | seen92 | yes | 55500 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| 11 | est_Latn | seen92 | yes | 13596009 | 1000 | 1000 | yes | yes | no | no | yes | yes | no | PASS |
| 12 | bre_Latn | seen92 | yes | 729939 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 13 | hrv_Latn | seen92 | yes | 17879552 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 14 | jav_Latn | seen92 | yes | 445504 | 1000 | 1000 | yes | no | yes | yes | yes | yes | no | PASS |
| 15 | ron_Latn | seen92 | yes | 19187651 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 16 | ell_Grek | seen92 | yes | 22029905 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 17 | nor_Latn | seen92 | yes | 14526502 | 1000 | 1000 | yes | no | no | no | yes | yes | no | PASS |
| 18 | slk_Latn | seen92 | yes | 14632178 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 19 | vie_Latn | seen92 | yes | 15585157 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 20 | amh_Ethi | seen92 | yes | 2833527 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 21 | epo_Latn | seen92 | yes | 8734217 | 1000 | 1000 | yes | yes | yes | yes | yes | no | no | PASS |
| 22 | bel_Cyrl | seen92 | yes | 5316656 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 23 | xho_Latn | seen92 | yes | 1199261 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| 24 | hin_Deva | seen92 | yes | 7002172 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 25 | tam_Taml | seen92 | yes | 3362892 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 26 | mon_Cyrl | seen92 | yes | 4612949 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| 27 | ces_Latn | seen92 | yes | 20372860 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 28 | san_Deva | seen92 | yes | 153070 | 1000 | 1000 | yes | no | yes | yes | yes | yes | no | PASS |
| 29 | hye_Armn | seen92 | yes | 1411139 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 30 | pus_Arab | seen92 | yes | 728035 | 1000 | 1000 | yes | no | no | no | yes | no | no | PASS |
| 31 | som_Arab | seen92 | yes | 10203 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |
| 32 | kan_Knda | seen92 | yes | 41803904 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 33 | isl_Latn | seen92 | yes | 19544858 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 34 | ori_Orya | seen92 | yes | 400076 | 1000 | 1000 | yes | no | no | no | yes | no | no | PASS |
| 35 | afr_Latn | seen92 | yes | 5154807 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 36 | deu_Latn | seen92 | yes | 31013917 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 37 | urd_Arab | seen92 | yes | 6006751 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 38 | bul_Cyrl | seen92 | yes | 21820051 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 39 | tgl_Latn | seen92 | yes | 7407827 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 40 | eus_Latn | seen92 | yes | 12772851 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 41 | pol_Latn | seen92 | yes | 19336808 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 42 | lat_Latn | seen92 | yes | 1147896 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 43 | tur_Latn | seen92 | yes | 29180577 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 44 | fra_Latn | seen92 | yes | 39194744 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 45 | cat_Latn | seen92 | yes | 8630854 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 46 | uig_Arab | seen92 | yes | 296694 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 47 | arb_Arab | seen92 | yes | 7697 | 1000 | 1000 | yes | no | yes | yes | no | no | no | PASS |
| 48 | sqi_Latn | seen92 | yes | 5471093 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 49 | sin_Sinh | seen92 | yes | 7290412 | 1000 | 1000 | yes | no | yes | yes | yes | yes | no | PASS |
| 50 | msa_Latn | seen92 | yes | 3892332 | 1000 | 1000 | yes | no | no | no | yes | no | no | PASS |
| 51 | swh_Latn | seen92 | yes | 41876 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| 52 | kor_Hang | seen92 | yes | 6346091 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 53 | ukr_Cyrl | seen92 | yes | 7435153 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 54 | kir_Cyrl | seen92 | yes | 1332662 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 55 | yid_Hebr | seen92 | yes | 216222 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| 56 | heb_Hebr | seen92 | yes | 18124264 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 57 | nld_Latn | seen92 | yes | 25058543 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 58 | fry_Latn | seen92 | yes | 923801 | 1000 | 1000 | yes | yes | yes | yes | yes | no | no | PASS |
| 59 | azb_Arab | seen92 | yes | 1 | 940 | 940 | yes | no | yes | yes | no | no | no | PASS |
| 60 | glg_Latn | seen92 | yes | 17846822 | 1000 | 1000 | yes | yes | no | no | yes | yes | no | PASS |
| 61 | fas_Arab | seen92 | yes | 18235931 | 1000 | 1000 | yes | no | no | no | yes | yes | no | PASS |
| 62 | eng_Latn | seen92 | yes | 36119560 | 1000 | 1000 | yes | no | no | no | yes | yes | yes | PASS |
| 63 | mkd_Cyrl | seen92 | yes | 14713827 | 1000 | 1000 | yes | yes | yes | yes | yes | no | no | PASS |
| 64 | ind_Latn | seen92 | yes | 23015064 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 65 | por_Latn | seen92 | yes | 27820986 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 66 | spa_Latn | seen92 | yes | 37283157 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 67 | dan_Latn | seen92 | yes | 19170974 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 68 | khm_Khmr | seen92 | yes | 563794 | 1000 | 1000 | yes | yes | yes | yes | yes | no | no | PASS |
| 69 | gla_Latn | seen92 | yes | 122953 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 70 | uig_Latn | seen92 | yes | 1 | 852 | 852 | yes | no | yes | yes | no | no | no | PASS |
| 71 | kat_Geor | seen92 | yes | 988785 | 1000 | 1000 | yes | yes | yes | yes | yes | no | no | PASS |
| 72 | mlg_Latn | seen92 | yes | 3701137 | 1000 | 1000 | yes | no | no | no | yes | no | no | PASS |
| 73 | snd_Arab | seen92 | yes | 476110 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 74 | ita_Latn | seen92 | yes | 23536832 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 75 | hau_Arab | seen92 | yes | 5594 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |
| 76 | cym_Latn | seen92 | yes | 1161276 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 77 | srp_Latn | seen92 | yes | 18369143 | 1000 | 1000 | yes | yes | yes | yes | no | yes | no | PASS |
| 78 | zho_Hani | seen92 | yes | 24071937 | 1000 | 1000 | yes | no | no | no | yes | yes | no | PASS |
| 79 | tha_Thai | seen92 | yes | 7625697 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 80 | swe_Latn | seen92 | yes | 20723321 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 81 | pan_Guru | seen92 | yes | 29023289 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 82 | prs_Arab | seen92 | yes | 8753 | 1000 | 1000 | yes | no | yes | yes | no | no | no | PASS |
| 83 | pes_Arab | seen92 | yes | 16762 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| 84 | san_Latn | seen92 | yes | 1 | 58 | 59 | yes | no | yes | yes | no | no | no | PASS |
| 85 | kaz_Cyrl | seen92 | yes | 12343817 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 86 | kur_Latn | seen92 | yes | 403169 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| 87 | mal_Mlym | seen92 | yes | 48093393 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 88 | nep_Deva | seen92 | yes | 1297063 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 89 | gle_Latn | seen92 | yes | 7176230 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 90 | swa_Latn | seen92 | yes | 5985318 | 1000 | 1000 | yes | no | no | no | yes | no | no | PASS |
| 91 | som_Latn | seen92 | yes | 3913898 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 92 | lit_Latn | seen92 | yes | 12423629 | 1000 | 1000 | yes | yes | yes | yes | yes | yes | no | PASS |
| 93 | guj_Gujr | target10 | no | 45736247 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 94 | asm_Beng | target10 | no | 1874644 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 95 | srp_Cyrl | target10 | no | 3861064 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 96 | sun_Latn | target10 | no | 2544902 | 1000 | 1000 | yes | no | yes | yes | yes | no | no | PASS |
| 97 | zsm_Latn | target10 | no | 847033 | 1000 | 1000 | yes | yes | yes | yes | no | no | no | PASS |
| 98 | aze_Latn | target10 | no | 46290511 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| 99 | fil_Latn | target10 | no | 33482266 | 1000 | 1000 | yes | no | yes | yes | no | no | no | PASS |
| 100 | bos_Latn | target10 | no | 11010783 | 1000 | 1000 | yes | yes | no | no | yes | no | no | PASS |
| 101 | dzo_Tibt | target10 | no | 42100 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |
| 102 | sat_Olck | target10 | no | 35581 | 1000 | 1000 | yes | no | no | no | no | no | no | PASS |

## Full Machine-Readable Table

```text
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.tsv
```

Important columns:

- `source_examples`, `train_examples`, `dev_examples`, `test_examples`
- `xlm_r_training_language`, `group`
- task flags: `has_pppl`, `has_tatoeba`, `has_bible`, `has_roundtrip`,
  `has_ner`, `has_pos`, `has_taxi1500`
- `split_status`, `split_notes`
