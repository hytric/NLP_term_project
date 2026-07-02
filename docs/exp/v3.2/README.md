# V3.2 Experiment Plan

작성일: 2026-06-19

## Purpose

`v3.2`는 `v3.1/05_additional`에서 확인된 language 성능 병목을 해결하기 위한 follow-up 실험 계획이다.

핵심 문제는 다음이다.

> append-only tokenizer 구조는 통과했지만, target10 low-resource language의 content-token MLM과 sentence-level semantic retrieval은 아직 확보되지 않았다.

`v3.2`의 목표는 tokenizer를 다시 크게 바꾸는 것이 아니라, `v3.1`의 weak result를 다음 세 가지로 분해해 해결하는 것이다.

기본 방향은 다음이다.

> high-resource language source를 최대한 많이 활용해서 low-resource target10의 Pseudoperplexity / MLM Intrinsic Evaluation 성능을 먼저 올린다. 이 지표가 현재 학습 proxy task이므로, v3.2의 1차 성공 기준은 sentence retrieval이나 translation이 아니라 low-resource content-token MLM 개선이다.

이를 위해 v3.2는 다음 네 가지를 실행한다.

1. high-resource source를 transfer/replay/teacher signal로 적극 활용한다.
2. `chr/cop/oji/syr` script/content-token 예측 실패를 직접 줄인다.
3. target10 language-balanced sampling을 적용해 high-resource source를 많이 쓰되 target script가 묻히지 않게 한다.
4. MLM만으로는 부족한 sentence retrieval은 후속 contrastive/TLM-style alignment stage로 보완한다.

## Main Evidence From V3.1

| Finding | Evidence | V3.2 Consequence |
| --- | --- | --- |
| Whole-token pseudoPPL is misleading. | all-token top-1 is about `43%`, but content-token top-1 is about `4%`. | content-token metrics become primary MLM diagnostics. |
| `chr/cop/oji` are near-zero content-token languages. | structured init average content-token top-10 is `0%` for `chr/cop/oji`. | tokenizer and MLM sampling must explicitly target these scripts. |
| `syr/cop` are retrieval bottlenecks. | centered-CSLS R@1 is lowest when `syr` or `cop` is source/target. | alignment stage must report source/target language macro breakdown. |
| `fvt` wins MLM loss but not retrieval. | `fvt` final dev loss is best, but retrieval selects other variants. | MLM and semantic alignment must be separate gates. |
| Training budget is too small. | `200 * 32 = 6,400` chunks, about `1/28,800` of Glot500 consumed chunks. | run longer target-balanced MLM before making language claims. |
| High-resource source is underused as a transfer engine. | v3.1 high-resource replay mainly protects compatibility and retention. | v3.2 should actively use high-resource source to improve low-resource MLM proxy performance. |
| MLM has no semantic objective. | no contrastive, TLM, NSP, or sentence-pair loss. | add a semantic alignment stage after MLM. |

## Folder Map

| Folder | Role |
| --- | --- |
| `00_problem_diagnosis` | freeze v3.1 failure analysis and v3.2 success gates |
| `01_tokenizer_repair` | audit and repair content-token coverage for weak scripts |
| `02_balanced_mlm` | high-resource-source-augmented MLM adaptation |
| `03_semantic_alignment` | contrastive/TLM-style sentence alignment stage |
| `04_downstream_translation` | downstream, retrieval, POS, and translation diagnostics |
| `05_report_package` | final claim map and report-ready tables |

## Claim Policy

Allowed after `v3.2` only if gates pass:

> high-resource-source-augmented MLM improves low-resource target10 content-token prediction, and optional explicit semantic alignment improves target10 sentence retrieval over `v3.1` checkpoints.

Not allowed unless downstream and translation gates also pass:

> the model solves low-resource translation or robust multilingual semantic transfer.
