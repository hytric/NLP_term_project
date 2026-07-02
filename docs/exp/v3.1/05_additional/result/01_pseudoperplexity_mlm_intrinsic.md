# Task 1. Pseudoperplexity / MLM Intrinsic Evaluation

작성일: 2026-06-19

## Task 정의

Pseudoperplexity는 masked LM이 target language의 실제 token을 얼마나 잘 예측하는지 보는 intrinsic evaluation이다.

핵심 질문은 다음이다.

> MLM continued training 이후, target10 low-resource language token prediction이 좋아졌는가?

이 task는 token-level 평가다. 번역 품질이나 sentence-level semantic alignment를 직접 증명하지 않는다.

Autoregressive LM은 왼쪽에서 오른쪽으로 perplexity를 계산할 수 있지만, XLM-R/Glot500 같은 bidirectional masked LM은 각 token을 하나씩 mask하고 원래 token 확률을 계산한다.

```text
Original: I went to the library.
Step 1:   <mask> went to the library. -> score "I"
Step 2:   I <mask> to the library.    -> score "went"
Step 3:   I went <mask> the library.  -> score "to"
```

각 token의 negative log likelihood 평균을 낸 뒤 exponentiate하면 pseudo-perplexity가 된다. 낮을수록 좋다.

## 데이터/설정

v3.1에는 intrinsic MLM signal이 두 종류 있다.

1. Dynamic MLM dev loss
   - target10 low-resource dev split만 사용, `701` chunked samples
   - HuggingFace dynamic MLM collator
   - non-special token 중 `15%` 선택
   - BERT-style `80/10/10`: mask/random/unchanged
   - 선택된 token 위치에 대해서만 loss 계산

2. Sampled strict pseudoPPL
   - `parallel_item_manifest.tsv`의 target10 low-resource dev rows만 사용
   - 언어별 첫 `50`개 dev row, 모델당 총 `500`개 row
   - max length `128`
   - non-special token을 하나씩 mask하고 score
   - 비교 모델: `xlmr_base` 및 다섯 `mlm200` init variants

여기서 중요한 구분:

> `xlmr_base`는 평가 대상 language가 아니라 baseline model이다. 모든 모델은 같은 target10 low-resource dev 문장에 대해 평가된다. 즉 high-resource language에 대한 pseudoPPL 결과가 아니다.

중요한 caveat:

> PseudoPPL은 tokenizer-sensitive metric이다. `xlmr_base`와 expanded-tokenizer candidate는 token 단위가 다르므로 base-vs-candidate 절대값 비교는 diagnostic으로만 다룬다. 더 안전한 비교는 expanded-tokenizer `mlm200` variant들 사이의 비교다.

추가 tokenization diagnostic 결과, 이 caveat는 특히 강하게 적용되어야 한다.

| Language | Model | Tokens | Unique tokens | Top token | Top token rate | Top tokens |
| --- | --- | ---: | ---: | --- | ---: | --- |
| `cop` | `xlmr_base` | `726` | `2` | `▁` | `0.964187` | `▁:700 .:26` |
| `cop` | `fvt_mlm200` | `1795` | `446` | `▁` | `0.442340` | `▁:794 ⲞⲨⲞϨ:74 ⲈⲂⲞⲖ:27 .:26 ϪⲈ:21` |
| `chr` | `xlmr_base` | `749` | `5` | `▁` | `0.775701` | `▁:581 ,:90 .:45 ;:29 ?:4` |
| `chr` | `fvt_mlm200` | `1648` | `379` | `▁` | `0.478762` | `▁:789 ,:90 .:45 ᎠᎴ:43 ᎾᏍᎩ:24` |
| `oji` | `xlmr_base` | `1028` | `6` | `▁` | `0.896887` | `▁:922 ,:76 ::16 !:10 ?:3` |
| `oji` | `fvt_mlm200` | `2352` | `527` | `▁` | `0.485544` | `▁:1142 ,:76 ᑕᔥ:41 ᐃᐃᒫ:24 ᐃᐃ:21` |

따라서 `xlmr_base`의 낮은 pseudoPPL은 low-resource text를 잘 modeling했다는 뜻이 아니다. Coptic/Cherokee/Ojibwa 같은 script에서 base tokenizer가 실제 문자를 거의 표현하지 못하고 `▁`/punctuation 중심으로 뭉개기 때문에, 맞혀야 할 token이 지나치게 쉬워진 것이다.

## 결과

Dynamic MLM dev loss:

| Rank | Init | Final dev loss | Delta vs `fvt` | Perplexity |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | `3.921798` | `0.000000` | `50.491170` |
| 2 | `focus` | `3.931313` | `0.009515` | `50.973852` |
| 3 | `align` | `4.060271` | `0.138473` | `57.990012` |
| 4 | `random` | `4.937548` | `1.015750` | `139.427975` |
| 5 | `mean` | `5.835072` | `1.913274` | `342.089214` |

