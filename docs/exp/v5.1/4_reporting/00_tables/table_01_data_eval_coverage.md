# Table 1. v5.1 Data And Evaluation Coverage

| Metric / data | Total | Head | Target10 | Report use |
| --- | ---: | ---: | ---: | --- |
| PPPL raw text | 102 | 92 | 10 | final held-out intrinsic metric |
| Tatoeba retrieval | 66 | 63 | 3 | target-subset retrieval evidence |
| Bible retrieval | 80 | 74 | 6 | target-subset retrieval evidence |
| Taxi1500 classification | 1 | 1 | 0 | Glot500 replay only, no target claim |
| NER | 84 | 78 | 6 | target-subset tagging evidence |
| POS | 58 | 58 | 0 | Glot500 replay only, no target claim |
| Roundtrip alignment | 80 | 74 | 6 | target-subset alignment evidence |

Definitions:

```text
head = XLM-R training languages among the fixed 92-language subset
target10 = selected XLM-R-unseen languages
all = head + target10 within this v5.1 102-language universe
```

Source:

```text
docs/exp/v5.1/3_evaluation/00_coverage/coverage_summary.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.md
```
