# 01 Introduction Draft

## 목적

왜 이 프로젝트가 필요한지, 기존 Glot500/XLM-R에서 어떤 빈틈을 보고, 이 보고서가 어떤 작은 실험 단위로 그 빈틈을 검증하는지 설명한다.

## 핵심 주장

1. Multilingual encoder는 많은 언어를 포함해도 tail language에서 token fragmentation과 representation mismatch 문제가 남는다.
2. Glot500은 vocabulary expansion + continued pretraining으로 이 문제를 줄이려는 강한 선행 연구다.
3. 이 프로젝트는 Glot500 전체를 크게 재현하기보다, XLM-R에 새 vocabulary row를 붙일 때 initialization이 얼마나 중요한지 50K-step controlled run으로 본다.

## 근거로 붙일 artifact

- Glot500 논문: vocabulary expansion, head/tail/all reporting.
- `docs/exp/v5.2/EXPERIMENT_DESIGN_KO.md`: v5.2 설계.
- `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md`: target7 tokenization reduction.
- `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png`: 50K convergence plot.
- `docs/exp/v5.2/3_evaluation/09_aggregation/main_head_tail_all.tsv`: final score table schema.

## 넣을 질문

- RQ1: Glot500-style tokenizer extension은 target7의 token fragmentation을 줄이는가?
- RQ2: 같은 tokenizer와 corpus에서 embedding initialization이 50K-step MLM 수렴에 영향을 주는가?
- RQ3: 수렴 후 score 변화는 tail/head/all group에서 다르게 나타나는가?
- RQ4: FVT 계열 초기화가 어떤 task family에서 특히 유리하거나 불리한가?

## 금지할 과장

- "Glot500을 완전 재현했다"라고 쓰지 않는다.
- "all low-resource languages"라고 일반화하지 않는다.
- target7이 모두 Latin script이므로 script diversity improvement라고 쓰지 않는다.

