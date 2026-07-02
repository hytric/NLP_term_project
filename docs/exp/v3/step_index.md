# Third Try Step Index

작성일: 2026-06-12

이 파일은 `third_try`의 실행 단계를 잠금식으로 정의한다. 중심 원칙은 target10 low-resource 실제 성능 개선 모델을 만들되, Glot500에서 배운 id-preserving vocabulary extension과 high-resource replay 원칙을 적용하는 것이다.

## Global Rule

- 모든 작업 문서는 `/home/axt/jongha/Glot500-py39-eval/docs/exp/third_try` 안에 둔다.
- 각 stage는 자기 폴더 안의 `plan.md`, `results.md`, `score_table.tsv`, `file_results.tsv`를 기준으로 진행한다.
- 다음 main stage로 이동하려면 현재 stage의 `results.md`에 `Gate status: PASS`가 있어야 한다.
- `PASS_NEGATIVE_RESULT`는 실패가 아니라 negative evidence를 완결한 상태다. 이 경우 다음 synthesis stage로 이동할 수 있지만 positive claim은 금지한다.
- `score_table.tsv`에는 `TBD`, 빈칸, `NA_NOT_CHECKED`가 남아 있으면 안 된다.
- `file_results.tsv`에는 각 생성 파일의 path, count/size, checksum 가능 여부, status를 기록한다.
- Main run과 ablation run의 artifact, score, claim 문구를 섞지 않는다.
- 실패하면 실패 stage의 `results.md`에 원인, 되돌아갈 stage, 재실행 조건을 적고 필요한 이전 stage로 돌아간다.
- 반복 실행은 덮어쓰지 않고 `iteration_log.md`에 run id, 변경점, gate 결과, 다음 행동을 남긴다.

## Confirmed Decisions

| Item | Decision |
| --- | --- |
| Base model | `xlm-roberta-base` |
| Optional scale baseline | not used; `xlm-roberta-base` only |
| Reference model | `cis-lmu/glot500-base` only as paper reference, not required baseline |
| Main framing | target10 performance-improvement model with Glot500-inspired protocol |
| Existing first/second try role | ablation and failure analysis |
| Main target set | target10: `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp` |
| Coptic/Syriac | main experiment |
| Vocabulary operation | preserve all XLM-R ids, append new pieces only |
| Main tokenizer | SentencePiece unigram auxiliary tokenizer |
| Main init | multiple embedding initialization methods; random required baseline |
| Seeds | at least 3 seeds for model-dependent comparisons |
| Main training | full-model MLM continued pretraining |
| Main data mixture | high-resource replay/control + target10 low-resource mixture |
| Sampling | language-script multinomial, alpha `0.3` |
| Main evaluation | target10 downstream improvement required |
| Extension cases | target10 밖의 추가 언어만 해당 |

## Stage Order

| Stage | Folder | Depends On | Must Produce | Exit Gate |
| --- | --- | --- | --- | --- |
| 00 | `00_scope` | `scope_lock_20260612.md`, `idea.md`, `plan.md`, references | target10 and high-resource replay scope freeze | target10 main set and high-resource replay set are fixed |
| 01 | `01_data` | 00 | corpus, split, high-resource, and MLM mixture manifests | train/dev/test are leakage-safe and high-resource + low-resource mixture is recorded |
| 02 | `02_baseline` | 01 | XLM-R baseline tokenizer/model metrics | target10 baseline table is complete |
| 03 | `03_tokenizer` | 02 | Glot500-style tokenizer append and fallback ablation | XLM-R ids are preserved and main tokenizer is separated from fallback ablations |
| 04 | `04_init` | 03 | resized model, row-copy audits, init method grid | base rows have zero drift and multiple init methods are ready |
| 05 | `05_mlm` | 04 | MLM config, logs, checkpoints, deviations, seed summary | full fine-tuning uses high-resource + low-resource mixture and >=3 seeds |
| 06 | `06_eval` | 05 | target10 downstream and representation tables | XLM-R-B vs third_try target10 downstream summary is complete |
| 07 | `07_main_claim` | 06 | evidence table and allowed/blocked claims | tokenizer-only and downstream claims are separated |
| 08 | `08_ablation` | 00 plus prior evidence; final read after 07 | ablation matrix and first/second try mapping | every prior experiment is labeled ablation/failure analysis, not main |
| 09 | `09_extension_case` | 07 and frozen protocol | optional non-target10 transfer package | all deviations from main protocol are documented |

## Current Progress

