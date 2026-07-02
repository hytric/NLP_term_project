# 06. Repair Probes

Sources:

- added-token weighted objective: `docs/exp/second_try/18_v2_added_token_repair`
- new-row-only repair: `docs/exp/second_try/19_v2_new_row_only_repair`
- staged/lower-rate repair: `docs/exp/second_try/20_v2_staged_added_token_repair`
- alternative init mean/align: `docs/exp/second_try/21_v2_alt_init_mlm_probe`

Goal: Step17에서 확인된 added-token bottleneck을 줄이기 위해 objective, trainable parameter scope, learning-rate schedule, initialization method를 바꿔 보았다.

Main finding: passing variant는 없었다. Added-token loss를 줄이는 시도는 all-token loss를 악화했고, base를 보존하는 시도는 added-token 개선에 실패했다. Alternative initialization도 `fvt`보다 못했다.

## Probe Summary

| Probe | Core idea | Main evidence | Result |
| --- | --- | --- | --- |
| Step18 added-token weighted objective | added-token target loss에 더 큰 weight를 줌 | added loss `-0.508373`, all loss `+0.122137` | FAIL |
| Step19 new-row-only repair | 새 embedding / LM-head row만 train | base loss `-0.048017`, added loss `+0.240600` | FAIL |
| Step20 staged/lower-rate repair | new-row 중심 + 낮은 LR/staged schedule | passing variants `0/3`, best all loss `-0.016669` | FAIL |
| Step21 alternative init | `mean`, `align` initialization 재시도 | best `align` loss `5.086652`, fvt `4.946829` | FAIL |

## Step18: Added-Token Weighted Objective

| Metric | Value |
| --- | ---: |
| Completed seeds | 3/3 |
| Added-token improved seeds | 3/3 |
| All-token nonworse seeds | 0/3 |
| Repaired seeds | 0/3 |
| Mean added loss delta vs Step17 | -0.508373 |
| Mean all loss delta vs Step17 | +0.122137 |

Interpretation: added-token prediction은 실제로 개선되었다. 하지만 all-token loss가 악화되어 전체 objective 기준으로는 실패다. Added-token pressure만 키우면 base/overall distribution과 충돌할 수 있다.

## Step19: New-Row-Only Repair

| Metric | Value |
| --- | ---: |
| Completed seeds | 3/3 |
| Trainable audit pass seeds | 3/3 |
| Added-token improved seeds | 0/3 |
| Base-token nonworse seeds | 3/3 |
| All-token nonworse seeds | 0/3 |
| Mean added loss delta vs source | +0.240600 |
| Mean base loss delta vs source | -0.048017 |
| Mean all loss delta vs source | +0.097944 |

Interpretation: base behavior 보존에는 성공했다. 그러나 새 row만 움직이는 방식으로는 added-token prediction을 개선하지 못했다. Added-token bottleneck은 row vector만의 문제가 아니라 context representation, LM-head 경쟁, objective 설계와 연결되어 있다.

## Step20: Staged / Lower-Rate Repair

| Metric | Value |
| --- | ---: |
| Configured variants | 3 |
| Completed variant/seed runs | 9/9 |
| Passing variants | 0/3 |
| Trainable audit failures | 0 |
| Selected variant | `new_row_added_lr1e-5` |
| Selected mean added delta | -0.004565 |
| Selected mean base delta | -0.029149 |
| Selected mean all delta | -0.016669 |

Interpretation: 낮은 learning rate와 staged update는 손상을 줄였지만, added-token 개선 폭이 너무 작았다. 실패 원인을 “LR이 너무 세서 망가진 것”만으로 설명하기 어렵다.

## Step21: Alternative Init Mean / Align

| Method | Mean final raw loss | Delta vs fvt | Ratio vs original control |
| --- | ---: | ---: | ---: |
| `fvt` | 4.946829 | baseline | 1.964580 |
| `align` | 5.086652 | +0.139823 | 2.020110 |
| `mean` | worse than `align` | n/a | n/a |
| original control | 2.518008 | n/a | baseline |

Interpretation: Step14의 zero-step ordering과 마찬가지로 `fvt`가 가장 낫다. Alternative init만으로는 Step15 gap을 닫지 못한다.

## Takeaway

Repair probes는 added-token problem이 실제 병목이라는 점을 다시 확인했다. 다만 단일 처방으로는 충분하지 않았다. 앞으로는 added-token supervision을 강화하면서 base-token behavior를 명시적으로 보존하는 결합 objective가 필요하다.
