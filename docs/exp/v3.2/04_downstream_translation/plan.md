# Stage 04: Downstream And Translation Diagnostics

작성일: 2026-06-19

## Goal

Check whether Stage 02/03 improvements transfer to usable downstream signals.

This stage is diagnostic. It should not overrule failed content-token or retrieval gates unless the shortcut risk is explicitly explained.

## Tasks

| Task | Purpose | Main Metric |
| --- | --- | --- |
| Coptic-Syriac pair classification | does frozen representation separate same verse from hard negatives? | macro F1, AUROC |
| target10 pair classification | does the signal generalize beyond Coptic-Syriac? | macro F1, AUROC |
| Coptic POS | does token-level syntactic signal improve? | token accuracy, macro F1 |
| retrieval-only translation | does retrieval quality improve without decoder confounds? | chrF++, diversity, same-item audit |
| simple decoder | does generation avoid collapse and improve quality? | chrF++, BLEU, EOS/script/repetition diagnostics |

## Baselines

Compare:

1. `xlm-roberta-base` diagnostic baseline;
2. `v3.1` best available checkpoint;
3. Stage 02 MLM-only checkpoint;
4. Stage 03 aligned checkpoint.

## Interpretation Rules

Allowed:

> Downstream probe improves in parallel with content-token and/or retrieval metrics.

Risky:

> Decoder chrF++ improves while retrieval and content-token metrics remain weak.

Forbidden:

> Translation quality is solved because script validity or chrF++ improves from a collapsed baseline.

## Required Outputs

| Artifact | Purpose |
| --- | --- |
| `downstream_task_manifest.tsv` | task/run metadata |
| `pair_classification_results.tsv` | Coptic-Syriac and target10 pair results |
| `pos_results.tsv` | POS results |
| `retrieval_translation_results.tsv` | retrieval-only baseline |
| `decoder_translation_results.tsv` | simple decoder scores |
| `translation_diagnostics.tsv` | EOS/script/empty/repetition/length diagnostics |
| `downstream_interpretation.md` | claim boundary |

## Exit Gate

`PASS_DOWNSTREAM_DIAGNOSTIC` if:

- pair classification does not regress and preferably improves;
- retrieval-only translation improves without diversity collapse;
- decoder does not regress on EOS/script/empty diagnostics;
- any claimed downstream gain is linked to Stage 02 or Stage 03 metric gains.

