# Reproducing Glot500 on a Controlled 102-Language Setting with Vocabulary-Extension Initialization

Status: execution draft, refreshed 2026-06-28.

This draft is written as a paper-style report. Unresolved result slots must be
filled only from measured artifacts in `docs/exp/v5/3_evaluation/09_aggregation/`
or from explicit blocker/status notes.
Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`docs/exp/v5/4_reporting/final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
draft header.

## Abstract

We reproduce the core Glot500 training and evaluation pattern on a controlled
102-language-script setting composed of 92 XLM-R-seen Glot500 language-scripts
and 10 diverse Glot500-internal target language-scripts. The experiment keeps
the Glot500-style corpus merge, SentencePiece vocabulary expansion, continued
MLM pretraining, and downstream metric families, while intentionally reducing
the language and compute scale. Our novelty is a focused comparison of
initialization policies for newly appended vocabulary rows. In addition to the
standard random resize baseline, we evaluate mean initialization and
source-token decomposition initialization, which initializes a new token by
averaging source embeddings obtained from the original tokenizer decomposition
of that token surface. Before continued MLM, source-token decomposition
substantially reduces target MLM proxy loss compared with random resize. Final
after-MLM and downstream transfer claims remain conditional on matched
`v5_random` and `v5_fvt` checkpoints and on available downstream task coverage.

## 1. Introduction

Multilingual language models such as XLM-R cover many languages, but their
tokenization and representation quality remain uneven across language, script,
and resource level. Glot500 addresses this limitation by scaling multilingual
corpora and continued pretraining to more than 500 languages. Reproducing the
full Glot500 experiment is expensive, but its experimental pattern can be
studied in a controlled subset.

This report focuses on a 102-language-script replay. The head group consists
of 92 local Glot500 language-scripts that are seen by XLM-R. The target group
consists of 10 language-scripts selected from Glot500 raw data that are not
XLM-R seen and have at least 30,000 rows. This setting lets us ask two linked
questions. First, can we faithfully execute the Glot500-style tokenizer,
continued pretraining, and metric pipeline in a controlled setting? Second,
when the tokenizer is expanded, does the initialization of newly appended
embedding rows affect early adaptation quality?

The contribution is therefore not a new corpus. It is an experiment design
that separates Glot500-style reproduction from a vocabulary-extension
initialization novelty. The current strongest measured evidence is intrinsic:
source-token decomposition initialization improves zero-step target MLM proxy
loss over random and mean initialization while preserving source rows,
special-token behavior, byte-row accounting, and LM-head tying.

### 1.1 Contributions

This report makes three bounded contributions.

First, it builds an artifact-audited controlled replay package for the
Glot500-style pipeline over 92 XLM-R-seen language-scripts and 10
Glot500-internal target language-scripts. The package ties together corpus
merge evidence, SentencePiece append-style tokenizer expansion, continued MLM
handoff, metric-family coverage, and claim-freeze audits, while explicitly
rejecting a full-scale 511-language reproduction claim.

Second, it isolates vocabulary-row initialization as the method novelty. The
source-token decomposition initializer preserves source row identity, remaps
`<mask>` by token identity, accounts for byte and fallback rows, keeps the LM
head tied, and lowers zero-step target weighted NLL relative to random resize.

Third, it keeps the Glot500 downstream metric families in the protocol rather
than dropping coverage-limited tasks. PPPL, retrieval, classification, tagging,
and Roundtrip alignment are all routed through aggregation, insertion, and
claim-promotion gates; target10 downstream gaps remain visible limitations
until measured task coverage exists.

## 2. Related Work And Positioning

Glot500 is the reproduction target for this experiment. The original Glot500
paper scales multilingual corpus construction and continued pretraining to more
than 500 languages, and its evaluation surface motivates the v5 requirement to
retain PPPL, retrieval, classification, tagging, and roundtrip-style metric
families. In v5, this citation supports the experimental pattern, not a claim
that the full 511-language training scale has been rerun. The local evidence
for the subset replay is instead the 92+10 merge report, tokenizer audit,
metric mapping, and coverage tables.

Yamaguchi et al. study low-resource continued vocabulary expansion and motivate
the broader question of how newly introduced vocabulary rows should be handled.
In this report, `Yamaguchi-style` refers to that inspiration and to the earlier
add-token route used in prior attempts. The main v5 tokenizer is deliberately
different: it follows the Glot500-style SentencePiece append route. The novelty
claim is therefore narrower and local to v5: after appending vocabulary rows,
we compare initialization policies for those rows, with source-token
decomposition as the main method candidate.

The citation boundary is maintained in:

```text
docs/exp/v5/4_reporting/03_final_report/citation_source_map.md
```

## 3. Scope And Reproduction Boundary

The allowed reproduction claim is:

```text
We reproduce the Glot500-style training/evaluation pattern on a controlled
102-language subset.
```

The disallowed claim is:

```text
We fully reproduce the original 511-language Glot500 experiment.
```

This distinction is important. The v5 run keeps the experimental logic of
Glot500, including SentencePiece append-style vocabulary expansion, continued
MLM pretraining, head/tail/all reporting, and the retained metric families.
However, it uses a smaller language set and a smaller compute budget.
`cis-lmu/glot500-base` is therefore an external reference model, not an
equal-budget baseline.

The detailed fidelity matrix is maintained in:

```text
docs/exp/v5/4_reporting/00_tables/table_15_glot500_reproduction_fidelity.md
```

The overview pipeline figure is:

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_01_experiment_pipeline.png
```

