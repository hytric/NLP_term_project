# Low-resource Table 3 Candidate Audit

Scope: non-XLM-R Glot500 tail language-scripts from `miscellaneous/languages_stats.csv`.
Known Table 3 task-list columns use local per-language lists for Tatoeba/Bible/NER/POS. Text Classification and original Roundtrip full language lists are not present in this repo; Roundtrip is reported as local JSONL or Bible-derived proxy only.

## Bucket Summary

| resource_bucket | tail_total_in_glot500_stats | any_known_table3_task_list | any_actionable_task | tatoeba_list | bible_list | bible_source_ready | ner_list | pos_list | roundtrip_bible_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lt30k | 109 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 30k_50k | 113 | 89 | 85 | 4 | 75 | 71 | 12 | 4 | 71 |
| 50k_100k | 70 | 40 | 36 | 0 | 34 | 32 | 6 | 8 | 32 |
| 100k_300k | 124 | 79 | 77 | 7 | 69 | 66 | 13 | 6 | 66 |
| 300k_1M | 101 | 70 | 69 | 9 | 56 | 56 | 23 | 6 | 56 |
| 1M_10M | 52 | 45 | 45 | 8 | 41 | 40 | 20 | 3 | 40 |
| 10M_plus | 10 | 10 | 10 | 4 | 8 | 6 | 8 | 2 | 6 |

## Low-resource Interpretation

- `30k_50k` and `50k_100k` are the strict low-resource zone used for conservative target selection.
- `100k_300k` is still low-resource relative to the long-tailed Glot500 distribution and gives more downstream coverage.
- Bible tail coverage is the main source of low-resource Table 3 evaluability; Tatoeba/NER/POS are much sparser.
- For Roundtrip, `RoundtripBibleProxy` means the Bible source is ready enough to materialize a local roundtrip input, not that the original Table 3 288-language list was recovered.

## Actionable Low-resource Candidates Under 300k

