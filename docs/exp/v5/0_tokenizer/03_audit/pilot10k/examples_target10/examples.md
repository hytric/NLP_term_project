# v5 Pilot Tokenization Example Analysis

This file compares `xlm-roberta-base` with the v5 pilot tokenizer at sentence level.

## Summary

| Language | Examples | Base TPW | v5 TPW | Delta TPW | Worse | Better | Same | v5 New Tokens | v5 Byte Tokens | v5 UNK Tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fur_Latn | 200 | 1.831300 | 1.685367 | -0.145933 | 0 | 173 | 27 | 845 | 0 | 0 |
| krc_Cyrl | 200 | 2.766343 | 2.178495 | -0.587848 | 0 | 195 | 5 | 1962 | 0 | 0 |
| acm_Arab | 200 | 2.220959 | 2.136670 | -0.084290 | 0 | 77 | 123 | 176 | 0 | 0 |
| dzo_Tibt | 200 | 4.450250 | 8.958617 | 4.508368 | 192 | 2 | 6 | 5770 | 0 | 0 |
| sat_Olck | 200 | 2.128843 | 2.052807 | -0.076035 | 57 | 139 | 4 | 16248 | 0 | 0 |
| mad_Latn | 200 | 1.509805 | 1.508748 | -0.001057 | 2 | 8 | 190 | 15 | 0 | 0 |
| bam_Latn | 200 | 2.231038 | 1.747709 | -0.483329 | 0 | 186 | 14 | 1439 | 0 | 0 |
| kjb_Latn | 200 | 2.536631 | 2.127811 | -0.408820 | 0 | 196 | 4 | 1670 | 0 | 0 |
| quw_Latn | 200 | 2.436716 | 1.806457 | -0.630259 | 0 | 199 | 1 | 2158 | 0 | 0 |
| rap_Latn | 200 | 1.644097 | 1.386176 | -0.257921 | 0 | 158 | 42 | 822 | 0 | 0 |

## Worst Regressions

### 1. dzo_Tibt example 6

- words: `13`
- base tokens: `134`
- v5 tokens: `510`
- delta tokens/word: `28.923077`
- v5 byte tokens: `0`
- v5 newly appended tokens: `496`
- text preview: `དེ་ཡང་སྔོན་རྒྱ་གར་དུ་སྙན་ངག་གི་བསྟན་བཅོས་བྷ་ར་ཏ་ཞེས་བྱ་བ་ཞིག་བརྩམས་པ་ཚོགས་བདག་གིས་ཡིན་མཁན་བྱས་ནས་བྲིས་པར་གྲགས་པའི་གཞུང་ཤོ་ལོ་ཀ་འབུམ་ལྷག་ཡོད་པ་དང༌། དྲང་སྲོང་མེ་བཞིན་འཇུག་གི་བུ་མོ...`

Base token preview:

```text
▁ དེ་ཡང་སྔ ོ ན་རྒྱ་གར་དུ་སྙན་ངག་གི་བསྟན་བཅ ོ ས་བྷ་ར་ཏ་ཞེས་བྱ་བ་ཞིག་བརྩམས་པ་ཚ ོ གས་བདག་གིས་ཡིན་མཁན་བྱས་ནས་བྲིས་པར་གྲགས་པའི་གཞུང་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ལྷག་ཡ ོ ད་པ་དང་། ▁ དྲང་སྲ ོ ང་མེ་བཞིན་འཇུག་གི་བུ་མ ོ ས་སྙན་ངག་རཱ་མ་ཡ་ན་ཞེས་པ་ཞིག་བརྩམས་པ་དེ་ནི་རྒྱལ་པ ོ ་རཱ་མ་ན་དང་དེའི་བཙུན་པ ོ ་ར ོ ལ་རྙེད་མའི་ལ ོ ་རྒྱུས་སྙན་ངག་ཏུ་སྦྱར་བ་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ཡ ོ ད་པ་ཞིག་དང་། ▁ མརྐེ་ཎ་ཊ་ཡིས་བརྩམས་པའི་སྙན་ངག་གི་བསྟན་བཅ ོ ས་ཁྱབ་འཇུག་གི་འཇུག་པ་བཅུ་ས ོ གས་གཙ ོ ་བ ོ ར་སྟ ོ ན་པ་ཤ ོ ་ལ ོ ་ ཀ ་འབུམ་ལྷག་ཡ ོ ད་པ་ཞིག་དང་། ▁ རཱ་མ་ཤརྨས་མཛད་པའི་སྙན་ངག་གི་བསྟན་བཅ ོ ས་ཤ ོ ་ལ ོ ་ ཀ ་སྟ ོ ང་ཕྲག་བརྒྱད་ཅུ་ཅན་དང་། ▁ ནག་མ ོ ་ཁ ོ ལ་གྱིས་མཛད་པའི་སྙན་ངག་གཞ ོ ན་ནུ་འབྱུང་བ་དང་། ▁ གཞན་སྙན་ངག་གི་བསྟན་བཅ
```

