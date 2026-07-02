# v5 Embedding Initialization

This stage compares initialization methods for new vocabulary rows after v5
tokenizer expansion.

Subfolders:

- `00_random/`: Hugging Face default resize baseline
- `01_mean/`: source/global mean initialization
- `02_fvt/`: source-token decomposition initialization, main candidate
- `03_align/`: character/script-aware fallback ablation
- `04_zero_step_eval/`: before-training MLM and row-stat comparisons
- `05_audit/`: cross-method row copy, `<mask>`, byte-row, LM-head audits

Core rule: copy existing rows by token identity, not id prefix.

Implementation warning: do not use a helper that assumes `ids >= base_vocab_size`
are all newly added lexical tokens. v5 modifies a SentencePiece model directly,
and special ids such as `<mask>` can move. The checkpoint builder must compare
source and target token strings, then write an explicit remap/audit report.

Canonical commands:

```bash
bash scripts/run_v5_build_initializers.sh
python3 scripts/build_v5_initialized_checkpoint.py \
  --mode align \
  --target-tokenizer /home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm \
  --out-root /home/axt/mnt2/jongha/v5_glot50010/initialized_models
```

Current main artifacts:

- initialized models:
  `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_random`
- initialized models:
  `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_mean`
- initialized models:
  `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_fvt`
- init reports:
  `docs/exp/v5/1_embedding/05_audit/main/init_reports/`
- zero-step eval:
  `docs/exp/v5/1_embedding/04_zero_step_eval/main/`

Main FVT status:

- source identity rows copied: `250,002`
- new token rows: `118,685`
- FVT-initialized rows: `118,427`
- byte/global-mean rows: `256`
- global mean fallback rows: `2`
- `<mask>` remap: `250001 -> 368686`, max diff `0.0`
- LM head tied: `true`

Main zero-step result: on the v5-target group, `v5_fvt` improves weighted NLL
over `v5_random` by `-9.626238` and over `v5_mean` by `-3.167624`.

## Stage Exit Line

Move to `../2_training/` only after all of the following are true:

- `00_random/` and `02_fvt/` checkpoints exist and load with the v5 tokenizer.
- `01_mean/` and `03_align/` are either produced or explicitly marked as
  compute-optional ablations.
- every produced checkpoint has `init_report.json`.
- `05_audit/` confirms source-row copy, `<mask>` remap, byte-row handling,
  input/LM-head consistency, and weight tying.
- `04_zero_step_eval/` summarizes head, tail, all, and v5-target MLM proxy.

Minimum artifact line:

```text
random init pass + fvt init pass + audit pass + zero-step table ready
```

If this line is not met, MLM training should remain a pilot only.
