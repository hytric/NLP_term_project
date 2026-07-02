# Second Try Plan

작성일: 2026-06-10

## Status

Planning complete. Individual reference summaries are in `docs/exp/second_try/reference_summaries/`, the synthesis is in `docs/exp/second_try/reference_summary.md`, downstream task details are in `docs/exp/second_try/downstream_tasks.md`, resolved decisions are in `docs/exp/second_try/questions.md`, execution rules are in `docs/exp/second_try/execution_rules.md`, and the locked execution order is in `docs/exp/second_try/step_index.md`. Step 09 was added as a post-hoc top-tier validation audit and supersedes Step 08 for translation success claims. Step 10 executes the P0 leakage/selection audit and keeps the current translation claim blocked. Step 11 checks fresh-heldout feasibility and shows F02/F03 require a new Step 01 split or new corpus. Step 12 creates a v2 split with `ACT` as clean final heldout and `JOH` excluded as burned old test. Step 13 completes the v2 tokenizer rerun and selects a 32k tokenizer using Mark/dev only. Step 14 completes v2 embedding initialization and selects `fvt` using full Mark/dev zero-step MLM loss. Step 15 completes the token-matched v2 MLM control artifact run, but its claim gate fails because the adapted checkpoint is not competitive with the original continued-pretraining control. Step 16 confirms this is not only a raw-token-loss artifact: estimated NLL per word/char also fails the competitive margin. Step 17 localizes the failure to added-token prediction. Step 18 improves added-token loss but worsens all-token loss. Step 19 confirms a strict new-row-only repair preserves base rows and base-token loss, but does not improve added-token loss. Step 20 tests bias-only and lower-rate added-only variants; the best variant improves mean all/base/added losses but fails the seed-stable repair gate. Step 21 tests `mean` and `align` alternative initializations under the Step15 budget and neither beats `fvt`, so positive model-dependent claims remain blocked. Step 22 audits the full experiment trail and concludes that v2 has no active shortcut found, while positive model-dependent claims still require additional experiments. Step 23 tests smaller 8k/16k vocab branches and passes the tokenizer-size redesign probe, selecting 8k as the next branch. Step 24 runs the 8k branch against the original-control normalized audit; artifact gate passes, but claim gate fails with word/char ratio `1.472019`. Step 25 continues both 8k and original-control checkpoints to about 1M total tokens; artifact gate passes, but probe gate fails with word/char ratio `1.587381`, so longer 8k MLM alone does not rescue the claim. Step 26 locks the current top-tier-safe framing as a diagnostic negative claim: tokenizer extension and smaller vocabularies help the preprocessing/added-token burden, but positive adapted-model, downstream, and translation claims remain blocked until a new objective/data redesign passes Step15/16-style controls. Step 27 converts that claim contract into a manuscript-ready package with abstract, claim wording, table manifest, reviewer-risk audit, and reproducibility checklist.

## Final Goal

`xlm-roberta-base`에 Glot500-style vocabulary extension과 language adaptation을 적용하고, 저자원/미지원 언어에서 tokenizer bottleneck이 줄어드는지와 그 개선이 encoder-only downstream task 성능으로 이어지는지 검증한다. 이후 translation benchmark를 추가해 high-resource reference score의 80% 이상을 목표로 한다.

Current Step26 conclusion: the 80% translation target and positive adapted-model claim are not supported. The top-tier-safe output is a diagnostic negative result unless a future objective/data redesign passes the required controls.

## Core Claim

저자원/미지원 언어에서는 기존 multilingual tokenizer가 과도한 fragmentation과 single-character token을 만든다. 기존 XLM-R vocabulary를 보존한 채 target-language subword를 append하면 tokenization 병목은 줄어든다. 그러나 v2 clean split과 matched-token original continued-pretraining control 아래에서는 현재 adapted extended-vocabulary model이 competitive하지 않다. 최종 claim은 vocabulary extension, initialization, vocabulary size가 appended-token learning burden에 영향을 준다는 diagnostic result와, 단순 repair/longer-budget으로는 positive model claim을 회복하지 못했다는 negative result로 제한한다.

## Fixed Decisions