v5 token preview:

```text
▁དེ་ ཡང་ སྔོན་ རྒྱ་ ག ར་ དུ་ ས ྙ ན་ ང ག་ གི་ བ སྟ ན་ བཅོས་ བ ྷ ་ ར་ ཏ ་ ཞ ེ ས་ བྱ་ བ་ ཞི ག་ བ རྩ མས་ པ་ ཚོགས་ བདག་ གིས་ ཡི ན་ མ ཁ ན་ བྱ ས་ ན ས་ བྲ ི ས་ པར་ གྲ གས་ པའི་ གཞུང་ ཤ ོ་ ལོ་ ཀ་ འབ ུམ་ ལྷག་ ཡོད་ པ་ དང་ ། ▁ དྲ ང་ སྲ ོང་ མ ེ་ བ ཞི ན་ འཇ ུག་ གི་ བ ུ་
```

### 2. dzo_Tibt example 175

- words: `1`
- base tokens: `4`
- v5 tokens: `23`
- delta tokens/word: `19.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `22`
- text preview: `རང་རང་སའི་དམིགས་གཏད་གུ་ཁོང་རའི་དབྱིབས་ཚུ་འདྲུད་ནི་དང་བཞག་`

Base token preview:

```text
▁ རང་རང་སའི་དམིགས་གཏད་གུ་ཁ ོ ང་རའི་དབྱིབས་ཚུ་འདྲུད་ནི་དང་བཞག་
```

v5 token preview:

```text
▁ རང་ རང་ ས འི་ དམིགས་ གཏ ད་ གུ་ ཁ ོང་ ར འི་ ད བྱ ི བས་ ཚུ་ འ དྲ ུད་ ནི་དང་ བཞག་
```

### 3. dzo_Tibt example 1

- words: `1`
- base tokens: `10`
- v5 tokens: `27`
- delta tokens/word: `17.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `25`
- text preview: `དང་པ་ཕས་རྒོལ་ཟིལ་གྱིས་གནོན་ཏེ་ཞི་བདེའི་གོ་སྐབས་བཟོ་གནང་བ།`

Base token preview:

```text
▁ དང་པ་ཕས་རྒ ོ ལ་ཟིལ་གྱིས་གན ོ ན་ཏེ་ཞི་བདེའི་ག ོ ་སྐབས་བཟ ོ ་གནང་བ།
```

v5 token preview:

```text
▁ དང་ པ་ ཕ ས་ ར ྒ ོ ལ་ ཟ ི ལ་ གྱིས་ གན ོན་ ཏེ་ ཞ ི་ བ ད ེ འི་ གོ་ སྐབས་ བཟོ་ གནང་ བ།
```

### 4. dzo_Tibt example 55

- words: `1`
- base tokens: `5`
- v5 tokens: `20`
- delta tokens/word: `15.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `18`
- text preview: `ཐག་རིང་གི་ཨའི་ཨེམ་ཨེ་པི་ཡན་ལག་སྣོད་འཛིན...`

Base token preview:

```text
▁ ཐག་རིང་གི་ཨའི་ཨེམ་ཨེ་པི་ཡན་ལག་སྣ ོ ད་འཛིན ...
```

v5 token preview:

```text
▁ ཐ ག་ རིང་ གི་ ཨའི་ ཨེམ་ ཨེ་ པི་ ཡ ན་ ལག་ ས ྣ ོད་ འ ཛ ི ན ...
```

### 5. dzo_Tibt example 39

- words: `1`
- base tokens: `6`
- v5 tokens: `20`
- delta tokens/word: `14.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `18`
- text preview: `སེལ་འཐུ་འབད་ཡོད་པའི་སེམ་མཉམ་ཐིག་གི་གྲུ་ཟུར་དེ་བསྒྱུར་བཆཅོས་འབད།`

