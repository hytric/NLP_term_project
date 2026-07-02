# Step 22 Results: Full Experiment Shortcut And Next-Experiment Audit

Status: COMPLETED

Run id: step22_full_experiment_audit_20260611

Completed date: 2026-06-11

Gate status: PASS_AUDIT_BLOCKS_POSITIVE_CLAIM

## Summary

The current second_try result is not a hidden shortcut pass. The old v1 translation shortcut was found and invalidated by Step09/Step10, and v2 Steps 13-27 keep `ACT` final protected. Step23 gives a passing smaller-vocab redesign probe, Step24 shows the selected 8k branch still fails original-control normalized competitiveness, Step25 shows longer 8k MLM alone does not rescue the gap, Step26 locks the top-tier-safe diagnostic claim, and Step27 packages it for manuscript writing.

| Check | Result |
| --- | ---: |
| score table bad cells | 0 |
| stale or missing file result entries | 0 |
| v2 no-final audit rows | 46 |
| v2 no-final bad rows | 0 |
| active v1 shortcut evidence used for final claim | 0 |
| v2 positive adapted-model claim allowed | 0 |

## Shortcut Verdict

V1 translation evidence is shortcut-prone and remains invalidated. It must not be used for top-tier claims.

V2 evidence through Step27 does not show active final-set leakage or shortcut selection. The current `PASS` labels include a real redesign probe pass, a diagnostic-claim synthesis pass, and a manuscript-package pass, but Steps24-25 confirm they are still not proof of a positive adapted-model claim against original continued pretraining.

## Additional Experiment Verdict

Additional experiments are required only if the target is a positive model-dependent claim. The mandatory path is:

1. Continue tokenizer/objective/data redesign beyond longer 8k MLM, or downgrade the model-dependent claim.
2. Rerun MLM control and normalized metric audits only after a new repair branch exists.
3. Then run v2 downstream and method-matched translation with `ACT` final read exactly once after all model/pair/scoring decisions are frozen.

The paper has now been downgraded to a negative/diagnostic top-tier claim in Step26 and packaged for manuscript writing in Step27. No new model experiment is required for that diagnostic framing, but the final wording must continue to remove unsupported adapted-model, downstream, and translation success claims.

## Failure Return

Failed positive claim gate: v2_positive_model_claim

Observed evidence: Step15 adapted/original ratio `1.964580`; Step16 normalized ratio `1.438660`; Step18/19/20 repair gates fail; Step21 alternative init probe fails; Step23 best 8k branch improves over 32k but still has raw ratio `1.803523` to original-control mean; Step24 8k word/char normalized ratio is `1.472019`; Step25 longer-budget word/char ratio is `1.587381`; Step26 diagnostic claim gate passes with positive claim ready `0`; Step27 manuscript package gate passes with positive package ready `0`.

Return-to step for positive claim: objective/data redesign beyond Step23/24, then `15_v2_mlm_control` and `16_v2_mlm_metric_fairness`.

Required fix before positive downstream or translation final readout: a new branch that passes Step15/Step16-style normalized control audits.
