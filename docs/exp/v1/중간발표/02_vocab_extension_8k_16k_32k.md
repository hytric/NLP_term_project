# 02. Vocabulary Extension: 8k / 16k / 32k Tokenizers

Source: `docs/exp/second_try/03_vocab_extension`

Method: Step 01 train-only tokenizer corpus로 target10 SentencePiece unigram tokenizer를 `8k`, `16k`, `32k` 크기로 학습했다. XLM-R SentencePiece model 내부에 직접 병합하면 `<mask>` id가 밀릴 수 있으므로, target SPM piece를 HuggingFace `added_tokens`로 append했다. 이 방식은 XLM-R original ids를 보존하면서 target-language subword를 뒤에 추가한다.

Main finding: 세 후보 모두 structural gate와 tokenization metric gate를 통과했다. Vocab size가 커질수록 평균 tokens/word 감소 폭이 커졌고, tokenizer-only 기준 best candidate는 `32k`였다.

## Candidate Summary

| Vocab size | Aux pieces | Added pieces | XLM-R overlap | Avg tokens/word delta | Single-char delta | `<unk>` delta |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8k | 7,997 | 6,418 | 953 | -19.581% | -39.693% | 0.000 |
| 16k | 15,997 | 13,877 | 1,212 | -26.353% | -41.349% | 0.000 |
| 32k | 31,997 | 29,011 | 1,488 | -31.766% | -42.365% | 0.000 |

Interpretation: 8k도 충분히 fragmentation을 줄였지만, 32k가 평균 token count와 single-character token 비율을 가장 많이 낮췄다. 그래서 Step03에서는 `32000`이 selected candidate가 되었다.

## Per-Language Tokens/Word

| ISO | Language | Baseline | 8k | 16k | 32k | Best reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| acu | Achuar-Shiwiar | 2.891 | 2.040 | 1.885 | 1.765 | -38.948% |
| ake | Akawaio | 3.311 | 2.326 | 2.265 | 2.219 | -32.981% |
| bsn | Barasana-Eduria | 3.520 | 2.036 | 1.906 | 1.817 | -48.381% |
| chr | Cherokee | 2.253 | 2.673 | 2.459 | 2.230 | -1.021% |
| cop | Coptic | 2.066 | 2.296 | 2.005 | 1.799 | -12.924% |
| kbh | Camsa | 3.564 | 2.205 | 1.989 | 1.817 | -49.018% |
| nhg | Nahuatl (Tetelcingo) | 2.943 | 1.901 | 1.712 | 1.589 | -46.007% |
| oji | Ojibwa | 2.111 | 2.423 | 2.197 | 1.973 | -6.537% |
| syr | Syriac | 4.854 | 2.240 | 1.857 | 1.599 | -67.058% |
| usp | Uspanteco | 2.502 | 2.211 | 2.157 | 2.132 | -14.788% |

Notes:

- `syr` gains the most: `4.854 -> 1.599` tokens/word with 32k.
- `kbh`, `bsn`, and `nhg` also improve strongly, around 46-49% reduction.
- `chr` and `oji` are weaker cases. They pass the overall candidate gate, but 8k/16k can make their tokens/word worse; 32k is roughly neutral to mildly better.
- `cop` improves only at 16k/32k; 8k is too small and increases tokens/word.

## Per-Language Single-Character Rate

| ISO | Language | Baseline single-char % | 8k | 16k | 32k | 32k delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| acu | Achuar-Shiwiar | 21.504 | 19.236 | 19.327 | 19.322 | -10.147% |
| ake | Akawaio | 60.238 | 35.515 | 35.699 | 35.570 | -40.951% |
| bsn | Barasana-Eduria | 39.333 | 22.336 | 22.287 | 22.289 | -43.333% |
| chr | Cherokee | 11.252 | 19.974 | 20.874 | 21.002 | +86.651% |
| cop | Coptic | 3.265 | 13.665 | 11.958 | 10.675 | +226.953% |
| kbh | Camsa | 30.394 | 21.319 | 21.124 | 21.261 | -30.049% |
| nhg | Nahuatl (Tetelcingo) | 24.075 | 18.279 | 16.748 | 15.986 | -33.599% |
| oji | Ojibwa | 6.104 | 16.468 | 16.803 | 16.953 | +177.736% |
| syr | Syriac | 74.251 | 20.225 | 15.338 | 11.972 | -83.876% |
| usp | Uspanteco | 37.852 | 33.464 | 32.996 | 32.697 | -13.619% |

