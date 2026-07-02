# Second Try Step Index

작성일: 2026-06-10

이 파일은 second_try의 실행 단계를 잠금식으로 정의한다. 각 step은 자기 폴더 안의 `plan.md`, `results.md`, `score_table.tsv`를 기준으로 진행한다.

## Global Rule

- 모든 작업 문서는 `/home/axt/jongha/Glot500-py39-eval/docs/exp/second_try` 안에 둔다.
- first_try는 구현/폴더 구조 감각만 참고한다. first_try의 수치, 결론, 성공 판정은 second_try evidence로 쓰지 않는다.
- 각 step은 이전 step의 `Gate status`가 `PASS`일 때만 시작한다. 단, `06_downstream_tasks`는 downstream negative result를 문서화한 `PASS_NEGATIVE_RESULT`도 `07_translation_benchmark` 진입을 허용한다.
- `08_final_analysis`는 `07_translation_benchmark`가 `FAIL`이어도 시작할 수 있다. 조건은 Step 07의 `Failure Return`, branch folder, branch `score_table.tsv`, branch `file_results.tsv`가 모두 완성되어 있어야 한다. 이 경우 Step 08은 `PASS_NEGATIVE_RESULT`로 닫고, 번역 성공 주장을 명시적으로 downgrade한다.
- `09_top_tier_validation`이 존재하면 top-tier translation claim은 Step 09의 method-matched 결과를 따른다. Step 09가 claim gate를 `FAIL`로 닫으면 Step 07/08의 branch pass 표현은 exploratory result로만 취급한다.
- `10_leakage_selection_audit`이 존재하면 translation claim의 selection validity는 Step 10을 따른다. Step 10이 claim gate를 `FAIL`로 닫으면 Step 07/Branch 001의 raw score는 top-tier 성공 근거가 아니라 무효화된 탐색 결과다.
- `11_fresh_holdout_feasibility`가 존재하면 F02/F03 translation rerun 가능 여부는 Step 11을 따른다. Step 11이 claim gate를 `FAIL`로 닫으면 현재 artifact만으로는 fresh held-out top-tier translation 실험을 진행하지 않는다.
- `12_v2_split_protocol`이 존재하면 이후 top-tier final claim은 v2 split 기준으로만 인정한다. v1 Step05/06/07/09 결과는 탐색 증거로만 남기고 v2 final claim에는 쓰지 않는다.
- `13_v2_tokenizer`가 존재하면 이후 v2 model-dependent stage는 Step13의 selected tokenizer를 기준으로 진행한다. Step13은 `ACT` final을 읽지 않은 train/dev-only tokenizer evidence다.
- `14_v2_embedding_init`이 존재하면 이후 v2 MLM/downstream/translation stage는 Step14의 selected initialization을 기준으로 진행한다. Step14은 `ACT` final을 읽지 않은 full Mark/dev zero-step evidence다.
- `15_v2_mlm_control`이 존재하면 이후 v2 model-dependent claim은 Step15의 control result를 따른다. Step15가 claim gate `FAIL`이면 downstream/translation은 top-tier positive claim으로 진행할 수 없고, Step15 재시도 또는 negative/downgraded claim으로 돌아간다.
- `16_v2_mlm_metric_fairness`가 존재하면 Step15의 cross-tokenizer raw loss 해석은 Step16의 normalized metric audit을 함께 따른다. Step16이 claim gate `FAIL`이면 raw-token-loss 착시만으로 Step15 실패를 무효화할 수 없다.
- `17_v2_added_token_failure_analysis`가 존재하면 Step15/16 failure repair target은 Step17의 category decomposition을 따른다. Step17이 added-token hotspot을 확인하면 다음 수리는 added-token learning/init/objective에 집중한다.
- `18_v2_added_token_repair`가 존재하면 added-token-weighted objective의 효과는 Step18 repair gate를 따른다. Step18이 repair gate `FAIL`이면 단순 added-token weighting은 충분하지 않으며 base-token 보존형 repair로 넘어간다.
- `19_v2_new_row_only_repair`가 존재하면 strict new-row-only repair의 효과는 Step19 repair gate를 따른다. Step19가 repair gate `FAIL`이면 base row 보존만으로는 충분하지 않으며 staged/lower-rate/objective-level repair로 돌아간다.
- `20_v2_staged_added_token_repair`가 존재하면 lower-rate/bias-only repair grid의 효과는 Step20 repair gate를 따른다. Step20이 repair gate `FAIL`이면 평균 개선만으로는 부족하고 seed-stable model-dependent claim은 계속 막힌다.
- `21_v2_alt_init_mlm_probe`가 존재하면 Step14 alternative initialization의 효과는 Step21 probe gate를 따른다. Step21이 probe gate `FAIL`이면 `fvt` 선택 자체만 실패 원인이라고 볼 수 없다.
- `22_full_experiment_audit`이 존재하면 shortcut 여부와 추가 실험 필요성은 Step22 audit gate를 따른다. Step22가 positive claim을 blocked로 표시하면 downstream/translation final readout은 positive claim으로 진행하지 않는다.
- `23_v2_vocab_size_objective_probe`가 존재하면 smaller-vocab redesign 효과는 Step23 probe gate를 따른다. Step23이 `PASS`여도 original-control competitive claim은 아직 아니며, 8k branch로 Step15/16 control을 다시 통과해야 한다.
- `24_v2_8k_mlm_control`이 존재하면 selected 8k branch의 model-dependent claim은 Step24 normalized audit을 따른다. Step24가 claim gate `FAIL`이면 downstream/translation final readout은 positive claim으로 진행하지 않는다.
- `25_v2_8k_continued_budget_probe`가 존재하면 longer-budget rescue 가능성은 Step25 probe gate를 따른다. Step25가 probe gate `FAIL`이면 8k longer MLM alone으로는 positive claim을 진행하지 않는다.
- `26_top_tier_diagnostic_claim_synthesis`가 존재하면 현재 최종 claim은 Step26의 diagnostic/negative claim contract를 따른다. Step26이 `PASS_DIAGNOSTIC_CLAIM_READY`이면 positive downstream/translation final readout은 계속 막히지만, unsupported positive wording을 제거한 top-tier diagnostic synthesis는 진행할 수 있다.
- `27_final_manuscript_synthesis`가 존재하면 Step26 claim contract는 manuscript-ready package로 변환된 것이다. Step27이 `PASS_MANUSCRIPT_READY`이면 diagnostic negative paper package는 준비됐고, positive performance paper는 여전히 막힌다.
- 각 step은 `results.md`, `score_table.tsv`, `file_results.tsv`를 반드시 출력한다.
- `score_table.tsv`에 `TBD`, 빈칸, `NA_NOT_CHECKED`가 남아 있으면 해당 step은 완료가 아니다.
- `file_results.tsv`에 각 생성 파일의 path, count/size, status가 없으면 해당 step은 완료가 아니다.
- `results.md`의 `Gate status`가 `PASS`가 아니면 다음 step으로 넘어갈 수 없다. 예외는 위에 명시한 `PASS_NEGATIVE_RESULT` 및 Step 08 negative synthesis뿐이다.
- 실패하면 실패 step의 `results.md`에 원인, 되돌아갈 step, 재실행 조건을 적고, 필요한 이전 step으로 돌아간다.