| language_script | language_name | new_length | resource_bucket | task_list_tasks | actionable_tasks | bible_shared_verses |
| --- | --- | --- | --- | --- | --- | --- |
| mhr_Cyrl | Eastern Mari | 100474 | 100k_300k | Tatoeba,Bible,NER | Tatoeba,Bible,NER,RoundtripBibleProxy | 7842 |
| cbk_Latn | Chavacano | 118789 | 100k_300k | Tatoeba,Bible,NER | Tatoeba,Bible,NER,RoundtripBibleProxy | 7926 |
| dtp_Latn | Kadazan Dusun | 48468 | 30k_50k | Tatoeba,Bible | Tatoeba,Bible,RoundtripBibleProxy | 7887 |
| ace_Latn | Achinese | 59333 | 50k_100k | Bible,NER | Bible,NER,RoundtripBibleProxy | 7887 |
| lzh_Hani | Literary Chinese | 86035 | 50k_100k | Bible,NER,POS | Bible,NER,RoundtripBibleProxy | 7929 |
| kab_Latn | Kabyle | 176015 | 100k_300k | Tatoeba,Bible | Tatoeba,Bible,RoundtripBibleProxy | 7918 |
| kaa_Latn | Kara-Kalpak | 30031 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7880 |
| pls_Latn | San Marcos Tlacoyalco Popoloca | 30136 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7930 |
| mrw_Latn |  | 30304 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7937 |
| tuc_Latn | Mutu | 30349 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7639 |
| krc_Cyrl | Karachay-Balkar | 30353 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7936 |
| mwm_Latn |  | 30432 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7926 |
| hra_Latn |  | 30472 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7930 |
| mzh_Latn | Wichí Lhamtés Güisnay | 30517 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7817 |
| ksd_Latn | Kuanua | 30550 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| ifa_Latn |  | 30621 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7926 |
| mcn_Latn |  | 30666 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7939 |
| kmm_Latn |  | 30671 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7896 |
| rug_Latn | Roviana | 30857 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7913 |
| izz_Latn |  | 30894 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| ifb_Latn |  | 30980 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7902 |
| tui_Latn |  | 31161 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7934 |
| zlm_Latn | Malay (individual language) | 31345 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7939 |
| wbm_Latn | Wa | 31394 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| hne_Deva | Chhattisgarhi | 31465 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| kjb_Latn | Q'anjob'al | 31471 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7907 |
| cuk_Latn | San Blas Kuna | 31612 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| xav_Latn | Xavánte | 31765 | 30k_50k | Bible,POS | Bible,RoundtripBibleProxy | 7418 |
| yan_Latn |  | 31775 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7916 |
| tca_Latn | Ticuna | 31852 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7727 |
| rop_Latn | Kriol | 31889 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7649 |
| caq_Latn |  | 31903 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| nmf_Latn |  | 31997 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7939 |
| jam_Latn | Jamaican Creole English | 32048 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| prk_Latn |  | 32085 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| bam_Latn | Bambara | 32150 | 30k_50k | Bible,POS | Bible,RoundtripBibleProxy | 7933 |
| tbz_Latn | Ditammari | 32264 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7932 |
| suz_Deva | Sunwar | 32811 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| tlh_Latn | Klingon | 32863 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7936 |
| mbb_Latn |  | 33240 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7850 |
| ixl_Latn | Ixil | 33289 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7799 |
| quw_Latn | Tena Lowland Quichua | 33449 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| tpm_Latn |  | 33517 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7903 |
| csb_Latn | Kashubian | 33743 | 30k_50k | Tatoeba,NER | Tatoeba,NER | 0 |
| csy_Latn | Siyin Chin | 34126 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7907 |
| aoj_Latn | Mufian | 34349 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7811 |
| kpg_Latn | Kapingamarangi | 34900 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7919 |
| hui_Latn | Huli | 34926 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7841 |
| giz_Latn |  | 35040 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| knv_Latn | Tabo | 35196 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7782 |
| agw_Latn |  | 35585 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7934 |
| gya_Latn |  | 35902 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7932 |
| bts_Latn |  | 36216 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| mdy_Ethi |  | 36370 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7928 |
| bim_Latn |  | 36835 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7891 |
| bqc_Latn | Boko (Benin) | 36881 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7921 |
| zom_Latn |  | 37013 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7919 |
| sba_Latn |  | 38040 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7939 |
| ikk_Latn | Ika | 38071 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| hnj_Latn | Hmong Njua | 38611 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7932 |
| cac_Latn |  | 38812 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7905 |
| mad_Latn | Madurese | 38993 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7886 |
| enm_Latn | Middle English (1100-1500) | 39809 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| crh_Cyrl | Crimean Tatar | 39985 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 4750 |
| kia_Latn |  | 40035 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7938 |
| teo_Latn | Teso | 40203 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| ium_Latn |  | 40683 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7928 |
| gor_Latn | Gorontalo | 41174 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7885 |
| tih_Latn |  | 41873 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7906 |
| myv_Cyrl | Erzya | 42147 | 30k_50k | Bible,POS | Bible,RoundtripBibleProxy | 7927 |
| npi_Deva | Nepali (individual language) | 43072 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7888 |
| ach_Latn | Acoli | 43974 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| tob_Latn |  | 44473 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7768 |
| quh_Latn | South Bolivian Quechua | 45566 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7892 |
| poh_Latn | Poqomchi' | 46454 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7941 |
| lam_Latn |  | 46853 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7940 |
| acr_Latn | Achi | 48886 | 30k_50k | Bible | Bible,RoundtripBibleProxy | 7914 |
| gkp_Latn |  | 50549 | 50k_100k | Bible | Bible,RoundtripBibleProxy | 7933 |
| mps_Latn | Dadibi | 50645 | 50k_100k | Bible | Bible,RoundtripBibleProxy | 7849 |
| sxn_Latn |  | 51749 | 50k_100k | Bible | Bible,RoundtripBibleProxy | 7886 |

Full TSV rows: 333; strict 30k-100k rows with any known task list: 129; low <300k rows with any known task list: 208.
