# Pilot Zero-Step MLM Proxy Analysis

작성일: 2026-06-26

## Scope

This is a pilot zero-step comparison, not a final downstream result. It uses the
pilot tokenizer and evaluates `5` examples per language over `5` head languages
and `10` v5 target languages.

Tokenizer:

```text
/home/axt/mnt2/jongha/v5_glot50010/tokenization/pilot10k_output/Glot500_extended_spm
```

Models:

- `v5_random`
- `v5_mean`
- `v5_fvt`

## Main Finding

`v5_fvt` strongly improves zero-step MLM proxy on the v5 target group compared
with both `v5_random` and `v5_mean`.

| Comparison | Group | Weighted NLL Delta | Interpretation |
| --- | --- | ---: | --- |
| `v5_fvt - v5_random` | v5 target | -9.448385 | large target-side improvement |
| `v5_fvt - v5_mean` | v5 target | -3.423689 | FVT improves beyond global mean |
| `v5_fvt - v5_random` | all | -6.503307 | overall pilot improvement |
| `v5_fvt - v5_mean` | all | -2.198663 | overall pilot improvement |
| `v5_fvt - v5_random` | head | -0.721256 | head control does not collapse |
| `v5_fvt - v5_mean` | head | +0.206423 | mean is slightly better on this tiny head sample |

Lower NLL is better.

## Summary Table

| Model | Group | Weighted NLL | Weighted PPPL |
| --- | --- | ---: | ---: |
| `v5_fvt` | all | 5.845506 | 345.677582 |
| `v5_fvt` | head | 3.573436 | 35.638850 |
| `v5_fvt` | v5 target | 7.002782 | 1099.688124 |
| `v5_mean` | all | 8.044169 | 3115.575309 |
| `v5_mean` | head | 3.367013 | 28.991806 |
| `v5_mean` | v5 target | 10.426471 | 33741.072977 |
| `v5_random` | all | 12.348813 | 230686.067210 |
| `v5_random` | head | 4.294692 | 73.309609 |
| `v5_random` | v5 target | 16.451167 | 13952471.416749 |

## Report Use

This is the first positive pilot evidence for the novelty claim:

```text
Source-token decomposition initialization gives newly appended target rows a
much better zero-step starting point than random resize.
```

Use cautiously:

- sample size is small;
- this is not after-MLM performance;
- full tokenizer and full zero-step evaluation must be rerun;
- downstream metrics are still required before final claims.
