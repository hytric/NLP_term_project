# Target10 재선정 필요성: downstream coverage 기준

작성 시각: 2026-06-28 KST

## 결론

사용자 지적이 맞다. 현재 v5 target10은 Glot500 raw text/PPPL 기준으로는
성립하지만, downstream target evidence를 얻기에는 적절하지 않다.

현재 target10은 모두 아래 상태다.

```text
PPPL raw-text: 10/10
Tatoeba retrieval: 0/10
Bible retrieval: 0/10
Roundtrip alignment: 0/10
Taxi1500: 0/10
NER: 0/10
POS: 0/10
```

따라서 현재 target10으로는 tokenizer/MLM/PPPL 이야기는 가능하지만,
target10에 대해 retrieval/tagging/classification downstream 개선을 직접 주장할
수 없다. 이 실험은 정말 좋은 방향으로 정돈되어 있지만, downstream claim까지
원하면 target10 selection rule을 바꿔야 한다.

## 왜 문제가 되는가?

처음 v5 target10 selection은 다음 기준을 강하게 봤다.

1. Glot500 내부 raw data에 존재한다.
2. `XLM-R=False`이다.
3. `new_length >= 30000`이다.
4. 지역/문자 다양성이 있다.

하지만 이 기준에는 아래 조건이 빠져 있었다.

```text
selected target language must overlap with at least one downstream evaluation resource
```

이 조건이 없으면 target language는 PPPL raw-text에는 들어가지만 Tatoeba/Bible/NER/POS
같은 downstream 평가에는 들어가지 않을 수 있다. 현재 v5 target10이 정확히 이
상태다.

## Candidate Audit 결과

재현 가능한 audit script:

```bash
python3 scripts/audit_v5_target_candidate_task_overlap.py
```

생성 파일:

```text
docs/exp/v5/0_tokenizer/00_data_scope/target_candidate_task_overlap.tsv
docs/exp/v5/0_tokenizer/00_data_scope/target_candidate_task_overlap.md
docs/exp/v5/0_tokenizer/00_data_scope/target_candidate_task_overlap_summary.json
```

요약:

| 항목 | 값 |
| --- | ---: |
| non-XLM-R + min30k Glot500 candidates | 318 |
| candidates with any local downstream coverage | 8 |
| current target10 with any local downstream coverage | 0 |
| candidates with Tatoeba | 3 |
| candidates with Bible retrieval | 6 |
| candidates with Roundtrip | 6 |
| candidates with NER | 6 |
| candidates with POS | 0 |

Score distribution:

| downstream task count | candidate count |
| ---: | ---: |
| 3 | 5 |
| 2 | 3 |
| 0 | 310 |

## Downstream 가능한 후보

`target_task_count`는 Tatoeba, Bible, Roundtrip, NER, POS 중 local coverage가
있는 task 수다. Bible과 Roundtrip은 같은 Bible-derived source에 묶이므로 함께
생기는 경우가 많다.

| language_script | language | script | raw size | task count | Tatoeba | Bible | Roundtrip | NER | POS |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| `guj_Gujr` | Gujarati | Gujr | 45,738,685 | 3 | no | yes | yes | yes | no |
| `srp_Cyrl` | Serbian | Cyrl | 3,864,091 | 3 | no | yes | yes | yes | no |
| `sun_Latn` | Sundanese | Latn | 2,586,011 | 3 | no | yes | yes | yes | no |
| `asm_Beng` | Assamese | Beng | 1,882,353 | 3 | no | yes | yes | yes | no |
| `zsm_Latn` | Standard Malay | Latn | 859,947 | 3 | yes | yes | yes | no | no |
| `aze_Latn` | Azerbaijani | Latn | 46,300,705 | 2 | yes | no | no | yes | no |
| `fil_Latn` | Filipino | Latn | 33,493,255 | 2 | no | yes | yes | no | no |
| `bos_Latn` | Bosnian | Latn | 11,014,744 | 2 | yes | no | no | yes | no |

## Bible로 downstream task를 구성할 수 있는가?

현재 v5 target10 자체는 Bible retrieval에 없다.

```text
current target10 Bible coverage = 0/10
```

따라서 지금 선택된 `fur_Latn`, `krc_Cyrl`, `acm_Arab`, `dzo_Tibt`,
`sat_Olck`, `mad_Latn`, `bam_Latn`, `kjb_Latn`, `quw_Latn`, `rap_Latn`으로는
Bible downstream target claim을 만들 수 없다.

다만 Bible 데이터셋은 로컬에 존재하고, v5 102개 중 74개 언어에 대해 실행된다.
이 경우 가능한 해석은 아래 둘 중 하나다.

| 사용 방식 | 가능 여부 | 해석 |
| --- | --- | --- |
| 현재 v5 target10에 대한 Bible downstream | no | target10 `0/10` coverage라 직접 claim 불가 |
| v5 102개 중 Bible-covered available languages 평가 | yes | Glot500-style available-language replay 가능 |
| 재선정 후보 중 Bible-covered target subset 평가 | yes, v5.1 필요 | target subset downstream evidence 가능 |

non-XLM-R + min30k 후보 중 Bible coverage가 있는 언어는 6개다.