Base token preview:

```text
▁ སེལ་འཐུ་འབད་ཡ ོ ད་པའི་སེམ་མཉམ་ཐིག་གི་གྲུ་ཟུར་དེ་བསྒྱུར་བཆཅ ོ ས་འབད།
```

v5 token preview:

```text
▁ སེལ་འཐུ་ འབད་ ཡོད་པའི་ སེ མ་ མཉམ་ ཐིག་ གི་ གྲ ུ་ ཟུར་ དེ་ བསྒྱུར་ བ ཆ ཅ ོ ས་ འབད།
```

### 6. dzo_Tibt example 116

- words: `4`
- base tokens: `16`
- v5 tokens: `72`
- delta tokens/word: `14.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `68`
- text preview: `ཨིསི་ལ་མིག་གསེར་གྱི་དུས་སྐབས་ནང་གི་མཚོན་རིག་མཁས་པ་མང་ཤོས་ཅིག་ ཡོན་ཏན་སྣ་མང་སྦེ་ཤེས་ཅིག་སྦེ་ཆ་བཞགཔ་ཨིནམ་དང་ དི་ཡང་ དེང་སང་གི་མཚོན་རིག་མཐུན་རྐྱེན་དང་འབྲེལ་བའི་རྣམ་གཞག་ཚུ་མེད་མི་ལས...`

Base token preview:

```text
▁ ཨིསི་ལ་མིག་གསེར་གྱི་དུས་སྐབས་ནང་གི་མཚ ོ ན་རིག་མཁས་པ་མང་ཤ ོ ས་ཅིག་ ▁ ཡ ོ ན་ཏན་སྣ་མང་སྦེ་ཤེས་ཅིག་སྦེ་ཆ་བཞགཔ་ཨིནམ་དང་ ▁ དི་ཡང་ ▁ དེང་སང་གི་མཚ ོ ན་རིག་མཐུན་རྐྱེན་དང་འབྲེལ་བའི་རྣམ་གཞག་ཚུ་མེད་མི་ལས་བརྟེན་ཏེ་ཨིན་མས།
```

v5 token preview:

```text
▁ ཨི སི་ ལ་ མི ག་ གས ེར་ གྱི་ དུས་ སྐབས་ ནང་ གི་ མ ཚོ ན་ རིག་ མཁས་ པ་ མང་ ཤོས་ ཅིག་ ▁ ཡ ོན་ ཏ ན་ ས ྣ ་ མང་ སྦེ་ ཤེས་ ཅིག་ སྦེ་ ཆ་ བ ཞ ག པ་ ཨིནམ་ དང་ ▁ ད ི་ ཡང་ ▁ ད ེ ང་ ས ང་ གི་ མ ཚོ ན་ རིག་ མཐུན་ རྐྱེན་ དང་ འབྲེལ་ བའི་ རྣམ་ ག ཞ ག་ ཚུ་ མེད་ མི་ ལས་བརྟེན་ ཏེ་ ཨིན་མས།
```

### 7. dzo_Tibt example 150

- words: `5`
- base tokens: `24`
- v5 tokens: `92`
- delta tokens/word: `13.600000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `87`
- text preview: `ཤར་ནས་ནུབ་ཏུ་ཟུག་པའི་རི་ཕྲན་དག་ནི་ས་དམར་ཡིན། གཞུང་ཆུའི་གཡས་གཡོན་གྱི་གཞོང་དང་རི་ཕྲན་དག་གི་བར་གསེང་ན་རྡོ་སྦིས་དུ་ཁ་སྟོང་། སྡེ་བ་ཉེར་གསུམ། མི་གྲངས་གཅིག་ཁྲི་ཉིས་སྟོང་ཙམ། སྟོད་སྨད་བར...`

Base token preview:

