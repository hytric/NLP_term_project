# 03. Embedding Initialization: random / mean / fvt / align / focus

Source:

- `docs/exp/second_try/04_embedding_init`
- v2 confirmation: `docs/exp/second_try/14_v2_embedding_init`

Definition source:

- Method list comes from the vocabulary-extension initialization tutorial summary: `docs/exp/second_try/reference_summaries/vocab_extension_tutorial.md`.
- Original tutorial PDF location: `docs/exp/second_try/feedback/vocab_extension_tutorial.pdf`.
- This project implements practical/proxy versions in `docs/exp/second_try/04_embedding_init/run_step04.py` and `docs/exp/second_try/14_v2_embedding_init/run_step14.py`.
- In particular, `align` and `focus` here should be read as this repo's proxy implementations, not a full external-library implementation of Align/Focus.

Goal: vocabulary extension으로 새로 추가된 token row를 어떻게 초기화할지 비교했다. Step04는 Step03 selected `32k` tokenizer 기준이고, Step14는 v2 split에서 다시 selected `32k` tokenizer를 같은 방식으로 초기화한 확인 실험이다.

## Method Definitions

| Method | Initialization rule | Main intuition |
| --- | --- | --- |
| `random` | `resize_token_embeddings` 후 새 row에 남아 있는 random initialized vector를 그대로 사용 | 가장 단순한 baseline |
| `mean` | 기존 XLM-R vocabulary embedding row 전체 평균을 모든 새 row에 복사 | 안정적이지만 token별 차이가 없음 |
| `fvt` | 새 token surface를 기존 XLM-R tokenizer로 다시 tokenize한 뒤, 해당 base subtoken embedding 평균을 사용 | 새 token을 기존 subtoken 조합의 의미 공간에 붙임 |
| `align` | 새 token surface의 문자들을 기존 single-character token row와 align해서 평균을 사용; 없으면 `fvt` 또는 mean fallback | character-level coverage를 활용하는 proxy alignment |
| `focus` | `0.50 * fvt + 0.30 * align + 0.20 * base_mean`, 이후 평균 norm으로 rescale | fvt, character alignment, global prior를 섞은 proxy method |

Note: `random`, `mean`, `fvt`, `align`, `focus`라는 비교 축은 tutorial에서 가져왔고, 위 표의 구체적인 계산 규칙은 이 레포의 Step04/Step14 구현 기준으로 적었다. 그래서 발표에서는 "tutorial의 method family를 가져와서, 본 실험에서는 lightweight proxy로 구현했다"라고 말하면 된다.

Important caveat: current `fvt` source-id construction keeps any id returned by the base tokenizer as long as it is inside the original vocab range. It does not explicitly exclude `<unk>` or special ids. Therefore, for scripts such as Coptic, a new token can be initialized partly from the original XLM-R `<unk>` embedding if the base tokenizer maps the surface token to id `3`. In that case `fallback_rows=0` means "some source id existed", not necessarily "all source ids were meaningful non-unk subtokens".

Example:

```text
base tokenizer on ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ
-> ▁ id 6 + ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ id 3
-> id 3 maps back to <unk>
```

So `fvt` is still the best observed method in this experiment, but its coverage should be interpreted with this id-level `<unk>` caveat.

## Step04 Comparison Table

Tokenizer: Step03 selected `32000`

Base vocab size: `250002`

Merged vocab size: `279013`

New rows: `29011`

| Method | Initialized rows | Fallback rows | Mean norm | Std norm | Zero-step dev loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| `random` | 29,011 | 0 | 0.553992 | 0.014175 | 20.809267 |
| `mean` | 29,011 | 0 | 2.598133 | 0.000000 | 12.437534 |
| `fvt` | 29,011 | 0 | 4.586410 | 0.582020 | 8.490678 |
| `align` | 29,011 | 11,120 | 4.389801 | 0.691121 | 9.039471 |
| `focus` | 29,011 | 11,120 | 5.865720 | 0.000001 | 15.581055 |

Result: `fvt`가 zero-step dev loss `8.490678`로 가장 좋았다. `align`도 `9.039471`로 가까웠지만, character alignment fallback이 11,120 rows에서 발생했다. `random`은 loss가 매우 높고, `mean`은 random보다 안정적이지만 token-specific signal이 부족했다. `focus`는 의도와 달리 loss가 `15.581055`로 나빠서 selected candidate가 되지 못했다.

## V2 Confirmation Table

train, dev, test set을 명확하게 book 단위로 나눴을 떄 

Tokenizer: Step13 v2 selected `32000`

New rows: `29079`

Evaluation: Mark/dev only, no ACT final access

| Method | Fallback rows | Mean norm | Std norm | V2 zero-step Mark/dev loss |
| --- | ---: | ---: | ---: | ---: |
| `random` | 0 | 0.553993 | 0.014180 | 18.015601 |
| `mean` | 0 | 2.598133 | 0.000000 | 11.257934 |
| `fvt` | 0 | 4.591066 | 0.579873 | 8.681328 |
| `align` | 11,323 | 4.397304 | 0.690973 | 9.065176 |
| `focus` | 11,323 | 5.865720 | 0.000001 | 16.083522 |

V2에서도 `fvt`가 best로 재현되었다. 그래서 이후 v2 MLM control은 `/home/axt/mnt2/jongha/second_try/checkpoints/14_v2_embedding_init/xlmr_v2_32000_fvt`를 selected initialization으로 사용했다.

## Code Locations

Primary implementation:

- [run_step04.py](/home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/04_embedding_init/run_step04.py:41)
  - method list: line `41`
  - source map construction for `fvt` and `align`: lines `120-152`
  - row initialization logic for all five methods: lines `155-210`
  - checkpoint loop and tokenizer resize: lines `312-329`

V2 implementation:

- [run_step14.py](/home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/14_v2_embedding_init/run_step14.py:41)
  - method list: line `41`
  - Mark/dev-only text loading and final-access guard context: lines `109-117`
  - source map construction for `fvt` and `align`: lines `124-154`
  - row initialization logic for all five methods: lines `157-210`
  - checkpoint loop and tokenizer resize: lines `319-330`

Legacy helper:

- [init_target10_embeddings.py](/home/axt/jongha/Glot500-py39-eval/scripts/init_target10_embeddings.py:19)
  - older helper for only `random` and `mean`: lines `19-53`, `63-100`
  - useful for historical context, but the five-way comparison is implemented in Step04/Step14 scripts above.

## Takeaway

For the extended tokenizer, initialization matters a lot before any MLM training. The zero-step ordering is:

`fvt` best, `align` close second, `mean` middle, `focus` poor, `random` worst.

The supported conclusion is that new token rows should not be treated as arbitrary random parameters. The best current initialization is to decompose each new token back into existing XLM-R subtokens and average their embeddings (`fvt`). However, later MLM-control results show that good initialization alone is not enough to make the extended-vocabulary model competitive with original continued pretraining.
