# v5 Post-Checkpoint Outcome Matrix Korean

작성 상태: execution draft, 2026-06-28 refresh 기준.

이 문서는 matched `v5_random`/`v5_fvt` checkpoint 이후 결과가 들어왔을 때,
최종 report와 PPT 결론을 어떤 문장으로 잠그는지 정하는 한국어 decision matrix이다.
숫자 자체는 이 문서에 직접 쓰지 않고, `3_evaluation/09_aggregation/`과
`00_tables/`에서 승격된 값만 사용한다.

## 0. 현재 Gate 해석

마지막 refresh 기준으로 `v5_random` post-10K row는 PPPL, Tatoeba, Bible,
Taxi1500, NER, POS, Roundtrip에 측정되어 있지만, `v5_fvt` row는 아직 matched
checkpoint가 없어 모두 `waiting_model`이다. 따라서 현재 `v5_random` row는
pipeline sanity check와 diagnostic evidence로만 사용하고, method win/loss
판정에는 사용하지 않는다.

현재 허용되는 결론:

```text
setup fidelity, Glot500-style metric-family replay protocol, zero-step FVT
initialization advantage
```

현재 잠긴 결론:

```text
FVT after-MLM PPPL improvement
FVT downstream improvement
target10 downstream improvement
full 511-language Glot500 reproduction
```

전환 조건은 `bash scripts/run_v5_post_checkpoint_evals.sh status`의
`READY_TO_LAUNCH=yes`이다. `READY_TO_LAUNCH=no`이면 이 문서의 outcome matrix를
결론 선택용으로 쓰지 말고, report/PPT는 execution draft wording을 유지한다.

## 1. 입력 순서

결론을 고르기 전에 아래 파일을 순서대로 확인한다.

```text
docs/exp/v5/3_evaluation/09_aggregation/main_head_tail_all.tsv
docs/exp/v5/3_evaluation/09_aggregation/v5_target_subset.tsv
docs/exp/v5/4_reporting/method_comparison_summary.md
docs/exp/v5/4_reporting/final_claim_decision_tree.md
docs/exp/v5/4_reporting/result_promotion_readiness_audit.md
docs/exp/v5/4_reporting/final_claim_freeze_audit.md
docs/exp/v5/4_reporting/00_tables/table_13_metric_fidelity_matrix.md
```

우선순위:

1. matched checkpoint pair가 존재하는가?
2. after-MLM PPPL에서 `v5_fvt`와 `v5_random`을 같은 scope로 비교할 수 있는가?
3. available downstream rows가 metric family별로 parsed 되었는가?
4. target10 downstream coverage가 여전히 `0/10`인지, 새 coverage가 생겼는가?
5. final claim decision tree가 `waiting`이 아닌 outcome을 선택했는가?

## 2. 판정 방향과 Tie Rule

결론 선택은 같은 metric, 같은 group, 같은 aggregation artifact 안에서만 비교한다.
`v5_fvt`와 `v5_random` 중 한쪽 row만 있으면 비교하지 않고 `incomplete evaluation`으로 둔다.
PPPL은 intrinsic evidence이고 downstream은 transfer evidence이므로, 두 층을 섞어
하나의 평균 점수로 만들지 않는다.

| Metric family | Primary comparison | Better direction | Tie / negligible wording |
| --- | --- | --- | --- |
| PPPL / MLM proxy | weighted PPPL, target/head/all | lower is better | 차이가 매우 작거나 parser/sample 조건이 다르면 `no clear after-MLM separation`으로 쓴다 |
| Tatoeba retrieval | Top-10 accuracy, available-language/head/all | higher is better | task별 mixed evidence로 유지 |
| Bible retrieval | Top-10 accuracy, available-language/head/all | higher is better | target10 claim으로 승격하지 않는다 |
| Taxi1500 text classification | macro-F1 | higher is better | local English-only 범위를 같이 적는다 |
| NER | F1 | higher is better | `fur_Latn` 단일 target row는 target10-wide evidence가 아니다 |
| POS | F1 | higher is better | `TRAIN_LANGS=tur_Latn` 조건을 유지한다 |
| Roundtrip alignment | accuracy | higher is better | retained metric-family evidence로 보고, coverage caveat를 유지한다 |

### Available Downstream Majority Rule

downstream 다수 판정은 PPPL을 제외하고 아래 6개 metric family 중
`v5_random`과 `v5_fvt`가 같은 scope에서 모두 parsed 된 family만 대상으로 한다.

