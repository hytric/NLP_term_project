# Third Try Final Diagnostic Report

작성일: 2026-06-13

## 결론

현재 세 번째 실험은 **positive claim으로 닫을 수 없다**. 대신 다음 진단적 결론으로 닫는 것이 안전하다.

> XLM-R-base에 id-preserving append-only vocabulary extension을 적용하면 target10 평균 tokenizer fragmentation은 줄어든다. 그러나 현재 compute-bounded Glot500-style continued-pretraining pilot에서는 이 tokenizer 개선이 broad target10 downstream/model improvement로 이어지지 않았고, high-resource control proxy도 악화되었다. 실패 조건은 vocab size, initialization, fallback, replay, appended-token learning ablation으로 설명해야 한다.

## Positive Claim 판정

| Requirement | Current Evidence | Verdict |
| --- | --- | --- |
| XLM-R-base 출발 | satisfied | PASS |
| 기존 vocab id 보존 append-only | changed existing ids = 0 | PASS |
| high-resource replay + target10 mixture | Stage 01/05 materialized mixture | PASS_WITH_DEVIATION |
| full MLM continued pretraining | 200-step pilot + replay-safe 1000-step 3-seed retry | PASS_RETRY_CANDIDATE |
| 3개 이상 seed | replay-safe fvt checkpoint seeds 13/17/23 | PASS_RETRY_CANDIDATE |
| target10 downstream 개선 | Coptic POS only; target10-wide supervised seed stability NOT_RUN | FAIL_FOR_POSITIVE |
| Coptic/Syriac 포함 | Coptic supervised; Syriac proxy-only | PARTIAL |
| high-resource no-collapse | replay-safe mean loss delta +0.675539; 0/4 pass threshold | FAIL_FOR_POSITIVE |

Final verdict: `NO_GO_FOR_POSITIVE_CLAIM`.

## Diagnostic Evidence

| Axis | Evidence | Reading |
| --- | --- | --- |
| tokenizer | target10 avg tokens/word delta `-29.812358%` | 평균 fragmentation은 개선됨 |
| fallback | byte fallback append delta is `-0.599816%` vs char | byte fallback은 tokenizer ablation에서 약간 우세하지만 main replacement는 아님 |
| init | fvt zero-step loss `7.925527`, best among tested methods | fvt 선택은 정당화됨 |
| MLM proxy | XLM-R `3.472837` vs replay-safe fvt mean `5.245928` | 200-step보다 개선됐지만 target10 proxy model quality는 여전히 XLM-R보다 악화 |
| Coptic POS | replay-safe token accuracy `+0.006781`, 3/3 checkpoint seeds | 약한 Coptic-only positive pilot; macro F1은 `-0.002656` |
| frozen proxy | retrieval 2/3 seeds positive, parallel AUC 1/3 | target10 proxy evidence mixed |
| high-resource control | replay-safe mean loss delta `+0.675539`, 0/4 pass | lower-LR retry로 완화됐지만 replay/control 실패 가능성 지속 |
| retained checkpoint selection | checkpoint-150 high-resource delta `+0.757355`, checkpoint-200 `+0.703114` | 저장된 earlier checkpoint 선택으로는 해결되지 않음 |
| replay-safe retry | target10 proxy `5.298593 -> 5.245928`, control delta `+0.703114 -> +0.675539` | 개선은 있으나 positive gate는 여전히 실패 |
| appended-token learning | second_try added-token loss dominates failure | tokenizer gain이 model gain으로 안 이어지는 핵심 원인 후보 |

Explicit Coptic/Syriac audit: `06_eval/coptic_syriac_evidence.md`.

- Coptic: tokenizer `-12.539893%`, replay-safe MLM proxy `+5.414744`, POS token accuracy `+0.006781`.
- Syriac: tokenizer `-66.873096%`, replay-safe MLM proxy `+3.025674`, supervised local downstream not found.

## Report Framing

Main text:

1. Glot500-style XLM-R-base vocabulary extension protocol.
2. Id-preserving append-only tokenizer construction.
3. High-resource replay + target10 mixture.
4. Stage05/06 current-candidate evidence.
5. Diagnostic negative conclusion.

Ablation section:

1. 8k/16k/32k/48k vocab size.
2. random/mean/fvt/align/focus initialization.
3. byte fallback vs character coverage.
4. high-resource replay/control vs target-only or original-control evidence.
5. appended-token failure and repair probes.
6. first_try translation/retrieval failures as downstream proxy diagnostics.

## Next Decision

If the objective is a **positive model claim**, return to Stage 05:

- go beyond the current replay-safe 1000-step retry;
- rebalance or strengthen high-resource replay/control;
- keep at least 3 seeds;
- rerun high-resource control;
- add stronger target10 downstream evidence, especially Syriac.

If the objective is a **finished course/report claim**, use Stage 07/08:

- claim diagnostic negative only;
- keep first_try/second_try as ablation/failure analysis;
- do not state that tokenizer improvement caused downstream improvement.

## Current Gate

- Stage 07: `PASS_NEGATIVE_MAIN_READY`
- Stage 08: `PASS_ABLATION_PACKAGE_READY`
- Active project goal: not complete as a positive full-budget experiment; complete enough for a diagnostic negative report package.
