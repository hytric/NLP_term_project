# v5 Final Report Section Draft

Last updated: 2026-06-27

This file contains prose blocks that can be moved into `../../Report.md` once
the remaining MLM and downstream results are measured.

## Abstract Draft

We reproduce the Glot500 training and evaluation pattern on a controlled
102-language-script setting consisting of 92 XLM-R-seen Glot500 languages and
10 diverse Glot500-internal target languages. The experiment preserves the
Glot500-style SentencePiece vocabulary extension, continued MLM pretraining,
and downstream metric families, while intentionally limiting the language set
and compute scale. Our main novelty is not a new corpus, but a comparison of
initialization policies for newly appended vocabulary rows. Before continued
training, source-token decomposition initialization substantially reduces MLM
proxy loss compared with random resize and global mean initialization,
especially on the target language group. Final downstream claims remain
conditional on matched MLM checkpoints and available task coverage.

## Main Claim Boundary

Allowed claim:

```text
We reproduce the Glot500-style pipeline on a controlled 102-language subset and
show that embedding initialization for appended vocabulary rows is a measurable
source of early adaptation quality.
```

Disallowed claim:

```text
We fully reproduce Glot500 at 511-language scale or prove target10 downstream
improvement across all Glot500 tasks.
```

Reason:

The v5 target10 has raw text for tokenization and PPPL, but current downstream
task flags do not cover those 10 language-scripts for Tatoeba, Bible, NER, POS,
or roundtrip alignment. Downstream replay should therefore be reported over
available languages with explicit coverage tables.

## Method Paragraph Draft

The v5 tokenizer follows the Glot500-style SentencePiece append procedure. We
train an auxiliary tokenizer on the controlled mixed corpus and append pieces
that are absent from the original XLM-R SentencePiece model. Because this
procedure can move special-token ids, all initialized checkpoints copy source
rows by token identity rather than by id prefix and explicitly remap the
source `<mask>` row to the target `<mask>` id. We compare random resize,
global/source mean initialization, and source-token decomposition
initialization. The source-token decomposition method initializes each new
lexical piece by tokenizing its surface form with the source tokenizer and
averaging the corresponding source embeddings; byte rows and fallback rows are
reported separately.

## Current Result Paragraph Draft

The full v5 merge produced 92,452,251 lines from 102 language-scripts with no
missing language directories. The main tokenizer contains 368,687 tokens,
adding 118,685 token strings over XLM-R. Tokenizer audit passed without
structural failures and improved token fertility for 29 of 30 audited
languages. For the target10 group, 9 of 10 languages improved; `dzo_Tibt`
remained a documented exception, worsening from 4.223938 to 5.552124
tokens/word. This failure is not driven by `<unk>` or byte fallback, but by the
behavior of newly appended Tibetan pieces.

Before continued MLM training, initialization differences are large. On the
v5-target group, FVT achieves weighted NLL 8.785518, compared with 18.411756
for random resize and 11.953142 for mean initialization. This corresponds to
FVT deltas of -9.626238 versus random and -3.167624 versus mean. Because these
are zero-step intrinsic results, they support the novelty hypothesis but do
not replace matched after-MLM and downstream evaluation.

Current baseline evaluation also establishes the reference scale for the final
comparison. On PPPL, XLM-R-base obtains target 61.980216, head 8.117338, and
all-language 9.986271, while the external Glot500-base reference obtains target
15.102934, head 10.213100, and all-language 10.640353. On Tatoeba retrieval,
XLM-R-base reaches head Top-10 accuracy 0.656309 and all-available Top-10
accuracy 0.566067; Glot500-base reaches 0.743755 and 0.706649 respectively.
On Bible retrieval, the materialized available-language set covers 74/102
language-scripts and 0/10 selected targets. XLM-R-base reaches Top-10 accuracy
0.381153, while Glot500-base reaches 0.509356. These Bible rows are therefore
available-language reference evidence, not target10 downstream evidence.
Roundtrip alignment is also retained over the same available 74-language local
set. XLM-R-base reaches accuracy 0.185300, while Glot500-base reaches 0.205189.
As with Bible retrieval, these rows establish available-language
baseline/reference behavior and wait for matched `v5_random` and `v5_fvt`
checkpoints before they can support a method comparison.
The local Taxi1500 text-classification baseline for XLM-R-base reaches macro-F1
0.592876 and accuracy 0.729730. The Glot500-base external reference reaches
macro-F1 0.743338 and accuracy 0.756757. These rows are baseline/reference
evidence, not yet the v5 method comparison, because matched `v5_random` and
`v5_fvt` checkpoints are still pending.

The XLM-R NER baseline is parsed by aggregation: all-available F1 is
0.549858, head F1 is 0.621207, and the v5-target actual evaluated intersection
is 0.459364 for `fur_Latn` only. The Glot500-base NER reference is also parsed:
all-available F1 is 0.627108, head F1 is 0.645915, and the v5-target actual
evaluated intersection is 0.553191 for `fur_Latn` only. The POS baselines are
also parsed under the local `TRAIN_LANGS=tur_Latn` condition: XLM-R-base
obtains all-available F1 0.481336 and head F1 0.571446, while Glot500-base
obtains all-available F1 0.567542 and head F1 0.573832.

## Limitations Paragraph Draft

This experiment is intentionally a controlled replay rather than a full-scale
Glot500 reproduction. It uses 102 language-scripts and a smaller compute budget,
so `cis-lmu/glot500-base` should be treated as an external reference rather
than an equal-budget baseline. Downstream coverage is also uneven: the selected
target10 is fully available for raw-text PPPL but not for the currently
materialized downstream task lists. We therefore separate intrinsic target10
evidence from downstream available-language evidence and report exclusions
explicitly.

## Remaining Insertions

- matched `v5_random` and `v5_fvt` 10K checkpoint metrics
- training curve summary
- PPPL for `v5_random` and `v5_fvt`
- remaining available-language downstream results for `v5_random` and
  `v5_fvt`
- final aggregation table from `../00_tables/` and `../../3_evaluation/09_aggregation/`

## Current Figure Insertions

- Experiment pipeline:
  `../01_figures/generated/figure_01_experiment_pipeline.png`
- Tokenizer fertility:
  `../01_figures/generated/figure_02_tokenizer_fertility_delta.png`
- Zero-step initialization:
  `../01_figures/generated/figure_03_zero_step_initialization.png`
- Evaluation coverage:
  `../01_figures/generated/figure_05_evaluation_coverage.png`

Use captions from `../01_figures/generated/captions.md`.
