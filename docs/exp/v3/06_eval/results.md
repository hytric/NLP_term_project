# Stage 06 Results: Target10 Evaluation

작성일: 2026-06-13

Gate status: IN_PROGRESS

## Summary

Stage 06 now contains the current diagnostic evaluation package: deterministic masked-LM proxy on locked target10 final-test rows, frozen Bible proxy, Coptic UD POS, high-resource control, retained-checkpoint selection, and the lower-LR replay-safe 1000-step retry evaluation.

The 3-seed `fvt` 200-step pilot is seed-stable as a training/eval proxy, but it does not beat XLM-R-base on the average target10 deterministic MLM proxy. The replay-safe 1000-step retry improves the 200-step pilot on target10 proxy and Coptic POS token accuracy, but it still remains worse than XLM-R on average and does not rescue high-resource control.

Frozen-encoder target10 Bible proxy evaluations were also run for all three fvt pilot checkpoints using the existing Step06 proxy runner from `second_try`. These proxy tasks show a small retrieval recall@1 improvement in 2 of 3 checkpoint seeds, but the effect is very small and parallel matching is not stable.

Coptic UD POS tagging was then run as the first local downstream task. The fvt pilot checkpoints improve Coptic token-level POS accuracy over XLM-R-base in all three checkpoint seeds, but the gain is small and this is Coptic-only. It is not enough to support the final target10 claim.

High-resource Bible-control held-out books (`ACT,JOH,MAR`) were also evaluated with the deterministic MLM proxy. This sanity check still shows potential high-resource control collapse after the replay-safe retry: fvt mean MLM loss is higher than XLM-R-base for English, German, Japanese, and Korean, with `0/4` no-large-collapse languages.

## Inputs

