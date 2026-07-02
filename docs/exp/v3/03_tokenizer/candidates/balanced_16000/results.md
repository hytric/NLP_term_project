# Stage 03 Results: Tokenizer Extension

작성일: 2026-06-13

Gate status: IN_PROGRESS

## Summary

Balanced high-resource + target10 corpus로 SentencePiece unigram `16000` auxiliary tokenizer를 학습하고, XLM-R-base 기존 vocab id를 보존한 상태에서 새 token만 append한 첫 main candidate를 만들었다.

## Candidate

| Item | Value |
| --- | --- |
| variant | `main_added_16000` |
| tokenizer path | `/home/axt/mnt2/jongha/third_try/tokenizers/stage03_20260613_r1/tokenizers/xlmr_third_try_mixture_added_16000` |
| base vocab size | 250002 |
| actual added tokens | 2621 |
| extended vocab size | 252623 |
| avg tokens/word delta | -10.242096% |
| avg single-char ratio delta | 61.494136% |

## Gate Evidence

- changed existing token ids: `0`
- changed special token ids: `0`
- appended token id violations: `0`
- fallback ablation is separated in `fallback_ablation.tsv`

## Remaining Work

- Candidate snapshot superseded by the selected 48000 top-level Stage 03 result.
- See `../../candidate_comparison.tsv` and `../../fallback_ablation_summary.tsv`.

## Failure Return

- failed gate: NOT_APPLICABLE_YET
- observed evidence: first main candidate created and structurally valid
- likely cause: candidate snapshot superseded by selected top-level Stage 03 result
- return-to stage: NOT_APPLICABLE_YET
- required fix before retry: NOT_APPLICABLE
