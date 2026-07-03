# v5.2 Runtime Decisions

작성일: 2026-06-28

## 2026-06-28 22:19 KST: switch to fast diagnostic run

초기 overnight run은 정상적으로 시작됐지만 `PER_DEVICE_TRAIN_BATCH_SIZE=8`,
`GRADIENT_ACCUMULATION_STEPS=48`, `SAVE_STEPS=1000`, `MAX_STEPS=8000`으로 실행되어
optimizer step당 약 12-17초가 걸렸다. 이 속도에서는 8시간 안에 5-8개 checkpoint와
score table을 만들기 어렵다.

확인 당시 checkpoint는 0개였으므로 학습 artifact 손실 없이 slow run을 중단했다. 이후
동일 corpus, tokenizer, initializer를 재사용해 아래 fast diagnostic 설정으로 재시작했다.

```text
METHODS=random mean fvt align
GPUS=0 1 2 3
MAX_STEPS=4000
SAVE_STEPS=500
SAVE_TOTAL_LIMIT=8
PER_DEVICE_TRAIN_BATCH_SIZE=8
GRADIENT_ACCUMULATION_STEPS=8
LOGGING_STEPS=25
```

해석 규칙:

- 이 run은 8시간 table score를 확보하기 위한 checkpoint diagnostic이다.
- 비교 축은 `random`, `mean`, `fvt`, `align` initialization으로 유지한다.
- Glot500 논문식 effective batch 384 reproduction claim과는 분리해서 보고한다.
- 최종 claim은 paired checkpoint 결과가 실제로 채워진 뒤에만 승격한다.

관련 로그:

```text
/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/launch_v52_fast_ablation_20260628_221944.log
/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/v52_checkpoint_eval_watch_fast_20260628_221959.log
```

## 2026-06-30 KST: switch planned independent ablation to 5 initialization variants

`align`은 FVT와 byte-identical하게 collapse되었으므로 독립 방법으로 해석하지 않는다.
후속 ablation은 아래 5개 variant를 사용한다.

```text
METHODS=random mean fvt weighted_fvt family_mean
```

해석 규칙:

- `weighted_fvt`는 FVT source subtoken 평균에 surface-length weight를 주는 refinement이다.
- `family_mean`은 target7과 같은 family의 raw corpus provenance를 이용해 family별 source-token 평균으로 새 row를 초기화한다.
- 두 방법은 post-hoc exploratory ablation이며, 기존 v5.2 main 결과와 구분해서 보고한다.

## 2026-06-28 22:21 KST: relaunch with detached session

첫 fast diagnostic launch는 `nohup` background 방식으로 시작했지만, tool 세션 종료와 함께
child process group이 내려가면서 Python error 없이 weight loading 부근에서 로그가 끊겼다.
해당 attempt는 checkpoint를 만들기 전 종료됐으므로 training artifact는 없다.

이후 `setsid`로 학습과 watcher를 다시 분리 실행했다.

```text
train launch log:
/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/launch_v52_fast_ablation_setsid_20260628_222125.log

eval watcher log:
/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/v52_checkpoint_eval_watch_fast_setsid_20260628_222238.log
```

22:22 KST 확인 기준 네 method 모두 train loop에 진입했다. 로그상 설정은 다음과 같다.

```text
Num examples = 343112
Total train batch size = 64
Gradient Accumulation steps = 8
Total optimization steps = 4000
save_steps = 500
```

## 2026-06-28 22:49 KST: first 4-way checkpoint score row

`checkpoint-500`이 네 method 모두에서 생성됐고, watcher가 PPPL과 Tatoeba retrieval을
성공적으로 실행했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 500 | 374.606977 | 479.424743 | 161.877958 | 161.877958 | lower_is_better |
| pseudoperplexity | v5_target | 500 | 374.606977 | 479.424743 | 161.877958 | 161.877958 | lower_is_better |
| retrieval_tatoeba | all | 500 | 0.209241 | 0.217194 | 0.223194 | 0.223194 | higher_is_better |
| retrieval_tatoeba | v5_target | 500 | 0.209241 | 0.217194 | 0.223194 | 0.223194 | higher_is_better |

