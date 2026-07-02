# Stage 02 Results: XLM-R Baseline Audit

작성일: 2026-06-13

Gate status: IN_PROGRESS

## Summary

XLM-R-base tokenizer baseline과 deterministic 15% masked-LM eval baseline을 target10 final test에서 산출했다. Exact PPPL과 downstream baseline은 아직 실행 전이며, GPU가 필요한 실행은 사용자 지시에 따라 `CUDA_VISIBLE_DEVICES=3`으로만 진행한다.

## Current Evidence

| Item | Status |
| --- | --- |
| target10 tokenization metrics | PASS |
| high-resource control tokenization sample metrics | PASS |
| XLM-R-large excluded | PASS |
| deterministic masked-LM eval baseline | PASS |
| exact PPPL baseline | DEFERRED_COMPUTE |
| downstream baseline | PENDING_TASK_SELECTION |

## Target10 Summary

| Metric | Value |
| --- | ---: |
| avg tokens/word | 3.011828 |
| avg single-character token ratio | 0.305295 |
| avg deterministic MLM loss | 3.472799 |
| avg deterministic MLM perplexity | 155.299643 |
| final-test rows | 9804 |

## Important Interpretation Note

Low MLM loss for Cherokee/Coptic/Ojibwa is partly caused by high `<unk>` behavior in XLM-R tokenization. This should not be interpreted as good downstream representation quality. The tokenizer metrics and MLM eval must be read together.

## Next Command Constraint

All GPU commands:

```bash
CUDA_VISIBLE_DEVICES=3 <command>
```

## Failure Return

- failed gate: NOT_APPLICABLE_YET
- observed evidence: tokenization and deterministic MLM eval complete; exact PPPL/downstream pending
- likely cause: NOT_APPLICABLE_YET
- return-to stage: NOT_APPLICABLE_YET
- required fix before retry: run exact PPPL if budget allows and downstream baseline on GPU 3