```text
▁ ཤར་ནས་ནུབ་ཏུ་ཟུག་པའི་རི་ཕྲན་དག་ནི་ས་དམར་ཡིན། ▁ གཞུང་ཆུའི་གཡས་གཡ ོ ན་གྱི་གཞ ོ ང་དང་རི་ཕྲན་དག་གི་བར་གསེང་ན་རྡ ོ ་སྦིས་དུ་ཁ་སྟ ོ ང་། ▁ སྡེ་བ་ཉེར་གསུམ། ▁ མི་གྲངས་གཅིག་ཁྲི་ཉིས་སྟ ོ ང་ཙམ། ▁ སྟ ོ ད་སྨད་བར་གསུམ་དུ་གནས་ཡ ོ ད།
```

v5 token preview:

```text
▁ ཤ ར་ ན ས་ ན ུ བ་ ཏ ུ་ ཟ ུག་ པའི་ རི་ ཕྲ ན་ ད ག་ ནི་ ས་ ད མ ར་ ཡི ན། ▁ གཞུང་ ཆ ུ འི་ ག ཡ ས་ གཡོ ན་ གྱི་ ག ཞ ོང་ དང་ རི་ ཕྲ ན་ ད ག་ གི་ བར་ གས ེ ང་ ན་ ར ྡ ོ་ སྦ ི ས་ དུ་ ཁ་ སྟ ོང་ ། ▁ སྡེ་ བ་ ཉ ེར་ གས ུ མ། ▁ མི་ གྲངས་ གཅིག་ ཁྲི་ ཉི ས་ སྟ ོང་ ཙ
```

### 8. dzo_Tibt example 48

- words: `2`
- base tokens: `12`
- v5 tokens: `37`
- delta tokens/word: `12.500000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `35`
- text preview: `ང་བཅས་ར་འཛམ་གླིང་གི་དབྱིས་འདི་སྒོང་རྡོག་རིལ་རི་སྦེ་ཨིན་མས་ཟེར་ སེམས་ཁར་འཆར་མི་འགོ་དང་པ་འདི་ཁོ་ཨིན་མས།`

Base token preview:

```text
▁ ང་བཅས་ར་འཛམ་གླིང་གི་དབྱིས་འདི་སྒ ོ ང་རྡ ོ ག་རིལ་རི་སྦེ་ཨིན་མས་ཟེར་ ▁ སེམས་ཁར་འཆར་མི་འག ོ ་དང་པ་འདི་ཁ ོ ་ཨིན་མས།
```

v5 token preview:

```text
▁ ང་ བཅ ས་ ར་ འཛམ་གླིང་ གི་ ད བྱ ི ས་ འདི་ སྒ ོང་ ར ྡ ོག་ རི ལ་ རི་ སྦེ་ ཨིན་ མས་ ཟེར་ ▁ སེམས་ ཁར་ འཆར་ མི་ འ གོ་ དང་ པ་ འདི་ ཁ ོ་ ཨིན་མས།
```

### 9. dzo_Tibt example 42

- words: `1`
- base tokens: `4`
- v5 tokens: `16`
- delta tokens/word: `12.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `14`
- text preview: `སེ་མ་རང་/ཨཱ་མཱད་ཡ་ནི།`

Base token preview:

```text
▁ སེ་མ་རང་ / ཨཱ་མཱད་ཡ་ནི།
```

v5 token preview:

```text
▁ ས ེ་ མ་ རང་ / ཨ ཱ ་ མ ཱ ད་ ཡ་ ན ི །
```

### 10. dzo_Tibt example 134

- words: `1`
- base tokens: `3`
- v5 tokens: `15`
- delta tokens/word: `12.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `13`
- text preview: `ཀུན་བཟང་བླ་མའི་ཞལ་ལུང་།`

Base token preview:

```text
▁ ཀ ུན་བཟང་བླ་མའི་ཞལ་ལུང་།
```

v5 token preview:

```text
▁ ཀ ུ ན་ བ ཟ ང་ བླ ་ མའི་ ཞ ལ་ ལ ུང་ །
```

### 11. dzo_Tibt example 174

- words: `5`
- base tokens: `21`
- v5 tokens: `77`
- delta tokens/word: `11.200000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `70`
- text preview: `ཐབས་རིག་རེ་རེ་བཞིན་དུ་ལག་ལེན་འཐབ་ཏེ་ ཀུའིན་དང་གོ་དྲལ་གི་ཐབས་རིག་ལ་ལུ་ཅིག་བསལ་ནི་གི་དཔའ་བཅམ་མི་ ཨང་རྩིས་རིག་པའི་མཚན་ཉིད་རིག་པ་ཅིག་གི་དོན་ལས་ པེ་ལི་ལོབ་མེ་གྲི་གི་ ཨང་རྩིས་རིག་པའི་...`

