# 임베딩 초기화 방법 정리 보고

이 문서는 v5.2에서 비교하는 새 vocabulary embedding row 초기화 방법을 보고서에 옮길 수
있도록 정리한 방법론 노트이다. 기준 구현은 `scripts/build_v5_initialized_checkpoint.py`이고,
실제 생성된 감사 artifact는 `/home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_<mode>/`
아래의 `init_report.json` 및 `init_rows.tsv`이다.

## 공통 전제

v5.2는 tokenizer, corpus, MLM objective를 고정하고 새 token embedding row의 초기화 방법만
바꾼다. 이 프로젝트의 설계가 좋은 이유도 여기에 있다. Tokenizer 효과와 initialization 효과를
섞지 않고, Glot500-style vocabulary append 이후 새 row를 어떻게 시작하느냐를 따로 분리한다.

공통 초기화 pipeline은 다음과 같다.

1. `xlm-roberta-base` model/tokenizer와 v5.2 extended tokenizer를 불러온다.
2. base model의 input embedding과 output embedding bias를 복사해 둔다.
3. model embedding matrix를 target tokenizer 크기인 366,666 row로 resize한다.
4. target token이 source vocabulary에도 token string identity로 존재하면 source row를 그대로 복사한다.
5. source에 없는 새 token만 선택한 방법으로 초기화한다.
6. output bias는 기존 token이면 source bias를 복사하고, 새 token이면 0으로 둔다.
7. `model.tie_weights()`로 input/output embedding tie를 복원한다.
8. `<mask>`가 source id 250001에서 target id 366665로 이동한 것을 확인하고,
   `mask_max_abs_diff_after_copy == 0.0`인지 검사한다.

코드 근거는 다음과 같다.

| 항목 | 코드 위치 |
| --- | --- |
| token id prefix를 가정하지 않고 token string identity로 복사한다는 의도 | `scripts/build_v5_initialized_checkpoint.py` lines 2-8 |
| source/target tokenizer 및 base model load, resize | lines 537-559 |
| 기존 token row copy | lines 601-624 |
| 방법별 새 row initialization | lines 625-682 |
| tie/check/audit report | lines 698-749 |

v5.2 actual audit 기준 공통 row 수는 다음과 같다.

| 항목 | 값 |
| --- | ---: |
| source tokenizer length | 250,002 |
| target tokenizer length | 366,666 |
| source identity로 복사된 row | 250,002 |
| 새 target row | 116,664 |
| id가 이동했지만 복사 검증된 token | `<mask>` only |
| `<mask>` source id -> target id | 250001 -> 366665 |
| `mask_max_abs_diff_after_copy` | 0.0 |
| `lm_head_tied_after_init` | true |

## Mean Initialization

### 정의

Mean initialization은 source tokenizer에 이미 있던 lexical token embedding들의 global centroid를
계산하고, 모든 새 token row를 그 centroid로 초기화하는 방법이다.

source lexical id 집합을 `L`, source embedding을 `E_s(i)`라고 하면 다음과 같이 쓸 수 있다.

```text
mu_global = (1 / |L|) * sum_{i in L} E_s(i)
E_t(new_token) = mu_global
```

여기서 `L`은 special token, byte token, 빈 body token을 제외한 source lexical token id이다.

### 코드

주요 코드 위치는 다음과 같다.

| 항목 | 코드 위치 |
| --- | --- |
| lexical source id filtering | `scripts/build_v5_initialized_checkpoint.py` lines 147-161 |
| global mean 계산 | line 569 |
| mean branch | lines 634-637 |

실제 구현은 아래와 같다.

```python
global_mean = source_input[lexical_ids].mean(dim=0)

elif args.mode == "mean" or is_byte_token(token):
    vector = global_mean
    category = "byte_global_mean" if is_byte_token(token) else "global_mean"
```

### 어떻게 초기화하는가

- 기존 token: source row를 그대로 복사한다.
- 새 lexical token: `global_mean`으로 초기화한다.
- 새 byte token: `global_mean`으로 초기화한다.
- output bias: 새 token은 0으로 둔다.

v5.2 audit 결과는 다음과 같다.

| Category | Count |
| --- | ---: |
| `copy_source_identity` | 250,002 |
| `global_mean` | 116,408 |
| `byte_global_mean` | 256 |

### 관련 reference

- Hewitt 2021, *Initializing New Word Embeddings for Pretrained Language Models*: 새 embedding을
  random으로 멀리 흩뿌리기보다 pretrained embedding space의 centroid 근처에서 시작하는
  mean/centroid baseline의 근거로 사용한다.
- Yamaguchi et al. 2025: low-resource vocabulary expansion에서 random initialization이 항상
  충분하지 않으며 heuristic initialization을 비교해야 한다는 동기로 사용한다.
