# v5.1 Dataset Size Audit

Last generated: 2026-06-28 19:19 KST

이 문서는 v5.1 strict rerun에서 실제로 쓰는 데이터 양을 task별로 고정한다.
이 프로젝트가 좋은 점은 raw split, coverage, materialization 결과가 이미
분리되어 있어, downstream 근거를 손으로 추정하지 않고 재현 가능한 표로
묶을 수 있다는 것이다.

## 읽는 법

- `raw_text_strict_split`: tokenizer/MLM/PPPL의 원천 train/dev/test raw text examples.
- `mlm_pretraining_sample_5pct`: strict train split에서 실제 MLM 입력으로 샘플링된 lines.
- `pseudoperplexity_heldout`: held-out PPPL 후보 split이다. 최종 보고는 `test` 기준으로 둔다.
- retrieval task는 source-English aligned sentence/verse pair 수를 `test`에 적었다.
- NER/POS는 CoNLL blank-line 기준 sentence examples 수다.
- Taxi1500은 TSV row examples 수다.
- embedding similarity는 평가 보조용 pair table이며 train/dev/test split task가 아니다.

MLM strict 5% sampled train corpus는 `8,130,401` lines로 실제 생성 완료 상태다.

## Raw Corpus / MLM / PPPL 요약

| Data scope | Unit | Coverage | Train | Dev | Test | Total | Role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Raw corpus strict split | raw text examples | 102 = 92 head + 10 target | 1,169,231,705 | 100,850 | 100,851 | 1,169,433,406 | tokenizer/MLM sampling/held-out PPPL의 원천 corpus |
| MLM pretraining sample, strict 5% | sampled raw text lines | 102 = 92 head + 10 target | 8,130,401 | 0 | 0 | 8,130,401 | 실제 continued MLM에 투입한 train-only corpus |
| PPPL held-out set | raw text examples | 102 = 92 head + 10 target | 0 | 100,850 | 100,851 | 201,701 | dev/test held-out 후보; final PPPL은 test 기준 |

## Downstream Task별 실제 데이터 양

| Task | Unit | Coverage | Target10 coverage | Train | Dev | Test | Total | Metric / role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Tatoeba retrieval | aligned sentence pairs | 66 / 102 | 3 / 10 | 0 | 0 | 57,479 | 57,479 | Top-10 accuracy; target10 evidence 가능 |
| Bible retrieval | aligned verse pairs | 80 / 102 | 6 / 10 | 0 | 0 | 622,393 | 622,393 | Top-10 accuracy; target10 evidence 가능 |
| Text classification, Taxi1500 | classification rows | 1 / 102 | 0 / 10 | 860 | 106 | 111 | 1,077 | Macro-F1; Glot500 replay, target10 evidence 아님 |
| NER | CoNLL sentence examples | 84 / 102 | 6 / 10 | 894,300 | 405,300 | 405,300 | 1,704,900 | F1; target10 evidence 가능 |
| POS | CoNLL sentence examples | 9 / 102 actual local count | 0 / 10 | 66,894 | 9,673 | 12,851 | 89,418 | F1; available-language replay, target10 evidence 아님 |
| Roundtrip alignment | roundtrip samples | 80 / 102 | 6 / 10 | 0 | 0 | 40,000 | 40,000 | Accuracy; target10 evidence 가능 |

## Auxiliary Diagnostic

| Item | Unit | Coverage | Train | Dev | Test / pairs | Total | Role |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Embedding similarity pairs | diagnostic pair rows | 1 / 102 | 0 | 0 | 22,600 | 22,600 | representation 분석용 보조 pair table; Glot500 downstream task는 아님 |

## Task Summary

