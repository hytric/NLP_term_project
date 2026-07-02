# Stage 04 Results: Model Initialization

작성일: 2026-06-13

Gate status: PASS

## Summary

Stage 03에서 선택한 third_try target-heavy high-resource 48k tokenizer에 맞춰 `xlm-roberta-base`를 resize하고, 다섯 가지 embedding initialization 후보를 생성했다.

Selected init method: `fvt`

Selected checkpoint:

`/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt`

## Candidate Summary

| Init | New rows | Fallback rows | Zero-step dev loss | Status |
| --- | ---: | ---: | ---: | --- |
| random | 30849 | 0 | 17.998567 | PASS |
| mean | 30849 | 0 | 10.910376 | PASS |
| fvt | 30849 | 0 | 7.925527 | PASS |
| align | 30849 | 11070 | 8.700895 | PASS |
| focus | 30849 | 11070 | 16.760191 | PASS |

## Gate Evidence

- Base embedding row drift: 0.
- Base LM head row drift: 0.
- New row count mismatch: 0.
- Random init exists.
- Four non-random init methods exist.
- Input embedding and LM head shapes match tokenizer length.
- Weight tying is preserved.
- No initialized row is NaN or zero-norm.
- GPU work used `CUDA_VISIBLE_DEVICES=3`.

## Important Note

`fvt` is selected only for the first Stage 05 pilot because it has the best zero-step Mark/dev MLM loss. The final claim still requires model training and downstream evaluation with at least 3 seeds.

## Failure Return

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- likely cause: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix before retry: NOT_APPLICABLE
