# Step 16 Plan: V2 MLM Metric Fairness Audit

## Goal

Audit whether Step 15's raw per-masked-token MLM loss is an adequate cross-tokenizer control metric. The Step 15 adapted and original-control checkpoints use different tokenizers, so this step reports token-normalized, word-normalized, and character-normalized MLM diagnostics on the same Mark/dev text.

## Inputs

| Role | Path | Split Policy |
| --- | --- | --- |
| Step 15 seed summary | `docs/exp/second_try/15_v2_mlm_control/seed_summary.tsv` | checkpoint metadata only |
| v2 Mark/dev text | `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt` | dev only |

`ACT` clean final must not be read in this step.

## Work

1. Evaluate every Step 15 final checkpoint on the same Mark/dev lines.
2. Record raw masked-token MLM loss.
3. Record non-special token counts, words, and characters under each tokenizer.
4. Estimate per-word and per-character NLL as `mean_masked_token_loss * non_special_tokens / normalization_unit`.
5. Compare adapted and original-control aggregates across the same seeds.

## Required Outputs

| File | Required Content |
| --- | --- |
| `score_table.tsv` | gate rows and normalized aggregate ratios |
| `normalized_mlm_scores.tsv` | every family/seed checkpoint with token, word, and char normalized metrics |
| `v2_no_final_access_audit.tsv` | input access audit with `final_access=NO` |
| `results.md` | interpretation and return path |
| `file_results.tsv` | path/count/size/checksum evidence for every output |

## Exit Criteria

Artifact gate passes only if all six Step 15 checkpoints are evaluated and no ACT final input is read.

Claim gate passes only if the adapted family is competitive with the original-control family on both estimated NLL per word and estimated NLL per character within the configured margin. If this fails, Step 15's negative model-dependent conclusion remains in force.

