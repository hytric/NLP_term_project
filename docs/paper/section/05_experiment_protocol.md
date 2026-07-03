# 05 Experiment Protocol

## 5.1 Controlled variables

다섯 방법은 **오직 새 vocabulary row 초기화만** 다르고 나머지는 모두 같다: 같은 확장 tokenizer, 같은 MLM corpus, 같은 objective/hyperparameter, 같은 50K budget, 같은 evaluation runner. 따라서 표에서 보이는 차이는 initialization과 그로 인한 training dynamics의 상호작용으로 해석한다.

## 5.2 Reporting groups & metric direction

- **tail**: Target7(또는 target coverage가 있는 unseen) 그룹.
- **head**: XLM-R-seen replay 그룹.
- **all**: 평가된 언어 전체.
- Coverage 없는 group은 `NA`. metric 방향은 표마다 명시(↓ lower better, ↑ higher better).

## 5.3 50K convergence reporting policy

모든 최종 수치는 **50K-step 수렴 checkpoint**를 기준으로 보고한다. 초기 진단(Step-4000 등)은 본문 결과 표에 쓰지 않으며, 필요한 경우 10K→50K **궤적**으로만 학습 진행을 보인다(§6.4). 50K는 4K/8K 진단으로는 수렴을 단정하기 부족했기에 둔 conservative budget이고, checkpoint/log interval은 1,000 step으로 evaluation granularity와 맞춘다.

## 5.4 Downstream task 정의 (입력 → 처리 → 출력 → 해석)

평가 task는 Glot500 downstream suite에서 가져왔다. 먼저 한눈에 보는 요약 표를 두고, 이어 각 task의 동작을 입력·처리·출력·해석 순으로 정의한다.

**Table (개요). 평가 항목 요약.**

| 평가 항목 | 무엇을 평가하나 | 해석 |
| --- | --- | --- |
| Pseudoperplexity | MLM 모델이 해당 언어 문장을 얼마나 자연스럽게 예측하는지 | 낮을수록 좋음 |
| Sentence Retrieval Tatoeba | 영어 문장과 같은 의미의 다른 언어 문장을 Tatoeba에서 찾는 능력 | Top-10 Acc. 높을수록 좋음 |
| Sentence Retrieval Bible | Bible parallel corpus에서 의미가 같은 문장을 찾는 능력 | Top-10 Acc. 높을수록 좋음 |
| Text Classification | 영어로 fine-tuning한 분류 모델이 다른 언어에도 zero-shot으로 잘 전이되는지 | F1 높을수록 좋음 |
| NER | 영어 NER 학습 후 다른 언어의 개체명 인식이 가능한지 | F1 높을수록 좋음 |
| Roundtrip Alignment | 여러 언어를 거쳐 단어 alignment를 돌렸을 때 원래 단어로 돌아오는지 | Accuracy 높을수록 좋음 |

### (공통) Sentence embedding 추출

Retrieval과 embedding similarity는 동일한 문장 벡터 추출을 공유한다(근거: `evaluation/retrieval/evaluate_retrieval_tatoeba.py`).
1. 각 문장을 모델 tokenizer로 인코딩하고 `AutoModel`로 forward한다.
2. hidden states 중 **layer index 7**(0-index 8번째 layer)을 고른다 — Glot500 retrieval 관행.
3. special/padding token을 제외한 token hidden state를 **mean pooling**한다.
4. 문장 벡터를 L2 normalize한다. (similarity 분석에서는 전체 평균을 빼는 centered normalize도 추가.)

### 5.4.1 Pseudoperplexity (PPPL) — ↓ lower better

- **입력.** Target7 held-out 문장 pool(언어당 100문장, 총 700; 현재 진단 run은 140문장·5,196 masked token).
- **처리.** 각 위치를 차례로 `<mask>`로 가리고 MLM이 정답 token에 부여하는 확률로 negative log-likelihood를 구한 뒤, 이를 지수화해 pseudo-perplexity로 집계(weighted PPPL)한다. fine-tuning 없이 모델의 intrinsic language fit을 잰다.
- **출력.** language-weighted pseudoperplexity 스칼라.
- **핵심 코드(개념).**
  ```python
  # 각 위치 t를 마스킹하고 정답 token의 NLL을 합산 → 지수화
  for t in range(len(ids)):
      masked = ids.clone(); masked[t] = mask_id
      logp = log_softmax(model(masked).logits[t])
      nll += -logp[ids[t]]
  pppl = exp(nll / num_tokens)   # lower is better
  ```
