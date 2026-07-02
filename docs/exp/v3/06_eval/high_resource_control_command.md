# High-Resource Control Commands

작성일: 2026-06-13

## Scope

This check evaluates held-out Bible-domain control books that were excluded from Stage 01 control training:

- languages: `eng`, `deu`, `jpn`, `kor`
- books: `ACT`, `JOH`, `MAR`
- metric: deterministic masked-LM loss proxy
- collapse diagnostic threshold: fvt mean loss delta vs XLM-R `> +0.500000`

## Smoke

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_stage06_high_resource_control_eval.py \
  --require-cuda \
  --fp16 \
  --max-rows-per-language 2 \
  --detail-name high_resource_control_mlm_eval_smoke.tsv \
  --comparison-name high_resource_control_language_comparison_smoke.tsv \
  --summary-name high_resource_control_summary_smoke.tsv \
  --model xlmr_base=xlm-roberta-base=NA \
  --model fvt_seed13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot=13 \
  --model fvt_seed17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot=17 \
  --model fvt_seed23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot=23
```

## Full Control Proxy

```bash
CUDA_VISIBLE_DEVICES=3 \
python3 preprocessing/run_third_try_stage06_high_resource_control_eval.py \
  --require-cuda \
  --fp16 \
  --batch-size 8 \
  --detail-name high_resource_control_mlm_eval.tsv \
  --comparison-name high_resource_control_language_comparison.tsv \
  --summary-name high_resource_control_summary.tsv \
  --model xlmr_base=xlm-roberta-base=NA \
  --model fvt_seed13=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot=13 \
  --model fvt_seed17=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot=17 \
  --model fvt_seed23=/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot=23
```

Outputs:

- `docs/exp/third_try/06_eval/high_resource_control_mlm_eval.tsv`
- `docs/exp/third_try/06_eval/high_resource_control_language_comparison.tsv`
- `docs/exp/third_try/06_eval/high_resource_control_summary.tsv`