```text
Tatoeba retrieval
Bible retrieval
Taxi1500 text classification
NER
POS
Roundtrip alignment
```

판정 규칙:

1. 같은 family 안에서 우선 `all available` group을 비교하고, 없으면 `head` group을
   사용한다. `target10` group은 coverage가 생겼을 때만 별도 보조 증거로 둔다.
2. FVT 우세 family 수가 measured downstream family의 절반을 초과하면
   `available downstream row 다수도 FVT 우세`로 쓴다.
3. measured downstream family가 2개 이하이면 downstream majority claim을 하지 않고
   `downstream evidence too sparse`로 쓴다.
4. 동률이거나 family별 방향이 갈리면 `downstream mixed`로 쓴다.
5. 한 family에서 한쪽 모델 row만 있거나 parser/coverage 조건이 다르면 그 family는
   majority count에서 제외하고 `incomplete` note로 남긴다.

Outcome 선택 규칙:

1. PPPL target/head/all 중 primary target 또는 all에서 FVT가 우세하고,
   downstream available metric family 다수가 FVT 우세이면 `bounded positive`.
2. PPPL에서는 FVT가 우세하지만 downstream metric family가 서로 갈리면
   `intrinsic positive, downstream mixed`.
3. zero-step만 FVT 우세이고 after-MLM PPPL에서 우세가 사라지면
   `early-only diagnostic`.
4. PPPL과 downstream 모두 random이 같거나 우세하면 `negative final comparison`.
5. row, parser, coverage, checkpoint 중 하나라도 비교 조건을 깨면
   `incomplete evaluation`.

## 3. 결론 Matrix

| Outcome | Evidence condition | Report 결론 | PPT 결론 | 허용 claim |
| --- | --- | --- | --- | --- |
| bounded positive | FVT가 after-MLM PPPL에서 random보다 좋고, available downstream row 다수도 FVT 우세 | FVT initialization은 intrinsic adaptation과 available-task transfer 모두에서 제한적 positive evidence를 보였다 | slide 14에서 bounded positive claim 사용 | target10 downstream coverage caveat를 단 채 method benefit 주장 가능 |
| intrinsic positive, downstream mixed | FVT가 PPPL에서는 우세하지만 downstream은 task별로 섞임 | FVT는 intrinsic adaptation에는 유리하지만 downstream transfer는 task/coverage-dependent | slide 12는 positive, slide 14는 bounded/mixed | PPPL 기반 method claim 가능, downstream 일반화 금지 |
| early-only diagnostic | zero-step은 FVT 우세지만 after-MLM PPPL에서 random이 따라잡거나 역전 | FVT는 early adaptation을 바꾸지만 10K MLM 이후 superiority는 확인되지 않음 | slide 14를 diagnostic conclusion으로 교체 | novelty는 initialization diagnostic으로 제한 |
| negative final comparison | PPPL과 downstream 모두 random이 같거나 우세 | decomposition initialization만으로 final gain을 보장하지 못했다 | slide 14를 negative-but-informative conclusion으로 교체 | controlled negative result claim 가능 |
| incomplete evaluation | 한쪽 model row, PPPL, downstream parser 중 하나라도 빠짐 | current execution draft 유지, pending result를 숨기지 않음 | slide 11-14는 waiting/pending 유지 | final method/downstream claim 금지 |

### 한국어 결론 문장 후보

### Bounded Positive

```text
matched continued MLM 이후 FVT는 PPPL에서 random resize보다 유리했고,
available-language downstream row 다수에서도 같은 방향의 evidence를 보였다.
따라서 본 실험의 최종 결론은 target10 downstream coverage 한계를 명시한
bounded positive claim이다.
```

### Intrinsic Positive, Downstream Mixed

```text
FVT는 after-MLM PPPL에서 random resize보다 유리했지만 downstream 결과는 task와
coverage에 따라 섞였다. 따라서 최종 claim은 intrinsic adaptation 개선으로
제한하고, downstream transfer는 coverage-dependent하게 해석한다.
```

### Early-Only Diagnostic

```text
FVT는 zero-step target MLM proxy에서 뚜렷하게 좋은 시작점을 제공했지만, matched
continued MLM 이후 그 차이가 유지되지는 않았다. 이 결과는 새 vocabulary row
initialization이 early adaptation을 바꾼다는 diagnostic evidence로 해석한다.
```

