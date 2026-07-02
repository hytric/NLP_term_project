# Third Try Final Pre-Start Report

작성일: 2026-06-13

## Post-Pilot Addendum

이 문서는 Stage 05 pilot 시작 전 go/no-go 보고서로 보존한다. 이후 진행으로 다음 항목이 갱신되었다.

- Stage 05 fvt 3-seed 200-step pilot은 완료되었다.
- Stage 06 Coptic POS는 약한 positive pilot이지만, high-resource control proxy는 potential collapse로 실패했다.
- Byte fallback vs character coverage 비교는 Stage 03 ablation으로 완료되었다.
- Stage 07은 `PASS_NEGATIVE_MAIN_READY`, Stage 08은 `PASS_ABLATION_PACKAGE_READY`로 정리되었다.

따라서 최신 최종 판단은 이 pre-start 문서가 아니라 `07_main_claim/results.md`와 `08_ablation/results.md`를 따른다.

## 결론

Gate decision: `CONDITIONAL_GO_TO_STAGE05_PILOT`

`third_try`는 Stage 05 continued-MLM pilot을 시작할 준비가 거의 끝났다. 다만 final claim을 시작할 준비가 된 것은 아니다. 현재 상태에서 허용되는 것은 **GPU 3번에서 fvt 초기화 checkpoint로 Stage 05 pilot을 시작하는 것**이고, final positive claim은 Stage 05/06에서 3개 이상 seed와 downstream evidence가 나온 뒤에만 가능하다.

## 핵심 피드백 반영 상태

| Feedback | Current handling | Status |
| --- | --- | --- |
| Glot500 실험을 따라가라 | XLM-R-base, id-preserving append, SentencePiece unigram, high-resource replay, full MLM, alpha-style sampling, downstream evaluation 원칙을 채택 | PASS_WITH_DEVIATION |
| 현재까지의 실험은 ablation으로 가라 | `first_try`/`second_try`, target-only, LoRA, repair, seed-1 pilot, fallback 비교를 ablation/failure analysis로 분리 | PASS |
| high-resource와 low-resource를 함께 써라 | GlotCC-V1 web replay 4개 언어와 target10, Bible control을 Stage 01 mixture에 포함 | PASS |
| Coptic/Syriac는 중요 evidence다 | `cop`, `syr`를 target10 main experiment에 포함 | PASS |
| byte fallback vs char 비교도 넣어라 | Stage 03 `fallback_ablation.tsv`와 `fallback_ablation_summary.tsv`로 ablation 축에 추가 | PASS_COMPLETED_ABLATION |

Important clarification:

현재 locked scope는 "Glot500 literal reproduction"이 아니라 "Glot500에서 배운 핵심 protocol을 target10 성능 개선 모델에 적용"하는 것이다. 따라서 최종 보고서에서는 "Glot500을 그대로 재현했다"라고 쓰면 안 된다. 대신 "Glot500-style controls under a target10 low-resource adaptation setting"이라고 써야 한다.

## 현재 Stage 상태

| Stage | Status | Decision |
| --- | --- | --- |
| 00 Scope | PASS | target10, high-resource replay/control, XLM-R-base-only rule locked |
| 01 Data | PASS | leakage-safe mixture manifest complete |
| 02 Baseline | IN_PROGRESS | tokenization + deterministic MLM baseline done; exact PPPL/downstream pending |
| 03 Tokenizer | PASS_DEVIATION_DOCUMENTED | target-heavy 48k tokenizer selected; fallback ablation separated |
| 04 Init | PASS | random/mean/fvt/align/focus checkpoints created; fvt selected for first pilot |
| 05 MLM | READY_FOR_PILOT | training config and command still need to be written before launch |
| 06 Eval | BLOCKED_ON_T05 | final evaluation cannot start yet |
| 07 Claim | POST_PILOT_DONE | latest result: `PASS_NEGATIVE_MAIN_READY`; at pre-start time this was blocked |

## Ready Artifacts

### Data

| Component | Rows |
| --- | ---: |
| target10 train after exact eval duplicate exclusion | 52016 |
| GlotCC-V1 web replay | 800000 |
| Bible high-resource domain control | 114136 |
| total MLM train row index | 966152 |
| target10 dev | 6521 |
| target10 final test | 9804 |

Large manifests:

- `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_train_rows.tsv`
- `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_dev_rows.tsv`
- `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/final_eval_rows.tsv`

### Tokenizer

Selected provisional tokenizer:

`/home/axt/mnt2/jongha/third_try/tokenizers/stage03_targetheavy_20260613_r3/tokenizers/xlmr_third_try_mixture_added_48000`

