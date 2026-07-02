# Broad Target10 Positive Route: Survey and Methodology

작성일: 2026-06-18

## 목적

`third_try`의 현재 결론은 diagnostic negative report package다. Positive claim으로 재진입하려면 목표를 다음으로 좁혀야 한다.

> XLM-R-base의 기존 vocabulary id를 보존한 append-only vocabulary extension이 target10 전체 또는 거의 전체에서 seed-stable한 downstream/model-quality improvement를 만들고, 동시에 high-resource control collapse를 일으키지 않는지 검증한다.

현재 blocker는 세 가지다.

1. High-resource control: replay-safe retry 후에도 held-out high-resource control MLM loss delta가 `+0.675539`, no-collapse 통과가 `0/4`.
2. Target10 downstream coverage: Coptic POS만 supervised downstream으로 확인되었고, Syriac 포함 다수 target language는 proxy-only다.
3. Tokenizer-to-model gap: target10 평균 tokenizer fragmentation은 줄었지만, append token learning과 continued-pretraining schedule이 broad model gain으로 이어지지 않았다.

User preference: target10 broad evidence는 가능하면 언어간 번역 또는 classification으로 구성한다. `xlm-roberta-base`는 encoder-only 모델이므로 생성형 NMT를 main downstream으로 두면 모델 계열이 바뀐다. 따라서 positive route의 primary downstream은 cross-lingual classification으로 두고, translation은 sentence retrieval / translation ranking / bitext mining proxy로 둔다.

## Survey Map

| 축 | 핵심 문헌 | 읽는 이유 | third_try에 주는 결정 |
| --- | --- | --- | --- |
| Multilingual base and scaling | Glot500, XLM-R | Low-resource gain은 corpus size, script, related-language help, model capacity가 함께 결정된다. XLM-R은 high/low-resource tradeoff를 명시한다. | target10-only가 아니라 high-resource replay와 related-language bridge를 protocol에 넣고, high-resource control을 primary gate로 둔다. |
| Vocabulary extension | Yamaguchi et al. 2025, FOCUS, WECHSEL | Low-resource vocab expansion에서는 random init + naive full tuning이 위험하고, mean/align/FOCUS/WECHSEL류 initialization과 staged adaptation이 중요하다. | 기존 `fvt`만 최종으로 고정하지 말고, init과 warmup을 positive-route ablation으로 재개한다. |
| Tokenization fairness | Petrov et al. 2023, Ahia et al. 2023 | Fertility/token count 개선은 필요하지만 충분하지 않다. 언어별 over-fragmentation과 script별 불공정이 model quality와 비용에 영향을 준다. | tokenizer 선택 기준을 target10 평균 tokens/word 하나가 아니라 per-language non-regression, single-char/STRR, script-specific floor로 바꾼다. |
| Adaptive pretraining | Gururangan et al. 2020 | DAPT/TAPT는 task/domain unlabeled data를 단계적으로 넣을 때 downstream gain이 커진다. | full-MLM 전에 task/domain-aware unlabeled splits를 만들고, downstream dev와 분리된 TAPT-style train-only corpus를 구성한다. |
| Forgetting and replay | LoRA learns less/forgets less, Continually Adding New Languages, BaM | Continued pretraining은 새 언어 학습과 기존 능력 보존 사이 tradeoff가 있다. Replay, reduced LR, model merging, selective adaptation이 forgetting을 줄인다. | main은 full-model MLM을 유지하되, high-resource collapse가 재발하면 schedule/replay/BaM-style merge를 controlled deviation으로 둔다. |
| Broad evaluation | Glot500 eval suite, Taxi1500, Tatoeba/Bible retrieval, Coptic UD | Glot500은 retrieval, classification, NER/POS, alignment 등 다중 task로 평가한다. Taxi1500은 Bible 기반 1500+ 언어 classification으로 sparse-language coverage를 보완할 수 있다. Retrieval/ranking은 encoder-only 모델에서 번역 능력을 보는 가장 직접적인 proxy다. | target10-wide claim은 Coptic POS만으로 금지한다. Cross-lingual classification을 primary로 두고, language-pair translation retrieval/ranking을 secondary로 둔다. |

Primary references:

- Glot500: https://arxiv.org/abs/2305.12182
- XLM-R: https://arxiv.org/abs/1911.02116
- Low-resource vocabulary expansion: https://arxiv.org/abs/2406.11477
- FOCUS: https://arxiv.org/abs/2305.14481
- WECHSEL: https://arxiv.org/abs/2112.06598
- DAPT/TAPT: https://aclanthology.org/2020.acl-main.740/
- LoRA forgetting tradeoff: https://arxiv.org/abs/2405.09673
- Continually adding languages: https://openreview.net/forum?id=HE84ER1BNL
- Branch-and-Merge: https://aclanthology.org/2024.findings-emnlp.1000/
- Taxi1500: https://aclanthology.org/2025.naacl-short.36/
- Coptic UD: https://github.com/UniversalDependencies/UD_Coptic-Scriptorium