| Item | Decision |
| --- | --- |
| Base model | `xlm-roberta-base` |
| Architecture | encoder-only |
| Translation | separate Step 07 benchmark; not part of encoder-only downstream gate |
| Main data | Bible corpus, confirmed target10 최대한 유지 |
| Downstream | Bible proxy task 허용, 쉬운 task라는 한계 명시 |
| Vocab sizes | 8k, 16k, 32k |
| Tokenizer method | SentencePiece unigram |
| Vocab merge | 기존 XLM-R token id 보존, 새 piece append |
| Init methods | tutorial 기준 가능한 방법 전체 비교 |
| Gate | tokenization 개선 + MLM dev loss 개선 |
| Samples | 언어별 10개 + 대표 실패 케이스 10개 |
| Checkpoints | gate 통과 후보만 저장 |
| Result format | stage별 `results.md` + TSV metrics + sample markdown |
| GPU policy | GPU 4 우선, 현재 환경에서는 GPU 4 미표시로 GPU 3 fallback |
| Large artifacts | `/home/axt/mnt2/jongha/second_try` |
| Translation target | high-resource reference score의 80% 이상 |

## Target Languages

우선 confirmed target10을 유지한다.

| ISO | Language | Script | Role |
| --- | --- | --- | --- |
| cop | Coptic | Coptic | core non-Latin bottleneck |
| syr | Syriac | Syriac | core non-Latin bottleneck |
| chr | Cherokee | Cherokee | non-Latin bottleneck |
| oji | Ojibwa | Aboriginal Syllabics | non-Latin bottleneck |
| bsn | Barasana-Eduria | Latin | low-resource Latin comparison |
| usp | Uspanteco | Latin | low-resource Latin comparison |
| nhg | Nahuatl (Tetelcingo) | Latin | low-resource Latin comparison |
| ake | Akawaio | Latin | low-resource Latin comparison |
| kbh | Camsa | Latin | low-resource Latin comparison |
| acu | Achuar-Shiwiar | Latin | low-resource Latin comparison |

Downstream task에서 모든 언어를 쓸 수 없으면 target10 전체로 vocab/MLM을 하고, downstream은 가능한 language subset으로 평가한다.

## Method Overview

1. Build held-out-safe target10 data.
2. Run XLM-R baseline tokenization audit.
3. Train target10 SentencePiece unigram tokenizers with vocab sizes 8k, 16k, 32k.
4. Merge each target tokenizer into XLM-R tokenizer by appending genuinely new pieces.
5. Initialize new token embeddings with all feasible tutorial methods.
6. Run controlled MLM adaptation.
7. Select gate-passing checkpoints.
8. Run encoder-only downstream pilots.
9. Run final best checkpoint with 3 seeds.
10. Run translation benchmark against high-resource reference score.
11. Produce tables, samples, and final evidence map.
12. Run method-matched top-tier validation if any translation pass depends on a branch or external encoder.
13. Run leakage and selection audit before any top-tier translation claim is allowed.
14. Confirm a fresh held-out set exists before rerunning method-matched translation.
15. Create a v2 split and rerun all model-dependent evidence under that split.
16. Rerun v2 tokenizer training/merge from v2 train only and select on Mark/dev only.
17. Rerun v2 embedding initialization and select initialization on Mark/dev only.
18. Rerun v2 MLM adaptation with an original continued-pretraining control across at least 3 seeds.
19. Audit cross-tokenizer MLM metrics with word/character-normalized diagnostics.
20. Decompose adapted MLM failure into base-token and added-token losses to identify the repair target.
21. Test an added-token-focused repair objective and measure whether it improves added-token loss without degrading all-token loss.
22. Test a strict new-row-only repair from Step15 adapted checkpoints and audit whether base rows are actually preserved.
23. Test staged/lower-rate added-only repair variants and require seed-stable improvement before rerunning MLM controls.
24. Test plausible alternative initializations under the same MLM budget before concluding the failure is not just the `fvt` initialization choice.
25. Audit the complete experiment trail for active shortcuts and define mandatory next experiments before any positive top-tier model claim.
26. Test smaller 8k and 16k tokenizer branches under the Step15 MLM budget and promote a passing branch only after dev-only evidence.
27. Rerun MLM control and normalized metrics for the selected 8k branch before any downstream or translation final readout.
28. Probe whether a longer 8k MLM budget closes the original-control gap before deciding between further objective/data redesign and negative diagnostic framing.
29. Lock the top-tier-safe diagnostic claim and list the required future experiments before any positive final readout.
30. Package the diagnostic negative claim as a manuscript-ready outline with tables, reviewer risk audit, and reproducibility checklist.