## Confirmed Decisions

| Item | Decision |
| --- | --- |
| Base model | `xlm-roberta-base` |
| Architecture | encoder-only downstream plus separate translation benchmark |
| Translation | separate Step 07 benchmark, target >= 80% high-resource reference |
| Target languages | confirmed target10 최대한 유지 |
| Main corpus | Bible corpus |
| Split default | train = all except Mark/John, dev = Mark, test = John |
| Tokenizer | SentencePiece unigram |
| Vocab sizes | 8k, 16k, 32k |
| Merge style | preserve XLM-R ids, append new pieces |
| Byte fallback | off by default; record if any fallback mechanism is used |
| Init methods | random, mean, fvt, align, focus; Ofa/Wechsel optional only |
| MLM data | target10 Bible train/dev only, leakage guarded |
| Downstream tasks | book/genre classification, verse retrieval/ranking, parallel verse matching |
| Diagnostic task | language identification only as sanity check |
| Full downstream seeds | original XLM-R and selected best checkpoint, 3 seeds |
| Checkpoints | gate-passing candidates only |
| Primary GPU | GPU 4 requested; current environment falls back to GPU 3 because GPU 4 is not visible |
| Large artifact root | `/home/axt/mnt2/jongha/second_try` |
| Translation objective | target translation score >= 80% of high-resource reference score |

