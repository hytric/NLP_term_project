# Step 14 Results: V2 Embedding Initialization

Status: COMPLETED

Run id: step14_v2_init_20260611_154436

Completed date: 2026-06-11

Artifact gate status: PASS

Claim gate status: PASS

## Summary

Step 14 initialized the Step 13 selected 32k tokenizer with all required methods: random, mean, fvt, align, and focus. Selection used full Mark/dev MLM loss only. No ACT final file was read.

Selected init method: `fvt`.

Selected checkpoint: `/home/axt/mnt2/jongha/second_try/checkpoints/14_v2_embedding_init/xlmr_v2_32000_fvt`.

Best zero-step Mark/dev MLM loss: `8.681328`.

## Gate Evidence

- every required method has a checkpoint and `status=PASS`.
- input embedding and LM head shapes match tokenizer length.
- weight tying is preserved.
- no initialized row is NaN or zero-norm.
- `v2_no_final_access_audit.tsv` lists only selected tokenizer metadata and Mark/dev manifest.

## Failure Return

Failed gate: NOT_APPLICABLE

Observed evidence: NOT_APPLICABLE

Return-to step: NOT_APPLICABLE

Required fix: NOT_APPLICABLE

Runtime minutes: 2.765
