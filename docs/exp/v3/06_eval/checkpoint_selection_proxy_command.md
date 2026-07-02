# Stage 06 Checkpoint Selection Proxy Commands

작성일: 2026-06-13

## High-Resource Control For Checkpoint-150

```bash
CUDA_VISIBLE_DEVICES=3 python3 preprocessing/run_third_try_stage06_high_resource_control_eval.py \
  --output-dir docs/exp/third_try/06_eval \
  --detail-name high_resource_control_mlm_eval_ckpt150.tsv \
  --comparison-name high_resource_control_language_comparison_ckpt150.tsv \
  --summary-name high_resource_control_summary_ckpt150.tsv \
  --model xlmr_base=xlm-roberta-base \
  --model fvt_ckpt150_seed13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot/checkpoint-150=13 \
  --model fvt_ckpt150_seed17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot/checkpoint-150=17 \
  --model fvt_ckpt150_seed23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot/checkpoint-150=23 \
  --baseline-label xlmr_base \
  --batch-size 4 \
  --max-length 512 \
  --fp16 \
  --require-cuda
```

## Target10 MLM Proxy For Checkpoint-150

```bash
CUDA_VISIBLE_DEVICES=3 python3 preprocessing/run_third_try_stage06_mlm_proxy_eval.py \
  --output-dir docs/exp/third_try/06_eval \
  --detail-name mlm_proxy_eval_ckpt150.tsv \
  --summary-name mlm_proxy_summary_ckpt150.tsv \
  --model xlmr_base=xlm-roberta-base \
  --model fvt_ckpt150_seed13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot/checkpoint-150=13 \
  --model fvt_ckpt150_seed17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot/checkpoint-150=17 \
  --model fvt_ckpt150_seed23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot/checkpoint-150=23 \
  --batch-size 4 \
  --max-length 512 \
  --fp16 \
  --require-cuda
```
