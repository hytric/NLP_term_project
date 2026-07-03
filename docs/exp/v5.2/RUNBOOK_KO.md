# v5.2 Runbook

작성일: 2026-06-28

## Run Identity

```text
run_id = v5.2_glot5007
experiment_name = Glot500_v52_glot5007_xlmr100
root = /home/axt/mnt2/jongha/v5.2_glot5007
docs = docs/exp/v5.2
```

## 0. 확정된 실험

- Glot500 논문 흐름을 따른다.
- corpus는 `92 XLM-R-seen + 7 XLM-R-unseen target`이다.
- target7은 `dtp_Latn`, `xav_Latn`, `bam_Latn`, `csb_Latn`, `ile_Latn`, `lij_Latn`, `fur_Latn`이다.
- tokenizer는 Glot500식 vocab injection으로 고정한다.
- Yamaguchi vocabulary expansion은 main에서 제외하고 추가 실험으로 둔다.
- main table은 `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean` 5-way initialization ablation이다.
- checkpoint 평가는 8시간 run 동안 5-8회 정도 발생하도록 둔다.

## 1. Target7 준비

이미 2026-06-28에 실행했고 성공했다.

```bash
bash preprocessing/run_v52_glot5007_prepare.sh
```

확인 결과:

```text
XLM-R seen dataset dirs available under v5 raw: 92/92
selected Glot500 targets: 7/7
v5 raw: /home/axt/mnt2/jongha/v5.2_glot5007/raw
```

생성된 파일:

```text
docs/exp/v5.2/0_tokenizer/miscellaneous/languages_stats_glot5007_xlmr100.csv
docs/exp/v5.2/0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv
docs/exp/v5.2/0_tokenizer/miscellaneous/glot500_candidate_pool_min30k.tsv
```

## 2. Corpus Merge

8시간 run용 기본값은 기존 strict sampled corpus 흐름에 맞춰 `alpha=0.3`, `scale=1.5`를
사용한다. full-scale 재현이 필요하면 `SCALE`을 비우거나 더 크게 둔다.

```bash
LG_SAMPLING_FACTOR=0.3 SCALE=1.5 bash preprocessing/run_v52_glot5007_merge.sh
```

예상 output:

```text
/home/axt/mnt2/jongha/v5.2_glot5007/data/Glot500_v52_glot5007_xlmr100.txt
docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.manifest.tsv
docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.report.json
```

## 3. Tokenizer

```bash
bash tokenization/train_v52_glot5007.sh
```

예상 output:

```text
/home/axt/mnt2/jongha/v5.2_glot5007/tokenization/output/Glot500_extended_spm
```

## 4. Initialization

5-way ablation용 `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean` 전체를 만든다.

```bash
bash scripts/run_v52_build_initializers.sh
```

`family_mean`은 기본적으로 `FAMILY_MAX_EXAMPLES_PER_LANGUAGE=5000` capped provenance scan을
사용한다. full raw scan이 필요하면 `FAMILY_MAX_EXAMPLES_PER_LANGUAGE=0`으로 실행한다.

예상 output:

```text
/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_random
/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_mean
/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_fvt
/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_weighted_fvt
/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_family_mean
```

각 directory의 `init_report.json`에서 확인할 것:

- `mask_max_abs_diff_after_copy == 0` 또는 매우 작은 값
- `lm_head_tied_after_init == true`
- `copied_with_id_remap` count
- `initialized_fvt`, `initialized_weighted_fvt`, `initialized_family_mean`, `initialized_global_mean_fallback`, `new_byte_rows`

## 5. MLM Training

아침까지 빠르게 table score를 만들려면 GPU 2장만 사용해 `random`, `mean`,
`fvt`, `weighted_fvt`, `family_mean` 다섯 method를 학습한다.

논문식 hyperparameter parity를 유지하는 기본 command는 아래와 같다. 이 설정은
effective batch 384를 맞추지만, 실제 machine throughput에 따라 8시간 안에 5-8개
checkpoint를 만들기 어려울 수 있다.

```bash
METHODS="random mean fvt weighted_fvt family_mean" GPUS="2 3" SAVE_STEPS=1000 MAX_STEPS=8000 \
  bash modeling/launch_v52_init_all.sh
```

method 수가 GPU 수보다 많으면 launcher는 GPU 목록 크기만큼 먼저 실행하고, 남은 method를
다음 wave로 이어서 실행한다.

