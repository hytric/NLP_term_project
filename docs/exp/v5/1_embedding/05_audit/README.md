# 05 Embedding Audit

Use this folder for cross-method audits:

- copied source row preservation
- target-only row initialization status
- byte row status
- `<mask>` row status
- input embedding / LM head consistency

Current pilot FVT smoke artifact:

```text
pilot10k/fvt_init_report.json
pilot10k/init_reports/
```

Pilot FVT smoke status:

```text
<mask> remap diff 0.0 + LM head tied true
```

Current main audit artifacts:

```text
main/init_reports/random_init_report.json
main/init_reports/mean_init_report.json
main/init_reports/fvt_init_report.json
```

Main audit status:

| Method | Target Len | New Rows | Main Init Rows | Byte Rows | Mask Diff | LM Head Tied |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| random | 368,687 | 118,685 | 118,685 random | 256 | 0.0 | true |
| mean | 368,687 | 118,685 | 118,685 mean | 256 | 0.0 | true |
| fvt | 368,687 | 118,685 | 118,427 FVT + 2 fallback | 256 | 0.0 | true |

## Next Step Gate

Move to `../../2_training/` only after the checkpoint audit passes for every
method that will be trained.

Pass line:

- source token rows are copied by token identity, not id prefix.
- target-only lexical rows have a known initialization source.
- special tokens, especially `<mask>`, are mapped correctly.
- byte rows are separated from lexical rows in the audit.
- input embedding and LM head are tied or intentionally untied with a reason.
- all trained methods have comparable audit reports.

Required artifacts:

- cross-method audit table
- per-method `init_report.json` links
- `<mask>` audit table
- byte-row audit table
- final pass/fail note

If any required method fails this audit, regenerate that checkpoint before MLM
training.

Current status: pass for `random`, `mean`, and `fvt`.
