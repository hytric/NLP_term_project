# v5.2 시작 체크리스트

목표: `docs/exp/v5.2` 실험을 실제로 시작하고, 중간 결과를 사용자가 직접 확인할 수 있게 한다.

## 바로 볼 파일

| File | Purpose |
| --- | --- |
| `LIVE_STATUS.md` | 현재 준비/merge/tokenizer/init/MLM/checkpoint 상태 |
| `LIVE_STATUS.tsv` | 스크립트로 읽기 쉬운 상태 표 |
| `RUNBOOK_KO.md` | 전체 실행 순서 |
| `GOAL_COMMAND_KO.md` | 최종 goal 문안 |
| `3_evaluation/incremental_table_tracker.tsv` | downstream/table-fill 추적 |

상태 갱신:

```bash
python3 scripts/write_v52_live_status.py
```

## 시작 순서

| Step | Command | Expected output |
| ---: | --- | --- |
| 1 | `bash preprocessing/run_v52_glot5007_prepare.sh` | target7 symlink, stats/manifest |
| 2 | `LG_SAMPLING_FACTOR=0.3 SCALE=1.5 bash preprocessing/run_v52_glot5007_merge.sh` | sampled corpus text |
| 3 | `bash tokenization/train_v52_glot5007.sh` | Glot500-style extended tokenizer |
| 4 | `bash scripts/run_v52_build_initializers.sh` | `random/mean/fvt/weighted_fvt/family_mean` initialized checkpoints |
| 5 | `METHODS="random mean fvt weighted_fvt family_mean" GPUS="2 3" SAVE_STEPS=1000 MAX_STEPS=8000 bash modeling/launch_v52_init_all.sh` | five MLM runs, two jobs at a time |

## Overnight wrapper

위 과정을 한 번에 시작:

```bash
SCALE=1.5 LG_SAMPLING_FACTOR=0.3 METHODS="random mean fvt weighted_fvt family_mean" GPUS="2 3" \
  bash scripts/start_v52_overnight_pipeline.sh
```

백그라운드 시작은:

```bash
nohup bash scripts/start_v52_overnight_pipeline.sh \
  > /home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/start_v52_overnight.nohup.log 2>&1 &
```

## 완료 판정

- `LIVE_STATUS.md`에서 corpus/tokenizer/init 5종이 `ready`.
- `mlm random/mean/fvt/weighted_fvt/family_mean` row에 checkpoint가 1개 이상 생김.
- 최종 목표는 `checkpoint-8000`; `checkpoint-4000`은 수렴 결과가 아니라 diagnostic으로만 사용.
- 시간이 부족하면 `checkpoint-5000` 이상을 최소 table용으로 쓰되 final claim은 보류.
- downstream은 준비된 metric부터 채우고, POS/Taxi1500은 materialization 상태를 별도 row로 둔다.
