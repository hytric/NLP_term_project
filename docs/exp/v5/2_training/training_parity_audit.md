# v5 Training Parity Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `training_parity_ready`

This generated audit checks the central method-comparison precondition:
`v5_random` and `v5_fvt` should differ by initialization method while
sharing corpus, tokenizer, launcher, schedule, checkpoint rule, and
post-checkpoint eligibility. It does not claim training has finished.

| Item | Status | Evidence | Action |
| --- | --- | --- | --- |
| required parity artifacts | ready | launch script, train script, selection plan, manifest, and model matrix exist | none |
| paired launcher contract | ready | random and FVT use the same train script, shared launch env, 10K max steps, and random-first order | none |
| shared MLM train script contract | ready | train script fixes shared corpus, tokenizer, batch, accumulation, LR, save interval, max length, and workers | none |
| pre-declared checkpoint selection rule | ready | selection plan requires matched 10K full-corpus checkpoints and forbids comparing failed short runs | none |
| model matrix parity | ready | v5_random_status=ready; v5_fvt_status=ready; tokenizer_match=True; required_pair=True; downstream_pair=True | none |
| live execution parity state | ready | manifest=matched_v5_checkpoints_ready; running_status_mentions_pair=True | none |

Use:

- Keep this audit ready before promoting any FVT-vs-random after-MLM or
  downstream claim.
- If it reports `waiting_runs`, the parity contract is ready but the
  matched checkpoints are not yet complete.