If a later benchmark fails, the final analysis must not invent a positive claim. It may close as
`PASS_NEGATIVE_RESULT` only when the failed gate, measured evidence, return-to step, and retry
condition are fully documented.

## Locked Step Folders

The authoritative execution plan is split into per-step folders. Each folder contains:

- `plan.md`: work instructions and exit criteria
- `results.md`: required result summary
- `score_table.tsv`: mandatory score table to fill before step exit
- `file_results.tsv`: per-output-file status, row/count or size, and path evidence

No step may advance while its `score_table.tsv` contains `TBD`, blank fields, or unchecked values. No step may advance without a complete `file_results.tsv` for files produced by that step.

Step 08 is allowed to synthesize a documented negative result when Step 07 has a complete
failure branch and return protocol. In that case Step 08 must use `Gate status: PASS_NEGATIVE_RESULT`
and keep the failed claim marked as unsupported.

Step 09 is the authority for top-tier translation claims whenever it exists. If Step 09 marks the
method-matched translation claim as failed, Step 08 translation success wording is superseded.

Step 10 is the authority for leakage/selection validity whenever it exists. If Step 10 marks selection
protocol as failed, Step 07/Branch 001 translation success rows remain exploratory even if their raw
chrF score is high.

Step 11 is the authority for whether F02/F03 can be run from current artifacts. If Step 11 marks fresh
held-out availability as failed, return to Step 01 or import a new corpus before translation reruns.

Step 12 defines the v2 split for reruns. Once Step 12 exists, v1 checkpoints and v1 translation scores
remain exploratory only; v2 final claims require v2 tokenizer, MLM, downstream, and translation reruns.

Step 13 defines the v2 tokenizer selected for later initialization and MLM reruns. Later v2 model
experiments must use the selected Step13 tokenizer unless they explicitly open a new v2 tokenizer branch.

Step 14 defines the v2 initialized checkpoint selected for MLM reruns. Later v2 model experiments must
start from the selected Step14 initialization unless they explicitly open a new v2 initialization branch.

Step 15 defines the first v2 model-dependent MLM control. The latest run matches train tokens at 500k
per run and has artifact gate `PASS` but claim gate `FAIL`; later downstream or translation runs may
use its checkpoints only as negative or exploratory evidence unless Step 15 is rerun with a passing
claim gate or the final claim is explicitly downgraded.

Step 16 defines the tokenizer-normalized MLM metric audit. It has artifact gate `PASS` but claim gate
`FAIL`; raw-token Step15 failure remains valid under estimated NLL per word and per character.

Step 17 defines the added-token failure analysis. It has artifact gate `PASS` and diagnostic gate
`PASS`: added-token loss is the dominant failure source, so repair should target added-token
learning/init/objective before downstream or translation positive claims.

Step 18 defines the first added-token-focused repair. It has artifact gate `PASS` but repair gate
`FAIL`: added-token loss improves in all seeds, but all-token loss worsens in all seeds. The next
repair should preserve base-token behavior, for example with frozen-base or new-row-only training.

Step 19 defines the strict new-row-only repair. It has artifact gate `PASS` and trainable audit
`PASS`, but repair gate `FAIL`: base rows are preserved and base-token loss is nonworse in all seeds,
yet added-token loss worsens in all seeds. The next repair should use a changed schedule/objective,
such as lower-rate staged training or another added-token learning method, before rerunning Step 15.

Step 20 defines the staged/lower-rate added-only repair grid. It has artifact gate `PASS` and
trainable audit `PASS`, but repair gate `FAIL`: no variant improves added-token loss without
base/all degradation in every seed. The best variant, `new_row_added_lr1e-5`, improves mean all,
base, and added losses but only improves added-token loss in `1/3` seeds, so it is not seed-stable.

Step 21 defines the alternative-initialization MLM probe. It has artifact gate `PASS` but probe gate
`FAIL`: `mean` and `align` both improve from zero-step but neither beats the Step15 `fvt` adapted
baseline on raw mean loss or category seed gates. The best alternative, `align`, has raw mean final
loss `5.086652`, worse than `fvt` `4.946829`, and raw ratio to original control `2.020110`.