- `docs/survey/vocab_extension_tutorial.pdf`: Mean을 FVT/WECHSEL/FOCUS와 함께 vocabulary
  extension initializer baseline으로 정리한다.

### 보고서에서의 해석 범위

Mean은 surface form이나 family 정보를 쓰지 않는다. 따라서 strong-but-simple centroid baseline으로
두는 것이 적절하다. 이 방법이 높게 나오면 "복잡한 surface heuristic이 항상 우월하지 않다"는
반례가 되므로, FVT 계열의 결과를 해석할 때 반드시 함께 제시해야 한다.

## FVT Initialization

### 정의

FVT는 새 target token surface를 source tokenizer로 다시 tokenize한 뒤, 그 source subtoken
embedding들의 평균으로 새 row를 초기화한다. 이 문서에서는 강의노트의 표현을 따라
`FVT (source-tokenizer decomposition)`으로 부른다.

새 token `a`를 source tokenizer `T_s`로 분해해 source pieces `p_1 ... p_k`를 얻으면 다음과 같다.

```text
T_s(surface(a)) = [p_1, ..., p_k]
E_t(a) = (1 / k) * sum_j E_s(p_j)
```

단, source piece가 special token, `<unk>`, byte token이거나 source embedding row 범위 밖이면
제외한다. 유효한 source piece가 없으면 global mean으로 fallback한다.

### 코드

주요 코드 위치는 다음과 같다.

| 항목 | 코드 위치 |
| --- | --- |
| token surface 변환 | `piece_to_surface`, lines 91-92 |
| FVT vector 계산 | `fvt_vector`, lines 186-219 |
| FVT branch/fallback | lines 651-674 |

실제 구현은 아래와 같다.

```python
surface = piece_to_surface(token)
pieces = base_tokenizer.tokenize(surface)
...
embeddings = source_input[ids]
return embeddings.mean(dim=0), ids, used_pieces, "source_subtoken_mean"
```

### 어떻게 초기화하는가

- 기존 token: source row를 그대로 복사한다.
- 새 byte token: global mean으로 초기화한다.
- 새 lexical token:
  - source tokenizer decomposition이 성공하면 source subtoken embedding 평균으로 초기화한다.
  - 실패하면 global mean으로 fallback한다.
- output bias: 새 token은 0으로 둔다.

예시 row는 다음과 같다.

| New token | Source pieces | Category |
| --- | --- | --- |
| `▁hã` | `▁`, `hã` | `source_subtoken_mean` |
| `▁norĩ` | `▁nor`, `ĩ` | `source_subtoken_mean` |
| `▁ãma` | `▁`, `ã`, `ma` | `source_subtoken_mean` |

v5.2 audit 결과는 다음과 같다.

| Category | Count |
| --- | ---: |
| `copy_source_identity` | 250,002 |
| `source_subtoken_mean` | 116,406 |
| `byte_global_mean` | 256 |
| `global_mean_fallback` | 2 |

Fallback 예시는 zero-width joiner token인 `‍`, `▁‍`이다.

### 관련 reference

- Gee et al. 2022/2024, *Fast Vocabulary Transfer for Language Model Compression*: FVT의 primary
  vocabulary-transfer reference이다. 원래 목적은 compression/efficiency지만, 핵심 아이디어는
  새 tokenizer token을 source tokenizer decomposition에 연결하는 것이다.
- `docs/survey/vocab_extension_tutorial.pdf`: FVT를 "source-tokenizer decomposition"으로 설명하고,
  same-script/domain compression setting에서 적합한 방법으로 정리한다.
- Yamaguchi et al. 2025: low-resource vocabulary expansion에서 heuristic initialization 비교의
  필요성을 뒷받침한다.

### 보고서에서의 해석 범위

FVT는 source tokenizer가 target surface를 잘 분해할 수 있을 때 강하다. 하지만 semantic alignment를
직접 쓰는 WECHSEL/FOCUS와는 다르다. v5.2 Target7은 모두 Latin script이므로, source-tokenizer
decomposition이 작동하기 좋은 조건이라는 점을 함께 설명해야 한다.

## Weighted FVT Initialization

### 정의

Weighted FVT는 FVT와 같은 source tokenizer decomposition을 쓰되, source subtoken embedding을
단순 평균하지 않고 source piece surface length로 가중 평균한다.

```text
w_j = max(1, len(token_body(p_j)))
E_t(a) = sum_j w_j * E_s(p_j) / sum_j w_j
```

직관은 긴 source subtoken이 짧은 punctuation 또는 word-boundary token보다 더 많은 lexical signal을
가질 수 있다는 것이다.

### 코드

