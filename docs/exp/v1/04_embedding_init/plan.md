# Step 04 Plan: Embedding Initialization

## Goal

Initialize newly added token embeddings for every selected vocab size and required initialization method.

## Inputs

- Step 03 `Gate status: PASS`
- Extended tokenizer artifacts
- Original `xlm-roberta-base` model

## Required Methods

- `random`
- `mean`
- `fvt`
- `align`
- `focus`

Optional:

- `ofa`
- `wechsel`

## Required Work

1. Resize input embeddings and MLM head for each selected tokenizer.
2. Initialize every new row for each method.
3. Verify input embedding and MLM head shape.
4. Verify weight tying behavior.
5. Record fallback counts.
6. Compute embedding norm diagnostics.
7. Compute zero-step MLM loss on dev data.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `embedding_init_metrics.tsv`
- `zero_step_mlm.tsv`
- `nearest_neighbors.md`
- `file_results.tsv`
- initialized model artifacts for gate-passing candidates

## Score Table Contract

Every vocab size and init method combination must have shape checks, fallback counts, norm stats, and zero-step loss. No `TBD` is allowed before exit.

## Exit Criteria

- All required methods either pass or have a documented implementation failure.
- At least random, mean, and fvt pass for every selected vocab size.
- No missing/uninitialized rows.
- Zero-step MLM loss is recorded.
- `file_results.tsv` records every generated file with path, count or size, and status.
- `results.md` has `Gate status: PASS`.

## Failure Return

If model resize or tying fails, stay in Step 04. If tokenizer id mapping is the cause, return to Step 03. If method-specific external resources are unavailable, mark that method as failed with evidence and continue only if required baseline methods pass.
