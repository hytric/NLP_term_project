# v5 언어 소스와 Coverage Overlap

작성 시각: 2026-06-28 KST

이 문서는 v5에서 말하는 "XLM-R 학습 언어", "별도로 내려받은 Glot500 raw
data", "downstream/evaluation data"가 어떻게 다른지와, 각 metric이 어떤
언어 subset을 실제로 갖는지를 정리한다.

## 핵심 결론

v5의 denominator는 항상 controlled `102` language-script subset이다.

```text
102 = 92 XLM-R-seen language-scripts + 10 Glot500-internal target language-scripts
```

중요한 구분:

- `XLM-R=True`는 **XLM-R pretraining에 포함된 언어인지에 대한 metadata label**이다.
- v5에서 실제 tokenizer/MLM/PPPL에 사용한 local raw text는 102개 모두
  **별도로 내려받아 연결한 Glot500 raw text**이다.
- downstream data는 또 다른 layer다. Tatoeba, Bible, Taxi1500, NER, POS,
  Roundtrip은 local evaluation dataset과 v5 102 언어의 intersection만 가진다.
- 따라서 아래 coverage 숫자는 전체 task dataset의 언어 수가 아니라,
  **v5 102 Glot500 subset 안에서 해당 metric을 실행할 수 있는 언어 수**이다.

## Data Layer 구분

