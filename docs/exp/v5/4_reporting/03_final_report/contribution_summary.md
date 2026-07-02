# v5 Contribution Summary

Last updated: 2026-06-28 KST

This file summarizes what v5 can currently claim as contributions and what
must remain pending until matched checkpoints and final downstream outputs are
available.

## Current Contribution Statement

Safe one-paragraph version:

```text
We reproduce the Glot500-style training and evaluation workflow on a controlled
102-language-script setting consisting of 92 XLM-R-seen Glot500 languages and
10 diverse Glot500-internal target languages. Within this replay, we isolate a
vocabulary-extension question that is not answered by the corpus construction
itself: how should newly appended embedding rows be initialized? The current
completed evidence shows that source-token decomposition initialization
substantially improves zero-step target MLM proxy loss over random resize while
passing source-row, <mask>, byte-row, and LM-head tying audits. Final after-MLM
and downstream transfer claims remain pending matched v5_random/v5_fvt
checkpoints and parsed task outputs. The measured v5-random rows are diagnostic
single-method evidence, not a paired method claim.
```

## Contributions

| Contribution | Current evidence | Claim status |
| --- | --- | --- |
| Controlled Glot500-style replay | 102-language corpus, full merge PASS, tokenizer append, initialized checkpoints, metric wrappers | supported as setup/execution-in-progress |
| Glot500-internal target10 design | target manifest, `new_length >= 30000`, raw dirs present, diversity criteria | supported |
| Tokenizer append audit | extended vocab 368,687; 118,685 appended tokens; 29/30 audited languages improve | supported with `dzo_Tibt` caveat |
| Initialization correctness | identity row copy, `<mask>` remap diff 0.0, byte-row accounting, LM-head tied | supported |
| FVT zero-step advantage | target weighted NLL random 18.411756, mean 11.953142, FVT 8.785518 | supported intrinsically |
| Glot500 metric retention | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, Roundtrip folders/wrappers/coverage notes | supported as metric-family design |
| Baseline/reference replay rows | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip XLM-R/Glot500-base rows parsed where local data exists | supported with coverage caveats |
| v5-random diagnostic replay rows | PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip rows parsed for the 10K random checkpoint where local data exists | supported as diagnostic, not a method win |
| After-MLM FVT improvement | matched 10K checkpoints not yet available | pending |
| Downstream FVT improvement | paired v5-FVT downstream rows not yet available | pending |

## What To Emphasize In The Report

1. The work is a faithful controlled replay of the Glot500 pattern, not a
   full-scale model release.
2. The novelty is method-level: initialization of appended vocabulary rows.
3. The zero-step result is already strong enough to justify the hypothesis.
4. The experiment is carefully audited because SPM append moves special ids.
5. Coverage limitations are a result, not a reason to silently omit metrics.
6. Live dev scores and running steps are progress signals, not final result
   rows.

## What Not To Claim

- Do not claim full 511-language Glot500 reproduction.
- Do not claim target10 downstream improvement until partial official target task
  membership is materialized and evaluated correctly.
- Do not claim after-MLM FVT improvement until matched checkpoints are evaluated.
- Do not treat `cis-lmu/glot500-base` as an equal-budget baseline.
- Do not hide `dzo_Tibt`; it is a documented tokenizer regression and a useful
  failure analysis case.

## Elevator Pitch

Short version:

```text
This project reruns the Glot500 recipe on a controlled 102-language subset and
shows that how we initialize newly appended vocabulary rows matters before
continued training even starts.
```

Slightly longer version:

```text
We keep the Glot500-style tokenizer, MLM, and metric structure, but focus the
experiment on 92 XLM-R-seen languages plus 10 diverse Glot500-internal targets.
The key novelty is source-token decomposition initialization for new vocabulary
rows, which gives a much better zero-step target MLM proxy than random resize.
The remaining question is whether this early advantage survives matched MLM
training and transfers to available downstream tasks.
```

## Final Upgrade Conditions

The contribution can be upgraded from an intrinsic initialization result to an
after-training method result only after:

1. `v5_random_mlm_10k` and `v5_fvt_mlm_10k` both produce selected checkpoints.
2. PPPL is evaluated for both checkpoints with the same cached examples.
3. Available downstream tasks are evaluated through `scripts/run_v5_eval_metric.sh`.
4. The guarded post-checkpoint wrapper and reporting refresh parse the outputs:
   `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all`
   followed by `python3 scripts/refresh_v5_reporting.py --with-plots`.
5. `paper_draft.md`, `ppt_content.md`, and `presenter_script_ko.md` are updated
   from measured artifacts rather than live snapshots.
