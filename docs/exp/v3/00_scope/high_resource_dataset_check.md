# High-Resource Dataset Check

작성일: 2026-06-13

## Summary

사용 가능한 high-resource Bible dataset은 domain-matched replay/control로는 충분하다. 하지만 일반적인 "진짜 high-resource continued pretraining corpus"라고 부르기에는 규모와 도메인이 부족하다. 따라서 third_try main에는 GlotCC-V1 web corpus를 추가한다.

Bible-domain replay/control에는 compute와 해석 안정성을 위해 아래 4개를 core로 추천한다.

| Role | Language | File | Verse rows | Status |
| --- | --- | --- | --- | --- |
| core replay/control | English | `English.xml` | 31102 | usable |
| core replay/control | German | `German.xml` | 31102 | usable |
| core replay/control | Japanese | `Japanese.xml` | 31087 | usable |
| core replay/control | Korean | `Korean.xml` | 31102 | usable |

Inventory:

- `high_resource_inventory.tsv`

## Recommended Use

Main mixture:

- target10 low-resource: use V2 clean split artifacts.
- true high-resource replay: use sampled `GlotCC-V1` web text for `eng-Latn`, `deu-Latn`, `jpn-Jpan`, `kor-Hang`.
- domain-matched high-resource control: use Bible `English.xml`, `German.xml`, `Japanese.xml`, `Korean.xml`.
- Sampling: cap or downweight high-resource rows so they do not dominate target10.

Optional expansion:

- Add French/Spanish/Chinese/Arabic/Russian/Hindi only if Stage 05 has spare compute or if high-resource control needs broader script/family coverage.
- Keep Greek/Latin as reference/pivot diagnostics, not core high-resource replay.

## Important Notes

- `English-WEB.xml`, `Japanese-tok.xml`, and `Chinese-tok.xml` are alternates. Do not use both raw and alternate versions of the same language in the same main mixture unless the duplication is intentional.
- Local Taxi1500 currently has English only, so it is not enough for target10 downstream success.
- The next missing artifact is `01_data/mlm_mixture_manifest.tsv`, which should combine target10 V2 train/dev with selected GlotCC web replay and Bible-domain control rows.
