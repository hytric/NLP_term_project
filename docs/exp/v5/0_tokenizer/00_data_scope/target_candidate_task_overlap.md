# v5 Target Candidate Downstream Overlap Audit

This audit intersects non-XLM-R Glot500 candidates with local downstream task resources.

## Summary

- candidate_count: `318`
- candidates_with_any_downstream: `8`
- current_target10_with_any_downstream: `0`
- task_counts: `{"bible": 6, "ner": 6, "pos": 0, "roundtrip": 6, "tatoeba": 3}`
- score_distribution: `{"0": 310, "2": 3, "3": 5}`

## Candidates With Any Downstream Coverage

| language_script | language_name | script | new_length | target_task_count | has_tatoeba | has_bible | has_roundtrip | has_ner | has_pos | bible_shared_verses |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| guj_Gujr | Gujarati | Gujr | 45738685 | 3 | no | yes | yes | yes | no | 7883 |
| srp_Cyrl | Serbian | Cyrl | 3864091 | 3 | no | yes | yes | yes | no | 7941 |
| sun_Latn | Sundanese | Latn | 2586011 | 3 | no | yes | yes | yes | no | 7938 |
| asm_Beng | Assamese | Beng | 1882353 | 3 | no | yes | yes | yes | no | 7939 |
| zsm_Latn | Standard Malay | Latn | 859947 | 3 | yes | yes | yes | no | no | 7888 |
| aze_Latn | Azerbaijani | Latn | 46300705 | 2 | yes | no | no | yes | no | 0 |
| fil_Latn | Filipino | Latn | 33493255 | 2 | no | yes | yes | no | no | 7941 |
| bos_Latn | Bosnian | Latn | 11014744 | 2 | yes | no | no | yes | no | 0 |

## Current v5 Target10

| language_script | language_name | script | new_length | target_task_count | has_tatoeba | has_bible | has_roundtrip | has_ner | has_pos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fur_Latn | Friulian | Latn | 30052 | 0 | no | no | no | no | no |
| rap_Latn | Rapanui | Latn | 30102 | 0 | no | no | no | no | no |
| krc_Cyrl | Karachay-Balkar | Cyrl | 30353 | 0 | no | no | no | no | no |
| kjb_Latn | Q'anjob'al | Latn | 31471 | 0 | no | no | no | no | no |
| bam_Latn | Bambara | Latn | 32150 | 0 | no | no | no | no | no |
| quw_Latn | Tena Lowland Quichua | Latn | 33449 | 0 | no | no | no | no | no |
| mad_Latn | Madurese | Latn | 38993 | 0 | no | no | no | no | no |
| sat_Olck | Santali | Olck | 39614 | 0 | no | no | no | no | no |
| acm_Arab | Mesopotamian Arabic | Arab | 44505 | 0 | no | no | no | no | no |
| dzo_Tibt | Dzongkha | Tibt | 52732 | 0 | no | no | no | no | no |

## Recommended If Target Downstream Matters

Use the eight candidates that have any local downstream coverage, then keep two PPPL-only anchors for script diversity.

| language_script | language_name | script | new_length | target_task_count | has_tatoeba | has_bible | has_roundtrip | has_ner | has_pos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| guj_Gujr | Gujarati | Gujr | 45738685 | 3 | no | yes | yes | yes | no |
| asm_Beng | Assamese | Beng | 1882353 | 3 | no | yes | yes | yes | no |
| srp_Cyrl | Serbian | Cyrl | 3864091 | 3 | no | yes | yes | yes | no |
| sun_Latn | Sundanese | Latn | 2586011 | 3 | no | yes | yes | yes | no |
| zsm_Latn | Standard Malay | Latn | 859947 | 3 | yes | yes | yes | no | no |
| aze_Latn | Azerbaijani | Latn | 46300705 | 2 | yes | no | no | yes | no |
| fil_Latn | Filipino | Latn | 33493255 | 2 | no | yes | yes | no | no |
| bos_Latn | Bosnian | Latn | 11014744 | 2 | yes | no | no | yes | no |
| dzo_Tibt | Dzongkha | Tibt | 52732 | 0 | no | no | no | no | no |
| sat_Olck | Santali | Olck | 39614 | 0 | no | no | no | no | no |
