# Step 26 Results: Top-Tier Diagnostic Claim Synthesis

Status: COMPLETED

Run id: step26_top_tier_diagnostic_claim_20260611

Completed date: 2026-06-11

Gate status: PASS_DIAGNOSTIC_CLAIM_READY

## Summary

Step 26 locks the final `second_try` claim as a diagnostic negative result. The supported claim is that vocabulary extension reduces tokenization fragmentation and that initialization/vocab size affect appended-token learning, but current adapted extended-vocabulary models are not competitive with original continued pretraining under v2 matched-token and normalized controls.

This step does not open `ACT` final evaluation. It uses prior `second_try` documents only.

## Final Claim Decision

| Claim direction | Decision | Evidence |
| --- | --- | --- |
| Positive adapted-model claim | BLOCKED | Step15 ratio `1.964580`; Step16 ratio `1.438660`; Step24 ratio `1.472019`; Step25 ratio `1.587381` |
| Positive method-matched translation claim | BLOCKED | Step09 selected adapted XLM-R ratio `0.638034`, below `0.800000` |
| Tokenizer fragmentation claim | ALLOWED | Step02/03 and Step13 evidence |
| Initialization/vocab-size diagnostic claim | ALLOWED | Step14, Step21, Step23 evidence |
| Added-token failure diagnosis | ALLOWED | Step17 and repair failures in Steps18-20 |
| Top-tier diagnostic negative claim | READY | Step22 shortcut audit plus Step26 claim contract |

## Output Files

- `final_claim_contract.md`: allowed and forbidden final wording.
- `evidence_table.tsv`: source-backed claim map.
- `unsupported_claims.tsv`: blocked positive claims and return paths.
- `next_positive_experiments.tsv`: required P0 experiments if positive claims are pursued later.
- `paper_framing.md`: title, abstract, contribution, and table guidance.

## Failure Return

If the paper still needs a positive performance claim, do not proceed to final `ACT` readout. Return to objective/data redesign beyond smaller vocab and longer 8k MLM, then rerun Step15/16-style controls.

If the paper accepts a diagnostic negative claim, proceed to final synthesis with unsupported adapted-model, downstream, and translation success wording removed.
