# Step 15 Checkpoint Selection

Run id: `step15_v2_mlm_control_20260611_160304`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

## Selected Adapted Checkpoint

| Metric | Value |
| --- | --- |
| model family | `adapted_extended` |
| seed | `13` |
| checkpoint | `/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control/adapted_extended_seed13` |
| zero-step dev loss | `8.707869` |
| final dev loss | `5.601889` |
| delta | `-3.105981` |
| status | `PASS` |

## Selected Original-Control Checkpoint

| Metric | Value |
| --- | --- |
| model family | `original_control` |
| seed | `13` |
| checkpoint | `/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control/original_control_seed13` |
| zero-step dev loss | `4.524689` |
| final dev loss | `3.081141` |
| delta | `-1.443548` |
| status | `CONTROL_COMPLETE` |

## Aggregate Diagnostic

| Metric | Value |
| --- | --- |
| adapted mean final dev loss | `5.618403` |
| adapted std final dev loss | `0.015010` |
| original-control mean final dev loss | `3.123752` |
| original-control std final dev loss | `0.031961` |
| adapted/original ratio | `1.798607` |
| competitive margin | `1.100000` |
| claim gate | `FAIL` |

The loss ratio is diagnostic because tokenizer vocabularies differ. The selected checkpoints still require downstream and translation validation before any final top-tier claim.