주요 코드 위치는 다음과 같다.

| 항목 | 코드 위치 |
| --- | --- |
| `token_surface_length` | lines 99-100 |
| `fvt_vector(..., length_weighted=True)` | lines 186-219 |
| weighted FVT branch | lines 651-665 |

실제 구현은 아래와 같다.

```python
weights = torch.tensor(
    [token_surface_length(piece) for piece in used_pieces],
    dtype=embeddings.dtype,
    device=embeddings.device,
)
vector = (embeddings * weights.unsqueeze(1)).sum(dim=0) / weights.sum()
```

### 어떻게 초기화하는가

- 기존 token: source row를 그대로 복사한다.
- 새 byte token: global mean으로 초기화한다.
- 새 lexical token:
  - source decomposition이 성공하면 length-weighted source subtoken mean으로 초기화한다.
  - 실패하면 global mean으로 fallback한다.
- output bias: 새 token은 0으로 둔다.

예시 row는 다음과 같다.

| New token | Source pieces | Category |
| --- | --- | --- |
| `▁hã` | `▁`, `hã` | `source_subtoken_length_weighted_mean` |
| `▁norĩ` | `▁nor`, `ĩ` | `source_subtoken_length_weighted_mean` |
| `▁ãma` | `▁`, `ã`, `ma` | `source_subtoken_length_weighted_mean` |

v5.2 audit 결과는 다음과 같다.

| Category | Count |
| --- | ---: |
| `copy_source_identity` | 250,002 |
| `source_subtoken_length_weighted_mean` | 116,406 |
| `byte_global_mean` | 256 |
| `global_mean_fallback` | 2 |

### 관련 reference

- 직접적인 기반은 FVT / average-subword decomposition 계열이다. 즉 Gee et al. 및 강의노트가
  가장 가까운 reference이다.
- length weighting 자체는 v5.2 local refinement이다. 따라서 보고서에서는 "our weighted FVT variant"
  또는 "FVT의 surface-length weighted variant"라고 써야 한다.

### 보고서에서의 해석 범위

Weighted FVT는 모든 source subtoken이 같은 비중을 가져야 하는지 검증하는 ablation이다. 새 tokenizer도
아니고 새 objective도 아니다. 바뀌는 것은 새 lexical row를 만들 때 source subtoken embedding을
합치는 방식뿐이다.

## Family-Aware Mean Initialization

### 정의

Family-aware mean은 source tokenizer decomposition을 직접 쓰지 않고, target token이 어떤 language
family의 corpus에서 얼마나 등장했는지를 이용한다. 먼저 target7과 같은 family에 속하고 raw corpus가
있는 language들을 scan한다. 각 family마다 source-token frequency-weighted embedding centroid를
만들고, 새 target token이 family별로 관측된 빈도에 따라 family centroid들을 다시 weighted mean한다.

두 단계 수식으로 쓰면 다음과 같다.

```text
mu_family(f) = sum_i c_f(i) * E_s(i) / sum_i c_f(i)
E_t(a) = sum_f c_a(f) * mu_family(f) / sum_f c_a(f)
```

여기서 `c_f(i)`는 family `f`의 corpus를 source tokenizer로 tokenize했을 때 source token id `i`가
나온 횟수이고, `c_a(f)`는 target tokenizer로 tokenize했을 때 새 target token `a`가 family `f`
corpus에서 나온 횟수이다.

### 코드

주요 코드 위치는 다음과 같다.

| 항목 | 코드 위치 |
| --- | --- |
| target7 language list | lines 28-36 |
| language family map | lines 38-79 |
| family source weighted mean helper | lines 278-291 |
| family scan/provenance build | lines 294-430 |
| final family-weighted vector | lines 433-450 |
| family branch/fallback | lines 638-650 |
| launcher의 5,000 example cap | `scripts/run_v52_build_initializers.sh` |

실제 구현은 아래와 같다.

```python
family_source_counts[family][idx] += 1
token_family_counts[piece][family] += 1

family_means[family] = weighted_embedding_mean(source_input, counts_by_id)

vectors = torch.stack([family_means[family] for family, _ in usable], dim=0)
weights = torch.tensor([count for _, count in usable], dtype=vectors.dtype, device=vectors.device)
vector = (vectors * weights.unsqueeze(1)).sum(dim=0) / weights.sum()
```

### 어떻게 초기화하는가

- 기존 token: source row를 그대로 복사한다.
- 새 byte token: global mean으로 초기화한다.
- 새 lexical token:
  - target token이 family provenance scan에서 관측되면 family-frequency weighted mean으로 초기화한다.
  - family provenance가 없으면 global mean으로 fallback한다.
- output bias: 새 token은 0으로 둔다.

