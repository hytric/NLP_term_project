# Merge Artifacts

이 폴더는 pilot and main corpus merge manifest/report를 보관한다.

Main evidence:

- `Glot500_v5_glot50010_xlmr100.report.json`
- `Glot500_v5_glot50010_xlmr100.manifest.tsv`

Promotion rule: use the main merge as report evidence only when the report is
`PASS`, missing language dirs are `0`, and actual sample count matches the
planned sample count.