## Step Order

| Step | Folder | Depends On | Must Produce | Exit Gate |
| --- | --- | --- | --- | --- |
| 00 | `00_scope_and_references` | existing references | reference/scope audit | all decisions and source docs mapped |
| 01 | `01_data_and_splits` | 00 | split files and data stats | leakage-safe train/dev/test ready |
| 02 | `02_tokenization_audit` | 01 | XLM-R baseline tokenization metrics | bottleneck quantified |
| 03 | `03_vocab_extension` | 02 | 8k/16k/32k extended tokenizer metrics | valid tokenizer candidates selected |
| 04 | `04_embedding_init` | 03 | initialized checkpoints and diagnostics | all required init methods load |
| 05 | `05_mlm_adaptation` | 04 | MLM results and checkpoint selection | tokenization + MLM gate pass |
| 06 | `06_downstream_tasks` | 05 | downstream task results | best adapted model tested vs baseline |
| 07 | `07_translation_benchmark` | 06 | translation benchmark and high-resource reference comparison | target score >= 80% high-resource reference or branch/failure path documented |
| 08 | `08_final_analysis` | 07 or documented 07 failure branch | final evidence map and tables | final claim supported or negative result documented |
| 09 | `09_top_tier_validation` | 08 or requested shortcut audit | method-matched translation audit and claim contract | artifact gate PASS; claim gate may be FAIL if documented |
| 10 | `10_leakage_selection_audit` | 09 or requested shortcut audit | leakage audit, selection trace, invalidated runs | artifact gate PASS; claim gate may be FAIL if documented |
| 11 | `11_fresh_holdout_feasibility` | 10 or requested top-tier rerun | data availability and fresh held-out protocol | artifact gate PASS; claim gate may be FAIL if documented |
| 12 | `12_v2_split_protocol` | 11 | v2 split manifest, ACT clean final heldout, rerun protocol | v2 final split sufficient and old John excluded |
| 13 | `13_v2_tokenizer` | 12 | v2 tokenizer candidates, selected tokenizer, no-final-access audit | tokenizer ids preserved and dev fragmentation improves |
| 14 | `14_v2_embedding_init` | 13 | v2 init scores, zero-step MLM, selected init, checkpoints | all required init methods load and selected init is dev-only |
| 15 | `15_v2_mlm_control` | 14 | MLM learning curves, seed summary, checkpoint selection, original control | adapted improves from zero-step and is competitive with original continued-pretraining control |
| 16 | `16_v2_mlm_metric_fairness` | 15 | normalized MLM scores and no-final-access audit | adapted is competitive on estimated NLL per word and per char |
| 17 | `17_v2_added_token_failure_analysis` | 16 | token category loss, language breakdown, added-token samples | added-token failure source diagnosed without final data |
| 18 | `18_v2_added_token_repair` | 17 | repair summary, category loss, checkpoint selection | added loss improves without all-token degradation |
| 19 | `19_v2_new_row_only_repair` | 18 | new-row repair summary, trainable audit, checkpoint selection | appended rows improve without base/all degradation |
| 20 | `20_v2_staged_added_token_repair` | 19 | staged repair summary, variant summary, trainable audit, checkpoint selection | at least one repair variant is seed-stable without base/all degradation |
| 21 | `21_v2_alt_init_mlm_probe` | 20 | alternative-init MLM summary, variant summary, category comparison | at least one alternative init beats fvt on raw mean and category gates |
| 22 | `22_full_experiment_audit` | 21 | shortcut matrix, next-experiments matrix, audit score table | no active shortcut remains and unsupported positive claims are blocked |
| 23 | `23_v2_vocab_size_objective_probe` | 22 | smaller-vocab init, MLM, category loss, variant summary | at least one smaller vocab beats 32k and improves added/base/all losses in every seed |
| 24 | `24_v2_8k_mlm_control` | 23 | 8k raw control, normalized MLM scores, checkpoint selection | 8k branch competitive with original-control normalized MLM metrics |
| 25 | `25_v2_8k_continued_budget_probe` | 24 | continued-budget summary, normalized MLM scores, checkpoint selection | longer 8k budget closes original-control normalized gap |
| 26 | `26_top_tier_diagnostic_claim_synthesis` | 25 | final claim contract, evidence table, unsupported claim table, future positive experiment path | diagnostic top-tier claim is ready and unsupported positive claims are blocked |
| 27 | `27_final_manuscript_synthesis` | 26 | manuscript outline, paper claims, table manifest, reviewer risk audit, reproducibility checklist | diagnostic manuscript package is ready and positive performance package is blocked |

