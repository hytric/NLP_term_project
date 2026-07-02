# 02 Related Work Draft

## 목적

본 실험의 각 선택이 어디에서 왔는지 연결한다. 단순 문헌 소개가 아니라 "이 실험에서 어떤 값을 왜 가져왔는가"를 설명해야 한다.

## Glot500

### 가져온 아이디어

- XLM-R 계열 multilingual encoder를 더 많은 언어로 확장한다.
- Mixed corpus에서 SentencePiece unigram tokenizer를 학습한다.
- 기존 tokenizer에 새 vocabulary piece를 append한다.
- MLM continued pretraining을 수행한다.
- 결과를 head/tail/all group으로 나눠 보고한다.

### 본 보고서에서 달라진 점

- 전체 500개 언어 확장이 아니라 92 seen + 7 target 설정이다.
- main question은 full scaling이 아니라 new embedding row initialization이다.
- target7은 downstream coverage가 있는 XLM-R-unseen language-script로 제한했다.

## XLM-R

### 가져온 아이디어

- Base encoder와 tokenizer의 출발점.
- MLM objective와 multilingual pretraining framing.
- 기존 token embedding row는 token string identity 기준으로 보존한다.

### 써야 할 근거

- `xlm-roberta-base`가 source model이다.
- source tokenizer length는 250002이고, `<mask>` source id는 250001이다.

## SentencePiece / Unigram LM

### 가져온 아이디어

- `--model_type=unigram`.
- `--byte_fallback=true`.
- `--character_coverage=1.0`.

### 보고서에서 설명할 이유

- XLM-R/Glot500 계열과 tokenizer family를 맞추기 위해 unigram을 사용한다.
- byte fallback은 새 문자나 드문 문자를 안전하게 분해하기 위한 장치다.
- target7은 Latin script지만 low-resource corpus이므로 unknown 처리보다 byte fallback이 낫다.

## Initialization Literature

### 연결할 문헌

- FVT: 새 token을 source tokenizer로 다시 분해하고 source subtoken embedding 평균을 사용한다.
- WECHSEL/FOCUS류: vocabulary transfer와 lexical overlap 기반 initialization의 근거.
- Hewitt류: 새 embedding을 기존 embedding distribution 근처에 두는 것이 안정적이라는 근거.

### 본 보고서의 위치

이 실험은 논문 방법을 그대로 대규모로 재현하는 것이 아니라, Glot500-style tokenizer append 이후 새 row를 어떻게 초기화할지 비교하는 local controlled ablation이다.

