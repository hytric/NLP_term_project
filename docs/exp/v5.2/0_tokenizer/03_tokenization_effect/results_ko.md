# v5.2 Tokenization Effect 결과 요약

## 목적

v5.2 tokenizer 확장이 target7 raw corpus에서 실제로 tokenization을 얼마나 개선하는지
확인한다. 비교는 동일한 문장에 대해 `xlm-roberta-base` tokenizer와 v5.2 extended
tokenizer를 각각 적용하는 방식으로 수행했다.

## 설정

| 항목 | 값 |
| --- | ---: |
| base tokenizer length | 250,002 |
| v5.2 tokenizer length | 366,666 |
| appended/novel token strings | 116,664 |
| languages | 7 target tail languages |
| samples per language | 500 |
| total sentences | 3,500 |

## 전체 결과

| Scope | Base tokens/word | v5.2 tokens/word | Token reduction | Base chars/token | v5.2 chars/token | New-token share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| target7 | 2.204134 | 1.592392 | 27.754280% | 2.074479 | 2.871421 | 28.392427% |

해석하면, v5.2 tokenizer는 target7에서 XLM-R tokenizer보다 평균적으로 약
27.75% 적은 subword를 사용한다. 즉 vocabulary extension은 실제로 tail language의
subword fertility를 개선한다.

## 언어별 결과

| Language | Name | Base TPW | v5.2 TPW | Token reduction | New-token share |
| --- | --- | ---: | ---: | ---: | ---: |
| `bam_Latn` | Bambara | 2.248034 | 1.513428 | 32.677703% | 32.346790% |
| `csb_Latn` | Kashubian | 2.934551 | 1.945100 | 33.717290% | 34.388850% |
| `dtp_Latn` | Kadazan Dusun | 1.975990 | 1.496198 | 24.281085% | 34.394223% |
| `fur_Latn` | Friulian | 1.824645 | 1.453669 | 20.331393% | 23.974143% |
| `ile_Latn` | Interlingue | 1.544606 | 1.352672 | 12.426036% | 14.416863% |
| `lij_Latn` | Ligurian | 2.195411 | 1.824073 | 16.914278% | 19.795870% |
| `xav_Latn` | Xavánte | 2.398465 | 1.561237 | 34.906811% | 34.478046% |

## 왜 tokenizer만으로 설명되지 않는가

v5.2 main ablation에서 `random`, `mean`, `fvt`는 모두 같은 extended tokenizer와
같은 MLM corpus/schedule을 사용한다. 따라서 이 세 모델 사이의 성능 차이는
tokenizer 확장 자체가 아니라, 새 vocabulary row의 embedding initialization과
이후 continued MLM dynamics에서 나온다.

대표적으로 step4000에서:

| Metric | Random | FVT | 해석 |
| --- | ---: | ---: | --- |
| PPPL | 119.581715 | 58.025602 | 같은 tokenizer에서도 FVT가 훨씬 낮음 |
| Tatoeba Acc10 | 0.248908 | 0.282957 | 같은 tokenizer에서도 FVT가 높음 |
| Roundtrip accuracy | 0.019533 | 0.025167 | 같은 tokenizer에서도 FVT가 높음 |

따라서 발표 문장은 다음처럼 잡는다.

> Tokenizer extension은 tail language의 subword fertility를 개선한다. 그러나
> v5.2 ablation에서 모든 initialization variant가 같은 tokenizer를 공유하므로,
> downstream/PPPL 차이는 tokenizer만으로 설명되지 않는다. 이 차이가 바로
> embedding initialization novelty의 실험적 위치다.

## 산출물

| File | 내용 |
| --- | --- |
| `tokenization_effect_summary.tsv` | 언어별 변화율 요약 |
| `tokenization_effect_examples.tsv` | 문장별 base/v5.2 tokenization 비교 |
| `tokenization_effect_change.png` | 언어별 token reduction bar plot |
| `README.md` | 영어 요약 |

## 실행 명령

```bash
python3 scripts/run_v52_tokenization_effect.py
```
