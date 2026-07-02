# v5 Final Deck Source Korean

작성 상태: execution draft, 2026-06-28 기준.

이 파일은 실제 PPT 제작용 한국어 slide source이다. 숫자와 claim은
`ppt_content.md`, `presenter_script_ko.md`, `00_tables/`,
`post_result_patch_plan_ko.md`, `post_checkpoint_outcome_matrix_ko.md`,
`final_claim_decision_tree.md`
와 동기화해야 한다. 현재 final conclusion은 `decision_tree_waiting_for_results`
상태이므로 after-MLM/downstream 개선 주장은 잠금 상태이다.
현재 checkpoint 진행률과 평가 Go/No-Go는 이 source에 직접 고정하지 않고
`final_action_dashboard_ko.md`와 `run_v5_post_checkpoint_evals.sh status`를
우선한다.

---

## 1. 제목

**Controlled Glot500-Style Replay with Vocabulary-Extension Initialization**

- 92 XLM-R-seen Glot500 language-scripts
- 10 Glot500-internal non-XLM-R target language-scripts
- novelty: appended vocabulary row initialization

Source:

```text
docs/exp/v5/4_reporting/03_final_report/claim_ledger.md
docs/exp/v5/4_reporting/final_claim_decision_tree.md
```

---

## 2. 문제의식과 기여

**Problem: multilingual coverage is broad, but not uniform.**

- Reproduction: artifact-audited 92+10 Glot500-style replay
- Novelty: appended vocabulary row initialization with FVT
- Fidelity: PPPL, retrieval, classification, tagging, Roundtrip retained
- Claim rule: final method claims wait for matched checkpoints

---

## 3. 재연 범위

**Full Glot500 reproduction이 아니라 controlled subset replay이다.**

Scope comparison:

- scale: Glot500 500+ languages -> v5 102 language-scripts
- corpus: Glot500-c -> 92 seen + 10 target
- tokenizer: SentencePiece expansion -> SPM append-style expansion
- training: continued MLM -> continued MLM
- evaluation: Glot500 metrics -> same metric families

Backup evidence:

```text
docs/exp/v5/4_reporting/00_tables/table_15_glot500_reproduction_fidelity.md
docs/exp/v5/4_reporting/01_figures/generated/figure_01_experiment_pipeline.png
```

금지 표현:

```text
full 511-language Glot500 reproduction
```

---

## 4. Target10 선정

**Target10은 Glot500 내부 raw dataset에서 골랐다.**

선정 조건:

- XLM-R seen이 아님
- `new_length >= 30000`
- local raw directory 존재
- 지역/문자/어족 다양성

Coverage snapshot:

- scripts: Latn, Cyrl, Arab, Tibt, Olck
- regions: Europe, North Caucasus, West Asia, Himalaya, South/Southeast Asia,
  West Africa, Mesoamerica, Andean South America, Polynesia
- new_length range: 30,052-52,732

Target codes:

```text
fur_Latn, krc_Cyrl, acm_Arab, dzo_Tibt, sat_Olck,
mad_Latn, bam_Latn, kjb_Latn, quw_Latn, rap_Latn
```

Source:

```text
docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv
```

---

## 5. Corpus construction

**Data scope는 고정됐다.**

Corpus snapshot:

- seen languages: 92
- target languages: 10
- merged lines: 92,452,251
- output size: 19G
- missing language dirs: 0

Claim:

```text
The 102-language corpus is reproducibly merged with no missing directories.
```

---

## 6. Tokenizer method

**v5는 Glot500-style SentencePiece append route를 따른다.**

- XLM-R SPM에 auxiliary SPM의 novel pieces를 append
- extended HF tokens: 368,687
- appended token strings: 118,685
- `<mask>` id: 250001 -> 368686

Audit result:

- 29/30 audited languages improved
- target10: 9/10 improved
- `dzo_Tibt`: 4.223938 -> 5.552124 tokens/word로 악화

