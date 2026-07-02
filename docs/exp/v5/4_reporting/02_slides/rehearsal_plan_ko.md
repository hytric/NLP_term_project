# v5 발표 리허설 플랜

작성 상태: execution draft, 2026-06-28 기준.

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
rehearsal plan header.

이 문서는 `final_deck_ko.md`와 `presenter_script_ko.md`를 실제 발표 시간에 맞게
운영하기 위한 리허설용 계획이다. 현재 결론은 `final_claim_freeze_audit.md` 기준으로
`claim_freeze_waiting_for_results` 상태이므로, after-MLM/downstream improvement는
말하지 않는다.

## 발표 운영 원칙

- 핵심 메시지는 "controlled Glot500-style replay + vocabulary-row initialization
  novelty"이다.
- 발표를 시작하기 전 `../one_page_summary_ko.md`의 `발표 직전 60초 체크`를
  먼저 읽고, dashboard/runbook/decision tree 순서로 현재 gate를 확인한다.
- `full 511-language reproduction`처럼 들리는 표현은 피한다.
- zero-step FVT advantage는 강하게 말해도 된다.
- after-MLM PPPL, downstream improvement, target10 downstream improvement는
  matched v5 checkpoint와 aggregation row가 생긴 뒤에만 말한다.
- 숫자는 `00_tables/`, `09_aggregation/`, `final_claim_decision_tree.md`에서 온 것만
  사용한다.

## 12분 기본 발표안

| Slide | Time | Must say | Shorten if needed |
| --- | ---: | --- | --- |
| 1. Title | 0:20 | full Glot500이 아니라 controlled replay | 세부 target 수는 slide 3에서 말함 |
| 2. Motivation + Contributions | 0:45 | uneven coverage, 92+10 replay, FVT novelty, metric fidelity를 한 번에 소개 | Glot500 설명을 한 문장으로 압축 |
| 3. Boundary | 0:50 | scale은 줄였지만 pipeline logic은 유지 | 표를 모두 읽지 않음 |
| 4. Target10 | 0:55 | Glot500 내부, non-XLM-R, 30K+, diversity | 언어 이름 전체 낭독 생략 가능 |
| 5. Corpus | 0:40 | 102 language-script, 92,452,251 lines, 0 missing dirs | output size 생략 가능 |
| 6. Tokenizer | 1:05 | 118,685 appended tokens, 29/30 improved, `dzo_Tibt` caveat | audit 세부 수치 일부 생략 |
| 7. Novelty | 0:55 | novelty는 corpus가 아니라 row initialization | align은 exploratory라고만 말함 |
| 8. Init Audit | 0:55 | identity copy, `<mask>` remap, byte accounting, LM-head tying | fallback 세부는 Q&A로 이동 |
| 9. Zero-Step | 1:05 | FVT zero-step gain은 intrinsic evidence이며 method claim은 아직 locked | 모든 delta를 다 읽지 않음 |
| 10. Training | 0:45 | matched 10K checkpoint 전까지 method claim locked | live step 수치는 말하지 않음 |
| 11. Metrics | 0:55 | Glot500 metric family 모두 유지 | coverage table 전체 설명 생략 |
| 12. Current Rows | 1:00 | baseline/reference와 v5-random diagnostic rows measured, v5-FVT pending | 모든 숫자를 읽지 않고 대표 2-3개만 |
| 13. Limitations | 0:55 | target10 downstream 0/10, Bible/Roundtrip v5 checkpoint gaps | 한계가 fidelity의 일부라고 강조 |
| 14. Conclusion | 0:45 | setup fidelity + zero-step novelty + pending final claims | conclusion을 과장하지 않음 |
| 15. Backup | 0:30 | all artifacts and commands are traceable | 시간이 부족하면 skip |

Target total: about 12 minutes.

## 8분 압축 발표안

반드시 남길 slide:

```text
1 -> 3 -> 4 -> 6 -> 8 -> 9 -> 11 -> 12 -> 13 -> 14
```

압축 원칙:

- Slide 2 motivation은 slide 1 opening에 흡수한다.
- Slide 5 corpus는 slide 4 끝에서 "merge 92M lines, 0 missing"으로만 말한다.
- Slide 7 novelty는 slide 8 앞 문장으로 흡수한다.
- Slide 10 training은 slide 12/14의 pending gate 설명으로 흡수한다.
- Slide 15 backup은 Q&A 때만 연다.

8분 버전의 결론 문장:

```text
현재까지는 Glot500-style pipeline을 102-language subset에서 재연했고,
FVT initialization이 zero-step target MLM proxy에서 random보다 확실히 좋은
시작점을 만든다는 결론까지 안전하게 말할 수 있습니다. after-MLM과 downstream은
matched checkpoint 이후 같은 wrapper로 평가한 뒤에만 claim으로 올립니다.
```

## 5분 긴급 발표안

시간이 5분으로 줄면 결과 숫자를 많이 읽지 말고, 실험의 방어 가능한 구조만
명확히 전달한다.

반드시 남길 slide:

```text
1 -> 3 -> 6 -> 8 -> 9 -> 11 -> 14
```

운영 방식:

- Slide 1에서 "full Glot500이 아니라 92+10 controlled replay"를 먼저 잠근다.
- Slide 3에서 scope limitation을 20초 안에 말한다.
- Slide 6에서 tokenizer는 `118,685` appended tokens와 `dzo_Tibt` caveat만 말한다.
- Slide 8에서 `<mask>` remap, identity copy, LM-head tying을 correctness evidence로 묶는다.
- Slide 9에서 zero-step FVT advantage를 novelty의 핵심 결과로 말한다.
- Slide 11에서 모든 Glot500 metric family를 유지했다는 protocol fidelity만 말한다.
- Slide 14에서 after-MLM/downstream claim이 아직 gate 뒤에 있으면 잠긴 상태로 끝낸다.

