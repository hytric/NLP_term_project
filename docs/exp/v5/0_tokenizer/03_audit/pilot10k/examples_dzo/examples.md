# v5 Pilot Tokenization Example Analysis

This file compares `xlm-roberta-base` with the v5 pilot tokenizer at sentence level.

## Summary

| Language | Examples | Base TPW | v5 TPW | Delta TPW | Worse | Better | Same | v5 New Tokens | v5 Byte Tokens | v5 UNK Tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| dzo_Tibt | 500 | 4.493663 | 8.874784 | 4.381121 | 483 | 5 | 12 | 13949 | 3 | 0 |

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

### 2. dzo_Tibt example 311

- words: `1`
- base tokens: `6`
- v5 tokens: `27`
- delta tokens/word: `21.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `26`
- text preview: `ཨེབ་རྟགས་ནང་པོཔ་ཨཔས་ཁ་ཕྱེ་ནི་ཚབ་ལུ་ཝིན་ཌོ་གསརཔ་ཚུ་ཁ་ཕྱེ།`

Base token preview:

```text
▁ ཨེབ་རྟགས་ནང་པ ོ པ་ཨཔས་ཁ་ཕྱེ་ནི་ཚབ་ལུ་ཝིན་ཌ ོ ་གསརཔ་ཚུ་ཁ་ཕྱེ།
```

v5 token preview:

```text
▁ ཨེ བ་ རྟགས་ ནང་ པོ པ་ ཨ པ ས་ ཁ་ ཕྱ ེ་ ནི་ ཚ བ་ ལུ་ ཝ ིན་ ཌ ོ་ གསརཔ་ ཚུ་ ཁ་ ཕྱ ེ །
```

### 3. dzo_Tibt example 175

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

### 4. dzo_Tibt example 1

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

### 5. dzo_Tibt example 252

- words: `1`
- base tokens: `6`
- v5 tokens: `22`
- delta tokens/word: `16.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `21`
- text preview: `ཡོངས་གྲགས་ལྟར་མཚུངས་གསལ་གྱི་སྒྲ་རེ་ལྔ་པོ་དེ།`

Base token preview:

```text
▁ ཡ ོ ངས་གྲགས་ལྟར་མཚུངས་གསལ་གྱི་སྒྲ་རེ་ལྔ་པ ོ ་དེ།
```

v5 token preview:

```text
▁ ཡོངས་ གྲ གས་ ལྟ ར་ མ ཚུ ངས་ གསལ་ གྱི་ སྒ ྲ ་ རེ་ ལ ྔ ་ པོ་ ད ེ །
```

### 6. dzo_Tibt example 390

- words: `1`
- base tokens: `4`
- v5 tokens: `20`
- delta tokens/word: `16.000000`
- v5 byte tokens: `0`
- v5 newly appended tokens: `19`
- text preview: `ཐུམ་སྒྲིལ་རྒྱ་བསྐྱེད་ཐོག་ཡིག་འདི་གནམ་མེད་ས་མེད་རིངམ་འདུག`

Base token preview:

```text
▁ ཐུམ་སྒྲིལ་རྒྱ་བསྐྱེད་ཐ ོ ག་ཡིག་འདི་གནམ་མེད་ས་མེད་རིངམ་འདུག
```

v5 token preview:

```text
▁ ཐ ུམ་ སྒྲི ལ་ རྒྱ་ བ སྐྱེ ད་ ཐོག་ ཡིག་ འདི་ གན མ་ མེད་ ས་ མེད་ རི ངམ་ འདུག
```

### 7. dzo_Tibt example 55

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

### 8. dzo_Tibt example 39

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


## Best Improvements

### 1. dzo_Tibt example 220

- words: `1`
- base tokens: `10`
- v5 tokens: `9`
- delta tokens/word: `-1.000000`
- v5 newly appended tokens: `5`
- text preview: `ཡིག་སྣོད་ཚུ་བཏོག(_t)`

Base token preview:

```text
▁ ཡིག་སྣ ོ ད་ཚུ་བཏ ོ ག ( _ t )
```

v5 token preview:

```text
▁ ཡིག་སྣོད་ ཚུ་ བཏ ོ ག (_ t )
```

### 2. dzo_Tibt example 411

- words: `1`
- base tokens: `8`
- v5 tokens: `7`
- delta tokens/word: `-1.000000`
- v5 newly appended tokens: `5`
- text preview: `ཡིག་སྣོད་བཏོན་གཏང་དོ།`

