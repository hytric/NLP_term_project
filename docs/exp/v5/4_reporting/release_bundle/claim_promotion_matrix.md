# v5 Claim Promotion Matrix

Last checked: 2026-06-28 18:08 KST

Verdict: `claim_boundaries_ready_pending_results`

This generated matrix turns the claim ledger into report/PPT update
instructions. A claim is promotable only when its evidence and gate are
both current. Disallowed claims should stay visible here because they are
useful guardrails during final writing.

| Claim | Promotion state | Current evidence | Unlock gate | Report action | Slide action |
| --- | --- | --- | --- | --- | --- |
| controlled 102-language Glot500-style replay | promotable_now | ledger=supported; merge=PASS; seen=92; target=10; samples=92452251 | none | Use in abstract/introduction/method, always with controlled-subset wording. | Use on slides 1, 3, and 14 as the reproduction boundary. |
| full 511-language Glot500 reproduction | disallowed | ledger=disallowed | not unlockable within v5 scope | Do not use this phrase in the final report. | Do not use this phrase in the title, conclusion, or Q&A. |
| target10 is Glot500-internal and diversity-selected | promotable_now | ledger=supported | none | Use in data section with manifest path and 30K threshold. | Use on target-selection slide with region/script diversity. |
| main tokenizer expansion is structurally valid | promotable_with_caveat | ledger=proven with documented risk; target_len=368687; appended=118685; dzo_Tibt_regression=documented | none | Report 29/30 fertility improvement and keep dzo_Tibt in limitations. | Show tokenizer gain and the dzo_Tibt caveat on slide 6 or 13. |
| tokenizer improves every target language | disallowed | ledger=disallowed; dzo_Tibt=worse | only unlockable after a repaired tokenizer audit | Do not state universal target improvement. | Keep dzo_Tibt visible if discussing target language details. |
| FVT improves zero-step target MLM proxy over random | promotable_now | ledger=proven intrinsically; target_weighted_nll_delta_fvt_minus_random=-9.626238 | none | Use as the completed intrinsic novelty result. | Use as the main evidence on initialization slides 8 and 12. |
| FVT improves after-MLM PPPL over random | locked_pending_result | ledger=pending; matched_gate=ready; pppl_gate=pending | matched checkpoints ready and after-MLM PPPL parsed for v5_random/v5_fvt | Keep as hypothesis until PPPL rows are parsed; then choose result_interpretation_blocks outcome. | Do not upgrade slide 12/14 until aggregation contains both v5 rows. |
| FVT improves downstream performance | locked_pending_result | ledger=pending; downstream_gate=pending; metrics=pseudoperplexity:partial,retrieval_tatoeba:measured,retrieval_bible:measured,text_classification:measured,ner:partial,pos:partial,roundtrip_alignment:partial | available downstream rows parsed for v5_random/v5_fvt | Report available-language results only; avoid target10 downstream wording unless coverage changes. | Update main results and conclusion slides only from aggregation tables. |
| all Glot500 metric families are retained | promotable_as_protocol_execution_partial | ledger=supported; metrics=pseudoperplexity:partial,retrieval_tatoeba:measured,retrieval_bible:measured,text_classification:measured,ner:partial,pos:partial,roundtrip_alignment:partial; roundtrip_gate=pending | final performance claims still depend on parsed v5 rows or explicit blockers | Use as evaluation-protocol fidelity claim, not as full measured-results claim. | Use on metric-fidelity slide with pending/blocked status and coverage caveats. |
| target10 downstream improves | disallowed_for_now | ledger=disallowed for now; target10_downstream_coverage_zero=True | target10 downstream task data materialized and evaluated | Limit target10 claims to tokenization, zero-step, and PPPL unless coverage changes. | Frame downstream as available-language/head/all replay. |
| Glot500-base is an equal-budget baseline | disallowed | ledger=disallowed | not unlockable without equal-budget retraining | Call Glot500-base an external reference only. | Use external-reference wording in result and Q&A slides. |

Final-use rule:

- `promotable_now` and `promotable_with_caveat` claims can appear in the
  current report/PPT if their caveats remain attached.
- `locked_pending_result` claims must stay as hypotheses until the named
  gate is ready and aggregation has parsed the relevant rows.
- `disallowed` claims should not appear as positive claims anywhere in the
  final report or deck.
