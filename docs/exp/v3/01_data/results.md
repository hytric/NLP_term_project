# Stage 01 Results: Data Collection And Split

작성일: 2026-06-13

Gate status: PASS

## Summary

Stage 01 manifest 생성을 완료했다. Main training mixture에는 target10 V2 train, GlotCC-V1 high-resource web replay, Bible high-resource domain control이 동시에 들어간다.

Target10 train에서 dev/final과 exact text가 겹치는 rows는 main train row index에서 제외했다.

GPU constraint: all GPU runs after this stage must use `CUDA_VISIBLE_DEVICES=3`.

## Main Counts

| Component | Rows |
| --- | ---: |
| target10 V2 train, original | 52124 |
| target10 V2 train, exact eval duplicates excluded | 52016 |
| excluded target10 train duplicates | 108 |
| GlotCC-V1 web replay | 800000 |
| Bible domain control, heldout books excluded | 114136 |
| total MLM train row index | 966152 |
| target10 V2 dev | 6521 |
| target10 V2 final test | 9804 |

## Leakage Controls

- target10 train/dev/final overlap by `iso + verse_id`: PASS
- target10 exact text overlap across train/dev/final: PASS
- Bible control excludes held-out books: `ACT,JOH,MAR`
- GlotCC web replay is non-Bible high-resource web data.

## Artifacts

| Artifact | Path |
| --- | --- |
| corpus manifest | `corpus_manifest.tsv` |
| split manifest | `split_manifest.tsv` |
| high-resource manifest | `high_resource_manifest.tsv` |
| MLM mixture manifest | `mlm_mixture_manifest.tsv` |
| leakage audit | `leakage_audit.tsv` |
| row-level train index | `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_train_rows.tsv` |
| row-level dev index | `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_dev_rows.tsv` |
| row-level final index | `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/final_eval_rows.tsv` |
| excluded target10 train duplicates | `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/target10_train_exact_duplicate_exclusions.tsv` |

## Stage 02 Handoff

Stage 02 can now run XLM-R-base baseline audits using GPU 3 only:

```bash
CUDA_VISIBLE_DEVICES=3 <baseline command>
```

## Failure Return

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- likely cause: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix before retry: NOT_APPLICABLE
