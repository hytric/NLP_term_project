# v5.2 Convergence Audit

작성일: 2026-06-29 09:45 KST

## 판정

`완벽하게 수렴했다`고 말하기는 어렵다. 이 run은 4000 optimizer step에서
linear scheduler가 거의 0 learning rate까지 내려가며 종료된 short diagnostic run이다.
따라서 `planned run completed`와 `last checkpoints mostly plateaued`는 맞지만,
엄밀한 full convergence claim은 보류한다.

발표용으로는 다음 표현이 안전하다.

```text
The 8-checkpoint diagnostic run completed and the final interval shows
near-plateau behavior. We do not claim full convergence; we use the run to
compare initialization methods under the same short continued-pretraining budget.
```

## 근거

학습은 네 method 모두 `checkpoint-4000`까지 완료됐고, score table에 pending 값은 없다.
최종 live status 기준 active v5.2 train/eval process도 없다.

마지막 구간 `3500 -> 4000`에서 PPPL 개선폭은 작아졌다.

| Method | PPPL 3000 | PPPL 3500 | PPPL 4000 | 3500->4000 delta | Delta % |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 133.106839 | 121.631484 | 119.581715 | -2.049769 | -1.69% |
| mean | 138.513402 | 131.012510 | 128.258830 | -2.753680 | -2.10% |
| fvt | 61.603757 | 58.939731 | 58.025602 | -0.914129 | -1.55% |
| align | 61.603757 | 58.939731 | 58.025602 | -0.914129 | -1.55% |

Tatoeba retrieval은 마지막 구간에서 개선이라기보다 작은 진동 범위다.

| Method | Tatoeba 3000 | Tatoeba 3500 | Tatoeba 4000 | 3500->4000 delta |
| --- | ---: | ---: | ---: | ---: |
| random | 0.249892 | 0.247225 | 0.248908 | +0.001683 |
| mean | 0.246495 | 0.247829 | 0.246194 | -0.001635 |
| fvt | 0.282306 | 0.280321 | 0.282957 | +0.002636 |
| align | 0.282306 | 0.280321 | 0.282957 | +0.002636 |

학습 로그의 마지막 logged learning rate는 거의 0이다.

| Method | Last logged loss | Last logged LR | Final epoch |
| --- | ---: | ---: | ---: |
| random | 4.1249 | 7.5e-08 | 0.75 |
| mean | 4.1587 | 7.5e-08 | 0.75 |
| fvt | 3.2943 | 6.25e-08 | 0.75 |
| align | 3.2943 | 6.25e-08 | 0.75 |

## 해석

- `fvt`는 8개 checkpoint 전체에서 independent method 중 PPPL 최저, Tatoeba 최고다.
- `align`은 이번 artifact에서 `fvt`와 byte-identical collapse가 확인됐으므로 독립 수렴
  evidence로 해석하지 않는다.
- 마지막 PPPL은 아직 조금 내려가고 있으므로, 더 긴 학습을 주면 추가 개선 가능성은 있다.
- 하지만 Tatoeba는 이미 작은 진동 범위이고, learning rate가 0에 가까워졌기 때문에 이
  4000-step budget 안에서는 안정화됐다고 볼 수 있다.

