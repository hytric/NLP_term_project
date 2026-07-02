# 01 Merge

Use this folder for full corpus merge commands, detached run logs, final merge
manifest copies, and line-count/size checks.

Current dry-run artifacts:

- `../merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- `../merge/Glot500_v5_glot50010_xlmr100.report.json`

Current main merge artifact:

- `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt`
- `/home/axt/mnt2/jongha/v5_glot50010/logs/full_merge_20260626_230847.log`
- `../merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- `../merge/Glot500_v5_glot50010_xlmr100.report.json`

Current pilot artifacts:

- `../merge/Glot500_v5_glot50010_xlmr100_pilot10k.manifest.tsv`
- `../merge/Glot500_v5_glot50010_xlmr100_pilot10k.report.json`
- `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100_pilot10k.txt`

Pilot status:

```text
PASS, 1,020,000 lines, 212M, missing dirs 0
```

Main status:

```text
PASS, 92,452,251 lines, 19G, missing dirs 0, manifest rows 102/102 PASS
```

Canonical command:

```bash
DRY_RUN=1 bash preprocessing/run_v5_glot50010_merge.sh
bash preprocessing/run_v5_glot50010_merge.sh
```

Pilot command:

```bash
EXP_NAME=Glot500_v5_glot50010_xlmr100_pilot10k \
  MAX_SAMPLES_PER_LANGUAGE=10000 \
  bash preprocessing/run_v5_glot50010_merge.sh
```

## Next Step Gate

Move to `../02_tokenizer_train/` only after the merge is reproducible and
complete enough for tokenizer training.

Pass line:

- final or approved-pilot merged corpus path is written.
- merge manifest and report are saved.
- missing language dirs is `0`.
- planned and actual line counts are recorded.
- sampling policy for seen/head and target/tail groups is recorded.
- disk location and file size are recorded.

Required artifacts:

- final merge command
- detached run log or terminal log
- manifest TSV
- report JSON
- line-count check

If the full `92.45M` line merge is too expensive, an approved pilot corpus can
pass this gate only for pilot tokenizer or smoke tests. It cannot be used for
the main v5 tokenizer claim without being labeled pilot.
