# v5.1 Strict Split Verification

Last checked: 2026-06-28 17:53 KST

The original v5.1 split manifest was created from `new_length` stats. This
verification recounts the actual local Arrow shards with `pyarrow.ipc.open_stream`
and promotes the Arrow-count manifest to the default strict split contract.

## Summary

| Item | Value |
| --- | ---: |
| verified languages | 102 |
| rows with source-count delta | 102 |
| stats source examples | 1171467571 |
| Arrow source examples | 1169433406 |
| Arrow dev examples | 100850 |
| Arrow test examples | 100851 |
| rows requiring small-policy shrink | 3 |
| verified manifest status | PASS |

## Shrink Exceptions

These languages have fewer than `dev=1000 + test=1000 + min_train=1` actual
Arrow examples, so v5.1 keeps one train example and shrinks dev/test.

| language_script | stats_source_examples | arrow_source_examples | delta_arrow_minus_stats | stats_dev_examples | arrow_dev_examples | stats_test_examples | arrow_test_examples | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| azb_Arab | 33758 | 1881 | -31877 | 1000 | 940 | 1000 | 940 | PASS | count_source=arrow; small_policy=shrink; requested_dev=1000; requested_test=1000; min_train=1 |
| uig_Latn | 9637 | 1705 | -7932 | 1000 | 852 | 1000 | 852 | PASS | count_source=arrow; small_policy=shrink; requested_dev=1000; requested_test=1000; min_train=1 |
| san_Latn | 25742 | 118 | -25624 | 1000 | 58 | 1000 | 59 | PASS | count_source=arrow; small_policy=shrink; requested_dev=1000; requested_test=1000; min_train=1 |

## Largest Source-Count Deltas

| language_script | stats_source_examples | arrow_source_examples | delta_arrow_minus_stats | stats_dev_examples | arrow_dev_examples | stats_test_examples | arrow_test_examples | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arb_Arab | 159884 | 9697 | -150187 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| kor_Hang | 6468444 | 6348091 | -120353 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| vie_Latn | 15697827 | 15587157 | -110670 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| tha_Thai | 7735209 | 7627697 | -107512 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| cym_Latn | 1244783 | 1163276 | -81507 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| zho_Hani | 24143786 | 24073937 | -69849 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| jav_Latn | 516833 | 447504 | -69329 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| kir_Cyrl | 1397566 | 1334662 | -62904 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| xho_Latn | 1262364 | 1201261 | -61103 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| lit_Latn | 12479626 | 12425629 | -53997 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| sqi_Latn | 5526836 | 5473093 | -53743 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| swh_Latn | 95776 | 43876 | -51900 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| hye_Armn | 1463123 | 1413139 | -49984 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| nor_Latn | 14576191 | 14528502 | -47689 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| gle_Latn | 7225513 | 7178230 | -47283 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| hin_Deva | 7046700 | 7004172 | -42528 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| uzb_Latn | 3223485 | 3182187 | -41298 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| fas_Arab | 18277593 | 18237931 | -39662 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| sun_Latn | 2586011 | 2546902 | -39109 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |
| pes_Arab | 57511 | 18762 | -38749 | 1000 | 1000 | 1000 | 1000 | PASS | count_source=arrow |

## Files

```text
strict_split_manifest.tsv                 # Arrow-verified default manifest
strict_split_indices.jsonl                # Arrow-verified default indices
strict_split_manifest.stats_plan.tsv      # preserved stats-based plan
strict_split_indices.stats_plan.jsonl     # preserved stats-based indices
strict_split_verification_mismatches.tsv  # full comparison table
```
