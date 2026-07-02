# Plan: Source Grounding And Retrieval Editing

Status: 10A, pointwise 10B, pairwise 10B, a small 10C pairwise-selected edit gate, and same-checkpoint 10C controls complete; 10C is a negative neural-editing gate

## Goal

Design the next Coptic/Syriac experiment around source grounding, not simple scaling. The current evidence says retrieval is strong, but neural retrieval-augmented generation mostly copies the retrieved Coptic hint. This stage tests whether the model can choose, edit, or reject retrieved candidates based on the source verse.

## Current Motivation

Previous gates:

- Direct NMT runs end-to-end but collapses into repetitive or formulaic target fragments.
- Greek pivot/back-translation is a negative gate; scaling synthetic data from it is not recommended.
- Character n-gram retrieval is a strong full-test baseline around chrF++ 22.
- Top8 oracle retrieval reaches chrF++ 28.3327, so candidate selection has real headroom.
- Feature reranking improves top1 retrieval to chrF++ 24.5921, but neural retrieval-augmented generation remains copy-heavy.
- CPU-only 10B improves the retrieval selector slightly to chrF++ 24.6862, with oracle@8 still at 28.3327.
- CPU-only pairwise 10B improves the selector again to chrF++ 24.7438, with oracle@8 still at 28.3327.
- A small 10C ByT5 edit gate with pairwise-selected hints reaches test chrF++ 18.3574 on the 64-example slice, below the selected retrieval candidate itself at 26.6235.
- Same-checkpoint 10C controls show source-only collapse at chrF++ 0.2729, retrieved-only slightly above correct source+retrieval at 18.6220, wrong-shift1 at 12.8253, and feature-selected top8 at 19.1558.

## Hypothesis

A source-grounded candidate-selection or retrieval-editing objective will be more useful than another direct seq2seq or pivot run. If the model cannot improve over feature reranking or reduce copy dependence on diagnostic controls, then the paper should frame retrieval editing as future work rather than a completed positive result.

## Planned Experiments

### 10A. Source-Candidate Diagnostic Table

Run a CPU-only analysis over English/Syriac -> Coptic top-k retrieval outputs.

Inputs:

- top1 retrieval candidate
- feature-reranked candidate
- top8 oracle candidate
- gold Coptic reference
- source verse

Measurements:

- chrF++ gap: top1 vs feature reranker vs oracle
- exact-copy and near-copy rates
- candidate length ratio
- source-neighbor mismatch examples
- examples where feature reranker improves or hurts top1

Output:

- `source_candidate_diagnostics.tsv`
- `source_candidate_summary.md`
- `source_candidate_examples.md`

Success gate:

- Passed. The diagnostic profile explains where feature reranking helps, where it degrades top1, and how much oracle@8 headroom remains.

### 10B. Keep/Edit/Reject Classifier

Train or fit a lightweight candidate decision model that predicts whether a retrieved Coptic candidate should be kept, edited, or rejected.

Candidate implementations:

- CPU feature model over top-k retrieval features;
- small transformer classifier if GPU 3 is available;
- pairwise candidate ranker trained from oracle top-k labels.

Labels:

- `KEEP` when top1 is close to gold and better than alternatives;
- `SWAP_TO_RANK_k` when another top-k candidate is clearly better;
- `REJECT` when all retrieved candidates are poor.

Metrics:

- candidate-choice accuracy against oracle labels
- selected-candidate chrF++
- improvement over top1 retrieval
- degradation rate relative to top1

Output:

- `candidate_decision_results.tsv`
- `candidate_decision_model_cv.tsv`
- `candidate_decision_test_selected.tsv`
- `candidate_decision_feature_importances.tsv`
- `candidate_decision_method.md`
- `candidate_decision_summary.md`
- `candidate_decision_errors.md`

Success gate:

- Passed with caveat. The validation-selected gradient-boosting selector beats top1 retrieval and slightly improves over the existing feature reranker on corpus chrF++, but it still leaves a meaningful oracle@8 gap.

### 10C. Retrieval-Editing Pilot

Train a small edit model only after 10A/10B show that candidate decisions are meaningful.

Input format:

```text
translate/edit
source_lang=<eng|syr>
target_lang=cop
source=<source verse>
retrieved_source=<nearest source verse>
retrieved_coptic=<candidate>
decision_hint=<KEEP|EDIT|REJECT>
```

Target:

- gold Coptic verse

Training scope:

- Start with a 64 or 128 example pilot.
- Use `google/byt5-small` only as a diagnostic model.
- Use physical GPU 3 only via `source scripts/gpu3_env.sh`.
- Use `--skip_save_model` for first gates unless a run clearly improves.

Controls:

- correct retrieval
- wrong retrieval
- retrieved-only
- source-only
- feature-selected top8 hint

Metrics:

- BLEU
- chrF++
- exact-copy rate from retrieved Coptic
- wrong-retrieval sensitivity
- generated length
- target-script rate

Output:

- `retrieval_edit_pilot_results.tsv`
- `retrieval_edit_controls.md`
- `retrieval_edit_qualitative.md`
- `retrieval_edit_control_datasets.tsv`
- `retrieval_edit_control_results.tsv`

Success gate:

- Failed for the first pairwise-selected gate. Exact-copy behavior is reduced, but the generated output remains retrieval-like and underperforms the retrieved candidate itself.
- Failed. Same-checkpoint controls show that retrieved-only slightly beats correct source+retrieval, while source-only collapses. Wrong retrieval hurts, so the model is retrieval-sensitive, but the current small ByT5 gate is not source-grounded enough.

## GPU Policy

GPU work in this stage must use only physical GPU 3:

```bash
source scripts/gpu3_env.sh
```

Inside the process, physical GPU 3 appears as `cuda:0`.

## Decision Rule

Proceed in this order:

1. Finish 10A diagnostics.
2. Only run 10B if diagnostics show candidate-selection headroom not already exhausted by feature reranking.
3. Only run 10C if 10B produces a selector that improves over top1 retrieval or gives useful keep/edit/reject labels.

Do not scale direct NMT, Greek pivot, or back-translation unless a new gate fixes the current source-grounding and target-script failures.

Current decision:

- Pairwise 10B is the preferred CPU retrieval selector for any next retrieval-augmented run.
- 10C has one completed small GPU gate; it is a negative signal, not a positive translation result.
- 10C follow-up same-checkpoint controls are complete.
- Use the 10C result as failure analysis, not as a positive neural-editing claim.
- Do not scale neural retrieval editing until the source-control tests pass.

## Paper Outcome

Positive outcome:

- Add a final source-grounding experiment showing retrieval can be used as evidence rather than copied verbatim.

Negative outcome:

- Add a clean failure analysis: retrieval is a strong baseline, but current neural models do not learn reliable source-conditioned editing under this budget.
