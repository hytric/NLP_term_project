# v5.2 Plan

## Phase 0. Decision Freeze

- [x] `92 XLM-R-seen + 7 XLM-R-unseen target`으로 확정한다.
- [x] target7을 downstream overlap 최대화 기준으로 확정한다.
- [x] low-resource 표현을 `XLM-R-unseen tail + downstream 가능한 최소 corpus band`로 고정한다.
- [x] Yamaguchi vocabulary method는 main에서 빼고 추가 실험으로 둔다.
- [x] main axis를 Glot500식 vocab injection 고정 + embedding initialization ablation으로 둔다.

## Phase 1. Prep

- [x] target7 selection strategy를 preprocessing script에 추가한다.
- [x] v5.2 prepare/merge/tokenizer/initializer/training wrapper를 추가한다.
- [x] `random/mean/fvt/align` initializer 전체를 default build 대상으로 둔다.
- [x] target7 raw data validation을 실행한다.
- [x] `92/92` seen + `7/7` target symlink 준비를 확인한다.

## Phase 2. Corpus And Tokenizer

- [ ] `alpha=0.3` sampling으로 `Glot500_v52_glot5007_xlmr100` corpus를 merge한다.
- [ ] 같은 corpus로 SentencePiece unigram tokenizer를 학습한다.
- [ ] XLM-R SPM 뒤에 new pieces를 append한 `Glot500_extended_spm`을 audit한다.

## Phase 3. Initialization

- [ ] `random` initialized checkpoint를 만든다.
- [ ] `mean` initialized checkpoint를 만든다.
- [ ] `fvt` initialized checkpoint를 만든다.
- [ ] `align` initialized checkpoint를 만든다.
- [ ] `init_report.json`과 row report에서 `<mask>` remap, copied rows, fallback rows를 확인한다.

## Phase 4. MLM

- [ ] GPU 2장으로 init method 2개씩 병렬 학습한다.
- [ ] 8시간 run에서 checkpoint 5-8개가 생기도록 `SAVE_STEPS`를 조정한다.
- [ ] 1차 wave: `random` vs `fvt`.
- [ ] 2차 wave: `mean` vs `align`.

## Phase 5. Evaluation And Logging

- [ ] 다른 GPU에서 중간 checkpoint마다 PPPL/retrieval/NER/POS 가능분을 평가한다.
- [ ] Bible/Roundtrip/Taxi1500 materialization 상태를 별도 logging한다.
- [ ] `incremental_table_tracker.tsv`를 checkpoint별로 갱신한다.
- [ ] paired result가 들어온 경우에만 claim ledger로 승격한다.

## Expected Presentation Claim

```text
We reproduce the Glot500-style vocabulary injection pipeline on 92 seen
languages plus 7 XLM-R-unseen downstream-capable tail languages, and isolate
the effect of new-token embedding initialization under the same tokenizer,
corpus, sampling, and MLM schedule.
```
