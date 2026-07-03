# Detailed Report Outline

이 문서는 term report의 전체 개요를 문단 단위로 풀어쓴 설계도다. 최종 LaTeX는 `docs/paper/tex/sections/`에 작성하되, 실제 글을 쓰기 전에는 여기에서 논리 흐름, 근거 artifact, 표/그림 위치, claim boundary를 먼저 확인한다.

## Paper-Level Thesis

본 보고서의 중심 주장은 다음과 같다.

> Glot500-style tokenizer expansion은 target7의 subword fragmentation을 줄일 수 있지만, 같은 tokenizer를 쓰더라도 새 vocabulary embedding row를 어떻게 초기화하느냐에 따라 50K-step MLM convergence와 downstream score가 달라진다. 따라서 low-resource vocabulary adaptation에서는 tokenizer 확장뿐 아니라 initialization policy까지 controlled ablation으로 보고해야 한다.

이 문장을 벗어나는 과장된 주장은 하지 않는다. 특히 "FVT가 항상 최고", "Glot500 전체 재현", "모든 low-resource language 일반화"는 본 보고서의 claim이 아니다.

## Core Argument Chain

1. XLM-R은 강한 multilingual encoder지만, XLM-R에 없는 tail language에서는 subword fragmentation과 representation mismatch가 남는다.
2. Glot500은 vocabulary expansion과 continued MLM pretraining으로 이 문제를 줄이는 큰 방향을 제시했다.
3. 본 프로젝트는 그 큰 방향을 v5.2의 작은 controlled setup으로 가져온다.
4. Tokenizer는 Glot500-style SentencePiece append로 고정한다.
5. 따라서 main comparison은 tokenizer가 아니라 새 embedding row initialization이다.
6. `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean` 다섯 방법을 같은 corpus/objective/schedule/evaluation protocol에서 비교한다.
7. Step-4000 결과는 early diagnostic으로만 사용한다.
8. Final claim은 50K-step convergence run의 loss trajectory와 tail/head/all score table을 근거로 세운다.
9. Task coverage가 다르므로 score는 반드시 coverage와 함께 해석한다.
10. 최종 결론은 "initialization matters under this controlled setup"으로 제한한다.

## Proposed Final Table Of Contents

1. Abstract
2. Introduction
3. Related Work
4. Data and Experimental Scope
5. Method
6. Experiment Protocol
7. Results
8. Representation Analysis
9. Discussion
10. Limitations
11. Conclusion
12. Appendix: Artifact and Code Map

현재 LaTeX 파일은 Discussion/Limitations/Conclusion이 하나의 section으로 묶여 있다. 최종 분량이 허용되면 `08_limitations_conclusion.tex`를 Discussion, Limitations, Conclusion으로 내부 subsection 분리하면 된다.

## 00 Abstract

### 역할

전체 보고서의 문제, 방법, 비교축, main evidence, claim boundary를 한 번에 요약한다.

### 문단 구성

**Paragraph 1: problem and setup**

- XLM-R 기반 multilingual encoder를 low-resource tail language로 확장하는 문제를 제시한다.
- Glot500-style vocabulary expansion을 작은 재현 가능한 설정으로 가져왔다고 말한다.
- 92 seen + 7 target, SentencePiece unigram append, XLM-R-base를 명시한다.
- Main ablation은 tokenizer가 아니라 new embedding row initialization이라고 못 박는다.

**Paragraph 2: evidence and claim boundary**

- 50K-step convergence run이 final evidence라고 말한다.
- 다섯 methods와 tail/head/all reporting을 명시한다.
- Step-4000은 early diagnostic으로만 사용한다고 말한다.
- Universal best claim을 피하고, controlled setup에서 initialization effect를 검증한다고 끝낸다.

### 반드시 들어갈 키워드

- `Glot500-style vocabulary extension`
- `XLM-R`
- `new vocabulary embedding row initialization`
- `50K-step convergence`
- `tail/head/all`
- `Step-4000 early diagnostic`

## 01 Introduction

### 역할

독자에게 왜 이 실험이 필요한지 설득한다. "왜 또 Glot500인가?"가 아니라 "Glot500-style expansion에서 아직 initialization이라는 작은 but 중요한 선택이 남아 있다"로 끌고 간다.

### 문단 구성

**Paragraph 1: broad motivation**

- Multilingual pretrained encoders는 많은 언어를 커버하지만, tail language는 여전히 약하다.
- 약한 이유를 두 갈래로 둔다: token fragmentation, insufficient representation adaptation.
- 너무 일반론으로 길게 가지 말고 XLM-R과 Glot500으로 바로 연결한다.

