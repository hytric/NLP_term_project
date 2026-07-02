# Pivot And Backtranslation 요약

## 목적

이 단계의 목적은 Greek pivot path가 back-translation 확대에 사용할 만큼 안정적인지 확인하는 것이다.

앞 단계 `06_nmt_baselines`에서 direct Coptic/Syriac NMT는 학습은 가능했지만 반복 출력과 collapse를 보였다. 그래서 직접 Coptic <-> Syriac만 학습하는 대신, Greek 또는 English를 중간 언어로 사용하는 pivot/back-translation 전략을 검토했다.

원래 기대한 흐름은 다음과 같다.

```text
Syriac -> Greek
Greek -> Coptic
        ↓
synthetic Coptic/Syriac pair 생성
        ↓
NMT 재학습
```

하지만 synthetic data를 대량 생성하기 전에, 먼저 pivot model이 최소한 올바른 target script로 안정적인 출력을 만드는지 gate test를 수행했다.

## 데이터

기반 데이터는 `06_nmt_baselines`와 같은 aligned Bible pivot 데이터다. Coptic, Syriac, Greek, English가 verse ID 단위로 정렬되어 있고, 이 단계에서는 Greek pivot path를 확인하기 위해 다음 두 방향만 사용했다.

| Direction | 목적 |
| --- | --- |
| Syriac -> Greek | Greek pivot first leg 확인 |
| Greek -> Coptic | Coptic 생성 second leg 확인 |

각 run은 back-translation을 대규모로 돌리기 전의 작은 gate 설정으로 수행했다.

| 항목 | 설정 |
| --- | --- |
| Train slice | 256 examples |
| Dev/Test slice | 32 examples each |
| Steps | 50 |
| Max source length | 320 |
| Max target/generation length | 128 |

## 모델과 토크나이저

이 단계에서는 `pilot10k_mean` Glot500 encoder-decoder가 아니라 `google/byt5-small`을 사용했다.

이유는 pivot/back-translation gate에서 pretrained seq2seq model이 direct Glot500 encoder-decoder보다 collapse를 덜 보이는지 빠르게 확인하기 위해서다. ByT5는 byte-level tokenizer를 사용하므로 Syriac, Greek, Coptic 같은 다양한 script를 `<unk>` 없이 처리할 수 있다.

공통 설정:

- Model: `google/byt5-small`
- Tokenizer: ByT5 byte-level tokenizer
- Precision: fp32
- GPU: physical GPU 3
- Language tag: `translate {source_lang_name} to {target_lang_name}:`
- Model saving: disabled with `--skip_save_model`

## 학습 방식

두 run 모두 같은 작은 조건에서 학습했다.

- 256 train examples
- 32 validation examples
- 32 test examples
- 50 optimizer steps
- fp32 training
- checkpoint 저장 없이 metric과 generated prediction만 저장

이 설정은 최종 성능을 얻기 위한 full training이 아니라, back-translation을 확대해도 되는지 판단하기 위한 gate run이다.

## 결과

| Run | Direction | Train loss | Eval loss | Test loss | Test BLEU | Test chrF++ | Gen len | Unique pred | Target-script lines | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `byt5_small_pivot_syr_to_grc_len320_128_pilot256_step50_fp32_nosave` | Syriac -> Greek | 1.9952 | 1.4501 | 1.4563 | 0.0000 | 3.5930 | 127.0 | 16/32 | Greek 32/32 | Greek-looking but max-length repetition |
| `byt5_small_pivot_grc_to_cop_len320_128_pilot256_step50_fp32_nosave` | Greek -> Coptic | 2.2424 | 1.7635 | 1.7652 | 0.0000 | 0.0000 | 127.0 | 32/32 | Coptic 0/32 | target-script switch failure |

가장 중요한 신호는 `Gen len = 127.0`이다. `max target/generation length`가 128이므로, 모델이 거의 항상 길이 제한 직전까지 생성했다는 뜻이다. 즉 EOS를 제대로 배우지 못하고 max-length repetition으로 간 것이다.

## 질적 예시

Syriac -> Greek 출력은 Greek script를 사용하지만 반복적이다.

```text
αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα αναιμονα ανα
ανανανναννοια ανανναννανναννανναννανναννανναννανναννανναννανναν
```

Greek -> Coptic 출력은 더 심각하다. Coptic을 생성해야 하지만 Greek script를 계속 출력한다.

```text
ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο ητο
εν τω κοσμω, και εν τω κοσμω, και εν τω κοσμω, και εν τω κοσμω, και εν τω
```

즉 second leg가 Coptic target script로 전환하지 못했다.

## 해석

Greek pivot path는 back-translation 확대에 사용할 만큼 안정적이지 않다.

- Syriac -> Greek은 낮은 loss를 보이지만, 출력은 Greek-looking repetition이다.
- Greek -> Coptic은 target script 자체가 실패했다.
- 두 방향 모두 BLEU가 0.0이다.
- Greek -> Coptic test chrF++도 0.0이다.
- 이 상태로 synthetic data를 생성하면 noisy non-target-script data가 만들어질 가능성이 크다.

따라서 이 단계에서는 back-translation round를 진행하지 않고 gate에서 중단했다.

## 결론

`07_pivot_backtranslation`의 결론은 Greek pivot이 현재 설정에서는 usable하지 않다는 것이다. ByT5-small fp32는 `<unk>` 문제 없이 다양한 script를 처리할 수 있지만, 50-step gate run에서는 max-length 반복과 target-script failure를 보였다.

따라서 이 checkpoint들로 synthetic Coptic/Syriac data를 생성하면 오류가 누적될 가능성이 크다. 이후 back-translation을 다시 시도하려면 더 강한 pivot model, 더 나은 EOS/length control, target-script control, 또는 pivot-quality filtering이 먼저 필요하다.

## 발표용 한 줄 요약

> Greek pivot을 이용해 back-translation 데이터를 만들 수 있는지 gate test를 했지만, Syriac -> Greek은 max-length Greek 반복으로, Greek -> Coptic은 Coptic script 전환 실패로 무너졌다. 따라서 이 설정에서는 synthetic data 생성을 중단하고 back-translation을 확대하지 않았다.
