# Novelty Analysis and Experiment Plan

작성일: 2026-06-19

## Purpose

`06_novelty`는 main experiment를 하나 더 추가하는 섹션이 아니다.  
목적은 현재 결과를 term report에서 방어 가능한 novelty claim으로 정리하고, 어떤 추가 실험이 그 claim을 강화하는지 명확히 하는 것이다.

핵심 질문:

> MLM-only multilingual encoder에서 raw cosine이 과도하게 높게 나올 때, low-resource cross-lingual semantic alignment를 어떻게 더 안정적으로 평가하고 개선할 것인가?

현재 `idea.md`, `problem.md`, `survey.md`의 결론은 같다.

- absolute cosine threshold는 Coptic-Syriac sentence equivalence 평가에 부적절하다.
- MLM loss는 token prediction proxy이지 sentence semantic alignment objective가 아니다.
- 따라서 positive/negative cosine 절대값보다 ranking, margin, hubness, downstream bridge를 봐야 한다.
- centering, PCA removal, whitening, CSLS는 anisotropy와 hubness를 완화하기 위한 핵심 방법론이다.

## Novelty Thesis

권장 novelty thesis:

> We propose an anisotropy-aware, margin-calibrated evaluation pipeline for append-only low-resource MLM adaptation. Instead of relying on raw cosine similarity, the pipeline removes language/script/domain common components and evaluates cross-lingual sentence equivalence through hard-negative retrieval, CSLS, and downstream probes.

한국어 보고서용 표현:

> 본 프로젝트는 append-only vocabulary extension과 MLM continued training 이후, low-resource ancient language representation을 raw cosine만으로 평가하면 과대평가가 발생한다는 문제를 보이고, language/script/domain 공통 성분 제거와 CSLS 기반 ranking/margin 평가를 통해 cross-lingual sentence alignment를 더 안정적으로 측정하는 방법론을 제안한다.

이 thesis에서 가장 중요한 점은 "translation을 해결했다"가 아니다.  
안전한 claim은 "tokenizer 보존, MLM adaptation, cosine attachment, semantic retrieval, shallow downstream, decoder collapse를 분리해서 평가하는 diagnostic framework"다.

## What Is Novel

| Component | Existing source | Our use | Novelty strength |
| --- | --- | --- | --- |
| append-only tokenizer extension | XLM-R/Glot500-style vocabulary extension, vocab extension tutorial | 기존 XLM-R id를 `0`개도 바꾸지 않고 새 target10 piece만 뒤에 append | medium |
| MLM continued training | Glot500-style adaptation | small fixed-budget controlled probe로 init/tokenizer 효과 확인 | low |
| raw cosine feature similarity | common sentence embedding probe | same cosine와 semantic retrieval을 분리해 calibration failure를 보임 | medium |
| centering/PCA/whitening | BERT anisotropy and whitening literature | low-resource ancient cross-lingual verse retrieval에 적용 | medium |
| CSLS | cross-lingual retrieval hubness correction | sentence-level Coptic-Syriac/target10 retrieval hubness 완화에 적용 | medium |
| hard-negative margin | retrieval/contrastive learning | random negative 대신 same-chapter/length/nearest-neighbor negative로 평가 | medium |
| contrastive adaptation | SimCSE/triplet/InfoNCE | aligned verse positive와 same-chapter hard negative로 low-resource alignment 학습 | high, optional |
| decoder collapse diagnostic | sequence generation evaluation | target-script validity, EOS/max-length, empty output를 translation score와 분리 | medium |

## Proposed Method: DCLR

메인 방법론 이름은 `Debiased Cross-Lingual Retrieval (DCLR)`로 둔다.

DCLR은 학습 모델 자체보다 evaluation/post-processing pipeline이다.

1. Sentence embedding extraction
   - model: XLM-R-base, third_try candidate, optional MLM200 initialization variants
   - layer: `8`, `last`, `last4`
   - pooling: mean without special tokens as main, first `<s>` as ablation

2. Representation dispersion
   - raw
   - global centering
   - language centering
   - language centering + PCA removal `top1/top3/top5`
   - whitening
   - optional chapter/book centering as diagnostic only

3. Similarity calibration
   - cosine
   - centered cosine
   - CSLS `k=10`
   - optional CSLS `k=5/20` sensitivity

4. Ranking and margin evaluation
   - Recall@1/5/10
   - MRR
   - mean rank
   - positive-random margin
   - positive-hard margin
   - hubness@10 max/entropy

