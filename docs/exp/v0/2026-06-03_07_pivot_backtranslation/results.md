# Results: Pivot And Backtranslation Gate

작성일: 2026-06-04

## Setup

목표:

- 07번 단계의 첫 게이트로 Greek pivot path가 back-translation 확대에 쓸 만큼 안정적인지 확인한다.
- 기존 English pivot이 formulaic/max-length 실패를 보였기 때문에, Greek pivot도 같은 작은 조건에서 먼저 검사한다.

공통 설정:

- GPU: physical GPU 3 only, via `source scripts/gpu3_env.sh`
- Model: `google/byt5-small`
- Precision: fp32
- Train slice: 256 examples
- Dev/test slice: 32 examples each
- Steps: 50
- Max source length: 320
- Max target/generation length: 128
- Language tag: `translate {source_lang_name} to {target_lang_name}:`
- Model saving: disabled with `--skip_save_model`

## Results

| Run | Direction | Train loss | Eval loss | Test loss | Test BLEU | Test chrF++ | Gen len | Unique pred | Target-script lines | Judgment |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `byt5_small_pivot_syr_to_grc_len320_128_pilot256_step50_fp32_nosave` | Syriac -> Greek | 1.9952 | 1.4501 | 1.4563 | 0.0000 | 3.5930 | 127.0 | 16/32 | Greek 32/32 | Greek-looking but max-length repetition |
| `byt5_small_pivot_grc_to_cop_len320_128_pilot256_step50_fp32_nosave` | Greek -> Coptic | 2.2424 | 1.7635 | 1.7652 | 0.0000 | 0.0000 | 127.0 | 32/32 | Coptic 0/32 | fails to switch into Coptic |

Peak GPU memory:

- Syriac -> Greek: 5,419.7 MiB
- Greek -> Coptic: 5,435.7 MiB

Artifact size:

- `docs/exp/2026-06-03_07_pivot_backtranslation`: 72K
- No model checkpoints were saved.

## Qualitative Check

Syriac -> Greek sample outputs are Greek-script but repetitive and cap-bound:

```text
αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα ανα
ανανανναννοια ανανναννανναννανναννανναννανναννανναννανναννανναν
```

Greek -> Coptic sample outputs are Greek-script, not Coptic:

```text
ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο
εν τω κοσμω, και εν τω κοσμω, και εν τω κοσμω, και εν τω κοσμω, και εν τω
```

## Interpretation

The Greek pivot path does not pass the back-translation gate.

- The first leg, Syriac -> Greek, learns low loss but generates to the maximum cap and repeats Greek-looking fragments.
- The second leg, Greek -> Coptic, is a hard failure for the current setting: all 32 test predictions contain Greek characters and none contain Coptic characters.
- BLEU is 0.0 for both legs.
- Greek pivot should not be scaled into synthetic Coptic/Syriac data generation yet.

## Decision

Stop this back-translation line after the gate run for now.

Recommended next step:

- Move to 08 evaluation/analysis to consolidate evidence for the report, or
- Test a stronger pivot/back-translation model or objective before generating synthetic data.

Do not run round-1 back-translation from these checkpoints; it would compound noisy, non-target-script outputs.
