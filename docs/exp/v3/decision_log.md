# Third Try Decision Log

작성일: 2026-06-12

## Locked Decisions

| Decision | Value | Source | Status |
| --- | --- | --- | --- |
| Main framing | target10 low-resource performance-improvement model, Glot500-inspired protocol | `scope_lock_20260612.md` | LOCKED |
| Existing first/second try role | ablation/failure analysis | `ablation_study.md` | LOCKED |
| Base model | `xlm-roberta-base` | `plan.md` | LOCKED |
| Scale baseline | do not use `xlm-roberta-large` | `scope_lock_20260612.md` | LOCKED |
| Main target set | existing target10: `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp` | `scope_lock_20260612.md` | LOCKED |
| Coptic/Syriac role | main experiment | `scope_lock_20260612.md` | LOCKED |
| High-resource data | must be used simultaneously with low-resource targets as replay/control | `scope_lock_20260612.md` | LOCKED |
| Vocabulary operation | preserve existing XLM-R ids and append new pieces | `plan.md` | LOCKED |
| Main init | compare multiple embedding initialization methods; random remains required baseline | `scope_lock_20260612.md` | LOCKED |
| Seeds | at least 3 seeds for model-dependent comparisons | `scope_lock_20260612.md` | LOCKED |
| Main training | full-model MLM | `plan.md` | LOCKED |
| Main data | high-resource + target10 low-resource mixture | `scope_lock_20260612.md` | LOCKED |
| Main evaluation | downstream improvement on target10 is required | `scope_lock_20260612.md` | LOCKED |

## Resolved Stage 00 Decisions

| Decision | Resolution | Evidence | Status |
| --- | --- | --- | --- |
| Exact high-resource replay language list | English, German, Japanese, Korean | GlotCC-V1 configs and Bible XML inventory confirmed | RESOLVED |
| True high-resource source | GlotCC-V1 web replay: `eng-Latn`, `deu-Latn`, `jpn-Jpan`, `kor-Hang` | materialized manifest under `/home/axt/mnt2/jongha/third_try/high_resource/glotcc` | RESOLVED |
| Domain-matched high-resource control | Bible English, German, Japanese, Korean | raw Bible XML row counts confirmed | RESOLVED |
| Target10 low-resource split | second_try V2 clean split | V2 train/dev/final-test artifacts confirmed | RESOLVED |
| Byte fallback vs character coverage | measured as Stage 03 ablation, not main tokenizer replacement | `03_tokenizer/fallback_ablation_summary.tsv` | RESOLVED |
| Current claim route | diagnostic negative for current compute-bounded candidate | `07_main_claim/results.md` | RESOLVED |
| Prior experiment placement | first_try/second_try mapped as ablation/failure analysis | `08_ablation/results.md` | RESOLVED |

## Decisions To Resolve Later

| Decision | Default | Needed Evidence | Owner |
| --- | --- | --- | --- |
| Downstream task subset for target10 | Coptic POS plus target10 Bible proxies under current local data | dataset availability and leakage safety | Stage 06 |
| Exact init method list | random, mean, fvt, align, focus candidates | implementation feasibility and compute budget | Stage 04 |
| Vocab size grid under 1-GPU budget | reuse 8k/16k/32k plus selected main size | tokenizer and MLM pilot evidence | Stage 03 |

## Claim Guardrails

| Claim Type | Allowed Only If |
| --- | --- |
| tokenizer improvement | tokenization before/after table passes Stage 03 |
| representation improvement | PPPL/retrieval/alignment improves in Stage 06 |
| downstream improvement | classification/NER/POS or accepted Glot500 task improves in Stage 06 |
| no catastrophic forgetting | high-resource replay/control summary does not collapse |
| ablation conclusion | Stage 08 maps the run as ablation and links evidence |
| extension transfer | Stage 09 records every deviation from main protocol |
