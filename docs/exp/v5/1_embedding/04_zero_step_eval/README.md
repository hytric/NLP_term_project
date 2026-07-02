# 04 Zero-Step Eval

Use this folder for before-training comparisons across initialization methods.

Required summaries:

- head MLM proxy
- tail MLM proxy
- all MLM proxy
- v5-target subset MLM proxy
- row norm and cosine preservation tables

Current pilot result:

```text
pilot10k/results.md
pilot10k/analysis.md
```

Pilot finding: `v5_fvt` improves v5-target weighted NLL over `v5_random` by
`-9.448385` and over `v5_mean` by `-3.423689`.

Current main result:

```text
main/results.md
main/analysis.md
```

Main finding: with the full tokenizer and full initialized checkpoints,
`v5_fvt` improves v5-target weighted NLL over `v5_random` by `-9.626238` and
over `v5_mean` by `-3.167624`. It also improves head weighted NLL over
`v5_random` by `-6.273844`.

## Next Step Gate

Move to `../05_audit/` and then `../../2_training/` only after zero-step results
are comparable across methods.

Pass line:

- `v5_random` and `v5_fvt` are evaluated on the same data split.
- `xlmr_base` is included where the metric is meaningful.
- head, tail, all, and v5-target subset summaries are present.
- method checkpoint paths and tokenizer path are recorded.
- any missing `mean` or `align` result has a reason.

Required artifacts:

- model-wise zero-step table
- command log
- data split note
- row norm/cosine preservation table

If `v5_fvt` is worse than `v5_random`, do not stop automatically. Carry the
result forward as an important diagnostic, but make sure training comparisons
preserve the same setup.

Current status: pass for `random`, `mean`, and `fvt` zero-step comparison.