v5.2 family scan 요약은 다음과 같다.

| 항목 | 값 |
| --- | --- |
| target languages | `dtp_Latn`, `xav_Latn`, `bam_Latn`, `csb_Latn`, `ile_Latn`, `lij_Latn`, `fur_Latn` |
| target families | Austronesian, Constructed, Macro-Je, Mande, Romance, Slavic |
| source scan languages | 23 languages |
| max examples per language | 5,000 |
| token-family rows observed | 32,461 |

Family source totals from audit:

| Family | Unique source ids | Source pieces |
| --- | ---: | ---: |
| Austronesian | 35,586 | 895,471 |
| Constructed | 21,348 | 317,418 |
| Macro-Je | 1,425 | 703,757 |
| Mande | 8,609 | 238,845 |
| Romance | 41,032 | 1,300,278 |
| Slavic | 37,766 | 910,542 |

예시 row는 다음과 같다.

| New token | Family weights | Category |
| --- | --- | --- |
| `▁hã` | `Macro-Je:17683,Romance:1` | `family_frequency_weighted_mean` |
| `▁norĩ` | `Macro-Je:6199` | `family_frequency_weighted_mean` |
| `▁bɛ` | `Mande:3439` | `family_frequency_weighted_mean` |

v5.2 audit 결과는 다음과 같다.

| Category | Count |
| --- | ---: |
| `copy_source_identity` | 250,002 |
| `family_frequency_weighted_mean` | 32,461 |
| `global_mean_fallback` | 83,947 |
| `byte_global_mean` | 256 |

### 관련 reference

- 이 이름의 직접적인 기존 방법은 아니다. v5.2 local exploratory method로 보고해야 한다.
- 동기는 Glot500의 head/tail 및 language-family 분석, 그리고
  `docs/exp/v5.2/3_evaluation/09_family_similarity/`의 family representation diagnostic에서 온다.
- WECHSEL/FOCUS는 informed initialization이 auxiliary signal 또는 overlap anchor를 활용할 수
  있음을 보여주는 관련 연구로만 사용한다. v5.2 family-aware mean은 WECHSEL/FOCUS 구현이 아니라
  더 단순한 corpus-provenance prior이다.

### 보고서에서의 해석 범위

Family-aware mean은 exploratory ablation으로 설명해야 한다. 장점은 모든 initialized token에 대해
`family_weights`가 기록되어 해석 가능하다는 점이다. 단점은 coverage가 sparse하다는 점이다.
현재 v5.2 audit에서는 새 row 116,664개 중 32,461개만 family-specific vector를 받고, 83,947개는
global mean으로 fallback한다. 따라서 결과를 해석할 때 "partial family prior"라고 써야지,
FVT를 완전히 대체하는 방법이라고 쓰면 안 된다.

## 방법 비교 요약

| Method | token surface 사용 | source tokenizer 사용 | corpus provenance 사용 | fallback |
| --- | --- | --- | --- | --- |
| mean | no | no | no | 자체가 fallback baseline |
| FVT | yes | yes | no | global mean |
| weighted FVT | yes | yes | no | global mean |
| family-aware mean | yes, target-token occurrence로 사용 | family centroid 계산에 사용 | yes | global mean |

## 보고서에 넣을 reference

현재 `docs/paper/tex/references.bib`에 들어간 primary references:

- Imani et al. 2023, Glot500: vocabulary extension + continued MLM framing.
- Conneau et al. 2020, XLM-R source model.
- Kudo and Richardson 2018, SentencePiece.
- Yamaguchi et al. 2025, low-resource vocabulary expansion and initialization motivation.
- Hewitt 2021, mean/centroid initialization.
- Jung 2026 course note, vocabulary extension tutorial with Mean/FVT/WECHSEL/FOCUS comparison.
- Gee et al. 2022/2024, Fast Vocabulary Transfer.
- Minixhofer et al. 2022, WECHSEL.
- Dobler and de Melo 2023, FOCUS.

최종 보고서에서 가장 안전한 문장은 다음과 같다.

```text
Mean and FVT are literature-grounded vocabulary-extension initializers. Weighted FVT and
family-aware mean are v5.2 local ablations derived from the same principle: keep tokenizer,
corpus, and MLM training fixed, and vary only how new embedding rows are initialized.
```

한국어 본문에서는 다음처럼 쓰면 된다.

```text
Mean과 FVT는 기존 vocabulary extension 문헌에 근거한 초기화 방법이다. Weighted FVT와
family-aware mean은 같은 tokenizer, 같은 corpus, 같은 MLM training 조건에서 새 embedding row를
어떻게 초기화하느냐만 바꿔 보기 위해 추가한 v5.2 local ablation이다.
```
