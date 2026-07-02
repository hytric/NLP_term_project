# Step 28 Results: Appended-Token Solution Roadmap

Status: COMPLETED

Run id: step28_solution_roadmap_20260612

Completed date: 2026-06-12

Gate status: PASS_SOLUTION_ROADMAP_READY

## Summary

Step28 converts the Step17 appended-token failure localization into concrete solution hypotheses and falsifiable experiment protocols. The recommended remedy is subtoken-teacher distillation for appended tokens, combined with curriculum added-token MLM and base-token KL/replay preservation.

This step does not claim that the remedy works. It defines the next experiment needed to reopen a positive model claim.

## Main Recommendation

Run a future `E28_02_CURRICULUM_KL_MLM` experiment:

1. initialize appended rows with original-XLM-R subtoken teacher supervision;
2. train with scheduled added-token mask/loss pressure;
3. preserve base-token behavior with KL or replay;
4. require added/base/all seed-stable gates and Step16-style normalized ratios `<=1.100000`.

## Why This Is The Right Next Step

Prior repairs failed in complementary ways:

- Step18 improved added-token loss but worsened all-token loss.
- Step19 preserved base-token behavior but did not improve added-token loss.
- Step25 showed longer 8k MLM alone does not close the original-control gap.

The proposed remedy directly combines stronger appended-token supervision with explicit base-token preservation.

## Failure Return

If the proposed remedy fails, return to objective/data redesign or external non-final target data collection. Do not open downstream or translation final readout until Step15/16-style controls pass.