Step 22 defines the full shortcut and next-experiment audit. It has audit gate
`PASS_AUDIT_BLOCKS_POSITIVE_CLAIM`: no active v2 shortcut or final-set leakage is found, v1
translation shortcuts remain invalidated, and positive adapted-model claims remain blocked until a
tokenizer/objective redesign passes seed-stable repair and control gates.

Step 23 defines the tokenizer-size redesign probe. It has artifact gate `PASS` and probe gate
`PASS`: both 8k and 16k smaller-vocab branches beat the 32k Step15 raw mean final loss and improve
added/base/all category losses in `3/3` seeds. The best branch is 8k with raw mean final loss
`4.541285` versus 32k `4.946829`, but it still has raw ratio `1.803523` to the original-control
mean `2.518008`; therefore it must rerun Step15/16-style controls before any positive claim.

Step 24 defines the selected 8k MLM control and normalized audit. It has artifact gate `PASS` but
claim gate `FAIL`: the 8k branch improves over zero-step in `3/3` seeds and keeps matched token
budget ratio `1.000714`, but estimated NLL per word/char ratio is `1.472019`, above the required
`<=1.100000`. Positive model-dependent downstream/translation claims remain blocked.

Step 25 defines the 8k continued-budget probe. It has artifact gate `PASS` but probe gate `FAIL`:
both 8k and original-control checkpoints are continued to about 1M total train tokens, but the
normalized word/char ratio worsens to `1.587381`. Longer 8k MLM alone does not rescue the
model-dependent claim.

Step 26 defines the top-tier diagnostic claim synthesis. It has gate
`PASS_DIAGNOSTIC_CLAIM_READY`: the allowed final claim is a controlled diagnostic negative result.
Positive adapted-model, downstream, and translation final claims remain blocked until a new
objective/data redesign passes Step15/16-style original-control and normalized audits.

Step 27 defines the final manuscript synthesis. It has gate `PASS_MANUSCRIPT_READY`: the diagnostic
negative manuscript package is ready with abstract, paper claims, table/figure manifest, reviewer
risk audit, and reproducibility checklist. A positive performance manuscript remains blocked.

| Step | Folder | Purpose |
| --- | --- | --- |
| 00 | `00_scope_and_references` | freeze scope and reference mapping |
| 01 | `01_data_and_splits` | create leakage-safe data manifests |
| 02 | `02_tokenization_audit` | measure original XLM-R tokenization bottleneck |
| 03 | `03_vocab_extension` | train/merge 8k, 16k, 32k tokenizers |
| 04 | `04_embedding_init` | initialize new token rows and run diagnostics |
| 05 | `05_mlm_adaptation` | run MLM adaptation and select checkpoint |
| 06 | `06_downstream_tasks` | run encoder-only downstream evaluations |
| 07 | `07_translation_benchmark` | run translation benchmark and 80% high-resource comparison |
| 08 | `08_final_analysis` | produce final evidence map and report tables |
| 09 | `09_top_tier_validation` | audit shortcut risk with method-matched translation comparisons |
| 10 | `10_leakage_selection_audit` | audit split leakage, test-aware selection, and invalidated translation runs |
| 11 | `11_fresh_holdout_feasibility` | determine whether F02/F03 can run on a fresh held-out set |
| 12 | `12_v2_split_protocol` | create the v2 fresh-heldout split and required rerun protocol |
| 13 | `13_v2_tokenizer` | train/merge v2 tokenizers from train only and select on Mark/dev |
| 14 | `14_v2_embedding_init` | initialize Step13 tokenizer and select init method on full Mark/dev MLM loss |
| 15 | `15_v2_mlm_control` | run v2 MLM adaptation plus original continued-pretraining control with 3 seeds |
| 16 | `16_v2_mlm_metric_fairness` | audit cross-tokenizer MLM loss with word/character-normalized diagnostics |
| 17 | `17_v2_added_token_failure_analysis` | decompose v2 adapted MLM failure into base-token and added-token loss |
| 18 | `18_v2_added_token_repair` | test added-token-focused repair objective |
| 19 | `19_v2_new_row_only_repair` | test strict appended-row-only repair from Step15 adapted checkpoints |
| 20 | `20_v2_staged_added_token_repair` | test bias-only and lower-rate added-only repair variants |
| 21 | `21_v2_alt_init_mlm_probe` | test mean and align initializations under the Step15 MLM budget |
| 22 | `22_full_experiment_audit` | audit shortcut risk and define required next experiments |
| 23 | `23_v2_vocab_size_objective_probe` | test smaller 8k and 16k vocab branches under the Step15 MLM budget |
| 24 | `24_v2_8k_mlm_control` | audit selected 8k branch against original-control normalized MLM metrics |
| 25 | `25_v2_8k_continued_budget_probe` | continue 8k and original-control checkpoints to probe longer MLM budget |
| 26 | `26_top_tier_diagnostic_claim_synthesis` | lock the top-tier-safe diagnostic claim and future positive-claim gates |
| 27 | `27_final_manuscript_synthesis` | package the diagnostic negative claim into manuscript-ready artifacts |

