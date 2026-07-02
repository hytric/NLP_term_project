# 07. Smaller Vocab Probe

Sources:

- `docs/exp/second_try/23_v2_vocab_size_objective_probe`
- normalized check: `docs/exp/second_try/24_v2_8k_mlm_control`

Goal: 32k extension이 tokenizer-only metric에서는 best였지만, added rows가 너무 많아 model-side 학습을 어렵게 만들 수 있다. 그래서 8k/16k smaller vocab이 MLM control에서 더 나은지 확인했다.

Main finding: 8k가 32k보다 낫긴 했다. 그러나 original XLM-R continued-pretraining control 대비 gap은 여전히 컸고, normalized fairness gate도 실패했다.

## Raw MLM Comparison

| Model / vocab | Mean final raw dev loss | Vs 32k | Vs original control |
| --- | ---: | ---: | ---: |
| Adapted 32k | 4.946829 | baseline | 1.964580 |
| Adapted 16k | 4.798048 | -0.148781 | 1.905494 |
| Adapted 8k | 4.541285 | -0.405544 | 1.803523 |
| Original control | 2.518008 | n/a | baseline |

## Vocab Size Effect

| Comparison | Loss difference | Relative change | Interpretation |
| --- | ---: | ---: | --- |
| 16k vs 32k | -0.148781 | -3.008% | 16k가 32k보다 약간 나음 |
| 8k vs 32k | -0.405544 | -8.198% | 8k가 32k보다 뚜렷하게 나음 |
| 8k vs 16k | -0.256763 | -5.351% | 8k가 16k보다도 나음 |

Interpretation: vocab size를 줄이면 raw MLM loss가 내려갔다. 즉 32k는 tokenizer-only metric에서는 가장 좋았지만, model-side에서는 added row가 너무 많아 학습 부담이 컸던 것으로 해석된다. 8k는 added-token class 수를 줄여서 32k보다 좋은 MLM loss를 보였지만, original XLM-R control과의 gap은 여전히 남았다.

Additional run status:

| Metric | Value |
| --- | ---: |
| Vocab sizes tested | 8k, 16k |
| Completed runs | 6/6 |
| Token budget ratio | 1.000450 |
| Passing variants within Step23 local gate | 2/2 |
| Best vocab | 8k |

Interpretation: smaller vocab reduces the added-row burden. The direction is useful: `8k < 16k < 32k` in final raw dev loss. This supports the trade-off that tokenizer-side compression is not the only objective; model-side class sparsity matters.

## Normalized Fairness Check For 8k

| Metric | Adapted 8k | Original control | Ratio | Status |
| --- | ---: | ---: | ---: | --- |
| Step23 raw final dev loss | 4.541285 +/- 0.021088 | 2.518008 +/- 0.033126 | 1.803523 | FAIL |
| Re-evaluated raw masked loss | n/a | n/a | 1.811332 | FAIL |
| Estimated NLL per word | n/a | n/a | 1.472019 | FAIL |
| Estimated NLL per char | n/a | n/a | 1.472019 | FAIL |

허용 기준은 `ratio <= 1.100000`이다. 8k는 32k보다 유리하지만, original control과 비교하면 여전히 크게 뒤진다.

## Takeaway

Smaller vocab은 올바른 방향의 개선이지만 충분한 해결책은 아니다. 32k의 문제를 “vocab이 너무 커서만”이라고 볼 수는 없다. 8k에서도 added-token prediction과 objective mismatch 문제가 남아 있으며, original XLM-R continued-pretraining control을 따라잡지 못했다.
