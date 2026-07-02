# Step 13 Plan: V2 Tokenizer

## Goal

Execute `V2_01_TOKENIZER`: train and merge 8k, 16k, and 32k target tokenizers using only the Step 12 v2 train text, then select a tokenizer using only Mark/dev tokenization metrics.

## Inputs

- Train text: `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt`
- Dev manifest: `docs/exp/second_try/12_v2_split_protocol/v2_dev_manifest.tsv`
- Forbidden for this step: `v2_final_test_act_clean.tsv`, `v2_final_test_act_clean.txt`, and any Step07/09 test output.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `v2_vocab_extension_metrics.tsv`
- `v2_vocab_merge_report.tsv`
- `v2_tokenization_examples.md`
- `v2_no_final_access_audit.tsv`
- `selected_tokenizer.md`
- `file_results.tsv`

Large tokenizer artifacts go under `/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer/`.

## Exit Criteria

- 8k, 16k, and 32k candidates are trained or loaded from v2 train-only artifacts.
- XLM-R special ids are preserved for every candidate.
- Mark/dev tokenization improves over base XLM-R on tokens/word and high single-character rate.
- A selected tokenizer is chosen only from dev metrics.
- No final ACT file is read by the script.
- No `score_table.tsv` cell is blank or `TBD`.

## Failure Return

If no tokenizer passes the dev gate, return to Step 12 or revise tokenizer sizes before running v2 initialization.
