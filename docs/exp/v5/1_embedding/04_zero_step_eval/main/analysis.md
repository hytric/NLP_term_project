# v5 Main Zero-Step Analysis

Main zero-step MLM proxy uses the full v5 tokenizer and full initialized
checkpoints before MLM training.

## Setup

- tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- models: `v5_random`, `v5_mean`, `v5_fvt`
- sampled languages: `5` head + `10` v5 target
- examples per language: `5`
- max length: `96`

## Key Result

| Group | FVT - Random weighted NLL | FVT - Mean weighted NLL |
| --- | ---: | ---: |
| v5_target | -9.626238 | -3.167624 |
| head | -6.273844 | -1.415560 |
| all | -8.471624 | -2.564187 |

Lower NLL is better. The main tokenizer result supports the initialization
novelty: source-token decomposition initialization is much better than random
resize at zero step, and also better than global/source mean initialization.

## Interpretation

This is still an intrinsic pre-MLM diagnostic, not a downstream result. Its
role is to show that initialization quality is visible before continued
pretraining can wash out the effect. The final claim still requires matched
`v5_random` and `v5_fvt` MLM training and downstream evaluation.
