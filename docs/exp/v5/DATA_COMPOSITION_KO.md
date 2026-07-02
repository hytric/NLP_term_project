# v5 데이터 구성 요약

먼저 볼 상세 문서:

```text
LANGUAGE_SOURCE_OVERLAP_KO.md
0_tokenizer/00_data_scope/data_composition_by_language.md
```

전체 언어별 TSV:

```text
0_tokenizer/00_data_scope/data_composition_by_language.tsv
```

이 표는 언어별 `XLM-R` 포함 여부, seen/target group, raw corpus 크기,
continued-MLM train sample 수, PPPL/downstream task별 train/dev/test 또는
test-pair count를 정리한다.

## 언어 소스 구분

v5에서 `XLM-R=True`는 XLM-R pretraining에 포함된 언어인지에 대한 metadata
label이다. 실제 v5 tokenizer/MLM/PPPL에서 읽은 local raw text는 102개 모두
별도로 내려받은 Glot500 raw data다.

| Source layer | 언어 수 | 의미 |
| --- | ---: | --- |
| XLM-R-seen/head label | 92 | Glot500 metadata에서 `XLM-R=True`인 language-script |
| Glot500-internal target label | 10 | `XLM-R=False`, `new_length >= 30000`, raw directory 존재 조건으로 고른 target |
| v5 local Glot500 raw text | 102 | tokenizer/continued MLM/PPPL에 쓰는 실제 local raw-text universe |
| downstream/eval data | task별 상이 | v5 102와 local task resource의 intersection |

즉 `102 = 92 seen + 10 target`이고, 이 102개는 모두 Glot500 raw text를 가진다.
반면 Tatoeba/Bible/Roundtrip/Taxi1500/NER/POS는 해당 task dataset이 제공하고
local로 materialize된 언어와의 교집합만 평가한다.

Metric coverage count 해석:

| Metric family | v5 denominator | has data | seen overlap | target overlap |
| --- | ---: | ---: | ---: | ---: |
| PPPL raw-text | 102 | 102 | 92 | 10 |
| Tatoeba retrieval | 102 | 63 | 63 | 0 |
| Bible retrieval | 102 | 74 | 74 | 0 |
| Roundtrip alignment | 102 | 74 | 74 | 0 |
| Taxi1500 classification | 102 | 1 | 1 | 0 |
| NER | 102 | 78 | 78 | 0 |
| POS | 102 | 58 | 58 | 0 |

각 metric의 원천 dataset:

| Metric family | Dataset/source | 무엇을 평가하나 |
| --- | --- | --- |
| PPPL raw-text | v5 local Glot500 raw text | MLM pseudo-perplexity proxy |
| Tatoeba retrieval | LASER Tatoeba v1 parallel sentence data | English sentence retrieval |
| Bible retrieval | local Bible/PBC 계열 parallel verse corpus | English verse retrieval |
| Roundtrip alignment | Bible-derived multilingual JSONL + SimAlign | word alignment cycle consistency |
| Taxi1500 classification | Taxi1500 English Bible verse topic split | 6-way text classification |
| NER | PAN-X/WikiAnn via HuggingFace `tner/wikiann` | named entity tagging |
| POS | Universal Dependencies v2.11 | part-of-speech tagging |

핵심 해석:

- v5 MLM corpus는 별도 validation/test split 없이 train corpus로 구성되어 있다.
- PPPL은 102/102 언어의 raw text를 사용한다.
- 위 downstream coverage count는 전체 task dataset 규모가 아니라, v5 102개
  Glot500 subset과 local evaluation resource의 교집합이다.
- target10 downstream direct coverage는 현재 PPPL을 제외하면 coverage gate 기준
  0/10이다. 단, NER output에는 `fur_Latn` 1개 actual local intersection row가
  남아 있으므로 이것은 target10-wide evidence가 아니라 coverage-limited example로만
  해석한다.
- 따라서 target-language downstream claim을 목표로 한다면 현재 target10은
  부적절하며, `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md`의 downstream-aware
  후보를 기준으로 재선정해야 한다.
- downstream task는 available-language/head/all replay로 보고해야 한다.
