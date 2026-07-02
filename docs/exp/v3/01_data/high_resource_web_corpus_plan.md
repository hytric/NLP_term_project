# High-Resource Web Corpus Plan

작성일: 2026-06-13

## Decision

Bible full-language data is not enough to call the replay source "true high-resource pretraining data." It remains useful as domain-matched replay/control, but third_try should add general-domain high-resource web text.

Use `cis-lmu/GlotCC-V1` as the first high-resource web source because:

- it is already used by existing project scripts for Coptic/Syriac;
- it is CommonCrawl-derived web text, not Bible-only;
- it exposes configs for the desired core languages;
- it can be sampled by shard to fit the 1-GPU/few-days budget.

## Core Configs

| Language | GlotCC config | Available shards | Available size |
| --- | --- | ---: | ---: |
| English | `eng-Latn` | 541 | 691.054 GB |
| German | `deu-Latn` | 90 | 134.654 GB |
| Japanese | `jpn-Jpan` | 2 | 2.451 GB |
| Korean | `kor-Hang` | 8 | 13.906 GB |

## Optional Configs

| Language | GlotCC config | Available shards | Available size |
| --- | --- | ---: | ---: |
| French | `fra-Latn` | 90 | 139.798 GB |
| Spanish | `spa-Latn` | 94 | 141.708 GB |
| Mandarin Chinese | `cmn-Hani` | 26 | 33.170 GB |
| Russian | `rus-Cyrl` | 106 | 257.588 GB |
| Hindi | `hin-Deva` | 1 | 1.321 GB |

## Materialization Command

Started with deterministic shard sampling:

```bash
python3 preprocessing/prepare_third_try_high_resource_glotcc.py \
  --configs eng-Latn,deu-Latn,jpn-Jpan,kor-Hang \
  --max-shards-per-config 2 \
  --max-docs-per-config 50000 \
  --max-lines-per-config 200000
```

Expected output root:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc`

Expected files:

- `glotcc_eng-Latn.jsonl`
- `glotcc_deu-Latn.jsonl`
- `glotcc_jpn-Jpan.jsonl`
- `glotcc_kor-Hang.jsonl`
- `high_resource_glotcc_manifest.tsv`

## Materialized Sample

실행일: 2026-06-13

Log:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc/logs/download_20260613.log`

| Config | Status | Selected shards | Selected source size | Docs written | Lines written | JSONL size |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `eng-Latn` | PASS | 2 / 541 | 2.559 GB | 11274 | 200000 | 69 MB |
| `deu-Latn` | PASS | 2 / 90 | 2.984 GB | 9573 | 200000 | 72 MB |
| `jpn-Jpan` | PASS | 2 / 2 | 2.451 GB | 20555 | 200000 | 111 MB |
| `kor-Hang` | PASS | 2 / 8 | 2.506 GB | 14732 | 200000 | 109 MB |

Total materialized lines: 800000

Manifest:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`

## Claim Wording

Allowed:

> high-resource web replay sampled from GlotCC-V1.

Allowed with caveat:

> high-resource replay/control under a compute-bounded deterministic shard sample.

Avoid:

> full high-resource pretraining corpus.

## Integration

Stage 01 should combine:

- target10 V2 train/dev split;
- GlotCC high-resource web sample for replay;
- Bible full-language high-resource as domain-matched control only.