| Item | Path |
| --- | --- |
| final-test manifest | `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/final_eval_rows.tsv` |
| XLM-R baseline | `xlm-roberta-base` |
| seed13 checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot` |
| seed17 checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot` |
| seed23 checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot` |
| eval script | `preprocessing/run_third_try_stage06_mlm_proxy_eval.py` |
| Coptic POS data | `/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos` |
| Coptic POS runs | `/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200` |
| high-resource control eval script | `preprocessing/run_third_try_stage06_high_resource_control_eval.py` |

## MLM Proxy Summary

| Model | Seed | Avg MLM loss | Avg MLM perplexity |
| --- | ---: | ---: | ---: |
| XLM-R-base | NA | 3.472837 | 155.079528 |
| fvt pilot | 13 | 5.282255 | 211.068380 |
| fvt pilot | 17 | 5.303112 | 216.313110 |
| fvt pilot | 23 | 5.310412 | 216.775571 |
| fvt pilot mean | NA | 5.298593 | 214.719020 |
| fvt pilot seed range | NA | 0.028157 | 5.707191 |

Language-level loss comparison:

| Language | XLM-R loss | FVT mean loss | Delta FVT-XLMR | Seed range |
| --- | ---: | ---: | ---: | ---: |
| acu | 6.127476 | 5.389076 | -0.738400 | 0.078161 |
| ake | 4.032243 | 4.552107 | 0.519864 | 0.089617 |
| bsn | 4.639948 | 4.664550 | 0.024602 | 0.090055 |
| chr | 0.281844 | 5.374069 | 5.092225 | 0.084301 |
| cop | 0.172038 | 5.713588 | 5.541550 | 0.048957 |
| kbh | 5.804295 | 5.783509 | -0.020786 | 0.061965 |
| nhg | 5.802889 | 5.609999 | -0.192890 | 0.088843 |
| oji | 0.159655 | 5.531056 | 5.371401 | 0.061010 |
| syr | 2.157834 | 5.217867 | 3.060033 | 0.086935 |
| usp | 5.550147 | 5.150111 | -0.400036 | 0.078836 |

## Interpretation

- The fvt 200-step pilot lowers deterministic MLM loss in 4 of 10 target languages: `acu`, `kbh`, `nhg`, and `usp`.
- Coptic and Syriac do not improve on this proxy. Coptic especially is dominated by the XLM-R `<unk>` shortcut baseline, so this metric is diagnostic rather than a fair downstream proxy.
- The three fvt seeds are stable on this proxy: target10 average loss range is `0.028157`.
- This result is compatible with a future diagnostic negative claim, but it is not enough to close the experiment. Real downstream/proxy downstream still has to run.

## Frozen Encoder Proxy

The frozen proxy runner evaluates book/genre classification, verse retrieval, and parallel verse matching. Classification is saturated at `1.0`, so retrieval and matching are the meaningful proxy tasks.

| Checkpoint seed | Retrieval recall@1 delta | Parallel matching AUC delta | Proxy interpretation |
| ---: | ---: | ---: | --- |
| 13 | 0.000963 | -0.001111 | retrieval improves only |
| 17 | -0.000259 | 0.001574 | matching improves only |
| 23 | 0.001074 | -0.002408 | retrieval improves only |
| mean | 0.000593 | -0.000649 | weak/mixed proxy evidence |

Interpretation:

- Retrieval recall@1 improves in 2 of 3 checkpoint seeds.
- Parallel matching improves in 1 of 3 checkpoint seeds.
- The proxy effect is tiny. It is useful as a smoke downstream-like signal, not as final evidence.

## Coptic UD Availability

Local Coptic UD data exists and should be the next official/local downstream run.

| Split | Sentences |
| --- | ---: |
| train | 1467 |
| dev | 380 |
| test | 405 |

## Coptic POS Pilot

Coptic UD Scriptorium was converted to the local `evaluation/tagging/run_tag.py` format and evaluated with a 200-step POS fine-tuning pilot. The upstream tagger reports `seqeval` F1, but that metric is NER-style and inappropriate for plain UPOS tags, so the primary POS metric below is direct token-level accuracy computed from gold labels and `test_cop_predictions.txt`.

| Model | Checkpoint seed | Test token accuracy | Delta vs XLM-R | Test macro F1 | Delta macro F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| XLM-R-base | NA | 0.253182 | 0.000000 | 0.163298 | 0.000000 |
| fvt pilot | 13 | 0.260991 | 0.007809 | 0.169313 | 0.006015 |
| fvt pilot | 17 | 0.257809 | 0.004627 | 0.162237 | -0.001061 |
| fvt pilot | 23 | 0.257424 | 0.004242 | 0.158390 | -0.004908 |
| fvt pilot mean | NA | 0.258741 | 0.005559 | 0.163313 | 0.000015 |

Interpretation:

- Coptic POS token accuracy improves in 3/3 fvt checkpoint seeds.
- The mean improvement is small: `+0.005559` absolute token accuracy.
- Macro F1 is effectively tied: fvt mean `+0.000015` over XLM-R, with only seed13 improving.
- This is useful downstream pilot evidence for Coptic, but not a target10-wide downstream result.

## High-Resource Control

The high-resource control check uses Bible-domain control languages that were included in the Stage 01 mixture, but evaluates only the held-out books excluded from control training: `ACT`, `JOH`, and `MAR`.

Collapse diagnostic threshold: a language is flagged if fvt mean MLM loss is more than `+0.500000` above XLM-R-base.

| Language | XLM-R loss | FVT mean loss | Delta FVT-XLMR | Seed range | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| eng | 2.280143 | 2.905420 | 0.625277 | 0.031575 | FAIL_POTENTIAL_COLLAPSE_PROXY |
| deu | 2.337446 | 2.966584 | 0.629138 | 0.037842 | FAIL_POTENTIAL_COLLAPSE_PROXY |
| jpn | 2.563769 | 3.351112 | 0.787343 | 0.062251 | FAIL_POTENTIAL_COLLAPSE_PROXY |
| kor | 2.875957 | 3.646656 | 0.770699 | 0.090839 | FAIL_POTENTIAL_COLLAPSE_PROXY |
| mean | 2.514329 | 3.217443 | 0.703114 | NA | FAIL_POTENTIAL_COLLAPSE_PROXY |

Interpretation:

- `0/4` high-resource control languages pass the no-large-collapse proxy threshold.
- This does not prove downstream forgetting, but it blocks a positive main claim under the current pilot checkpoints.
- The result points toward a diagnostic negative claim unless a longer/better replay schedule or different checkpoint selection reverses this control loss.

## Retained Checkpoint Selection Proxy

See `checkpoint_selection_proxy_summary.tsv` and `checkpoint_selection_proxy.md`.

Stage 05 retained only checkpoint-150 and checkpoint-200. Checkpoint-150 was evaluated to test whether earlier checkpoint selection could avoid the high-resource control proxy failure.

| Checkpoint | Target10 FVT mean loss | Target10 delta vs XLM-R | High-resource delta vs XLM-R | No-large-collapse languages |
| ---: | ---: | ---: | ---: | ---: |
| 150 | 5.348870 | +1.876033 | +0.757355 | 0/4 |
| 200 | 5.298593 | +1.825756 | +0.703114 | 0/4 |

Interpretation:

- The retained earlier checkpoint does not rescue the current candidate.
- Checkpoint-150 is worse than checkpoint-200 on both target10 MLM proxy and high-resource control proxy.
- Checkpoint-50 and checkpoint-100 were not retained, so this is an ablation over retained checkpoints only.

## Replay-Safe 1000-Step Retry

See `replay_safe_candidate_summary.tsv`.

A lower-LR 1000-step retry was run for seeds 13/17/23 after the 200-step pilot showed high-resource control degradation. This retry keeps the same XLM-R-base append-only tokenizer, fvt initialization, full-model MLM objective, and Stage 01 high-resource replay + target10 mixture.

| Metric | 200-step fvt | replay-safe 1000-step fvt | Reading |
| --- | ---: | ---: | --- |
| Stage05 final dev mean loss | 3.981250 | 3.903145 | improved |
| target10 MLM proxy mean loss | 5.298593 | 5.245928 | improved, still worse than XLM-R |
| target10 languages better than XLM-R | 4/10 | 5/10 | weak proxy gain |
| high-resource control delta vs XLM-R | +0.703114 | +0.675539 | smaller degradation, still fails |
| high-resource no-large-collapse languages | 0/4 | 0/4 | not rescued |
| Coptic POS mean token accuracy | 0.258741 | 0.259963 | weak Coptic-only improvement |
| Coptic POS mean macro F1 | 0.163313 | 0.160642 | worsens |

Interpretation:

- The replay-safe retry is a strictly better compute-bounded candidate than the 200-step fvt pilot on Stage05 dev loss, target10 MLM proxy, and Coptic POS token accuracy.
- It does not rescue the positive claim: high-resource control still fails in `0/4` languages, target10 proxy remains worse than XLM-R on average, and target10 supervised downstream coverage is still sparse.
- The current best framing remains diagnostic negative, with replay schedule/learning-rate as an ablation axis.

## Target10 Downstream Availability

Local supervised downstream coverage is sparse. The audit in `target10_downstream_availability.tsv` records:

- Coptic has a local official-style POS task via UD Coptic-Scriptorium and has been run.
- The other 9 target10 languages have no separate local supervised task found under the current data roots.
- Syriac has Bible proxy coverage and legacy Coptic-Syriac parallel data, but that legacy NMT/translation path is outside the current encoder-only final claim unless a fresh protocol is written.
- All target10 languages have Bible-domain proxy coverage through the frozen proxy tasks.

## Target10 Language Evidence

See `target10_language_evidence.tsv`, `coptic_syriac_evidence.md`, and `syriac_downstream_search.tsv`.

| Language | Tokenizer delta | MLM delta | Supervised/local status | Current status |
| --- | ---: | ---: | --- | --- |
| Coptic | -12.539893% | +5.541550 | UD POS run | weak Coptic-only positive, not target10 |
| Syriac | -66.873096% | +3.060033 | proxy-only | tokenizer improves, model proxy negative |

Interpretation:

- Coptic and Syriac are included as target10 main languages.
- Both improve in tokenizer fertility.
- Neither supports a broad positive target10 downstream claim under the current evidence.
- Coptic has a weak POS token-accuracy pilot; Syriac remains proxy-only and negative/mixed at the model-proxy level.
- The Syriac search audit found Bible/proxy and translation data, but no local POS/NER/classification-style supervised task suitable for the current encoder-only protocol.

## Current Decision

`REPLAY_SAFE_RETRY_IMPROVES_BUT_HIGH_RESOURCE_CONTROL_COLLAPSE_DIAGNOSTIC_NEGATIVE_READY`

## Next Work

1. If pursuing a positive claim, go beyond the current replay-safe 1000-step retry with stronger replay/control changes, because high-resource control still fails.
2. Add a fresh Syriac-relevant supervised/proxy task only if it can be kept encoder-only and leakage-safe.
3. Keep final positive claim blocked; current evidence supports diagnostic negative wording.

## Failure Return

- failed gate: POSITIVE_TARGET10_DOWNSTREAM_AND_HIGH_RESOURCE_CONTROL
- observed evidence: deterministic MLM proxy complete; frozen encoder proxy complete; Coptic POS pilot complete; target10 language evidence complete; high-resource control MLM proxy flags potential collapse
- likely cause: current pilot does not learn appended-token/model behavior strongly enough and replay does not protect high-resource control
- return-to stage: Stage 05 for positive retry, or Stage 07 for diagnostic negative synthesis
- required fix before retry: stronger replay/full-budget evidence plus broader target10 downstream coverage, especially Syriac