초기 diagnostic 기준으로는 `fvt`와 `align`이 `random`/`mean`보다 PPPL이 낮고 Tatoeba가
높다. 단, final claim은 후속 checkpoints에서도 같은 방향이 유지되는지 본 뒤 승격한다.

## 2026-06-28 22:50 KST: align collapsed to fvt

`fvt`와 `align`의 `checkpoint-500` score가 완전히 같아서 initializer artifact를 비교했다.
결과적으로 초기 `pytorch_model.bin`과 `checkpoint-500/pytorch_model.bin`의 SHA-256 hash가
각각 동일했다.

```text
v5_fvt init   = 3b2028be5bcb1382cca3c3bc007a1a1da8c01e6701b69182c614c0a40d7afa73
v5_align init = 3b2028be5bcb1382cca3c3bc007a1a1da8c01e6701b69182c614c0a40d7afa73

fvt step500   = 220037c170759c1f8af533906b703d83a12849da238f77b9ebfd97542d3ada63
align step500 = 220037c170759c1f8af533906b703d83a12849da238f77b9ebfd97542d3ada63
```

원인은 `align` 구현이 먼저 FVT decomposition을 시도하고, 실패한 token에만 unicode block
mean fallback을 적용하는 구조이기 때문이다. 이번 v5.2 tokenizer에서는 새 token 대부분이
FVT로 처리되어 `align`이 독립 method가 아니라 `fvt`와 동일한 artifact로 collapse됐다.

따라서 table에는 `align` 값을 남기되, 발표/보고에서는 독립 ablation으로 해석하지 않는다.
진짜 독립 align ablation이 필요하면 별도 script-aware/block-mean-only initializer를 추가
실험으로 만들어야 한다.

## 2026-06-28 23:08 KST: second 4-way checkpoint score row

`checkpoint-1000`도 네 method 모두 생성됐고, watcher가 PPPL/Tatoeba를 성공적으로
완료했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 1000 | 241.797413 | 270.934481 | 108.603835 | 108.603835 | lower_is_better |
| pseudoperplexity | v5_target | 1000 | 241.797413 | 270.934481 | 108.603835 | 108.603835 | lower_is_better |
| retrieval_tatoeba | all | 1000 | 0.222845 | 0.214241 | 0.254813 | 0.254813 | higher_is_better |
| retrieval_tatoeba | v5_target | 1000 | 0.222845 | 0.214241 | 0.254813 | 0.254813 | higher_is_better |

두 checkpoint 연속으로 `fvt`가 PPPL 최저, Tatoeba 최고다. 다만 `align`은 artifact
collapse 때문에 `fvt`와 같은 값으로 기록되며, 독립 method evidence로 세지 않는다.

## 2026-06-28 23:27 KST: third 4-way checkpoint score row

`checkpoint-1500`도 네 method 모두 생성됐고, watcher가 PPPL/Tatoeba를 성공적으로
완료했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 1500 | 190.915409 | 208.204215 | 90.288642 | 90.288642 | lower_is_better |
| pseudoperplexity | v5_target | 1500 | 190.915409 | 208.204215 | 90.288642 | 90.288642 | lower_is_better |
| retrieval_tatoeba | all | 1500 | 0.239559 | 0.235511 | 0.265353 | 0.265353 | higher_is_better |
| retrieval_tatoeba | v5_target | 1500 | 0.239559 | 0.235511 | 0.265353 | 0.265353 | higher_is_better |

세 checkpoint 연속으로 `fvt`가 독립 method 중 PPPL 최저, Tatoeba 최고다. `align`은
계속 `fvt`와 동일 artifact로 해석한다.

## 2026-06-28 23:50 KST: fourth 4-way checkpoint score row

`checkpoint-2000`도 네 method 모두 PPPL/Tatoeba 평가가 완료됐다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 2000 | 160.498560 | 172.580672 | 75.258020 | 75.258020 | lower_is_better |
| pseudoperplexity | v5_target | 2000 | 160.498560 | 172.580672 | 75.258020 | 75.258020 | lower_is_better |
| retrieval_tatoeba | all | 2000 | 0.245495 | 0.235162 | 0.274544 | 0.274544 | higher_is_better |
| retrieval_tatoeba | v5_target | 2000 | 0.245495 | 0.235162 | 0.274544 | 0.274544 | higher_is_better |

