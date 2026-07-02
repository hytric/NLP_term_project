# Plan: Evaluation And Analysis

Status: metrics, paper tables, tokenization figure, qualitative analysis, and error taxonomy drafted

## Goal

Turn experiment outputs into paper-ready evidence: tables, figures, and qualitative analysis.

## Required Analyses

- tokenization audit table
- vocabulary extension table
- embedding initialization ablation table
- NMT BLEU/chrF++ table
- qualitative translation examples
- error taxonomy
- limitations and failure cases

## Planned Work

1. Standardize metric computation with sacrebleu.
2. Record sacrebleu signature.
3. Build result tables by direction.
4. Plot tokenization metrics and loss curves.
5. Select qualitative examples.
6. Categorize errors:
   - untranslated source fragments
   - wrong named entities
   - morphology/script errors
   - overliteral pivot artifacts
   - hallucinated religious formulae
7. Connect tokenizer metrics to NMT metrics.

## Metrics

- BLEU
- chrF++
- tokenization fertility
- single-character token ratio
- loss and pseudo-perplexity
- qualitative adequacy and fluency notes

## Outputs

- `final_metrics.tsv`
- `paper_tables.md`
- `paper_figures.md`
- `qualitative_analysis.md`
- `error_taxonomy.md`

## Success Gate

This phase passes when all claims in the paper have direct evidence.

## Decision Rule

Any claim without a metric, table, example, or explicit source note should be downgraded to speculation or future work.