Failure and return rules are defined in `step_index.md` and repeated inside each step `plan.md`.

## Stage 00: Reference And Implementation Audit

Goal:

- Confirm the exact implementation path for XLM-R tokenizer merge and embedding resize.
- Use prior implementation structure only as engineering reference. All second_try evidence, commands, metrics, and results must be newly produced under second_try.

Work:

1. Read `reference_summary.md`.
2. Inspect available implementation patterns only to define second_try-specific commands.
3. Create XLM-R-specific implementation notes and artifact paths.
4. Verify special token ids:
    - `<s>`
    - `</s>`
    - `<pad>`
    - `<unk>`
    - `<mask>`

Outputs:

- `docs/exp/second_try/00_scope_and_references/results.md`
- `docs/exp/second_try/00_scope_and_references/reference_trace.md`
- `docs/exp/second_try/00_scope_and_references/scope_decisions.tsv`

Gate:

- XLM-R tokenizer and model can be loaded.
- Original special token ids and meanings are documented.

## Stage 01: Data And Splits

Goal:

- Build reproducible train/dev/test splits for tokenizer training, MLM adaptation, samples, and downstream proxy tasks.

Default split:

- Train: all books except dev/test books
- Dev: Mark
- Test: John

Reason:

- Book-level split reduces random verse leakage.
- It is easy to explain in report.
- It is simple, explainable, and leakage-aware.

Work:

1. Rebuild target10 Bible verse table if needed.
2. Confirm language counts.
3. Create tokenizer train text from train split only.
4. Create MLM train/dev files from train/dev only.
5. Keep test books out of tokenizer and MLM adaptation.
6. Prepare sample rows: 10 per language + 10 failure cases.

Outputs:

- `data/processed/second_try/target_languages.tsv`
- `data/processed/second_try/target10_bible_verses.tsv`
- `data/processed/second_try/target10_stats.tsv`
- `data/processed/second_try/tokenizer_train.txt`
- `data/processed/second_try/mlm_train.txt`
- `data/processed/second_try/mlm_dev.txt`
- `docs/exp/second_try/01_data_and_splits/results.md`

Gate:

- Each language has enough train/dev/test examples.
- Test verses are not used in tokenizer training or MLM adaptation.

## Stage 02: Baseline Tokenization Audit

Goal:

- Quantify XLM-R tokenization bottleneck before extension.

Metrics:

- avg tokens/sentence
- tokens/word
- tokens/char
- single-character token percentage
- `<unk>` token percentage
- byte fallback percentage if applicable
- sequence length p50/p90/p95
- blank/degenerate encoding cases
- qualitative tokenization examples

Work:

1. Run XLM-R tokenizer on held-out target10 samples.
2. Use XLM-R as the official baseline. Do not use previous-run scores as second_try evidence.
3. Identify worst languages by fragmentation and blank/unk/character-level behavior.

Outputs:

- `docs/exp/second_try/02_tokenization_audit/results.md`
- `docs/exp/second_try/02_tokenization_audit/xlmr_target10_tokenization_metrics.tsv`
- `docs/exp/second_try/02_tokenization_audit/tokenization_examples.md`

Gate:

- At least several target languages show meaningful tokenization bottleneck.
- If the bottleneck is weak, downstream claims must focus on representation adaptation rather than tokenizer bottleneck.

## Stage 03: Vocabulary Extension

Goal:

- Train target10 unigram tokenizers and append new pieces to the original XLM-R tokenizer.

Conditions:

| Condition | Auxiliary vocab size |
| --- | ---: |
| spm8k | 8,000 |
| spm16k | 16,000 |
| spm32k | 32,000 |

