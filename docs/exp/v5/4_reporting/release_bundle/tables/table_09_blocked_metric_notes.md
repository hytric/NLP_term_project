# Table 9. Blocked And Coverage-Limited Metric Notes

Last updated: 2026-06-28

Caption draft:

```text
Bible retrieval and roundtrip alignment remain required Glot500 metric
families in v5. Bible retrieval now has local materialized data for available
Glot500 Bible task languages and measured XLM-R/Glot500-base plus v5_random
diagnostic rows; v5_fvt waits for its matched checkpoint. Roundtrip alignment
now has local Bible-derived inputs, a v5 runner, and measured
XLM-R/Glot500-base plus v5_random diagnostic rows; v5_fvt waits for its
matched checkpoint.
```

| Metric | Current status | Coverage | Blocking evidence | Reporting rule |
| --- | --- | ---: | --- | --- |
| Bible retrieval | baseline/reference and v5_random diagnostic rows measured; v5_fvt waiting checkpoint | 74/102, target10 0/10 | `coverage_retrieval_bible.tsv`; `03_retrieval_bible/materialization_summary.tsv`; `evaluation/download_data/download/retrieval_bible` contains 148 source/English files for 74 language-scripts; XLM-R Top-10 `0.381153`; Glot500-base Top-10 `0.509356`; v5_random Top-10 `0.328019`; target10 remains outside the Glot500 Bible task flags | run v5_fvt after checkpoint; do not claim target10 Bible improvement |
| Roundtrip alignment | baseline/reference and v5_random diagnostic rows measured; v5_fvt waiting checkpoint | 74/102, target10 0/10 | `coverage_roundtrip_alignment.tsv`; `evaluation/download_data/download/roundtrip_alignment` contains Bible-derived JSONL inputs; v5 runner exists at `evaluation/round-trip/evaluate_roundtrip_v5.py`; XLM-R accuracy `0.185300`; Glot500-base accuracy `0.205189`; v5_random accuracy `0.190300` | run v5_fvt after checkpoint; do not claim target10 roundtrip improvement |

Source artifacts:

- `docs/exp/v5/3_evaluation/00_coverage/coverage_summary.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_retrieval_bible.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_roundtrip_alignment.tsv`
- `docs/exp/v5/3_evaluation/03_retrieval_bible/materialization_summary.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/data_materialization.md`
- `docs/exp/v5/3_evaluation/03_retrieval_bible/README.md`
- `docs/exp/v5/3_evaluation/07_roundtrip_alignment/README.md`
