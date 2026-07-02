# Shortcut And Next Experiments Audit

작성일: 2026-06-11

## Verdict

현재 상태에서 top-tier positive claim은 아직 불가하다. Step26에서 top-tier-safe diagnostic/negative claim은 별도로 잠갔다.

다만 v1 shortcut은 숨겨진 채 남아 있지 않고 Step09, Step10에서 명시적으로 invalidated 처리되었다. v2 Steps 12-26는 final `ACT` 접근 없이 Mark/dev 기반으로 진행된 것으로 기록되어 있으며, 현재까지의 깨끗한 positive evidence는 split, tokenizer, embedding initialization, added-token failure diagnosis, smaller-vocab redesign probe까지로 제한된다. Step24 confirms that the selected 8k branch is still not competitive with original continued pretraining, Step25 shows longer 8k MLM alone does not rescue the gap, and Step26 locks the allowed final wording as a diagnostic negative claim.

## Checks Performed

| Check | Result | Evidence |
| --- | --- | --- |
| 모든 `score_table.tsv` 빈칸, `TBD`, `NA_NOT_CHECKED` 스캔 | PASS | bad cells `0` |
| 모든 `file_results.tsv` 산출물 path 존재 여부 | PASS | missing paths `0` |
| v2 no-final-access audit row 검사 | PASS | bad rows `0`; Steps 13-27 all `final_access=NO` |
| Steps 13-27 run scripts and synthesis outputs final path 정적 검색 | PASS | `v2_final`/final-test input read 발견 없음 |
| v1 translation shortcut audit | FAIL by design | Step10 invalidates Step07 and Branch001 |
| v2 model-dependent claim | FAIL | Step15/16 adapted model not competitive with original control |
| added-token repair / init probe | MIXED_NEGATIVE | Step18 added loss improves but all-token loss worsens; Step19 preserves base rows but worsens added-token loss; Step20 has no seed-stable passing variant; Step21 alt init has no passing method; Step23 smaller-vocab probe passes; Step24 8k control fails; Step25 longer 8k budget fails |

## Shortcut Findings

1. v1 Step07 translation row is shortcut-prone and cannot support a claim.
   - Target pair was selected on John/test.
   - Step10 marks it `FAIL_INVALIDATES_CLAIM`.

2. Branch001 LaBSE+CSLS success is exploratory only.
   - It used repeated test feedback before the final branch row.
   - It compared a LaBSE target row against an XLM-R high-resource reference.
   - Step09 method-matched audit fails all translation rows.

3. v2 final set protection is currently acceptable.
   - Step12 reserves `ACT` as clean final and excludes burned `JOH`.
   - Steps 13-27 use train, Mark/dev, or docs-only inputs.
   - `v2_no_final_access_audit.tsv` rows all pass.

4. Current `PASS` labels should be read carefully.
   - Step13 and Step14 `PASS` mean clean tokenizer/init artifacts.
   - Step15 artifact gate passes, but claim gate fails.
   - Step16 artifact gate passes, but normalized MLM claim gate fails.
   - Step18 artifact/partial added-token improvement passes, but repair gate fails.
   - Step19 trainable audit passes, but repair gate fails.
   - Step20 lower-rate/bias-only grid is closer, but repair gate fails.
   - Step21 alternative initialization probe fails.
   - Step23 smaller-vocab redesign probe passes, but it is not an original-control competitiveness pass.
   - Step24 selected 8k normalized control fails.
   - Step25 longer 8k budget probe fails.

## Result Validity Summary