Sampled strict pseudoPPL:

`xlmr_base`는 tokenization diagnostic에서 degenerate tokenization이 확인되었으므로, 보고서용 pseudoPPL 비교 표에서는 제외한다. Raw artifact에는 transparency를 위해 남겨둔다.

| Model | Phase | Weighted mean NLL | Weighted pseudoPPL | Macro mean NLL | Macro pseudoPPL |
| --- | --- | ---: | ---: | ---: | ---: |
| `align_mlm200` | mlm200 | `4.950712` | `141.275524` | `4.941329` | `139.956170` |
| `fvt_mlm200` | mlm200 | `5.002871` | `148.839893` | `5.001087` | `148.574587` |
| `focus_mlm200` | mlm200 | `5.054046` | `156.655071` | `5.052181` | `156.363199` |
| `random_mlm200` | mlm200 | `5.548407` | `256.828019` | `5.574280` | `263.559777` |
| `mean_mlm200` | mlm200 | `6.428914` | `619.500824` | `6.496823` | `663.031898` |

### 수치와 실제 예측 매칭 점검

PseudoPPL 수치만 보면 `align/fvt/focus`가 `random/mean`보다 좋지만, 이것을 "문장 안의 실제 단어를 잘 맞춘다"로 해석하면 과하다. 추가로 top-k prediction diagnostic을 계산한 결과, 전체 token 기준 top-1은 약 `43%`처럼 보이지만 이는 상당 부분 `▁` 공백 경계 token과 punctuation을 맞춘 효과다.

평균 정답 token 확률 score는 `exp(-weighted_mean_nll)`로 계산한다. 즉 pseudoPPL의 역수에 가까운 값이며, 모델이 masked 위치의 실제 gold token에 평균적으로 몇 % 확률을 줬는지를 나타낸다.

| Rank | Model | Weighted mean NLL | Weighted pseudoPPL | 평균 정답 token 확률 score | Percent |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `align_mlm200` | `4.986757` | `146.460676` | `0.006828` | `0.6828%` |
| 2 | `fvt_mlm200` | `5.033308` | `153.439754` | `0.006517` | `0.6517%` |
| 3 | `focus_mlm200` | `5.090770` | `162.514902` | `0.006153` | `0.6153%` |
| 4 | `random_mlm200` | `5.564147` | `260.902633` | `0.003833` | `0.3833%` |
| 5 | `mean_mlm200` | `6.439363` | `626.007745` | `0.001597` | `0.1597%` |

따라서 상위 세 모델도 정답 token에 평균 `0.6~0.7%` 정도의 확률만 준다. 이 score는 `random/mean`보다 상대적으로 높지만, 절대적으로는 1% 미만이므로 "잘 맞춘다"는 의미가 아니다.

내용 token만 따로 보면 실제 매칭률은 매우 낮다.

| Model | 전체 top-1 | 전체 평균 gold prob | 내용 token top-1 | 내용 token top-5 | 내용 token top-10 | 내용 token 평균 gold prob |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `align_mlm200` | `0.436359` | `0.006828` | `0.045114` | `0.077521` | `0.096517` | `0.000213` |
| `fvt_mlm200` | `0.427400` | `0.006517` | `0.040080` | `0.084566` | `0.110627` | `0.000213` |
| `focus_mlm200` | `0.434602` | `0.006153` | `0.040108` | `0.076205` | `0.094909` | `0.000175` |
| `random_mlm200` | `0.430646` | `0.003833` | `0.040033` | `0.070260` | `0.088453` | `0.000083` |
| `mean_mlm200` | `0.435263` | `0.001597` | `0.037271` | `0.064516` | `0.081685` | `0.000016` |

예측 샘플도 같은 방향을 보인다.

| Model | Language | Gold token | Gold prob | Top-1 prediction | Top-5 hit |
| --- | --- | --- | ---: | --- | ---: |
| `align_mlm200` | `cop` | `ⲦⲀ` | `0.000086` | `.` | `0` |
| `align_mlm200` | `cop` | `ⲘⲠⲒⲈⲨⲀⲄⲄⲈⲖⲒⲞⲚ` | `0.000059` | `.` | `0` |
| `align_mlm200` | `chr` | `ᎧᏃᎮᏛ` | `0.000136` | `.` | `0` |
| `fvt_mlm200` | `bsn` | `yigu̶` | `0.056677` | `̶` | `1` |
| `fvt_mlm200` | `cop` | `ⲠⲬⲢⲒⲤⲦⲞⲤ` | `0.000056` | `.` | `0` |

