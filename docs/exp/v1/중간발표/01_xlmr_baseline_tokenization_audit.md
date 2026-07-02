# 01. XLM-R Baseline Tokenization Audit

Source: `docs/exp/second_try/02_tokenization_audit`

Baseline tokenizer: `xlm-roberta-base`

Split: Step 01 `train` only, max 500 verses per language

Main finding: target10 전체에서 XLM-R tokenization fragmentation이 확인되었다. 모든 언어가 `tokens_per_word >= 2.0` 기준의 bottleneck에 걸렸고, 일부 Latin-script 언어와 Syriac은 single-character token 비율도 높았다. 가장 심한 언어는 Syriac으로, 평균 `tokens_per_word=4.854`, `single_char_token_pct=74.251%`였다.

## Metrics Table

| ISO | Language | Script | Sentences | Avg words | Avg tokens | Tokens/word | Single-char token % | `<unk>` % | P95 seq len | Bottleneck |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| acu | Achuar-Shiwiar | Latin | 500 | 22.604 | 65.354 | 2.891 | 21.504 | 0.000 | 128 | high tokens/word |
| ake | Akawaio | Latin | 500 | 23.604 | 78.144 | 3.311 | 60.238 | 0.000 | 135 | high tokens/word + high single-char |
| bsn | Barasana-Eduria | Latin | 500 | 30.008 | 105.626 | 3.520 | 39.333 | 0.000 | 221 | high tokens/word + high single-char |
| chr | Cherokee | Cherokee | 500 | 13.176 | 29.684 | 2.253 | 11.252 | 0.000 | 53 | high tokens/word |
| cop | Coptic | Coptic | 500 | 14.942 | 30.876 | 2.066 | 3.265 | 0.000 | 51 | high tokens/word |
| kbh | Camsa | Latin | 500 | 27.980 | 99.730 | 3.564 | 30.394 | 0.000 | 147 | high tokens/word + high single-char |
| nhg | Nahuatl (Tetelcingo) | Latin | 500 | 22.450 | 66.068 | 2.943 | 24.075 | 0.000 | 119 | high tokens/word |
| oji | Ojibwa | Aboriginal Syllabics | 500 | 17.582 | 37.122 | 2.111 | 6.104 | 0.000 | 65 | high tokens/word |
| syr | Syriac | Syriac | 500 | 13.038 | 63.280 | 4.854 | 74.251 | 0.000 | 107 | high tokens/word + high single-char |
| usp | Uspanteco | Latin | 500 | 27.608 | 69.074 | 2.502 | 37.852 | 0.000 | 126 | high tokens/word + high single-char |

## How To Read The Bottleneck Labels

`high tokens/word` means a word is split into too many tokens on average. In this audit, the threshold is `tokens_per_word >= 2.0`.

`high single-char` means many produced tokens are only one character long. In this audit, the threshold is `single_char_token_pct >= 25.0`.

`high tokens/word + high single-char` means both conditions hold: words are heavily split, and much of the split is character-level rather than meaningful subword-level.

`<unk> % = 0` in this audit means no visible token string was equal to `<unk>` in `tokenizer.tokenize(...)`. It does not guarantee that every displayed surface token maps to a real non-unk vocabulary id. For scripts such as Coptic, XLM-R can display surface-looking unknown pieces, but those pieces may still map to the `<unk>` id when converted to ids. Therefore `<unk>` should be treated as an audit caveat here; the main reliable signal in this table is fragmentation, especially `tokens_per_word` and `single_char_token_pct`.

## Representative Samples

### Syriac: strongest fragmentation

- Verse: `b.MAT.5.4`
- Words/chars/tokens: `4 / 25 / 28`
- Tokens per word: `7.000`
- Single-character token %: `82.143`

Text:

> ܛܘܒܝܗܘܢ ܠܐܒܝܠܐ ܕܗܢܘܢ ܢܬܒܝܐܘܢ

Token preview:

```text
▁ ܛ ܘ ܒ ܝ ܗ ܘ ܢ ▁ ܠ ܐ ܒ ܝ ܠ ܐ ▁ ܕ ܗܢ ܘ ܢ ▁ ܢ ܬ ܒ ܝ ܐ ܘ ܢ
```

Interpretation: Syriac 단어가 의미 있는 subword보다 개별 문자 단위로 거의 풀려서, sequence length가 단어 수 대비 비정상적으로 길어진다.