## Failure Return Protocol

When a step fails:

1. Set `Gate status: FAIL` in that step's `results.md`.
2. Fill the `Failure Return` section:
    - failed gate
    - observed evidence
    - likely cause
    - return-to step
    - required fix before retry
3. Mark any later step results as invalid if they depend on the failed artifact.
4. Return to the earliest step that can fix the cause.
5. On rerun, append a new run id instead of overwriting previous evidence.

Common return paths:

| Failure | Return To | Reason |
| --- | --- | --- |
| target data leakage | 01 | split/source issue |
| no tokenization bottleneck | 02 | baseline interpretation issue |
| extended tokenizer cannot round-trip | 03 | tokenizer merge issue |
| special ids changed | 03 | merge must be fixed |
| embedding/LM head mismatch | 04 | init/resize issue |
| MLM loss worsens for all candidates | 03 or 04 | vocab size or init issue |
| downstream task too easy | 06 | negative sampling/label issue |
| only language ID improves | 06 | final task evidence insufficient |
| translation below 80% reference | 07 | tune translation branch or return to model/data steps |
| final claim unsupported | 08 | report as negative or return to failed stage |
| method-matched translation claim fails | 09 | return to Step 05/06/07 with stronger adaptation, dev-only selection, and fresh held-out test |
| selection protocol fails | 10 | return to Step 07 with frozen dev-only selection and fresh held-out final test |
| no fresh held-out set remains | 11 | return to Step 01 to reserve a new final test book or import a new external corpus |
| v2 split created | 12 | rerun tokenizer, MLM, downstream, and translation under v2 before making final claims |
| v2 tokenizer created | 13 | proceed to v2 embedding initialization using selected tokenizer |
| v2 init created | 14 | proceed to v2 MLM adaptation/control using selected init |
| v2 MLM control claim fails | 15 | rerun Step 15 with revised initialization/objective, revisit Step 14 initialization, or downgrade the final model-dependent claim |
| v2 normalized MLM metric claim fails | 16 | do not treat Step15 failure as raw-token metric artifact; revise objective/init or downgrade the model-dependent claim |
| v2 added-token hotspot diagnosed | 17 | repair added-token learning/init/objective before rerunning Step 15 |
| added-token weighted repair worsens all-token loss | 18 | try frozen-base/new-row-only or staged repair before rerunning Step 15 |
| new-row-only repair worsens added-token loss | 19 | try lower learning rate, staged repair, changed objective, or revisit initialization before rerunning Step 15 |
| staged repair grid has no seed-stable passing variant | 20 | revisit initialization/objective or downgrade model-dependent claim before downstream/translation final readout |
| alternative initialization probe fails | 21 | revisit tokenizer/objective or downgrade model-dependent claim before downstream/translation final readout |
| full shortcut audit blocks positive claim | 22 | run tokenizer/objective redesign before positive downstream/translation readout, or downgrade to negative/diagnostic synthesis |
| smaller-vocab probe passes but remains worse than original control | 23 | rerun Step15/16 controls with the 8k branch before downstream/translation final readout |
| 8k normalized MLM control fails | 24 | redesign objective/data beyond smaller-vocab branch or downgrade model-dependent claim before downstream/translation final readout |
| 8k continued-budget probe fails | 25 | objective/data redesign beyond longer 8k MLM, or downgrade to negative/diagnostic synthesis |
| diagnostic claim synthesis complete | 26 | proceed with negative/diagnostic paper framing; return to objective/data redesign only if a future positive model claim is required |
| manuscript synthesis complete | 27 | proceed to write the diagnostic negative manuscript; return to objective/data redesign only for a future positive performance manuscript |