**Paragraph 2: prior solution**

- Glot500은 horizontal language scaling을 위해 tokenizer expansion과 continued MLM pretraining을 사용했다.
- Head/tail/all evaluation을 통해 high-resource와 tail-resource를 분리해 봤다는 점을 강조한다.
- 이 reporting style을 본 보고서가 가져온다고 말한다.

**Paragraph 3: gap**

- Vocabulary expansion 후 새 token embedding row를 어떻게 초기화할지는 별도의 modeling decision이다.
- Random initialization은 간단하지만 새 token이 source embedding space와 무관하게 시작한다.
- Mean/FVT 계열은 기존 embedding geometry를 재사용하려는 시도다.

**Paragraph 4: our setup**

- v5.2 setup: 92 seen replay + target7.
- Target7은 XLM-R-unseen이고 downstream coverage가 가능한 language-script다.
- Tokenizer, corpus, MLM objective, schedule은 고정하고 initialization만 바꾼다.

**Paragraph 5: research questions and contributions**

- RQ1: Tokenizer extension이 target7 fertility를 줄이는가?
- RQ2: Initialization이 50K loss convergence에 영향을 주는가?
- RQ3: Tail/head/all downstream score에서 method별 차이가 나타나는가?
- RQ4: Early diagnostic과 final 50K 결과가 일치하는가?

### 넣을 표/그림

- Introduction에는 큰 표를 넣지 않아도 된다.
- 필요하면 contribution bullet만 간단히 둔다.

### 근거 artifact

- `docs/exp/v5.2/EXPERIMENT_DESIGN_KO.md`
- `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md`
- `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png`

## 02 Related Work

### 역할

선행연구를 단순 나열하지 말고, 본 실험의 선택을 정당화하는 근거로 사용한다.

### Subsection 2.1: XLM-R and multilingual pretraining

**쓸 내용**

- XLM-R은 multilingual MLM pretraining의 base model이다.
- 본 실험은 XLM-R-base를 출발점으로 하므로 architecture 자체를 새로 제안하지 않는다.
- Contribution은 model architecture가 아니라 vocabulary expansion 후 initialization policy 비교다.

**연결 근거**

- `xlm-roberta-base`
- source tokenizer length 250002
- source `<mask>` id 250001

### Subsection 2.2: Glot500 and horizontal language scaling

**쓸 내용**

- Glot500은 더 많은 language-script로 XLM-R류 모델을 확장했다.
- SentencePiece unigram tokenizer training, vocabulary append, continued MLM pretraining을 사용했다.
- Head/tail/all reporting을 사용했기 때문에 본 보고서의 final table도 이 구조를 따른다.

**주의**

- "Glot500을 완전 재현했다"라고 쓰지 않는다.
- 본 실험은 small controlled reproduction/ablation이다.

### Subsection 2.3: Vocabulary transfer and embedding initialization

**쓸 내용**

- 새 vocabulary row를 기존 embedding space에 잘 배치하는 문제를 소개한다.
- Mean initialization은 안정적인 centroid baseline이다.
- FVT는 새 token surface를 source tokenizer로 decomposition해서 source subtoken embeddings를 재사용한다.
- Weighted FVT와 family-aware mean은 이 프로젝트의 local variants로 설명한다.

**References**

- FVT 관련 문헌.
- WECHSEL/FOCUS 계열 vocabulary transfer.
- Hewitt류 embedding initialization 안정성.

### Subsection 2.4: Evaluation framing

**쓸 내용**

- Low-resource adaptation은 single aggregate score만 보면 왜곡될 수 있다.
- 따라서 tail/head/all group을 분리한다.
- Task coverage가 다른 경우 coverage를 같이 보고한다.

## 03 Data And Experimental Scope

### 역할

언어 선택과 evaluation coverage를 투명하게 밝힌다. 이 절은 feedback에서 중요했던 "왜 이 언어인가", "task별 coverage가 무엇인가"에 답해야 한다.

### Subsection 3.1: Language scope

**쓸 내용**

- 92 XLM-R-seen language-script는 replay/head side다.
- 7 XLM-R-unseen target language-script는 tail side다.
- Target7: `dtp_Latn`, `xav_Latn`, `bam_Latn`, `csb_Latn`, `ile_Latn`, `lij_Latn`, `fur_Latn`.
- 모두 Latin script임을 명시한다.

