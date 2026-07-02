# Step 15 Checkpoint Selection

Run id: `step15_v2_mlm_control_20260611_163731`

Selection data: `MAR` dev only.

Final data access: `NO_ACT_FINAL_ACCESS`.

## Selected Adapted Checkpoint

| Metric | Value |
| --- | --- |
| model family | `adapted_extended` |
| seed | `23` |
| checkpoint | `/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control_token500k/adapted_extended_seed23` |
| zero-step dev loss | `8.711814` |
| final dev loss | `4.934210` |
| delta | `-3.777604` |
| status | `PASS` |

## Selected Original-Control Checkpoint

| Metric | Value |
| --- | --- |
| model family | `original_control` |
| seed | `23` |
| checkpoint | `/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control_token500k/original_control_seed23` |
| zero-step dev loss | `4.521164` |
| final dev loss | `2.471175` |
| delta | `-2.049989` |
| status | `CONTROL_COMPLETE` |

## Aggregate Diagnostic

| Metric | Value |
| --- | --- |
| adapted mean final dev loss | `4.946829` |
| adapted std final dev loss | `0.009023` |
| original-control mean final dev loss | `2.518008` |
| original-control std final dev loss | `0.033126` |
| adapted/original ratio | `1.964580` |
| competitive margin | `1.100000` |
| token budget target | `500000` |
| train token range | `500008-500407` |
| token budget tolerance | `1.020000` |
| claim gate | `FAIL` |

The loss ratio is diagnostic because tokenizer vocabularies differ. The selected checkpoints still require downstream and translation validation before any final top-tier claim.