GPU를 두 장만 직접 지정하려면 pair launcher도 사용할 수 있다.

```bash
METHOD_A=random METHOD_B=fvt GPU_A=2 GPU_B=3 SAVE_STEPS=1000 MAX_STEPS=8000 \
  bash modeling/launch_v52_init_pair.sh
```

기본 MLM hyperparameter는 Glot500 논문을 따른다.

| Item | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| objective | MLM |
| learning rate | `5e-5` |
| Adam betas | `0.9`, `0.999` |
| per-device batch | `12` default, `8` overnight-safe |
| gradient accumulation | `32` default, `48` overnight-safe |
| effective batch per method | `384` |
| max sequence length | `512` |
| MLM probability | `0.15` |
| language sampling alpha | `0.3` |

checkpoint 수가 너무 적으면 `SAVE_STEPS`를 낮추고, 너무 많으면 올린다. 목표는
`5000/6000/7000/8000` trajectory를 볼 수 있게 하는 것이다. 이전 `4000` step 결과는
수렴 checkpoint가 아니라 early diagnostic으로만 사용한다. 원 Glot500은 `10K` step마다
checkpoint를 저장했지만, v5.2는 short-budget initialization ablation이므로 `1000` step
default를 사용한다.

### Overnight fast diagnostic mode

8시간 안에 score table을 반드시 채워야 할 때는 parity run과 분리해서 fast diagnostic
mode를 사용한다. Corpus, tokenizer, initializer는 동일하게 유지하되, optimizer step을
빠르게 만들기 위해 gradient accumulation을 낮춘다. 이 표는 initialization ablation의
빠른 비교용이며, 수렴 결과나 Glot500 논문식 effective batch 384 claim과는 분리해서
보고한다.

```bash
METHODS="random mean fvt weighted_fvt family_mean" GPUS="2 3" \
MAX_STEPS=4000 SAVE_STEPS=500 SAVE_TOTAL_LIMIT=8 \
PER_DEVICE_TRAIN_BATCH_SIZE=8 GRADIENT_ACCUMULATION_STEPS=8 LOGGING_STEPS=25 \
  bash modeling/launch_v52_init_all.sh
```

fast diagnostic table을 인용할 때는 다음 caveat를 함께 둔다.

```text
This overnight table uses the same v5.2 corpus, tokenizer, and initialized models,
but lowers gradient accumulation to produce checkpoint-level diagnostics within
the available wall-clock budget. The Glot500-parity effective-batch run remains
the stronger reproduction setting. A 4000-step checkpoint should be treated as an
early diagnostic point, not as a converged final checkpoint.
```

## 6. Checkpoint Evaluation

다른 GPU, 예를 들어 GPU 2를 평가 전용으로 둔다.

```bash
CUDA_VISIBLE_DEVICES=2
```

checkpoint가 생길 때마다 우선순위는 다음과 같다.

| Priority | Metric |
| ---: | --- |
| 1 | training loss / checkpoint health |
| 2 | PPPL or MLM proxy |
| 3 | Tatoeba retrieval |
| 4 | Bible retrieval after materialization |
| 5 | NER |
| 6 | POS if splits are available |
| 7 | Roundtrip/Taxi1500 after generated data exists |
| 8 | Embedding similarity/2D map |

기존 v5 evaluation wrappers는 `docs/exp/v5` model matrix에 강하게 묶여 있으므로,
v5.2 첫 checkpoint가 생기면 `docs/exp/v5.2/3_evaluation/model_matrix.tsv`를 생성한
뒤 wrapper를 연결한다. 그 전까지는 각 metric command를 checkpoint path 기준으로 직접
실행하고, 결과를 `incremental_table_tracker.tsv`에 수동/반자동으로 넣는다.

## 7. Logging Rule

결과 table에는 항상 아래 네 열을 둔다.

```text
method, checkpoint, metric, status
```

claim 승격 규칙:

- paired method 결과가 없으면 claim으로 쓰지 않는다.
- `fvt`가 단일 checkpoint에서 좋아도 최종 claim으로 바로 승격하지 않는다.
- `random/mean/fvt/weighted_fvt/family_mean` 전체 table이 나온 뒤 `fvt` 계열 우위를 말한다.
- POS/Taxi1500은 local data가 없으면 pending/materialization-needed로 남긴다.
