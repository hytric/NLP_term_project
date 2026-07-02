# Stage 06 Checkpoint Selection Proxy

작성일: 2026-06-13

## Question

Could an earlier saved checkpoint avoid the high-resource control collapse while preserving target10 behavior?

## Compared Checkpoints

Saved checkpoints available from the Stage 05 fvt pilot:

- `checkpoint-150`
- `checkpoint-200`

Checkpoint-50 and checkpoint-100 were not retained because Stage 05 used `save_total_limit=2`.

## Result

| Checkpoint | Target10 FVT mean loss | Target10 delta vs XLM-R | High-resource delta vs XLM-R | No-large-collapse languages |
| ---: | ---: | ---: | ---: | ---: |
| 150 | 5.348870 | +1.876033 | +0.757355 | 0/4 |
| 200 | 5.298593 | +1.825756 | +0.703114 | 0/4 |

## Interpretation

Early checkpoint selection does not rescue the current candidate. The retained `checkpoint-150` is worse than `checkpoint-200` on both target10 MLM proxy and high-resource control proxy. The failure is therefore not just a late-training overfit that can be solved by selecting the earlier retained checkpoint.

## Claim Boundary

This does not prove that all earlier checkpoints would fail, because checkpoint-50 and checkpoint-100 were not retained. It does show that the available retained earlier checkpoint cannot support a positive claim.
