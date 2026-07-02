# Task 5. POS Tagging

작성일: 2026-06-19

## Task 정의

POS tagging은 token-level syntactic labeling을 평가한다. Glot500에서는 English POS로 fine-tuning한 뒤 target-language UD-style POS data에 zero-shot으로 평가한다.

## 데이터/설정

현재 사용할 수 있는 local result는 Coptic UD POS supervised pilot이다. 이 결과는 `05_additional` 아래로 재집계했다.

중요한 caveat:

> 이 결과는 Glot500-style English-to-target zero-shot POS가 아니다. Local UD Coptic data를 사용한 Coptic supervised POS pilot이다.

설정:

- data: local UD Coptic-Scriptorium train/dev/test
- baseline: `xlm-roberta-base`
- candidate group: replay-safe third_try `fvt` checkpoints, seeds `13`, `17`, `23`
- downstream seed: `13`
- requested max steps: `200`

## 결과

| Metric | Baseline | Candidate mean | Delta / status |
| --- | ---: | ---: | --- |
| test token accuracy | `0.253182` | `0.259963` | `+0.006781` |
| positive checkpoint seeds | `NA` | `3/3` | all replay-safe seeds improve token accuracy |
| test macro F1 | `0.163298` | `0.160642` | `-0.002656` |

Seed-level token accuracy:

| Model | Test token accuracy | Delta vs XLM-R | Test macro F1 | Delta macro F1 |
| --- | ---: | ---: | ---: | ---: |
| `xlmr_base` | `0.253182` | `0.000000` | `0.163298` | `0.000000` |
| `fvt_replay_safe_seed13` | `0.261473` | `+0.008291` | `0.158773` | `-0.004525` |
| `fvt_replay_safe_seed17` | `0.260413` | `+0.007231` | `0.161195` | `-0.002103` |
| `fvt_replay_safe_seed23` | `0.258002` | `+0.004820` | `0.161958` | `-0.001340` |

## 해석

Replay-safe candidates는 세 checkpoint seed 모두에서 XLM-R-base보다 Coptic POS token accuracy가 약간 높다. 하지만 macro F1은 약간 낮다. 따라서 이 결과는 weak POS pilot이지 broad POS transfer evidence가 아니다.

## 주장 가능 범위

가능:

> Coptic UD POS pilot에서 replay-safe candidates가 token accuracy를 약하게 개선했다.

불가능:

> v3.1이 Glot500-style zero-shot POS transfer 또는 target10-wide POS evaluation을 통과했다고 주장할 수 없다.

## 산출물

| Artifact | 용도 |
| --- | --- |
| `../coptic_pos_results_replay_safe.tsv` | per-run POS result |
| `../coptic_pos_summary_replay_safe.tsv` | POS summary |
| `../coptic_pos_label_metrics_replay_safe.tsv` | per-label POS metrics |
