# Stage 00 Results: Scope Freeze

작성일: 2026-06-13

Gate status: PASS

## Summary

Stage 00 scope를 닫는다. Main target은 기존 target10 전체이며, Coptic/Syriac는 extension이 아니라 main experiment이다. Base model은 `xlm-roberta-base`만 사용하고, `xlm-roberta-large`는 제외한다.

High-resource 조건은 두 역할로 분리한다.

- True high-resource web replay: GlotCC-V1 `eng-Latn`, `deu-Latn`, `jpn-Jpan`, `kor-Hang`
- Domain-matched high-resource control: Bible English, German, Japanese, Korean

## Evidence

| Item | Evidence | Status |
| --- | --- | --- |
| target10 main inventory | `language_inventory.tsv` | PASS |
| Coptic/Syriac main role | `cop`, `syr` rows marked `IN_MAIN` | PASS |
| high-resource Bible control | `high_resource_inventory.tsv` | PASS |
| true high-resource web replay | `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv` | PASS |
| mixture rule | `mixture_contract.tsv` | PASS |
| task availability | `task_availability.tsv` | PASS |
| fixed decisions | `scope_decisions.tsv` | PASS |

## High-Resource Web Replay

| Config | Lines | Docs | Status |
| --- | ---: | ---: | --- |
| `eng-Latn` | 200000 | 11274 | PASS |
| `deu-Latn` | 200000 | 9573 | PASS |
| `jpn-Jpan` | 200000 | 20555 | PASS |
| `kor-Hang` | 200000 | 14732 | PASS |

Total materialized lines: 800000

## Stage 01 Handoff

Stage 01 must build these artifacts before Stage 02 starts:

- `01_data/corpus_manifest.tsv`
- `01_data/high_resource_manifest.tsv`
- `01_data/mlm_mixture_manifest.tsv`
- `01_data/leakage_audit.tsv`
- `01_data/results.md`

## Failure Return

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- likely cause: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix before retry: NOT_APPLICABLE
