# v5 Tokenization Example Analysis

This file compares `xlm-roberta-base` with the selected v5 tokenizer at sentence level.

- target tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm`
- manifest: `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`

## Summary

| Language | Examples | Base TPW | v5 TPW | Delta TPW | Worse | Better | Same | v5 New Tokens | v5 Byte Tokens | v5 UNK Tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dzo_Tibt | 500 | 4.493663 | 5.609507 | 1.115844 | 330 | 131 | 39 | 9140 | 0 | 0 |

## Worst Regressions

### 1. dzo_Tibt example 6

- words: `13`
- base tokens: `134`
- v5 tokens: `348`
- delta tokens/word: `16.461538`
- v5 byte tokens: `0`
- v5 newly appended tokens: `344`
- text preview: `དེ་ཡང་སྔོན་རྒྱ་གར་དུ་སྙན་ངག་གི་བསྟན་བཅོས་བྷ་ར་ཏ་ཞེས་བྱ་བ་ཞིག་བརྩམས་པ་ཚོགས་བདག་གིས་ཡིན་མཁན་བྱས་ནས་བྲིས་པར་གྲགས་པའི་གཞུང་ཤོ་ལོ་ཀ་འབུམ་ལྷག་ཡོད་པ་དང༌། དྲང་སྲོང་མེ་བཞིན་འཇུག་གི་བུ་མོ...`

Base token preview:

```text
▁ དེ་ཡང་སྔ ོ ན་རྒྱ་གར་དུ་སྙན་ངག་གི་བསྟན་བཅ ོ ས་བྷ་ར་ཏ་ཞེས་བྱ་བ་ཞིག་བརྩམས་པ་ཚ ོ གས་བདག་གིས་ཡིན་མཁན་བྱས་ནས་བྲིས་པར་གྲགས་པའི་གཞུང་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ལྷག་ཡ ོ ད་པ་དང་། ▁ དྲང་སྲ ོ ང་མེ་བཞིན་འཇུག་གི་བུ་མ ོ ས་སྙན་ངག་རཱ་མ་ཡ་ན་ཞེས་པ་ཞིག་བརྩམས་པ་དེ་ནི་རྒྱལ་པ ོ ་རཱ་མ་ན་དང་དེའི་བཙུན་པ ོ ་ར ོ ལ་རྙེད་མའི་ལ ོ ་རྒྱུས་སྙན་ངག་ཏུ་སྦྱར་བ་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ཡ ོ ད་པ་ཞིག་དང་། ▁ མརྐེ་ཎ་ཊ་ཡིས་བརྩམས་པའི་སྙན་ངག་གི་བསྟན་བཅ ོ ས་ཁྱབ་འཇུག་གི་འཇུག་པ་བཅུ་ས ོ གས་གཙ ོ ་བ ོ ར་སྟ ོ ན་པ་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ལྷག་ཡ ོ ད་པ་ཞིག་དང་། ▁ རཱ་མ་ཤརྨས་མཛད་པའི་སྙན་ངག་གི་བསྟན་བཅ ོ ས་ཤ ོ ་ལ ོ ་ ཀ ་སྟ ོ ང་ཕྲག་བརྒྱད་ཅུ་ཅན་དང་། ▁ ནག་མ ོ ་ཁ ོ ལ་གྱིས་མཛད་པའི་སྙན་ངག་གཞ ོ ན་ནུ་འབྱུང་བ་དང་། ▁ གཞན་སྙན་ངག་གི་བསྟན་བཅ
```

v5 token preview:

```text
▁དེ་ཡང་ སྔོན་ རྒྱ་གར་ དུ་ སྙན་ ངག་ གི་ བསྟན་ བཅོས་ བ ྷ ་ ར་ ཏ་ ཞེས་ བྱ་བ་ ཞི ག་ བརྩ མས་ པ་ ཚོགས་ བདག་ གིས་ ཡིན་ མཁན་ བྱ ས་ ནས་ བྲིས་ པར་ གྲགས་ པའི་ གཞུང་ ཤོ ་ ལོ་ ཀ་ འབུ མ་ ལྷག་ ཡོད་ པ་དང་ ། ▁དྲ ང་ སྲ ོང་ མེ་ བཞིན་ འཇ ུག་ གི་ བུ་ མོ ས་ སྙན་ ངག་ ར ཱ་ མ་ཡ ་ན་ ཞེས་ པ་ ཞི ག་ བརྩ མས་ པ་ དེ་ ནི་ རྒྱལ་པོ་ ར ཱ་ མ་ ན་དང་ དེའི་ བཙ ུན་ པོ་
```

### 2. dzo_Tibt example 39

- words: `1`
- base tokens: `6`
- v5 tokens: `16`
- delta tokens/word: `10.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `16`
- text preview: `སེལ་འཐུ་འབད་ཡོད་པའི་སེམ་མཉམ་ཐིག་གི་གྲུ་ཟུར་དེ་བསྒྱུར་བཆཅོས་འབད།`

