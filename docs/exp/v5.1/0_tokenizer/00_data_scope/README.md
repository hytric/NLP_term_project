# v5.1 Data Scope

## Selection Summary

| language_script | source sentences | coverage |
| --- | ---: | --- |
| `guj_Gujr` | 45,738,685 | Bible, Roundtrip, NER |
| `asm_Beng` | 1,882,353 | Bible, Roundtrip, NER |
| `srp_Cyrl` | 3,864,091 | Bible, Roundtrip, NER |
| `sun_Latn` | 2,586,011 | Bible, Roundtrip, NER |
| `zsm_Latn` | 859,947 | Tatoeba, Bible, Roundtrip |
| `aze_Latn` | 46,300,705 | Tatoeba, NER |
| `fil_Latn` | 33,493,255 | Bible, Roundtrip |
| `bos_Latn` | 11,014,744 | Tatoeba, NER |
| `dzo_Tibt` | 52,732 | PPPL-only script anchor |
| `sat_Olck` | 39,614 | PPPL-only script anchor |

## Coverage Counts

| Target coverage | Count |
| --- | ---: |
| any downstream | 8/10 |
| Bible retrieval | 6/10 |
| Roundtrip alignment | 6/10 |
| NER | 6/10 |
| Tatoeba retrieval | 3/10 |
| POS | 0/10 |
| Taxi1500 | 0/10 |

## Generated Files

```text
docs/exp/v5.1/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv
docs/exp/v5.1/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv
docs/exp/v5.1/0_tokenizer/miscellaneous/glot500_candidate_pool_min30k.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_manifest.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_verification_summary.md
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_verification_mismatches.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.md
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_summary.json
docs/exp/v5.1/0_tokenizer/merge/Glot500_v51_glot50010_xlmr100.manifest.tsv
docs/exp/v5.1/0_tokenizer/merge/Glot500_v51_glot50010_xlmr100.report.json
```

## Strict Split / Task Overlap Table

Main table:

```text
strict_data_composition_by_language.md
```

Key counts:

| 범위 | total | seen92 | target10 |
| --- | ---: | ---: | ---: |
| PPPL / raw text | 102 | 92 | 10 |
| Tatoeba retrieval | 66 | 63 | 3 |
| Bible retrieval | 80 | 74 | 6 |
| Roundtrip alignment | 80 | 74 | 6 |
| NER | 84 | 78 | 6 |
| POS | 58 | 58 | 0 |
| Taxi1500 | 1 | 1 | 0 |

The split manifest is now Arrow-verified and has status `PASS`. The preserved
stats-based planning files are:

```text
strict_split_manifest.stats_plan.tsv
strict_split_indices.stats_plan.jsonl
```

Three small seen languages use `small_policy=shrink`: `azb_Arab`, `uig_Latn`,
and `san_Latn`.

## Repro Command

```bash
python3 preprocessing/prepare_v5_glot50010_merge_inputs.py \
  --selection_strategy downstream_aware \
  --v5_raw /home/axt/mnt2/jongha/v5_1_glot50010/raw \
  --stats_out docs/exp/v5.1/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv \
  --target_manifest_out docs/exp/v5.1/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv \
  --candidate_pool_out docs/exp/v5.1/0_tokenizer/miscellaneous/glot500_candidate_pool_min30k.tsv \
  --overwrite_links \
  --prune_raw_links
```
