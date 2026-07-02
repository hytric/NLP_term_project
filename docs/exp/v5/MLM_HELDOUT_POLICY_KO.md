# v5 MLM / PPPL Held-Out Policy

작성일: 2026-06-28

## 결론

v5는 버리지 않는다. v5는 `92` XLM-R-seen language-script와 `10` Glot500-internal
target language-script를 사용한 controlled Glot500-style replay로 유지한다.
다만 현재 v5 PPPL은 local raw Arrow dataset의 `train` split에서 추출한
train-source intrinsic diagnostic이므로, Glot500 논문의 held-out test PPPL과
동일한 final test metric으로 승격하지 않는다.

strict Glot500-style PPPL 재현은 v5.1 correction line으로 넘긴다. v5.1에서는 raw
text를 먼저 language별 `train/dev/test`로 고정 분리하고, merge/tokenizer/MLM에는
`train`만 사용하며, PPPL은 `dev` 또는 `test`에서만 측정한다.

## Glot500 원칙

Glot500 논문은 language-script별 corpus를 `train/dev/test`로 나누고, dev `1000`
문장과 test `1000` 문장을 hold out한 뒤 pretraining에는 train만 사용한다. Bible
translation이 있으면 parallel verse도 dev/test에 따로 넣는다. PPPL은 held-out
test set에서 token을 하나씩 mask해서 계산한다.

따라서 final report에서 다음 두 항목을 반드시 분리한다.

| 항목 | v5 처리 | report claim |
| --- | --- | --- |
| train-source PPPL / MLM proxy | 현재 v5에서 이미 측정된 row를 유지 | intrinsic diagnostic |
| held-out PPPL | v5.1에서 split 생성 후 측정 | strict Glot500-style test metric |

## v5에서 살릴 것

- full 102-language corpus construction
- Glot500-style SentencePiece extension
- tokenizer fertility/audit 결과
- random/mean/FVT embedding initialization
- source row copy, `<mask>` remap, byte-row handling, LM-head tying audit
- zero-step FVT advantage
- matched `v5_random`/`v5_fvt` 10K checkpoints
- Glot500 downstream metric families over available benchmark languages

## v5에서 claim을 낮출 것

현재 `PPPL_SPLIT=train`으로 생성된 rows는 아래처럼 표기한다.

```text
train-source MLM/PPPL diagnostic
```

사용 금지 표현:

```text
held-out test PPPL
final Glot500 PPPL reproduction
test-set pseudoperplexity
```

사용 가능 표현:

```text
The current v5 PPPL row is an intrinsic train-source diagnostic used to compare
matched initialization conditions under the same sampled raw-text protocol.
It is not promoted as the Glot500 held-out test PPPL.
```

## v5.1로 넘길 것

v5.1은 strict held-out correction line이다.

필수 조건:

1. 각 language-script raw dataset에서 deterministic split을 만든다.
2. `dev=1000`, `test=1000` 문장을 먼저 hold out한다.
3. 남은 `train`만 merge/tokenizer/continued MLM에 사용한다.
4. tokenizer training에도 dev/test 문장이 들어가지 않게 한다.
5. PPPL은 `dev` 또는 `test` split에서만 실행한다.
6. downstream benchmark는 각 task의 official train/dev/test split을 따른다.

권장 명명:

```text
v5 = controlled replay + diagnostic PPPL + available downstream replay
v5.1 = strict held-out PPPL correction
```

## 실행 가드

`scripts/run_v5_eval_metric.sh pppl ...`은 이제 `PPPL_SPLIT=train`일 때 기본적으로
실행을 거부한다. 현재 v5 diagnostic row를 의도적으로 실행할 때만 아래처럼 명시한다.

```bash
ALLOW_TRAIN_SOURCE_PPPL=1 \
PPPL_EVAL_ROLE=train_source_diagnostic \
bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

post-checkpoint wrapper에서 paired diagnostic PPPL을 실행하려면:

```bash
RUN_TRAIN_SOURCE_PPPL_DIAGNOSTIC=1 \
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 \
bash scripts/run_v5_post_checkpoint_evals.sh pppl
```

strict held-out PPPL은 held-out split을 만든 뒤에만 실행한다.

```bash
PPPL_SPLIT=test \
PPPL_EVAL_ROLE=heldout_test \
bash scripts/run_v5_eval_metric.sh pppl v5_fvt 1
```

## Report/PPT 문장

```text
본 실험은 v5를 폐기하지 않고 controlled 102-language Glot500-style replay로
유지한다. 다만 현재 PPPL은 local raw train split에서 추출한 intrinsic diagnostic
이므로 Glot500의 held-out test PPPL로 주장하지 않는다. strict held-out PPPL
재현은 v5.1에서 train/dev/test split을 먼저 만든 뒤 수행하는 correction line으로
분리한다.
```