Base token preview:

```text
▁ སེལ་འཐུ་འབད་ཡ ོ ད་པའི་སེམ་མཉམ་ཐིག་གི་གྲུ་ཟུར་དེ་བསྒྱུར་བཆཅ ོ ས་འབད།
```

v5 token preview:

```text
▁སེལ་འཐུ་འབད་ ཡོད་པའི་ སེ མ་ མཉམ་ ཐིག་ གི་ གྲུ་ ཟུར་ དེ་ བསྒྱུར་ བ ཆ ཅོ ས་ འབད།
```

### 3. dzo_Tibt example 175

- words: `1`
- base tokens: `4`
- v5 tokens: `14`
- delta tokens/word: `10.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `14`
- text preview: `རང་རང་སའི་དམིགས་གཏད་གུ་ཁོང་རའི་དབྱིབས་ཚུ་འདྲུད་ནི་དང་བཞག་`

Base token preview:

```text
▁ རང་རང་སའི་དམིགས་གཏད་གུ་ཁ ོ ང་རའི་དབྱིབས་ཚུ་འདྲུད་ནི་དང་བཞག་
```

v5 token preview:

```text
▁རང་ རང་ སའི་ དམིགས་གཏད་ གུ་ ཁོང་ ར འི་ དབྱིབས་ ཚུ་ འདྲ ུད་ ནི་དང་ བཞག་
```

### 4. dzo_Tibt example 390

- words: `1`
- base tokens: `4`
- v5 tokens: `14`
- delta tokens/word: `10.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `13`
- text preview: `ཐུམ་སྒྲིལ་རྒྱ་བསྐྱེད་ཐོག་ཡིག་འདི་གནམ་མེད་ས་མེད་རིངམ་འདུག`

Base token preview:

```text
▁ ཐུམ་སྒྲིལ་རྒྱ་བསྐྱེད་ཐ ོ ག་ཡིག་འདི་གནམ་མེད་ས་མེད་རིངམ་འདུག
```

v5 token preview:

```text
▁ ཐུམ་སྒྲིལ་ རྒྱ་ བསྐྱེད་ ཐོག་ ཡིག་ འདི་ གནམ་ མེད་ ས་ མེད་ རིང མ་ འདུག
```

### 5. dzo_Tibt example 311

- words: `1`
- base tokens: `6`
- v5 tokens: `15`
- delta tokens/word: `9.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `15`
- text preview: `ཨེབ་རྟགས་ནང་པོཔ་ཨཔས་ཁ་ཕྱེ་ནི་ཚབ་ལུ་ཝིན་ཌོ་གསརཔ་ཚུ་ཁ་ཕྱེ།`

Base token preview:

```text
▁ ཨེབ་རྟགས་ནང་པ ོ པ་ཨཔས་ཁ་ཕྱེ་ནི་ཚབ་ལུ་ཝིན་ཌ ོ ་གསརཔ་ཚུ་ཁ་ཕྱེ།
```

v5 token preview:

```text
▁ཨེབ་ རྟགས་ ནང་ པོ པ་ ཨ པ ས་ ཁ་ཕྱེ་ ནི་ ཚབ་ལུ་ ཝིན་ཌོ་ གསརཔ་ ཚུ་ ཁ་ཕྱེ།
```

### 6. dzo_Tibt example 150

- words: `5`
- base tokens: `24`
- v5 tokens: `67`
- delta tokens/word: `8.600000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `65`
- text preview: `ཤར་ནས་ནུབ་ཏུ་ཟུག་པའི་རི་ཕྲན་དག་ནི་ས་དམར་ཡིན། གཞུང་ཆུའི་གཡས་གཡོན་གྱི་གཞོང་དང་རི་ཕྲན་དག་གི་བར་གསེང་ན་རྡོ་སྦིས་དུ་ཁ་སྟོང་། སྡེ་བ་ཉེར་གསུམ། མི་གྲངས་གཅིག་ཁྲི་ཉིས་སྟོང་ཙམ། སྟོད་སྨད་བར...`

