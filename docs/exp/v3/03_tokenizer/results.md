# Stage 03 Results: Tokenizer Extension

작성일: 2026-06-13

Gate status: PASS_DEVIATION_AND_FALLBACK_ABLATION_DOCUMENTED

## Summary

Target-heavy high-resource + target10 corpus로 SentencePiece unigram `48000` auxiliary tokenizer를 학습하고, XLM-R-base 기존 vocab id를 보존한 상태에서 새 token만 append한 provisional main candidate를 만들었다.

## Candidate

| Item | Value |
| --- | --- |
| variant | `main_added_48000` |
| tokenizer path | `/home/axt/mnt2/jongha/third_try/tokenizers/stage03_targetheavy_20260613_r3/tokenizers/xlmr_third_try_mixture_added_48000` |
| base vocab size | 250002 |
| actual added tokens | 30849 |
| extended vocab size | 280851 |
| avg tokens/word delta | -29.812358% |
| worst language tokens/word delta | +1.504758% |
| avg single-char ratio delta | +37.402719% |

## Candidate Comparison

See `candidate_comparison.tsv`.

The selected candidate is preferred over `third_try_balanced_16k` because it improves average target10 tokens/word much more strongly and reduces the worst-case degradation. It is preferred as the main third_try tokenizer over the reused second_try target-only tokenizer because it keeps high-resource replay/control text in the tokenizer training corpus, matching the third_try novelty condition.

## Fallback Ablation

See `fallback_ablation_summary.tsv` and `fallback_ablation_comparison.tsv`.

| Variant | Avg append tokens/word delta vs XLM-R | Worst append delta | Avg new-token hit rate | Status |
| --- | ---: | ---: | ---: | --- |
| `char_coverage_1_0` | -29.812358% | +1.504758% | 0.520904 | main-compatible |
| `byte_fallback_0_9995` | -30.215948% | +0.540536% | 0.523078 | ablation-only |

The byte-fallback auxiliary tokenizer is slightly better than the character-coverage variant on target10 dev tokenization: mean auxiliary tokens/word delta is `-0.733735%`, and mean append-only XLM-R tokens/word delta versus the char variant is `-0.599816%`. This does not replace the main tokenizer, because SentencePiece BYTE pieces are not faithfully activated by literal `add_tokens` matching in the XLM-R tokenizer. The result is therefore used as fallback-axis diagnostic evidence, not as a new main candidate.

## Gate Evidence

- changed existing token ids: `0`
- changed special token ids: `0`
- appended token id violations: `0`
- fallback ablation is separated and measured in `fallback_ablation.tsv`

## Remaining Work

- Proceed with this provisional candidate into Stage 04/05/06 interpretation unless downstream/model evidence rejects it.
- Treat byte fallback as an ablation-only result unless the tokenizer implementation is changed from `add_tokens` extension to a tokenizer that can execute SentencePiece byte fallback directly.

## Deviation

- Planned grid was 8k/16k/32k plus selected main size.
- A 48k target-heavy high-resource candidate was added because 16k/32k high-resource candidates left larger worst-case tokenization degradation.
- This deviation is allowed as a compute-bounded tokenizer selection choice and must be reported in final claims.

## Failure Return

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- likely cause: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix before retry: NOT_APPLICABLE
