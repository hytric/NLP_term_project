# Final Goal Completion Audit

작성일: 2026-06-13

## Verdict

Final positive model claim: `NO_GO`.

Diagnostic negative report package: `READY`.

## Requirement Audit Summary

| Area | Verdict | Evidence |
| --- | --- | --- |
| XLM-R-base start | PASS | `05_mlm/deviation_from_protocol.tsv` |
| Append-only id preservation | PASS | `03_tokenizer/id_preservation_audit.tsv` |
| Target10 scope including Coptic/Syriac | PASS | `scope_lock_20260612.md`, `00_scope/results.md` |
| High-resource replay + target10 mixture | PASS_WITH_DEVIATION | `01_data/mlm_mixture_manifest.tsv` |
| Full-model MLM continued pretraining | PASS_COMPUTE_BOUNDED | `05_mlm/replay_safe_seed_summary.tsv` |
| At least 3 seeds | PASS | seeds 13/17/23 for replay-safe retry |
| Byte fallback vs char comparison | PASS_ABLATION | `03_tokenizer/fallback_ablation_summary.tsv` |
| Coptic downstream | PASS_WEAK_COPTIC_ONLY | `06_eval/coptic_pos_summary_replay_safe.tsv` |
| Syriac downstream | PARTIAL_PROXY_ONLY | `06_eval/syriac_downstream_search.tsv` |
| Target10-wide downstream seed stability | FAIL_FOR_POSITIVE | `06_eval/target10_seed_summary.tsv` |
| High-resource no-collapse | FAIL_FOR_POSITIVE | `06_eval/high_resource_control_summary_replay_safe.tsv` |
| Existing experiments as ablation | PASS | `08_ablation/ablation_matrix.tsv` |

## Positive Claim Blockers

1. Replay-safe target10 MLM proxy mean loss is `5.245928`, still worse than XLM-R-base `3.472837`.
2. Replay-safe high-resource control mean loss delta is `+0.675539`; `0/4` control languages pass the no-large-collapse threshold.
3. Coptic POS token accuracy is weakly positive, but macro-F1 worsens and this is Coptic-only.
4. Syriac has no local supervised encoder-only downstream task in the current protocol.
5. Target10-wide downstream seed stability is not available.
6. Stage 05 is compute-bounded: 200-step pilot plus 1000-step retry, effective batch 32, materialized mixture.

## Allowed Final Goal Statement

The final report should pursue this goal:

> Diagnose why a Glot500-style, id-preserving XLM-R-base vocabulary extension improves target10 tokenizer fragmentation but does not produce a broad target10 downstream/model-quality gain under the current compute-bounded continued-pretraining setup.

The report should not claim:

> The final model improves target10 downstream performance over XLM-R-base.

## Next Positive-Retry Gate

If a positive model result is still required, return to Stage 05 and require all of the following before Stage 07:

1. stronger replay/control schedule or larger training budget;
2. 3+ seeds retained;
3. high-resource control no-collapse;
4. target10 downstream/proxy-downstream improvement beyond Coptic-only POS;
5. Syriac-specific encoder-only evidence;
6. unchanged append-only id-preservation audit.
