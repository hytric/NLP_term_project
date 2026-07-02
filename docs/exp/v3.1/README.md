# V3.1 Embedding Alignment and Downstream Plan

작성일: 2026-06-18

## Core Direction

`v3.1`은 `v3`의 diagnostic negative 결론 이후, broad target10 positive route를 다시 열기 위한 평가 중심 실험 계획이다.

실험은 세 단계로 진행한다.

1. **Experiment 1: Cross-lingual semantic embedding alignment + 2D map**
   - low-resource language가 XLM-R/third_try encoder embedding space에 잘 붙었는지 확인한다.
   - 같은 의미의 문장/verse가 언어와 script를 넘어 가까워지는지 cosine/retrieval/margin/UMAP으로 평가한다.

2. **Experiment 2: Embedding-vector downstream tasks**
   - 1번에서 얻은 embedding vector를 frozen feature로 사용한다.
   - translation retrieval, translation pair classification, Taxi1500/Bible-topic classification으로 XLM-R-base 대비 개선을 평가한다.

3. **Experiment 3: Simple decoder translation task**
   - 최종 task로 XLM-R/third_try encoder 위에 작은 decoder layer를 학습한다.
   - 같은 decoder 구조를 XLM-R-base와 candidate encoder에 붙여 translation task를 비교/검증한다.

Tokenizer는 반드시 append-only protocol을 따른다. 새 tokenizer를 학습하더라도 final tokenizer로 교체하지 않고, high-resource + low-resource mixture에서 얻은 새 piece만 기존 XLM-R vocabulary 뒤에 붙인다.

## Documents

| File | Purpose |
| --- | --- |
| `00_append_only_tokenizer_protocol.md` | 기존 XLM-R tokenizer id를 보존하고 새 piece만 append하는 절차 |
| `00_tokenizer_audit/results.md` | 실제 third_try tokenizer 후보의 append-only/id-preservation audit 결과 |
| `plan.md` | v3.1 전체 실험 목표, gate, 실행 순서 |
| `reference_map.md` | `docs/exp/v3`, `docs/survey`, term guideline, vocab tutorial에서 가져온 방법론 근거 |
| `task_board.tsv` | stage별 상태와 next action |
| `01_embedding_alignment/plan.md` | 1번 실험: semantic alignment, 2D map, retrieval/margin 평가 계획 |
| `02_embedding_downstream/plan.md` | 2번 실험: embedding vector 기반 downstream task 계획 |
| `02_embedding_downstream/results.md` | 2번 실험 1차 결과: Coptic-Syriac frozen pair classification |
| `03_decoder_translation/plan.md` | 3번 최종 task: simple decoder translation 실험 및 검증 |
| `04_ablation/plan.md` | main/ablation 경계와 ablation 배치 |
| `04_ablation/init_mlm_probe/glot500_size_comparison.md` | Glot500-c/Glot500-m 대비 현재 v3.1 MLM probe의 corpus/training-budget 규모 비교 |
| `04_ablation/init_mlm_probe/mlm_training_protocol.md` | MLM masking, preprocessing, optimizer, eval-loss 계산 방식 |
| `04_ablation/init_mlm_probe/results.md` | 다섯 embedding initialization을 동일 MLM masked-prediction budget으로 학습한 후 비교한 결과 |
| `04_ablation/init_mlm_probe/feature_similarity_results.md` | MLM dev set의 같은 의미 target10 row로 encoder output feature similarity를 측정한 결과 |
| `05_additional/plan.md` | Glot500 비교, MLM protocol, feature proxy, 추가 실험을 보고서 섹션으로 묶는 계획 |
| `05_additional/idea.md` | Glot500 low-resource evaluation 구조 정리 |
| `05_additional/method.md` | Glot500 downstream/proxy task 설명 |
| `06_novelty/plan.md` | raw cosine calibration 문제를 DCLR novelty claim과 추가 실험 계획으로 정리 |
| `06_novelty/idea.md` | Coptic-Syriac semantic retrieval, pooling/layer/debiasing 실험 아이디어 |
| `06_novelty/problem.md` | cosine 과대평가, anisotropy, hard-negative/margin 평가 필요성 분석 |
| `06_novelty/survey.md` | BERT-flow, whitening, SimCSE, CSLS 기반 novelty survey |

## Reading Order

1. `README.md`
2. `reference_map.md`
3. `00_append_only_tokenizer_protocol.md`
4. `plan.md`
5. `01_embedding_alignment/plan.md`
6. `02_embedding_downstream/plan.md`
7. `03_decoder_translation/plan.md`
8. `04_ablation/plan.md`
9. `05_additional/plan.md`
10. `06_novelty/plan.md`
11. `../v3/positive_route_survey_methodology_20260618.md`
12. `../v3/10_embedding_alignment_downstream/plan.md`
13. `../../survey/termProjectGuideLine.pdf`
14. `../../survey/vocab_extension_tutorial.pdf`

## Current Status

Status: `STARTED`.

Current progress:

- append-only tokenizer structural audit: `PASS`;
- alignment/translation manifests: generated from the v3/v1 split lineage;
- Coptic-Syriac embedding alignment/retrieval, CSLS/centered retrieval, and PCA 2D maps: completed as a decoder-link diagnostic;
- simple decoder translation runner: implemented;
- `cop -> syr` XLM-R-base and third_try candidate smoke runs: completed;
- full-data 1-epoch `cop -> syr` and `syr -> cop` XLM-R-base baseline plus third_try seed13/17/23 candidate runs: completed;
- train-bank retrieval-only translation baseline: completed; retrieval beats the simple decoder but is hubness/generic-verse dominated;
- decoder full-prediction collapse diagnostics: completed; `syr -> cop` XLM-R-base shows near-total empty/max-length collapse, while third_try avoids that failure but remains repetitive;
- embedding downstream pair classification: completed for Coptic-Syriac; result is positive for pairwise diff/product logistic probes but mixed for raw cosine;
- initialization ablation: random/mean/fvt/align/focus all trained for identical 200-step MLM masked prediction; `fvt` ranks first but `focus` nearly catches up, so this remains a sensitivity result;
- MLM-dev same-meaning feature similarity: completed over all 90 directed target10 language pairs; it does not select `fvt`, so MLM loss and semantic feature retrieval are separate diagnostics;
- additional report plan: written; it packages Glot500 scale comparison, MLM protocol, feature-similarity proxy, pooling ablation, and next proxy/downstream priorities;
- novelty plan: written; it frames DCLR, hard-negative retrieval, CSLS/hubness, and decoder collapse diagnostics as the defensible novelty route;
- target10-wide downstream/topic classification: pending.

## One-Line Contract

`v3.1` tests whether target10 low-resource languages become semantically aligned in XLM-R-style encoder embedding space, whether those embeddings support broad downstream transfer, and whether a simple decoder trained on top of the encoder improves low-resource translation over the XLM-R-base encoder baseline.