Base token preview:

```text
▁ ཤར་ནས་ནུབ་ཏུ་ཟུག་པའི་རི་ཕྲན་དག་ནི་ས་དམར་ཡིན། ▁ གཞུང་ཆུའི་གཡས་གཡ ོ ན་གྱི་གཞ ོ ང་དང་རི་ཕྲན་དག་གི་བར་གསེང་ན་རྡ ོ ་སྦིས་དུ་ཁ་སྟ ོ ང་། ▁ སྡེ་བ་ཉེར་གསུམ། ▁ མི་གྲངས་གཅིག་ཁྲི་ཉིས་སྟ ོ ང་ཙམ། ▁ སྟ ོ ད་སྨད་བར་གསུམ་དུ་གནས་ཡ ོ ད།
```

v5 token preview:

```text
▁ ཤར་ ནས་ ནུབ་ ཏུ ་ཟ ུག་ པའི་ རི་ ཕྲན་ དག་ ནི་ ས་ དམ ར་ ཡིན ། ▁གཞུང་ ཆུ འི་ གཡས་ གཡོན་ གྱི་ གཞ ོང་ དང་ རི་ ཕྲན་ དག་ གི་ བར་ ག སེང་ ན་ རྡོ་ སྦ ིས་ དུ་ ཁ་ སྟོང་ ། ▁ སྡེ་ བ་ ཉེ ར་ གས ུ མ། ▁མི་ གྲངས་ གཅིག་ ཁྲི་ ཉི ས་ སྟོང་ ཙ མ། ▁སྟ ོད་ སྨ ད་ བར་ གསུམ་ དུ་ གནས་ ཡོད།
```

### 7. dzo_Tibt example 1

- words: `1`
- base tokens: `10`
- v5 tokens: `18`
- delta tokens/word: `8.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `18`
- text preview: `དང་པ་ཕས་རྒོལ་ཟིལ་གྱིས་གནོན་ཏེ་ཞི་བདེའི་གོ་སྐབས་བཟོ་གནང་བ།`

Base token preview:

```text
▁ དང་པ་ཕས་རྒ ོ ལ་ཟིལ་གྱིས་གན ོ ན་ཏེ་ཞི་བདེའི་ག ོ ་སྐབས་བཟ ོ ་གནང་བ།
```

v5 token preview:

```text
▁དང་པ་ ཕ ས་ རྒ ོལ་ ཟི ལ་ གྱིས་ ག ནོ ན་ ཏེ་ ཞི་བ དེའི་ གོ་སྐབས་ བཟོ་ གནང་ བ།
```

### 8. dzo_Tibt example 346

- words: `1`
- base tokens: `3`
- v5 tokens: `11`
- delta tokens/word: `8.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `10`
- text preview: `དཔེ་ཚད་བིཊི་མེཔསི་གི་ལྟག་ལུ:`

Base token preview:

```text
▁ དཔེ་ཚད་བིཊི་མེཔསི་གི་ལྟག་ལུ :
```

v5 token preview:

```text
▁དཔེ་ ཚད་ བ ིཊི་ མེ པ སི་གི་ ལྟ ག་ ལུ :
```


## Best Improvements

### 1. dzo_Tibt example 369

- words: `1`
- base tokens: `10`
- v5 tokens: `3`
- delta tokens/word: `-7.000000`
- v5 newly appended tokens: `3`
- text preview: `ཆོག་ཡིག་དགོས་མཁོ་ཡོདཔ།`

Base token preview:

```text
▁ ཆ ོ ག་ཡིག་དག ོ ས་མཁ ོ ་ཡ ོ དཔ།
```

v5 token preview:

```text
▁ཆོག་ཡིག་ དགོས་མཁོ་ ཡོདཔ།
```

### 2. dzo_Tibt example 14

- words: `1`
- base tokens: `12`
- v5 tokens: `7`
- delta tokens/word: `-5.000000`
- v5 newly appended tokens: `5`
- text preview: `རྩེདམོ་ལོག་འགོ་བཙུགས།(_R)`