## Methodology

### 1. Evaluation-First Gate

Training을 다시 돌리기 전에 evaluation suite를 먼저 닫는다. Positive claim은 model selection 후에 찾는 것이 아니라, training 전부터 고정된 scorecard로만 허용한다.

Preferred downstream shape:

1. Primary: zero-shot or few-shot cross-lingual classification.
2. Secondary: language-pair translation retrieval/ranking, not free-form generation.
3. Tertiary: Coptic POS and any license-safe Syriac tagging task.

Primary target10 scorecard:

| Metric group | Scope | Model-dependent? | Use |
| --- | --- | --- | --- |
| Taxi1500 or reconstructed Bible topic classification | target10 coverage audit 필요 | yes | Primary broad downstream candidate |
| Bible/Tatoeba sentence retrieval | target10 language pairs where parallel text exists | yes | Translation proxy; frozen encoder Recall@1/MRR |
| Translation ranking / bitext mining classifier | target10 language pairs where parallel text exists | yes | Translation proxy; cross-encoder/reranker or pair classifier |
| Cross-lingual semantic embedding alignment | parallel target10 sentence/verse ids | yes | CLIP/CLAP-style similarity and 2D map diagnostic |
| Coptic UD POS | `cop` | yes | Coptic-specific official supervised evidence |
| Syriac POS or morphology corpus, if license-safe | `syr` | yes | Syriac-specific evidence; otherwise proxy-only label remains explicit |
| Target10 MLM proxy | all target10 | yes, but proxy | Early training monitor, not standalone downstream claim |
| High-resource MLM control | eng/deu/jpn/kor | yes, proxy | Hard safety gate |

Positive gate:

1. XLM-R-base baseline is rerun with the same code and split.
2. All model-dependent results use at least seeds `13/17/23`.
3. Primary macro language mean improves over XLM-R-base.
4. At least `7/10` target languages improve on the primary broad metric, and `cop` plus `syr` cannot both be negative/proxy-only.
5. High-resource control mean MLM loss delta must be `<= +0.3` preferred, `<= +0.5` absolute maximum.
6. No final test set is used for model or checkpoint selection.

Classification design:

| Variant | Train | Eval | Claim strength | Notes |
| --- | --- | --- | --- | --- |
| Taxi1500 zero-shot | English Bible classification | target10 Bible translations if available | strongest broad classification candidate | Requires PBC/Taxi1500 processing or equivalent per-language files. |
| Local Bible topic classification | English or high-resource labeled verses | target10 local Bible verses with shared verse ids | strong if labels are external and split-clean | Prefer Taxi1500 labels; avoid deriving labels from target test text. |
| Target10 few-shot classification | small target-language train split | held-out target-language test | useful but less cross-lingual | Must be 3-seed and language-balanced. |
| Book/chapter classification | Bible book/chapter labels | target10 Bible verses | weak diagnostic only | Too easy to exploit lexical/domain shortcuts; not enough for main positive claim. |

Translation/retrieval design:

| Variant | Input | Metric | Claim strength | Local fit |
| --- | --- | --- | --- | --- |
| Bi-encoder sentence retrieval | source sentence retrieves aligned target sentence | Recall@1, Recall@5, MRR | good encoder translation proxy | Existing `evaluation/retrieval/evaluate_retrieval_bible.py` can be reused. |
| Cross-encoder translation ranking | source-target pair scored as aligned/not aligned | pairwise accuracy, MAP, MRR | stronger translation proxy, but supervised | Existing reranker scripts can be adapted. |
| Bitext mining | all source/target embeddings mined for parallel pairs | F1 / precision@k | good language-pair representation test | Needs hard negatives and fixed candidate pools. |
| Free-form NMT generation | source text to generated target text | BLEU/chrF/COMET | not suitable for XLM-R main | Requires encoder-decoder model; keep outside main claim unless model family changes. |

Cross-lingual semantic embedding map:

This is the CLIP/CLAP-style view adapted to multilingual text. CLIP aligns image and text encoders in a shared embedding space by scoring paired examples; CLAP does the same for audio and text. Here, each language is a different view of the same semantic item.

