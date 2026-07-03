# v5.2 Final Framing

작성일: 2026-06-28

## 결정

v5.2는 `92 XLM-R-seen + 7 XLM-R-unseen target`으로 Glot500-style pipeline을 다시
수행하는 main run이다.

```text
MAIN = v5.2_glot5007
TARGET = XLM-R-unseen tail + downstream 가능한 최소 corpus band
TOKENIZER = Glot500-style vocab injection
ABLATION = random / mean / fvt / align embedding initialization
YAMAGUCHI = additional experiment only
```

## 말할 수 있는 것

- Glot500식 tokenizer 확장과 continued MLM을 따른다.
- 같은 corpus와 같은 tokenizer에서 initialization만 바꿔 비교한다.
- target7은 strict `<=10k`가 아니라 downstream이 가능한 가장 낮은 tail band다.
- checkpoint마다 table을 갱신하고, paired 결과가 들어온 경우에만 claim으로 승격한다.

## 말하지 않는 것

- Yamaguchi vocabulary expansion이 main method라고 말하지 않는다.
- POS/Taxi1500이 준비되기 전 measured result처럼 쓰지 않는다.
- 단일 checkpoint에서 `fvt`가 좋아도 최종 결론으로 과장하지 않는다.

## 발표용 문장

```text
We follow the Glot500 vocabulary injection pipeline on 92 XLM-R-seen languages
plus 7 XLM-R-unseen tail languages selected from the smallest corpus band with
downstream coverage, and isolate the effect of new-token embedding
initialization.
```
