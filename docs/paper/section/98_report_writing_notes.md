# Report Writing Notes

이 파일은 실제 report 문장을 작성할 때 옆에 두고 확인하는 유의사항이다. `99_claim_boundary_checklist.md`가 과장 표현을 막는 최종 점검표라면, 이 파일은 문단, 표, 그림, reference를 작성하는 방식에 대한 작업 규칙이다.

## 1. 전체 작성 원칙

- 글은 간결하게 쓴다. 단, 내용은 빈틈 없이 완결되어야 한다.
- 한 문장에는 가능하면 하나의 주장만 담는다.
- 모든 주장에는 근거를 붙인다. 근거가 없는 문장은 삭제하거나 `[EVIDENCE NEEDED]`로 표시한다.
- 모든 실험 행동에는 근거를 붙인다. "이렇게 했다"에서 끝내지 말고, "왜 그렇게 했는지"와 "어느 코드/artifact에서 확인되는지"를 같이 쓴다.
- Report의 main evidence는 50K-step convergence result다.
- Step-4000 result는 early diagnostic으로만 쓴다.
- `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean` 다섯 방법을 main comparison으로 둔다.
- Final score는 `tail`, `head`, `all` group을 분리해서 쓴다.
- Coverage가 없는 cell은 `0`이 아니라 `NA`로 쓴다.
- Target7은 모두 Latin script이므로 script diversity claim을 하지 않는다.

## 2. 문장 톤

- 짧은 문장을 쓴다. 긴 배경 설명보다 claim, evidence, interpretation을 분리한다.
- 문단은 `claim -> evidence -> interpretation -> boundary` 순서로 쓴다.
- 강한 일반화보다 controlled setup 안의 관찰로 쓴다.
- "proves"보다 "shows", "suggests", "in this controlled setup"을 선호한다.
- 특정 method가 모든 task에서 최고라고 쓰지 않는다. 모든 row가 뒷받침할 때만 best claim을 쓴다.
- 실패나 regression이 있으면 숨기지 말고 coverage, task family, group 차이와 함께 설명한다.

## 3. Claim-Evidence 작성 규칙

모든 핵심 문장은 아래 네 요소 중 최소 `claim`과 `evidence`를 가져야 한다.

| 요소 | 역할 | 예시 |
| --- | --- | --- |
| Claim | 주장 | v5.2 tokenizer는 target7 fragmentation을 줄였다. |
| Evidence | 근거 | `results_ko.md`의 tokens/word가 2.204에서 1.592로 감소했다. |
| Interpretation | 해석 | 따라서 tokenizer extension은 tail language surface segmentation에는 효과가 있었다. |
| Boundary | 한계 | 그러나 모든 method가 같은 tokenizer를 쓰므로 initialization 비교의 직접 원인은 아니다. |

좋은 문장 구조:

> v5.2 tokenizer는 target7 tokens/word를 2.204에서 1.592로 줄였다. 이 값은 `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md`에서 확인된다. 따라서 tokenizer extension은 fragmentation을 줄였지만, 모든 initialization method가 같은 tokenizer를 공유하므로 method 간 score 차이는 tokenizer만으로 설명하지 않는다.

피할 문장:

> v5.2 tokenizer는 아주 효과적이다.

이 문장은 짧지만 근거와 범위가 없으므로 report 문장으로 쓰지 않는다.

## 4. 숫자 작성 규칙

- 숫자는 항상 source artifact와 연결한다.
- Lower-better metric과 higher-better metric을 표 제목 또는 score column에 표시한다.
- Average score만 쓰지 말고 language coverage count를 같이 쓴다.
- Head/tail/all 평균이 같은 language set에서 계산됐는지 확인한다.
- Step이 다른 checkpoint의 score를 같은 final result처럼 섞지 않는다.

## 5. 표 작성 규칙

- Method 비교 표의 기본 column은 `Random`, `Mean`, `FVT`, `Weighted FVT`, `Family-aware mean`이다.
- Metric별 group row는 `tail`, `head`, `all`을 우선한다.
- Coverage가 없는 group은 `NA`와 이유를 적는다.
- Caption에는 table source를 적는다.
- 표 아래 해석 문장은 "무엇이 best인가"보다 "어느 metric/group에서 어떤 pattern이 보이는가"를 먼저 설명한다.

## 6. 그림 작성 규칙

모든 figure caption 또는 본문 설명은 아래 질문에 답해야 한다.

- 제목은 어떤 실험 단계와 비교 대상을 가리키는가?
- x축은 raw step, aligned step, language, metric 중 무엇인가?
- y축 metric은 무엇이고 낮을수록/높을수록 좋은가?
- point, marker, color, line은 각각 무엇을 의미하는가?
- 왜 이 step range를 보여주는가?
- smoothing, alignment, filtering이 있으면 원본 값이 어디에 보존되어 있는가?
- 이 그림으로 주장하면 안 되는 것은 무엇인가?

## 7. 50K Convergence Plot 유의사항

- `convergence_5way_loss_curve.png`는 final convergence 판단을 위한 main plot이다.
- x축은 raw local step이 아니라 weighted-FVT-aligned 1K grid다.
- 1K point interval은 checkpoint/log/evaluation granularity와 맞추기 위한 것이다.
- 50K는 4K/8K diagnostic으로는 수렴 주장을 하기 부족했기 때문에 둔 conservative convergence budget이다.
- Raw loss와 display loss를 구분한다.
- Plot-only smoothing/bridging이 있으면 반드시 disclosure를 적는다.

## 8. Reference 연결 규칙

- Glot500은 tokenizer expansion, continued MLM pretraining, head/tail/all reporting의 근거로 쓴다.
- XLM-R은 base encoder/tokenizer와 multilingual MLM framing의 근거로 쓴다.
- SentencePiece는 unigram tokenizer와 byte fallback 설정의 근거로 쓴다.
- FVT/WECHSEL/FOCUS/Hewitt 계열은 embedding initialization과 vocabulary transfer의 근거로 쓴다.
- Weighted FVT와 family-aware mean은 local experimental variants로 소개하고, 선행연구의 standard method처럼 쓰지 않는다.

## 9. 피해야 할 표현

- "FVT is always best."
- "Glot500을 완전 재현했다."
- "모든 low-resource language에 일반화된다."
- "target7은 script diversity를 대표한다."
- "4K에서 수렴했다."
- "coverage가 없는 task에서 target 성능이 개선됐다."
- "PPPL이 좋아졌으므로 downstream도 반드시 좋아진다."

## 10. 작성 전 체크

- [ ] 이 문단의 핵심 claim이 무엇인지 한 문장으로 말할 수 있는가?
- [ ] claim을 뒷받침하는 artifact path가 있는가?
- [ ] 근거가 없는 형용사나 부사가 없는가?
- [ ] 한 문장에 여러 주장이 섞여 있지 않은가?
- [ ] figure/table caption이 독립적으로 읽히는가?
- [ ] Step-4000과 50K가 섞이지 않았는가?
- [ ] coverage limitation을 같이 썼는가?
- [ ] final claim이 data보다 세지 않은가?
