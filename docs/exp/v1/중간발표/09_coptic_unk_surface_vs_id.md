# 09. Coptic `<unk>` Caveat: Surface Token vs Id-Level Token

Source:

- Baseline audit code: `docs/exp/second_try/02_tokenization_audit/run_step02.py`
- Baseline audit summary: `docs/exp/second_try/중간발표/01_xlmr_baseline_tokenization_audit.md`

## Why This Note Exists

Step02의 baseline tokenization audit에서는 Coptic의 `<unk>` 비율이 `0.000%`로 기록됐다. 그런데 XLM-R tokenizer를 직접 확인해보면, Coptic surface token이 화면에는 Coptic 문자열처럼 보이지만 실제 vocabulary id로는 `<unk>` id에 매핑될 수 있다.

따라서 Step02의 `<unk> % = 0`은 다음처럼 해석해야 한다.

> `tokenizer.tokenize(...)` 결과에서 보이는 token string 중 `<unk>`라는 문자열이 없었다는 뜻이지, id-level `<unk>`가 없었다는 뜻은 아니다.

## Audit Code Behavior

Step02는 `<unk>`를 token string 기준으로 세었다.

```python
tokens = tokenizer.tokenize(text)
unk_count = sum(1 for token in tokens if unk_token is not None and token == unk_token)
```

즉 `tokens` 안에 문자열 `"<unk>"`가 직접 나타나는지만 확인했다.

## Coptic Example

Text:

```text
ⲘⲠⲈⲢϮϨⲀⲠ ϨⲒⲚⲀ ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ ⲈⲢⲰⲦⲈⲚ.
```

This is the same Coptic sample used in the baseline tokenization note.

## What `tokenizer.tokenize(...)` Shows

```text
▁ ⲘⲠⲈⲢϮϨⲀⲠ ▁ ϨⲒⲚⲀ ▁ ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ ▁ ⲈⲢⲰⲦⲈⲚ .
```

이 출력만 보면 Coptic 단어들이 실제 vocabulary token처럼 보인다. 그래서 string 기준 `<unk>` count는 `0`이다.

## Id-Level Check

하지만 token string을 id로 바꾸고 다시 token으로 돌리면 다르게 보인다.

| # | Visible token from `tokenize` | Token id | Id maps back to |
| ---: | --- | ---: | --- |
| 1 | `▁` | 6 | `▁` |
| 2 | `ⲘⲠⲈⲢϮϨⲀⲠ` | 3 | `<unk>` |
| 3 | `▁` | 6 | `▁` |
| 4 | `ϨⲒⲚⲀ` | 3 | `<unk>` |
| 5 | `▁` | 6 | `▁` |
| 6 | `ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ` | 3 | `<unk>` |
| 7 | `▁` | 6 | `▁` |
| 8 | `ⲈⲢⲰⲦⲈⲚ` | 3 | `<unk>` |
| 9 | `.` | 5 | `.` |

XLM-R의 `<unk>` id는 `3`이다.

Counts for this sample:

| Count type | Value |
| --- | ---: |
| visible `<unk>` string count | 0 |
| id-level `<unk>` count | 4 |

## Interpretation

이 예시는 Coptic이 XLM-R vocabulary에 제대로 포함되어 있다고 보기 어렵다는 점을 보여준다. tokenizer output은 Coptic surface string을 보여줄 수 있지만, 실제 model id로는 `<unk>`에 매핑될 수 있다.

그래서 Coptic baseline은 이렇게 해석해야 한다.

- `tokens_per_word=2.066`은 surface tokenization 기준으로 mild/moderate fragmentation처럼 보인다.
- `single_char_token_pct=3.265%`도 surface token string 기준이다.
- 하지만 id-level coverage에서는 Coptic chunks가 `<unk>`로 들어갈 수 있으므로, Coptic은 "XLM-R가 잘 알고 있던 언어"라고 말하면 안 된다.

## Presentation Wording

발표에서는 이렇게 말하면 안전하다.

> Step02의 `<unk>` 비율은 token string 기준이라 Coptic처럼 surface-looking unknown piece가 실제로는 `<unk>` id에 매핑되는 경우를 놓칠 수 있습니다. 그래서 Coptic은 XLM-R가 원래 잘 알고 있던 언어라기보다, token string preview와 id-level vocabulary coverage를 구분해서 해석해야 합니다.

## Takeaway

Step02의 핵심 claim은 `<unk>` coverage가 아니라 fragmentation audit이다. 다만 Coptic처럼 surface token과 id-level token이 어긋나는 경우가 있으므로, Coptic 결과를 설명할 때는 `<unk>` metric을 강하게 주장하지 않고, id-level caveat를 함께 말해야 한다.

## Link To Embedding Initialization

이 caveat는 embedding initialization에도 영향을 준다. Step04/Step14의 current `fvt` implementation은 base tokenizer가 반환한 id가 original vocab range 안에 있으면 source id로 사용한다. 이때 `<unk>` id `3`도 제외하지 않는다.

따라서 Coptic 같은 경우:

```text
new extended token surface
-> base XLM-R tokenizer
-> visible Coptic token string
-> actual id 3
-> <unk> embedding used as one of the source vectors
```

즉 `fvt fallback rows = 0`이라고 해서 모든 새 token이 meaningful known subword로 초기화됐다는 뜻은 아니다. 어떤 row는 `<unk>` embedding을 포함해 초기화됐을 수 있다.
