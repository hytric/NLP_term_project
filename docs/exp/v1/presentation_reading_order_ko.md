# Second Try 발표 읽기 순서

작성일: 2026-06-12

이 문서는 `second_try` 실험을 발표할 때 읽고 보여줄 순서를 정리한 발표용 안내서다. 목표는 모든 step을 시간순으로 나열하는 것이 아니라, 청중이 이해하기 쉬운 task 흐름으로 재구성하는 것이다.

최종 발표 메시지는 다음 한 문장으로 고정한다.

> Vocabulary extension은 target10 언어의 tokenization fragmentation을 줄이지만, 현재 방식의 extended-vocabulary XLM-R adaptation은 clean v2 control에서 original continued pretraining보다 competitive하지 않다. 실패는 appended-token prediction에 집중된다.

## 발표 전체 흐름

```text
1. 문제 제기: 왜 unsupported-script/low-resource tokenizer가 문제인가
2. 데이터와 split: target10, Bible, v2 final 보호
3. Baseline tokenizer bottleneck 확인
4. Vocabulary extension으로 fragmentation이 줄어드는지 확인
5. Embedding initialization과 vocab size가 왜 중요한지 설명
6. Clean MLM control에서 positive model claim이 실패함을 보임
7. 실패 원인이 appended-token prediction임을 진단
8. 진단에서 파생되는 해결책 roadmap 제시
9. Repair attempts가 왜 충분하지 않았는지 정리
10. Smaller vocab / longer budget probe 결과 정리
11. Translation/downstream positive claim을 왜 막았는지 설명
12. Shortcut audit과 no-final-access 검증
13. 최종 top-tier-safe claim: diagnostic negative paper
```

## 발표 전 지켜야 할 문장

### 말해도 되는 문장

- "XLM-R tokenizer는 target10에서 fragmentation 병목을 보인다."
- "Vocabulary extension은 tokenization fragmentation을 줄인다."
- "하지만 v2 clean control에서 adapted extended-vocab model은 original continued pretraining보다 competitive하지 않다."
- "실패는 appended-token prediction에 집중된다."
- "현재 논문 claim은 positive performance claim이 아니라 diagnostic negative claim이다."

### 말하면 안 되는 문장

- "Adapted model이 original XLM-R보다 좋아졌다."
- "8k branch가 model adaptation을 해결했다."
- "Translation이 high-resource reference의 80%에 도달했다."
- "`ACT` final 결과를 확인했다."
- "Step07/Branch001 translation pass를 top-tier evidence로 쓴다."

## 빠른 발표용 수치

| 메시지 | 대표 수치 | 출처 |
| --- | ---: | --- |
| XLM-R fragmentation bottleneck | `syr tokens_per_word=4.854`; `single_char_token_pct=74.251` | [02 score](02_tokenization_audit/score_table.tsv) |
| Vocabulary extension improves tokenization | `avg_tokens_per_word_delta_pct=-31.766`; `single_char_delta_pct=-42.365` | [03 score](03_vocab_extension/score_table.tsv) |
| Step15 clean MLM control fails | adapted/original ratio `1.964580` | [15 score](15_v2_mlm_control/score_table.tsv) |
| Normalized metric also fails | word/char ratio `1.438660` | [16 score](16_v2_mlm_metric_fairness/score_table.tsv) |
| Added-token failure concentration | added/base loss ratio `2.835906`; added loss share `74.269955%` | [17 score](17_v2_added_token_failure_analysis/score_table.tsv) |
| Smaller 8k branch helps but is not enough | 8k raw loss `4.541285` vs 32k `4.946829`; raw ratio to original `1.803523` | [23 score](23_v2_vocab_size_objective_probe/score_table.tsv) |
| Selected 8k control fails | word/char ratio `1.472019` | [24 score](24_v2_8k_mlm_control/score_table.tsv) |
| Longer 8k budget fails | word/char ratio `1.587381` | [25 score](25_v2_8k_continued_budget_probe/score_table.tsv) |
| Manuscript package status | `PASS_MANUSCRIPT_READY` | [27 results](27_final_manuscript_synthesis/results.md) |

## Task별 발표 순서

### Task 1. 문제와 최종 메시지

목적:

- 발표 시작 1분 안에 "이 연구는 tokenizer win을 보였지만 model adaptation positive claim은 실패했다"는 프레임을 고정한다.
- 실패를 숨기는 발표가 아니라, 통제된 failure analysis임을 먼저 말한다.

수행상황:

- Step26에서 final claim contract가 완성됐다.
- Step27에서 manuscript-ready package가 완성됐다.
- Positive performance paper는 blocked, diagnostic negative paper는 ready.

발표에 쓸 시각화:

- 한 장짜리 flow diagram:
  - `tokenization bottleneck -> vocab extension helps -> clean MLM control fails -> added-token failure -> repair probes fail -> diagnostic claim`

Before-after 예시:

- Before framing:
  - "Vocabulary extension improves XLM-R."
- After framing:
  - "Vocabulary extension improves tokenization, but controlled XLM-R adaptation remains noncompetitive."

볼 table:

- [27 score](27_final_manuscript_synthesis/score_table.tsv)
- [26 evidence table](26_top_tier_diagnostic_claim_synthesis/evidence_table.tsv)
- [26 unsupported claims](26_top_tier_diagnostic_claim_synthesis/unsupported_claims.tsv)

요약 문서:

- [Step27 results](27_final_manuscript_synthesis/results.md)
- [Step27 manuscript outline](27_final_manuscript_synthesis/manuscript_outline.md)
- [Step27 paper claims](27_final_manuscript_synthesis/paper_claims.md)
- [Step26 final claim contract](26_top_tier_diagnostic_claim_synthesis/final_claim_contract.md)

발표용 문장:

> 이 발표의 결론은 성공 주장보다 더 보수적입니다. Vocabulary extension은 tokenization을 개선하지만, clean v2 control에서 model adaptation은 실패했고, 그 실패 원인을 appended-token prediction으로 좁혔습니다.

---

### Task 2. 데이터, target10, split 설계

목적:

- 어떤 언어와 데이터를 썼는지 설명한다.
- 왜 v2 split을 새로 만들었는지 설명한다.
- `JOH`는 burned old test, `ACT`는 clean final holdout으로 분리했다는 점을 강조한다.

수행상황:

- Step01에서 initial data/split을 구성했다.
- Step11에서 fresh holdout feasibility를 검토했다.
- Step12에서 v2 split을 만들었다.
- 이후 Step13-27은 `ACT` final을 읽지 않은 상태로 진행됐다.

발표에 쓸 시각화:

- Split diagram:
  - train: `all except MAR, JOH, ACT`
  - dev: `MAR`
  - burned old test: `JOH`
  - protected final: `ACT`
- Target10 language table: language, script, role.

Before-after 예시:

- Before: v1에서는 `JOH` test-aware selection 위험이 있었다.
- After: v2에서는 `ACT` final을 보호하고 `JOH`를 burned로 제외했다.

볼 table:

- [01 split stats](01_data_and_splits/split_stats.tsv)
- [12 split stats](12_v2_split_protocol/v2_split_stats.tsv)
- [12 execution matrix](12_v2_split_protocol/v2_execution_matrix.tsv)
- [12 score](12_v2_split_protocol/score_table.tsv)

요약 문서:

- [01 results](01_data_and_splits/results.md)
- [11 results](11_fresh_holdout_feasibility/results.md)
- [12 results](12_v2_split_protocol/results.md)
- [12 rerun protocol](12_v2_split_protocol/v2_rerun_protocol.md)

발표용 문장:

> v1 결과는 탐색 evidence로만 남기고, 최종 claim은 `ACT` final을 보호하는 v2 split 기준으로만 판단했습니다.

---

### Task 3. Baseline tokenization bottleneck 확인

목적:

- 기존 XLM-R tokenizer가 target10 언어에서 과도하게 쪼개지는지 정량화한다.
- 연구의 출발점이 실제 병목인지 보여준다.

수행상황:

- Step02 완료.
- XLM-R baseline tokenization bottleneck이 확인됐다.

발표에 쓸 시각화:

- 언어별 `tokens_per_word` bar chart.
- 언어별 `single_char_token_pct` bar chart.
- high-fragmentation token preview 한두 개.

Before-after 예시:

- Before-only 예시로 Step02 token preview를 보여준다.
- 예시 파일: [02 tokenization examples](02_tokenization_audit/tokenization_examples.md)
- 발표 때는 `ake`, `bsn`, `syr`, `cop` 중 하나를 골라 XLM-R가 글자를 잘게 찢는 모습을 보여준다.

볼 table:

- [02 score](02_tokenization_audit/score_table.tsv)
- [02 baseline metrics](02_tokenization_audit/xlmr_baseline_tokenization_metrics.tsv)

요약 문서:

- [02 results](02_tokenization_audit/results.md)
- [02 tokenization examples](02_tokenization_audit/tokenization_examples.md)

발표용 문장:

> XLM-R는 일부 target 언어에서 단어를 의미 있는 subword보다 single-character 단위에 가깝게 분해합니다. 이게 vocabulary extension의 직접 동기입니다.

---

### Task 4. Vocabulary extension과 before-after tokenization

목적:

- XLM-R id를 보존하면서 target-language pieces를 append하면 fragmentation이 줄어드는지 보여준다.
- tokenizer-level positive result를 명확히 말한다.

수행상황:

- Step03에서 initial 8k/16k/32k tokenizer extension을 수행했다.
- Step13에서 v2 train-only tokenizer rerun을 수행했고, Mark/dev 기준으로 tokenizer를 선택했다.
- Tokenization 개선은 supported claim이다.

발표에 쓸 시각화:

- Before/after token count bar:
  - base token count vs selected token count.
- Token preview two-column slide:
  - 왼쪽 XLM-R base tokens
  - 오른쪽 extended tokenizer tokens

Before-after 예시:

- [13 v2 tokenization examples](13_v2_tokenizer/v2_tokenization_examples.md)
- 좋은 발표 예시:
  - `acu b.MAR.1.1`: base token count `23` -> selected token count `13`
  - `bsn b.MAR.1.1`: base token count `341` -> selected token count `167`
  - `kbh b.MAR.1.1`: base token count `39` -> selected token count `14`
- v1 스타일 예시도 필요하면 [03 tokenization examples](03_vocab_extension/tokenization_examples.md)를 appendix로 사용한다.

볼 table:

- [03 score](03_vocab_extension/score_table.tsv)
- [03 vocab merge report](03_vocab_extension/vocab_merge_report.tsv)
- [13 score](13_v2_tokenizer/score_table.tsv)
- [13 v2 vocab metrics](13_v2_tokenizer/v2_vocab_extension_metrics.tsv)
- [13 v2 merge report](13_v2_tokenizer/v2_vocab_merge_report.tsv)

요약 문서:

- [03 results](03_vocab_extension/results.md)
- [13 results](13_v2_tokenizer/results.md)
- [13 selected tokenizer](13_v2_tokenizer/selected_tokenizer.md)

발표용 문장:

> Tokenizer level에서는 성공입니다. 새 vocabulary는 XLM-R id를 보존하면서 target text fragmentation을 줄였습니다.

---

### Task 5. Embedding initialization

목적:

- 새 token row가 생기면 embedding과 LM head를 어떻게 초기화해야 하는지 설명한다.
- initialization이 zero-step MLM readiness에 영향을 준다는 점을 보여준다.

수행상황:

- Step04에서 initial init methods를 비교했다.
- Step14에서 v2 tokenizer 기준 random, mean, fvt, align, focus를 비교했다.
- Step21에서 `mean`과 `align`이 full MLM budget에서 `fvt`를 이기지 못함을 확인했다.

발표에 쓸 시각화:

- Init method별 zero-step loss bar chart.
- `random`, `mean`, `fvt`, `align`, `focus` 비교표.
- nearest neighbor 예시는 appendix로 사용한다.

Before-after 예시:

- Before: 새 token embedding row가 없음.
- After: 새 row가 초기화되고 model checkpoint가 load 가능해짐.
- Nearest-neighbor qualitative 예시:
  - [04 nearest neighbors](04_embedding_init/nearest_neighbors.md)
  - [14 v2 nearest neighbors](14_v2_embedding_init/v2_nearest_neighbors.md)

볼 table:

- [04 score](04_embedding_init/score_table.tsv)
- [04 embedding init metrics](04_embedding_init/embedding_init_metrics.tsv)
- [14 score](14_v2_embedding_init/score_table.tsv)
- [14 v2 init scores](14_v2_embedding_init/v2_embedding_init_scores.tsv)
- [14 zero-step MLM](14_v2_embedding_init/v2_zero_step_mlm.tsv)
- [21 score](21_v2_alt_init_mlm_probe/score_table.tsv)
- [21 init probe summary](21_v2_alt_init_mlm_probe/init_probe_summary.tsv)

요약 문서:

- [04 results](04_embedding_init/results.md)
- [14 results](14_v2_embedding_init/results.md)
- [14 selected init](14_v2_embedding_init/selected_init.md)
- [21 results](21_v2_alt_init_mlm_probe/results.md)

발표용 문장:

> Initialization은 중요하지만, initialization만으로 model adaptation failure가 해결되지는 않았습니다. Step21에서 mean과 align도 fvt를 넘지 못했습니다.

---

### Task 6. MLM adaptation과 original-control failure

목적:

- tokenizer 개선이 실제 model adaptation 성능으로 이어졌는지 검증한다.
- matched-token original continued-pretraining control이 왜 필요한지 설명한다.

수행상황:

- Step05 initial MLM adaptation은 exploratory/limited evidence다.
- Step15 v2 clean MLM control에서 adapted model은 original continued-pretraining control보다 나빴다.
- Step16 normalized metric audit도 같은 결론을 냈다.