Base token preview:

```text
▁ ཐབས་རིག་རེ་རེ་བཞིན་དུ་ལག་ལེན་འཐབ་ཏེ་ ▁ ཀ ུའིན་དང་ག ོ ་དྲལ་གི་ཐབས་རིག་ལ་ལུ་ཅིག་བསལ་ནི་གི་དཔའ་བཅམ་མི་ ▁ ཨང་རྩིས་རིག་པའི་མཚན་ཉིད་རིག་པ་ཅིག་གི་ད ོ ན་ལས་ ▁ པེ་ལི་ལ ོ བ་མེ་གྲི་གི་ ▁ ཨང་རྩིས་རིག་པའི་ནང་གི་དང ོ ས་གནས་རིང་ལུགས་འདི་བལྟ་དག ོ པ་ཨིན།
```

v5 token preview:

```text
▁ ཐབས་ རིག་ རེ་ རེ་ བ ཞི ན་ དུ་ ལག་ལེན་འཐབ་ ཏེ་ ▁ ཀ ུ འ ིན་ དང་ གོ་ དྲ ལ་ གི་ ཐབས་ རིག་ ལ་ ལུ་ ཅིག་ བ ས ལ་ ནི་ གི་ དཔ འ་ བཅ མ་ མི་ ▁ ཨང་ རྩིས་ རིག་ པའི་ མཚན་ ཉི ད་ རིག་ པ་ ཅིག་ གི་ དོན་ ལས་ ▁ པ ེ ་ལི་ ལ ོ བ་ མ ེ་ གྲ ི་ གི་ ▁ ཨང་ རྩིས་ རིག་ པའི་ ནང་ གི་ དངོས་ གནས་ རིང་ ལུགས་ འདི་ བལྟ་ དགོཔ་ ཨིན།
```

### 12. dzo_Tibt example 72

- words: `1`
- base tokens: `4`
- v5 tokens: `15`
- delta tokens/word: `11.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `14`
- text preview: `སེལ་འཐུ་འབད་ནི་པེན་ནང་ཡིག་སྣོད་ཚུ་གུ་གཉིས་ལྡན་ཨེབ་གཏང་འབད།`

Base token preview:

```text
▁ སེལ་འཐུ་འབད་ནི་པེན་ནང་ཡིག་སྣ ོ ད་ཚུ་གུ་གཉིས་ལྡན་ཨེབ་གཏང་འབད།
```

v5 token preview:

```text
▁ སེལ་འཐུ་ འབད་ནི་ པ ེན་ ནང་ ཡིག་སྣོད་ ཚུ་ གུ་ གཉིས་ ལྡན་ ཨེ བ་ གཏང་ འབད།
```


## Best Improvements

### 1. acm_Arab example 156

- words: `7`
- base tokens: `38`
- v5 tokens: `20`
- delta tokens/word: `-2.571429`
- v5 newly appended tokens: `11`
- text preview: `مَا يِحِبّكَ يَوْمٌ بَسّ الخاين إِلَيَّ يُكَذَّبُ.`

Base token preview:

```text
▁م َ ا ▁ي ِ ح ِ ب ّ ك َ ▁ي َ و ْ م ٌ ▁ب َ س ّ ▁الخ اين ▁إ ِ ل َ ي َّ ▁ي ُ ك َ ذ َّ ب ُ .
```

v5 token preview:

```text
▁مَا ▁ي ِ حِ بّ كَ ▁يَوْم ٌ ▁بَ سّ ▁الخ اين ▁إِلَي َّ ▁يُ كَ ذ َّ بُ .
```

### 2. acm_Arab example 0

- words: `9`
- base tokens: `73`
- v5 tokens: `59`
- delta tokens/word: `-1.555556`
- v5 newly appended tokens: `17`
- text preview: `@basmabas1154 هّهّهّهّهّهّ مُاضٌحَك نَيّالُهّ لُيّ يّنَامُ بُحَظُنَ ؤٌالُدًهّ http://t.co/EM8EjgsJe7`

Base token preview:

```text
▁@ bas ma bas 11 54 ▁ه ّ ه ّ ه ّ ه ّ ه ّ ه ّ ▁م ُ اض ٌ ح َ ك ▁ن َ ي ّ ال ُ ه ّ ▁ل ُ ي ّ ▁ي ّ ن َ ام ُ ▁ب ُ ح َ ظ ُ ن َ ▁ ؤ ٌ ال ُ د ً ه ّ ▁http :// t . co / EM 8 E j gs Je 7
```

v5 token preview:

```text
▁@ bas ma bas 11 54 ▁ه ّه ّه ّه ّه ّه ّ ▁مُ اض ٌ حَ ك ▁نَ يّ ال ُ ه ّ ▁ لُ يّ ▁ يّ نَا مُ ▁ بُ حَ ظ ُ نَ ▁ ؤ ٌ ال ُ د ً ه ّ ▁http :// t . co / EM 8 E j gs Je 7
```

### 3. krc_Cyrl example 160

- words: `15`
- base tokens: `57`
- v5 tokens: `36`
- delta tokens/word: `-1.400000`
- v5 newly appended tokens: `15`
- text preview: `Барабанда да сурат салыннганладан къалгъанла болургъа боллукъдула, алай а, аланы туз басыб, тюбюнден кёрюнмезге боллукъдула.`

Base token preview:

```text
▁Бара бан да ▁да ▁су рат ▁са лын н ган ла дан ▁ къ ал гъ ан ла ▁бол ург ъ а ▁бол лук ъд у ла , ▁а лай ▁а , ▁ала ны ▁ту з ▁ басы б , ▁ тю бю н ден ▁к ёр юн ме з ге ▁бол лук ъд у ла .
```

v5 token preview:

```text
▁Бара б анда ▁да ▁сура т ▁салын нган ладан ▁къа лгъан ла ▁болургъа ▁боллукъду ла , ▁алай ▁а , ▁аланы ▁ту з ▁бас ыб , ▁тюбю н ден ▁кёрю н ме з ге ▁боллукъду ла .
```

### 4. quw_Latn example 40

- words: `13`
- base tokens: `39`
- v5 tokens: `21`
- delta tokens/word: `-1.384615`
- v5 newly appended tokens: `10`
- text preview: `Paiguna Jesús yachachishca runaunara maquira mana maillasha micuujcunara ricusha , paigunara cauźayachinauca .`

Base token preview:

```text
▁Pai guna ▁Jesús ▁ya ch ach ish ca ▁ runa unar a ▁ma qui ra ▁mana ▁mail lash a ▁mi cu uj cun ara ▁ ric usha ▁ , ▁pai guna ra ▁cau ź aya china uca ▁ .
```

v5 token preview:

```text
▁Paiguna ▁Jesús ▁yachachishca ▁runaunara ▁maqui ra ▁mana ▁mail lash a ▁micu u jcunara ▁ricusha ▁ , ▁paigunara ▁cauźayachi nauca ▁ .
```

### 5. bam_Latn example 111

- words: `11`
- base tokens: `37`
- v5 tokens: `22`
- delta tokens/word: `-1.363636`
- v5 newly appended tokens: `9`
- text preview: `Mɔgɔw ye furakɛcogo caman lajɛ, nka kunpɛɲɛ matarafali de ɲɔgɔn tɛ.`

Base token preview:

```text
▁M ɔ g ɔ w ▁ye ▁fur ak ɛ co go ▁ca man ▁la j ɛ , ▁ nka ▁kun p ɛ ɲ ɛ ▁mata raf ali ▁de ▁ ɲ ɔ g ɔ n ▁t ɛ .
```

v5 token preview:

```text
▁M ɔgɔ w ▁ye ▁furakɛ cogo ▁caman ▁lajɛ , ▁ nka ▁kun p ɛ ɲɛ ▁ma taraf ali ▁de ▁ɲɔgɔn ▁tɛ .
```

### 6. quw_Latn example 155

- words: `26`
- base tokens: `76`
- v5 tokens: `42`
- delta tokens/word: `-1.307692`
- v5 newly appended tokens: `25`
- text preview: `Ñucanchi ricushcara uyashcaras cangunama cuintanchi , canguna shinallara ñucanchihua parijumanda llaquinausha tiangaj . Ñucanchi parijumanda llaquinaushca sirtu pacha Dioshua pa...`

Base token preview:

```text
▁ Ñ uca nchi ▁ ric ush cara ▁uy ash cara s ▁can guna ma ▁cu inta nchi ▁ , ▁can guna ▁shin al lara ▁ ñ uca nchi hua ▁pari ju manda ▁ lla quina usha ▁ti ang aj ▁ . ▁ Ñ uca nchi ▁pari ju manda ▁ lla quina ush ca ▁sir tu ▁pa cha ▁Dios hua ▁pari ju ▁pai hua ▁Ch uri ▁Jesu cris to hua ▁pari ju ▁tu cun ▁ .
```

v5 token preview:

```text
▁Ñucanchi ▁ricu shcara ▁uya shcara s ▁canguna ma ▁cuinta nchi ▁ , ▁canguna ▁shinallara ▁ñucanchi hua ▁pariju manda ▁llaquina usha ▁tia ngaj ▁ . ▁Ñucanchi ▁pariju manda ▁llaquina ushca ▁sirtu ▁pacha ▁Dios hua ▁pariju ▁paihua ▁Churi ▁Jesucristo hua ▁pariju ▁tucun ▁ .
```

### 7. krc_Cyrl example 26

- words: `12`
- base tokens: `40`
- v5 tokens: `25`
- delta tokens/word: `-1.250000`
- v5 newly appended tokens: `10`
- text preview: `Ол джыллада Къарачайны уруннганлары къралны башха къарнаш халкъларыча алгъа уллу атламла этгендиле.`

Base token preview:

```text
▁Ол ▁д жыл лада ▁Къ ара чай ны ▁у рун н ган лары ▁ кър ал ны ▁баш ха ▁ къ арна ш ▁хал къ лары ча ▁ал гъ а ▁ул лу ▁ат лам ла ▁эт ген ди ле .
```

v5 token preview:

```text
▁Ол ▁джыллада ▁Къарачай ны ▁у рун нган лары ▁кърал ны ▁башха ▁къа рна ш ▁халкъ лары ча ▁алгъа ▁уллу ▁ат лам ла ▁этгенди ле .
```

### 8. bam_Latn example 77

- words: `20`
- base tokens: `66`
- v5 tokens: `41`
- delta tokens/word: `-1.250000`
- v5 newly appended tokens: `16`
- text preview: `Dugujukɔrɔjiw nɔgɔli sababu bɛ bɔ yɔrɔw kɛcogo la i n’a fɔ dugukolo suguya, yɔrɔ ɲigincogo, ani dugujukɔrɔji yɔrɔ janya hakɛ.`

Base token preview:

```text
▁Du gu juk ɔ r ɔ ji w ▁n ɔ g ɔ li ▁sababu ▁b ɛ ▁b ɔ ▁y ɔ r ɔ w ▁k ɛ co go ▁la ▁i ▁n ’ a ▁f ɔ ▁dugu kolo ▁sugu ya , ▁y ɔ r ɔ ▁ ɲ ig in co go , ▁ani ▁dugu juk ɔ r ɔ ji ▁y ɔ r ɔ ▁ja nya ▁hak ɛ .
```

v5 token preview:

```text
▁Du gu ju kɔrɔ ji w ▁n ɔgɔ li ▁sababu ▁bɛ ▁bɔ ▁yɔrɔ w ▁kɛ cogo ▁la ▁i ▁n ’ a ▁fɔ ▁dugukolo ▁suguya , ▁yɔrɔ ▁ɲ ig in cogo , ▁ani ▁dugu ju kɔrɔ ji ▁yɔrɔ ▁ja nya ▁hakɛ .
```

### 9. quw_Latn example 108

- words: `17`
- base tokens: `50`
- v5 tokens: `29`
- delta tokens/word: `-1.235294`
- v5 newly appended tokens: `14`
- text preview: `Shinallara yachanguichi imasna cangunara camachicanchi , cushiyacanchi caran duiñura , shu yaya paihua churiunara cushiyachishca cuinta .`

Base token preview:

```text
▁Shin al lara ▁ya chang u ichi ▁ imas na ▁can guna ra ▁cama chi can chi ▁ , ▁cu s hiya can chi ▁cara n ▁du iñ ura ▁ , ▁shu ▁ya ya ▁pai hua ▁chur i unar a ▁cu s hiya ch ish ca ▁cu inta ▁ .
```

v5 token preview:

```text
▁Shinallara ▁ya cha nguichi ▁imasna ▁cangunara ▁cama chica nchi ▁ , ▁cushiya can chi ▁caran ▁duiñu ra ▁ , ▁shu ▁yaya ▁paihua ▁churiuna ra ▁cushiya chishca ▁cuinta ▁ .
```

### 10. krc_Cyrl example 172

- words: `13`
- base tokens: `39`
- v5 tokens: `23`
- delta tokens/word: `-1.230769`
- v5 newly appended tokens: `10`
- text preview: `9 ноябрь — григориан орузламада джылны 313-чю кюнюдю (високос джыллада — 314-чю кюнюдю).`

Base token preview:

```text
▁9 ▁но яб рь ▁— ▁гри го риан ▁ор уз лама да ▁д жыл ны ▁31 3- ч ю ▁к ю ню дю ▁( високо с ▁д жыл лада ▁— ▁31 4- ч ю ▁к ю ню дю ).
```

v5 token preview:

```text
▁9 ▁ ноябр ь ▁— ▁г ригориан ▁орузлама да ▁джылны ▁31 3- чю ▁кюнюдю ▁( високос ▁джыллада ▁— ▁31 4- чю ▁кюнюдю ).
```

### 11. krc_Cyrl example 189

- words: `13`
- base tokens: `47`
- v5 tokens: `31`
- delta tokens/word: `-1.230769`
- v5 newly appended tokens: `10`
- text preview: `Газет республикада болгъан джамагъат–политика ишлени ачыкълайды, дагъыда малкъарлыланы тарихлерини эмда культураларыны юсюнден басмалайды.`

Base token preview:

```text
▁Газ ет ▁республика да ▁бол гъ ан ▁ джа ма гъ ат – полит ика ▁иш лени ▁ачык ъ лайды , ▁да гъ ы да ▁мал къ ар лы ла ны ▁тарих лери ни ▁эм да ▁культура ларын ы ▁ ю сю н ден ▁басма лайды .
```

v5 token preview:

```text
▁Газ ет ▁республика да ▁болгъан ▁джамагъат – полит ика ▁ишле ни ▁ачыкъ лайды , ▁да гъы да ▁мал къ ар лы ланы ▁тарих лерини ▁эмда ▁культура ларыны ▁юсюнден ▁басма лайды .
```

### 12. bam_Latn example 152

- words: `36`
- base tokens: `93`
- v5 tokens: `49`
- delta tokens/word: `-1.222222`
- v5 newly appended tokens: `18`
- text preview: `Kabini aw bɛ banajugu dɔ taamasiɲɛ fɔlɔ ye, aw ye dɔgɔtɔrɔ dɔ ka dɛmɛ ɲini, aw kana a to bana ka juguya fo banabagatɔ ka dɛsɛ ka taama ka taa dɔgɔtɔrɔ fɛ yen walima dɔgɔtɔrɔso la.`

Base token preview:

```text
▁Kab ini ▁a w ▁b ɛ ▁bana ju gu ▁d ɔ ▁ta a masi ɲ ɛ ▁f ɔ l ɔ ▁ye , ▁a w ▁ye ▁d ɔ g ɔ t ɔ r ɔ ▁d ɔ ▁ka ▁d ɛ m ɛ ▁ ɲ ini , ▁a w ▁kana ▁a ▁to ▁bana ▁ka ▁jugu ya ▁fo ▁bana baga t ɔ ▁ka ▁d ɛ s ɛ ▁ka ▁ta ama ▁ka ▁ta a ▁d ɔ g ɔ t ɔ r ɔ ▁f ɛ ▁yen
```

v5 token preview:

```text
▁Kab ini ▁aw ▁bɛ ▁bana ju gu ▁dɔ ▁taamasiɲɛ ▁fɔlɔ ▁ye , ▁aw ▁ye ▁dɔgɔtɔrɔ ▁dɔ ▁ka ▁dɛmɛ ▁ ɲini , ▁aw ▁kana ▁a ▁to ▁bana ▁ka ▁jugu ya ▁fo ▁bana baga tɔ ▁ka ▁ dɛsɛ ▁ka ▁ta ama ▁ka ▁taa ▁dɔgɔtɔrɔ ▁fɛ ▁yen ▁walima ▁dɔgɔtɔrɔ so ▁la .
```