| language_script | language | script | raw size | Bible shared verses | 같이 가능한 task |
| --- | --- | --- | ---: | ---: | --- |
| `guj_Gujr` | Gujarati | Gujr | 45,738,685 | 7,883 | Bible, Roundtrip, NER |
| `srp_Cyrl` | Serbian | Cyrl | 3,864,091 | 7,941 | Bible, Roundtrip, NER |
| `sun_Latn` | Sundanese | Latn | 2,586,011 | 7,938 | Bible, Roundtrip, NER |
| `asm_Beng` | Assamese | Beng | 1,882,353 | 7,939 | Bible, Roundtrip, NER |
| `zsm_Latn` | Standard Malay | Latn | 859,947 | 7,888 | Tatoeba, Bible, Roundtrip |
| `fil_Latn` | Filipino | Latn | 33,493,255 | 7,941 | Bible, Roundtrip |

마감이 가까운 현재 상황에서는 Bible을 새 target10 본실험으로 재구성하지 않는 것이
낫다. 대신 현재 v5에서 Bible retrieval은 `available-language downstream`으로
보고하고, target 언어 직접 downstream은 아래처럼 limitation/future work로 둔다.

```text
The current target10 is not covered by Bible retrieval. Bible retrieval is
therefore reported as an available-language Glot500 metric replay. A corrected
v5.1 target selection would include the six non-XLM-R/min30k languages with
Bible coverage: guj_Gujr, srp_Cyrl, sun_Latn, asm_Beng, zsm_Latn, and fil_Latn.
```

## 현재 target10 상태

| language_script | language | script | raw size | downstream task count |
| --- | --- | --- | ---: | ---: |
| `fur_Latn` | Friulian | Latn | 30,052 | 0 |
| `krc_Cyrl` | Karachay-Balkar | Cyrl | 30,353 | 0 |
| `acm_Arab` | Mesopotamian Arabic | Arab | 44,505 | 0 |
| `dzo_Tibt` | Dzongkha | Tibt | 52,732 | 0 |
| `sat_Olck` | Santali | Olck | 39,614 | 0 |
| `mad_Latn` | Madurese | Latn | 38,993 | 0 |
| `bam_Latn` | Bambara | Latn | 32,150 | 0 |
| `kjb_Latn` | Q'anjob'al | Latn | 31,471 | 0 |
| `quw_Latn` | Tena Lowland Quichua | Latn | 33,449 | 0 |
| `rap_Latn` | Rapanui | Latn | 30,102 | 0 |

## 추천 수정안

target10에서 downstream target evidence를 얻으려면 아래처럼 바꾸는 것이 낫다.

### Option A: downstream 최대화 + 최소 script 다양성

8개 downstream-covered 후보를 모두 포함하고, 남은 2개는 PPPL-only script-diversity
anchor로 둔다.

```text
guj_Gujr
asm_Beng
srp_Cyrl
sun_Latn
zsm_Latn
aze_Latn
fil_Latn
bos_Latn
dzo_Tibt
sat_Olck
```

장점:

- target10 중 8개는 적어도 하나 이상의 downstream task에 직접 들어간다.
- Bible/Roundtrip/NER/Tatoeba target evidence를 얻을 수 있다.
- `dzo_Tibt`, `sat_Olck`로 Tibt/Olck script diversity를 일부 유지한다.

단점:

- target10이 기존보다 high-resource 쪽으로 이동한다.
- POS target coverage는 여전히 없다.
- Taxi1500 target coverage도 없다. 현재 local Taxi1500은 English-only이므로
  target10 selection만으로 해결되지 않는다.

### Option B: strict downstream-only target8

위 8개만 target set으로 두고 target10이라는 이름을 포기한다.

장점:

- 모든 target이 downstream coverage를 가진다.
- target downstream claim이 가장 깨끗하다.

단점:

- target10이 아니라 target8이 된다.
- 기존 "10개 언어" 계획과 다르다.

### Option C: 현재 v5 유지, claim 축소

현재 실행을 그대로 두고, target10 claim은 PPPL/tokenization/MLM proxy에만 둔다.

장점:

- 지금까지 생성한 tokenizer, checkpoint, report/PPT draft를 보존한다.
- 실험을 멈추지 않는다.

단점:

- target10 downstream novelty claim은 불가능하다.
- downstream은 available-language/head/all replay로만 해석해야 한다.

## 추천 결정

보고서에서 downstream task를 novelty의 핵심 축으로 삼으려면 **Option A로
재실행**하는 것이 맞다.

현재 v5를 그대로 사용할 경우 final claim은 아래처럼 제한해야 한다.

```text
The selected target10 supports raw-text PPPL and tokenization/MLM proxy
analysis, but not direct target10 downstream evaluation. Downstream metrics are
reported on available-language Glot500 replay subsets.
```

downstream까지 target evidence를 만들고 싶다면 아래처럼 새 branch를 잡는다.

```text
v5.1 = v5 data/method pipeline + downstream-aware target10
```

v5.1에서 다시 해야 하는 단계:

1. target manifest 재작성.
2. 92 seen + new target10 raw symlink/merge 재생성.
3. tokenizer 재학습 또는 최소한 같은 tokenizer 유지 가능성 검토.
4. random/FVT initialized checkpoint 재생성.
5. matched MLM run 재실행.
6. PPPL + target-overlap downstream rows 재측정.

## 보고서에 바로 쓸 문장

```text
An audit of 318 non-XLM-R Glot500 candidates with at least 30K raw sentences
showed that the initial target10 selection had 0/10 direct downstream coverage
outside PPPL. Therefore, if the paper aims to make target-language downstream
claims, the target set should be revised to include the eight candidates with
local downstream overlap: guj_Gujr, asm_Beng, srp_Cyrl, sun_Latn, zsm_Latn,
aze_Latn, fil_Latn, and bos_Latn.
```