### Akawaio: Latin script with many character splits

- Verse: `b.MAT.5.43`
- Words/chars/tokens: `6 / 59 / 40`
- Tokens per word: `6.667`
- Single-character token %: `62.500`

Text:

> “Eta'pʉ auya'nokon; ‘Ɨtonpa i'nʉnkakɨ, ɨyeyaton ewaruma'tɨi'ma.’

Token preview:

```text
▁“ E ta ' p ʉ ▁au ya ' no kon ; ▁‘ Ɨ ton pa ▁i ' n ʉ n kak ɨ , ▁ ɨ ye ya ton ▁e war uma ' t ɨ i ' ma . ’
```

Interpretation: Latin 기반 문자라도 apostrophe, 특수 모음, low-resource orthography가 섞이면 XLM-R vocabulary가 안정적인 subword를 만들지 못하고 문자 단위로 쪼갠다.

### Barasana-Eduria: long Latin-script verses become very long token sequences

- Verse: `b.MAT.12.20`
- Words/chars/tokens: `19 / 173 / 99`
- Tokens per word: `5.211`
- Single-character token %: `46.465`

Text:

> Yu̶re quẽnaro ajitirũ̶nu̶menare, yu̶ bojarore bajiro yimasibeticõari, tu̶oĩasu̶tiritirãre quẽne mairu̶cu̶mi. Ĩnare ĩamaicõari, ‘Quẽnaro yu̶re ajitirũ̶nu̶ato ĩna’ yigu̶, ĩnare ejarẽmoru̶cu̶mi.

Token preview:

```text
▁Yu ̶ re ▁qu ẽ na ro ▁a ji tir ũ ̶ nu ̶ men are , ▁y u ̶ ▁boja rore ▁baj iro ▁y imas ibe tic õ ari , ...
```

Interpretation: combining marks and uncommon orthographic units are split into separate tokens, so long verses quickly approach high sequence lengths.

### Camsa: diacritics and complex morphology

- Verse: `b.MAT.10.17`
- Words/chars/tokens: `14 / 161 / 78`
- Tokens per word: `5.571`
- Single-character token %: `28.205`

Text:

> Ents̈angbiama cuedado s̈mochtsebomna, chëngbe pueblents̈a amë́ndayëngbe cucuats̈iñe ts̈ëngaftanga cmochanjábashejuana y chëngbe enefjuana yebnënguenache cmochanjátsets̈enaye.

Token preview:

```text
▁Ent s ̈ ang bia ma ▁cu ed ado ▁s ̈ m ocht se bom na , ▁ch ën g be ▁pu e ble nts ̈ a ...
```

Interpretation: Camsa도 많은 단어가 짧은 조각과 combining mark로 분해되어, Latin script라는 사실만으로 XLM-R tokenization이 안정적이라고 보기 어렵다.

### Coptic: mild token-count bottleneck, not catastrophic

- Verse: `b.MAT.7.1`
- Words/chars/tokens: `4 / 31 / 9`
- Tokens per word: `2.250`
- Single-character token %: `11.111`

Text:

> ⲘⲠⲈⲢϮϨⲀⲠ ϨⲒⲚⲀ ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ ⲈⲢⲰⲦⲈⲚ.

Token preview:

```text
▁ ⲘⲠⲈⲢϮϨⲀⲠ ▁ ϨⲒⲚⲀ ▁ ⲚⲦⲞⲨϢⲦⲈⲘϮϨⲀⲠ ▁ ⲈⲢⲰⲦⲈⲚ .
```

Interpretation: Coptic은 Syriac처럼 문자 단위로 완전히 붕괴되지는 않는다. 평균 `tokens_per_word=2.066`이라 token-count bottleneck은 있지만, `single_char_token_pct=3.265%`라 surface-token 기준으로는 mild/moderate case처럼 보인다. 다만 Coptic surface token이 실제 vocab id로는 `<unk>`에 매핑될 수 있으므로, Coptic은 token string preview와 id-level coverage를 구분해서 해석해야 한다.

## Takeaway

Step02의 핵심은 “모든 target10 언어가 XLM-R 기준으로 일정 수준 이상의 fragmentation을 보인다”는 점이다. 특히 Syriac은 평균과 sample 모두에서 character-level 붕괴가 뚜렷하므로, 다음 단계의 vocabulary extension 실험을 정당화하는 가장 강한 근거가 된다.
