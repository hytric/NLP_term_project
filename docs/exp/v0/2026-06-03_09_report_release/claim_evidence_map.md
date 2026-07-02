# Claim Evidence Map

작성일: 2026-06-04

This file maps paper/report claims to current evidence files.
Use it as the audit table before writing final prose.

## Claim Status Legend

| Status | Meaning |
| --- | --- |
| Strong | Supported by direct metrics and/or controlled comparisons |
| Moderate | Supported, but needs careful wording or qualitative caveats |
| Weak | Preliminary, diagnostic, or negative-only evidence |
| Do not claim | Not supported by current evidence |

## Evidence Map

| Claim | Status | Evidence | Notes |
| --- | --- | --- | --- |
| The experiment uses a fixed 10-language low-resource target set. | Strong | `data/processed/target10/target_languages.tsv`, `docs/exp/2026-06-03_01_data_and_splits/results.md` | Scope is exactly target10, not a broad benchmark. |
| Glot500 overfragments several target10 scripts. | Strong | `docs/exp/2026-06-03_02_tokenization_audit/target10_tokenization_metrics.tsv`, `results.md` | Especially Coptic, Syriac, Cherokee, Ojibwa. |
| NLLB has high `<unk>` rates for some unsupported scripts. | Strong | `docs/exp/2026-06-03_02_tokenization_audit/target10_tokenization_metrics.tsv` | Coptic/Syriac/Cherokee/Ojibwa show the clearest issue. |
| The merged target10 tokenizer reduces tokens per word for target scripts. | Strong | `docs/exp/2026-06-03_03_vocab_extension/glot500_target10_merged_metrics.tsv`, `results.md` | Syriac and Coptic improve by about two thirds. |
| Mean embedding initialization is better than Random in the 10k MLM pilot. | Strong | `docs/exp/2026-06-03_05_mlm_adaptation/mlm_pilot10k_results.tsv`, `results.md` | Use stable fp32 bsz16 re-eval, not built-in bsz2 NaN eval. |
| Mean pilot10k is the selected downstream checkpoint. | Strong | `docs/exp/2026-06-03_05_mlm_adaptation/checkpoint_selection.md`, `results.md` | Selected for NMT diagnostics. |
| Direct Coptic/Syriac NMT runs end-to-end. | Strong | `docs/exp/2026-06-03_06_nmt_baselines/results.md`, run summaries under `docs/exp/2026-06-03_06_nmt_baselines/` | Pipeline passes train/eval/decode/metrics. |
| Direct NMT is not a usable translator yet. | Strong | `docs/exp/2026-06-03_06_nmt_baselines/results.md`, `docs/exp/2026-06-03_08_evaluation_analysis/qualitative_analysis.md` | Output is repetitive and low-BLEU. |
| Retrieval is a strong non-neural baseline. | Strong | `docs/exp/2026-06-03_06_nmt_baselines/retrieval_char345_eng_to_cop/run_summary.json`, `retrieval_char345_syr_to_cop/run_summary.json`, `results.md` | Full-test chrF++ around 22. |
| Top-k retrieval has reranking headroom. | Strong | `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_oracle_eng_to_cop_char345_k8/run_summary.json`, `summary.md` | Top1 22.5362 vs oracle@8 28.3327. |
| Feature reranking improves full-test top1 retrieval. | Moderate | `docs/exp/2026-06-03_06_nmt_baselines/retrieval_topk_feature_reranker_eng_to_cop_char345_k8/run_summary.json`, `summary.md` | Improves to 24.5921 but remains below oracle. |
| Source-candidate selection still has headroom after feature reranking. | Strong | `docs/exp/2026-06-04_10_source_grounding_editing/source_candidate_summary.md`, `source_candidate_diagnostics.tsv` | 10A shows oracle@8 is often not rank 1 and feature selection remains below oracle. |
| A CPU-only candidate decision selector slightly improves retrieval selection. | Moderate | `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_summary.md`, `candidate_decision_results.tsv` | 10B reaches corpus chrF++ 24.6862 vs existing feature reranker 24.5921; improvement is small. |
| Pairwise CPU candidate selection is the current best retrieval selector. | Moderate | `docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_summary.md`, `pairwise_selector_results.tsv` | Pairwise logistic selector reaches corpus chrF++ 24.7438; improvement over pointwise 10B is small. |
| Retrieval-augmented neural generation improves overlap. | Moderate | `docs/exp/2026-06-03_06_nmt_baselines/results.md`, `final_metrics.tsv` | True on the 64-slice, but copy-heavy. |
| Retrieval-augmented neural generation is source-grounded translation. | Do not claim | `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_results.tsv`, `retrieval_edit_controls.md`, wrong-retrieval/retrieved-only/source-only controls in `results.md` and `error_taxonomy.md` | Same-checkpoint 10C controls contradict this claim: source-only 0.2729, retrieved-only 18.6220, correct source+retrieval 18.3574. |
| Greek pivot/back-translation is ready to scale. | Do not claim | `docs/exp/2026-06-03_07_pivot_backtranslation/results.md` | Gate failed; Greek -> Coptic emits no Coptic. |
| Back-translation improves Coptic/Syriac translation. | Do not claim | no successful synthetic-data condition yet | 07 is a negative gate, not a BT success. |
| Vocabulary extension alone solves downstream translation. | Do not claim | NMT and pivot results contradict this | Representation helps, generation remains unsolved. |
| chrF++ alone is sufficient evidence of translation quality. | Do not claim | `error_taxonomy.md`, qualitative analysis | chrF++ can be inflated by repetition/copying. |

## Recommended Claim Wording

Use:

- "The target10 tokenizer extension substantially reduces overfragmentation."
- "Mean initialization is more stable in our target10 MLM pilot."
- "Direct neural Coptic/Syriac translation remains a diagnostic failure under current settings."
- "Retrieval is a strong baseline and useful signal, but current neural retrieval augmentation is copy-heavy."
- "Lightweight source-candidate selectors slightly improve retrieval selection, with pairwise selection currently best, but oracle@8 shows substantial remaining reranking headroom."
- "Same-checkpoint 10C controls show that the current neural edit gate is retrieval-sensitive but not source-grounded enough: retrieved-only slightly beats correct source+retrieval, and source-only collapses."

Avoid:

- "We solve Coptic/Syriac translation."
- "Back-translation improves translation."
- "Retrieval-augmented generation is source-grounded."
- "High chrF++ means adequate translation."