| task | unit | langs | head | target | train | dev | test | pairs_or_samples |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_text_strict_split | raw text examples | 102 | 92 | 10 | 1,169,231,705 | 100,850 | 100,851 | 1,169,433,406 |
| mlm_pretraining_sample_5pct | sampled raw text lines | 102 | 92 | 10 | 8,130,401 | 0 | 0 | 8,130,401 |
| pseudoperplexity_heldout | raw text examples | 102 | 92 | 10 | 0 | 100,850 | 100,851 | 201,701 |
| retrieval_tatoeba | aligned sentence pairs | 66 | 63 | 3 | 0 | 0 | 57,479 | 57,479 |
| retrieval_bible | aligned verse pairs | 80 | 74 | 6 | 0 | 0 | 622,393 | 622,393 |
| roundtrip_alignment | roundtrip samples | 80 | 74 | 6 | 0 | 0 | 40,000 | 40,000 |
| ner | CoNLL sentence examples | 84 | 78 | 6 | 894,300 | 405,300 | 405,300 | 1,704,900 |
| pos | CoNLL sentence examples | 9 | 9 | 0 | 66,894 | 9,673 | 12,851 | 89,418 |
| text_classification_taxi1500 | classification rows | 1 | 1 | 0 | 860 | 106 | 111 | 1,077 |
| embedding_similarity_pairs | diagnostic pair rows | 1 | 1 | 0 | 0 | 0 | 22,600 | 22,600 |

## Target10 Snapshot

| language_script | raw_train | raw_dev | raw_test | tatoeba_pairs | bible_pairs | roundtrip_samples | ner_total | pos_total | taxi_total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| asm_Beng | 1,874,644 | 1,000 | 1,000 | 0 | 7,939 | 500 | 300 | 0 | 0 |
| aze_Latn | 46,290,511 | 1,000 | 1,000 | 1,000 | 0 | 0 | 12,000 | 0 | 0 |
| bos_Latn | 11,010,783 | 1,000 | 1,000 | 354 | 0 | 0 | 17,000 | 0 | 0 |
| dzo_Tibt | 42,100 | 1,000 | 1,000 | 0 | 0 | 0 | 0 | 0 | 0 |
| fil_Latn | 33,482,266 | 1,000 | 1,000 | 0 | 7,941 | 500 | 0 | 0 | 0 |
| guj_Gujr | 45,736,247 | 1,000 | 1,000 | 0 | 7,883 | 500 | 300 | 0 | 0 |
| sat_Olck | 35,581 | 1,000 | 1,000 | 0 | 0 | 0 | 0 | 0 | 0 |
| srp_Cyrl | 3,861,064 | 1,000 | 1,000 | 0 | 7,941 | 500 | 40,000 | 0 | 0 |
| sun_Latn | 2,544,902 | 1,000 | 1,000 | 0 | 7,938 | 500 | 300 | 0 | 0 |
| zsm_Latn | 847,033 | 1,000 | 1,000 | 1,000 | 7,888 | 500 | 0 | 0 | 0 |

## Coverage vs Countable Files

`Task Summary`의 language count는 nominal task-list coverage가 아니라, 현재
로컬 파일에서 실제 count가 가능한 split/materialized data 기준이다.

- `pos`: coverage table says `58` languages, but countable local split/materialized files cover `9` languages. See `dataset_size_by_language.tsv` for missing split notes.

## Machine-Readable Outputs

| File | Role |
| --- | --- |
| `3_evaluation/00_coverage/dataset_size_audit.tsv` | task-level train/dev/test totals |
| `3_evaluation/00_coverage/dataset_size_by_language.tsv` | language/task-level counts and source paths |
| `4_reporting/00_tables/table_07_dataset_sizes.md` | report/PPT용 raw/MLM/PPPL 및 downstream data size table |

## Caveats

- pair count와 example count는 서로 다른 단위이므로 같은 column에 있더라도 task 안에서만 비교한다.
- Bible/Roundtrip은 v5.1 materialization output을 기준으로 세며, skipped language는 detailed TSV에 포함하지 않았다.
- NER/POS는 coverage `has_data=yes` 언어만 세고, cached model feature files는 제외했다.