따라서 이 task의 올바른 결론은 다음이다.

> 현재 pseudoPPL/MLM intrinsic 결과는 "잘 맞춘다"가 아니라 "`align/fvt/focus`가 `random/mean`보다 덜 나쁘고, low-resource token distribution에 조금 더 안정적으로 적응했다"는 증거로 해석해야 한다.

더 엄밀히 말하면, target10 low-resource의 내용 token MLM은 아직 실질적으로 확보되지 않았다. 현재 결과는 MLM이 "된다"는 증거가 아니라, 제한된 budget에서 structured initialization이 collapse를 조금 덜 만든다는 약한 intrinsic signal이다.

## 해석

Raw pseudoPPL artifact의 절대값만 보면 `xlmr_base`가 가장 낮은 pseudoPPL을 보인다. 하지만 위 tokenization diagnostic 때문에 이것을 "XLM-R-base가 low-resource language를 가장 잘 modeling한다"로 해석하면 안 된다.

정확한 해석은 다음이다.

> `xlmr_base`의 pseudoPPL은 degenerate tokenization 때문에 artificially low일 수 있다. 따라서 base-vs-expanded pseudoPPL 비교는 invalid 또는 매우 약한 diagnostic으로만 다루고, expanded-tokenizer `mlm200` variants 사이의 순위를 중심으로 본다.

Expanded-tokenizer `mlm200` variants 안에서 sampled pseudoPPL 순위는 다음과 같다.

> `align` < `fvt` < `focus` < `random` < `mean`

Dynamic MLM dev loss에서는 `fvt`가 가장 좋고 `focus`가 거의 따라붙는다. Sampled pseudoPPL에서는 `align`, `fvt`, `focus`가 `random`, `mean`보다 앞선다. 두 intrinsic metric이 완전히 같지는 않지만, structured initialization 계열이 `random/mean`보다 안정적이라는 방향은 일치한다.

두 metric의 차이는 자연스럽다.

- pseudoPPL은 모든 scored token을 하나씩 mask한다.
- 현재 pseudoPPL은 언어별 `50`개 row sample이다.
- dynamic MLM loss는 token의 약 `15%`만 sampled mask한다.
- tokenizer/token distribution이 pseudoPPL에 크게 영향을 줄 수 있다.

가장 중요한 보고서 nuance:

> MLM token prediction과 semantic retrieval은 별도 diagnostic이다. `fvt`가 dynamic MLM loss에서 가장 좋아도 sentence retrieval이나 translation에서 가장 좋다는 뜻은 아니다.

보고서용 문장:

> Pseudoperplexity/MLM intrinsic evaluation shows that initialization affects low-resource masked-token prediction. Dynamic MLM dev loss selects `fvt`, while sampled pseudoPPL places `align`, `fvt`, and `focus` ahead of `random` and `mean`. We treat this as token-level adaptation evidence, not as proof of sentence-level semantic alignment.

더 정확히는 다음처럼 쓴다.

> All pseudoPPL evaluations are performed on target10 low-resource dev text. `xlmr_base` is included only as a baseline model on the same low-resource data, not as a high-resource evaluation condition.

## 주장 가능 범위

가능:

> Dynamic MLM loss와 sampled pseudoPPL은 initialization이 target10 token prediction에 영향을 준다는 intrinsic evidence를 제공한다. 이 관점에서는 `fvt/focus/align`이 가장 안정적인 variant들이다.

불가능:

> 이 결과만으로 low-resource content-token MLM이 충분히 작동한다고 주장할 수 없다. sentence-level semantic alignment나 translation quality도 증명할 수 없다.

## 산출물

| Artifact | 용도 |
| --- | --- |
| `../pseudoperplexity_scores.tsv` | per-language sampled pseudoPPL |
| `../pseudoperplexity_summary.tsv` | raw model-level sampled pseudoPPL, includes degenerate `xlmr_base` diagnostic row |
| `../pseudoperplexity_summary_expanded_only.tsv` | report-ready pseudoPPL summary excluding `xlmr_base` |
| `../pseudoperplexity_accuracy_scores.tsv` | per-language top-k prediction diagnostic |
| `../pseudoperplexity_accuracy_summary.tsv` | model-level top-k/content-token diagnostic |
| `../pseudoperplexity_gold_probability_scores.tsv` | average gold-token probability score, percent view |
| `../pseudoperplexity_prediction_samples.tsv` | content-token prediction examples |
| `../../04_ablation/init_mlm_probe/results.md` | dynamic MLM dev loss |
| `../../04_ablation/init_mlm_probe/mlm_training_protocol.md` | masking/training details |
| `../pseudoperplexity_tokenization_diagnostics.tsv` | pseudoPPL sample tokenization diagnostic |