발표에 쓸 시각화:

- Learning curve line chart:
  - adapted extended vs original control.
- Final dev loss bar:
  - adapted mean vs original mean.
- Normalized word/char ratio bar:
  - threshold `1.100000` 선을 표시.

Before-after 예시:

- Before: initialized extended checkpoint.
- After: MLM adaptation 후 adapted loss는 자기 zero-step보다 개선되지만, original control과 비교하면 실패.
- 발표 핵심 비교:
  - Step15 adapted/original ratio `1.964580`
  - Step16 word/char ratio `1.438660`

볼 table:

- [05 score](05_mlm_adaptation/score_table.tsv)
- [15 score](15_v2_mlm_control/score_table.tsv)
- [15 seed summary](15_v2_mlm_control/seed_summary.tsv)
- [15 learning curves](15_v2_mlm_control/mlm_learning_curves.tsv)
- [16 score](16_v2_mlm_metric_fairness/score_table.tsv)
- [16 normalized scores](16_v2_mlm_metric_fairness/normalized_mlm_scores.tsv)

요약 문서:

- [05 results](05_mlm_adaptation/results.md)
- [15 results](15_v2_mlm_control/results.md)
- [15 checkpoint selection](15_v2_mlm_control/checkpoint_selection.md)
- [16 results](16_v2_mlm_metric_fairness/results.md)

발표용 문장:

> Adapted checkpoint는 자기 초기 상태보다 좋아졌지만, top-tier claim은 original continued-pretraining control을 이겨야 합니다. 그 기준에서는 실패했습니다.

---

### Task 7. Added-token failure diagnosis

목적:

- 왜 adapted model이 실패했는지 category-level로 분해한다.
- 실패가 base-token 전체가 아니라 appended-token prediction에 집중됨을 보여준다.

수행상황:

- Step17 완료.
- Added tokens are `50.456741%` of adapted non-special tokens but account for `74.269955%` of adapted MLM loss.
- Added/base loss ratio is `2.835906`.

발표에 쓸 시각화:

- Pie/bar chart:
  - added token share vs added loss share.
- Category loss bar:
  - base-token loss vs added-token loss.
- Language-level heatmap:
  - iso별 added_token_pct와 loss_added.

Before-after 예시:

- Before: "왜 MLM이 안 되는지 모름."
- After: "added-token prediction이 dominant failure source."
- Hard added-token examples:
  - [17 new token loss samples](17_v2_added_token_failure_analysis/new_token_loss_samples.tsv)

볼 table:

- [17 score](17_v2_added_token_failure_analysis/score_table.tsv)
- [17 token category loss](17_v2_added_token_failure_analysis/token_category_loss.tsv)
- [17 language token breakdown](17_v2_added_token_failure_analysis/language_token_breakdown.tsv)
- [17 new token loss samples](17_v2_added_token_failure_analysis/new_token_loss_samples.tsv)

요약 문서:

- [17 results](17_v2_added_token_failure_analysis/results.md)

발표용 문장:

> Tokenizer는 text를 덜 쪼개게 만들었지만, model은 새 token을 잘 예측하지 못했습니다. 실패는 appended-token rows에 집중되어 있습니다.

---

### Task 8. 해결책 roadmap: appended-token bottleneck을 어떻게 풀 것인가

목적:

- "원인을 찾았으면 어떤 해결책이 맞는가"에 답한다.
- 단순 future work가 아니라 appended-token bottleneck에 직접 대응하는 remedy를 제시한다.
- 다만 아직 검증된 성능 개선이 아니므로 solution hypothesis로 말한다.

수행상황:

- Step28에서 appended-token solution roadmap을 작성했다.
- 후보 해결책 `6개`, future experiment protocol `5개`를 정의했다.
- 최우선 해결책은 subtoken-teacher distillation + curriculum added-token MLM + base KL/replay preservation이다.

발표에 쓸 시각화:

- Diagnosis-to-remedy diagram:
  - `added-token loss dominates -> teacher-guided appended rows -> curriculum added MLM -> base KL/replay -> Step15/16 control rerun`
- Solution candidate table:
  - method, targeted failure, mechanism, pass gate.

Before-after 예시:

- Before:
  - ordinary MLM mask만으로 appended tokens를 학습한다.
- After:
  - original XLM-R subtoken decomposition을 teacher signal로 사용해 appended token span을 supervision한다.
  - added-token pressure를 curriculum으로 키우고 base-token behavior는 KL/replay로 보존한다.

볼 table:

- [28 solution candidates](28_appended_token_solution_roadmap/solution_candidates.tsv)
- [28 experiment protocol](28_appended_token_solution_roadmap/experiment_protocol.tsv)
- [28 score](28_appended_token_solution_roadmap/score_table.tsv)

