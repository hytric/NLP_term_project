# Stage 07 Results: Main Claim Synthesis

작성일: 2026-06-13

Gate status: PASS_NEGATIVE_MAIN_READY

## Summary

Stage 00-06 evidence does not support the positive claim. The structurally valid XLM-R append-only tokenizer improves average target10 tokenization, and Coptic POS shows a weak token-accuracy pilot gain, but target10 MLM proxy, frozen proxy downstream, task coverage, and high-resource control do not support a broad seed-stable target10 downstream improvement.

Coptic/Syriac are explicitly audited in `../06_eval/coptic_syriac_evidence.md`: Coptic has weak POS token-accuracy improvement but worsens on the MLM proxy, while Syriac has strong tokenizer improvement but remains proxy-only and negative/mixed at the model-proxy level.

Retained checkpoint selection is also audited in `../06_eval/checkpoint_selection_proxy_summary.tsv`. The available earlier checkpoint (`checkpoint-150`) is worse than `checkpoint-200` on both target10 MLM proxy and high-resource control proxy, so the current negative result is not rescued by selecting the earlier retained checkpoint.

A lower-LR replay-safe 1000-step retry is audited in `../06_eval/replay_safe_candidate_summary.tsv`. It improves over the 200-step fvt pilot on Stage05 dev loss, target10 MLM proxy, and Coptic POS token accuracy, but it still fails high-resource control (`0/4` no-large-collapse languages) and remains worse than XLM-R on target10 MLM proxy average.

## Claim Decision

Allowed route: diagnostic negative claim for the current compute-bounded candidate.

Blocked route: positive target10 downstream claim.

## Evidence Links

- Claim evidence: `evidence_table.tsv`
- Allowed wording: `allowed_claims.md`
- Blocked wording: `blocked_claims.md`
- Main result summary: `main_result_summary.md`
- Limitations and deviations: `limitation_and_deviation_summary.md`

## Final Claim Draft

In the current Glot500-style XLM-R vocabulary-extension experiment, append-only target10 vocabulary expansion reduced average tokenizer fragmentation, and byte fallback was slightly better than character coverage in tokenizer-only ablation. A replay-safe lower-LR retry improved the 200-step pilot but did not rescue the positive claim: target10 MLM proxy remained worse than XLM-R on average, proxy downstream evidence was mixed, only Coptic POS token accuracy showed a weak supervised improvement, and high-resource control MLM loss still degraded. Therefore, the current result should be framed as a diagnostic negative result and used to motivate ablations over vocab size, initialization, fallback, replay, and appended-token learning.

## Failure Return

- failed gate: POSITIVE_MAIN_CLAIM
- observed evidence: high-resource control proxy failure, target10 MLM proxy degradation, sparse supervised target10 task coverage
- likely cause: compute-bounded training scale, insufficient replay schedule, appended-token learning not strong enough, and tokenizer fallback implementation mismatch
- return-to stage: Stage 05 for final-budget training or Stage 08 for ablation packaging
- required fix before positive retry: full-budget seed grid plus stronger target10 downstream coverage and high-resource no-collapse evidence