Interpretation: single-character reduction은 원래 single-char bottleneck이 큰 언어에서 특히 뚜렷하다. Syriac은 `74.251% -> 11.972%`로 거의 character-level tokenization에서 벗어난다. 반대로 Cherokee, Coptic, Ojibwa는 baseline single-char rate가 낮았기 때문에, extension 후 single-char rate가 오르는 부작용도 보인다. 그래서 이 지표는 전체 평균만 보면 안 되고, baseline bottleneck 유형과 함께 읽어야 한다.

## Tokenizer-Model Trade-Off

Tokenizer-only metric에서는 vocab이 클수록 대체로 좋아진다. 하지만 모델 학습까지 보면 trade-off가 생긴다.

| Vocab | Tokenizer-side benefit | Model-side cost |
| ---: | --- | --- |
| 8k | fragmentation 감소는 32k보다 작음 | added row가 적어서 학습 부담이 낮음 |
| 16k | 중간 수준의 tokenization 개선 | added row와 rare token 증가 |
| 32k | tokenizer-only 기준 best | added row가 많아 MLM에서 새 token 예측 부담이 큼 |

Step23 probe에서는 8k가 32k보다 낮은 MLM loss를 보였다:

| Vocab | Final raw MLM loss | Vs 32k |
| ---: | ---: | ---: |
| 32k | 4.946829 | baseline |
| 16k | 4.798048 | better |
| 8k | 4.541285 | best |

Therefore: 32k는 tokenizer metric에서는 가장 좋지만, model-side에서는 added-token row 수와 sparse supervision 때문에 8k보다 불리할 수 있다.

## Before/After Samples With 32k

### Syriac: character-level collapse largely fixed

- Verse: `b.MAT.1.1`
- Baseline token count: `47`
- Extended token count: `10`

Text:

> ܟܬܒܐ ܕܝܠܝܕܘܬܗ ܕܝܫܘܥ ܡܫܝܚܐ ܒܪܗ ܕܕܘܝܕ ܒܪܗ ܕܐܒܪܗܡ

Baseline preview:

```text
▁ ܟ ܬ ܒ ܐ ▁ ܕ ܝ ܠ ܝ ܕ ܘ ܬ ܗ ▁ ܕ ܝ ܫ ܘ ܥ ▁ ܡ ܫ ܝ ܚ ܐ ▁ ܒ ܪ ܗ ▁ ܕ ܕ ܘ ܝ ܕ ▁ ܒ ܪ ܗ ▁ ܕ ܐ ܒ ܪ ܗ ܡ
```

Extended preview:

```text
ܟܬܒܐ ܕܝܠܝ ܕܘ ܬܗ ܕܝܫܘܥ ܡܫܝܚܐ ܒܪܗ ܕܕܘܝܕ ܒܪܗ ܕܐܒܪܗܡ
```

Interpretation: baseline은 거의 모든 문자를 독립 token으로 쪼개지만, 32k extension은 단어 또는 더 긴 subword 단위로 묶는다.

### Barasana-Eduria: long verse compression

- Verse: `b.MAT.1.1`
- Baseline token count: `120`
- Extended token count: `59`

Text:

> Jesús ñacami “Rotimu̶orũ̶gõru̶cu̶ja mu̶” yigu̶, Dios ĩ cõar'i, Abraham ñamasir'i, to yicõari, U̶ju̶ David ñamasir'i jãnami. Tire mu̶a masisere bojagu̶ ñari, ĩ ñicu̶a vãmere mu̶are gotigu̶agu̶ yaja yu̶. Ado bajiro vãme cu̶timasiñujarã ĩna:

Baseline preview:

```text
▁Jesús ▁ ña cami ▁“ Ro ti mu ̶ or ũ ̶ g õr u ̶ cu ̶ ja ▁mu ̶ ” ▁y igu ̶ , ▁Dios ▁ ĩ ▁c õ ar ' i , ▁Abraham ▁ ña mas ir ' i , ...
```

Extended preview:

```text
Jesús ñacami ▁“ Rotim u̶orũ̶gõru̶cu̶ ▁ja mu̶ ▁” yigu̶ ▁ , Dios ▁ ĩ cõar ▁' i , Abraham ñamasir ▁' i , ...
```

Interpretation: combining marks와 긴 형태소가 완전히 해결되지는 않지만, baseline 대비 token count가 절반 수준으로 줄어 sequence-length 부담이 크게 낮아진다.

### Camsa: Latin-script low-resource morphology benefits

- Verse: `b.MAT.1.1`
- Baseline token count: `37`
- Extended token count: `19`

Text:

> Quemënga imnamna Jesucristbe bëts taitanga: Jesucristna Rey David y Abrahámbents̈ana ents̈á inamna.

Baseline preview:

```text
▁Quem ën ga ▁im nam na ▁Jesu cris t be ▁bë ts ▁tai tang a : ▁Jesu cris t na ▁Rey ▁David ▁y ▁Abra hám bent s ̈ ana ▁en ts ̈ á ▁in am na .
```

Extended preview:

```text
Quem ënga imnamna Jesucrist ▁be bëts taitanga ▁: Jesucrist ▁na Rey ▁David ▁y Abrahám bents̈ana ents̈á inamna ▁ .
```

Interpretation: Latin script라도 XLM-R가 잘 모르는 orthography와 morphology는 잘게 쪼개졌고, target-specific pieces가 이를 상당히 복구한다.

### Coptic: modest but real token-count improvement

- Verse: `b.MAT.1.1`
- Baseline token count: `17`
- Extended token count: `12`

Text:

> ⲠϪⲰⲘ ⲘⲘⲒⲤⲒ ⲚⲦⲈⲒⲎⲤⲞⲨⲤ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲠϢⲎⲢⲒ ⲚⲆⲀⲨⲒⲆ ⲠϢⲎⲢⲒ ⲚⲀⲂⲢⲀⲀⲘ.

Baseline preview:

```text
▁ ⲠϪⲰⲘ ▁ ⲘⲘⲒⲤⲒ ▁ ⲚⲦⲈⲒⲎⲤⲞⲨⲤ ▁ ⲠⲬⲢⲒⲤⲦⲞⲤ ▁ ⲠϢⲎⲢⲒ ▁ ⲚⲆⲀⲨⲒⲆ ▁ ⲠϢⲎⲢⲒ ▁ ⲚⲀⲂⲢⲀⲀⲘ .
```

Extended preview:

```text
▁ Ⲡ ϪⲰⲘ ⲘⲘⲒⲤⲒ ⲚⲦⲈⲒⲎⲤⲞⲨⲤ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲠϢⲎⲢⲒ ⲚⲆⲀⲨⲒⲆ ⲠϢⲎⲢⲒ ⲚⲀⲂⲢⲀⲀⲘ ▁ .
```

Interpretation: Coptic은 Syriac만큼 극단적이지 않아서 개선 폭이 작지만, 32k 기준 평균 tokens/word가 `2.066 -> 1.799`로 감소한다.

## Takeaway

Tokenizer-only 관점에서는 vocabulary extension이 성공적이다. 8k, 16k, 32k 모두 special id를 보존하고 round-trip gate를 통과했으며, 평균 fragmentation을 줄였다. 다만 이 결과는 “좋은 tokenizer 후보”를 의미하지, 곧바로 “좋은 adapted model”을 의미하지는 않는다. 이후 MLM control에서는 added-token row 학습 문제가 별도로 드러났기 때문에, Step03 결과는 model-performance claim이 아니라 tokenizer bottleneck 해소 evidence로 써야 한다.
