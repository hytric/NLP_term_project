# Low-Resource Task-Fill Candidates

작성일: 2026-06-28

## 먼저 정정할 점

`new_length <= 10k`를 Glot500 corpus-size 기준으로 엄격하게 적용하면, 현재
`miscellaneous/languages_stats.csv`에서 non-XLM-R tail은 10개뿐이다.

| language_script | new_length | note |
| --- | ---: | --- |
| `mzn_Latn` | 1,201 | no local task-list membership |
| `udm_Latn` | 4,616 | no local task-list membership |
| `koi_Latn` | 4,749 | no local task-list membership |
| `kom_Latn` | 5,538 | no local task-list membership |
| `wuu_Latn` | 5,631 | no local task-list membership |
| `rup_Latn` | 6,794 | no local task-list membership |
| `bod_Latn` | 7,689 | no local task-list membership |
| `mrj_Latn` | 8,755 | no local task-list membership |
| `dty_Deva` | 9,010 | no local task-list membership |
| `ceb_Hani` | 9,433 | no local task-list membership |

따라서 strict corpus `<=10k`로는 아래 task들을 각각 3개씩 채울 수 없다. 원 논문
Table 3의 `tail 200+`는 corpus-size `<=10k`가 아니라 XLM-R-unseen tail 전체를 뜻한다.

`train corpus <=10k`로 해석해도 결론은 같다. v5.1식 strict split처럼 dev/test를
각각 1k씩 뺀다고 가정하면 `train <=10k`는 대략 `new_length <=12k`이다. 이 범위의
non-XLM-R tail은 13개이고, 역시 Tatoeba/Bible/NER/POS task-list membership은 없다.

| language_script | new_length | estimated_train | note |
| --- | ---: | ---: | --- |
| `mzn_Latn` | 1,201 | 0 | no local task-list membership |
| `udm_Latn` | 4,616 | 2,616 | no local task-list membership |
| `koi_Latn` | 4,749 | 2,749 | no local task-list membership |
| `kom_Latn` | 5,538 | 3,538 | no local task-list membership |
| `wuu_Latn` | 5,631 | 3,631 | no local task-list membership |
| `rup_Latn` | 6,794 | 4,794 | no local task-list membership |
| `bod_Latn` | 7,689 | 5,689 | no local task-list membership |
| `mrj_Latn` | 8,755 | 6,755 | no local task-list membership |
| `dty_Deva` | 9,010 | 7,010 | no local task-list membership |
| `ceb_Hani` | 9,433 | 7,433 | no local task-list membership |
| `xmf_Latn` | 10,673 | 8,673 | no local task-list membership |
| `chv_Latn` | 10,693 | 8,693 | no local task-list membership |
| `sat_Latn` | 11,724 | 9,724 | no local task-list membership |

현재 확인 가능한 첫 downstream membership은 대체로 `new_length ~= 30k` 근처에서
시작한다. 단, task별 최저 corpus 언어를 그대로 고르면 task마다 언어가 갈라지므로,
v5.2의 실제 table-fill 후보는 language overlap을 우선한다. 따라서 Bible/Roundtrip/Taxi는
`dtp_Latn`, `xav_Latn`, `bam_Latn`으로 묶고, Tatoeba/Embedding은 `csb_Latn`,
`dtp_Latn`, `ile_Latn`으로 묶는다.

## 실험용 완화 기준

각 task를 실제로 채우려면 기준을 다음처럼 두는 것이 안전하다.

```text
language = non-XLM-R tail
corpus size = roughly <=50k Glot500 sentences
eval item count = <=10k pairs/samples where countable
```

이 기준이면 task별 3개 후보를 만들 수 있다. 또한 언어가 task 간 최대한 겹치도록
overlap-optimized selection을 사용한다.

## 추천 후보

| Task | 3 candidates | Status |
| --- | --- | --- |
| Tatoeba retrieval | `csb_Latn`, `dtp_Latn`, `ile_Latn` | ready: local pair files exist |
| Bible retrieval | `dtp_Latn`, `xav_Latn`, `bam_Latn` | materializable: Bible corpus exists, tail flag 포함 필요 |
| Roundtrip alignment | `dtp_Latn`, `xav_Latn`, `bam_Latn` | materializable after Bible retrieval files |
| NER | `csb_Latn`, `lij_Latn`, `fur_Latn` | ready: PAN-X train/dev/test exist |
| POS | `xav_Latn`, `bam_Latn`, `lij_Latn` | task-list only: UD split materialization needed |
| Taxi1500 | `dtp_Latn`, `xav_Latn`, `bam_Latn` | not local-ready: Taxi1500/PBC generation needed |
| Embedding similarity | `csb_Latn`, `dtp_Latn`, `ile_Latn` | ready: local Tatoeba pairs exist |

이 조합은 총 21개 task slot을 unique 7개 언어로 줄인다.

| language_script | language full name | region | new_length | Covered tasks |
| --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Southeast Asia | 48,468 | Tatoeba, Bible, Roundtrip, Taxi1500, Embedding similarity |
| `xav_Latn` | Xavánte | South America | 31,765 | Bible, Roundtrip, POS, Taxi1500 |
| `bam_Latn` | Bambara | West Africa | 32,150 | Bible, Roundtrip, POS, Taxi1500 |
| `csb_Latn` | Kashubian | Europe | 33,743 | Tatoeba, NER, Embedding similarity |
| `ile_Latn` | Interlingue | Constructed/Europe | 40,984 | Tatoeba, Embedding similarity |
| `lij_Latn` | Ligurian | Europe | 42,447 | NER, POS |
| `fur_Latn` | Friulian | Europe | 30,052 | NER |

상세 표는 `low_resource_task_fill_candidates.tsv`에 둔다.

## 해석

- Table 3의 큰 숫자는 맞다. 다만 그 숫자는 `<=10k corpus` 숫자가 아니다.
- Bible/Roundtrip은 가장 빨리 살릴 수 있다. `/disk3/moon/paralleltext/bibles/corpus`
  원본이 있고, `dtp/xav/bam`은 English와 공유 verse가 각각 `7887/7418/7933`개다.
- NER는 바로 쓸 수 있다. `csb/lij/fur` 모두 local PAN-X train/dev/test가 `100/100/100`
  문장 단위로 있다.
- POS는 Table/list 후보는 있지만 현재 local UD split이 부족하다. `xav`는 local test만
  있고, `bam/lij`는 split을 새로 materialize해야 한다.
- Taxi1500은 논문/원 데이터 기준으로는 가능성이 크지만, 이 repo에는 English split만
  materialized 되어 있다. 원 Taxi1500/PBC generation step 없이는 target 언어 3개를
  measured result로 주장하면 안 된다.