Base token preview:

```text
▁ ཡིག་སྣ ོ ད་བཏ ོ ན་གཏང་ད ོ །
```

v5 token preview:

```text
▁ ཡིག་སྣོད་ བཏོན་ གཏང་ ད ོ །
```

### 3. dzo_Tibt example 486

- words: `1`
- base tokens: `11`
- v5 tokens: `10`
- delta tokens/word: `-1.000000`
- v5 newly appended tokens: `5`
- text preview: `ཤོག་ཀུའི་ཚད་:(_s)`

Base token preview:

```text
▁ ཤ ོ ག་ ཀ ུའི་ཚད་ : ( _ s )
```

v5 token preview:

```text
▁ ཤོག་ ཀ ུ འི་ ཚད་ : (_ s )
```

### 4. dzo_Tibt example 33

- words: `2`
- base tokens: `10`
- v5 tokens: `9`
- delta tokens/word: `-0.500000`
- v5 newly appended tokens: `3`
- text preview: `སྲོལ་སྒྲིག་ (_C)popup`

Base token preview:

```text
▁ སྲ ོ ལ་སྒྲིག་ ▁( _ C ) pop up
```

v5 token preview:

```text
▁ སྲོལ་ སྒྲིག་ ▁ (_ C ) pop up
```

### 5. dzo_Tibt example 92

- words: `3`
- base tokens: `14`
- v5 tokens: `13`
- delta tokens/word: `-0.333333`
- v5 newly appended tokens: `8`
- text preview: `འཕྲིན་དོན་འདི་ ལོག་སྟེ་མ་སྟོན། (_D)`

Base token preview:

```text
▁ འཕྲིན་ད ོ ན་འདི་ ▁ ལ ོ ག་སྟེ་མ་སྟ ོ ན། ▁( _ D )
```

v5 token preview:

```text
▁ འཕྲིན་ དོན་ འདི་ ▁ ལོག་ སྟེ་ མ་ སྟོན། ▁ (_ D )
```

### 6. dzo_Tibt example 28

- words: `4`
- base tokens: `16`
- v5 tokens: `16`
- delta tokens/word: `0.000000`
- v5 newly appended tokens: `10`
- text preview: `གཟུགས་བརྙན་ཡིག་སྣོད་ཀྱི་རྩ་སྒྲིག་ ’%s དེ་ ངོས་འཛིན་འབད་མ་ཚུགས།`

Base token preview:

```text
▁ གཟུགས་བརྙན་ཡིག་སྣ ོ ད་ ཀ ྱི་རྩ་སྒྲིག་ ▁ ’ % s ▁ དེ་ ▁ ང ོ ས་འཛིན་འབད་མ་ཚུགས།
```

v5 token preview:

```text
▁ གཟུགས་བརྙན་ ཡིག་སྣོད་ ཀྱི་ རྩ་ སྒྲིག་ ▁ ’ % s ▁དེ་ ▁ ངོས་ འཛིན་ འབད་ མ་ཚུགས།
```

### 7. dzo_Tibt example 29

- words: `1`
- base tokens: `8`
- v5 tokens: `8`
- delta tokens/word: `0.000000`
- v5 newly appended tokens: `7`
- text preview: `དཔེ་མཛོད་ཀྱི་གནས་ཁོངས་སེལ་འཐུ་འབད་`

Base token preview:

```text
▁ དཔེ་མཛ ོ ད་ ཀ ྱི་གནས་ཁ ོ ངས་སེལ་འཐུ་འབད་
```

v5 token preview:

```text
▁ དཔེ་ མཛོད་ ཀྱི་ གན ས་ཁོངས་ སེལ་འཐུ་ འབད་
```

### 8. dzo_Tibt example 81

- words: `2`
- base tokens: `8`
- v5 tokens: `8`
- delta tokens/word: `0.000000`
- v5 newly appended tokens: `6`
- text preview: `བདག་པོ་ གཞི་སྒྲིག་འབད་མི་ཆོག་`

Base token preview:

```text
▁ བདག་པ ོ ་ ▁ གཞི་སྒྲིག་འབད་མི་ཆ ོ ག་
```

v5 token preview:

```text
▁ བདག་ པོ་ ▁ གཞི་སྒྲིག་ འབད་མི་ ཆ ོག་
```