| Component | Choice |
| --- | --- |
| Positive pair | Same `verse_id` or sentence id across two languages |
| Negative pair | Different `verse_id`; include hard negatives from same book/chapter or same topic |
| Encoder | XLM-R-base or third_try checkpoint |
| Representation | Mean-pooled layer 8 hidden states, plus CLS-pool ablation |
| Similarity | cosine similarity after L2 normalization |
| Retrieval metric | Recall@1, Recall@5, MRR, median rank |
| Alignment metric | positive cosine mean, positive-minus-hard-negative margin, same-meaning centroid variance |
| Hubness metric | top-k neighbor concentration by language and by sentence id |
| 2D map | UMAP primary, t-SNE/PCA as sensitivity checks |

2D map interpretation:

1. Good cross-lingual alignment: points cluster by `verse_id` / semantic item, not by language.
2. Bad language siloing: points cluster by language/script even when meanings are the same.
3. Bad hubness: one or two high-resource languages become nearest-neighbor hubs for many unrelated target sentences.
4. Useful positive-route signal: after continued pretraining, same-meaning cross-language clusters tighten while high-resource control clusters do not collapse.

The 2D plot is diagnostic, not sufficient by itself. The report should pair it with retrieval and margin scores so the figure is not just an attractive anecdote.

### 2. Data Redesign

Current Stage 01 materialized mixture is useful but too rigid. The positive route should replace it with online language sampling.

Required corpora:

1. Target10 train/dev/test split with exact leakage audit.
2. High-resource replay from true web sources, not Bible only.
3. High-resource Bible held-out control, never used for model selection except as no-collapse gate.
4. Bible downstream data split separately from MLM data, so verse classification/retrieval is not trivially memorized.
5. Related-language bridge corpora where justifiable:
   - Coptic: Greek, Arabic, Egyptian/Coptic-adjacent liturgical or scholarly transliteration only if leakage-safe.
   - Syriac: Arabic, Hebrew/Aramaic-adjacent resources, Peshitta-aligned material with strict train/dev/test separation.
   - Latin-script Amazonian/Mesoamerican languages: same family or geographic bridge only if language ID and license are clean.

Sampling policy:

| Schedule | Description | When to keep |
| --- | --- | --- |
| `alpha_0.3` | Glot500/XLM-R-style temperature sampling | Default candidate |
| `alpha_0.5` | More high-resource mass, less tail oversampling | Keep if high-resource collapse improves without losing target10 |
| `target_floor_control_cap` | Minimum target10 exposure plus high-resource cap | Keep if rare target languages under-train |
| `dynamic_replay` | Increase high-resource replay when control delta worsens | Keep only if dev-only rule and deterministic logging are clean |

### 3. Tokenizer Redesign

Keep the append-only id-preserving rule. Do not optimize only target10 average tokens/word.

Tokenizer selection score:

1. Existing XLM-R ids unchanged.
2. Special token ids unchanged.
3. Target10 macro tokens/word improves.
4. No target language has severe regression; `chr` and `oji` regressions from the current 48k candidate must be fixed or explicitly bounded.
5. Single-character ratio / STRR-like metric does not worsen sharply.
6. New token frequency is not concentrated in only Coptic/Syriac or only Latin scripts.
7. Byte fallback is only eligible for main if the actual XLM-R tokenizer path faithfully activates byte pieces. Otherwise it stays ablation-only.

Candidate grid:

| Candidate | Purpose |
| --- | --- |
| `targetheavy_32k_v2` | Lower capacity pressure than 48k |
| `targetheavy_48k_v2` | Current best average fragmentation, repaired for `chr`/`oji` |
| `script_balanced_48k` | Prevent Latin/Coptic/Syriac imbalance |
| `bridge_augmented_48k` | Add related-language bridge text to token learning |

### 4. Initialization and Warmup

The current `fvt` choice is justified for the diagnostic run, but positive route should reopen initialization as a controlled axis.

Recommended sequence:

1. Build new-row initialization candidates: `mean`, `align`, `fvt`, `focus_like`, and `wechsel_like` where auxiliary static embeddings exist.
2. Run zero-step MLM dev only on train/dev splits, not final test.
3. Run a short embedding acclimation phase:
   - update embeddings and LM head;
   - optionally update layer norm parameters;
   - keep transformer frozen for stability;
   - use target10 + bridge + small high-resource replay.
4. Then switch to full-model MLM. The final model must have full-model training, but warmup can be documented as initialization/acclimation.

Keep ablations:

- no warmup vs warmup;
- fvt vs align/focus-like;
- embeddings-only warmup length: 0, 1k, 5k optimizer steps.

### 5. Full-Model Continued Pretraining

Current 1000-step retry is too small to support broad positive wording. The next route should use a staged budget with gates.

