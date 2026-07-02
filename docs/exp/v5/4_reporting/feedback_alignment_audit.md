# v5 Feedback Alignment Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `feedback_aligned_pending_results`

This generated audit maps `feadback.md` requirements to concrete v5
artifacts. It answers whether the experiment is ready to execute,
whether the Glot500 replay claim is bounded correctly, and whether the
novelty path is placed in a defensible way.

| Feedback item | Status | Feedback requirement | Evidence | Action |
| --- | --- | --- | --- | --- |
| feedback source retained | ready | Keep the meeting feedback as an auditable source for report/PPT decisions. | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/feadback.md | none |
| target10 selection follows feedback | ready | Use 10 Glot500-internal target languages, each with at least 30K examples, selected for region/script diversity. | rows=10; min_new_length=30052; scripts=5; regions=10; glot500_raw=True | none |
| controlled Glot500 replay scope | ready | Reproduce the Glot500 workflow on the v5 controlled subset rather than claim a full 511-language rerun. | merge_status=PASS; seen=92; target=10; samples=92452251 | none |
| head-tail-all framing | ready | Preserve Glot500's head/tail/all comparison, with low-resource target languages visible. | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/Plan.md; /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/3_evaluation/glot500_metric_requirements.md | none |
| Glot500 metric families retained | protocol_ready_execution_partial | Measure every Glot500 metric family: PPPL, Tatoeba, Bible, text classification, NER, POS, and Roundtrip. | present=ner,pos,pseudoperplexity,retrieval_bible,retrieval_tatoeba,roundtrip_alignment,text_classification; statuses=ner:partial;pos:partial;pseudoperplexity:partial;retrieval_bible:measured;retrieval_tatoeba:measured;roundtrip_alignment:partial;text_classification:measured | finish v5_random/v5_fvt rows after matched checkpoints and post-checkpoint preflight; keep pending/blocked rows explicit |
| coverage and eval caveats recorded | ready_with_caveat | Do not hide missing task coverage; record measured language sets and target10 exclusions. | coverage_all_102=True; pppl_target10=True; target10_downstream_zero=retrieval_tatoeba,retrieval_bible,text_classification,ner,pos,roundtrip_alignment | keep coverage-limited language in report/PPT until new task data is materialized |
| Glot500 vs Yamaguchi method boundary | ready | Explain that v5 main tokenization is Glot500-style, while the earlier add-token path is Yamaguchi-style framing. | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/Report.md | none |
| initialization novelty is isolated | intrinsic_ready_after_mlm_pending | Compare new-token embedding initialization methods under the same tokenizer/corpus setup. | init_reports=3; zero_step_target_nll_delta_fvt_minus_random=-9.626238 | wait for after-MLM PPPL and downstream rows before promoting final method claims |
| matched MLM comparison gate | ready | Only compare random vs FVT after matched 10K checkpoints are selected. | matched_gate=ready | run `bash scripts/run_v5_post_checkpoint_evals.sh status` after both model files exist; launch long eval only after post-checkpoint preflight is ready-to-launch |
| downstream task replay gate | pending_result | Run available downstream tasks for v5_random and v5_fvt instead of stopping at intrinsic metrics. | downstream_gate=pending; v5_pending_metrics=ner,pos,pseudoperplexity,roundtrip_alignment; baseline_models=ner:glot500_base,v5_random,xlmr_base;pos:glot500_base,v5_random,xlmr_base;pseudoperplexity:glot500_base,v5_random,xlmr_base;retrieval_bible:glot500_base,v5_fvt,v5_random,xlmr_base;retrieval_tatoeba:glot500_base,v5_fvt,v5_random,xlmr_base;roundtrip_alignment:glot500_base,v5_random,xlmr_base;text_classification:glot500_base,v5_fvt,v5_random,xlmr_base | after checkpoints and post-checkpoint preflight, run `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all` for the current measured-row queue |
| Roundtrip retained with explicit gate | ready | Roundtrip is a required Glot500 metric family; document either blocker evidence or the runnable available-language gate rather than omit it. | roundtrip_blocker_verdict=roundtrip_inputs_ready_pending_results | baseline/reference rows are measured; run v5 rows after checkpoints and post-checkpoint preflight, and keep target10 0/10 caveat |
| optional embedding similarity diagnostic | optional_scoped | Use 2D/sentence-vector similarity only as explanatory novelty, not as a replacement for Glot500 metrics. | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/3_evaluation/08_embedding_similarity/README.md | add source data and figures only if time remains after required metrics |
| claim locks and no overclaim | ready | Keep unsupported claims locked: no full Glot500 rerun claim, no target10 downstream improvement claim yet, no equal-budget Glot500-base baseline claim. | /home/axt/jongha/Glot500-py39-eval/docs/exp/v5/4_reporting/03_final_report/claim_ledger.md | review claim ledger before final conclusion and slide summary |
| report and PPT scaffolding | needs_document_cleanup | Maintain report/PPT drafts, source maps, citations, figures, and finalization gates while results are pending. | reporting_package_audit=needs_document_cleanup | promote from execution draft only after matched checkpoints and parsed metrics |
| operational handoff commands | ready | Make the next execution step reproducible through guarded scripts rather than manual command fragments. | scripts/run_v5_post_checkpoint_evals.sh; scripts/watch_v5_mlm_handoff.sh | use watcher for status-only polling and paired wrapper after checkpoints and post-checkpoint preflight |

Readiness interpretation:

- The v5 plan is execution-ready as a controlled 102-language
  Glot500-style replay, not as a full 511-language reproduction.
- The novelty axis is well placed: tokenizer/corpus are held fixed while
  new-token embedding initialization is compared.
- Final result claims remain locked until matched `v5_random` and
  `v5_fvt` checkpoints are selected and required metrics are parsed.
- Roundtrip and target10 downstream coverage gaps are documented as
  explicit limitations rather than silent omissions.