**Table**

- `table_target7.tex`
- Columns: language-script, language name, family, reason selected, available tasks.

### Subsection 3.2: Why target7

**쓸 내용**

- 완전히 임의 선택이 아니라 downstream evaluation이 가능한 unseen language-script를 고른 것이다.
- 평가 불가능한 언어를 많이 넣는 것보다, 적은 수라도 tokenizer/training/evaluation을 연결할 수 있는 언어를 선택했다.
- 이 선택은 generality보다 traceability를 우선한 것이다.

### Subsection 3.3: Training corpus and sampling

**쓸 내용**

- Seen replay와 target corpus를 섞는다.
- Sampling은 high-resource domination을 줄이기 위한 장치다.
- `alpha=0.3` 등 local sampling strategy를 코드 근거와 연결한다.

**근거 artifact**

- `preprocessing/merge_files.py`
- `docs/exp/v5.2/1_data_scope/`

### Subsection 3.4: Evaluation coverage

**쓸 내용**

- Metric별로 target/head/all coverage가 다르다.
- Coverage 없는 group은 `NA`다.
- Coverage가 작은 task는 해석을 제한한다.

**Table**

- `table_task_coverage.tex`
- PPPL, Tatoeba, Bible, Text classification, NER, POS, Roundtrip.

## 04 Method

### 역할

어떤 실험 행동을 했는지 step-by-step으로 설명한다. 여기서는 재현 가능성이 핵심이다.

### Subsection 4.1: Tokenizer extension

**Paragraph plan**

1. XLM-R tokenizer를 source로 둔다.
2. v5.2 mixed corpus에서 SentencePiece unigram auxiliary model을 학습한다.
3. 기존 XLM-R SPM에 없는 piece만 append한다.
4. HuggingFace `add_tokens()`가 아니라 SPM protobuf append를 사용한 이유를 Glot500-style 구현과 연결한다.
5. `<mask>` id 이동 위험을 설명한다.

**설정값과 이유**

- `model_type=unigram`: XLM-R/Glot500 계열과 맞춤.
- `byte_fallback=true`: rare/OOV character 처리.
- `character_coverage=1.0`: target7 character 보존.
- `input_sentence_size=20000000`: SPM memory/time 통제.

**근거**

- `tokenization/train_v52_glot5007.sh`
- `tokenization/run.py`

### Subsection 4.2: Embedding initialization

**Paragraph plan**

1. 모든 method는 같은 tokenizer/corpus/schedule을 사용한다고 선언한다.
2. Existing token string은 source row를 복사한다.
3. New token row만 method별로 초기화한다.
4. `<mask>` remap과 LM head tying 검증을 구현 근거로 제시한다.

**Methods**

- `random`: model init distribution baseline.
- `mean`: source lexical embeddings global mean.
- `FVT`: source tokenizer decomposition 후 subtoken embedding 평균.
- `weighted FVT`: FVT에 source subtoken length weight 적용.
- `family-aware mean`: language family provenance 기반 frequency-weighted mean.

**Table**

- `table_initialization_methods.tex`

**Audit numbers**

- source tokenizer length 250002.
- target tokenizer length 366666.
- new rows 116664.
- `<mask>` source 250001 -> target 366665.
- `<mask>` diff 0.0.
- lm head tied true.

### Subsection 4.3: Continued MLM pretraining

**Paragraph plan**

1. MLM objective를 설명한다.
2. HuggingFace Trainer/DataCollator 기반임을 밝힌다.
3. max length 512, MLM probability 0.15 등 설정값을 표로 둔다.
4. Main convergence budget은 50K이고 checkpoint/logging interval은 1000 steps라고 쓴다.

**근거**

- `modeling/train_v52_glot5007_mlm.sh`
- `modeling/run.py`

## 05 Experiment Protocol

### 역할

결과를 보기 전에 비교 규칙을 고정한다. 어떤 score를 어떻게 읽어야 하는지 정의하는 절이다.

### Subsection 5.1: Controlled variables

**쓸 내용**

- Same tokenizer.
- Same training corpus.
- Same MLM objective.
- Same evaluation runners.
- Same 50K convergence budget.
- Difference: initialization method only.

### Subsection 5.2: Metrics

**쓸 내용**

- PPPL: lower is better.
- Tatoeba/Bible retrieval: Acc10, higher is better.
- Text classification: macro-F1, higher is better.
- NER/POS: F1, higher is better.
- Roundtrip alignment: accuracy, higher is better.

**주의**

