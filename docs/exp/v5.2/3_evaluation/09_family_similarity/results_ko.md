# v5.2 Family Similarity 결과 요약

## 목적

v5.2 target7은 모두 `Latn` script이므로, 단순히 "라틴 문자라서 가까운가"와
"언어 계통이 가까워서 가까운가"를 분리해서 확인할 수 있다.

이 분석은 모든 비교쌍에 최소 하나의 unseen tail language를 포함하도록 구성했다.
따라서 head language끼리만 비교하는 pair는 없다.

## 실행 범위

| 항목 | 값 |
| --- | ---: |
| sampled languages | 38 |
| sentence points | 3,708 |
| tail-anchored pair rows | 11,956 |
| models | random / mean / fvt step4000 |
| samples per language | up to 100 |
| pair samples per language pair | up to 50 |
| layer | 7, 0-index 기준 layer 8 |

## 비교 기준

| Relation type | 의미 |
| --- | --- |
| `tail_within_language` | 같은 unseen tail 언어 안의 인접 raw 문장 |
| `tail_tail_same_family` | tail 언어끼리 같은 family |
| `tail_tail_same_macro_family` | tail 언어끼리 macro-family만 같음 |
| `tail_tail_different_family` | tail 언어끼리 다른 family |
| `tail_head_same_family` | tail + XLM-R-seen head, 같은 family |
| `tail_head_same_macro_family` | tail + head, macro-family만 같음 |
| `tail_head_different_family_same_script` | tail + head, 둘 다 Latn이지만 family 다름 |
| `tail_head_different_family_different_script` | tail + head, script와 family 모두 다름 |

### family / macro-family 판정 기준

| 기준 | 판정 규칙 | 예시 |
| --- | --- | --- |
| 같은 언어 | `language_script_a == language_script_b` | `dtp_Latn` - `dtp_Latn` |
| 같은 family | `family_a == family_b` | `fur_Latn` - `lij_Latn`: Romance |
| 같은 macro-family | `macro_family_a == macro_family_b` 그리고 `family_a != family_b` | `csb_Latn` - `fur_Latn`: Slavic/Romance, 둘 다 Indo-European |
| 같은 script, 다른 family | `script_a == script_b` 그리고 `family_a != family_b` | `bam_Latn` - `fra_Latn`: 둘 다 Latn, Mande/Romance |
| 다른 script, 다른 family | `script_a != script_b` 그리고 `family_a != family_b` | `bam_Latn` - `ara_Arab`: Latn/Arab, Mande/Semitic |

여기서 `same macro-family`는 `same family`와 겹치지 않도록 더 넓은 계통은 같지만
세부 family는 다른 경우로 제한한다. 따라서 `fur_Latn` - `lij_Latn`은 Romance로
같은 family이고, `csb_Latn` - `fur_Latn`은 Slavic/Romance로 family는 다르지만
Indo-European macro-family가 같다.

| tail language | family | macro-family | region | 가까운 기준 예시 |
| --- | --- | --- | --- | --- |
| `bam_Latn` | Mande | Niger-Congo | West Africa | `xho_Latn`과 same macro-family |
| `csb_Latn` | Slavic | Indo-European | Europe | `ces/hrv/pol/slk/slv`와 same family, `fur/lij`와 same macro-family |
| `dtp_Latn` | Austronesian | Austronesian | Southeast Asia | `ind/jav/mlg/msa/tgl`과 same family |
| `fur_Latn` | Romance | Indo-European | Europe | `lij` 및 `cat/fra/ita/por/ron`과 same family |
| `ile_Latn` | Constructed | Constructed | Constructed/Europe | `epo_Latn`과 same family |
| `lij_Latn` | Romance | Indo-European | Europe | `fur` 및 `cat/fra/ita/por/ron`과 same family |
| `xav_Latn` | Macro-Je | Macro-Je | South America | 현재 sampled subset에서는 가까운 same-family head가 없음 |

### 실제 language-pair bucket

아래 표는 문장 pair 11,956개를 만들기 전에 사용한 unique language-pair 기준이다.
`same macro-family`는 `same family`를 제외한 bucket이다.

| tail-tail bucket | 실제 언어쌍 |
| --- | --- |
| within language | `bam-bam`, `csb-csb`, `dtp-dtp`, `fur-fur`, `ile-ile`, `lij-lij`, `xav-xav` |
| same family | `fur-lij` = Romance |
| same macro-family | `csb-fur`, `csb-lij` = Indo-European macro-family, Slavic/Romance |
| different family | `bam-csb`, `bam-dtp`, `bam-fur`, `bam-ile`, `bam-lij`, `bam-xav`, `csb-dtp`, `csb-ile`, `csb-xav`, `dtp-fur`, `dtp-ile`, `dtp-lij`, `dtp-xav`, `fur-ile`, `fur-xav`, `ile-lij`, `ile-xav`, `lij-xav` |