Figure:

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_02_tokenizer_fertility_delta.png
```

---

## 7. Novelty

**Novelty는 corpus가 아니라 appended vocabulary row initialization이다.**

Initialization arms:

- random: HF default random resize, baseline
- mean: source/global mean, stable ablation
- fvt: source-token decomposition mean, main novelty
- align: script-aware fallback, exploratory

핵심 질문:

```text
new token row를 random으로 둘 것인가, 기존 tokenizer decomposition으로 초기화할 것인가?
```

---

## 8. Initialization audit

**초기화 비교는 row-copy correctness가 보장될 때만 의미가 있다.**

필수 audit:

- source rows copied by token identity
- `<mask>` row remapped explicitly
- byte fallback rows separated
- LM head tying verified

Main FVT audit:

- source identity rows: 250,002
- FVT rows: 118,427
- byte/global-mean rows: 256
- lexical fallback rows: 2
- `<mask>` max abs diff: 0.0

---

## 9. Zero-step evidence

**FVT는 training 전 target MLM proxy에서 가장 좋다.**

Zero-step target weighted NLL:

- random: 18.411756
- mean: 11.953142
- fvt: 8.785518

FVT vs random:

- target: -9.626238 NLL
- relative reduction: 52.28%

주의:

```text
This is intrinsic zero-step evidence, not after-MLM or downstream proof.
```

---

## 10. Training setup

**Main method claim은 matched MLM checkpoint 이후에만 열린다.**

Fixed comparison:

- model: XLM-R-base initialized with v5 tokenizer
- methods: `v5_random` vs `v5_fvt`
- corpus/tokenizer/schedule/checkpoint rule 동일
- max steps: 10,000
- selected checkpoint: both 10K rows required

Current gate:

```text
v5_random_mlm_10k: selected 10K checkpoint ready
v5_fvt_mlm_10k: running, model file pending
post-checkpoint evaluation: locked until wrapper-ready + preflight
```

Source:

```text
docs/exp/v5/3_evaluation/running_status.md
docs/exp/v5/2_training/mlm_progress_eta.md
```

Speaker guard:

```text
Live progress is not a model result; it only keeps the checkpoint gate honest.
```

---

## 11. Glot500 metrics

**Glot500에서 측정한 metric family를 모두 유지한다.**

local coverage and target10 coverage:

- PPPL / MLM proxy: 102/102 local, target10 10/10
- Tatoeba retrieval: 63/102 local, target10 0/10
- Bible retrieval and Roundtrip alignment: 74/102 local, target10 0/10
- Text classification: 1/102 local, target10 0/10
- NER/POS: 78/102 audit and 58/102 local, target10 0/10
- v5 random PPPL/Tatoeba/Bible/Taxi1500/NER/POS/Roundtrip rows: measured;
  FVT rows wait for matched checkpoints

Coverage principle:

```text
missing task coverage is reported, not silently dropped.
```

Source:

```text
docs/exp/v5/4_reporting/00_tables/table_13_metric_fidelity_matrix.md
```

---

## 12. Current measured rows

**현재는 baseline/reference rows와 v5-random PPPL/downstream rows가 측정됐고, FVT method claim은 checkpoint 대기다.**

Measured baseline/reference rows:

- target PPPL: XLM-R 61.980216; Glot500-base 15.102934
- v5-random PPPL: target 39.222875; head 18.726452; all 20.138927
- Tatoeba all Top-10: XLM-R 0.566067; Glot500-base 0.706649; v5-random 0.610353
- Bible all Top-10: XLM-R 0.381153; Glot500-base 0.509356; v5-random 0.328019
- Taxi1500 macro-F1: XLM-R 0.592876; Glot500-base 0.743338; v5-random 0.702956
- NER all F1: XLM-R 0.549858; Glot500-base 0.627108; v5-random 0.544628
- POS all F1: XLM-R 0.481336; Glot500-base 0.567542; v5-random 0.481102
- Roundtrip acc.: XLM-R 0.185300; Glot500-base 0.205189; v5-random 0.190300

Interpretation:

```text
v5-random is a diagnostic row, not a method win.
The decisive comparison is matched v5-random vs v5-FVT after the same 10K MLM budget.
```

---

## 13. Coverage and limitations

**Target10 downstream coverage는 현재 PPPL 중심이다.**

- PPPL target10 coverage: 10/10; retained downstream target10 coverage: 0/10
- NER target row is actual evaluated intersection, not target10-wide evidence
- Roundtrip은 74/102 available-language 기준 XLM-R/Glot500-base/v5-random 측정 완료,
  FVT row는 checkpoint 대기
- `dzo_Tibt` tokenizer regression remains visible

Conclusion boundary:

```text
target10 downstream improvement is not a supported claim yet.
```

---

## 14. Conclusion

**현재 확정 결론은 setup fidelity + zero-step novelty이다.**

Can say now:

- v5 reproduces the Glot500-style workflow on a controlled 102-language subset.
- tokenizer expansion and initialization audits are complete.
- FVT strongly improves zero-step target MLM proxy over random resize.
- all Glot500 metric families are retained with coverage/blocker accounting.

Cannot say yet:

- FVT improves after-MLM PPPL.
- FVT improves downstream performance.
- target10 downstream improves.

Final conclusion source:

```text
docs/exp/v5/4_reporting/final_claim_decision_tree.md
docs/exp/v5/4_reporting/post_checkpoint_outcome_matrix_ko.md
docs/exp/v5/4_reporting/post_result_patch_plan_ko.md
docs/exp/v5/4_reporting/final_claim_freeze_audit.md
```

---

## 15. Backup: execution path

**Checkpoint 이후 실행선**

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
sed -n '1,120p' docs/exp/v5/4_reporting/post_result_patch_plan_ko.md
```

Audit files:

```text
docs/exp/v5/4_reporting/final_handoff_runbook.md
docs/exp/v5/4_reporting/post_result_patch_plan_ko.md
docs/exp/v5/3_evaluation/post_checkpoint_execution_plan.md
docs/exp/v5/4_reporting/finalization_gate_status.md
docs/exp/v5/4_reporting/final_claim_freeze_audit.md
docs/exp/v5/4_reporting/reporting_package_audit.md
docs/exp/v5/4_reporting/artifact_reference_audit.md
```

Final rule:

```text
Only aggregation-promoted values become final report/PPT claims.
```
