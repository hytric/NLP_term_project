# v5 Current Result Snapshot

Last checked: 2026-06-28 18:08 KST

Verdict: `execution_draft_not_final`

This generated snapshot is a compact handoff for report/PPT updates.
Use it to find current measured rows and open gates, but promote claims
only from the underlying aggregation and metric artifacts.

PPPL policy: rows produced with `PPPL_SPLIT=train` are train-source
intrinsic diagnostics. They are not Glot500-style held-out test PPPL;
strict held-out PPPL is assigned to the v5.1 correction line.

## Current Safe Claim

```text
The controlled 102-language Glot500-style setup and zero-step
initialization evidence are ready. Matched after-MLM and downstream
claims remain pending until v5_random and v5_fvt checkpoints and
parsed metric outputs exist.
```

## Metric Completion

| Metric | Status | Coverage | Measured models | Missing models |
| --- | --- | ---: | --- | --- |
| pseudoperplexity | partial | 102/102 | glot500_base,v5_random,xlmr_base | v5_fvt |
| retrieval_tatoeba | measured | 63/102 | glot500_base,v5_fvt,v5_random,xlmr_base | - |
| retrieval_bible | measured | 74/102 | glot500_base,v5_fvt,v5_random,xlmr_base | - |
| text_classification | measured | 1/102 | glot500_base,v5_fvt,v5_random,xlmr_base | - |
| ner | partial | 78/102 | glot500_base,v5_random,xlmr_base | v5_fvt |
| pos | partial | 58/102 | glot500_base,v5_random,xlmr_base | v5_fvt |
| roundtrip_alignment | partial | 74/102 | glot500_base,v5_random,xlmr_base | v5_fvt |

## Measured Score Rows