네 checkpoint 연속으로 independent methods 중 `fvt`가 PPPL 최저, Tatoeba 최고다.

## 2026-06-29 00:15 KST: fifth 4-way checkpoint score row

`checkpoint-2500`도 네 method 모두 PPPL/Tatoeba 평가가 완료됐다. 이로써 originally
planned 5-8 checkpoint diagnostic의 하한선인 5개 complete rows를 확보했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 2500 | 145.951840 | 150.454629 | 66.575042 | 66.575042 | lower_is_better |
| pseudoperplexity | v5_target | 2500 | 145.951840 | 150.454629 | 66.575042 | 66.575042 | lower_is_better |
| retrieval_tatoeba | all | 2500 | 0.250543 | 0.243860 | 0.290893 | 0.290893 | higher_is_better |
| retrieval_tatoeba | v5_target | 2500 | 0.250543 | 0.243860 | 0.290893 | 0.290893 | higher_is_better |

다섯 checkpoint 연속으로 independent methods 중 `fvt`가 PPPL 최저, Tatoeba 최고다.

## 2026-06-29 00:23 KST: sixth 4-way checkpoint score row

`checkpoint-3000`도 네 method 모두 PPPL/Tatoeba 평가가 완료됐다. 이로써 originally
planned 5-8 checkpoint diagnostic 범위 안에서 6개 complete rows를 확보했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 3000 | 133.106839 | 138.513402 | 61.603757 | 61.603757 | lower_is_better |
| pseudoperplexity | v5_target | 3000 | 133.106839 | 138.513402 | 61.603757 | 61.603757 | lower_is_better |
| retrieval_tatoeba | all | 3000 | 0.249892 | 0.246495 | 0.282306 | 0.282306 | higher_is_better |
| retrieval_tatoeba | v5_target | 3000 | 0.249892 | 0.246495 | 0.282306 | 0.282306 | higher_is_better |

여섯 checkpoint 연속으로 independent methods 중 `fvt`가 PPPL 최저, Tatoeba 최고다.
`checkpoint-3500`은 00:32 KST 기준 `mean`과 `align` 평가가 완료됐고, `fvt`/`random`
생성 및 평가가 이어지는 중이다.

## 2026-06-29 00:45 KST: seventh 4-way checkpoint score row

`checkpoint-3500`도 네 method 모두 PPPL/Tatoeba 평가가 완료됐다. 이로써 originally
planned 5-8 checkpoint diagnostic 범위 안에서 7개 complete rows를 확보했다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 3500 | 121.631484 | 131.012510 | 58.939731 | 58.939731 | lower_is_better |
| pseudoperplexity | v5_target | 3500 | 121.631484 | 131.012510 | 58.939731 | 58.939731 | lower_is_better |
| retrieval_tatoeba | all | 3500 | 0.247225 | 0.247829 | 0.280321 | 0.280321 | higher_is_better |
| retrieval_tatoeba | v5_target | 3500 | 0.247225 | 0.247829 | 0.280321 | 0.280321 | higher_is_better |

일곱 checkpoint 연속으로 independent methods 중 `fvt`가 PPPL 최저, Tatoeba 최고다.
`checkpoint-4000`은 00:45 KST 기준 `mean` 학습 및 평가가 완료됐고, `align` 학습 완료,
`fvt`/`random` 학습이 마지막 구간을 진행 중이다.

## 2026-06-29 00:49 KST: move watcher eval gpu to GPU1

기존 watcher는 GPU2에서 평가를 수행했고, 해당 시점에 `fvt` 학습도 GPU2를 사용하고 있었다.
`mean`과 `align` 학습이 완료되어 GPU1/GPU3가 비었으므로 watcher를 GPU1로 옮겨 마지막
`fvt`/`random` 학습과 평가가 충돌하지 않도록 했다.