5. Downstream bridge
   - frozen pair classification with transformed embeddings
   - target10-wide pair classification if enough aligned rows exist
   - decoder translation used only as final diagnostic, not as direct proof of DCLR

## Current Evidence Mapping

| Evidence | Current result | Supports | Limitation |
| --- | --- | --- | --- |
| append-only tokenizer audit | base ids changed `0`, appended rows `30,849` | controlled tokenizer intervention | does not prove semantic alignment |
| Glot500 scale comparison | v3.1 train mixture `297.5MB`, about `1/28,800` consumed chunks vs Glot500 budget | small controlled probe framing | not scale-comparable to Glot500 |
| MLM protocol | dynamic token MLM `15%`, BERT-style `80/10/10`, no NSP/contrastive | token prediction adaptation is well defined | MLM loss is not semantic objective |
| 200-step init MLM | `fvt` final dev loss `3.9218`, `focus` `3.9313`, `align` `4.0603` | initialization sensitivity after actual training | single-seed, short-budget result |
| same-meaning feature cosine | `mean_mlm200` `0.996556`, `fvt_mlm200` `0.990975`, base `0.986126` | target10 cosine attachment improves | all cosine values are too high |
| semantic feature retrieval | same-random gap tiny, hard margin negative, R@1/MRR weak | motivates DCLR and hard-negative ranking | raw MLM feature is not enough |
| pooling ablation | mean pooling beats CLS on R@1/MRR | main pooling should be mean, CLS only ablation | still weak absolute retrieval |
| Coptic-Syriac CSLS/centering | centered CSLS improves MRR and drops hubness; final Recall@1 still below `1%` | CSLS/centering direction is promising | not robust semantic retrieval yet |
| pair classification | final macro F1 improves: `cop->syr +0.0352`, `syr->cop +0.0718`; AUROC improves | shallow probe can extract cross-lingual signal | learned classifier, not raw similarity |
| decoder probe | third_try avoids `syr->cop` XLM-R empty/max-length collapse; chrF++ improves but remains low | target-script/generation collapse diagnostic | not high-quality translation |

Safe reading:

> Current evidence supports a layered diagnostic claim: append-only MLM adaptation improves token prediction and some representation usability, while raw cosine retrieval remains poorly calibrated. This motivates anisotropy-aware retrieval and hard-negative margin evaluation as the novelty direction.

Unsafe reading:

> The current model solves Coptic-Syriac translation or robust semantic retrieval.

## Experiment Plan

### P0. DCLR Retrieval and Margin Evaluation

Goal:

Check whether centering/PCA/whitening/CSLS improves ranking and hard-negative margin over raw cosine.

Dataset:

- primary: Coptic-Syriac aligned dev/final rows
- extension: target10 aligned Bible/item rows
- positive: same `item_id` across languages
- negatives:
  - random shifted negative
  - same-book negative
  - same-chapter negative
  - length-matched negative
  - nearest-neighbor negative under raw embedding

Experiment grid:

| Axis | Values |
| --- | --- |
| model | `xlmr_base`, third_try seed/mean, optional `random/mean/fvt/align/focus_mlm200` |
| layer | `8`, `last`, `last4` |
| pooling | mean without special tokens, first `<s>` |
| transform | raw, global center, language center, lang center + PCA-1/3/5, whitening |
| similarity | cosine, CSLS `k=10` |
| direction | `cop->syr`, `syr->cop`, target10 directed pairs |

Main score table:

| Model | Layer | Pooling | Transform | Similarity | Pos cos | Rand gap | Hard margin | R@1 | R@5 | R@10 | MRR | Hubness@10 |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

Expected artifacts:

| Artifact | Purpose |
| --- | --- |
| `dclr_retrieval_scores.tsv` | per-direction and per-setting ranking metrics |
| `dclr_pair_scores.tsv` | optional per-query positive/negative scores |
| `dclr_hard_negative_breakdown.tsv` | random vs hard negative margin |
| `dclr_hubness_summary.tsv` | hubness before/after CSLS |
| `dclr_map_points.tsv` | 2D map input after selected transforms |
| `dclr_results.md` | report-ready summary |

Pass condition:

- transformed/CSLS setting improves MRR and Recall@5/10 over raw cosine;
- positive-hard margin becomes less negative or positive;
- hubness@10 drops or does not worsen;
- improvement holds in both directions or target10 macro, not only one cherry-picked direction.

Fail condition:

- same cosine remains high but MRR/margin do not improve;
- CSLS reduces hubness but destroys retrieval;
- gains disappear under hard negatives.

