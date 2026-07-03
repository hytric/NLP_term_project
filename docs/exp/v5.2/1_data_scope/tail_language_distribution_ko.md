# Tail Language Corpus-Size Distribution

## 기준

원 Glot500 논문에서 `tail`은 strict corpus-size bin이 아니라 XLM-R coverage
기준이다. 즉 이 문서에서는:

```text
tail = XLM-R에 covered 되지 않은 language-script
```

로 계산한다. 로컬 `miscellaneous/languages_stats.csv` 기준 전체는 `679`
language-script이고, 이 중 XLM-R head는 `100`, non-XLM-R tail은 `579`이다.

## 전체 Tail 분포

이 표의 downstream membership은 현재 repo에서 per-language list를 확인할 수 있는
Tatoeba, Bible, NER, POS 기준이다. 원 논문 Table 3의 Text Classification과 Roundtrip은
coverage count가 있지만, 이 repo에는 같은 형태의 language list가 없어 bucket별
membership에는 포함하지 않는다.

| Bin | Count | Percent | Local task-list any |
| --- | ---: | ---: | ---: |
| `<30k` | 109 | 18.8 | 0 |
| `30k-50k` | 113 | 19.5 | 89 |
| `50k-100k` | 70 | 12.1 | 40 |
| `100k-300k` | 124 | 21.4 | 79 |
| `300k-1M` | 101 | 17.4 | 70 |
| `1M-10M` | 52 | 9.0 | 45 |
| `10M+` | 10 | 1.7 | 10 |

핵심 관찰:

- tail의 median은 `97,041` sentences이다.
- tail의 mean은 `917,731` sentences로 median보다 훨씬 크다.
- 즉 tail 분포는 오른쪽 꼬리가 길고, 소수 high-resource tail이 평균을 크게 올린다.
- local task-list membership은 `30k-100k` strict low-resource tail에도
  존재한다. 주로 Bible retrieval이고, 일부 NER/POS/Tatoeba도 있다.
- 기존 `0` 결론은 task list의 두 번째 컬럼 `0/1`을 availability로 오해한 결과다.
  실제로는 Table 3의 head/tail count와 맞는 head/tail flag다.

## Percentiles

| Percentile | new_length |
| --- | ---: |
| min | 1,201 |
| p10 | 22,134 |
| p25 | 31,997 |
| p50 | 97,041 |
| p75 | 356,561 |
| p90 | 1,070,170 |
| p95 | 2,365,271 |
| p99 | 18,659,517 |
| max | 63,411,156 |

## Local min30k Candidate Pool

실제 target selection에 쓰인 local candidate pool은 더 엄격하다. `non-XLM-R`,
`new_length >= 30k`, local raw/source 조건을 거친 pool은 `318`개다.

| Bin | Count | Percent |
| --- | ---: | ---: |
| `30k-50k` | 73 | 23.0 |
| `50k-100k` | 39 | 12.3 |
| `100k-300k` | 72 | 22.6 |
| `300k-1M` | 74 | 23.3 |
| `1M-10M` | 50 | 15.7 |
| `10M+` | 10 | 3.1 |

v5 target10은 이 pool의 하단 `30k-53k` 구간에 있다. 반면 v5.1 downstream-aware
target들은 `zsm_Latn`을 제외하면 대부분 `1M+`, 일부는 `10M+`에 있다.

## 해석

`tail`이라는 단어만으로는 low-resource claim을 방어하기 어렵다. 원 논문에서
tail은 XLM-R coverage 기준이기 때문에, tail 안에는 `30k` 근처 언어도 있고
`10M+` 언어도 있다.

따라서 v5.2의 최종 표현은 다음과 같이 둔다.

```text
v5 = corpus-size low-resource tail target10 with partial local task-list membership
v5.1 = downstream-aware XLM-R-unseen/tail diagnostic, mostly mid/high-resource
```

이 구분 덕분에 `low-resource target` claim은 유지하면서도, downstream은
`task-list membership`과 `현재 로컬 measured result`를 분리해 보고할 수 있다.
