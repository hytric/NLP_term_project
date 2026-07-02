# v5 Glot500 Metric Mapping

Last updated: 2026-06-28

This document maps each Glot500-required metric family to the concrete v5
runner, inherited evaluator, data root, and report artifact. It is the bridge
between the reproduction claim and the actual commands used in this fork.

## Required Metric Mapping

| Metric id | Glot500-style task | v5 wrapper | Inherited/local evaluator | Data root | Primary output |
| --- | --- | --- | --- | --- | --- |
| `pppl` | pseudoperplexity / MLM proxy | `scripts/run_v5_eval_metric.sh pppl <model_key> <gpu>` | `modeling/run_v5_zero_step_mlm_proxy.py` | v5 raw manifest input dirs | `3_evaluation/01_pseudoperplexity/<model_key>/summary.tsv` |
| `retrieval_tatoeba` | sentence retrieval, Tatoeba Top-10 | `scripts/run_v5_eval_metric.sh retrieval_tatoeba <model_key> <gpu>` | `evaluation/retrieval/evaluate_retrieval_tatoeba.sh` | `evaluation/download_data/download/retrieval_tatoeba/` | `3_evaluation/02_retrieval_tatoeba/<model_key>/` plus v5 eval output dir |
| `retrieval_bible` | sentence retrieval, Bible Top-10 | `scripts/run_v5_eval_metric.sh retrieval_bible <model_key> <gpu>` | `evaluation/retrieval/evaluate_retrieval_bible.sh` | `evaluation/download_data/download/retrieval_bible/` | `3_evaluation/03_retrieval_bible/<model_key>/` plus v5 eval output dir |
| `text_classification` | Taxi1500 classification F1 | `scripts/run_v5_eval_metric.sh text_classification <model_key> <gpu>` | `evaluation/text_classification/evaluate_taxi1500.py` | `evaluation/download_data/download/taxi1500/` | `evaluation/text_classification/taxi1500/<model_key>/summary.json` |
| `ner` | PAN-X / WikiAnn NER F1 | `scripts/run_v5_eval_metric.sh ner <model_key> <gpu>` | `evaluation/tagging/evaluate_ner.sh` | `evaluation/download_data/download/ner/` | `3_evaluation/05_ner/<model_key>/` plus v5 eval output dir |
| `pos` | UD-POS tagging F1 | `scripts/run_v5_eval_metric.sh pos <model_key> <gpu>` | `evaluation/tagging/evaluate_pos.sh` | `evaluation/download_data/download/pos/` | `3_evaluation/06_pos/<model_key>/` plus v5 eval output dir |
| `roundtrip_alignment` | roundtrip alignment accuracy | `scripts/run_v5_eval_metric.sh roundtrip_alignment <model_key> <gpu>` | `evaluation/round-trip/evaluate_roundtrip_v5.py` | `evaluation/download_data/download/roundtrip_alignment/` | `v5_root/evaluation/roundtrip_alignment/<model_key>/test_results.txt` plus `3_evaluation/07_roundtrip_alignment/<model_key>/run_meta.tsv` |

## Wrapper Guarantees

The v5 wrapper is required for final runs because it records:

- `model_key`, model path, tokenizer path, GPU, and data root in `run_meta.tsv`.
- command logs under each metric/model folder.
- v5 output directories under `/home/axt/mnt2/jongha/v5_glot50010/evaluation/`.
- model readiness through `docs/exp/v5/3_evaluation/model_matrix.tsv`.

Do not run inherited evaluation scripts directly for final results unless the
same metadata and output paths are recorded manually.

## Environment Fixes

The inherited scripts assumed `python` exists. In this environment the stable
interpreter is `python3`, so the following shell evaluators now support:

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
```

Patched evaluators:

- `evaluation/retrieval/evaluate_retrieval_tatoeba.sh`
- `evaluation/retrieval/evaluate_retrieval_bible.sh`
- `evaluation/tagging/evaluate_ner.sh`
- `evaluation/tagging/evaluate_pos.sh`
- `evaluation/download_data/download_data.sh`

PAN-X / WikiAnn materialization uses `tner/wikiann` by default. In the local
`datasets==2.7.1` environment, the default `wikiann` and
`unimelb-nlp/wikiann` entries expose only the `ace` config, which can silently
write wrong language files if verification is bypassed. The current downloader
smoke-tests language-specific content and uses the T-NER WikiAnn integer tag
mapping.

## Reporting Columns

For each measured metric, final tables should include:

- model: `xlmr_base`, `glot500_base`, `v5_random`, `v5_fvt`
- group: `head`, `v5_target` where available, `all`
- score and direction
- number of measured languages
- target10 coverage count
- exclusion reason for missing target languages

## Aggregation Parsers

`scripts/aggregate_v5_metrics.py` currently normalizes these output formats:

| Metric | Parsed file pattern | Parsed score | Grouping rule |
| --- | --- | --- | --- |
| `pppl` | `3_evaluation/01_pseudoperplexity/*/summary.tsv` | `weighted_pseudo_perplexity` and `weighted_mean_nll` | groups already written by PPPL script |
| `retrieval_tatoeba` | `v5_root/evaluation/retrieval_tatoeba/*/test_results.txt` | `Acc10` as `top10_accuracy` | language -> group from `coverage_retrieval_tatoeba.tsv` |
| `retrieval_bible` | `v5_root/evaluation/retrieval_bible/*/test_results.txt` | `Acc10` as `top10_accuracy` | language -> group from `coverage_retrieval_bible.tsv` |
| `text_classification` | `v5_root/evaluation/text_classification/taxi1500/*/summary.json` | test `macro_f1` | English local split reported as `head` and `all` |
| `ner` | `v5_root/evaluation/ner/*/test_results.txt` | `f1` | language -> group from `coverage_ner.tsv` |
| `pos` | `v5_root/evaluation/pos/*/test_results.txt` | `f1` | language -> group from `coverage_pos.tsv` |
| `roundtrip_alignment` | `v5_root/evaluation/roundtrip_alignment/*/test_results.txt` | `accuracy` | language -> group from `coverage_roundtrip_alignment.tsv` |

Roundtrip alignment now has Bible-derived JSONL inputs, a v5 batch runner, and
parsed XLM-R-base/Glot500-base baseline/reference rows over `74/102`
available language-scripts. The `v5_random` diagnostic row is also parsed; the
remaining method-comparison gap is the paired `v5_fvt` row, which waits for the
matched checkpoint.

## Current Coverage Boundary

Current coverage is tracked in:

```text
3_evaluation/00_coverage/coverage_summary.tsv
```

The important reporting boundary is:

```text
target10 has 10/10 raw-text PPPL coverage, but 0/10 local downstream coverage
outside PPPL at the current materialization point.
```

This means target10 claims should be centered on tokenization, zero-step MLM
proxy, and after-MLM PPPL unless downstream task data is later materialized.
The current v5-random rows are useful diagnostic evidence that every retained
metric family can flow through the wrapper and aggregation path; they are not
a final method comparison until the matched v5-FVT rows are parsed or explicitly
blocked.