The short interpretation is that v5 is faithful at the level of experimental
logic: Glot500-internal data, tokenizer expansion, continued MLM, required
metric-family accounting, and head/tail/all-style reporting. It is intentionally
not faithful at the level of full language scale or original compute budget.

## 4. Data

The v5 corpus contains 92 head language-scripts and 10 target language-scripts.
The target group is selected from Glot500 raw data with the following criteria:
not XLM-R seen, `new_length >= 30000`, local raw directory available, and
regional/script diversity.

Target10:

```text
fur_Latn
krc_Cyrl
acm_Arab
dzo_Tibt
sat_Olck
mad_Latn
bam_Latn
kjb_Latn
quw_Latn
rap_Latn
```

The full merge completed successfully.

| Item | Value |
| --- | ---: |
| head language-scripts | 92 |
| target language-scripts | 10 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 363,421 |
| planned total samples | 92,452,251 |
| actual total samples | 92,452,251 |
| missing language dirs | 0 |
| merged file size | 19G |

Primary artifacts:

- corpus:
  `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt`
- manifest:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- report:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`

## 5. Tokenizer Expansion

The main tokenizer follows the Glot500-style SentencePiece append route. An
auxiliary SentencePiece tokenizer is trained on the controlled mixed corpus.
Pieces that are absent from the original XLM-R SentencePiece model are
appended to the base model.

This differs from the earlier Yamaguchi-style add-token route used in prior
experiments. The add-token route preserves existing tokenizer ids more
directly, while the Glot500-style append route is closer to the target
reproduction method but requires explicit special-token auditing. In v5,
`<mask>` moves from source id `250001` to target id `368686`, so model rows
must be copied by token identity rather than by id prefix.

Tokenizer result:

| Item | Value |
| --- | ---: |
| base vocab size | 250,002 |
| extended vocab size | 368,687 |
| appended token count | 118,685 |
| byte fallback rows | 256 |
| source `<mask>` id | 250001 |
| target `<mask>` id | 368686 |
| audited languages improved | 29/30 |
| target10 improved | 9/10 |

The main tokenizer reduced tokens per word for most audited languages. The
main caveat is `dzo_Tibt`, which worsened from 4.223938 to 5.552124
tokens/word. The regression is not explained by `<unk>` or byte fallback. It
appears to be a score-calibration/fertility issue where newly appended Tibetan
pieces can outcompete useful original pieces.

## 6. Embedding Initialization

We compare three initialized checkpoint families:

| Method | Description | Role |
| --- | --- | --- |
| `random` | Hugging Face resize with random new rows | Glot500-style baseline |
| `mean` | source/global mean initialization | simple stable ablation |
| `fvt` | source-token decomposition mean | main novelty candidate |

For all non-random checkpoints, source rows are copied by token identity. The
source `<mask>` row is explicitly remapped to the target `<mask>` id. Byte rows
and fallback rows are counted separately, and input embeddings and LM head are
checked for consistency.

Main FVT initialization audit:

| Audit item | Value |
| --- | ---: |
| source identity rows copied | 250,002 |
| new token rows | 118,685 |
| FVT-initialized rows | 118,427 |
| byte/global-mean rows | 256 |
| global mean lexical fallback rows | 2 |
| `<mask>` max absolute diff | 0.0 |
| LM head tied | true |

## 7. Continued MLM Pretraining

The main after-training comparison requires matched `v5_random` and `v5_fvt`
checkpoints. The paired launcher trains `v5_random_mlm_10k` first and then
`v5_fvt_mlm_10k` with the same corpus, tokenizer, schedule, seed family, and
checkpoint interval.

Current live state is recorded in:

```text
docs/exp/v5/3_evaluation/running_status.md
```

At the current check, `v5_random_mlm_10k` has produced the selected 10K
checkpoint, while `v5_fvt_mlm_10k` is still running and has not yet produced a
model file. This live status is not a result claim, and post-checkpoint
evaluation remains locked until both rows report `ready_for_wrapper=yes` and
`post_checkpoint_preflight.md` reports `post_checkpoint_preflight_ready_to_launch`.

| Setting | Value |
| --- | --- |
| base model | `xlm-roberta-base` |
| tokenizer | v5 extended tokenizer |
| objective | MLM |
| max length | 512 |
| learning rate | 5e-5 |
| max steps | 10,000 |
| checkpoint interval | 10,000 |
| primary comparison | `v5_random` vs `v5_fvt` |

## 8. Evaluation Setup

All Glot500 metric families are retained as required evaluation targets.
Coverage limitations are recorded rather than silently dropping a metric.

| Metric | Score | Current coverage | Current status |
| --- | --- | ---: | --- |
| PPPL / MLM proxy | weighted PPPL | 102/102, target10 10/10 | XLM-R, Glot500-base, and v5-random rows measured; FVT waiting |
| Tatoeba retrieval | Top-10 accuracy | 63/102, target10 0/10 | XLM-R, Glot500-base, and v5-random rows measured; FVT waiting |
| Bible retrieval | Top-10 accuracy | 74/102, target10 0/10 | XLM-R, Glot500-base, and v5-random rows measured; FVT waiting |
| Text classification | macro-F1 | 1/102, target10 0/10 | XLM-R, Glot500-base, and v5-random rows measured; FVT waiting |
| NER | F1 | 78/102 materialized coverage, target10 0/10; actual runner includes `fur_Latn` | XLM-R baseline, Glot500-base reference, and v5-random rows measured; FVT waiting |
| POS | F1 | 58/102, target10 0/10 | XLM-R baseline, Glot500-base reference, and v5-random rows measured with `TRAIN_LANGS=tur_Latn`; FVT waiting |
| Roundtrip alignment | accuracy | 74/102, target10 0/10 | XLM-R, Glot500-base, and v5-random rows measured; FVT waiting |

The target10 coverage boundary is central to interpretation. Target10 claims
should focus on tokenization, zero-step initialization diagnostics, and
after-MLM PPPL unless target10 downstream task data is later materialized.
Downstream results should be reported over available languages with explicit
head/all and coverage notes.

For final assembly, the metric-by-metric fidelity boundary is also summarized
in `00_tables/table_13_metric_fidelity_matrix.md`. This table is the canonical
bridge between the reproduction claim and the local execution state: each
Glot500 metric family is either measured for the relevant model columns,
waiting on matched v5 checkpoints, coverage-limited, or explicitly blocked.

### 8.1 Glot500 Fidelity Map

The experiment is designed as a faithful subset replay rather than a scale
match. Each Glot500 component is retained where local data and inherited
runners make it executable; otherwise the missing component is kept as an
explicit blocked metric instead of being removed from the protocol.

| Glot500 component | v5 implementation | Evidence | Status |
| --- | --- | --- | --- |
| multilingual corpus construction | 92 XLM-R-seen Glot500 language-scripts + 10 Glot500-internal target language-scripts | merge report has `92,452,251` actual samples and `0` missing dirs | complete |
| SentencePiece vocabulary expansion | auxiliary SPM pieces appended to XLM-R SPM | extended vocab `368,687`, appended rows `118,685` | complete |
| continued MLM pretraining | paired `v5_random` then `v5_fvt` 10K run | launcher active on GPUs `2,3` | in progress |
| intrinsic PPPL / MLM proxy | wrapper and aggregation over 102 language-scripts | `xlmr_base`, `glot500_base`, and `v5_random` rows measured | partial, FVT row pending checkpoint |
| sentence retrieval | Tatoeba runner retained | `xlmr_base`, `glot500_base`, and `v5_random` rows measured over available languages | partial, FVT row pending checkpoint |
| text classification | Taxi1500 runner retained | `xlmr_base`, `glot500_base`, and `v5_random` rows measured on local English split | partial, coverage-limited, FVT row pending checkpoint |
| sequence tagging | NER and POS runners retained | NER `xlmr_base`/`glot500_base`/`v5_random` measured; POS `xlmr_base`/`glot500_base`/`v5_random` measured with `TRAIN_LANGS=tur_Latn` | partial, FVT rows pending checkpoint |
| Bible retrieval | metric family retained | 74/102 local parallel data materialized; XLM-R Top-10 `0.381153`, Glot500-base Top-10 `0.509356`, v5-random Top-10 `0.328019` | partial, FVT row pending checkpoint |
| roundtrip alignment | metric family retained | Bible-derived input set and v5 runner materialized; XLM-R accuracy `0.185300`; Glot500-base accuracy `0.205189`; v5-random accuracy `0.190300` | partial, FVT row pending checkpoint |

This map is the basis for final wording. It supports a claim of Glot500-style
experimental fidelity on a controlled subset, but not a claim of full-scale
Glot500 reproduction.

### 8.2 Result Promotion Rules

The report separates four evidence levels:

| Evidence level | Can appear in final tables? | Example | Allowed wording |
| --- | --- | --- | --- |
| audited artifact | yes | merge report, tokenizer audit, init report, zero-step summary | proven setup or intrinsic result |
| parsed metric output | yes | non-empty `test_results.txt` or `summary.tsv` parsed by aggregation | measured result |
| live run snapshot | no | current training step, dev F1 during tagging training | execution progress only |
| blocked or model-pending coverage row | yes, as limitation | FVT Bible/Roundtrip rows pending | retained metric with explicit status |

This rule prevents three common overstatements. First, a live dev score is not a
downstream result until the final prediction/evaluation file is complete and
parsed. Second, `cis-lmu/glot500-base` is an external reference, not an
equal-budget baseline. Third, target10 downstream improvement cannot be claimed
while target10 task coverage is absent outside PPPL.

The final conclusion should therefore be written in two layers. The first layer
contains completed evidence: data scope, tokenizer expansion, initialization
audits, zero-step FVT advantage, and measured baseline/reference rows. The
second layer states the open test: whether the zero-step FVT advantage survives
matched continued MLM and transfers to available downstream tasks.

## 9. Results

### 9.1 Tokenization

The tokenizer append run is structurally valid and improves audited fertility
for 29/30 languages. It improves 9/10 target languages. The exception is
`dzo_Tibt`, which remains a visible failure case.

### 9.2 Zero-Step Initialization

Before continued MLM, initialization differences are large on the v5 target
group.

| Method | Target weighted NLL | Head weighted NLL | Status |
| --- | ---: | ---: | --- |
| `random` | 18.411756 | 12.895301 | measured |
| `mean` | 11.953142 | 8.037017 | measured |
| `fvt` | 8.785518 | 6.621457 | measured |

FVT improves target weighted NLL by `-9.626238` compared with random resize
and by `-3.167624` compared with mean initialization. The central comparison
artifact is `docs/exp/v5/4_reporting/method_comparison_summary.md`; in that
summary, FVT reduces weighted NLL relative to random by `52.28%` on v5 target,
`48.65%` on the head sample, and `51.31%` on all measured zero-step rows. This
supports the initialization novelty at zero step. It does not by itself prove
after-MLM or downstream improvement.

### 9.3 Baseline And Reference Evaluation

The current parsed baseline/reference rows establish the comparison scale for
later v5 method results.

| Metric | Model | Group | Score | Value |
| --- | --- | --- | --- | ---: |
| PPPL | `xlmr_base` | v5 target | weighted PPPL | 61.980216 |
| PPPL | `xlmr_base` | head | weighted PPPL | 8.117338 |
| PPPL | `xlmr_base` | all | weighted PPPL | 9.986271 |
| PPPL | `glot500_base` | v5 target | weighted PPPL | 15.102934 |
| PPPL | `glot500_base` | head | weighted PPPL | 10.213100 |
| PPPL | `glot500_base` | all | weighted PPPL | 10.640353 |
| Tatoeba | `xlmr_base` | head | Top-10 | 0.656309 |
| Tatoeba | `xlmr_base` | all available | Top-10 | 0.566067 |
| Tatoeba | `glot500_base` | head | Top-10 | 0.743755 |
| Tatoeba | `glot500_base` | all available | Top-10 | 0.706649 |
| Tatoeba | `v5_random` | head | Top-10 | 0.700285 |
| Tatoeba | `v5_random` | all available | Top-10 | 0.610353 |
| Bible | `xlmr_base` | head/all available | Top-10 | 0.381153 |
| Bible | `glot500_base` | head/all available | Top-10 | 0.509356 |
| Bible | `v5_random` | head/all available | Top-10 | 0.328019 |
| Taxi1500 | `xlmr_base` | head/all available | macro-F1 | 0.592876 |
| Taxi1500 | `glot500_base` | head/all available | macro-F1 | 0.743338 |
| Taxi1500 | `v5_random` | head/all available | macro-F1 | 0.702956 |
| NER | `xlmr_base` | all available | F1 | 0.549858 |
| NER | `xlmr_base` | head | F1 | 0.621207 |
| NER | `xlmr_base` | v5-target actual intersection | F1 | 0.459364 |
| NER | `glot500_base` | all available | F1 | 0.627108 |
| NER | `glot500_base` | head | F1 | 0.645915 |
| NER | `glot500_base` | v5-target actual intersection | F1 | 0.553191 |
| NER | `v5_random` | all available | F1 | 0.544628 |
| NER | `v5_random` | head | F1 | 0.608020 |
| NER | `v5_random` | v5-target actual intersection | F1 | 0.560554 |
| POS | `xlmr_base` | all available | F1 | 0.481336 |
| POS | `xlmr_base` | head | F1 | 0.571446 |
| POS | `glot500_base` | all available | F1 | 0.567542 |
| POS | `glot500_base` | head | F1 | 0.573832 |
| POS | `v5_random` | all available | F1 | 0.481102 |
| POS | `v5_random` | head | F1 | 0.587430 |
| Roundtrip | `xlmr_base` | head/all available | accuracy | 0.185300 |
| Roundtrip | `glot500_base` | head/all available | accuracy | 0.205189 |
| Roundtrip | `v5_random` | head/all available | accuracy | 0.190300 |

The NER v5-target row should be interpreted narrowly: it comes from the actual
evaluated intersection and currently consists of `fur_Latn` only. It is not a
target10-wide downstream result.

The POS rows are available-language tagging references. XLM-R-base,
Glot500-base, and v5-random POS runs use `TRAIN_LANGS=tur_Latn` because the
local POS materialization does not include `train-eng_Latn.tsv`. The measured
v5-random POS row has F1 `0.481102` over all available POS languages and
`0.587430` over the head group; the matched FVT POS row remains checkpoint-gated.

### 9.4 Pending Main Method Results

The `v5_random` after-MLM PPPL row is now measured. Its weighted PPPL is
`39.222875` on v5 target10, `18.726452` on the head group, and `20.138927`
on all 102 language-scripts. This is a measured random-initialized checkpoint
row, not yet a method comparison: the corresponding `v5_fvt` PPPL row is still
locked until the matched FVT checkpoint is ready and parsed by aggregation.
The `v5_random` Tatoeba retrieval row is measured with Top-10 accuracy
`0.700285` on the 63-language head split and `0.610353` over all 98 available
language-scripts. This fills the random-checkpoint available-language row; it is
not a target10 downstream result because Tatoeba target10 coverage remains
`0/10`.
The `v5_random` Taxi1500 row is measured with macro-F1 `0.702956` and accuracy
`0.747748` on the local English-only split. This is a limited available-language
classification row; it does not unlock a target10 downstream claim.
The `v5_random` Roundtrip row is also measured with accuracy `0.190300` over
the same 74 available language-scripts as the XLM-R and Glot500-base reference
rows. This is available-language downstream evidence for the random checkpoint
only; downstream method claims remain locked until the matched `v5_fvt`
Roundtrip row exists.
The `v5_random` Bible retrieval row is measured as well, with Top-10 accuracy
`0.328019` over the same 74 available Bible language-scripts. This is a
single-checkpoint measured row, not evidence that the embedding initialization
method wins; that comparison still requires the matched `v5_fvt` Bible row.
The `v5_random` NER row is measured too, with F1 `0.544628` over all 164
actual runner language rows, `0.608020` over the head group, and `0.560554` on
the one-language v5-target actual intersection (`fur_Latn`). This is
available-language tagging evidence for the random checkpoint only; it does not
unlock a target10-wide downstream claim.
The `v5_random` POS row is also measured with F1 `0.481102` over all available
POS languages and `0.587430` over the head group under the same
`TRAIN_LANGS=tur_Latn` condition as the baseline/reference POS rows. It is a
random-checkpoint tagging row, not yet a method win; that comparison requires
the matched `v5_fvt` POS row.

Taken together, the measured `v5_random` rows are best interpreted as a
diagnostic lower-bound checkpoint. The random-initialized model improves
target10 PPPL relative to XLM-R (`39.222875` versus `61.980216`) but is still
substantially behind Glot500-base (`15.102934`), and its head/all PPPL remains
worse than both references. Available-language downstream behavior is mixed:
it improves over XLM-R on Tatoeba and Taxi1500 but not to the Glot500-base
reference level; it is below both references on Bible retrieval; it is near
XLM-R on all-language POS, above both references on head POS, and between
XLM-R and Glot500-base on Roundtrip. This mixed profile strengthens the need
for the matched `v5_fvt` test rather than weakening the design: the final
method claim must depend on whether source-token-decomposition initialization
improves over this random-checkpoint baseline after the same 10K MLM budget.

The following rows are intentionally pending:

- `v5_fvt` after-MLM PPPL.
- `v5_fvt` Tatoeba retrieval.
- `v5_fvt` Bible retrieval over available Bible languages.
- `v5_fvt` text classification after the matched checkpoint.
- `v5_fvt` NER and `v5_fvt` POS over available task languages.
- `v5_fvt` Roundtrip alignment over available Roundtrip languages.

The required post-checkpoint insertion path is:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

Only rows parsed into `3_evaluation/09_aggregation/` should replace the
pending labels above. If a metric remains unavailable, it must stay as
`blocked-data` or `coverage-limited` rather than disappearing from the results.
The exact launch environment, output/log paths, and promotion rule are generated
in `3_evaluation/post_checkpoint_execution_plan.md`.

### 9.5 Outcome-Conditioned Final Wording

After post-checkpoint evaluation, the abstract and conclusion should be
updated from the decision tree rather than rewritten ad hoc. The outcome matrix
for the Korean report/PPT is:

```text
docs/exp/v5/4_reporting/post_checkpoint_outcome_matrix_ko.md
```

The English prose blocks are maintained in:

```text
docs/exp/v5/4_reporting/03_final_report/result_interpretation_blocks.md
```

The file-by-file report/PPT edit order is maintained in:

```text
docs/exp/v5/4_reporting/post_result_patch_plan_ko.md
```

The final report should choose exactly one of these outcome families:

| Outcome family | Required evidence | Final wording rule |
| --- | --- | --- |
| bounded positive | FVT wins after-MLM PPPL and most available downstream rows | claim a bounded method benefit, while keeping target10 downstream coverage caveats |
| intrinsic positive, downstream mixed | FVT wins after-MLM PPPL but downstream rows vary by task | claim intrinsic adaptation improvement only; describe downstream as task- and coverage-dependent |
| early-only diagnostic | FVT wins zero-step but not after matched MLM | frame initialization as early-adaptation evidence rather than final superiority |
| negative final comparison | FVT does not beat random in PPPL or downstream | report a controlled negative result and discuss training/objective implications |
| incomplete evaluation | matched rows or parsers remain missing | keep the execution-draft conclusion and leave final method claims locked |

No final abstract or conclusion sentence should be upgraded unless
`post_result_patch_plan_ko.md`, `final_claim_decision_tree.md`,
`result_promotion_readiness_audit.md`, and `final_claim_freeze_audit.md`
agree on the same non-pending outcome and patch scope.

## 10. Analysis

The zero-step results suggest that new vocabulary rows are not a neutral
implementation detail. Random resize creates a large target-group penalty
before training. Mean initialization stabilizes the rows, but source-token
decomposition produces the best current intrinsic result. The method appears
especially useful when a new surface form can be decomposed into informative
source subpieces by the original tokenizer.

The tokenizer result is also instructive. A larger vocabulary can reduce
fertility for most languages but still harm an individual script when appended
piece scores alter segmentation behavior. The `dzo_Tibt` case should remain in
the main analysis because it prevents overclaiming and points to a concrete
repair direction: score calibration or script-aware filtering of appended
pieces.

## 11. Limitations

This is not a 511-language Glot500 reproduction. It is a controlled
102-language replay. The selected target10 has raw-text coverage but little
downstream task coverage in the currently materialized evaluation data.
Therefore target10 downstream improvement is not a supported claim.

Bible retrieval and roundtrip alignment are retained as required metric
families. Bible retrieval now has available-language local parallel data
materialized for `74/102` language-scripts, with target10 coverage still
`0/10`. XLM-R-base, Glot500-base, and v5-random rows are measured, while the
remaining gap is the matched v5-FVT row after checkpoint completion and
post-checkpoint preflight. Roundtrip alignment now has Bible-derived inputs, a
v5 runner, and measured XLM-R-base/Glot500-base/v5-random rows over 74
language-scripts; its remaining gap is also v5-FVT execution after the matched
checkpoint. These states should appear in final tables explicitly rather than
being omitted.

`cis-lmu/glot500-base` is an external reference model with a different
training scale. It is useful context, but it is not an equal-compute baseline.

## Reproducibility Appendix

The full command/path appendix for reproducing or auditing v5 is maintained in:

```text
docs/exp/v5/4_reporting/03_final_report/reproducibility_appendix.md
```

The appendix records the 92+10 scope lock, canonical local paths, merge and
tokenizer commands, paired MLM launch, metric-wrapper pattern, model keys,
required metric handling, result-promotion rules, and the post-result patch
plan that keeps report/PPT edits tied to parsed aggregation rows.

## 12. Conclusion

The v5 setup establishes a faithful controlled replay of the Glot500-style
workflow on a 102-language subset. The data scope is frozen, the full corpus
merge is complete, the SentencePiece append tokenizer is trained and audited,
and all Glot500 metric families are retained with coverage or blocker
accounting. This is not a full 511-language reproduction, but it preserves the
experimental structure needed to study tokenizer expansion, continued MLM, and
head/tail/all evaluation under a tractable budget.

The completed method evidence already supports the central novelty
motivation. Newly appended vocabulary rows are not an implementation detail:
source-token decomposition initialization lowers v5-target zero-step weighted
NLL from `18.411756` under random resize to `8.785518`, while preserving source
rows, remapping `<mask>` correctly, separating byte fallback rows, and keeping
the LM head tied. The tokenizer audit is also mostly positive, improving
fertility for `29/30` audited languages, with `dzo_Tibt` kept as a visible
regression and analysis case.

The remaining conclusion depends on matched `v5_random` and `v5_fvt`
continued-MLM checkpoints and the available downstream replay. Until those rows
are parsed, the final claim should remain bounded: v5 demonstrates a controlled
Glot500-style replay and a strong intrinsic initialization advantage before
training; whether that advantage survives MLM and transfers to downstream tasks
is the next measured gate.

## References

- Ayyoob ImaniGooghari et al. 2023. Glot500: Scaling Multilingual Corpora and
  Language Models to 500 Languages. ACL 2023.
  `https://aclanthology.org/2023.acl-long.61/`, DOI `10.18653/v1/2023.acl-long.61`.
- Glot500 official code: `https://github.com/cisnlp/Glot500`
- Atsuki Yamaguchi, Aline Villavicencio, Nikolaos Aletras. 2026. How Can We
  Effectively Expand the Vocabulary of LLMs with 0.01GB of Target Language
  Text? Computational Linguistics 52(1):295-330.
  `https://aclanthology.org/2026.cl-1.9/`, DOI `10.1162/coli.a.581`.
- Yamaguchi et al. official code: `https://github.com/gucci-j/lowres-cve`
