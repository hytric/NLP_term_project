# Third Try Ablation Study Positioning

작성일: 2026-06-12

## 목적

기존 실험은 폐기하지 않는다. 다만 `third_try`에서는 main experiment가 아니라 ablation study로 배치한다.

Main experiment는 target10 성능 개선 모델이다. Ablation은 high-resource replay, embedding initialization, vocab size, objective 선택에서 벗어나면 어떤 일이 생기는가를 설명한다.

## 기존 실험의 위치

| Existing work | Third-try role | 해석 |
| --- | --- | --- |
| `first_try` target10 tokenizer/MLM/NMT | prototype ablation | 초기 engineering proof와 downstream collapse 사례 |
| `second_try` 8k/16k/32k vocab grid | main candidate evidence plus vocab size ablation | target10 vocab budget 선택 근거 |
| `second_try` random/mean/fvt/align/focus | main candidate evidence plus init ablation | embedding initialization novelty와 candidate selection 근거 |
| `second_try` CPT-only control | no-extension ablation | vocabulary extension의 효과를 continued pretraining 효과와 분리 |
| `second_try` target-only/repair probes | training objective ablation | replay/full MLM 없이 appended-token만 고치려 할 때 실패 조건 확인 |
| NMT/retrieval experiments | downstream proxy ablation | encoder representation 개선이 translation으로 바로 이어지는지의 exploratory evidence |

## Main과 Ablation의 경계

Main result에 포함:

- XLM-R-B baseline
- target10 tokenizer append
- random plus non-random embedding initialization methods
- full MLM continued pretraining
- high-resource replay + target10 low-resource mixture
- 3개 이상 seed
- target10 downstream evaluation

Ablation으로만 포함:

- byte fallback vs character fallback/coverage tokenizer variants
- LoRA
- target-only MLM
- seed-1-only pilot
- downstream 없이 tokenizer/PPPL만 있는 run
- new-row-only repair
- translation decoder experiment

## 왜 이렇게 분리하는가

현재 scope의 핵심은 "target10 실제 성능 개선 모델을 만들고, high-resource와 low-resource를 동시에 사용하라"이다. 그러므로 중심 주장은 target10 downstream 개선, seed stability, high-resource control을 함께 보여야 한다.

기존 실험은 설계 일부만 바꾼 evidence 또는 ablation이다. 특히 `second_try`는 tokenizer extension 자체가 항상 model gain으로 이어지지 않는다는 중요한 negative diagnostic이며, third_try의 high-resource replay + multi-init + seed-stable downstream design을 정당화한다.

## Ablation Claim Template

좋은 표현:

> In ablations, vocabulary size and initialization choices changed appended-token learning behavior; the final claim is based on the high-resource-replay target10 model with downstream evaluation across multiple seeds.

한국어 보고서 표현:

> 보조 실험에서는 vocab 크기와 초기화 방법이 appended-token 학습 난이도에 영향을 주는 것을 확인했다. 그러나 최종 main claim은 high-resource replay를 포함한 target10 모델이 3개 이상 seed에서 downstream 개선을 보이는지로 판단한다.

피해야 할 표현:

- "Mean init이 좋아졌으므로 vocabulary extension이 성공했다."
- "Tokenizer fragmentation이 줄었으므로 모델 성능이 좋아졌다."
- "Bible proxy task 결과만으로 target10 downstream 개선 모델에 성공했다."
- "LoRA 결과를 Glot500 full fine-tuning 결과처럼 해석한다."

## Second Try Negative Result 재사용 방식

`second_try`의 결론은 다음처럼 쓴다.

Allowed:

- tokenizer extension reduces fragmentation;
- appended-token learning is hard under limited data;
- original continued-pretraining control is necessary;
- initialization/vocab size choices are ablation variables;
- positive downstream claims require high-resource replay, target10 evaluation, and seed stability.

Blocked:

- `second_try`만으로 positive adapted-model claim;
- `second_try`만으로 translation success claim;
- target-only or LoRA result를 target10 final model result로 해석.

## Ablation Matrix

| Axis | Third-try main value | Ablation values |
| --- | --- | --- |
| Base | XLM-R-base | XLM-R-large optional/reference only |
| Vocab operation | append to XLM-R vocab | smaller append grids, selective append |
| Aux tokenizer | SentencePiece unigram multilingual | per-language tokenizer, target-only tokenizer |
| Fallback | selected target10 setting | byte fallback, character fallback/coverage |
| Init | random plus selected non-random methods | excluded init methods or failed init branches |
| Training | full MLM | LoRA, new-row-only, staged repair |
| Data | high-resource + target10 mixture | target-only, Bible-only |
| Evaluation | target10 downstream | PPPL-only, NMT, retrieval diagnostics |

## Final Placement In Report

1. Main paper body: target10 high-resource-replay method and downstream evaluation.
2. Ablation section: current experiments.
3. Appendix: detailed failed branches, repair probes, sample outputs.

이 구조로 가면 "실제 성능 개선 모델"과 "기존 실험을 ablation/failure analysis로 살리는 전략"이 충돌하지 않고 같이 살아난다.