요약 문서:

- [28 solution roadmap](28_appended_token_solution_roadmap/solution_roadmap.md)
- [28 presentation insert](28_appended_token_solution_roadmap/presentation_insert.md)
- [28 results](28_appended_token_solution_roadmap/results.md)

발표용 문장:

> 진단이 가리키는 해결책은 단순히 더 오래 학습하는 것이 아니라, appended token을 original XLM-R subtoken teacher로 지도하고, base-token behavior를 KL/replay로 보존하면서 curriculum으로 added-token prediction을 키우는 것입니다. 이건 아직 proven result가 아니라, 다음 positive claim을 열기 위한 falsifiable protocol입니다.

---

### Task 9. Repair attempts: 좋아진 부분과 실패한 gate를 분리

목적:

- "해결하려고 무엇을 했는가"를 보여준다.
- partial improvement와 top-tier success를 구분한다.

수행상황:

- Step18 added-token weighting:
  - added loss improves `3/3`
  - all-token nonworse `0/3`
  - repair gate fail
- Step19 new-row-only:
  - trainable audit passes `3/3`
  - base nonworse `3/3`
  - added improves `0/3`
  - repair gate fail
- Step20 staged/lower-rate:
  - `9/9` runs complete
  - passing variants `0/3`
  - repair gate fail

발표에 쓸 시각화:

- Repair attempt matrix:
  - rows: Step18, Step19, Step20
  - columns: added improved, base nonworse, all nonworse, seed-stable pass.
- Traffic-light table:
  - green for partial success
  - red for failed required gate.

Before-after 예시:

- Step18:
  - Before: added-token loss high.
  - After: added loss improves, but all-token loss worsens.
- Step19:
  - Before: base behavior may be damaged.
  - After: base rows preserved, but added-token prediction does not improve.

볼 table:

- [18 score](18_v2_added_token_repair/score_table.tsv)
- [18 repair summary](18_v2_added_token_repair/repair_summary.tsv)
- [18 repair category loss](18_v2_added_token_repair/repair_category_loss.tsv)
- [19 score](19_v2_new_row_only_repair/score_table.tsv)
- [19 new-row summary](19_v2_new_row_only_repair/new_row_repair_summary.tsv)
- [19 trainable parameters](19_v2_new_row_only_repair/trainable_parameters.tsv)
- [20 score](20_v2_staged_added_token_repair/score_table.tsv)
- [20 staged summary](20_v2_staged_added_token_repair/staged_repair_summary.tsv)
- [20 variant summary](20_v2_staged_added_token_repair/variant_summary.tsv)

요약 문서:

- [18 results](18_v2_added_token_repair/results.md)
- [19 results](19_v2_new_row_only_repair/results.md)
- [20 results](20_v2_staged_added_token_repair/results.md)
- [20 variant selection](20_v2_staged_added_token_repair/variant_selection.md)

발표용 문장:

> Repair attempts는 useful diagnostic information을 줬지만, top-tier positive model claim을 열 gate는 통과하지 못했습니다.

---

### Task 10. Smaller vocab branch와 longer budget probe

목적:

- 32k appended vocab이 너무 커서 생긴 문제인지 검증한다.
- 8k branch와 longer budget이 positive claim을 구제하는지 확인한다.

수행상황:

- Step23:
  - 8k/16k smaller-vocab branches pass redesign probe.
  - best 8k raw loss `4.541285` vs 32k `4.946829`.
  - 하지만 raw ratio to original is `1.803523`.
- Step24:
  - selected 8k normalized control fails.
  - word/char ratio `1.472019`.
- Step25:
  - longer 8k budget fails.
  - word/char ratio worsens to `1.587381`.

발표에 쓸 시각화:

- Vocab size vs raw loss bar:
  - 32k, 16k, 8k.
- 8k vs original normalized ratio bar:
  - threshold `1.100000` 표시.
- 500k vs 1M-ish budget comparison:
  - 8k improves, original improves faster.

Before-after 예시:

- Before: 32k branch has severe added-token burden.
- After: 8k mitigates burden but still fails original-control competitiveness.

볼 table:

- [23 score](23_v2_vocab_size_objective_probe/score_table.tsv)
- [23 vocab probe summary](23_v2_vocab_size_objective_probe/vocab_probe_summary.tsv)
- [23 vocab variant summary](23_v2_vocab_size_objective_probe/vocab_probe_variant_summary.tsv)
- [24 score](24_v2_8k_mlm_control/score_table.tsv)
- [24 raw control summary](24_v2_8k_mlm_control/raw_control_summary.tsv)
- [24 normalized scores](24_v2_8k_mlm_control/normalized_mlm_scores.tsv)
- [25 score](25_v2_8k_continued_budget_probe/score_table.tsv)
- [25 continued budget summary](25_v2_8k_continued_budget_probe/continued_budget_summary.tsv)
- [25 normalized scores](25_v2_8k_continued_budget_probe/normalized_mlm_scores.tsv)

