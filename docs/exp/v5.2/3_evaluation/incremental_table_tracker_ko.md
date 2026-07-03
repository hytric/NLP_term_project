# Incremental Table Tracker

작성일: 2026-06-28

## 운영 원칙

MLM 학습이 끝날 때까지 기다리지 않고 표를 계속 채운다. 단, 표의 성격을 분리한다.

```text
1. coverage/materialization table = 지금 작성 가능
2. checkpoint metric table = MLM checkpoint가 생길 때마다 갱신
3. final claim table = paired random/FVT 결과가 모두 파싱된 뒤에만 승격
```

이렇게 하면 내일 오전까지도 보고서가 빈 표처럼 보이지 않는다. 대신 어떤 row가
`ready`, `materializable`, `pending`, `not_local_ready`인지 명확히 남긴다.

## Task별 상태

| Task | 후보 | 지금 채울 수 있는 표 | MLM 중 갱신 | Final gate |
| --- | --- | --- | --- | --- |
| Tatoeba | `csb_Latn`, `dtp_Latn`, `ile_Latn` | pair count, coverage | checkpoint retrieval rows | paired random/FVT parsed |
| Bible | `dtp_Latn`, `xav_Latn`, `bam_Latn` | shared verse count, materialization plan | materialized files, retrieval rows | paired random/FVT parsed |
| Roundtrip | `dtp_Latn`, `xav_Latn`, `bam_Latn` | Bible-derived plan | JSONL, alignment rows | paired random/FVT parsed |
| NER | `csb_Latn`, `lij_Latn`, `fur_Latn` | train/dev/test count | checkpoint NER rows | paired random/FVT test rows |
| POS | `xav_Latn`, `bam_Latn`, `lij_Latn` | Table 3 91-language coverage, `pos_rebuilt` count | recovered split metric rows | paired random/mean/FVT parsed |
| Taxi1500 | `dtp_Latn`, `xav_Latn`, `bam_Latn` | Table 3/local-missing note | pending until PBC/Taxi generation | no claim without target files |
| Embedding similarity | `csb_Latn`, `dtp_Latn`, `ile_Latn` | pair count | similarity scores/plots per checkpoint | diagnostic only |

## 오전 제출용 표현

안전한 문장:

```text
We maintain the low-resource task table incrementally during MLM training.
Coverage and materialization rows are filled before training finishes, while
model-dependent metric cells remain checkpoint-gated. POS is evaluated on the
recovered Table 3 split, while Taxi1500 is kept as a pending/local-data-limited
row rather than being silently dropped.
```

한국어 버전:

```text
MLM 학습 중에도 low-resource task table은 계속 갱신한다. 학습 완료 전에는
coverage, pair/sample count, materialization 상태를 먼저 채우고, 모델 checkpoint가
생길 때마다 metric column을 추가한다. POS는 복구된 Table 3 split 기준으로
평가하고, Taxi1500은 local data 한계 때문에 pending row로 남기며, measured
result처럼 주장하지 않는다.
```

## 바로 할 일

1. `low_resource_task_fill_candidates.tsv`를 main coverage table의 후보 입력으로 쓴다.
2. Bible materializer를 tail flag 포함으로 다시 돌려 `dtp/xav/bam` pair 파일을 만든다.
3. Bible 결과를 바탕으로 `dtp/xav/bam` roundtrip JSONL을 만든다.
4. NER는 `csb/lij/fur` target subset count와 metric row를 분리해서 집계한다.
5. POS는 `pos_rebuilt` 기준 91개 Table 3 언어 결과로 넣고, Taxi1500은 pending/materialization-needed row로 표에 넣는다.
6. Embedding similarity는 Tatoeba와 겹치는 `csb/dtp/ile` pair count를 먼저 넣고 checkpoint별 score를 나중에 붙인다.