Merge rule:

- Preserve all original XLM-R token ids.
- Append only target pieces not already present in XLM-R.
- Preserve special tokens and their ids.
- Save merge report with added/overlap counts.

Metrics:

- auxiliary vocab size
- overlap count with XLM-R
- genuinely added token count
- meaningful overlap count excluding punctuation/digits/specials
- tokens/word reduction
- single-char token reduction
- `<unk>` and byte fallback rate
- sequence length reduction
- encode/decode round-trip status

Outputs:

- `data/processed/second_try/spm8k/`
- `data/processed/second_try/spm16k/`
- `data/processed/second_try/spm32k/`
- `data/processed/second_try/xlmr_target10_spm8k/`
- `data/processed/second_try/xlmr_target10_spm16k/`
- `data/processed/second_try/xlmr_target10_spm32k/`
- `docs/exp/second_try/03_vocab_extension/results.md`
- `docs/exp/second_try/03_vocab_extension/vocab_extension_metrics.tsv`
- `docs/exp/second_try/03_vocab_extension/tokenization_examples.md`

Gate:

- Extended tokenizer can encode/decode target10 samples.
- Original XLM-R special token ids are preserved.
- Tokenization improves over XLM-R baseline on tokens/word and single-character percentage.

Working numeric gate:

- Prefer at least 10% tokens/word reduction.
- Prefer at least 10% single-character token reduction.
- `<unk>`/blank/degenerate cases must not increase.

## Stage 04: Embedding Initialization

Goal:

- Initialize newly added token rows under controlled methods from the tutorial.

Required conditions:

| Init | Description |
| --- | --- |
| random | default random rows after resize |
| mean | global source embedding mean or Gaussian mean baseline |
| fvt | tokenize new piece with original XLM-R and average old subtoken embeddings |
| align | corpus span alignment between original and extended tokenizers |
| focus | overlap-anchor fastText/similarity-based initialization |

Optional if implementation cost is acceptable:

- `ofa`
- `wechsel`

Checks:

- input embedding size equals tokenizer vocab size.
- MLM head size equals tokenizer vocab size.
- tied weights remain tied if expected by XLM-R implementation.
- every new row is initialized.
- fallback count is recorded.
- embedding norm distribution is sane.
- zero-step MLM loss is computed.

Outputs:

- `data/processed/second_try/initialized_models/{vocab_size}/{init_method}/`
- `docs/exp/second_try/04_embedding_init/results.md`
- `docs/exp/second_try/04_embedding_init/embedding_init_metrics.tsv`
- `docs/exp/second_try/04_embedding_init/nearest_neighbors.md`

Gate:

- All required init methods produce loadable checkpoints.
- No missing or uninitialized rows.
- Zero-step MLM loss and embedding norms are recorded.

## Stage 05: MLM Adaptation

Goal:

- Compare vocab size and init methods under controlled MLM adaptation.

Training setup:

- Objective: Masked Language Modeling
- Base: `xlm-roberta-base`
- Data: Bible train/dev only
- Sequence length: start with 128 or 256 for pilot, consider 512 if GPU permits
- Learning rate: start at `5e-5`
- Seeds: init comparison uses 3 seeds
- GPU: stage-dependent, use GPU 2 and 3 in parallel for independent runs

Comparison scope:

- Original XLM-R eval-only baseline.
- For each vocab size: all feasible init methods.
- For all-init vocab+MLM: fixed compute budget.
- Select best vocab+init by dev MLM loss and tokenization gate.

Metrics:

- zero-step dev loss
- fixed-step train loss
- fixed-step dev loss
- pseudo-perplexity if feasible
- tokens/sec
- GPU runtime
- fallback and new-token usage correlation

Outputs:

- `docs/exp/second_try/05_mlm_adaptation/results.md`
- `docs/exp/second_try/05_mlm_adaptation/mlm_results.tsv`
- `docs/exp/second_try/05_mlm_adaptation/checkpoint_selection.md`
- gate-passing checkpoints only

Gate:

- Tokenization metrics improve.
- MLM dev loss improves over the corresponding zero-step checkpoint and is competitive with original XLM-R on the held-out target text.
- Best checkpoint is documented with vocab size, init method, seed, and config.

## Stage 06: Downstream Proxy Tasks

Goal:

- Test whether vocabulary extension + MLM adaptation improves encoder-only downstream performance.

