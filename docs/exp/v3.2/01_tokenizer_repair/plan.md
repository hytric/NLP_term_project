# Stage 01: Tokenizer Repair

작성일: 2026-06-19

## Goal

Decide whether the v3.1 append-only tokenizer is sufficient for v3.2, or whether a small append-only repair is needed for `chr/cop/oji/syr`.

The repair must preserve the central rule:

> Never reindex existing XLM-R tokens. Only append new pieces.

## Problem

In v3.1, the tokenizer audit passed structurally, but content-token evaluation still failed for several scripts.

Examples:

- `chr`, `cop`, and `oji` have structured-init content-token top-10 near `0`.
- `xlmr_base` pseudoPPL is degenerate because several scripts collapse to `▁` and punctuation.
- expanded-tokenizer variants still have high standalone `▁` rates, so all-token metrics remain contaminated.

## Candidate Actions

| Option | Description | Risk | Use If |
| --- | --- | --- | --- |
| keep v3.1 tokenizer | no tokenizer change; only change sampling/training | lowest risk | content coverage is adequate after audit |
| append-only script repair | train tiny additional pieces for weak scripts and append them | moderate | `chr/cop/oji/syr` content tokens are fragmented or missing |
| normalization-only repair | fix Unicode normalization before training/eval | moderate | audit finds inconsistent combining marks or script variants |
| full tokenizer redo | rejected for v3.2 main route | high | only if append-only repair cannot represent target scripts |

## Required Audits

1. Token distribution by language.
2. Standalone `▁` rate by language.
3. Content-token length distribution.
4. Added-token hit rate on target10 train/dev.
5. Script-specific unknown/fragment pattern examples.
6. Unicode normalization check for combining marks.

## Required Outputs

| Artifact | Purpose |
| --- | --- |
| `tokenization_repair_audit.tsv` | per-language tokenization diagnostics |
| `weak_script_examples.md` | examples for `chr/cop/oji/syr` |
| `append_only_repair_report.tsv` | if repair is applied |
| `tokenizer_decision.md` | final keep/repair decision |

## Exit Gate

`PASS_TOKENIZER_REPAIR_READY` if:

- no base token ids or special token ids change;
- weak-script content-token coverage improves;
- standalone `▁` dominance does not worsen;
- tokenization examples are inspected for `chr/cop/oji/syr`.

`KEEP_V31_TOKENIZER` if:

- audit shows representation is sufficient and the main bottleneck is training scale/objective.

