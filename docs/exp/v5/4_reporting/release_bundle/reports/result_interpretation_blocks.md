# v5 Result Interpretation Blocks

Last updated: 2026-06-28

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`../final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
interpretation block header.

These blocks are ready-to-adapt prose for the final report and presentation
after matched `v5_random` and `v5_fvt` results arrive. Use only the block that
matches parsed evidence in `3_evaluation/09_aggregation/`.

## Template-Only Guard

These are outcome templates, not current-result claims. Do not copy any
positive, mixed, or negative final outcome block into `Report.md`,
`paper_draft_ko.md`, `final_deck_ko.md`, or `presenter_script_ko.md` until:

1. both matched checkpoints are `ready_for_wrapper=yes`;
2. `post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`;
3. paired `v5_random`/`v5_fvt` PPPL and available downstream rows are parsed in
   `3_evaluation/09_aggregation/`; and
4. `comparison_materiality_audit.md` marks the relevant difference as more than
   `tie_band`; and
5. final_claim_decision_tree.md selects a non-pending outcome.

Before those gates close, the current conclusion remains setup fidelity plus
zero-step initialization evidence, with after-MLM and downstream method claims
locked.

## Final Evidence Packet Rule

Before using any outcome block below, assemble a single evidence packet from
the same refresh point:

1. checkpoint pair: `model_matrix.tsv`, `selected_checkpoint_manifest.md`, and
   `post_checkpoint_preflight.md`;
2. parsed rows: `metric_completion.tsv`, `main_head_tail_all.tsv`, and
   `v5_target_subset.tsv`;
3. provenance: `post_checkpoint_provenance_audit.md` plus metric command logs;
4. materiality: `method_comparison_summary.md` and
   `comparison_materiality_audit.md`;
5. claim gates: `claim_promotion_matrix.md`, `final_claim_decision_tree.md`,
   and `final_claim_freeze_audit.md`;
6. patch targets: `post_result_patch_plan_ko.md` and this file; and
7. final package checks: `reporting_package_audit.md`,
   `final_submission_smoke_audit.md`, and `release_bundle_audit.md`.

If any item is missing, stale, or still waiting, keep the current
execution-draft conclusion. A strong single metric, live log, or random-only
row is not enough to select a final outcome block.

## Core Interpretation Rule

The paper should separate three evidence layers:

1. setup fidelity: corpus, tokenizer, initialization, and metric protocol;
2. intrinsic method evidence: zero-step and after-MLM PPPL;
3. downstream transfer evidence: available-language task results with coverage.

Do not let downstream coverage limitations erase the initialization result, and
do not let a strong zero-step result become an unsupported downstream claim.
The currently measured `v5_random` rows are diagnostic single-method rows until
the matched `v5_fvt` rows are parsed; they should not be promoted as method
wins or losses by themselves.

## If FVT Wins On PPPL

Report paragraph:

```text
After matched continued MLM, FVT retains the zero-step advantage on the
intrinsic PPPL evaluation. Because `v5_random` and `v5_fvt` share the same
tokenizer, corpus, training budget, and checkpoint-selection rule, this result
supports the hypothesis that initialization of appended vocabulary rows affects
adaptation beyond the first forward pass. The result should be interpreted as
an intrinsic language-modeling gain over the controlled v5 language set, with
target10 downstream transfer evaluated separately according to task coverage.
```

Slide line:

```text
The initialization advantage survives matched MLM on PPPL.
```

## If FVT Wins At Zero-Step But Not After MLM

Report paragraph:

```text
FVT strongly improves zero-step target MLM proxy, but the advantage does not
survive the matched continued-MLM budget. This suggests that source-token
decomposition provides a better starting point, while subsequent MLM updates
can reduce or overwrite the initialization gap. In this outcome, the main
contribution remains diagnostic: initialization matters early, but longer or
more targeted training is needed to determine whether the advantage is
preserved.
```

Slide line:

```text
FVT gives a better start; matched MLM tests how long that start matters.
```

## If FVT Helps PPPL But Downstream Is Mixed

Report paragraph:

```text
The intrinsic PPPL result and downstream transfer result diverge. FVT improves
language-modeling behavior under the controlled v5 evaluation, but available
downstream tasks show mixed or coverage-limited movement. This is plausible:
the selected target10 has raw-text coverage but little downstream task
coverage, and several downstream rows are measured over available head/all
languages rather than the selected target set. The correct conclusion is
therefore a bounded one: FVT improves intrinsic adaptation, while downstream
transfer remains task- and coverage-dependent.
```

Slide line:

```text
Intrinsic gains are clearer than downstream transfer under current coverage.
```

## If FVT Does Not Beat Random

Report paragraph:

```text
Despite a strong zero-step advantage, FVT does not outperform random resize in
the final matched evaluation. This negative result is still informative
because the method was tested under controlled tokenizer, corpus, and budget
conditions. It suggests that initialization alone may not be sufficient once
new rows receive enough MLM updates, or that the decomposition signal is not
aligned with the downstream objective. The zero-step result remains evidence
that initialization changes early behavior, but the final method claim should
be limited accordingly.
```

Slide line:

```text
Initialization changes the starting point, but final gains are not guaranteed.
```

## If Bible And Roundtrip V5 Rows Are Pending

Report paragraph:

```text
Bible retrieval and roundtrip alignment are retained as Glot500 metric
families. Bible retrieval is materialized for available Glot500 Bible task
languages, and XLM-R-base/Glot500-base/v5-random rows are measured. The
remaining Bible gap is the v5-FVT row, which waits for the matched checkpoint.
Roundtrip alignment now has Bible-derived inputs, a v5 runner, and measured
XLM-R-base/Glot500-base/v5-random rows over 74/102 available language-scripts.
The remaining Roundtrip gap is also the v5-FVT row, which waits for the matched
checkpoint. We therefore report both metrics as partial rather than omitting
either metric family.
```

Slide line:

```text
Bible and Roundtrip have measured XLM-R/Glot500/v5-random rows; both wait for v5-FVT.
```

## If Target10 Downstream Coverage Remains 0/10

Report paragraph:

```text
The selected target10 is fully represented in raw-text PPPL but not in the
currently materialized downstream task sets. As a result, target10-specific
claims are restricted to tokenization, initialization diagnostics, and PPPL.
Downstream rows are reported over available languages with head/all grouping
and explicit coverage notes. This prevents a coverage gap from being mistaken
for either a positive or negative target10 transfer result.
```

Slide line:

```text
Target10 evidence is intrinsic; downstream replay is available-language based.
```

## Korean Talk Blocks

### Strong PPPL Outcome

```text
같은 tokenizer, 같은 corpus, 같은 budget에서 FVT가 PPPL에서도 random보다 좋다면,
이건 단순히 zero-step에서만 좋은 초기값이 아니라 continued MLM 이후에도 남는
초기화 효과라고 말할 수 있습니다. 다만 downstream은 task coverage가 다르기
때문에 따로 해석해야 합니다.
```

### Mixed Outcome

```text
zero-step에서는 FVT가 분명히 좋지만 downstream은 섞여 나올 수 있습니다. 이때
중요한 점은 결과를 실패로 단순화하지 않는 것입니다. target10은 PPPL에는
들어가지만 downstream에는 거의 없기 때문에, intrinsic result와 downstream
transfer를 분리해서 말해야 합니다.
```

### Negative Outcome

```text
만약 최종적으로 random이 FVT를 따라잡는다면, 결론은 FVT가 틀렸다는 것이 아니라
초기화 효과가 training 과정에서 희석될 수 있다는 것입니다. 이 경우에도
zero-step 결과는 새 vocabulary row initialization이 early adaptation에 영향을
준다는 evidence로 남습니다.
```

### Coverage Defense

```text
Bible과 roundtrip은 일부러 빼지 않았습니다. Glot500 metric family로 유지했고,
Bible retrieval은 available language-script 74개로 materialize 되었기 때문에
XLM-R-base, Glot500-base, v5-random row까지 측정했습니다. Roundtrip도
Bible-derived input과 v5 runner를 materialize했고 XLM-R-base, Glot500-base,
v5-random row를 측정했습니다. 남은 것은 두 metric 모두 matched checkpoint 이후
v5-FVT row입니다. 이게 reproduction boundary를 정직하게 보여주는 부분입니다.
```

## Current Execution-Draft Conclusion

```text
This work reproduces the Glot500-style workflow on a controlled 102-language
subset and isolates appended-vocabulary initialization as the main method
question. The setup fidelity is supported by the fixed 92+10 corpus, successful
SentencePiece append, audited embedding initialization, and retained Glot500
metric families. The current intrinsic evidence shows a strong zero-step FVT
advantage on the v5 target group, while the final paired method claim remains
pending the matched `v5_fvt` checkpoint. Baseline/reference rows are measured
for PPPL, Tatoeba retrieval, Bible retrieval, Taxi1500 text classification,
NER, POS, and Roundtrip alignment where local task data exists, and v5-random
rows are already measured for PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and
Roundtrip. Target10 downstream claims remain bounded by task coverage. Overall,
the current draft supports a setup-fidelity and intrinsic-initialization claim,
not yet a final after-training or downstream superiority claim.
```

## Final Abstract Update Choices

Use one abstract update only after `final_claim_decision_tree.md` selects the
matching outcome. Keep the first abstract sentences about scope and method
stable; replace only the final result/claim sentences.

### Abstract: FVT Wins PPPL And Most Available Downstream Rows

```text
After matched continued MLM, source-token decomposition initialization retains
its intrinsic PPPL advantage over random resize and improves most
available-language downstream rows under the controlled v5 budget. These
results support a bounded positive claim: appended-row initialization can
improve both intrinsic adaptation and available-task transfer, while target10
downstream claims remain constrained by task coverage.
```

Korean abstract sentence:

```text
matched continued MLM 이후 FVT는 intrinsic PPPL 우위를 유지하고 available-language
downstream row 대부분에서도 random resize보다 유리했다. 따라서 본 연구의 최종 claim은
target10 downstream coverage 한계를 명시한 bounded positive claim으로 둔다.
```

### Abstract: FVT Wins PPPL But Downstream Is Mixed

```text
After matched continued MLM, source-token decomposition initialization improves
intrinsic PPPL relative to random resize, but available downstream results are
mixed across tasks and coverage regimes. The final claim is therefore bounded:
FVT improves intrinsic adaptation, while downstream transfer remains task- and
coverage-dependent.
```

Korean abstract sentence:

```text
matched continued MLM 이후 FVT는 intrinsic PPPL에서는 random resize보다 유리했지만,
downstream transfer는 task와 coverage에 따라 섞여 나타났다. 따라서 최종 claim은
intrinsic adaptation 개선으로 제한하고, downstream 효과는 coverage-dependent하게 해석한다.
```

### Abstract: FVT Wins Zero-Step Only

```text
Source-token decomposition initialization substantially improves zero-step
target MLM proxy loss, but the advantage is not preserved after the matched
continued-MLM budget. This outcome makes the contribution diagnostic rather
than superiority-based: appended-row initialization changes early adaptation,
but final gains require additional conditions.
```

Korean abstract sentence:

```text
FVT는 zero-step target MLM proxy에서 random resize보다 훨씬 좋은 시작점을 제공했지만,
matched continued MLM 이후 그 우위가 보존되지는 않았다. 이 경우 본 연구의 기여는
final superiority가 아니라 early adaptation을 바꾸는 diagnostic evidence로 해석한다.
```

### Abstract: Random Catches Or Beats FVT After MLM

```text
Although source-token decomposition initialization changes the zero-step
starting point, random resize catches or exceeds it in the final matched
evaluation. The result is negative but informative: initialization affects
early behavior, yet continued MLM can reduce or reverse the initial advantage
under this budget.
```

Korean abstract sentence:

```text
FVT는 zero-step starting point를 바꾸지만, 최종 matched evaluation에서 random resize가
따라잡거나 앞선다면 after-training superiority claim은 하지 않는다. 이 결과는 초기화
효과가 training 중 줄거나 뒤집힐 수 있음을 보여주는 negative but useful evidence이다.
```

### Abstract: Incomplete Evaluation / Execution Draft

```text
The controlled v5 setup, tokenizer expansion, initialization audits, and
Glot500 metric-family replay protocol are complete, but the final matched
method comparison remains pending because one or more selected checkpoint,
parsed metric, provenance, or final-evidence-packet gates are not closed. We
therefore report setup fidelity and zero-step initialization evidence while
leaving after-MLM and downstream superiority claims locked.
```

Korean abstract sentence:

```text
controlled v5 setup, tokenizer expansion, initialization audit, Glot500 metric-family
replay protocol은 준비되었지만 selected checkpoint, parsed metric, provenance,
또는 Final Evidence Packet gate 중 하나라도 닫히지 않으면 최종 method comparison은
pending으로 둔다. 따라서 현재 결론은 setup fidelity와 zero-step initialization evidence까지로
제한하고, after-MLM/downstream superiority claim은 잠근다.
```

## Final Conclusion Fill-In Choices

Use one of these final-clause choices after matched v5 rows are parsed:

| Outcome | Final method claim |
| --- | --- |
| FVT wins PPPL and most available downstream rows | `source-token decomposition initialization improves both intrinsic adaptation and available-language downstream transfer under the controlled v5 budget` |
| FVT wins PPPL but downstream is mixed | `source-token decomposition initialization improves intrinsic adaptation, while downstream transfer remains task- and coverage-dependent` |
| FVT wins zero-step only | `source-token decomposition initialization provides a better starting point, but the advantage is not preserved across the matched continued-MLM/evaluation budget` |
| random catches or beats FVT after MLM | `initialization changes early behavior, but continued MLM can reduce or reverse the initial advantage` |
| incomplete evaluation / execution draft | `setup fidelity and zero-step initialization evidence are supported, while final after-MLM and downstream superiority claims remain locked` |

## Korean Final Conclusion Choices

보고서 `8. 결론 초안`과 발표 slide 14는 아래 다섯 가지 중 aggregation 결과와
`final_claim_decision_tree.md`가 허용하는 문장만 사용한다.

### FVT Wins PPPL And Most Available Downstream Rows

```text
본 실험은 controlled 102-language setting에서 Glot500-style workflow를 재연하고,
vocabulary extension 이후 source-token decomposition 기반 FVT initialization이
intrinsic PPPL뿐 아니라 available-language downstream transfer에서도 random resize보다
유리할 수 있음을 보였다. 다만 target10 downstream coverage는 제한적이므로, target10에
대한 직접 downstream 개선 claim은 PPPL 및 coverage가 허용하는 범위로만 해석한다.
```

Slide 14 line:

```text
FVT는 controlled v5 budget에서 intrinsic adaptation과 available-language transfer를 함께 개선했다.
```

### FVT Wins PPPL But Downstream Is Mixed

```text
본 실험은 controlled 102-language setting에서 Glot500-style workflow를 재연하고,
FVT initialization이 matched MLM 이후 intrinsic PPPL에서는 random resize보다 유리함을
보였다. 그러나 downstream transfer는 task와 coverage에 따라 섞여 나타났다. 따라서
최종 결론은 FVT가 intrinsic adaptation을 개선하지만 downstream 효과는 available task와
coverage에 의존한다는 bounded claim으로 제한한다.
```

Slide 14 line:

```text
FVT의 intrinsic gain은 명확하지만 downstream transfer는 coverage-dependent하다.
```

### FVT Wins Zero-Step Only

```text
본 실험은 FVT initialization이 zero-step MLM proxy에서 random resize보다 훨씬 좋은
시작점을 제공한다는 점을 보였다. 하지만 matched continued MLM 이후 그 advantage가
보존되지 않는다면, 최종 claim은 early adaptation 진단으로 제한한다. 즉 새 vocabulary row
초기화는 출발점을 바꾸지만, 같은 MLM budget 이후의 우위는 별도 조건이 필요하다.
```

Slide 14 line:

```text
FVT는 더 좋은 시작점을 제공하지만, matched MLM 이후 우위 보존은 확인되지 않았다.
```

### Random Catches Or Beats FVT After MLM

```text
본 실험은 initialization이 early behavior를 크게 바꿀 수 있음을 보였지만, 최종 matched
평가에서 random resize가 FVT를 따라잡거나 앞선다면 after-training superiority claim은
하지 않는다. 이 경우 v5의 기여는 negative result를 포함한 진단적 기여이다. 새 row
초기화는 중요하지만, continued MLM이 초기 차이를 줄이거나 뒤집을 수 있음을 보여준다.
```

Slide 14 line:

```text
초기화는 early behavior를 바꾸지만, final gain은 보장되지 않는다.
```

### Incomplete Evaluation / Execution Draft

```text
본 실험은 controlled 102-language setting에서 Glot500-style workflow를 재연하는
setup, tokenizer expansion, embedding initialization audit, metric-family replay
protocol을 완성했다. 그러나 matched checkpoint, parsed metric row, provenance,
Final Evidence Packet 중 하나라도 닫히지 않은 상태에서는 final method/downstream
superiority claim을 하지 않는다. 이 경우 보고서와 발표의 확정 결론은 setup fidelity와
zero-step FVT initialization advantage까지로 제한한다.
```

Slide 14 line:

```text
현재 확정 결론은 setup fidelity와 zero-step novelty이며, final method claim은 evidence packet 이후에만 열린다.
```

## Metric-Specific Replacement Checklist

When final v5 rows arrive, replace the pending text in the report and deck in
this order:

| Metric family | Required replacement | Keep if still true |
| --- | --- | --- |
| PPPL / MLM proxy | `v5_random`, `v5_fvt`, and `fvt - random` for target/head/all | target10 PPPL is the main target-specific after-MLM evidence |
| Tatoeba retrieval | available-language head/all `v5_random` and `v5_fvt` Top-10 | selected target10 coverage remains `0/10` unless data changes |
| Bible retrieval | available-language `v5_random` and `v5_fvt` Top-10 over the local Bible set | Bible is partial but retained; target10 coverage remains `0/10` |
| Taxi1500 classification | local available-language macro-F1 for both v5 models | local data is English-only unless materialization changes |
| NER/POS | final test F1 for both v5 models, with train-language caveats | NER target intersection is not target10-wide evidence |
| Roundtrip alignment | available-language `v5_random` and `v5_fvt` accuracy over the local Roundtrip set | baseline/reference rows are measured; target10 coverage remains `0/10` |

After replacement, rerun:

```bash
python3 scripts/refresh_v5_reporting.py --with-plots
```

Then inspect `comparison_materiality_audit.md` before strengthening the prose:
`large` or `moderate` FVT wins can support stronger wording, `small` wins should
stay cautious, and `tie_band` must be written as no clear practical separation.