요약 문서:

- [23 results](23_v2_vocab_size_objective_probe/results.md)
- [24 results](24_v2_8k_mlm_control/results.md)
- [25 results](25_v2_8k_continued_budget_probe/results.md)

발표용 문장:

> Smaller vocab is a good redesign direction, but not a positive result yet. 8k helps relative to 32k, but it still loses to original continued pretraining under normalized controls.

---

### Task 11. Downstream / translation claim을 왜 막았는가

목적:

- v1 downstream/translation 결과를 어떻게 해석해야 하는지 설명한다.
- Step07/Branch001을 왜 top-tier evidence로 쓰면 안 되는지 설명한다.
- v2 positive downstream/translation final readout이 왜 아직 열리지 않았는지 설명한다.

수행상황:

- Step06 downstream proxy는 exploratory/legacy evidence다.
- Step07 translation benchmark에는 branch pass가 있었지만 Step09/10에서 invalidated 또는 exploratory로 downgrade됐다.
- Step09 method-matched translation ratio:
  - selected adapted XLM-R `0.638034`
  - LaBSE+CSLS upper bound `0.567179`
  - threshold `0.800000`
- v2 downstream/translation final readout은 positive model gate가 실패했기 때문에 blocked.

발표에 쓸 시각화:

- Translation ratio bar:
  - selected adapted XLM-R
  - LaBSE+CSLS upper bound
  - threshold `0.800000`
- Evidence status table:
  - v1 branch: exploratory/invalidated
  - v2 final readout: not opened

Before-after 예시:

- Before: Step07 branch row looked like a translation pass.
- After: Step09 method-matched audit and Step10 leakage/selection audit block it as top-tier claim.

볼 table:

- [06 score](06_downstream_tasks/score_table.tsv)
- [06 downstream results](06_downstream_tasks/downstream_results.tsv)
- [07 score](07_translation_benchmark/score_table.tsv)
- [07 translation results](07_translation_benchmark/translation_results.tsv)
- [09 score](09_top_tier_validation/score_table.tsv)
- [09 method matched translation](09_top_tier_validation/method_matched_translation.tsv)
- [10 leakage audit](10_leakage_selection_audit/leakage_audit.tsv)
- [10 invalidated runs](10_leakage_selection_audit/invalidated_runs.tsv)

Before-after / qualitative 예시:

- [06 sample predictions](06_downstream_tasks/sample_predictions.md)
- [06 failure cases](06_downstream_tasks/failure_cases.md)
- [07 sample translations](07_translation_benchmark/sample_translations.md)
- [07 failure cases](07_translation_benchmark/failure_cases.md)
- [07 branch sentence embedding samples](07_translation_benchmark/branch_sentence_embedding_samples.md)
- [10 selection trace](10_leakage_selection_audit/selection_trace.md)

요약 문서:

- [06 results](06_downstream_tasks/results.md)
- [07 results](07_translation_benchmark/results.md)
- [09 results](09_top_tier_validation/results.md)
- [10 results](10_leakage_selection_audit/results.md)

발표용 문장:

> Translation success처럼 보였던 v1 branch는 method mismatch와 selection leakage risk 때문에 top-tier evidence로 쓰지 않습니다. 이 점을 막았기 때문에 최종 claim이 더 보수적이고 안전해졌습니다.

---

### Task 12. Shortcut audit과 no-final-access 검증

목적:

- 결과가 shortcut pass가 아님을 보여준다.
- 동시에 positive claim이 왜 blocked인지 명확히 한다.

수행상황:

- Step22 full audit 완료.
- v2 Steps 13-27 keep `ACT` final protected.
- no-final audit rows: `46`
- no-final bad rows: `0`
- v2 positive adapted-model claim allowed: `0`

발표에 쓸 시각화:

- Audit matrix:
  - v1 translation: invalidated
  - v2 final leakage: no active shortcut found
  - positive model claim: blocked
  - diagnostic claim: ready

Before-after 예시:

- Before: branch search and mixed-method comparison could inflate claims.
- After: Step22/26/27 explicitly block unsupported positive wording.

볼 table:

- [22 score](22_full_experiment_audit/score_table.tsv)
- [22 shortcut matrix](22_full_experiment_audit/shortcut_matrix.tsv)
- [26 score](26_top_tier_diagnostic_claim_synthesis/score_table.tsv)
- [27 score](27_final_manuscript_synthesis/score_table.tsv)
- [27 reproducibility checklist](27_final_manuscript_synthesis/reproducibility_checklist.tsv)

