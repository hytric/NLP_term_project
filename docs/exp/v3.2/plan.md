# V3.2 Overall Plan

작성일: 2026-06-19

## Objective

`v3.2` addresses the language-performance gap discovered in `v3.1/05_additional`.

The central question is:

> Can we turn the v3.1 append-only tokenizer and weak MLM adaptation into a model that actually predicts target-language content tokens and retrieves aligned target10 sentences above the current weak baseline?

## Core Optimization Principle

The first v3.2 target is not translation, retrieval, or POS.

The first target is:

> improve low-resource target10 Pseudoperplexity / MLM Intrinsic Evaluation by using as much high-resource language source as possible.

Reason:

- MLM is the training proxy task used by the adaptation pipeline;
- pseudoPPL/content-token MLM directly checks whether the model assigns higher probability to true low-resource tokens;
- sentence retrieval and translation should be treated as later diagnostics unless the MLM proxy first becomes credible.

This does not mean blindly increasing high-resource replay ratio. It means using high-resource data as the largest available transfer source while preserving enough target10 exposure for `chr/cop/oji/syr` content tokens to actually improve.

## Diagnosis To Fix

`v3.1` should be treated as a controlled diagnostic, not as a final low-resource adaptation success.

Main failures:

1. Content-token MLM is weak.
   - `align/fvt/focus` have content-token top-1 around `4%`.
   - average content-token gold probability is around `0.00018-0.00021`.
   - `chr/cop/oji` have content-token top-10 near `0%`.

2. Sentence retrieval is weak.
   - target10 centered-CSLS R@1 remains around `0.9%-1.2%`.
   - hard margin is negative for all `mlm200` variants.
   - `syr` and `cop` are the lowest retrieval languages by source/target macro.

3. The training signal is too small and diluted.
   - the 200-step probe consumes about `6,400` chunks.
   - target10 low-resource lines are only about `52K` out of `966K` train-mixture lines.
   - high-resource replay was useful for retention, but v3.2 should use high-resource source more deliberately as a transfer signal for low-resource MLM proxy improvement.

4. MLM does not optimize semantic retrieval.
   - `fvt` wins dynamic MLM dev loss but does not win sentence retrieval.
   - retrieval needs an explicit alignment objective or a downstream probe.

## Hypotheses

| ID | Hypothesis | Main Test |
| --- | --- | --- |
| H1 | The worst content-token failures are caused by insufficient target-script exposure after tokenizer expansion. | language-balanced MLM improves `chr/cop/oji/syr` content-token top-k and gold probability. |
| H2 | High-resource language source can improve low-resource MLM if sampled as transfer data rather than passive replay. | high-resource-source-heavy MLM improves target10 content-token pseudoPPL/gold probability over v3.1. |
| H3 | The current tokenizer still overuses boundary/punctuation-like easy tokens. | tokenization audit lowers standalone `▁` dominance and raises meaningful content-token coverage. |
| H4 | Longer MLM improves token prediction but not necessarily semantic retrieval. | compare content-token MLM and centered-CSLS retrieval separately at each checkpoint. |
| H5 | Sentence retrieval needs an explicit semantic alignment stage. | contrastive/TLM stage improves centered-CSLS R@1/MRR/margin over MLM-only. |
| H6 | Downstream/translation gains must be explained by retrieval and content-token metrics, not script-only collapse recovery. | pair classification, POS, retrieval-only translation, and decoder diagnostics agree with alignment gains. |

## Stage Order

| Stage | Folder | Depends On | Must Produce | Exit Gate |
| --- | --- | --- | --- | --- |
| 00 | `00_problem_diagnosis` | v3.1 artifacts | failure table, metric contract, pass/fail gates | `V32_DIAGNOSIS_FROZEN` |
| 01 | `01_tokenizer_repair` | v3.1 tokenizer audit | content-token/tokenization audit and repair decision | `PASS_TOKENIZER_REPAIR_READY` or `KEEP_V31_TOKENIZER` |
| 02 | `02_balanced_mlm` | 00, 01 | high-resource-source-augmented MLM checkpoints, learning curves, content-token eval | `PASS_CONTENT_TOKEN_MLM` |
| 03 | `03_semantic_alignment` | 02 | contrastive/TLM checkpoints, CSLS retrieval, hubness, language breakdown | `PASS_SEMANTIC_ALIGNMENT` |
| 04 | `04_downstream_translation` | 03 | downstream probes, POS, retrieval/decode diagnostics | `PASS_DOWNSTREAM_DIAGNOSTIC` or `WEAK_ONLY` |
| 05 | `05_report_package` | 00-04 | claim map, tables, final reading | `REPORT_READY` |

## Primary Metrics

### MLM / Language Modeling

This is the primary v3.2 proxy task.

Use these as main metrics:

- content-token top-1/top-5/top-10;
- content-token average gold probability;
- content-token pseudoPPL;
- language macro average and worst-language score;
- fixed-mask dev evaluation over multiple seeds.

