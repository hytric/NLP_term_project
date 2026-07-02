# 03 Align Init

Exploratory character/script-aware initialization. Use this folder for align
fallback experiments when `fvt` has many missing or `<unk>` decompositions.

## Next Step Gate

This exploratory ablation is eligible for `../04_zero_step_eval/` only after the
fallback rule is explicit enough to reproduce.

Pass line:

- align rule is written, including script/character matching policy.
- trigger condition from `../02_fvt/` is recorded.
- checkpoint loads with the v5 tokenizer.
- new row count, align-initialized count, and fallback count are recorded.
- `<mask>` remap and LM head consistency are checked.

Required artifacts:

- checkpoint path note
- `init_report.json`
- align-rule note
- fallback/count table

If the rule is not clearly better motivated than `fvt`, keep this method as an
appendix ablation rather than a main report condition.