| Claim | Current Status | Why |
| --- | --- | --- |
| XLM-R tokenizer bottleneck exists | Supported | Step02/Step13 show high fragmentation and v2 tokenizer improves Mark/dev fragmentation. |
| Vocab extension reduces tokenization fragmentation | Supported for Mark/dev preprocessing | Step13 selects 32k on dev only with no final access. |
| Embedding initialization matters | Supported for zero-step MLM readiness | Step14 tests random, mean, fvt, align, focus and selects `fvt` on Mark/dev. |
| Extended adapted model is competitive | Unsupported | Step15 adapted/original ratio `1.964580`, required `<=1.100000`. |
| Failure is only cross-tokenizer metric artifact | Unsupported | Step16 word/char normalized ratio `1.438660`, required `<=1.100000`. |
| Added-token weighting repairs the model | Unsupported | Step18 added loss improves `3/3`, but all-token nonworse is `0/3`. |
| New-row-only repair fixes added-token prediction | Unsupported | Step19 trainable audit passes `3/3`, but added-token loss improves `0/3`. |
| Staged/lower-rate repair fixes added-token prediction | Unsupported | Step20 passing variants `0/3`; best mean added delta `-0.004565`, but only `1/3` seeds improve added loss. |
| Alternative initialization fixes model-dependent failure | Unsupported | Step21 passing methods `0/2`; best `align` raw mean final loss is worse than `fvt`. |
| Smaller vocab size repairs the 32k failure mode | Supported as redesign probe | Step23 passing variants `2/2`; best 8k raw mean final loss `4.541285` vs 32k `4.946829`; added/base/all gates pass `3/3`. |
| Smaller vocab size already supports positive adapted-model claim | Unsupported pending controls | Step23 best 8k raw ratio vs original-control mean is `1.803523`; Step15/16 controls must be rerun. |
| Selected 8k branch supports positive adapted-model claim | Unsupported | Step24 word/char normalized ratio `1.472019`, required `<=1.100000`. |
| Longer 8k MLM budget supports positive adapted-model claim | Unsupported | Step25 word/char normalized ratio `1.587381`, required `<=1.100000`; original control improves faster. |
| Diagnostic negative claim is ready | Supported | Step26 `PASS_DIAGNOSTIC_CLAIM_READY`; evidence rows `14`; blocked positive claim rows `10`. |
| Translation reaches 80% high-resource reference | Unsupported | Step09 selected adapted XLM-R ratio `0.638034`; LaBSE upper-bound ratio `0.567179`. |
| Top-tier final claim | Not ready | v2 downstream and v2 final translation are not started. |

## Additional Experiments Required

### P0 Before Any Positive Model Claim

1. Tokenizer/objective/data redesign beyond longer 8k MLM.
   - Step19 already showed strict new-row-only repair from Step15 checkpoints preserves base rows but worsens added-token loss.
   - Step20 already showed lower-rate/bias-only variants are not seed-stable.
   - Step21 already showed `mean` and `align` do not beat `fvt` under the Step15 budget.
   - Step23 showed smaller vocab helps, but Step24 showed selected 8k still fails normalized original-control competitiveness.
   - Step25 showed additional 8k MLM budget worsens the normalized gap because the original control improves faster.
   - Keep train and Mark/dev only; no `ACT` access.
   - Required gate: normalized adapted/original ratio `<=1.100000`, with added loss improving in `3/3` and base/all loss nonworse in `3/3`.

2. Rerun MLM control after any new repair.
   - Compare repaired adapted model against original XLM-R continued-pretraining control at matched token budget and at least 3 seeds.
   - Repeat Step16 normalized MLM audit.
   - Required gate: adapted/original normalized ratio `<=1.100000` or explicitly downgrade the model-dependent claim.

3. V2 downstream hard-negative evaluation.
   - Use dev-only selection and bootstrap confidence intervals.
   - Evaluate `ACT` final exactly once after model/task freeze.
   - Required gate: statistically supported gains across languages/seeds.

4. V2 method-matched translation evaluation.
   - Use adapted XLM-R as main model.
   - Use the same method for high-resource reference and target comparison.
   - Select pair/scoring on Mark/dev only, then evaluate `ACT` final once.
   - Required gate: target/high-resource ratio `>=0.800000`.

### P1 For Stronger Paper Claims

1. Generation baseline with method-matched scoring.
   - Retrieval can stay as proxy, but generation claims require generation outputs.

2. External-domain validation beyond Bible.
   - Needed if the final wording claims broad low-resource generalization rather than Bible-domain evidence.

3. Initialization ablation after a successful repair.
   - Step14 tests all init methods at zero-step, but only selected `fvt` has been carried through MLM.
   - For a stronger initialization claim, rerun at least `mean` vs `fvt` under the successful repair objective.

## Final Recommendation

Do not proceed to positive downstream or translation final readout yet. The selected 8k branch and longer 8k budget both fail original-control competitiveness. Step26 has already framed the paper as a negative/diagnostic study: tokenizer extension improves segmentation, and smaller vocab reduces the added-token burden, but model-level gains remain unproven. Return to objective/data redesign only if a future positive model-dependent claim is required.