Use these only as secondary metrics:

- all-token pseudoPPL;
- dynamic MLM dev loss;
- all-token top-k.

### Sentence Retrieval

Use these as main metrics:

- centered-CSLS R@1/R@5/MRR;
- positive-minus-hard-negative margin;
- median rank;
- hubness@10 max and gini;
- source-language and target-language macro breakdown.

Do not claim semantic improvement from raw cosine alone.

### Downstream / Translation

Use these as diagnostic metrics:

- pair-classification macro F1 and AUROC;
- POS token accuracy and macro F1;
- retrieval-only train-bank chrF++ with diversity diagnostics;
- simple decoder chrF++/BLEU plus EOS, empty-output, script-valid, repetition, max-length rate.

## Model Ladder

| Model | Role |
| --- | --- |
| `xlm-roberta-base` | diagnostic baseline only, not direct pseudoPPL comparison for expanded tokenizer |
| `v3.1 fvt/focus/align mlm200` | weak starting checkpoint candidates |
| `v3.2 high-resource-source-augmented MLM` | main MLM adaptation candidate |
| `v3.2 aligned checkpoint` | main semantic retrieval candidate |
| `random/mean` | ablation controls only |

## Minimum V3.2 Pass Gates

`PASS_CONTENT_TOKEN_MLM` requires:

- structured candidate improves content-token average gold probability over `v3.1 fvt/focus/align`;
- `chr/cop/oji` no longer have content-token top-10 all equal to `0`;
- worst-language content-token top-5 improves;
- all-token improvement is not driven only by `▁` or punctuation;
- improvement is obtained under a documented high-resource-source usage policy.

`PASS_SEMANTIC_ALIGNMENT` requires:

- target10 centered-CSLS macro R@1 and MRR improve over `v3.1` MLM-only;
- hard margin becomes less negative or positive;
- `syr` and `cop` source/target macro improve;
- hubness does not worsen materially.

`PASS_DOWNSTREAM_DIAGNOSTIC` requires:

- Coptic-Syriac pair classification does not regress;
- retrieval-only and/or decoder diagnostics improve without collapse;
- claimed improvement is linked to content-token or retrieval gains.

## Recommended Execution Order

1. Freeze v3.1 diagnosis into reusable tables.
2. Run tokenizer/content-token audit focused on `chr/cop/oji/syr`.
3. Decide whether to keep v3.1 append-only tokenizer or add a small append-only repair.
4. Train high-resource-source-augmented, target-aware MLM with checkpoints at `1k`, `5k`, `10k`, `20k`, optionally `50k`.
5. Evaluate fixed-mask content-token MLM at every checkpoint.
6. Run target10 centered-CSLS retrieval at the same checkpoints.
7. Select one MLM checkpoint by content-token plus retrieval tradeoff, not dynamic loss alone.
8. Run contrastive/TLM alignment using `item_id` positives and hard negatives.
9. Re-run retrieval, pair classification, POS, and translation diagnostics.
10. Package claims by gate, not by best-looking single metric.

## Artifact Contract

| Artifact | Stage |
| --- | --- |
| `v31_failure_matrix.tsv` | 00 |
| `metric_contract.md` | 00 |
| `content_token_language_breakdown.tsv` | 00/02 |
| `tokenization_repair_audit.tsv` | 01 |
| `tokenizer_decision.md` | 01 |
| `high_resource_source_manifest.tsv` | 02 |
| `balanced_mlm_training_manifest.tsv` | 02 |
| `balanced_mlm_learning_curves.tsv` | 02 |
| `fixed_mask_content_mlm_scores.tsv` | 02 |
| `pseudoperplexity_content_summary.tsv` | 02 |
| `alignment_training_manifest.tsv` | 03 |
| `target10_centered_csls_scores.tsv` | 03 |
| `target10_language_breakdown.tsv` | 03 |
| `hubness_summary.tsv` | 03 |
| `pair_classification_results.tsv` | 04 |
| `pos_results.tsv` | 04 |
| `translation_diagnostics.tsv` | 04 |
| `claim_evidence_map.md` | 05 |
| `results.md` | each stage |

## Final Claim Routes

| Exit State | Meaning | Allowed Claim |
| --- | --- | --- |
| `PASS_CONTENT_AND_ALIGNMENT` | content-token MLM and retrieval both improve | v3.2 improves target10 language modeling and semantic retrieval diagnostics |
| `PASS_CONTENT_ONLY` | token prediction improves but retrieval remains weak | v3.2 improves intrinsic target-language token adaptation only |
| `PASS_ALIGNMENT_ONLY` | retrieval improves without content-token gain | semantic alignment stage helps retrieval, but lexical modeling remains weak |
| `DOWNSTREAM_ONLY` | task probes improve without clean intrinsic gains | report as task-specific diagnostic, investigate shortcut |
| `FAIL` | no reliable gain | return to data/tokenizer scale redesign |
