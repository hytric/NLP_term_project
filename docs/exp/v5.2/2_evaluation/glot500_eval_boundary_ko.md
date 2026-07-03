# Glot500 Evaluation Boundary

## 원 Glot500 Table 3 Coverage

원 Glot500은 모든 downstream task를 511개 전체 언어에 대해 수행하지 않았다. 논문
Table 3은 task별 head/tail language-script 수를 따로 제시한다.

| Task | Head | Tail | Measure |
| --- | ---: | ---: | --- |
| Sentence Retrieval Tatoeba | 70 | 28 | Top10 Acc. |
| Sentence Retrieval Bible | 94 | 275 | Top10 Acc. |
| Text Classification | 90 | 264 | F1 |
| NER | 89 | 75 | F1 |
| POS | 63 | 28 | F1 |
| Roundtrip Alignment | 85 | 288 | Accuracy |

중요한 점은 `tail`이 strict corpus-size bin이 아니라 XLM-R coverage 기준이라는 점이다.
논문은 head를 XLM-R가 cover하는 언어, tail을 그 나머지 언어로 정의한다.

## 우리 실험에 적용

v5 target10은 strict corpus-size low-resource target set이다. 현재 repo에서
per-language list를 확인할 수 있는 Tatoeba/Bible/NER/POS 기준으로는 `8/10`에 일부
downstream task membership이 있다. Table 3의 Text Classification과 Roundtrip은 논문에
coverage count가 있지만, 이 repo에는 같은 형태의 per-language list가 없어 여기서는
별도로 확정하지 않는다.

| v5 target | Local task-list membership |
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

따라서 이전 `0/10` 결론은 철회한다. 다만 기존 v5 local coverage/materialization
산출물은 task list의 두 번째 컬럼 `0/1`을 availability로 오해해서 tail language
task를 건너뛴 흔적이 있다. 이 컬럼은 Table 3 count와 맞는 head/tail flag로 보아야
한다.

논문/발표에서는 repair 전까지 v5 target10에 대해 tokenization/MLM proxy/PPPL 계열
intrinsic evidence를 중심으로 두고, downstream은 `task-list membership exists`와
`measured target claim pending materialization repair`를 분리해 쓴다.

v5.1은 downstream coverage를 target에 붙이려는 diagnostic이다. 그 결과 target이
mid/high-resource로 이동한다는 점 자체가 중요한 limitation evidence다.