- PPPL은 intrinsic proxy다.
- Downstream score와 항상 같은 방향으로 움직인다고 가정하지 않는다.

### Subsection 5.3: Head/tail/all reporting

**쓸 내용**

- Tail은 target coverage가 있는 XLM-R-unseen group이다.
- Head는 seen/replay group이다.
- All은 available evaluated languages 전체다.
- Coverage 없음은 `NA`다.

### Subsection 5.4: 50K convergence policy

**쓸 내용**

- Step-4000은 diagnostic이다.
- 4K에서 PPPL 개선 둔화가 있었더라도 training loss가 계속 감소했으므로 수렴이라고 부르지 않는다.
- 50K는 final claim을 위한 conservative budget이다.
- 1K interval은 checkpoint/log/eval의 실제 단위와 맞다.

## 06 Results

### 역할

Final 50K evidence를 먼저 보여주고, Step-4000은 보조 진단으로 배치한다.

### Subsection 6.1: Tokenizer fertility

**쓸 내용**

- XLM-R target7 tokens/word 2.204.
- v5.2 extended tokenizer target7 tokens/word 1.592.
- Reduction 27.75%.
- Interpretation: tokenizer extension reduces fragmentation.
- Boundary: method 간 score 차이는 tokenizer가 같으므로 fertility만으로 설명할 수 없다.

**Figure**

- `tokenization_effect_change.png`

### Subsection 6.2: 50K loss convergence

**쓸 내용**

- Main figure: `convergence_5way_loss_curve.png`.
- 다섯 method line을 비교한다.
- Loss flattening 여부를 본다.
- Final checkpoint marker와 1K point interval을 설명한다.

**Figure explanation requirement**

- Title reason.
- X-axis reason.
- Y-axis reason.
- Point interval reason.
- Why 50K.
- Color/marker meaning.
- Smoothing disclosure.

### Subsection 6.3: 50K final score table

**쓸 내용**

- Main numeric result.
- Rows: metric + group.
- Columns: random, mean, FVT, weighted FVT, family-aware mean.
- Coverage count.
- Best method per row.

**Source**

- regenerated `main_head_tail_all.tsv`.

**Interpretation template**

- Tail에서 좋은 method와 head에서 좋은 method가 다를 수 있다.
- PPPL best와 downstream best가 다를 수 있다.
- A method가 모든 task에서 best가 아니면 task-family-dependent effect로 쓴다.

### Subsection 6.4: Step-4000 diagnostic

**쓸 내용**

- Existing random/mean/FVT table을 보여준다.
- FVT가 early checkpoint에서 강한 signal을 보였다는 정도만 쓴다.
- Weighted FVT/family-aware mean이 없고 50K가 아니므로 final claim이 아니라고 명시한다.

### Subsection 6.5: Result summary

**쓸 내용**

- 가장 중요한 observation 3개만 정리한다.
- 예: tokenizer fragmentation 감소, loss convergence 차이, task/group별 score tradeoff.
- 아직 값이 없으면 `TBD`로 둔다.

## 07 Representation Analysis

### 역할

왜 어떤 initialization이 특정 task에서 유리했는지 representation 관점에서 해석한다. 단, diagnostic이라는 선을 지킨다.

### Subsection 7.1: Sentence representation geometry

**쓸 내용**

- Sentence embedding의 centered cosine similarity를 사용한다.
- Same-language, same-family, different-family relation bucket을 비교한다.
- FVT step-4000 plot은 초기 representation signal을 보여주는 diagnostic이다.

**Figure**

- `family_pair_boxplot_v52_fvt_step4000.png`

### Subsection 7.2: Family centroid map

**쓸 내용**

- 38-language subset의 family centroid를 2D로 시각화한다.
- 2D projection은 보조 그림이다.
- Numeric score보다 강한 claim을 만들지 않는다.

**Figure**

- `family_centroid_map_v52_fvt_step4000.png`

### Subsection 7.3: 50K representation comparison

**쓸 내용**

- 50K final checkpoints가 나오면 method별 같은 diagnostic을 비교한다.
- Early FVT advantage가 50K까지 남는지, weighted/family variants가 geometry를 바꾸는지 본다.

## 08 Discussion

### 역할

결과의 의미를 task와 method 관점에서 해석한다. 숫자를 반복하지 말고 "왜 이런 결과가 그럴듯한가"를 말한다.

### 논의 축