- **해석.** 낮을수록 모델이 해당 언어 문장을 자연스럽게 예측한다는 뜻. 단, held-out이 아니라 `target7 train-source diagnostic`이므로 Glot500-style held-out PPPL 재현이 아니라 checkpoint별 intrinsic 진단으로 해석한다.

### 5.4.2 Sentence Retrieval — Tatoeba — ↑ Acc10

- **입력.** Tatoeba의 English↔Target 병렬 문장(측정 대상 `dtp`, `ile`, `csb`, 2,253쌍).
- **처리.** 양쪽 문장을 위 방식으로 임베딩하고, 각 English 문장에 대해 target 문장 집합에서 cosine 최근접 이웃을 faiss로 검색한다(Top-10).
- **출력.** 정답 짝이 Top-10 안에 든 비율(Acc10).
- **핵심 코드(개념, `evaluate_retrieval_tatoeba.py`).**
  ```python
  X = embed(src_sents)[:, layer7]      # (N, 768) mean-pooled, L2-norm
  Y = embed(eng_sents)[:, layer7]
  index = faiss.IndexFlatL2(768); faiss.normalize_L2(X); faiss.normalize_L2(Y)
  index.add(X); _, top10 = index.search(Y, 10)   # 각 eng에 대한 최근접 10개
  acc10 = mean([i in top10[i] for i in range(N)])
  ```
- **해석.** 높을수록 두 언어의 같은 의미 문장이 임베딩 공간에서 가깝다는 뜻 — cross-lingual semantic alignment의 대리 지표.

### 5.4.3 Sentence Retrieval — Bible — ↑ Acc10

- **입력.** Parallel Bible Corpus의 verse-aligned English↔Target(`dtp`, `xav`, `bam`, 23,238 verse pairs).
- **처리/출력.** Tatoeba와 동일(Top-10 cosine retrieval, Acc10).
- **해석.** 종교 도메인 병렬 문장에서의 alignment. 단, 본 실험에서는 50K에서도 모든 초기화가 ~0.008로 floor라 초기화 우열 근거로는 쓰지 않는다(§6).

### 5.4.4 NER (Named Entity Recognition) — ↑ F1

- **입력.** WikiAnn(panx) BIO-태깅 데이터. English로 fine-tune, Target(`csb`, `lij`, `fur`, 언어당 100문장)으로 zero-shot 평가.
- **처리.** 인코더 위에 token classification head를 얹어 English NER로 학습(10 epoch, LR 2e-5, max len 256, `evaluation/tagging/run_tag.py`)한 뒤 target에 그대로 적용한다.
- **출력.** seqeval **entity-level F1**(precision/recall 조화평균).
- **핵심 코드(개념, `run_tag.py`).**
  ```python
  model = XLMRobertaForTokenClassification.from_pretrained(ckpt, num_labels=len(BIO))
  train(model, english_ner, epochs=10, lr=2e-5)     # English fine-tune
  preds = model(target_tokens).argmax(-1)            # zero-shot on target
  f1 = seqeval.f1_score(gold_spans, pred_spans)      # entity-level
  ```
- **해석.** 높을수록 English에서 배운 개체명 경계·유형이 다른 언어로 잘 전이된다는 뜻. 본 실험 target subset은 작아 diagnostic으로 본다.

### 5.4.5 Roundtrip alignment — ↑ accuracy

- **입력.** 여러 언어를 잇는 병렬 문장 cycle(`dtp`, `xav`, `bam` 중심, 22,669 samples; 근거 `evaluation/round-trip/evaluate_roundtrip.py`, simalign).
- **처리.** 인코더 임베딩으로 인접 언어쌍 간 **word alignment**(simalign)를 구하고, 한 단어를 cycle(예: src→eng→pivot→src)을 따라 따라간다.
- **출력.** 출발 단어로 되돌아온 단어 비율(round-trip consistency accuracy).
- **핵심 코드(개념, `evaluate_roundtrip.py` + simalign).**
  ```python
  aligner = SentenceAligner(model=ckpt, matching_methods="a")  # 임베딩 기반 word align
  # cycle: src -> eng -> pivot -> src, 각 인접쌍 alignment로 단어를 따라감
  for w in src_words:
      w2 = follow(w, aligns)      # cycle을 한 바퀴
      correct += int(w2 == w)     # 출발 단어로 복귀?
  acc = correct / total_words
  ```
- **해석.** 높을수록 여러 언어에 걸쳐 lexical alignment가 일관된다는 뜻 — token-level cross-lingual grounding의 대리 지표.

### 5.4.6 Text classification — Taxi1500 (zero-shot) — ↑ macro-F1