| Metric | Group | Model | Score | Value | Aux |
| --- | --- | --- | --- | ---: | --- |
| pseudoperplexity | all | glot500_base | weighted_pseudo_perplexity | 10.640353 | weighted_mean_nll=2.364654 |
| pseudoperplexity | head | glot500_base | weighted_pseudo_perplexity | 10.213100 | weighted_mean_nll=2.323671 |
| pseudoperplexity | v5_target | glot500_base | weighted_pseudo_perplexity | 15.102934 | weighted_mean_nll=2.714889 |
| pseudoperplexity | all | v5_random | weighted_pseudo_perplexity | 20.138927 | weighted_mean_nll=3.002655 |
| pseudoperplexity | head | v5_random | weighted_pseudo_perplexity | 18.726452 | weighted_mean_nll=2.929937 |
| pseudoperplexity | v5_target | v5_random | weighted_pseudo_perplexity | 39.222875 | weighted_mean_nll=3.669260 |
| pseudoperplexity | all | xlmr_base | weighted_pseudo_perplexity | 9.986271 | weighted_mean_nll=2.301211 |
| pseudoperplexity | head | xlmr_base | weighted_pseudo_perplexity | 8.117338 | weighted_mean_nll=2.094002 |
| pseudoperplexity | v5_target | xlmr_base | weighted_pseudo_perplexity | 61.980216 | weighted_mean_nll=4.126815 |
| retrieval_tatoeba | all | glot500_base | top10_accuracy | 0.706649 | languages=98 |
| retrieval_tatoeba | head | glot500_base | top10_accuracy | 0.743755 | languages=63 |
| retrieval_tatoeba | all | v5_fvt | top10_accuracy | 0.617507 | languages=98 |
| retrieval_tatoeba | head | v5_fvt | top10_accuracy | 0.712669 | languages=63 |
| retrieval_tatoeba | all | v5_random | top10_accuracy | 0.610353 | languages=98 |
| retrieval_tatoeba | head | v5_random | top10_accuracy | 0.700285 | languages=63 |
| retrieval_tatoeba | all | xlmr_base | top10_accuracy | 0.566067 | languages=98 |
| retrieval_tatoeba | head | xlmr_base | top10_accuracy | 0.656309 | languages=63 |
| retrieval_bible | all | glot500_base | top10_accuracy | 0.509356 | languages=74 |
| retrieval_bible | head | glot500_base | top10_accuracy | 0.509356 | languages=74 |
| retrieval_bible | all | v5_fvt | top10_accuracy | 0.370349 | languages=74 |
| retrieval_bible | head | v5_fvt | top10_accuracy | 0.370349 | languages=74 |
| retrieval_bible | all | v5_random | top10_accuracy | 0.328019 | languages=74 |
| retrieval_bible | head | v5_random | top10_accuracy | 0.328019 | languages=74 |
| retrieval_bible | all | xlmr_base | top10_accuracy | 0.381153 | languages=74 |
| retrieval_bible | head | xlmr_base | top10_accuracy | 0.381153 | languages=74 |
| roundtrip_alignment | all | glot500_base | accuracy | 0.205189 | languages=74 |
| roundtrip_alignment | head | glot500_base | accuracy | 0.205189 | languages=74 |
| roundtrip_alignment | all | v5_random | accuracy | 0.190300 | languages=74 |
| roundtrip_alignment | head | v5_random | accuracy | 0.190300 | languages=74 |
| roundtrip_alignment | all | xlmr_base | accuracy | 0.185300 | languages=74 |
| roundtrip_alignment | head | xlmr_base | accuracy | 0.185300 | languages=74 |
| text_classification | head | glot500_base | macro_f1 | 0.743338 | accuracy=0.756757 |
| text_classification | all | glot500_base | macro_f1 | 0.743338 | accuracy=0.756757 |
| text_classification | head | v5_fvt | macro_f1 | 0.717796 | accuracy=0.783784 |
| text_classification | all | v5_fvt | macro_f1 | 0.717796 | accuracy=0.783784 |
| text_classification | head | v5_random | macro_f1 | 0.702956 | accuracy=0.747748 |
| text_classification | all | v5_random | macro_f1 | 0.702956 | accuracy=0.747748 |
| text_classification | head | xlmr_base | macro_f1 | 0.592876 | accuracy=0.729730 |
| text_classification | all | xlmr_base | macro_f1 | 0.592876 | accuracy=0.729730 |
| ner | all | glot500_base | f1 | 0.627108 | languages=164 |
| ner | head | glot500_base | f1 | 0.645915 | languages=78 |
| ner | v5_target | glot500_base | f1 | 0.553191 | languages=1 |
| ner | all | v5_random | f1 | 0.544628 | languages=164 |
| ner | head | v5_random | f1 | 0.608020 | languages=78 |
| ner | v5_target | v5_random | f1 | 0.560554 | languages=1 |
| ner | all | xlmr_base | f1 | 0.549858 | languages=164 |
| ner | head | xlmr_base | f1 | 0.621207 | languages=78 |
| ner | v5_target | xlmr_base | f1 | 0.459364 | languages=1 |
| pos | all | glot500_base | f1 | 0.567542 | languages=18 |
| pos | head | glot500_base | f1 | 0.573832 | languages=9 |
| pos | all | v5_random | f1 | 0.481102 | languages=18 |
| pos | head | v5_random | f1 | 0.587430 | languages=9 |
| pos | all | xlmr_base | f1 | 0.481336 | languages=18 |
| pos | head | xlmr_base | f1 | 0.571446 | languages=9 |

## Open Finalization Gates

| Gate | Status | Next action |
| --- | --- | --- |
| after-MLM PPPL | pending | after checkpoint status and post-checkpoint preflight are ready, prefer SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl; canonical full rerun command: WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh pppl |
| v5 available downstream replay | pending | after checkpoint status and post-checkpoint preflight are ready, prefer SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream or all; canonical full rerun command: WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream |
| Bible retrieval accounting | pending | run Bible retrieval through SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream or all after checkpoints and post-checkpoint preflight are ready |
| Roundtrip alignment accounting | pending | run v5 roundtrip rows after matched checkpoints and post-checkpoint preflight are ready |