1. Tokenizer expansion vs embedding initialization.
2. Random baseline의 한계.
3. Mean initialization의 안정성.
4. FVT의 surface decomposition prior.
5. Weighted FVT의 length-weight prior.
6. Family-aware mean의 typology prior.
7. Tail gain과 head retention의 tradeoff.
8. PPPL과 downstream이 불일치할 수 있는 이유.

### 좋은 결론 문장 형태

- "This suggests..."보다 "In this controlled setup, this suggests..."로 제한한다.
- "Improves low-resource languages"보다 "improves the evaluated target coverage for [metric/group]"처럼 쓴다.

## 09 Limitations

### 역할

실험의 약점을 먼저 인정해서 보고서의 신뢰도를 높인다.

### 반드시 포함

- Target7은 모두 Latin script.
- Downstream coverage가 task마다 다름.
- Text classification target evidence가 제한적.
- Step-4000은 diagnostic.
- 50K는 local controlled budget이지 global optimum이 아님.
- Weighted FVT/family-aware mean은 local variants.
- One-run setting이면 seed variance가 충분히 평가되지 않았음을 명시한다.

## 10 Conclusion

### 역할

보고서의 main answer를 짧게 회수한다.

### 문단 구성

**Paragraph 1: what was done**

- XLM-R에 Glot500-style vocabulary extension을 적용했다.
- 다섯 initialization methods를 비교했다.
- 50K-step convergence와 tail/head/all score를 보고했다.

**Paragraph 2: what was found**

- Tokenizer fertility는 감소했다.
- Initialization은 loss convergence와 score에 영향을 주었다.
- Method effect는 task/group에 따라 다르게 나타났다.

**Paragraph 3: what remains**

- 더 넓은 script/language coverage.
- More seeds.
- Representation trajectory across steps.
- Better downstream coverage for target languages.

## Appendix

### 역할

본문에서 모든 코드를 길게 설명하지 않고도 재현 가능한 근거 지도를 제공한다.

### 포함 항목

- Artifact/code map.
- Full initialization audit counts.
- Full 50K score tables.
- Step-4000 diagnostic table.
- Plot generation scripts and raw TSV paths.
- Claim boundary checklist.

## Table And Figure Placement Plan

| 위치 | 항목 | 역할 | Source |
| --- | --- | --- | --- |
| Section 3 | Target7 table | 언어 선택 근거 | `glot5007_selected_manifest.tsv` |
| Section 3 | Task coverage table | coverage limitation 명시 | `low_resource_task_fill_candidates_ko.md` |
| Section 4 | Initialization methods table | method 정의 | `scripts/build_v5_initialized_checkpoint.py` |
| Section 6 | Tokenization fertility figure | tokenizer extension 효과 | `tokenization_effect_change.png` |
| Section 6 | 5-way convergence loss figure | 50K 수렴 근거 | `convergence_5way_loss_curve.png` |
| Section 6 | 50K head/tail/all table | final numeric result | regenerated `main_head_tail_all.tsv` |
| Section 6 | Step-4000 diagnostic table | early signal | `v52_final_downstream_table.tsv` |
| Section 7 | Family pair boxplot | representation diagnostic | `family_pair_boxplot_v52_fvt_step4000.png` |
| Section 7 | Family centroid map | representation diagnostic | `family_centroid_map_v52_fvt_step4000.png` |
| Appendix | Artifact/code map | reproducibility | local repo paths |

## Writing Order

1. `04_method.md`: method는 숫자와 무관하므로 먼저 완성한다.
2. `03_data_scope.md`: 언어 선택과 coverage를 고정한다.
3. `05_experiment_protocol.md`: evaluation rule을 고정한다.
4. `06_results_50k_convergence.md`: 50K 결과가 나오면 숫자를 채운다.
5. `07_analysis.md`: 결과 해석에 필요한 diagnostic만 남긴다.
6. `01_introduction.md`와 `00_abstract.md`: 결과 방향이 확정된 뒤 다시 다듬는다.
7. `08_discussion_limitations_conclusion.md`: final claim boundary에 맞춰 마무리한다.

## Final Claim Checklist

- [ ] 50K result와 Step-4000 diagnostic이 문장상 섞이지 않았는가?
- [ ] Every number has a source artifact.
- [ ] Every figure caption explains what the visual elements mean.
- [ ] Lower-better/higher-better metrics are clearly marked.
- [ ] Coverage-free cells are `NA`.
- [ ] Target7 Latin-script limitation is acknowledged.
- [ ] No universal best-method claim unless every row supports it.
- [ ] Head regression, if present, is reported honestly.

