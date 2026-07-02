# Table 1. v5 Data Scope

Last updated: 2026-06-27

Caption draft:

```text
v5 reproduces the Glot500 training pattern on a controlled 102-language-script
subset: 92 XLM-R-seen Glot500 languages and 10 diverse Glot500-internal target
languages that are not XLM-R seen and satisfy the 30K-row inclusion threshold.
```

| Item | Value |
| --- | ---: |
| seen/head language-scripts | 92 |
| target/tail language-scripts | 10 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 363,421 |
| planned seen samples | 82,943,520 |
| planned target samples | 9,508,731 |
| planned total samples | 92,452,251 |
| actual merged lines | 92,452,251 |
| merged corpus size | 19G |
| missing language dirs | 0 |

Selected target10:

| Language-script | Region / script note |
| --- | --- |
| `fur_Latn` | Europe, Latin |
| `krc_Cyrl` | North Caucasus, Cyrillic |
| `acm_Arab` | West Asia, Arabic |
| `dzo_Tibt` | Himalaya, Tibetan |
| `sat_Olck` | South Asia, Ol Chiki |
| `mad_Latn` | Southeast Asia, Latin |
| `bam_Latn` | West Africa, Latin |
| `kjb_Latn` | Mesoamerica, Latin |
| `quw_Latn` | Andean South America, Latin |
| `rap_Latn` | Polynesia, Latin |

Source artifacts:

- `docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`
- `docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv`
- `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`

