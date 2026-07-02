# Table 13. Glot500 Metric Fidelity Matrix

Last updated: 2026-06-28

Caption draft:

```text
The v5 experiment keeps every metric family used for Glot500-style evaluation.
For each family, the table records the inherited/local runner, current measured
baseline/reference status, diagnostic v5-random status, pending v5-FVT status,
and the claim boundary created by local task coverage.
```

| Metric family | Fidelity action in v5 | Runner/evaluator | Baseline/reference status | v5 method status | Coverage boundary | Final claim rule |
| --- | --- | --- | --- | --- | --- | --- |
| Pseudoperplexity | retained as intrinsic MLM proxy over all 102 language-scripts | `scripts/run_v5_eval_metric.sh pppl`; `modeling/run_v5_zero_step_mlm_proxy.py` | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 102/102 local data, target10 10/10 | can support target10 intrinsic and after-MLM adaptation claims only after paired v5 rows exist |
| Tatoeba retrieval | retained as sentence-retrieval Top-10 metric | `scripts/run_v5_eval_metric.sh retrieval_tatoeba`; inherited Tatoeba retrieval script | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 63/102 local data, target10 0/10 | report as available-language downstream evidence, not target10 downstream evidence |
| Bible retrieval | retained as sentence-retrieval Top-10 metric | `scripts/run_v5_eval_metric.sh retrieval_bible`; inherited Bible retrieval script | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 74/102 local data, target10 0/10 | report as available-language downstream evidence, with target10 exclusion visible |
| Text classification | retained as classification F1 metric | `scripts/run_v5_eval_metric.sh text_classification`; Taxi1500 evaluator | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 1/102 local data, target10 0/10 | report as narrow local baseline/reference and diagnostic v5-random evidence only |
| NER | retained as sequence-tagging F1 metric | `scripts/run_v5_eval_metric.sh ner`; inherited tagging script | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | materialized audit 78/102, target10 0/10; actual runner also produced one-language `fur_Latn` rows | report head/all available-language rows; do not generalize one target-language row to target10 |
| POS | retained as sequence-tagging F1 metric | `scripts/run_v5_eval_metric.sh pos`; inherited tagging script | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 58/102 local data, target10 0/10; local training uses `TRAIN_LANGS=tur_Latn` | report with the local train-language caveat |
| Roundtrip alignment | retained as required metric family with runnable available-language inputs | `scripts/run_v5_eval_metric.sh roundtrip_alignment`; `evaluation/round-trip/evaluate_roundtrip_v5.py`; inherited `RoundTripEvaluator` | `xlmr_base` and `glot500_base` measured | `v5_random` diagnostic row measured; `v5_fvt` waits for checkpoint | 74/102 local data, target10 0/10 | report only parsed model rows; do not claim target10 roundtrip improvement |

Promotion rule:

- A metric family is considered faithfully retained when it has either measured
  rows for the required model columns or an explicit coverage/blocker row.
- A metric family is not considered final for the v5 method comparison until
  `v5_random` and `v5_fvt` are both accounted for as measured or blocked.
- Current `v5_random` rows are diagnostic single-method rows; they verify the
  wrapper/aggregation path but do not prove the initialization novelty by
  themselves.
- Target10 downstream improvement remains unsupported until partial official
  target task membership is materialized and evaluated correctly.

Source artifacts:

- `docs/exp/v5/3_evaluation/glot500_metric_requirements.md`
- `docs/exp/v5/3_evaluation/metric_mapping.md`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
- `docs/exp/v5/3_evaluation/00_coverage/coverage_summary.tsv`
- `docs/exp/v5/4_reporting/finalization_gate_status.md`