### P0. 2D Map as Visualization, Not Main Metric

Goal:

Show whether same-meaning pairs become visually closer after debiasing.

Method:

- produce PCA/UMAP map from the same embeddings used in DCLR;
- color points by language;
- connect aligned positive pairs by thin lines;
- compare raw vs best DCLR transform;
- report quantitative metrics beside the map.

Important boundary:

> 2D map is an explanatory figure. The claim must be based on ranking, margin, and hubness, because projection can distort distances.

Expected artifacts:

| Artifact | Purpose |
| --- | --- |
| `dclr_2d_map_manifest.tsv` | figure inventory |
| `fig_raw_vs_dclr_map.png` | report figure |
| `fig_hard_negative_margin.png` | margin distribution figure |

### P1. Downstream Bridge With DCLR Features

Goal:

Check whether DCLR-transformed embeddings improve a learned downstream proxy beyond raw embeddings.

Tasks:

1. Pair classification
   - input features: `abs(e_src - e_tgt)`, `e_src * e_tgt`, cosine/CSLS score
   - labels: same `item_id` positive, hard negatives as negative
   - classifier: logistic regression or small MLP
   - metrics: macro F1, AUROC, AUPRC

2. Target10-wide pair classification
   - same design, macro-average by language pair
   - Coptic/Syriac separately reported

3. Optional book/topic classification
   - label: Bible book or coarse topic if labels are clean
   - use only as auxiliary evidence because book labels can reward topical shortcuts

Expected artifacts:

| Artifact | Purpose |
| --- | --- |
| `dclr_pair_classification_results.tsv` | raw vs DCLR downstream comparison |
| `target10_dclr_pair_classification_summary.tsv` | target10 macro result |
| `dclr_downstream_delta.md` | report interpretation |

Pass condition:

- DCLR features improve AUROC/AUPRC or macro F1 over raw features;
- hard-negative performance improves, not only random negative.

### P1. Relation to Decoder Diagnostics

Goal:

Keep generation evidence in the report, but do not overclaim it.

Analysis:

- correlate retrieval/MRR/margin with decoder chrF++ and collapse diagnostics;
- report target-script validity, EOS seen, hit max length, empty prediction rate, unique prediction rate;
- separate three axes:
  - semantic retrieval;
  - target-script availability;
  - generation quality.

Expected artifacts:

| Artifact | Purpose |
| --- | --- |
| `dclr_decoder_correlation.tsv` | retrieval metrics joined with decoder metrics |
| `decoder_claim_boundary.md` | safe/unsafe translation wording |

Safe conclusion if current pattern holds:

> DCLR/retrieval and decoder quality measure different failure modes. Retrieval can be strong by copying generic train verses, while the simple decoder reveals target-script collapse and repetition.

### P2. Optional Contrastive Adaptation

Goal:

If post-processing is not enough, train a small adaptation objective that directly optimizes positive-vs-hard-negative ranking.

Candidate method:

- name: `Hard-Negative Verse Contrastive Alignment (HNVCA)`
- encoder: frozen XLM-R/third_try plus projection head, or LoRA on upper layers
- positives: aligned Coptic-Syriac or target10 same `item_id`
- hard negatives: same chapter, length-matched, nearest-neighbor false positive
- loss:
  - InfoNCE, or
  - triplet margin loss

Controls:

- no train/dev/test item leakage;
- same negative construction as DCLR eval;
- compare against no-training DCLR;
- early stop on dev MRR, not train loss.

Expected artifacts:

| Artifact | Purpose |
| --- | --- |
| `hnvca_training_manifest.tsv` | train/dev/test split and hyperparameters |
| `hnvca_retrieval_results.tsv` | contrastive vs DCLR comparison |
| `hnvca_ablation.tsv` | projection-only vs LoRA, random vs hard negatives |

Claim boundary:

- If HNVCA improves retrieval and hard margin, it can become the strongest novelty.
- If it overfits or only improves random negatives, keep it as future work.

## Ablation Placement

| Ablation | Main question | Priority |
| --- | --- | --- |
| pooling: mean vs `<s>` | Is CLS appropriate for MLM-only encoder? | P0 |
| layer: 8 vs last vs last4 | Does Glot500-style layer 8 help retrieval? | P0 |
| transform: raw/center/PCA/whitening | Is anisotropy the core issue? | P0 |
| metric: cosine vs CSLS | Does hubness correction improve ranking? | P0 |
| negative type | Are gains robust to hard negatives? | P0 |
| initialization methods | Does MLM loss ranking transfer to semantic retrieval? | P1 |
| CSLS `k` | Is the result sensitive to neighborhood size? | P1 |
| contrastive objective | Does direct margin training beat no-training DCLR? | P2 |
| longer MLM budget | Does semantic retrieval catch up after more MLM? | P2 |

