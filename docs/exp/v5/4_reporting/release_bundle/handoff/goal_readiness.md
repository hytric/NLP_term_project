# v5 Goal Readiness Audit

작성일: 2026-06-28

Verdict: `goal_readiness_ready_for_post_checkpoint_eval`

## Verdict

현재 상태는 **main execution을 시작할 준비는 되었지만, final result claim을 할 준비는 아직 아니다**.
데이터 선택, folder gate, main tokenizer, main initialization, main zero-step evidence는 좋다.
남은 blocker: matched v5 metric outputs and remaining blocked data.

Glot500 재연성 표현은 아래처럼 제한해야 한다.

- 가능: `controlled 102-language subset에서 Glot500-style pipeline 재연`
- 불가: `Glot500 511-language full reproduction 완료`

## Stage Audit

| Stage | Status | Goal Clarity | Evidence | Next Line |
| --- | --- | --- | --- | --- |
| data scope freeze | ready | clear | target10 manifest exists; dry-run missing_language_dirs=0 | scope is frozen; use this manifest for all main runs |
| corpus merge | ready | clear | main corpus exists: /home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt; report status=PASS; actual_total_samples=92452251 | main tokenizer training may start |
| tokenizer expansion | ready | clear | main tokenizer exists: /home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm; target_len=368687; novel_tokens=118685; mask_id=368686; main audit exists | full initialization checkpoints may start |
| embedding initialization | ready | clear | full random/mean/fvt init reports exist; FVT rows=118427; fallback=2; mask diff=0.0; tied=True; main zero-step exists | MLM training may start |
| training parity contract | ready | clear | training_parity_audit=training_parity_ready; v5_random/v5_fvt share corpus, tokenizer, schedule, checkpoint rule, and downstream eligibility | none |
| continued MLM | ready | clear | random_state=ready; fvt_state=ready; paired 10K checkpoints exist | checkpoint selection and downstream evaluation may start |
| Glot500 metric evaluation | partial_baselines_measured | clear | measured model outputs exist: pseudoperplexity=glot500_base,v5_random,xlmr_base; retrieval_tatoeba=glot500_base,v5_fvt,v5_random,xlmr_base; retrieval_bible=glot500_base,v5_fvt,v5_random,xlmr_base; text_classification=glot500_base,v5_fvt,v5_random,xlmr_base; ner=glot500_base,v5_random,xlmr_base; pos=glot500_base,v5_random,xlmr_base; roundtrip_alignment=glot500_base,v5_random,xlmr_base; coverage: pseudoperplexity 102/102; retrieval_tatoeba 63/102; retrieval_bible 74/102; text_classification 1/102; ner 78/102; pos 58/102; roundtrip_alignment 74/102 | after matched v5 checkpoints, run `bash scripts/run_v5_post_checkpoint_evals.sh status`, then confirm `post_checkpoint_preflight_ready_to_launch`, then `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all` for the current measured-row queue; canonical full rerun command is `WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`; keep pending/blocked metric status explicit |
| reporting and aggregation | skeleton_ready | clear | Report/PPT drafts exist; aggregation skeleton can mark measured/blocked/pending | replace unresolved result slots only from measured artifacts |

## Novelty Audit

- status: `positioned`
- evidence: v5-target weighted NLL delta fvt-random = -9.626238
- novelty 위치: corpus novelty가 아니라, vocabulary extension 이후 새 embedding row initialization 비교.
- main claim 조건: `v5_random`과 `v5_fvt`가 같은 tokenizer, corpus, seed, MLM budget, checkpoint selection rule을 공유해야 한다.
- parity audit: training_parity_audit=training_parity_ready; v5_random/v5_fvt share corpus, tokenizer, schedule, checkpoint rule, and downstream eligibility
- 반드시 남길 audit: source row identity copy, `<mask>` remap, byte-row handling, LM-head tying, new-row norm.

## Evaluation Coverage Snapshot

pseudoperplexity 102/102; retrieval_tatoeba 63/102; retrieval_bible 74/102; text_classification 1/102; ner 78/102; pos 58/102; roundtrip_alignment 74/102

Target10 coverage snapshot:

pseudoperplexity 10/10; retrieval_tatoeba 0/10; retrieval_bible 0/10; text_classification 0/10; ner 0/10; pos 0/10; roundtrip_alignment 0/10

Interpretation: v5 target10은 raw-text PPPL에는 10/10으로 사용 가능하지만,
현재 retained downstream task families의 target10 coverage는 0/10이다.
따라서 downstream claim은 available-language/head/all 중심으로 두고,
target10 downstream은 coverage-limited로 보고해야 한다.

## Immediate Execution Line

1. `v5_random`과 `v5_fvt` MLM을 같은 budget으로 학습한다.
2. matched v5 checkpoints가 준비되면 `bash scripts/run_v5_post_checkpoint_evals.sh status`로 model matrix, checkpoint manifest, evaluation queue, command consistency, parser contract, post-checkpoint preflight를 갱신한다.
3. 권장 one-shot 경로는 `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_ready_to_final_package.sh`이다. 이 launcher는 `READY_TO_LAUNCH=yes`가 아니면 평가를 거부하고, ready이면 evaluation, refresh, Final Evidence Packet audit까지 수행한다.
4. `post_checkpoint_preflight.md`가 `post_checkpoint_preflight_ready_to_launch`를 보고한 뒤에만 `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`로 남은 PPPL과 available downstream v5 rows를 실행한다. canonical full rerun command는 `WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`이다.
5. `python3 scripts/refresh_v5_reporting.py --with-plots`로 aggregation, gates, figures, report/PPT audits를 갱신한다.
