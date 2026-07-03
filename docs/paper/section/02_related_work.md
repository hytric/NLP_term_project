# 02 Related Work

선행연구를 나열하는 대신, 본 실험의 각 설계 선택이 어디에서 왔고 왜 그 값을 가져왔는지를 연결한다.

## 2.1 XLM-R and multilingual MLM

`xlm-roberta-base`는 본 실험의 base encoder이자 source tokenizer다. 여기서 가져온 것은 (1) MLM objective와 multilingual pretraining framing, (2) 250,002 크기의 SentencePiece vocabulary와 그 embedding matrix다. 본 보고서는 아키텍처를 새로 제안하지 않는다. 기존 token은 **token string identity 기준으로 source row를 그대로 보존**하며, 확장으로 추가되는 새 row만 실험 대상으로 삼는다. 이 구분이 중요한 이유는, SPM protobuf에 piece를 append하면 `<mask>` 같은 special token의 id가 이동할 수 있어(250001 → 366665), id가 아니라 string으로 remap해야 하기 때문이다.

## 2.2 Glot500 and horizontal language scaling

Glot500에서 가져온 설계는 네 가지다. (1) mixed corpus에서 SentencePiece unigram tokenizer를 재학습, (2) 기존 XLM-R SPM 뒤에 새 piece를 append하는 append-only vocab injection, (3) 확장 모델의 continued MLM pretraining, (4) head/tail/all 그룹 분리 보고. 달라진 점은 규모와 질문이다. 본 보고서는 500개 언어 전체 확장이 아니라 **92 seen + 7 target**의 축소 설정이고, main question은 scaling 자체가 아니라 **new embedding row initialization**이다. 따라서 "Glot500을 재현했다"가 아니라 "Glot500-style 설정 위에서 하나의 축을 통제 비교했다"로 위치시킨다.

## 2.3 Vocabulary transfer and embedding initialization

새 vocabulary row를 기존 embedding 공간에 잘 배치하는 문제는 cross-lingual vocabulary transfer 연구에서 다뤄져 왔다.

- **FVT (Fast Vocabulary Transfer).** 새 token 표면형을 source tokenizer로 다시 분해하고, 그 구성 subtoken embedding의 평균을 새 row로 쓴다. 표면형/형태 정보를 재사용한다는 것이 핵심 직관이며, 본 실험의 main hypothesis다.
- **WECHSEL / FOCUS 계열.** lexical overlap이나 보조 임베딩을 이용해 target vocabulary를 source 공간으로 사상하는 vocabulary transfer 방법으로, "표면형·의미 유사성을 재사용하면 좋은 출발점을 얻는다"는 근거를 제공한다.
- **Embedding initialization 안정성(Hewitt류).** 새 embedding을 기존 embedding 분포 근처(예: 평균)에 두면 학습 초기 불안정을 줄일 수 있다는 근거로, `mean` baseline의 배경이다.

본 실험의 `weighted FVT`(subtoken 표면 길이 가중)와 `family-aware mean`(language family prior)은 위 아이디어를 확장한 **local experimental variant**이며, 표준 방법처럼 소개하지 않는다.

## 2.4 SentencePiece / Unigram LM 설정 근거

tokenizer는 `model_type=unigram`, `byte_fallback=true`, `character_coverage=1.0`으로 학습한다. unigram은 XLM-R/Glot500 계열과 tokenizer family를 맞추기 위한 선택이고, byte fallback은 드문 문자를 unknown 대신 byte piece로 안전하게 분해하기 위한 장치다. Target7은 Latin script지만 low-resource이므로 미등록 문자 처리에서 byte fallback이 유리하다.

## 2.5 Evaluation framing

Low-resource adaptation은 하나의 aggregate score만 보면 head 언어의 이득에 가려 왜곡되기 쉽다. 따라서 Glot500을 따라 tail/head/all을 분리하고, task마다 target coverage가 다르므로 coverage(언어 수)를 함께 보고한다.

**평가 프로토콜은 Glot500(Imani et al., 2023) Table 3의 downstream suite + pseudoperplexity를 따른다**(본 보고서는 그중 sentence retrieval·NER·roundtrip·text classification과 PPPL을 보고한다). Glot500은 저자원 언어에 labeled train set이 없다는 점을 명시하고, supervised task는 **English로 fine-tune한 뒤 target에 zero-shot 전이**하는 XTREME(Hu et al., 2020) 방식을 사용한다. 원문 그대로: *"Since training data does not exist for some languages, we finetune on English (with early stopping based on dev) and evaluate zero-shot transfer."* 본 보고서도 동일 프로토콜과 데이터를 사용하므로 XLM-R·Glot500-m baseline과 같은 축에서 비교된다.

- **Sequence labeling.** NER = WikiANN(Pan et al., 2017). English fine-tune, LR 2e-5 Adam, target zero-shot. metric F1.
- **Text classification.** Taxi1500(Ma et al., 2023). English fine-tune(LR 2e-5, batch 16), target zero-shot. metric macro-F1.
- **Sentence retrieval.** Tatoeba(Artetxe & Schwenk, 2019)와 Bible의 English-aligned 문장을 cosine 최근접으로 매칭(Hu et al., 2020). **fine-tune 없음.** metric Top-10 Acc.
- **Roundtrip alignment.** gold 없이 표현 품질을 보는 roundtrip(Dufter et al., 2018). **fine-tune 없음.** metric accuracy.
- **Pseudoperplexity.** held-out에서 token을 하나씩 masking(Salazar et al., 2020). **fine-tune 없음.** lower better.

왜 English-source zero-shot인가는 이 프로토콜의 핵심이다. tail 언어에 labeled 학습 데이터가 없으므로 target fine-tune이 불가능하고, English로만 supervision을 주면 target 성능이 나오는 유일한 경로가 **공유 multilingual 표현의 cross-lingual 정렬**뿐이라, 이 설정이 곧 vocabulary extension·initialization이 바꾸는 표현 정렬을 직접 측정한다. 각 task의 입력·처리·출력·해석·하이퍼파라미터는 §5에서 상세히 정의한다.
