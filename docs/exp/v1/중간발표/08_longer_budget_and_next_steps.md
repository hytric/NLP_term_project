# 08. Longer Budget Probe And Next Steps

Sources:

- longer budget probe: `docs/exp/second_try/25_v2_8k_continued_budget_probe`
- roadmap: `docs/exp/second_try/28_appended_token_solution_roadmap`

Goal: smaller vocab인 8k에서 train-token budget을 늘리면 original control과의 gap이 닫히는지 확인했다. 이후 결과를 바탕으로 다음 실험 방향을 정했다.

Main finding: 8k를 총 약 1M train tokens까지 늘려도 gap은 닫히지 않았다. Adapted 8k도 좋아졌지만 original control이 더 잘 좋아졌고, normalized ratio는 오히려 허용 기준에서 멀었다.

## Longer Budget Result

Step25는 8k adapted model과 original-control checkpoint를 추가 500k train tokens만큼 이어서 학습한 probe다. 따라서 total budget은 약 1M tokens이지만, fresh optimizer continuation probe이지 최종 from-scratch 1M control은 아니다.

| Metric | Adapted 8k continued | Original control continued | Ratio | Status |
| --- | ---: | ---: | ---: | --- |
| Final dev loss | 4.227845 +/- 0.017924 | 2.167797 +/- 0.035483 | 1.950296 | FAIL |
| Estimated NLL per word | n/a | n/a | 1.587381 | FAIL |
| Estimated NLL per char | n/a | n/a | 1.587381 | FAIL |

Interpretation: 더 오래 학습하면 adapted 8k loss는 내려간다. 하지만 original control도 더 빠르게 좋아지므로 상대 gap은 닫히지 않는다. 단순한 budget 증가는 현재 실패를 해결하지 못한다.

## Overall Experimental Flow

| Stage | Result | Interpretation |
| --- | --- | --- |
| XLM-R baseline audit | target10 전체 fragmentation 확인 | vocab extension의 필요성은 강함 |
| Vocabulary extension | 8k/16k/32k 모두 tokenizer 조건 충족, 32k tokenizer-only best | tokenizer 병목은 줄어듦 |
| Embedding initialization | `fvt`가 v2 zero-step loss `8.681328`로 best | random보다 훨씬 안정적 |
| Matched-token MLM control | adapted improves `3/3`, but original control much better | model-performance claim FAIL |
| Failure diagnosis | added/base loss ratio `2.835906`, added loss share `74.269955%` | 병목은 added-token prediction |
| Repair probes | weighted/new-row/staged/alt-init 모두 FAIL | 단일 처방으로는 부족 |
| Smaller vocab | 8k raw loss `4.541285` vs 32k `4.946829` | 8k가 낫지만 control 대비 FAIL |
| Longer budget | 8k normalized ratio `1.587381` | 더 오래 학습해도 gap 안 닫힘 |

## Recommended Next Experiment

Step28 roadmap 기준 다음 우선순위는 `E28_02_CURRICULUM_KL_MLM`이다.

핵심 아이디어:

1. Appended rows를 original XLM-R subtoken teacher supervision으로 더 강하게 초기/보정한다.
2. Added-token mask/loss pressure를 schedule로 조절한다.
3. Base-token behavior는 KL 또는 replay로 명시적으로 보존한다.
4. 성공 판정은 added/base/all loss를 모두 seed-stable하게 통과하고, Step16-style normalized word/char ratio가 `<= 1.100000`이어야 한다.

Rationale:

- Step18은 added loss를 줄였지만 all-token loss를 악화했다.
- Step19는 base를 보존했지만 added-token 개선에 실패했다.
- Step25는 longer MLM budget만으로 original-control gap이 닫히지 않음을 보였다.

따라서 다음 실험은 “added-token을 더 세게 학습”하거나 “base를 얼림” 중 하나만 택하는 방식이 아니라, stronger appended-token supervision과 explicit base preservation을 같이 넣어야 한다.

## Stop Rule

Step15/16-style controls가 통과하기 전에는 downstream 또는 translation final readout으로 넘어가지 않는다. `E28_02_CURRICULUM_KL_MLM`도 실패하면, vocabulary extension 자체보다 objective/data 설계 또는 external non-final target data collection 쪽으로 돌아가야 한다.

## Takeaway

현재 결론은 명확하다. Tokenizer-level vocabulary extension은 성공했지만, model-level MLM control은 실패했다. 실패 원인은 added-token prediction 병목이며, smaller vocab과 longer budget은 gap을 줄이는 데 충분하지 않았다. 다음 실험은 appended-token supervision과 base-token preservation을 함께 검증하는 objective로 가야 한다.
