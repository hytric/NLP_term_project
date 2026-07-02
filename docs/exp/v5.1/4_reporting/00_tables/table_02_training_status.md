# Table 02. v5.1 Live Training Status

Last checked: 2026-06-28 21:56:49 KST

## Training Setting Check

| Field | Expected | Observed | Status |
| --- | --- | --- | --- |
| optimizer | `AdamW` | `AdamW` | `ok` |
| learning_rate | `initial=5e-5` | `initial=; latest=2.01e-05` | `check` |
| adam_beta1 | `0.9` | `` | `check` |
| adam_beta2 | `0.999` | `` | `check` |
| per_device_batch | `8` | `` | `check` |
| gpu_count | `3` | `3` | `ok` |
| gradient_accumulation | `16` | `` | `check` |
| effective_batch | `384` | `384` | `ok` |
| sequence_length | `512` | `` | `check` |
| max_steps | `3000` | `3000` | `ok` |
| fp16 | `True` | `` | `check` |

## GPU Usage

| GPU | Role | Memory | GPU util |
| ---: | --- | ---: | ---: |
| 0 | v5.1_mlm_training | 1842/49140 MB (3.7%) | 0% |
| 1 | v5.1_mlm_training | 2144/49140 MB (4.4%) | 0% |
| 2 | other_process_or_available | 11/49140 MB (0.0%) | 0% |
| 3 | v5.1_mlm_training | 124/49140 MB (0.3%) | 0% |
