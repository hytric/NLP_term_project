# Task 7. Project-Specific Translation Diagnostic

작성일: 2026-06-19

## Task 정의

Translation은 Glot500의 core encoder-only evaluation task는 아니지만, Coptic-Syriac 프로젝트에서는 필요하다. 따라서 이 결과는 representation quality의 직접 증거라기보다 project-specific diagnostic으로 보고한다.

## 데이터/설정

- directions: `cop -> syr`, `syr -> cop`
- train rows: `5389`
- dev rows: `678`
- final-test rows: `1006`
- encoder: frozen XLM-R-base 또는 replay-safe third_try candidate
- decoder: 동일한 one-layer Transformer decoder
- candidate seeds: `13`, `17`, `23`
- metrics: chrF++, BLEU, script validity, EOS/max-length, empty prediction rate, diversity/collapse diagnostics

## 결과

Final-test chrF++:

| Direction | Final chrF++ baseline | Final chrF++ candidate mean | Delta |
| --- | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `+3.4949` |

핵심 collapse diagnostic:

| Direction | Model group | EOS seen | Hit max length | Empty pred rate | Script valid | chrF++ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `syr -> cop` | XLM-R-base | `0.0219` | `0.9781` | `1.0` | `0.0` | `0.0` |
| `syr -> cop` | third_try mean | `0.9970` | `0.0030` | `0.0` | `1.0` | `3.4949` |

Retrieval-only comparison:

| Direction | Model group | Decoder chrF++ | Retrieval chrF++ | Decoder - Retrieval |
| --- | --- | ---: | ---: | ---: |
| `cop -> syr` | XLM-R-base | `1.4169` | `3.7007` | `-2.2838` |
| `cop -> syr` | third_try mean | `3.6836` | `8.3751` | `-4.6915` |
| `syr -> cop` | XLM-R-base | `0.0` | `16.6706` | `-16.6706` |
| `syr -> cop` | third_try mean | `3.4949` | `12.2518` | `-8.7570` |

## 해석

Adapted encoder/tokenizer는 simple decoder가 severe target-script collapse를 피하도록 돕고, chrF++도 개선한다. 하지만 BLEU는 여전히 거의 0이고, 출력은 반복적/일반적이며, retrieval-only baseline이 decoder보다 높다.

따라서 이 task는 target-script/generation mechanics를 보여주는 diagnostic으로는 유용하지만, 번역 품질 성공을 주장하기에는 부족하다.

## 주장 가능 범위

가능:

> Adapted model은 simple-decoder diagnostic을 개선하고 major target-script collapse mode를 완화한다.

불가능:

> 이 시스템이 실제로 유용한 Coptic-Syriac translator라고 주장할 수 없다.

## 산출물

| Artifact | 용도 |
| --- | --- |
| `../../03_decoder_translation/results.md` | main decoder result |
| `../../03_decoder_translation/decoder_collapse_metric_summary.tsv` | collapse diagnostics |
| `../../03_decoder_translation/retrieval_vs_decoder_summary.tsv` | retrieval-only comparison |
| `../../03_decoder_translation/decoder_collapse_samples.md` | qualitative samples |
