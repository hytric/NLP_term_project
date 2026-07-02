# Glot500 vs Target10-Merged Tokenization Examples

작성일: 2026-06-05

같은 target10 Bible train 문장을 기존 Glot500 tokenizer와 vocab extension 후 `glot500_target10` tokenizer로 나란히 비교한다.
각 언어별로 첫 500개 train 문장 중 tokens/word 감소가 큰 예시 5개를 선택했다.

## Coptic (cop)

### Example 1

- verse_id: `b.1CO.14.32`
- words: 3
- Glot500 tokens: 36 (12.000 tokens/word)
- Glot500+target10 tokens: 10 (3.333 tokens/word)
- token reduction: 72.2%
- text: `ⲚⲒⲠⲚⲈⲨⲘⲀⲚⲦⲈⲚⲒⲠⲢⲞⲪⲎⲦⲎⲤ ϢⲀⲨϬⲚⲈϪⲰⲞⲨ ⲚⲚⲒⲠⲢⲞⲪⲎⲦⲎⲤ.`

Glot500 tokens:

```text
▁ ⲚⲒ Ⲡ Ⲛ Ⲉ Ⲩ Ⲙ ⲀⲚ Ⲧ Ⲉ ⲚⲒ Ⲡ Ⲣ ⲞⲪ Ⲏ Ⲧ Ⲏ Ⲥ ▁ Ϣ ⲀⲨ Ϭ Ⲛ Ⲉ Ϫ ⲰⲞⲨ ▁ ⲚⲚⲒ Ⲡ Ⲣ ⲞⲪ Ⲏ Ⲧ Ⲏ Ⲥ .
```

Glot500+target10 tokens:

```text
▁ⲚⲒ ⲠⲚⲈⲨⲘⲀⲚ ⲦⲈⲚ Ⲓ ⲠⲢⲞⲪⲎⲦⲎⲤ ▁ϢⲀⲨ ϬⲚⲈϪⲰⲞⲨ ▁ⲚⲚⲒ ⲠⲢⲞⲪⲎⲦⲎⲤ .
```

### Example 2

- verse_id: `b.1CO.8.12`
- words: 10
- Glot500 tokens: 82 (8.200 tokens/word)
- Glot500+target10 tokens: 20 (2.000 tokens/word)
- token reduction: 75.6%
- text: `ⲠⲀⲒⲢⲎϮ ⲆⲈ ⲈⲢⲈⲦⲈⲚⲈⲢⲚⲞⲂⲒ ⲈⲚⲒⲤⲚⲎⲞⲨ ⲞⲨⲞϨ ⲈⲢⲈⲦⲈⲚⲘⲒϢⲒ ⲈⲦⲞⲨⲤⲨⲚⲎⲆⲈⲤⲒⲤ ⲈⲦϢⲰⲚⲒ ⲀⲢⲈⲦⲈⲚⲈⲢⲚⲞⲂⲒ ⲈⲠⲬⲢⲒⲤⲦⲞⲤ.`

Glot500 tokens:

```text
▁ Ⲡ ⲀⲒ Ⲣ Ⲏ Ϯ ▁ Ⲇ Ⲉ ▁ Ⲉ Ⲣ Ⲉ Ⲧ Ⲉ Ⲛ Ⲉ Ⲣ ⲚⲞ Ⲃ Ⲓ ▁ Ⲉ ⲚⲒ Ⲥ Ⲛ Ⲏ ⲞⲨ ▁ ⲞⲨⲞ Ϩ ▁ Ⲉ Ⲣ Ⲉ Ⲧ Ⲉ Ⲛ Ⲙ Ⲓ Ϣ Ⲓ ▁ Ⲉ Ⲧ ⲞⲨ Ⲥ ⲨⲚ Ⲏ Ⲇ Ⲉ Ⲥ Ⲓ Ⲥ ▁ Ⲉ Ⲧ Ϣ ⲰⲚⲒ ▁ Ⲁ Ⲣ Ⲉ Ⲧ Ⲉ Ⲛ Ⲉ Ⲣ ⲚⲞ Ⲃ Ⲓ ▁ Ⲉ Ⲡ Ⲭ Ⲣ Ⲓ Ⲥ Ⲧ Ⲟ Ⲥ .
```

Glot500+target10 tokens:

```text
▁ ⲠⲀⲒⲢⲎϮ ▁ⲆⲈ ▁ⲈⲢⲈⲦⲈⲚ ⲈⲢⲚⲞⲂⲒ ▁ⲈⲚⲒ ⲤⲚⲎⲞⲨ ▁ⲞⲨⲞϨ ▁ⲈⲢⲈⲦⲈⲚ ⲘⲒ ϢⲒ ▁ⲈⲦⲞⲨ ⲤⲨⲚⲎⲆⲈⲤⲒⲤ ▁ⲈⲦ ϢⲰⲚⲒ ▁ⲀⲢⲈⲦⲈⲚ ⲈⲢⲚⲞⲂⲒ ▁Ⲉ ⲠⲬⲢⲒⲤⲦⲞⲤ .
```

### Example 3

- verse_id: `b.1CO.16.23`
- words: 5
- Glot500 tokens: 38 (7.600 tokens/word)
- Glot500+target10 tokens: 8 (1.600 tokens/word)
- token reduction: 78.9%
- text: `ⲠϨⲘⲞⲦ ⲘⲠⲈⲚϬⲞⲒⲤ ⲒⲎⲤⲞⲨⲤ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲚⲈⲘⲰⲦⲈⲚ.`

Glot500 tokens:

```text
▁ Ⲡ Ϩ Ⲙ Ⲟ Ⲧ ▁ Ⲙ Ⲡ Ⲉ Ⲛ Ϭ ⲞⲒ Ⲥ ▁ Ⲓ Ⲏ Ⲥ ⲞⲨ Ⲥ ▁ Ⲡ Ⲭ Ⲣ Ⲓ Ⲥ Ⲧ Ⲟ Ⲥ ▁ Ⲛ Ⲉ Ⲙ Ⲱ Ⲧ Ⲉ Ⲛ .
```

Glot500+target10 tokens:

```text
▁ ⲠϨⲘⲞⲦ ▁Ⲙ ⲠⲈⲚϬⲞⲒⲤ ▁ⲒⲎⲤⲞⲨⲤ ▁ⲠⲬⲢⲒⲤⲦⲞⲤ ▁ⲚⲈⲘⲰⲦⲈⲚ .
```

### Example 4

- verse_id: `b.1CO.16.24`
- words: 6
- Glot500 tokens: 41 (6.833 tokens/word)
- Glot500+target10 tokens: 7 (1.167 tokens/word)
- token reduction: 82.9%
- text: `ⲦⲀⲀⲄⲀⲠⲎ ⲚⲈⲘⲰⲦⲈⲚ ⲦⲎⲢⲞⲨ ϦⲈⲚⲠⲬⲢⲒⲤⲦⲞⲤ ⲒⲎⲤⲞⲨⲤ ⲀⲘⲎⲚ`

Glot500 tokens:

```text
▁ Ⲧ ⲀⲀⲄⲀ Ⲡ Ⲏ ▁ Ⲛ Ⲉ Ⲙ Ⲱ Ⲧ Ⲉ Ⲛ ▁ Ⲧ Ⲏ Ⲣ ⲞⲨ ▁ Ϧ Ⲉ Ⲛ Ⲡ Ⲭ Ⲣ Ⲓ Ⲥ Ⲧ Ⲟ Ⲥ ▁ Ⲓ Ⲏ Ⲥ ⲞⲨ Ⲥ ▁ Ⲁ Ⲙ Ⲏ Ⲛ
```

Glot500+target10 tokens:

```text
▁ⲦⲀ ⲀⲄⲀⲠⲎ ▁ⲚⲈⲘⲰⲦⲈⲚ ▁ⲦⲎⲢⲞⲨ ▁ϦⲈⲚⲠⲬⲢⲒⲤⲦⲞⲤ ▁ⲒⲎⲤⲞⲨⲤ ▁ⲀⲘⲎⲚ
```

### Example 5

- verse_id: `b.1CO.1.9`
- words: 11
- Glot500 tokens: 77 (7.000 tokens/word)
- Glot500+target10 tokens: 16 (1.455 tokens/word)
- token reduction: 79.2%
- text: `ϤⲈⲚϨⲞⲦ ⲚϪⲈⲪⲚⲞⲨϮ ⲪⲎ ⲈⲦⲀϤⲐⲀϨⲈⲘ ⲐⲎⲚⲞⲨ ⲈϦⲞⲨⲚ ⲈϮⲘⲈⲦϢⲪⲎⲢ ⲚⲦⲈⲠⲈϤϢⲎⲢⲒ ⲒⲎⲤⲞⲨⲤ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲠⲈⲚϬⲞⲒⲤ.`

Glot500 tokens:

```text
▁ Ϥ Ⲉ Ⲛ Ϩ Ⲟ Ⲧ ▁ Ⲛ Ϫ Ⲉ ⲪⲚⲞⲨ Ϯ ▁ Ⲫ Ⲏ ▁ Ⲉ Ⲧ Ⲁ Ϥ ⲐⲀ Ϩ Ⲉ Ⲙ ▁ Ⲑ Ⲏ ⲚⲞⲨ ▁ Ⲉ Ϧ ⲞⲨⲚ ▁ Ⲉ Ϯ Ⲙ Ⲉ Ⲧ Ϣ Ⲫ Ⲏ Ⲣ ▁ Ⲛ Ⲧ Ⲉ Ⲡ Ⲉ Ϥ Ϣ Ⲏ Ⲣ Ⲓ ▁ Ⲓ Ⲏ Ⲥ ⲞⲨ Ⲥ ▁ Ⲡ Ⲭ Ⲣ Ⲓ Ⲥ Ⲧ Ⲟ Ⲥ ▁ Ⲡ Ⲉ Ⲛ Ϭ ⲞⲒ Ⲥ .
```

Glot500+target10 tokens:

```text
▁ ϤⲈⲚϨⲞⲦ ▁ⲚϪⲈⲪⲚⲞⲨϮ ▁ⲪⲎ ▁ⲈⲦⲀϤ ⲐⲀϨⲈⲘ ▁ⲐⲎⲚⲞⲨ ▁ⲈϦⲞⲨⲚ ▁ⲈϮ ⲘⲈⲦϢⲪⲎⲢ ▁ⲚⲦⲈⲠⲈϤ ϢⲎⲢⲒ ▁ⲒⲎⲤⲞⲨⲤ ▁ⲠⲬⲢⲒⲤⲦⲞⲤ ▁ⲠⲈⲚϬⲞⲒⲤ .
```

## Syriac (syr)

### Example 1

- verse_id: `b.1CO.16.14`
- words: 4
- Glot500 tokens: 27 (6.750 tokens/word)
- Glot500+target10 tokens: 6 (1.500 tokens/word)
- token reduction: 77.8%
- text: `ܘܟܠܗܝܢ ܨܒܘܬܟܘܢ ܒܚܘܒܐ ܢܗܘܝܢ`

Glot500 tokens:

```text
▁ ܘ ܟ ܠ ܗ ܝ ܢ ▁ ܨ ܒ ܘ ܬ ܟ ܘ ܢ ▁ ܒ ܚ ܘ ܒ ܐ ▁ ܢ ܗ ܘ ܝ ܢ
```

Glot500+target10 tokens:

```text
▁ܘܟܠܗ ܝܢ ▁ܨܒܘ ܬܟܘܢ ▁ܒܚܘܒܐ ▁ܢܗܘܝܢ
```

### Example 2

- verse_id: `b.1CO.3.23`
- words: 4
- Glot500 tokens: 27 (6.750 tokens/word)
- Glot500+target10 tokens: 6 (1.500 tokens/word)
- token reduction: 77.8%
- text: `ܘܐܢܬܘܢ ܕܡܫܝܚܐ ܘܡܫܝܚܐ ܕܐܠܗܐ`

Glot500 tokens:

```text
▁ ܘ ܐ ܢ ܬ ܘ ܢ ▁ ܕ ܡ ܫ ܝ ܚ ܐ ▁ ܘ ܡ ܫ ܝ ܚ ܐ ▁ ܕ ܐ ܠ ܗ ܐ
```

Glot500+target10 tokens:

```text
▁ܘܐܢ ܬܘܢ ▁ܕܡܫܝܚܐ ▁ܘ ܡܫܝܚܐ ▁ܕܐܠܗܐ
```

### Example 3

- verse_id: `b.1JO.3.22`
- words: 10
- Glot500 tokens: 69 (6.900 tokens/word)
- Glot500+target10 tokens: 19 (1.900 tokens/word)
- token reduction: 72.5%
- text: `ܘܟܠܡܕܡ ܕܫܐܠܝܢܢ ܢܤܒܝܢܢ ܡܢܗ ܡܛܠ ܕܢܛܪܝܢܢ ܦܘܩܕܢܘܗܝ ܘܫܦܝܪܬܐ ܤܥܪܝܢܢ ܩܕܡܘܗܝ`

Glot500 tokens:

```text
▁ ܘ ܟ ܠ ܡ ܕ ܡ ▁ ܕ ܫ ܐ ܠ ܝ ܢ ܢ ▁ ܢ ܤ ܒ ܝ ܢ ܢ ▁ ܡ ܢ ܗ ▁ ܡ ܛ ܠ ▁ ܕ ܢ ܛ ܪ ܝ ܢ ܢ ▁ ܦ ܘ ܩ ܕ ܢ ܘ ܗ ܝ ▁ ܘ ܫ ܦ ܝ ܪ ܬ ܐ ▁ ܤ ܥ ܪ ܝ ܢ ܢ ▁ ܩ ܕ ܡ ܘ ܗ ܝ
```

Glot500+target10 tokens:

```text
▁ܘ ܟܠܡܕܡ ▁ܕ ܫܐܠܝܢ ܢ ▁ܢܤܒ ܝܢܢ ▁ܡܢܗ ▁ܡܛܠ ▁ܕܢ ܛܪ ܝܢܢ ▁ ܦܘܩܕܢܘܗܝ ▁ܘ ܫܦܝܪܬܐ ▁ܤܥܪ ܝܢܢ ▁ܩܕܡܘܗܝ
```

### Example 4

- verse_id: `b.1CO.6.20`
- words: 12
- Glot500 tokens: 81 (6.750 tokens/word)
- Glot500+target10 tokens: 22 (1.833 tokens/word)
- token reduction: 72.8%
- text: `ܐܙܕܒܢܬܘܢ ܓܝܪ ܒܕܡܝܐ ܗܘܝܬܘܢ ܗܟܝܠ ܡܫܒܚܝܢ ܠܐܠܗܐ ܒܦܓܪܟܘܢ ܘܒܪܘܚܟܘܢ ܗܢܘܢ ܕܐܝܬܝܗܘܢ ܕܐܠܗܐ`

Glot500 tokens:

```text
▁ ܐ ܙ ܕ ܒ ܢ ܬ ܘ ܢ ▁ ܓ ܝ ܪ ▁ ܒ ܕ ܡ ܝ ܐ ▁ ܗ ܘ ܝ ܬ ܘ ܢ ▁ ܗ ܟ ܝ ܠ ▁ ܡ ܫ ܒ ܚ ܝ ܢ ▁ ܠ ܐ ܠ ܗ ܐ ▁ ܒ ܦ ܓ ܪ ܟ ܘ ܢ ▁ ܘ ܒ ܪ ܘ ܚ ܟ ܘ ܢ ▁ ܗ ܢ ܘ ܢ ▁ ܕ ܐ ܝ ܬ ܝ ܗ ܘ ܢ ▁ ܕ ܐ ܠ ܗ ܐ
```

Glot500+target10 tokens:

```text
▁ܐ ܙܕܒܢ ܬܘܢ ▁ܓܝܪ ▁ܒ ܕܡ ܝܐ ▁ܗܘܝܬܘܢ ▁ܗ ܟܝܠ ▁ ܡܫܒܚܝܢ ▁ܠܐܠܗܐ ▁ܒܦܓܪ ܟܘܢ ▁ܘܒܪ ܘ ܚ ܟܘܢ ▁ܗܢܘܢ ▁ܕܐܝܬܝܗܘܢ ▁ܕܐܠܗܐ
```

### Example 5

- verse_id: `b.1CO.2.5`
- words: 8
- Glot500 tokens: 50 (6.250 tokens/word)
- Glot500+target10 tokens: 11 (1.375 tokens/word)
- token reduction: 78.0%
- text: `ܕܠܐ ܬܗܘܐ ܗܝܡܢܘܬܟܘܢ ܒܚܟܡܬܐ ܕܒܢܝܢܫܐ ܐܠܐ ܒܚܝܠܐ ܕܐܠܗܐ`

Glot500 tokens:

```text
▁ ܕ ܠ ܐ ▁ ܬ ܗ ܘ ܐ ▁ ܗ ܝ ܡ ܢ ܘ ܬ ܟ ܘ ܢ ▁ ܒ ܚ ܟ ܡ ܬ ܐ ▁ ܕ ܒ ܢ ܝ ܢ ܫ ܐ ▁ ܐ ܠ ܐ ▁ ܒ ܚ ܝ ܠ ܐ ▁ ܕ ܐ ܠ ܗ ܐ
```

Glot500+target10 tokens:

```text
▁ܕܠܐ ▁ܬܗܘܐ ▁ܗܝܡܢܘܬܟܘܢ ▁ ܒܚܟܡܬ ܐ ▁ܕܒܢܝܢܫܐ ▁ܐ ܠܐ ▁ܒܚܝܠܐ ▁ܕܐܠܗܐ
```