## Claim Gates

| Gate | Pass condition | Current state |
| --- | --- | --- |
| `PASS_TOKENIZER_CONTROL` | no base token id changes, append-only audit passes | pass |
| `PASS_MLM_ADAPTATION` | MLM dev loss improves after training under identical budget | partial pass |
| `PASS_COSINE_ATTACHMENT` | same-meaning cosine improves over XLM-R-base | partial pass |
| `PASS_DCLR_RETRIEVAL` | centering/PCA/CSLS improves MRR and margin over raw cosine | pending |
| `PASS_DCLR_HUBNESS` | hubness drops without destroying retrieval | partial evidence on Coptic-Syriac |
| `PASS_DOWNSTREAM_BRIDGE` | transformed/frozen features improve pair classification | pending |
| `PASS_TRANSLATION_DIAGNOSTIC` | decoder collapse metrics improve without claiming solved translation | partial pass |
| `PASS_CONTRASTIVE_EXTENSION` | optional HNVCA improves hard-negative retrieval over DCLR | pending |

## Final Report Structure

Recommended placement:

1. Motivation
   - low-resource vocabulary extension and semantic alignment problem
2. Controlled tokenizer extension
   - append-only protocol and audit
3. MLM adaptation
   - masking protocol, Glot500 scale comparison, init ablation
4. Problem diagnosis
   - same cosine high, hard margin negative, raw cosine calibration failure
5. Proposed method: DCLR
   - centering/PCA/whitening/CSLS and ranking/margin evaluation
6. DCLR experiments
   - retrieval, hard negatives, hubness, 2D map
7. Downstream bridge
   - pair classification and optional topic classification
8. Simple decoder translation diagnostic
   - chrF++, target-script validity, collapse analysis
9. Limitations and future work
   - contrastive adaptation, larger MLM budget, broader target10

## Safe Report Claims

Use:

> Raw cosine similarity is poorly calibrated for low-resource cross-lingual sentence equivalence after MLM-only adaptation.

Use:

> Centering/CSLS-style retrieval provides a more appropriate diagnostic than absolute cosine thresholding because it evaluates relative ranking and hubness.

Use:

> Append-only vocabulary extension preserves the base XLM-R id space, allowing downstream differences to be interpreted without destructive tokenizer replacement.

Use:

> The simple decoder result is a diagnostic of target-script/generation collapse, not evidence that translation is solved.

Avoid:

> The model solves Coptic-Syriac translation.

Avoid:

> Higher cosine alone proves semantic alignment.

Avoid:

> The tokenizer extension alone caused the downstream improvement.

Avoid:

> The current small-budget probe reproduces Glot500-scale training.

## Immediate Next Actions

1. Implement or rerun DCLR retrieval with raw, language-centering, PCA removal, whitening, and CSLS.
2. Add hard-negative breakdown for random, same-book/chapter, length-matched, and nearest-neighbor negatives.
3. Produce raw-vs-DCLR score table with MRR, Recall@k, margin, and hubness.
4. Generate a 2D map only after the quantitative table is fixed.
5. Run downstream pair classification using raw vs DCLR-transformed features.
6. Decide whether optional HNVCA contrastive adaptation is needed after P0/P1 results.

## Files To Cite

| File | Use |
| --- | --- |
| `idea.md` | raw cosine problem, pooling/layer/debiasing experiment sketch |
| `problem.md` | anisotropy, domain/style, hubness, hard-negative evaluation rationale |
| `survey.md` | BERT-flow, whitening, SimCSE, CSLS connection and DCLR framing |
| `../novelty_notes.md` | current evidence and safe/unsafe novelty boundaries |
| `../05_additional/plan.md` | Glot500 comparison, MLM protocol, feature proxy report bridge |
| `../04_ablation/init_mlm_probe/feature_similarity_results.md` | same-meaning feature similarity result |
| `../04_ablation/init_mlm_probe/pooling_comparison_results.md` | mean vs CLS pooling result |
| `../01_embedding_alignment/results.md` | Coptic-Syriac alignment and CSLS result |
| `../02_embedding_downstream/results.md` | pair classification downstream result |
| `../03_decoder_translation/results.md` | decoder translation and collapse diagnostic |