요약 문서:

- [22 results](22_full_experiment_audit/results.md)
- [26 results](26_top_tier_diagnostic_claim_synthesis/results.md)
- [27 results](27_final_manuscript_synthesis/results.md)
- [08 final checklist](08_final_analysis/final_checklist.md)

발표용 문장:

> Shortcut audit 결과, v2 final leakage는 발견되지 않았습니다. 하지만 no-shortcut이 positive success를 뜻하지는 않습니다. Positive model claim은 여전히 blocked입니다.

---

### Task 13. 최종 claim과 논문 패키지

목적:

- 발표 마지막에서 청중이 가져갈 claim을 고정한다.
- 어떤 논문으로 써야 하는지, 어떤 논문으로 쓰면 안 되는지 말한다.

수행상황:

- Step26: `PASS_DIAGNOSTIC_CLAIM_READY`
- Step27: `PASS_MANUSCRIPT_READY`
- Diagnostic negative manuscript package ready.
- Positive performance manuscript blocked.

발표에 쓸 시각화:

- Final claim slide:
  - "Tokenization improves"
  - "Model adaptation fails under controls"
  - "Failure source: appended-token prediction"
  - "Claim type: diagnostic negative result"
- Reviewer risk table:
  - common objection -> evidence response.

Before-after 예시:

- Before framing:
  - "Vocabulary extension improves XLM-R."
- After framing:
  - "Vocabulary extension improves tokenization but not current controlled MLM competitiveness."

볼 table:

- [27 paper tables](27_final_manuscript_synthesis/paper_tables.tsv)
- [27 reviewer risk audit](27_final_manuscript_synthesis/reviewer_risk_audit.tsv)
- [27 reproducibility checklist](27_final_manuscript_synthesis/reproducibility_checklist.tsv)
- [26 evidence table](26_top_tier_diagnostic_claim_synthesis/evidence_table.tsv)
- [26 unsupported claims](26_top_tier_diagnostic_claim_synthesis/unsupported_claims.tsv)
- [26 next positive experiments](26_top_tier_diagnostic_claim_synthesis/next_positive_experiments.tsv)

요약 문서:

- [27 manuscript outline](27_final_manuscript_synthesis/manuscript_outline.md)
- [27 paper claims](27_final_manuscript_synthesis/paper_claims.md)
- [26 final claim contract](26_top_tier_diagnostic_claim_synthesis/final_claim_contract.md)
- [08 claim evidence map](08_final_analysis/claim_evidence_map.md)

발표용 문장:

> 이 결과는 "우리가 성능을 올렸다"가 아니라 "tokenization 개선만으로는 충분하지 않고, appended-token learning이 실제 병목으로 남는다"는 통제된 negative result입니다.

## 슬라이드 구성 추천

| Slide | 제목 | 핵심 자료 | 말할 내용 |
| ---: | --- | --- | --- |
| 1 | One-sentence claim | [27 paper claims](27_final_manuscript_synthesis/paper_claims.md) | Diagnostic negative claim |
| 2 | Problem setup | [02 results](02_tokenization_audit/results.md) | Unsupported-script tokenization bottleneck |
| 3 | Data and split | [12 results](12_v2_split_protocol/results.md) | v2 split, `ACT` protected |
| 4 | Baseline bottleneck | [02 score](02_tokenization_audit/score_table.tsv) | XLM-R fragmentation |
| 5 | Tokenization before/after | [13 examples](13_v2_tokenizer/v2_tokenization_examples.md) | token count reduction examples |
| 6 | Initialization | [14 score](14_v2_embedding_init/score_table.tsv) | init affects readiness |
| 7 | Clean MLM control | [15 score](15_v2_mlm_control/score_table.tsv) | adapted/original ratio fails |
| 8 | Normalized metric audit | [16 score](16_v2_mlm_metric_fairness/score_table.tsv) | not just raw-token artifact |
| 9 | Failure localization | [17 score](17_v2_added_token_failure_analysis/score_table.tsv) | added-token failure source |
| 10 | Proposed solution roadmap | [28 solution roadmap](28_appended_token_solution_roadmap/solution_roadmap.md), [28 protocol](28_appended_token_solution_roadmap/experiment_protocol.tsv) | teacher-guided appended-token learning |
| 11 | Repair attempts | [20 variant summary](20_v2_staged_added_token_repair/variant_summary.tsv) | no seed-stable repair |
| 12 | Smaller vocab and budget | [23 score](23_v2_vocab_size_objective_probe/score_table.tsv), [24 score](24_v2_8k_mlm_control/score_table.tsv), [25 score](25_v2_8k_continued_budget_probe/score_table.tsv) | 8k helps but fails controls |
| 13 | Translation/downstream blocked | [09 score](09_top_tier_validation/score_table.tsv), [10 results](10_leakage_selection_audit/results.md) | v1 translation pass invalidated |
| 14 | Shortcut audit | [22 results](22_full_experiment_audit/results.md) | no active v2 shortcut; positive claim blocked |
| 15 | Final claim | [26 final claim contract](26_top_tier_diagnostic_claim_synthesis/final_claim_contract.md) | diagnostic negative result |
| 16 | Manuscript package | [27 manuscript outline](27_final_manuscript_synthesis/manuscript_outline.md) | ready to write paper |

