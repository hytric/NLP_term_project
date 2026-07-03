# Task List Flag Correction

작성일: 2026-06-28

## 정정 요지

`evaluation/*/*_lang_list.txt` 파일의 두 번째 컬럼 `0/1`은 downstream availability가
아니다. 원 Glot500 Table 3의 head/tail count와 일치하는 head/tail flag로 해석해야
한다.

즉:

```text
1 = XLM-R-covered head language-script
0 = non-XLM-R tail language-script
```

availability는 `flag == 1`이 아니라 해당 language-script가 task list에 존재하는지로
판단한다.

## Table 3와 로컬 리스트 count

| Task list | Total | Flag 1/head | Flag 0/tail | Table 3 |
| --- | ---: | ---: | ---: | --- |
| Tatoeba | 98 | 70 | 28 | 70 head / 28 tail |
| Bible | 369 | 94 | 275 | 94 head / 275 tail |
| NER | 164 | 89 | 75 | 89 head / 75 tail |
| POS | 91 | 63 | 28 | 63 head / 28 tail |

이 count가 Table 3와 맞으므로, `0`을 unavailable로 처리하면 tail downstream coverage를
대량으로 누락한다.

## v5 target10 local task-list membership

아래 표는 현재 repo에서 per-language list를 직접 확인할 수 있는 Tatoeba, Bible, NER,
POS 기준이다. 원 논문 Table 3의 Text Classification과 Roundtrip은 task-level coverage
count가 있지만, 같은 형태의 language list가 현재 repo에 없어 이 표에는 포함하지 않는다.

| language_script | Local task-list membership |
| --- | --- |
| `fur_Latn` | NER |
| `rap_Latn` | Bible |
| `krc_Cyrl` | Bible |
| `kjb_Latn` | Bible |
| `bam_Latn` | Bible, POS |
| `quw_Latn` | Bible |
| `mad_Latn` | Bible |
| `sat_Olck` | none |
| `acm_Arab` | none |
| `dzo_Tibt` | Bible |

따라서 v5 target10은 현재 확인 가능한 local task-list 기준 `8/10`에 일부 downstream membership이
있다.

## 보고 경계

기존 로컬 coverage/materialization 산출물은 이 flag를 잘못 해석한 흔적이 있으므로,
그 결과만 보고 `target downstream 0/10`이라고 쓰면 안 된다. 반대로 아직 재실행 없이
`target downstream 성능 향상`을 주장해서도 안 된다.

안전한 표현:

```text
The v5 low-resource target set has partial local Glot500 task-list
membership, mainly in Bible retrieval and partly in NER/POS. Existing local
materialization underestimated tail coverage because it treated the task-list
head/tail flag as an availability flag; measured target-language downstream
claims are therefore deferred until the materialization logic is repaired.
```
