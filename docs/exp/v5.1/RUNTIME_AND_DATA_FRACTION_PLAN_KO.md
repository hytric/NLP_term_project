# v5.1 Strict Rerun 데이터 비율 / GPU / ETA 계획

작성 시각: 2026-06-28 17:35 KST

## 결론

첫 strict rerun은 **5% corpus, `SCALE=1.5`** 로 시작하는 것을 권장한다. 전체
v5.1 dry-run 계획은 `162,608,099` lines라 full run은 너무 크다. 5%는 약
`8.13M` lines, 실제 5% dry-run 기준 `8,130,401` lines, 예상 text size 약 `1.67G`로 tokenizer/MLM/held-out PPPL/debug를
현실적으로 끝까지 밀 수 있는 크기다.

권장 실행 순서:

1. `5% + 3K steps`로 strict smoke/main hybrid를 먼저 완성한다.
2. 결과가 정상이고 시간이 남으면 `10% + 10K steps`를 main-strength rerun으로 올린다.
3. `20%` 이상은 보고서 마감 전 필수 경로가 아니라 optional compute ablation으로 둔다.

## 데이터 비율 후보

기준 dry-run:

```text
planned_total_samples = 162,608,099
scale = 30.0
```

| 사용 비율 | SCALE | planned lines | 예상 text size | 권장 용도 |
| ---: | ---: | ---: | ---: | --- |
| 1% | 0.3 | 1,626,081 | 0.33G | pipeline smoke only |
| 2% | 0.6 | 3,252,162 | 0.67G | tokenizer/init quick check |
| 3% | 0.9 | 4,878,243 | 1.00G | short debug run |
| **5%** | **1.5** | **8,130,401** | **1.67G** | **recommended first strict rerun; dry-run PASS** |
| 10% | 3.0 | 16,260,810 | 3.34G | stronger rerun if time allows |
| 20% | 6.0 | 32,521,620 | 6.68G | optional ablation |
| 100% | 30.0 | 162,608,099 | 33.42G | not deadline-safe |

예상 size는 v5 full merge `92,452,251` lines -> `19G`를 기준으로 환산했다.

## GPU / Batch 계획

현재 머신은 RTX A6000 48GB급 GPU 4장이 있다. strict rerun 학습은 가능하면
4장을 사용한다.

권장 4-GPU 설정:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3
NPROC_PER_NODE=4
PER_DEVICE_TRAIN_BATCH_SIZE=8
GRADIENT_ACCUMULATION_STEPS=12
```

effective batch:

```text
8 per_device * 4 GPUs * 12 accumulation = 384
```

이는 Glot500 continued pretraining의 batch `384`와 맞춘 설정이다.

Fallback:

| 상황 | 설정 |
| --- | --- |
| OOM 발생 | `PER_DEVICE_TRAIN_BATCH_SIZE=6`, `GRADIENT_ACCUMULATION_STEPS=16` |
| 안정적이고 VRAM 여유 | `PER_DEVICE_TRAIN_BATCH_SIZE=12`, `GRADIENT_ACCUMULATION_STEPS=8` |
| GPU 2장만 사용 가능 | `PER_DEVICE_TRAIN_BATCH_SIZE=12`, `GRADIENT_ACCUMULATION_STEPS=16` |

## 단계별 ETA

아래 ETA는 v5 관측값과 v5.1 dry-run 크기를 기준으로 한 보수적 추정이다. 실제 시간은
HF dataset cache 상태, disk I/O, SentencePiece sampling, GPU 점유율에 따라 달라진다.

### 5% + 3K steps 권장 경로

| Stage | 예상 시간 | 산출물 | Gate |
| --- | ---: | --- | --- |
| strict split planning manifest | done | `strict_split_manifest.tsv`, `strict_split_indices.jsonl` | stats 기반 planning complete |
| strict split arrow verification | done | verified split manifest | status PASS, 3 shrink exceptions |
| 5% merge dry-run | 1-3m | manifest/report | missing dirs 0, planned lines 8.13M |
| 5% train-only merge | done | train-only corpus | report PASS, 8,130,401 lines |
| tokenizer training | done | extended SPM | audit failure 0 |
| initializer build | done | random/FVT checkpoints | `<mask>` diff 0.0, tied head |
| zero-step + held-out PPPL setup | 30-60m | diagnostic + held-out cache | PPPL split recorded |
| random/FVT MLM 3K, 4 GPUs | 6-9h pair | matched 3K checkpoints | same steps/corpus/schedule |
| downstream + similarity | 3-8h | tables/plots | all required metric families accounted |
| report/PPT refresh | 20-60m | PDF/PPTX/table bundle | claim ledger updated |

### 10% + 10K stronger 경로

| Stage | 예상 시간 |
| --- | ---: |
| merge/tokenizer/init | 2-4h |
| random/FVT 10K MLM, 4 GPUs | 20-24h pair |
| downstream + similarity + report refresh | 5-10h |

## 실행 명령 템플릿

5% dry-run:

```bash
DOCS_EXP_ROOT=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1 \
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100_strict_5pct \
SCALE=1.5 \
SPLIT=train \
SPLIT_INDICES_PATH=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl \
DRY_RUN=1 \
bash preprocessing/run_v5_glot50010_merge.sh
```

5% train-only merge:

```bash
DOCS_EXP_ROOT=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1 \
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100_strict_5pct \
SCALE=1.5 \
SPLIT=train \
SPLIT_INDICES_PATH=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl \
bash preprocessing/run_v5_glot50010_merge.sh
```

4-GPU 3K MLM pair:

```bash
V5_ROOT=/home/axt/mnt2/jongha/v5_1_glot50010 \
EXP_NAME=Glot500_v51_glot50010_xlmr100_strict_5pct \
CUDA_VISIBLE_DEVICES=0,1,2,3 \
NPROC_PER_NODE=4 \
PER_DEVICE_TRAIN_BATCH_SIZE=8 \
GRADIENT_ACCUMULATION_STEPS=12 \
EXTRA_ARGS="--max_steps 3000 --save_steps 3000 --save_total_limit 2 --logging_steps 100" \
bash modeling/launch_v5_random_fvt_10k.sh
```

Held-out PPPL:

```bash
PPPL_SPLIT=test \
PPPL_EVAL_ROLE=heldout_test \
PPPL_SPLIT_INDICES_PATH=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl \
bash scripts/run_v5_eval_metric.sh pppl v5_fvt 0
```

## 현재 주의사항

- `strict_split_manifest.tsv`는 이제 `count_source=arrow` verified manifest이다.
- stats planning 파일은 `strict_split_manifest.stats_plan.tsv`로 보존했다.
- 일부 local raw dataset은 stats count와 실제 Arrow row count가 다르다.
  shrink 예외는 `azb_Arab`, `uig_Latn`, `san_Latn`이다.
- 따라서 final report에는 split manifest의 verification status와 shrink 예외를 반드시 적는다.
