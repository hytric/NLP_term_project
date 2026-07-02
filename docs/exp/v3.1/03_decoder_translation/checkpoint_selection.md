# Checkpoint Selection

작성일: 2026-06-18

## Full1ep Runs

The first full-data decoder probe used a one-epoch schedule. Because each run has only one training epoch, checkpoint selection is trivial:

- train on the full train split for one epoch;
- run a bounded dev subset at epoch end for compatibility with the runner's selection flow;
- reload the best epoch state;
- evaluate full dev and full final_test.

No test examples were used for checkpoint selection.

## Run Artifacts

| Run | Output Directory |
| --- | --- |
| `full1ep_xlmr_base_cop_to_syr` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_xlmr_base_cop_to_syr` |
| `full1ep_fvt_seed13_cop_to_syr` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed13_cop_to_syr` |
| `full1ep_fvt_seed17_cop_to_syr` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed17_cop_to_syr` |
| `full1ep_fvt_seed23_cop_to_syr` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed23_cop_to_syr` |
| `full1ep_xlmr_base_syr_to_cop` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_xlmr_base_syr_to_cop` |
| `full1ep_fvt_seed13_syr_to_cop` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed13_syr_to_cop` |
| `full1ep_fvt_seed17_syr_to_cop` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed17_syr_to_cop` |
| `full1ep_fvt_seed23_syr_to_cop` | `/home/axt/mnt2/jongha/v3_1/decoder_runs/full1ep_fvt_seed23_syr_to_cop` |

Each directory contains:

- `decoder_config.json`
- `decoder_training_curves.tsv`
- `translation_results.tsv`
- `translation_diagnostics.tsv`
- `sample_translations.md`
- `simple_decoder.pt`

## Next Selection Policy

For longer schedules, use dev chrF++ for checkpoint selection and report final_test once per selected checkpoint. If dev chrF++ ties, prefer the checkpoint with lower repetition/collapse diagnostics.