| tail | same-family head/reference | same macro-family-only head/reference |
| --- | --- | --- |
| `bam_Latn` | 없음 | `xho_Latn` = Niger-Congo, Bantu |
| `csb_Latn` | `ces_Latn`, `hrv_Latn`, `pol_Latn`, `slk_Latn`, `slv_Latn` = Slavic | `cat_Latn`, `fra_Latn`, `ita_Latn`, `por_Latn`, `ron_Latn` = Romance; `deu_Latn`, `eng_Latn`, `nld_Latn` = Germanic; `ell_Grek` = Hellenic; `mar_Deva` = Indo-Aryan |
| `dtp_Latn` | `ind_Latn`, `jav_Latn`, `mlg_Latn`, `msa_Latn`, `tgl_Latn` = Austronesian | 없음 |
| `fur_Latn` | `cat_Latn`, `fra_Latn`, `ita_Latn`, `por_Latn`, `ron_Latn` = Romance | `ces_Latn`, `hrv_Latn`, `pol_Latn`, `slk_Latn`, `slv_Latn` = Slavic; `deu_Latn`, `eng_Latn`, `nld_Latn` = Germanic; `ell_Grek` = Hellenic; `mar_Deva` = Indo-Aryan |
| `ile_Latn` | `epo_Latn` = Constructed | 없음 |
| `lij_Latn` | `cat_Latn`, `fra_Latn`, `ita_Latn`, `por_Latn`, `ron_Latn` = Romance | `ces_Latn`, `hrv_Latn`, `pol_Latn`, `slk_Latn`, `slv_Latn` = Slavic; `deu_Latn`, `eng_Latn`, `nld_Latn` = Germanic; `ell_Grek` = Hellenic; `mar_Deva` = Indo-Aryan |
| `xav_Latn` | 없음 | 없음 |

나머지 tail-head bucket은 contrast set으로 사용했다. unique language-pair 기준으로
`tail_head_different_family_same_script`는 122쌍, `tail_head_different_family_different_script`는
43쌍이다.

## 핵심 결과

raw cosine은 대부분 0.9 근처로 높게 나오므로 transformer sentence embedding의
anisotropy 영향을 받는다. 따라서 발표와 보고서에서는 `centered_cosine`을 중심으로
해석하는 것이 더 안전하다.

FVT step4000 기준:

| Relation type | Pairs | Mean centered cosine |
| --- | ---: | ---: |
| `tail_within_language` | 350 | 0.473229 |
| `tail_tail_same_family` | 50 | 0.306983 |
| `tail_tail_same_macro_family` | 100 | 0.181989 |
| `tail_tail_different_family` | 900 | 0.123785 |
| `tail_head_same_family` | 1,050 | 0.036947 |
| `tail_head_different_family_same_script` | 6,100 | -0.049819 |
| `tail_head_same_macro_family` | 1,550 | -0.063871 |
| `tail_head_different_family_different_script` | 1,856 | -0.078834 |

## 해석

1. 같은 tail 언어 내부 문장이 가장 강하게 모인다.
   이는 language identity와 corpus style이 sentence vector space에서 강하게 작동한다는 의미다.

2. tail끼리 비교해도 family가 가까울수록 centered cosine이 높다.
   `tail_tail_same_family` > `tail_tail_same_macro_family` > `tail_tail_different_family` 순서가 나온다.

3. 같은 Latin script라고 해서 무조건 가까운 것은 아니다.
   FVT 기준 `tail_head_same_family`는 0.036947이고,
   `tail_head_different_family_same_script`는 -0.049819이다.
   즉 같은 Latn script 효과보다 family/typology 효과가 더 설명력이 있다.

4. `tail_head_different_family_same_script`가
   `tail_head_different_family_different_script`보다 덜 낮다.
   이는 script 공유 효과도 일부 존재하지만, family 효과와 분리해서 해석해야 한다.

5. 이 결과는 공식 Glot500 metric이 아니라 novelty/diagnostic 분석이다.
   PPPL, retrieval, downstream 결과를 설명하는 보조 증거로 사용한다.

## 2D point map 판단

언어당 24개 샘플로 만든 초기 plot은 가능성 확인용으로는 충분했지만,
발표용 결론을 내리기에는 약했다. 따라서 최종 그림은 언어당 최대 100개 문장으로
다시 생성했다.

100개 버전 기준으로 보면 centroid map은 비교적 잘 나뉜다. `dtp_Latn`,
`bam_Latn`, `xav_Latn`은 sentence-level point map에서도 비교적 독립적인 영역을
형성한다. 반면 `csb_Latn`, `fur_Latn`, `ile_Latn`, `lij_Latn`은 모두 Latin script
기반 유럽권 언어라 sentence-level point가 상당히 겹친다.

따라서 발표에서는 "언어별 sentence vector가 완전히 분리된다"고 말하지 않는다.
더 안전한 표현은 다음이다.

> Sentence-level point는 완전한 cluster separation을 보이지는 않지만, tail
> language identity와 family/typology에 따른 구조가 centroid와 similarity
> distribution에서 일관되게 관찰된다.

## 생성된 plot

| Plot | 설명 |
| --- | --- |
| `family_pair_boxplot_<model>.png` | relation type별 similarity 분포 |
| `family_centroid_heatmap_<model>.png` | 언어 centroid cosine heatmap |
| `family_point_map_all_<model>.png` | tail + selected head 전체 sentence PCA |
| `family_point_map_tail_only_<model>.png` | tail 언어끼리만 sentence PCA |
| `family_point_map_tail_by_language_<model>.png` | tail 언어별 색상으로 본 sentence PCA |
| `family_point_map_all_tail_highlight_<model>.png` | head는 회색, tail은 언어별 색상으로 강조한 PCA |
| `family_centroid_map_<model>.png` | 언어 centroid PCA |

대표 발표용 plot 후보:

- `family_pair_boxplot_v52_fvt_step4000.png`
- `family_centroid_heatmap_v52_fvt_step4000.png`
- `family_point_map_tail_by_language_v52_fvt_step4000.png`
- `family_point_map_all_tail_highlight_v52_fvt_step4000.png`
- `family_centroid_map_v52_fvt_step4000.png`

## 실행 명령

```bash
GPU=2 bash scripts/run_v52_family_similarity.sh
```
