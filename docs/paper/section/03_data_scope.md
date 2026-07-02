# 03 Data And Scope Draft

## 목적

언어와 corpus 선택이 임의적이지 않다는 점을 설명한다. 특히 target7은 "평가 가능한 tail language"라는 기준으로 선택되었다고 써야 한다.

## Data Scope

- Seen replay: 92 XLM-R-seen language-script.
- Target: 7 XLM-R-unseen target language-script.
- Target7: `dtp_Latn`, `xav_Latn`, `bam_Latn`, `csb_Latn`, `ile_Latn`, `lij_Latn`, `fur_Latn`.
- Script: 모두 Latin script.

## Target7 선택 이유

1. XLM-R에 명시적으로 seen language로 포함되지 않은 language-script를 우선한다.
2. Tokenizer, MLM, downstream evaluation을 최소한으로 연결할 수 있는 언어를 고른다.
3. 완전히 평가 불가능한 언어보다, PPPL/retrieval/sequence labeling 중 일부라도 점검 가능한 언어를 선택한다.

## Task Coverage

보고서 표에는 task별 target coverage를 반드시 같이 적는다.

- PPPL: target7 전체.
- Tatoeba retrieval: 일부 target only.
- Bible retrieval: 일부 target only.
- Text classification: local target direct evidence 없음 또는 제한적.
- NER: `csb`, `lij`, `fur` 중심.
- POS: target-relevant 일부.
- Roundtrip alignment: Bible coverage가 있는 일부 target.

## Sampling Strategy

### 설명해야 할 코드 근거

- `preprocessing/merge_files.py`.
- `alpha=0.3`.
- seen/target mixed corpus.

### 쓸 문장 방향

Training corpus는 단순 concat이 아니라 language sampling weight를 사용한다. 이 선택은 high-resource 언어가 전체 update를 독점하지 않도록 하고, 동시에 target-only overfitting을 피하기 위한 절충이다.

## 금지할 표현

- target7이 전체 low-resource universe를 대표한다고 쓰지 않는다.
- target7이 script-diverse하다고 쓰지 않는다.
- coverage가 없는 task에서 target 성능을 추론하지 않는다.