Taxi1500(Ma et al., 2023)은 Glot500 Table 3의 정식 task다. Glot500도 English fine-tune → target zero-shot(LR 2e-5, batch 16)으로 평가했다. **다만 본 실험에서는 target test set이 Parallel Bible Corpus(PBC) 저작권으로 로컬에 없어 English(head)만 평가**된다. 즉 방법론 차이가 아니라 로컬 데이터 접근 한계다.

- **입력.** Taxi1500(Bible verse 기반 6-class 주제 분류). English train/dev/test TSV. 근거 `evaluation/text_classification/zero_shot_train.py`.
- **처리.** 인코더 위에 sequence classification head(`AutoModelForSequenceClassification`)를 얹어 English로 end-to-end fine-tune 후 평가.
- **출력.** macro-F1.
- **핵심 코드(개념, `zero_shot_train.py`).**
  ```python
  clf = AutoModelForSequenceClassification.from_pretrained(ckpt, num_labels=6)
  train(clf, taxi1500_english)                 # English로 end-to-end fine-tune
  pred = clf(test_sents).argmax(-1)
  macro_f1 = f1_score(gold, pred, average="macro")
  ```
- **해석.** 높을수록 문장 주제 표현이 강하다는 뜻. 위 데이터 한계로 **English(head)만** 평가되므로 tail 근거로 쓰지 않는다(방법론이 아니라 로컬 데이터 문제).

## 5.5 Final table plan

최종 표는 method(열)×group(행) 구조로, 다섯 초기화(`random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean`)와 세 baseline(XLM-R-B, XLM-R-L, Glot500-m)을 같은 50K target eval setup에서 비교한다(§6.2). coverage 없는 셀은 `NA`.

## 5.6 Downstream fine-tuning / evaluation 하이퍼파라미터

재현성을 위해 각 task의 정확한 설정을 명시한다. NER·Text는 English로 fine-tune 후 zero-shot 전이하며, retrieval·roundtrip·PPPL은 **fine-tuning 없이** frozen encoder를 평가한다. 모든 task는 평가 대상 checkpoint(다섯 초기화의 50K 및 baseline)를 동일 설정으로 돌린다.

**Table (setup). Task별 fine-tuning/평가 설정.**

| Task | Fine-tune? | Epochs | LR | Batch (eff.) | Max len | Optimizer / schedule | 기타 | Metric |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| NER | ✅ English | **10** | 2e-5 | 8×grad4 = 32 | 256 | AdamW(ε=1e-8), linear, warmup 0, wd 0.0, grad-clip 1.0 | seed 1, save/best 1000 step | seqeval entity F1 |
| Text (Taxi1500) | ✅ English | **30** | 2e-5 | 8×accum2 = 16 | 100 | AdamW, linear, warmup 0 | seed 42, num_labels 6 | macro-F1 |
| Tatoeba retrieval | ❌ frozen | — | — | 128 (infer) | 512 | — | layer 7, mean-pool, cosine, faiss top-10 | Acc10 |
| Bible retrieval | ❌ frozen | — | — | 128 (infer) | 512 | — | layer 7, mean-pool, cosine, faiss top-10 | Acc10 |
| Roundtrip | ❌ frozen | — | — | 25 (align) | — | — | simalign `matching="a"`(argmax), max-branch 5 | round-trip Acc |
| Pseudoperplexity | ❌ frozen | — | — | — | — | — | 위치별 mask 후 weighted NLL | weighted PPPL |

**근거 코드.** NER `evaluation/tagging/evaluate_ner.sh` + `run_tag.py`; Text `evaluation/text_classification/zero_shot_train.py`; retrieval `evaluation/retrieval/evaluate_retrieval_{tatoeba,bible}.sh`; roundtrip `evaluation/round-trip/evaluate_roundtrip.py`.

**Glot500 recipe와의 일치.** 이 설정은 Glot500(Imani et al., 2023)의 평가 recipe를 따른다: NER는 **LR 2e-5 Adam + English fine-tune + dev early stopping + target zero-shot**, Text(Taxi1500)는 **LR 2e-5, effective batch 16**로 논문과 일치한다. 따라서 우리 초기화 ablation 점수는 XLM-R·Glot500-m baseline과 같은 프로토콜에서 비교된다.

**주의.** batch는 per-GPU 기준이며 effective batch는 gradient accumulation(NER ×4, Text ×2)을 곱한 값이다. NER는 `save_only_best_checkpoint`로 dev 기준 best를 고른다. retrieval/roundtrip/PPPL은 학습이 없으므로 초기화·MLM 차이만이 점수 차이의 원인이다(fine-tune seed 분산 없음).
