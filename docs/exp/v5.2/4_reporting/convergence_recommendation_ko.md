# v5.2 Convergence Recommendation

작성일: 2026-06-30

## 결론

- 이전 `4000` step 결과는 제대로 수렴한 checkpoint로 보지 않는다.
- `4000` step table은 early diagnostic으로만 사용하고, final performance claim에는 쓰지 않는다.
- main 5-way 비교는 최소 `8000` step까지 학습한 뒤, `5000/6000/7000/8000` trajectory를 함께 본다.
- `8000`에서도 training loss와 PPPL이 계속 의미 있게 내려가면 `10000-12000` step extension을 추가한다.

## 근거

- FVT PPPL은 `3500 -> 4000`에서 `58.939731 -> 58.025602`로 `1.55%`만 추가 개선됐다.
- FVT Tatoeba top10은 `2500`에서 peak `0.290893`이고, `3000-4000`은 `0.280-0.283` band에서 흔들린다.
- 하지만 retrieval plateau처럼 보여도, training loss가 계속 내려가면 수렴으로 판정할 수 없다.
- stage-2 converge run은 `4000` 이후 약 `1000` local step까지 진행됐지만, SIGTERM으로 checkpoint 저장 전 중단됐다. 로그상 loss가 계속 내려갔으므로 `4000`은 아직 학습 중인 상태로 해석한다.
- 따라서 `4000` step 결과는 initialization effect의 초기 방향성을 보여주는 자료이지, 최종 성능 비교의 근거는 아니다.

## 권장 실행

- main 5-way run: `MAX_STEPS=8000`, `SAVE_STEPS=1000`
- convergence check: `5000/6000/7000/8000` checkpoint에서 train loss, PPPL, retrieval, downstream을 함께 비교
- extension 조건: `8000`에서도 PPPL 또는 train loss가 계속 크게 개선되면 `MAX_STEPS=12000`까지 연장
- 시간이 부족한 경우: `4000` 또는 `5000` table은 diagnostic으로만 보고, final claim은 보류
- loss graph: `docs/exp/v5.2/2_training/convergence_5way_loss_curve.png`

## 발표 문장

```text
이전 4000-step 결과는 수렴 checkpoint가 아니라 early diagnostic으로 해석한다.
FVT 계열이 초반부터 유리한 신호를 보였지만, final performance claim은 최소
8000-step 이후의 loss/PPPL/downstream trajectory를 확인한 뒤에 제시한다.
```