2026-06-13 기준:

| Stage | Status | Evidence | Next |
| --- | --- | --- | --- |
| 00 | DONE | target10, Coptic/Syriac main role, XLM-R-base-only rule, high-resource language set fixed | keep as locked scope |
| 01 | DONE | Stage 01 manifests PASS; train row index 966152 rows | proceed to baseline and tokenizer work |
| 02 | IN_PROGRESS | XLM-R-base tokenization and deterministic MLM eval baselines created; exact PPPL/downstream pending | choose downstream baseline subset and/or run exact PPPL if compute allows |
| 03 | DONE | PASS_DEVIATION_AND_FALLBACK_ABLATION_DOCUMENTED; target-heavy high-resource 48k tokenizer created; ids preserved; avg target10 tokens/word -29.812358%; byte fallback vs char measured | use selected tokenizer for Stage 04/05 and fallback evidence for Stage 08 |
| 04 | DONE | PASS; random/mean/fvt/align/focus checkpoints created; fvt best zero-step dev loss 7.925527 | use fvt for first Stage 05 pilot and keep random/mean for ablation |
| 05 | DONE_FOR_DIAGNOSTIC / IN_PROGRESS_FOR_POSITIVE | smoke test PASS; fvt 3-seed 200-step pilot completed; replay-safe 1000-step 3-seed retry completed with mean final eval loss 3.903145 and mean perplexity 49.572677 | use replay-safe candidate for diagnostic report; return here only for stronger/full-budget positive retry |
| 06 | DONE_FOR_DIAGNOSTIC / IN_PROGRESS_FOR_POSITIVE | deterministic MLM proxy, frozen Bible proxy, Coptic POS pilot/replay-safe eval, high-resource control proxy, retained checkpoint check, replay-safe retry eval, and target10 availability audit complete; replay-safe Coptic POS is weak positive but high-resource control still fails 0/4 | positive claim blocked unless Stage 05 is rerun with stronger replay/full-budget evidence and broader target10 downstream coverage |
| 07 | DONE | PASS_NEGATIVE_MAIN_READY; positive claim blocked; diagnostic negative wording documented | use Stage 07 wording in report; do not overclaim tokenizer-only gains |
| 08 | DONE | PASS_ABLATION_PACKAGE_READY; first_try and second_try mapped as ablation/failure analysis | place prior experiments in ablation section/appendix only |

## Final Exit Goal

`third_try` is complete when one of the following is true.

| Exit State | Meaning | Allowed Claim |
| --- | --- | --- |
| `PASS_MAIN_CLAIM_READY` | target10 downstream improves with high-resource replay and no control collapse | positive main claim with limitations |
| `PASS_NEGATIVE_MAIN_READY` | Main run is complete but does not support a positive model claim | negative/diagnostic claim only |
| `PASS_ABLATION_PACKAGE_READY` | Existing work is fully recast as ablation/failure analysis | ablation claim only |
| `BLOCKED_BY_DATA_OR_COMPUTE` | Required target10 downstream evidence cannot be produced in current 1-GPU budget | no performance claim; report blocker and fallback design |

## Failure Return Protocol

When a stage fails:

1. Set `Gate status: FAIL` in that stage's `results.md`.
2. Fill the `Failure Return` section:
   - failed gate
   - observed evidence
   - likely cause
   - return-to stage
   - required fix before retry
3. Mark dependent later results invalid if they used the failed artifact.
4. Append a new entry to `iteration_log.md` before rerun.
5. Rerun from the earliest stage that can fix the cause.

## Common Return Paths

| Failure | Return To | Reason |
| --- | --- | --- |
| language role ambiguous | 00 | scope issue |
| target language lacks enough usable data | 00 or 01 | scope or data inventory issue |
| dev/test leakage found | 01 | split issue |
| no tail tokenizer bottleneck | 02 | baseline interpretation issue |
| special ids changed | 03 | tokenizer merge issue |
| appended pieces are not auditable | 03 | tokenizer construction issue |
| base embedding rows drift | 04 | model resize/init issue |
| MLM run lacks high-resource replay or is LoRA-only | 05 | main condition violated |
| checkpoint selection uses final test | 05 or 06 | selection leakage issue |
| target10 downstream coverage too sparse | 00 or 06 | evaluation feasibility issue |
| downstream claim unsupported | 07 | downgrade claim or return to failed stage |
| ablation wording overclaims main success | 08 | claim packaging issue |
| extension case differs from main protocol silently | 09 | deviation documentation issue |