5분 버전의 결론 문장:

```text
이 실험의 현재 확정 결론은 Glot500-style pipeline을 92+10 controlled subset에서
재연했고, vocabulary extension 이후 FVT initialization이 random resize보다
zero-step target MLM proxy에서 훨씬 좋은 시작점을 만든다는 것입니다. 최종
after-MLM/downstream claim은 matched checkpoint와 aggregation row가 닫힌 뒤에만
업데이트합니다.
```

## 15분 확장 발표안

추가로 설명할 부분:

- Slide 4에서 target10의 지역/문자 다양성을 더 자세히 설명한다.
- Slide 6에서 `dzo_Tibt` regression을 failure analysis로 30초 더 설명한다.
- Slide 8에서 `<mask>` id drift와 identity-copy 필요성을 설명한다.
- Slide 9에서 zero-step NLL과 after-MLM gate의 차이를 더 분명히 설명한다.
- Slide 11에서 metric fidelity matrix를 한 줄씩 보여준다.
- Slide 13에서 Bible/Roundtrip의 v5 checkpoint-pending 상태를 "누락이 아니라 명시적 gate"로 방어한다.

15분 버전에서는 Q&A를 미리 줄이는 대신, limitations를 더 정직하게 말하는 것이 좋다.

## 말하면 좋은 전환 문장

| From | To | Transition |
| --- | --- | --- |
| motivation | boundary | "그래서 먼저 어느 범위를 재연했는지부터 잠그겠습니다." |
| target10 | corpus | "이 target set을 포함해 실제 학습 corpus를 고정했습니다." |
| tokenizer | novelty | "여기까지가 Glot500-style 재연이고, 이제 novelty 질문으로 넘어갑니다." |
| zero-step | training | "하지만 zero-step만으로 final method claim을 할 수는 없습니다." |
| metrics | results | "metric family는 유지했고, 현재 측정된 row는 다음과 같습니다." |
| results | limitations | "이 결과를 어디까지 말할 수 있는지는 coverage가 결정합니다." |
| limitations | conclusion | "따라서 현재 결론은 보수적으로 잠그는 것이 맞습니다." |

## Checkpoint 상태별 마지막 20초

발표 당일 `bash scripts/run_v5_post_checkpoint_evals.sh status` 결과에 따라
마지막 20초를 아래 중 하나로 고른다.

| Status | 마지막 문장 |
| --- | --- |
| `READY_TO_LAUNCH=no` | "현재는 checkpoint pair가 완전히 닫히기 전이므로 final method claim은 잠그고, setup fidelity와 zero-step novelty까지만 확정합니다." |
| `READY_TO_LAUNCH=yes`, evaluation not run | "두 checkpoint가 준비되었으므로 이제 같은 wrapper로 PPPL과 downstream replay를 실행할 수 있습니다. claim은 aggregation 이후에만 바꿉니다." |
| evaluation run, decision tree still waiting | "metric output은 생겼지만 final evidence packet이 아직 닫히지 않았으므로 measured-but-not-promotable 상태로 둡니다." |
| final decision tree selects outcome | "`post_checkpoint_outcome_matrix_ko.md`가 고른 outcome만 slide 14 결론으로 사용합니다. target10 downstream coverage caveat는 계속 유지합니다." |

## Q&A에서 바로 쓰는 답변

**Q. 왜 full Glot500 reproduction이 아니라고 계속 강조하나?**

```text
scale이 다르기 때문입니다. v5는 511-language full reproduction이 아니라,
92 seen + 10 target의 controlled subset에서 Glot500-style pipeline logic을
재연한 실험입니다. 이 경계를 분명히 해야 결과 claim이 정확해집니다.
```

**Q. target10 downstream 결과를 왜 주장하지 않나?**

```text
target10은 raw-text PPPL에는 10/10으로 들어가지만, 현재 materialized downstream
task coverage는 target10 0/10입니다. 그래서 target10 claim은 tokenization,
zero-step, after-MLM PPPL 중심으로 제한하고, downstream은 available-language
replay로 보고합니다.
```

**Q. FVT가 downstream에서도 좋다고 기대해도 되나?**

```text
기대는 할 수 있지만 claim은 아직 하지 않습니다. 현재 증거는 zero-step intrinsic
evidence입니다. after-MLM PPPL과 downstream rows는 matched `v5_random`/`v5_fvt`
checkpoint 이후 같은 wrapper로 평가해야 합니다.
```

**Q. `dzo_Tibt` regression은 실험 실패 아닌가?**

```text
전체 tokenizer audit은 29/30 개선이지만 `dzo_Tibt`는 분명한 failure case입니다.
이걸 숨기지 않는 것이 오히려 중요합니다. 새 SPM piece append가 항상 좋은
segmentation을 보장하지 않고, script-specific score calibration 문제가 생길 수
있다는 분석 포인트이기 때문입니다.
```

## 리허설 체크리스트

- 첫 리허설 전 `../one_page_summary_ko.md`의 60초 체크를 읽고 현재 allowed frame을
  한 문장으로 말한다.
- 12분 버전에서 slide 11 숫자를 모두 읽지 않는다.
- Slide 14에서 "final improvement"라는 표현을 쓰지 않는다.
- `Glot500-base`는 external reference라고 말한다.
- `v5_random`/`v5_fvt`가 아직 pending이면 "selected checkpoint 없음"만 말한다.
- Q&A에서 metric coverage를 물으면 `table_13_metric_fidelity_matrix.md`를 연다.
- 실험 재현 명령을 물으면 `final_submission_handoff_ko.md`와
  `final_handoff_runbook.md`를 연다.