| Metric | Value |
| --- | ---: |
| base vocab size | 250002 |
| appended tokens | 30849 |
| extended vocab size | 280851 |
| average target10 tokens/word delta | -29.812358% |
| worst language tokens/word delta | +1.504758% |
| average single-character ratio delta | +37.402719% |
| changed existing token ids | 0 |
| changed special token ids | 0 |

Interpretation:

Tokens/word improved strongly, especially Syriac. But single-character ratio worsened for some scripts, especially Coptic, Cherokee, and Ojibwa. Therefore tokenizer success must be phrased carefully: "fertility improved" is supported; "all tokenization pathology is fixed" is not supported yet.

### Initialization

Selected first pilot checkpoint:

`/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt`

| Init | Zero-step dev loss | Status |
| --- | ---: | --- |
| random | 17.998567 | baseline |
| mean | 10.910376 | candidate |
| fvt | 7.925527 | selected first pilot |
| align | 8.700895 | candidate |
| focus | 16.760191 | candidate |

Interpretation:

`fvt` is selected only as the first Stage 05 pilot start point because it has the best zero-step Mark/dev MLM loss. It is not yet the final method.

## Blocking Or Caution Items

| Item | Severity | Why it matters | Required handling |
| --- | --- | --- | --- |
| Stage 02 is still `IN_PROGRESS` | Medium | exact PPPL/downstream baseline is not closed | Stage 05 pilot may start, but Stage 06/final claim cannot close until baseline is completed or explicitly deferred |
| 48k tokenizer deviates from original 8k/16k/32k grid | Medium | reviewer may ask why this size was introduced | keep `PASS_DEVIATION_DOCUMENTED`; report compute-bounded target-heavy selection |
| average single-character ratio worsened | High | tokenizer improvement is mixed, not uniformly positive | track per-language downstream; byte-vs-char fallback ablation completed post-pilot |
| fvt chosen on 1000 Mark/dev rows | Medium | initialization selection may overfit dev subset | final claim requires training + 3 seeds + downstream, not zero-step loss |
| byte fallback vs char fallback completed post-pilot | Low for Stage 05, Medium for final ablation | user requested it; now measured in Stage 03 global fallback ablation | use as ablation-only evidence, not main tokenizer replacement |
| 1 GPU / several days budget | High | full 3-seed grid may be expensive | pilot first; then promote only viable method to 3 seeds |
| Official downstream sparse for target10 | High | many target10 languages have proxy-only downstream | mark proxy tasks explicitly; do not overclaim official task coverage |

## Start Conditions For Stage 05

Before launching the first GPU run, create these files:

- `05_mlm/training_config.json`
- `05_mlm/training_command.md`
- `05_mlm/deviation_from_protocol.tsv`

The command must include:

```bash
CUDA_VISIBLE_DEVICES=3
```

Minimum first pilot:

| Field | Value |
| --- | --- |
| checkpoint | `/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt` |
| tokenizer | `/home/axt/mnt2/jongha/third_try/tokenizers/stage03_targetheavy_20260613_r3/tokenizers/xlmr_third_try_mixture_added_48000` |
| train text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/mlm_train_full_mixture.txt` |
| dev text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/target10_dev.txt` |
| sequence length | 512 |
| objective | MLM |
| training mode | full model |
| init method | fvt |
| seed policy | pilot first, final candidate >=3 seeds |

## No-Go Conditions

Do not make a positive final claim if any of these remain true:

1. Stage 05 has fewer than 3 seeds for the selected final candidate.
2. Stage 06 lacks target10 downstream or accepted proxy downstream evidence.
3. High-resource control collapses and is not documented.
4. Final test is used for checkpoint selection.
5. Stage 03/04 artifacts are replaced without rerunning row/id drift audits.
6. Existing `first_try`/`second_try` results are presented as main evidence instead of ablation.

## Final Recommendation

Proceed with Stage 05 pilot, not with final claim.

Recommended next action:

1. Write `05_mlm/training_config.json` and `05_mlm/training_command.md`.
2. Launch one fvt pilot run on GPU 3.
3. If pilot loss behaves normally, run the selected final candidate with at least 3 seeds.
4. Complete Stage 02 downstream/exact-PPPL baseline before Stage 06 final evaluation.
5. Keep byte-vs-char fallback as Stage 08 ablation unless tokenizer failure forces an earlier branch.

## Final Pre-Start Statement

`third_try` is ready to start controlled continued pretraining. It is not yet ready to claim success. The experiment is scientifically cleaner than `first_try` and `second_try` because high-resource replay, target10 leakage-safe split, id-preserving tokenizer append, multi-init candidates, and seed-stable downstream requirements are now explicitly separated from ablation/failure-analysis evidence.
