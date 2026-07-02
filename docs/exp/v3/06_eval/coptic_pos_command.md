# Coptic POS Commands

작성일: 2026-06-13

## Data

```bash
python3 preprocessing/prepare_third_try_coptic_ud_pos.py
```

Output:

`/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos`

## Smoke

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_coptic_pos.py \
  --model xlmr_base=xlm-roberta-base \
  --output-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_smoke \
  --max-steps 2 \
  --save-steps 2 \
  --seed 13
```

## Pilot Runs

Common output root:

`/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200`

XLM-R-base:

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_coptic_pos.py \
  --model xlmr_base=xlm-roberta-base \
  --output-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200 \
  --max-steps 200 \
  --save-steps 200 \
  --seed 13
```

FVT seed 13:

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_coptic_pos.py \
  --model fvt_seed13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot \
  --output-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200 \
  --max-steps 200 \
  --save-steps 200 \
  --seed 13
```

FVT seed 17:

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_coptic_pos.py \
  --model fvt_seed17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot \
  --output-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200 \
  --max-steps 200 \
  --save-steps 200 \
  --seed 13
```

FVT seed 23:

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_coptic_pos.py \
  --model fvt_seed23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot \
  --output-root /home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200 \
  --max-steps 200 \
  --save-steps 200 \
  --seed 13
```

Note: the local `run_tag.py` stopping condition records `global_step = 201` for `--max-steps 200`.

## POS Metrics

The tagger's built-in `seqeval` F1 is NER-style and not the primary POS metric. Compute token-level POS accuracy and macro F1 from gold/pred labels:

```bash
python3 preprocessing/evaluate_third_try_coptic_pos_metrics.py
```

Outputs:

- `docs/exp/third_try/06_eval/coptic_pos_results.tsv`
- `docs/exp/third_try/06_eval/coptic_pos_summary.tsv`
- `docs/exp/third_try/06_eval/coptic_pos_label_metrics.tsv`