```text
old watcher: /home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/v52_checkpoint_eval_watch_fast_setsid_20260628_222238.log
new watcher: /home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/v52_checkpoint_eval_watch_gpu1_setsid_20260629_004858.log
new watcher PID: 3193294
EVAL_GPU=1
POLL_SECONDS=60
```

## 2026-06-29 01:02 KST: eighth 4-way checkpoint score row

`checkpoint-4000`도 네 method 모두 PPPL/Tatoeba 평가가 완료됐다. 이로써 planned
5-8 checkpoint diagnostic의 상한인 8개 complete rows가 모두 확보됐다.

| Metric | Group | Step | Random | Mean | FVT | Align | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| pseudoperplexity | all | 4000 | 119.581715 | 128.258830 | 58.025602 | 58.025602 | lower_is_better |
| pseudoperplexity | v5_target | 4000 | 119.581715 | 128.258830 | 58.025602 | 58.025602 | lower_is_better |
| retrieval_tatoeba | all | 4000 | 0.248908 | 0.246194 | 0.282957 | 0.282957 | higher_is_better |
| retrieval_tatoeba | v5_target | 4000 | 0.248908 | 0.246194 | 0.282957 | 0.282957 | higher_is_better |

여덟 checkpoint 연속으로 independent methods 중 `fvt`가 PPPL 최저, Tatoeba 최고다.
`align`은 여전히 `fvt`와 byte-identical artifact로 collapse된 row이므로, 독립 evidence로
해석하지 않는다. 최종 live status 기준 active v5.2 process는 없고 GPU도 모두 idle이다.

## 2026-06-30 12:16 KST: stage-2 convergence run on three GPUs

`checkpoint-4000` diagnostic 결과는 확보됐지만, training loss와 PPPL이 아직 완전 수렴으로
보기에는 더 내려갈 여지가 있었다. GPU 23은 현재 호스트에서 노출되지 않았으므로, 사용자가
3-GPU 사용을 승인한 뒤 현재 idle에 가까운 GPU 0/2/3에 세 독립 method를 병렬 배치했다.

기존 output directory에서 checkpoint resume을 걸면 이전 4000-step run의 scheduler state가
거의 0 LR 지점에 묶일 수 있으므로, 각 method의 `checkpoint-4000`을 `model_name_or_path`로
사용하고 새 output directory에서 stage-2를 시작했다.

```text
random -> gpu=0, session=v52_random_converge, output=v52_random_mlm_converge_from4000
mean   -> gpu=2, session=v52_mean_converge,   output=v52_mean_mlm_converge_from4000
fvt    -> gpu=3, session=v52_fvt_converge,    output=v52_fvt_mlm_converge_from4000

INIT_MODEL_DIR=<method>/checkpoint-4000
MAX_STEPS=12000
SAVE_STEPS=1000
SAVE_TOTAL_LIMIT=12
PER_DEVICE_TRAIN_BATCH_SIZE=8
GRADIENT_ACCUMULATION_STEPS=8
LEARNING_RATE=3e-5
LOGGING_STEPS=25
```

`align`은 `fvt`와 byte-identical artifact로 collapse됐으므로 stage-2 independent
comparison에서는 제외했다. 12:18 KST 확인 기준 세 run 모두 preprocessing을 끝내고 trainer
loop에 진입했으며, 각 GPU가 약 36GB 메모리와 97-100% utilization을 보였다.

12:21 KST에는 checkpoint watcher도 GPU1에 붙였다. `scripts/write_v52_eval_model_matrix.py`는
stage-2 output directory인 `v52_*_mlm_converge_from4000/checkpoint-*`도 스캔하도록 확장했고,
local checkpoint step에 4000을 더해 `v52_random_step5000`처럼 total-step key를 만들도록
했다. watcher는 `METRICS="pppl retrieval_tatoeba"`, `POLL_SECONDS=120`, `MAX_LOOPS=360`으로
실행 중이다.

```text
watcher session=v52_stage2_eval_watch
watcher gpu=1
watcher log=/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/v52_stage2_checkpoint_eval_watch_20260630_122132.log
```
