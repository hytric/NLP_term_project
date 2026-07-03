# Hybrid 10k + 30k Language Selection

작성일: 2026-06-28

## 선택 원칙

사용자 결정:

```text
10k 요소를 최대한 집어넣고, downstream이 부족한 부분은 30k 근처 언어로 채운다.
```

이 원칙이 가장 방어력이 좋다. strict `<=10k` 언어는 진짜 low-resource라는 점을 강하게
보여주지만, 현재 repo 기준 downstream membership이 없다. 따라서 역할을 나눈다.

```text
core_10k = MLM/tokenization/PPPL/embedding-init intrinsic target
fallback_30k = downstream table을 채우는 task-specific target
```

## Core 10k Set

`new_length <=10k`를 우선 넣고, `train <=10k`로 해석되는 `new_length <=12k` 언어까지
확장하면 총 13개를 core pool로 둘 수 있다.

| priority | language_script | new_length | estimated_train | role |
| ---: | --- | ---: | ---: | --- |
| 1 | `mzn_Latn` | 1,201 | 0 | intrinsic only, small split policy 필요 |
| 2 | `udm_Latn` | 4,616 | 2,616 | intrinsic core |
| 3 | `koi_Latn` | 4,749 | 2,749 | intrinsic core |
| 4 | `kom_Latn` | 5,538 | 3,538 | intrinsic core |
| 5 | `wuu_Latn` | 5,631 | 3,631 | intrinsic core |
| 6 | `rup_Latn` | 6,794 | 4,794 | intrinsic core |
| 7 | `bod_Latn` | 7,689 | 5,689 | intrinsic core |
| 8 | `mrj_Latn` | 8,755 | 6,755 | intrinsic core |
| 9 | `dty_Deva` | 9,010 | 7,010 | intrinsic core |
| 10 | `ceb_Hani` | 9,433 | 7,433 | intrinsic core |
| 11 | `xmf_Latn` | 10,673 | 8,673 | train<=10k core |
| 12 | `chv_Latn` | 10,693 | 8,693 | train<=10k core |
| 13 | `sat_Latn` | 11,724 | 9,724 | train<=10k core |

만약 target 수를 반드시 10개로 제한해야 하면 priority 1-10을 사용한다. target 수를
늘릴 수 있으면 13개 모두 넣는 것이 `train corpus <=10k` 취지에 더 맞다.

## 30k Fallback Set

downstream task는 10k core에서 채워지지 않으므로, task별 첫 available low-resource
구간인 30k 근처 언어로 채운다.

| Task | fallback languages | reason |
| --- | --- | --- |
| Bible retrieval | `dtp_Latn`, `xav_Latn`, `bam_Latn` | 30k-48k, POS/Tatoeba/Taxi와 overlap |
| Roundtrip alignment | `dtp_Latn`, `xav_Latn`, `bam_Latn` | Bible-derived JSONL로 바로 연결 |
| Taxi1500 | `dtp_Latn`, `xav_Latn`, `bam_Latn` | PBC/Taxi1500 generation 후보, local-ready는 아님 |
| NER | `csb_Latn`, `lij_Latn`, `fur_Latn` | PAN-X local train/dev/test ready, Tatoeba/POS와 overlap |
| POS | `xav_Latn`, `bam_Latn`, `lij_Latn` | POS task-list 후보, UD split 필요 |
| Tatoeba retrieval | `csb_Latn`, `dtp_Latn`, `ile_Latn` | Tatoeba ready 후보 중 NER/Bible과 overlap |
| Embedding similarity | `csb_Latn`, `dtp_Latn`, `ile_Latn` | Tatoeba와 동일 후보를 재사용 |

Overlap-optimized fallback은 21개 task slot을 unique 7개 언어로 줄인다.

| language_script | language full name | region | new_length | Covered tasks |
| --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Southeast Asia | 48,468 | Tatoeba, Bible, Roundtrip, Taxi1500, Embedding similarity |
| `xav_Latn` | Xavánte | South America | 31,765 | Bible, Roundtrip, POS, Taxi1500 |
| `bam_Latn` | Bambara | West Africa | 32,150 | Bible, Roundtrip, POS, Taxi1500 |
| `csb_Latn` | Kashubian | Europe | 33,743 | Tatoeba, NER, Embedding similarity |
| `ile_Latn` | Interlingue | Constructed/Europe | 40,984 | Tatoeba, Embedding similarity |
| `lij_Latn` | Ligurian | Europe | 42,447 | NER, POS |
| `fur_Latn` | Friulian | Europe | 30,052 | NER |

## 최종 구조

```text
Layer A: 10k core languages
  - 목적: MLM/tokenization/PPPL 중심의 진짜 저자원 evidence
  - downstream claim 없음

Layer B: 30k task-fill languages
  - 목적: Glot500-style downstream table 채우기
  - task별 coverage/materialization/metric row를 incremental하게 갱신
```

## 보고 문장

```text
We prioritize languages with <=10k estimated training examples for the intrinsic
low-resource adaptation target set. Because no such languages have local
downstream task membership, we fill downstream-specific rows with the nearest
available non-XLM-R low-resource languages, mostly around 30k cleaned sentences.
```

한국어:

```text
intrinsic/MLM target은 train corpus 10k 이하 언어를 최대한 포함한다. 단, 이 범위에는
로컬 downstream membership이 없으므로, downstream table은 가장 가까운 available
low-resource 구간인 30k 근처 언어로 task별 보충한다.
```

## Claim Boundary

- `10k core` 결과는 tokenizer, PPPL, MLM proxy, embedding initialization 중심으로 해석한다.
- `30k fallback` 결과는 downstream task-fill evidence로 해석한다.
- 두 set을 합쳐서 무조건 하나의 homogeneous target10이라고 부르지 않는다.
- 30k fallback 언어가 MLM corpus에 포함되지 않은 경우, 그 metric은 target adaptation이
  아니라 available-language replay이다.