Detailed task definitions are in `docs/exp/second_try/downstream_tasks.md`.

Final task set:

1. Book/genre classification
2. Verse retrieval/ranking
3. Parallel verse matching

Diagnostic-only task:

- Language identification

### Task 1: Book/Genre Classification

Input:

- A verse or short passage in one target language.

Label:

- Book id or coarser genre label.

Metrics:

- accuracy
- macro-F1

Purpose:

- Tests whether adapted encoder improves within-language classification in target scripts.

### Task 2: Verse Retrieval/Ranking

Input:

- Query verse embedding and candidate pool.

Target:

- Same verse id, same chapter neighborhood, or aligned counterpart depending on available data.

Metrics:

- Recall@1
- Recall@5
- MRR

Purpose:

- Tests sentence representation and cross-lingual alignment without a decoder.

### Task 3: Parallel Verse Matching

Input:

- Pair of verses.

Label:

- same verse id vs negative pair.

Metrics:

- accuracy
- macro-F1
- AUC

Purpose:

- Tests whether the encoder can distinguish true parallel pairs from hard negatives.

Baselines:

- majority/random baseline
- original XLM-R
- vocab-only if feasible
- best vocab+init+MLM checkpoint

Pilot comparison:

- Run downstream pilot for all three vocab sizes and required init methods if compute permits.
- Full downstream 3-seed run is reserved for the best selected checkpoint.

Outputs:

- `docs/exp/second_try/06_downstream_tasks/results.md`
- `docs/exp/second_try/06_downstream_tasks/downstream_results.tsv`
- `docs/exp/second_try/06_downstream_tasks/sample_predictions.md`
- `docs/exp/second_try/06_downstream_tasks/failure_cases.md`

Gate:

- Best adapted model improves over original XLM-R on at least one retrieval/classification task.
- If language identification improves but retrieval/classification does not, report tokenization sanity improvement only, not downstream success.

## Stage 07: Analysis And Report Tables

Goal:

- Convert experiment outputs into final-report-ready evidence.

Work:

1. Build claim/evidence map.
2. Create tables:
    - tokenization before/after
    - vocab size vs added token count
    - init method vs MLM dev loss
    - downstream baseline vs adapted
3. Create sample files:
    - language별 10 examples
    - 대표 실패 케이스 10 examples
4. Write limitations.

Outputs:

- `docs/exp/second_try/07_final_analysis/claim_evidence_map.md`
- `docs/exp/second_try/07_final_analysis/paper_tables.md`
- `docs/exp/second_try/07_final_analysis/qualitative_analysis.md`
- `docs/exp/second_try/07_final_analysis/limitations.md`

## Checkpoint Selection Rule

Rank checkpoints by:

1. pass tokenizer gate
2. pass MLM gate
3. downstream pilot average rank
4. lower added token count if performance is tied
5. lower runtime if performance is tied

Full 3-seed downstream evaluation is only for the final selected checkpoint and the original XLM-R baseline.

## GPU Policy

Available GPUs:

- physical GPU 2
- physical GPU 3

Policy:

- Tokenizer training and metric computation: CPU.
- Independent MLM/init/downstream pilots: run one process per GPU.
- DDP: use only if a single run is too slow and the script is stable.
- Prefer parallel independent runs over DDP during grid search.

## Risks

| Risk | Mitigation |
| --- | --- |
| Bible proxy task too easy | language identification diagnostic only; final claims use retrieval/classification |
| Vocab grid too expensive | run pilot first; full 3-seed only for selected checkpoint |
| Focus/Align implementation too slow | still run random, mean, fvt; document skipped methods |
| XLM-R tokenizer merge breaks ids | explicit special-id and encode/decode tests |
| Random init underperforms | expected baseline; do not use as final method unless it wins |
| Target-only MLM forgets old languages | note limitation; optional replay/forgetting probe |
| Downstream improvement weak | report tokenizer/MLM improvement and negative downstream result honestly |

## Immediate Next Steps

1. Complete `00_scope_and_references` notes and inspect XLM-R tokenizer/model loading.
2. Define the XLM-R-specific tokenizer merge path and document commands under second_try.
3. Rebuild target10 split under `data/processed/second_try`.
4. Run XLM-R baseline tokenization audit.
5. Train 8k/16k/32k unigram tokenizers.
