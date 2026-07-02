# v5.1 Tokenizer Stage

This folder tracks the downstream-aware target10 data scope, merge, tokenizer
training, and tokenizer audit.

## Stage Status

| Step | Status | Evidence |
| --- | --- | --- |
| target10 selection | done | `miscellaneous/glot50010_selected_manifest.tsv` |
| raw symlinks | done | `/home/axt/mnt2/jongha/v5_1_glot50010/raw`, count `102` |
| merge dry-run | done | `merge/Glot500_v51_glot50010_xlmr100.report.json` |
| full merge | done | strict 5% report PASS, line count `8,130,401` |
| tokenizer train | done | strict output dir exists |
| tokenizer audit | done | `03_audit/strict_5pct/results.md`, failures `0` |

## Stage Exit Line

```text
full merge PASS + extended tokenizer built + tokenizer audit failures = 0
```

## Important Difference From v5

v5.1 uses higher-resource target languages to make downstream target evaluation
possible. The dry-run planned corpus is therefore larger:

```text
v5   planned total samples:  92,452,251
v5.1 planned total samples: 162,608,099
```