## 발표용 visual 제작 목록

| Visual | 만들 내용 | Source | 추천 위치 |
| --- | --- | --- | --- |
| V1 | v2 split flow diagram | [12 execution matrix](12_v2_split_protocol/v2_execution_matrix.tsv) | Slide 3 |
| V2 | language별 baseline `tokens_per_word` bar | [02 metrics](02_tokenization_audit/xlmr_baseline_tokenization_metrics.tsv) | Slide 4 |
| V3 | tokenization before/after token count bar | [13 examples](13_v2_tokenizer/v2_tokenization_examples.md) | Slide 5 |
| V4 | init method zero-step loss bar | [14 zero-step MLM](14_v2_embedding_init/v2_zero_step_mlm.tsv) | Slide 6 |
| V5 | adapted vs original MLM final loss bar | [15 seed summary](15_v2_mlm_control/seed_summary.tsv) | Slide 7 |
| V6 | normalized ratio vs threshold bar | [16 normalized scores](16_v2_mlm_metric_fairness/normalized_mlm_scores.tsv), [24 normalized scores](24_v2_8k_mlm_control/normalized_mlm_scores.tsv), [25 normalized scores](25_v2_8k_continued_budget_probe/normalized_mlm_scores.tsv) | Slides 8, 11 |
| V7 | added token share vs loss share bar | [17 token category loss](17_v2_added_token_failure_analysis/token_category_loss.tsv) | Slide 9 |
| V8 | diagnosis-to-remedy diagram | [28 solution roadmap](28_appended_token_solution_roadmap/solution_roadmap.md), [28 presentation insert](28_appended_token_solution_roadmap/presentation_insert.md) | Slide 10 |
| V9 | repair matrix traffic-light table | [18 score](18_v2_added_token_repair/score_table.tsv), [19 score](19_v2_new_row_only_repair/score_table.tsv), [20 score](20_v2_staged_added_token_repair/score_table.tsv) | Slide 11 |
| V10 | vocab size probe bar | [23 vocab summary](23_v2_vocab_size_objective_probe/vocab_probe_summary.tsv) | Slide 12 |
| V11 | shortcut/claim status matrix | [22 shortcut matrix](22_full_experiment_audit/shortcut_matrix.tsv), [27 reviewer risk audit](27_final_manuscript_synthesis/reviewer_risk_audit.tsv) | Slides 14, 16 |

## 발표 때 appendix로 넘길 자료

- Full step index: [step_index](step_index.md)
- Full plan: [plan](plan.md)
- Final analysis: [08 results](08_final_analysis/results.md)
- Claim evidence map: [08 claim evidence map](08_final_analysis/claim_evidence_map.md)
- Manuscript package:
  - [27 manuscript outline](27_final_manuscript_synthesis/manuscript_outline.md)
  - [27 paper claims](27_final_manuscript_synthesis/paper_claims.md)
  - [27 paper tables](27_final_manuscript_synthesis/paper_tables.tsv)
  - [27 reviewer risk audit](27_final_manuscript_synthesis/reviewer_risk_audit.tsv)
  - [27 reproducibility checklist](27_final_manuscript_synthesis/reproducibility_checklist.tsv)
- Solution roadmap:
  - [28 solution roadmap](28_appended_token_solution_roadmap/solution_roadmap.md)
  - [28 solution candidates](28_appended_token_solution_roadmap/solution_candidates.tsv)
  - [28 experiment protocol](28_appended_token_solution_roadmap/experiment_protocol.tsv)
  - [28 presentation insert](28_appended_token_solution_roadmap/presentation_insert.md)

## 마지막 슬라이드 문장

> The tokenizer problem is real, and vocabulary extension helps tokenization. But under leakage-safe v2 controls, the adapted extended-vocabulary model fails against original continued pretraining. The main contribution is therefore a controlled diagnostic negative result: appended-token prediction is the bottleneck that future objectives or data redesigns must solve.