### Negative Final Comparison

```text
controlled tokenizer, corpus, budget 조건에서 FVT가 random resize를 최종적으로
넘어서지 못했다. 이는 source-token decomposition initialization이 항상 final
gain으로 이어지는 것은 아니며, 추가적인 training objective나 row update 전략이
필요할 수 있음을 보여준다.
```

### Incomplete Evaluation

```text
현재는 matched v5 checkpoint 또는 post-checkpoint metric row가 아직 완결되지
않았으므로, 최종 method/downstream claim은 잠근다. 보고서와 발표는 setup fidelity,
zero-step novelty, metric-family replay 준비 상태까지만 확정 결론으로 둔다.
```

## 4. Slide별 교체 규칙

| Slide | 교체 조건 | 교체 내용 |
| --- | --- | --- |
| 9 | selected checkpoint manifest가 두 모델 모두 ready | running/queued 문장을 checkpoint path와 global step으로 교체 |
| 11 | aggregation에 v5_random/v5_fvt metric rows parsed | waiting checkpoint column을 measured row와 delta로 교체 |
| 12 | after-MLM PPPL outcome 확정 | zero-step-only novelty에서 after-MLM intrinsic claim 여부로 교체 |
| 13 | downstream coverage 또는 blocker 상태 변화 | target10/downstream caveat와 Roundtrip/Bible 상태 갱신 |
| 14 | final decision tree가 non-waiting outcome 선택 | 위 결론 문장 중 하나로 최종 결론 교체 |

## 5. 발표 방어 원칙

- PPPL이 좋고 downstream이 섞이면 실패가 아니라 evidence layer 분리로 설명한다.
- target10 downstream coverage가 없으면 개선도 악화도 주장하지 않는다.
- `Glot500-base`는 equal-budget baseline이 아니라 external reference로만 말한다.
- Bible과 Roundtrip은 빠뜨린 metric이 아니라 retained metric family로 설명한다.
- live log, ETA, single-model output은 최종 claim source가 아니다.

## 6. 최종 Freeze 전 확인

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
python3 scripts/audit_v5_reporting_package.py
python3 scripts/write_v5_final_deliverable_audit.py
python3 scripts/build_v5_release_bundle.py
python3 scripts/audit_v5_release_bundle.py
```

위 명령 이후에도 `final_claim_decision_tree.md`가 `waiting`이면, report/PPT는
`execution draft`로 유지한다.

## 7. 최종 Evidence Packet

결론 문장을 바꾸기 전에 아래 packet이 모두 한 refresh 시점에서 서로 맞아야 한다.
하나라도 빠지면 outcome은 `incomplete evaluation`으로 둔다.

| Packet item | Required evidence | Fail-closed rule |
| --- | --- | --- |
| checkpoint pair | `model_matrix.tsv`, `selected_checkpoint_manifest.md`, `post_checkpoint_preflight.md` | 두 모델 모두 `ready_for_wrapper=yes`가 아니면 평가/결론을 열지 않는다 |
| metric rows | `metric_completion.tsv`, `main_head_tail_all.tsv`, `v5_target_subset.tsv` | 한쪽 model row만 있으면 paired comparison에서 제외한다 |
| provenance | `post_checkpoint_provenance_audit.md`, metric별 command log | source file, metadata, command log가 없으면 report/PPT 숫자로 쓰지 않는다 |
| materiality | `method_comparison_summary.md`, `comparison_materiality_audit.md` | `tie_band`는 win이 아니라 `no clear separation`으로 쓴다 |
| claim gate | `claim_promotion_matrix.md`, `final_claim_decision_tree.md` | decision tree가 `pending`이면 현재 execution-draft 결론을 유지한다 |
| report/PPT patch | `post_result_patch_plan_ko.md`, `result_interpretation_blocks.md` | `ready_for_patch` row만 고치고 나머지 pending row는 남긴다 |
| final freeze | `final_claim_freeze_audit.md`, `reporting_package_audit.md`, `final_submission_smoke_audit.md`, `release_bundle_audit.md` | 하나라도 `needs_*`면 final이 아니라 execution draft로 공유한다 |

이 packet은 숫자보다 우선한다. 좋은 숫자가 보여도 packet이 닫히지 않았으면
보고서와 발표에서는 “measured but not promotable”로 남긴다.
