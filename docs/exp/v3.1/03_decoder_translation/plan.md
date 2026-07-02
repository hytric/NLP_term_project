# Experiment 3 Plan: Simple Decoder Translation Task

작성일: 2026-06-18

## Goal

Train a small decoder on top of the XLM-R/third_try encoder and evaluate a real translation task.

This is the final downstream task in `v3.1`. Experiments 1 and 2 test whether the embedding space is aligned and useful as frozen features. Experiment 3 asks whether a simple decoder can use that encoder space to produce translations.

## Scope

Main translation setting:

| Direction | Status |
| --- | --- |
| `cop -> syr` | primary if parallel data is sufficient |
| `syr -> cop` | primary if parallel data is sufficient |
| `eng -> target10` / `target10 -> eng` | fallback broad evaluation if Coptic-Syriac data is too sparse |
| target-target Bible directions | optional matrix evaluation |

The main claim remains low-resource encoder adaptation. The decoder is intentionally simple so it tests encoder usability rather than becoming a large independent NMT system.

## Architecture

Default model:

| Component | Setting |
| --- | --- |
| encoder | XLM-R-base or third_try/v3.1 encoder checkpoint |
| encoder update | frozen in first pass; optional unfreeze as ablation |
| decoder | small Transformer decoder, 1-2 layers |
| decoder hidden size | match encoder hidden size, or use projection |
| attention | cross-attention over encoder states |
| output vocab | append-only expanded tokenizer vocab |
| training objective | teacher-forced autoregressive cross-entropy |

Why simple decoder:

1. It directly tests whether the encoder states contain usable cross-lingual semantic information.
2. It avoids confusing the result with a large seq2seq model's capacity.
3. It keeps the project aligned with XLM-R encoder evaluation.

## Tokenizer Constraint

The decoder must use the same append-only tokenizer protocol as the encoder.

Required:

1. Train auxiliary tokenizer on low-resource + high-resource text.
2. Keep the original XLM-R tokenizer intact.
3. Append only new pieces after the original vocab.
4. Preserve all existing token ids and special ids.
5. Initialize only new rows.
6. Record `append_only_merge_report.tsv` and id-preservation audit.

Forbidden:

- replacing the XLM-R tokenizer with a newly trained tokenizer;
- reindexing old tokens;
- training decoder with a tokenizer that cannot be mapped back to the expanded model vocab.

## Data

| Data | Use |
| --- | --- |
| Coptic-Syriac aligned Bible / sentence pairs | primary translation train/dev/test |
| English-target Bible pairs | fallback broad target10 translation evaluation |
| high-resource parallel/control pairs | sanity and control |
| target10 monolingual text | tokenizer/MLM only, not direct supervised translation labels |

Split:

- freeze train/dev/test by book or chapter group;
- avoid random verse-level leakage;
- use dev for early stopping and checkpoint selection;
- touch test once.

## Training Plan

Stage A: decoder-only probe

| Item | Setting |
| --- | --- |
| encoder | frozen |
| trainable params | decoder + output projection, optionally target embeddings |
| purpose | test whether encoder representation is already usable |

Stage B: light unfreeze ablation

| Item | Setting |
| --- | --- |
| encoder | unfreeze top 1-2 layers or LoRA adapters |
| purpose | check whether small adaptation improves translation |
| status | ablation, not main unless predeclared |

Stage C: retrieval-augmented diagnostic

| Item | Setting |
| --- | --- |
| retrieval | use Experiment 1 nearest neighbors |
| purpose | compare decoder generation against retrieval-only translation proxy |
| status | diagnostic/control |

## Metrics

Quantitative:

| Metric | Use |
| --- | --- |
| chrF++ | primary generation metric for low-resource/morphologically rich text |
| BLEU / sacreBLEU | secondary, report with signature |
| exact verse retrieval upper bound | compare with retrieval-only baseline |
| COMET or learned metric | optional only if language support is credible |
| length ratio | detect copying/truncation |
| copy rate | detect source copying |
| script validity | detect invalid script output |

Qualitative:

- 20-50 held-out examples;
- source, gold target, model output, retrieval nearest neighbor;
- error tags: copy, hallucination, wrong script, partial phrase, semantically close, word-order error.

## Baselines

| Baseline | Purpose |
| --- | --- |
| XLM-R-base encoder + same decoder | mandatory baseline |
| retrieval-only nearest neighbor | strong non-generative baseline |
| dictionary / identity-copy baseline | catches copy shortcuts |
| v3 replay-safe encoder + decoder | diagnostic candidate |
| future v3.1 encoder + decoder | main candidate |

The decoder architecture and training schedule must be identical when comparing encoders.

## Gate

`PASS_DECODER_TRANSLATION_READY` requires:

1. XLM-R-base encoder + simple decoder baseline is run.
2. Candidate encoder + identical decoder setup improves chrF++ and at least one retrieval/semantic metric.
3. BLEU/chrF++ are reported on a held-out test set.
4. Qualitative examples are included.
5. Copy/script validity diagnostics do not show collapse.
6. Coptic and Syriac directions are explicitly reported if they are the claimed translation pair.
7. If only English-target fallback pairs are available, the claim is broad target10 translation proxy, not Coptic-Syriac NMT.

Failure labels:

| Label | Meaning |
| --- | --- |
| `FAIL_DECODER_COPY` | decoder copies source or retrieval text |
| `FAIL_SCRIPT_VALIDITY` | output script invalid for target language |
| `FAIL_NO_BASELINE_GAIN` | candidate does not beat XLM-R-base encoder |
| `FAIL_DATA_SPARSE` | supervised pair data insufficient for claimed direction |
| `DIAGNOSTIC_RETRIEVAL_BETTER` | retrieval beats generation; report decoder as weak |

## Outputs

| Artifact | Path |
| --- | --- |
| translation data manifest | `translation_data_manifest.tsv` |
| decoder config | `decoder_config.json` |
| tokenizer merge report | `append_only_merge_report.tsv` |
| id preservation audit | `id_preservation_audit.tsv` |
| training curves | `decoder_training_curves.tsv` |
| checkpoint selection | `checkpoint_selection.md` |
| translation metrics | `translation_results.tsv` |
| copy/script diagnostics | `translation_diagnostics.tsv` |
| qualitative examples | `sample_translations.md` |
| summary | `results.md` |

## Claim Boundary

Allowed if gate passes:

> A simple decoder trained on top of the adapted encoder improves held-out low-resource translation metrics over the same decoder trained on XLM-R-base encoder states.

Not allowed:

> The encoder alone is a full NMT system.

> The tokenizer change alone explains translation improvement.

> A decoder trained with a replaced tokenizer preserves pretrained XLM-R behavior.

> Retrieval proxy success proves free-form translation success.