Base token preview:

```text
▁ རྩེདམ ོ ་ལ ོ ག་འག ོ ་བཙུགས། ( _ R )
```

v5 token preview:

```text
▁རྩེདམོ་ ལོག་ འགོ་བཙུགས ། (_ R )
```

### 3. dzo_Tibt example 288

- words: `1`
- base tokens: `13`
- v5 tokens: `8`
- delta tokens/word: `-5.000000`
- v5 newly appended tokens: `6`
- text preview: `འོད་རྟགས་ལུ་གཡོག་བཀོལ།(_R)`

Base token preview:

```text
▁ འ ོ ད་རྟགས་ལུ་གཡ ོ ག་བ ཀ ོ ལ། ( _ R )
```

v5 token preview:

```text
▁འོད་ རྟགས་ ལུ་ གཡོག་བཀོལ ། (_ R )
```

### 4. dzo_Tibt example 422

- words: `1`
- base tokens: `19`
- v5 tokens: `14`
- delta tokens/word: `-5.000000`
- v5 newly appended tokens: `11`
- text preview: `ས་ཁོངས་%s་ཀྱི་ཀུཀི་གཅིག་གཞི་སྒྲིག་འབད་ནིའི་དགོས་འདོད་ཡོད།`

Base token preview:

```text
▁ ས་ཁ ོ ངས་ % s ་ ཀ ྱི་ ཀ ུ ཀ ི་གཅིག་གཞི་སྒྲིག་འབད་ནིའི་དག ོ ས་འད ོ ད་ཡ ོ ད།
```

v5 token preview:

```text
▁ ས་ཁོངས་ % s ་ ཀྱི་ ཀུ ཀི་ གཅིག་ གཞི་སྒྲིག་ འབད་ནིའི་ དགོས་ འདོད་ ཡོད།
```

### 5. dzo_Tibt example 159

- words: `1`
- base tokens: `11`
- v5 tokens: `7`
- delta tokens/word: `-4.000000`
- v5 newly appended tokens: `5`
- text preview: `ཕྱགས་ཧོད་ནང་བཀོ་(_T)`

Base token preview:

```text
▁ ཕྱགས་ཧ ོ ད་ནང་བ ཀ ོ ་ ( _ T )
```

v5 token preview:

```text
▁ཕྱགས་ཧོད་ ནང་ བ ཀོ་ (_ T )
```

### 6. dzo_Tibt example 227

- words: `1`
- base tokens: `8`
- v5 tokens: `4`
- delta tokens/word: `-4.000000`
- v5 newly appended tokens: `4`
- text preview: `ད་ལྟོའི་མིང་ཚིག་གོམ་འགྱོ་`

Base token preview:

```text
▁ ད་ལྟ ོ འི་མིང་ཚིག་ག ོ མ་འགྱ ོ ་
```

v5 token preview:

```text
▁ད་ལྟོའི་ མིང་ཚིག་ གོ མ་འགྱོ་
```

### 7. dzo_Tibt example 258

- words: `1`
- base tokens: `10`
- v5 tokens: `6`
- delta tokens/word: `-4.000000`
- v5 newly appended tokens: `6`
- text preview: `ཟུར་རྟགས་བཀལ་ཡོདཔ་སོར་སྟོན་འབད་`

Base token preview:

```text
▁ ཟུར་རྟགས་བ ཀ ལ་ཡ ོ དཔ་ས ོ ར་སྟ ོ ན་འབད་
```

v5 token preview:

```text
▁ཟུར་ རྟགས་བཀལ ་ ཡོདཔ་ སོར་སྟོན་ འབད་
```

### 8. dzo_Tibt example 357

- words: `1`
- base tokens: `13`
- v5 tokens: `9`
- delta tokens/word: `-4.000000`
- v5 newly appended tokens: `4`
- text preview: `རྒྱུ་ལམ་བཏོན་གཏང་།(_D)channels-action`

Base token preview:

```text
▁ རྒྱུ་ལམ་བཏ ོ ན་གཏང་། ( _ D ) chan nel s - action
```

v5 token preview:

```text
▁རྒྱུ་ལམ་ བཏོན་གཏང་། (_ D ) channel s - action
```