| Layer | 의미 | 실제 위치/근거 | 언어 수 | 해석 |
| --- | --- | --- | ---: | --- |
| XLM-R membership | XLM-R 학습에 들어간 언어인지 여부 | `0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv`의 `XLM-R` column | yes `92`, no `10` | seen/head vs target/tail를 나누는 label |
| v5 Glot500 raw text | tokenizer/continued MLM/PPPL에 쓰는 local raw corpus | `/home/axt/mnt2/jongha/v5_glot50010/raw` | `102` | 92 seen + 10 target 모두 local raw text 있음 |
| v5 merged MLM corpus | 102개 raw text를 sampling/merge한 train corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt` | `102` | tokenizer train과 continued MLM의 공통 train source |
| task eval data | Glot500 metric family별 local evaluation resource | `evaluation/download_data/download`, coverage TSVs | task별 상이 | available-language replay로 해석 |

주의: "XLM-R 학습 언어"라고 해서 v5가 XLM-R 원본 pretraining corpus를 다시
사용했다는 뜻은 아니다. v5는 Glot500 raw text를 사용하되, 그 언어가 XLM-R에
이미 있었는지 여부로 `seen92`와 `target10`을 나눈다.

## 언어 Set

### XLM-R-seen 92

아래 92개는 `XLM-R=True`인 language-script이고, v5에서는 head/seen side로
사용한다. 이들도 모두 local Glot500 raw directory가 있다.

```text
lao_Laoo, mya_Mymr, ara_Arab, mar_Deva, hau_Latn, uzb_Latn,
slv_Latn, fin_Latn, hun_Latn, cmn_Hani, est_Latn, bre_Latn,
hrv_Latn, jav_Latn, ron_Latn, ell_Grek, nor_Latn, slk_Latn,
vie_Latn, amh_Ethi, epo_Latn, bel_Cyrl, xho_Latn, hin_Deva,
tam_Taml, mon_Cyrl, ces_Latn, san_Deva, hye_Armn, pus_Arab,
som_Arab, kan_Knda, isl_Latn, ori_Orya, afr_Latn, deu_Latn,
urd_Arab, bul_Cyrl, tgl_Latn, eus_Latn, pol_Latn, lat_Latn,
tur_Latn, fra_Latn, cat_Latn, uig_Arab, arb_Arab, sqi_Latn,
sin_Sinh, msa_Latn, swh_Latn, kor_Hang, ukr_Cyrl, kir_Cyrl,
yid_Hebr, heb_Hebr, nld_Latn, fry_Latn, azb_Arab, glg_Latn,
fas_Arab, eng_Latn, mkd_Cyrl, ind_Latn, por_Latn, spa_Latn,
dan_Latn, khm_Khmr, gla_Latn, uig_Latn, kat_Geor, mlg_Latn,
snd_Arab, ita_Latn, hau_Arab, cym_Latn, srp_Latn, zho_Hani,
tha_Thai, swe_Latn, pan_Guru, prs_Arab, pes_Arab, san_Latn,
kaz_Cyrl, kur_Latn, mal_Mlym, nep_Deva, gle_Latn, swa_Latn,
som_Latn, lit_Latn
```

### Glot500-internal target10

아래 10개는 `XLM-R=False`, `new_length >= 30000`, raw directory 존재 조건을
만족하도록 Glot500 내부에서 고른 target language-script이다.

| language_script | region/note | source_sentences_new_length | mlm_train_samples |
| --- | --- | ---: | ---: |
| `fur_Latn` | Europe | 30052 | 901560 |
| `krc_Cyrl` | North Caucasus | 30353 | 904259 |
| `acm_Arab` | West Asia | 44505 | 1014273 |
| `dzo_Tibt` | Himalaya | 52732 | 1067222 |
| `sat_Olck` | South Asia | 39614 | 979461 |
| `mad_Latn` | Southeast Asia | 38993 | 974829 |
| `bam_Latn` | West Africa | 32150 | 919998 |
| `kjb_Latn` | Mesoamerica | 31471 | 914125 |
| `quw_Latn` | Andean South America | 33449 | 930995 |
| `rap_Latn` | Polynesia | 30102 | 902009 |

이 target10은 PPPL/raw-text에는 모두 포함되지만, 현재 local downstream task
coverage gate 기준으로는 Tatoeba/Bible/Roundtrip/Taxi1500/NER/POS 직접 coverage가
없다.

## Metric Coverage Overlap

아래 표는 사용자가 적어둔 metric별 language count를 v5 102 denominator와
XLM-R-seen/target10 split으로 풀어쓴 것이다.

| Metric family | v5 denominator | has data total | XLM-R-seen overlap | target10 overlap | missing/block | 해석 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| PPPL raw-text | 102 | 102 | 92 | 10 | 0 | v5 raw text가 102개 모두 있으므로 target10 직접 평가 가능 |
| Tatoeba retrieval | 102 | 63 | 63 | 0 | 39 | available seen-language retrieval replay |
| Bible retrieval | 102 | 74 | 74 | 0 | 28 | available seen-language Bible retrieval replay |
| Roundtrip alignment | 102 | 74 | 74 | 0 | 28 | Bible coverage와 같은 seen-language alignment replay |
| Taxi1500 classification | 102 | 1 | 1 | 0 | 101 | 현재 local materialization은 `eng_Latn`만 있음 |
| NER | 102 | 78 | 78 | 0 | 24 | available seen-language tagging replay |
| POS | 102 | 58 | 58 | 0 | 44 | available seen-language tagging replay |

요약하면, PPPL은 target10을 직접 볼 수 있다. 나머지 downstream task는 지금
상태에서 target10 성능을 직접 주장하는 자료가 아니라, Glot500-style metric
family를 available-language/head/all setting으로 재현한 자료다.

중요한 correction: target-language downstream evidence가 목표라면 현재 target10은
부적절하다. 318개 non-XLM-R/min30k 후보를 audit한 결과, downstream coverage가
하나라도 있는 후보는 8개뿐이고 현재 target10은 그 8개를 하나도 포함하지 않는다.
자세한 재선정안은 `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md`와
`0_tokenizer/00_data_scope/target_candidate_task_overlap.md`를 본다.

## 각 항목이 무슨 데이터셋인가?

아래 항목들은 모두 v5에서 유지하는 Glot500-style evaluation surface에 속한다.
다만 "Glot500 평가 항목"이라는 뜻이지, 원천 데이터가 모두 같은 파일이라는 뜻은
아니다. 원천은 raw Glot500 text, Tatoeba, Bible/PBC 계열 parallel text,
Taxi1500, PAN-X/WikiAnn, Universal Dependencies로 나뉜다.

| Coverage row | 원천 데이터셋/파일 | 평가 내용 | 입력 형태 | 주요 metric |
| --- | --- | --- | --- | --- |
| PPPL raw-text languages | v5 local Glot500 raw text: `/home/axt/mnt2/jongha/v5_glot50010/raw/<language_script>` | MLM pseudo-perplexity proxy. raw sentence에서 token을 mask하고 모델이 원 token을 얼마나 잘 맞히는지 본다. | monolingual raw text, 현재 최대 `100` examples/language | weighted mean NLL, weighted pseudo-perplexity. 낮을수록 좋음 |
| Tatoeba retrieval languages | LASER repository의 Tatoeba v1 parallel sentence data를 `evaluation/download_data/download/retrieval_tatoeba/`로 변환 | source language sentence embedding으로 대응되는 English sentence를 nearest-neighbor retrieval | `<lang>`-English parallel sentence pairs | Acc@1, Acc@5, Acc@10. 높을수록 좋음 |
| Bible retrieval languages | local Bible parallel corpus: `/disk3/moon/paralleltext/bibles/corpus/*-x-bible*.txt`에서 English Bible과 shared verse를 맞춰 `retrieval_bible/`로 materialize | Tatoeba와 같은 sentence retrieval이지만 domain이 Bible verse다. | `<lang>`-English verse-aligned parallel text | Acc@1, Acc@5, Acc@10. 높을수록 좋음 |
| Roundtrip alignment languages | Bible retrieval에서 ready인 verse-aligned data를 `roundtrip_alignment/roundtrip.<lang>.jsonl`로 변환 | SimAlign으로 word alignment를 잡고, source token이 여러 언어 alignment cycle을 돌아 자기 자신으로 돌아오는지 측정 | Bible-derived multilingual sentence groups, pivot은 주로 `deu_Latn` | roundtrip alignment accuracy. 높을수록 좋음 |
| Taxi1500 languages | Taxi1500 English split: `evaluation/download_data/download/taxi1500/eng_{train,dev,test}.tsv` | Bible verse topic text classification. 현재 local data는 English만 있음. | English Bible verse text + 6-way topic label | accuracy, macro-F1. 높을수록 좋음 |
| NER languages | PAN-X/WikiAnn NER, HuggingFace `tner/wikiann`에서 받아 `evaluation/download_data/download/ner/`로 변환 | named entity recognition token classification | token + BIO label, labels: LOC/ORG/PER/O | entity/token classification F1. 높을수록 좋음 |
| POS languages | Universal Dependencies v2.11 treebanks를 CoNLL/TSV로 변환해 `evaluation/download_data/download/pos/`에 저장 | part-of-speech tagging token classification | token + UPOS tag | POS F1. 높을수록 좋음 |

짧게 말하면:

```text
PPPL      = Glot500 raw text로 MLM proxy
Tatoeba   = Tatoeba 병렬문장으로 sentence retrieval
Bible     = Bible/PBC 계열 병렬 verse로 sentence retrieval
Roundtrip = Bible-derived 병렬문장으로 SimAlign word-alignment consistency
Taxi1500  = Bible verse topic classification
NER       = PAN-X/WikiAnn named entity tagging
POS       = Universal Dependencies POS tagging
```

## 사용자가 적은 숫자의 의미

```text
PPPL raw-text languages        102
Tatoeba retrieval languages     63
Bible retrieval languages       74
Roundtrip alignment languages   74
Taxi1500 languages               1
NER languages                   78
POS languages                   58
```

이 숫자는 모두 **v5 102개 Glot500 language-script subset과 각 evaluation
resource의 intersection count**다. 예를 들어 Tatoeba `63`은 Tatoeba 전체 언어가
63개라는 뜻이 아니라, v5의 102개 중 현재 local Tatoeba retrieval 평가가 가능한
언어가 63개라는 뜻이다.

## Metric별 Available Language List

PPPL은 102개 전체다. 즉 XLM-R-seen 92 + target10 10 전체가 raw-text PPPL에
포함된다.

### Tatoeba retrieval: 63

```text
ara_Arab, mar_Deva, slv_Latn, fin_Latn, hun_Latn, cmn_Hani,
est_Latn, bre_Latn, hrv_Latn, ron_Latn, ell_Grek, slk_Latn,
vie_Latn, amh_Ethi, epo_Latn, bel_Cyrl, xho_Latn, hin_Deva,
tam_Taml, mon_Cyrl, ces_Latn, hye_Armn, isl_Latn, afr_Latn,
deu_Latn, urd_Arab, bul_Cyrl, tgl_Latn, eus_Latn, pol_Latn,
lat_Latn, tur_Latn, fra_Latn, cat_Latn, uig_Arab, sqi_Latn,
swh_Latn, kor_Hang, ukr_Cyrl, yid_Hebr, heb_Hebr, nld_Latn,
fry_Latn, glg_Latn, mkd_Cyrl, ind_Latn, por_Latn, spa_Latn,
dan_Latn, khm_Khmr, gla_Latn, kat_Geor, ita_Latn, cym_Latn,
srp_Latn, tha_Thai, swe_Latn, pes_Arab, kaz_Cyrl, kur_Latn,
mal_Mlym, gle_Latn, lit_Latn
```

### Bible retrieval / Roundtrip alignment: 74

Bible retrieval과 Roundtrip alignment는 현재 같은 74개 language-script에 걸린다.

```text
mya_Mymr, mar_Deva, hau_Latn, uzb_Latn, slv_Latn, fin_Latn,
hun_Latn, cmn_Hani, bre_Latn, hrv_Latn, jav_Latn, ron_Latn,
ell_Grek, slk_Latn, vie_Latn, amh_Ethi, epo_Latn, bel_Cyrl,
xho_Latn, hin_Deva, tam_Taml, ces_Latn, san_Deva, hye_Armn,
kan_Knda, isl_Latn, afr_Latn, deu_Latn, urd_Arab, bul_Cyrl,
tgl_Latn, eus_Latn, pol_Latn, lat_Latn, tur_Latn, fra_Latn,
cat_Latn, uig_Arab, arb_Arab, sqi_Latn, sin_Sinh, swh_Latn,
kor_Hang, ukr_Cyrl, kir_Cyrl, heb_Hebr, nld_Latn, fry_Latn,
azb_Arab, mkd_Cyrl, ind_Latn, por_Latn, spa_Latn, dan_Latn,
khm_Khmr, gla_Latn, uig_Latn, kat_Geor, snd_Arab, ita_Latn,
cym_Latn, srp_Latn, tha_Thai, swe_Latn, pan_Guru, prs_Arab,
pes_Arab, san_Latn, kaz_Cyrl, mal_Mlym, nep_Deva, gle_Latn,
som_Latn, lit_Latn
```

### Taxi1500 text classification: 1

```text
eng_Latn
```

### NER: 78

```text
mya_Mymr, ara_Arab, mar_Deva, uzb_Latn, slv_Latn, fin_Latn,
hun_Latn, est_Latn, bre_Latn, hrv_Latn, jav_Latn, ron_Latn,
ell_Grek, nor_Latn, slk_Latn, vie_Latn, amh_Ethi, epo_Latn,
bel_Cyrl, hin_Deva, tam_Taml, mon_Cyrl, ces_Latn, san_Deva,
hye_Armn, pus_Arab, kan_Knda, isl_Latn, ori_Orya, afr_Latn,
deu_Latn, urd_Arab, bul_Cyrl, tgl_Latn, eus_Latn, pol_Latn,
lat_Latn, tur_Latn, fra_Latn, cat_Latn, uig_Arab, sqi_Latn,
sin_Sinh, msa_Latn, kor_Hang, ukr_Cyrl, kir_Cyrl, yid_Hebr,
heb_Hebr, nld_Latn, fry_Latn, glg_Latn, fas_Arab, eng_Latn,
mkd_Cyrl, ind_Latn, por_Latn, spa_Latn, dan_Latn, khm_Khmr,
gla_Latn, kat_Geor, mlg_Latn, snd_Arab, ita_Latn, cym_Latn,
zho_Hani, tha_Thai, swe_Latn, pan_Guru, kaz_Cyrl, kur_Latn,
mal_Mlym, nep_Deva, gle_Latn, swa_Latn, som_Latn, lit_Latn
```

### POS: 58

```text
ara_Arab, mar_Deva, slv_Latn, fin_Latn, hun_Latn, est_Latn,
bre_Latn, hrv_Latn, jav_Latn, ron_Latn, ell_Grek, nor_Latn,
slk_Latn, vie_Latn, amh_Ethi, bel_Cyrl, hin_Deva, tam_Taml,
ces_Latn, san_Deva, hye_Armn, isl_Latn, afr_Latn, deu_Latn,
urd_Arab, bul_Cyrl, tgl_Latn, eus_Latn, pol_Latn, lat_Latn,
tur_Latn, fra_Latn, cat_Latn, uig_Arab, sqi_Latn, sin_Sinh,
kor_Hang, ukr_Cyrl, heb_Hebr, nld_Latn, glg_Latn, fas_Arab,
eng_Latn, ind_Latn, por_Latn, spa_Latn, dan_Latn, gla_Latn,
ita_Latn, cym_Latn, srp_Latn, zho_Hani, tha_Thai, swe_Latn,
kaz_Cyrl, mal_Mlym, gle_Latn, lit_Latn
```

## Report/PPT에서 써야 하는 표현

추천 표현:

```text
We define a 102-language Glot500 subset consisting of 92 language-scripts that
are marked as XLM-R training languages and 10 Glot500-internal target
language-scripts that are not marked as XLM-R training languages. All 102 have
local Glot500 raw text and are used for tokenizer/MLM/PPPL. Downstream metrics
are reported on the intersection between this 102-language subset and each
locally materialized Glot500 evaluation resource.
```

한국어 발표 문장:

```text
이번 v5에서 XLM-R 학습 언어라는 말은 실제 XLM-R pretraining corpus를 다시
쓴다는 뜻이 아니라, Glot500 metadata에서 XLM-R에 포함된 것으로 표시된
92개 언어를 head/seen 쪽으로 둔다는 뜻입니다. 실제 raw text는 102개 모두
별도로 내려받은 Glot500 raw data를 사용했습니다. PPPL은 102개 전체에 대해
가능하지만, downstream은 각 task dataset이 제공하는 언어와의 교집합만
평가하므로 Tatoeba 63, Bible/Roundtrip 74, Taxi1500 1, NER 78, POS 58개로
coverage가 달라집니다.
```

피해야 하는 표현:

```text
target10 downstream을 모든 task에서 직접 평가했다.
```

정확한 표현:

```text
target10은 PPPL/raw-text proxy에서 직접 평가했고, downstream은 local task
coverage가 있는 seen/head 언어 중심의 Glot500 metric replay로 보고했다.
```

## 근거 파일

| 목적 | 파일 |
| --- | --- |
| 언어별 전체 flag/count | `docs/exp/v5/0_tokenizer/00_data_scope/data_composition_by_language.tsv` |
| 읽기용 언어별 표 | `docs/exp/v5/0_tokenizer/00_data_scope/data_composition_by_language.md` |
| XLM-R flag와 source sentence count | `docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv` |
| selected target10 manifest | `docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| merge manifest | `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv` |
| metric coverage summary | `docs/exp/v5/3_evaluation/00_coverage/coverage_summary.tsv` |
| metric별 coverage TSVs | `docs/exp/v5/3_evaluation/00_coverage/coverage_*.tsv` |
