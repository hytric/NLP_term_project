# Table 3. Initialization And Zero-Step MLM Proxy

Last updated: 2026-06-27

Caption draft:

```text
Before continued MLM training, source-token decomposition initialization (FVT)
substantially improves weighted MLM proxy NLL over random resize and global
mean initialization, especially on the v5 target group.
```

| Method | New-row initialization | v5-target weighted NLL | head weighted NLL | all weighted NLL |
| --- | --- | ---: | ---: | ---: |
| `v5_random` | 118,685 random rows | 18.411756 | 12.895301 | 16.511807 |
| `v5_mean` | 118,685 global/source mean rows | 11.953142 | 8.037017 | 10.604370 |
| `v5_fvt` | 118,427 FVT rows + 2 lexical fallback rows + 256 byte rows | 8.785518 | 6.621457 | 8.040183 |

| Comparison | v5-target delta | head delta | all delta |
| --- | ---: | ---: | ---: |
| `v5_fvt - v5_random` | -9.626238 | -6.273844 | -8.471624 |
| `v5_fvt - v5_mean` | -3.167624 | -1.415560 | -2.564187 |

Audit line:

- source identity rows copied: 250,002
- `<mask>` remap diff: 0.0
- LM head tied after init: true

Source artifacts:

- `docs/exp/v5/1_embedding/04_zero_step_eval/main/summary.tsv`
- `docs/exp/v5/1_embedding/04_zero_step_eval/main/analysis.md`
- `docs/exp/v5/1_embedding/05_audit/main/init_reports/fvt_init_report.json`