| Phase | Budget | Seeds | Exit gate |
| --- | ---: | ---: | --- |
| Smoke | 500-1000 steps | 1 | Loss finite, no tokenizer/model mismatch |
| Schedule search | 2k-5k steps | 1 | target10 proxy improves and high-resource delta stays below warning |
| Mid-budget candidate | 10k-25k steps | 3 | target10 broad dev metric improves in macro mean; high-resource no-collapse |
| Final candidate | chosen full budget | 3+ | fixed checkpoint policy; final test once |

Training defaults:

- effective batch should move toward the Glot500-style batch instead of current 32 if hardware permits;
- use LR grid `5e-6`, `1e-5`, `2e-5`, with warmup and cosine/linear decay;
- save checkpoints frequently enough to test early overfitting, e.g. every 5-10% of budget;
- checkpoint selection must use only target10 dev + high-resource control dev;
- if high-resource control delta exceeds `+0.5`, abort or lower LR / increase replay before spending final budget.

### 6. Forgetting Mitigation Options

Main route remains full-model MLM with replay. If that keeps failing high-resource no-collapse, introduce these as explicit deviations:

1. KL/logit preservation on high-resource replay against frozen XLM-R-base.
2. L2-SP style regularization toward XLM-R weights.
3. Branch-and-Merge: train multiple full-model branches on disjoint sampled slices, then average/merge weights and evaluate the merged checkpoint.
4. Hybrid LoRA + full embedding/head update only as an ablation, not the main full-model claim, unless the success criterion is revised.

The important boundary: these methods may produce useful models, but the report must label whether the final claim is still "Glot500-style full-model MLM" or a regularized/merged adaptation variant.

### 7. Analysis Required for a Positive Paper Claim

For each final candidate, report:

1. Per-language target10 downstream metric with seed mean/range.
2. Macro target10 average and language-count win rate.
3. `cop` and `syr` explicit evidence table.
4. High-resource control table with per-language deltas.
5. Tokenizer metrics: tokens/word, single-char ratio, new-token utilization.
6. New-row learning diagnostics: appended-token frequency, MLM loss by old/new token category, embedding norm drift.
7. Training deviation audit: batch, LR, sampling, budget, checkpoint policy.

## Recommended Next Execution Order

1. Stage 06R: Build target10-wide evaluation coverage.
   - Audit Taxi1500 availability for `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp`.
   - If Taxi1500 is not fully available, reconstruct a license-safe Bible topic classification proxy using aligned train/dev/test verses and externally fixed labels.
   - Build a target10 language-pair retrieval matrix from available Bible/Tatoeba-style parallel text. Minimum pairs: `eng->target`, `target->eng`; preferred pairs: all target-target pairs with shared verse overlap.
   - Add translation ranking / bitext mining only after the frozen retrieval baseline is reproducible.
   - Produce a CLIP/CLAP-style semantic embedding report: cosine similarity matrix, retrieval metrics, positive-vs-hard-negative margins, hubness metrics, and UMAP/t-SNE 2D maps.
   - Add Syriac POS/morphology corpus only if license and split quality are acceptable.

2. Stage 01R: Rebuild corpus manifests.
   - Separate MLM text, downstream train/dev/test, and high-resource control.
   - Add online sampler manifests instead of only materialized text files.

3. Stage 03R: Tokenizer repair.
   - Repair `chr` and `oji` regression.
   - Add script-balanced candidate.
   - Keep byte fallback as ablation unless implementation is faithful.

4. Stage 04R: Init/warmup grid.
   - Compare `fvt`, `align`, `focus_like`, and `mean`.
   - Select by dev-only zero-step plus short warmup diagnostics.

5. Stage 05R: Schedule search.
   - One seed, short budgets, many schedules.
   - Kill schedules that improve target10 at the cost of high-resource collapse.

6. Stage 05F/06F: Final 3-seed candidate.
   - Run selected budget with seeds `13/17/23`.
   - Evaluate all fixed downstream/proxy tasks.
   - Permit positive claim only if the predeclared scorecard passes.

## Claim Template If Successful

Allowed wording:

> Under a predeclared target10-wide evaluation protocol, an id-preserving append-only XLM-R-base vocabulary extension with high-resource replay and full-model MLM continued pretraining improves macro target10 downstream/proxy-downstream performance over XLM-R-base across three seeds, while preserving high-resource control quality within the no-collapse threshold.

Forbidden unless the evidence really supports it:

> The model improves all target10 languages.

> Tokenizer fragmentation improvement alone causes downstream improvement.

> Coptic POS improvement proves broad target10 improvement.

> A proxy-only Syriac result proves supervised Syriac downstream improvement.
