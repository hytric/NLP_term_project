# Additional Analysis and Report Plan

작성일: 2026-06-19

## Purpose

`05_additional`은 main experiment를 하나 더 추가하는 섹션이 아니다.  
이 섹션의 목적은 지금까지의 질문과 결과를 term report에서 방어 가능한 형태로 정리하는 것이다.

핵심 질문:

> MLM continued training으로 low-resource language가 encoder space에 붙었는가, 그리고 그 signal을 어떤 proxy task로 안전하게 보고할 수 있는가?

따라서 `05_additional`은 다음 네 가지를 묶는다.

1. Glot500과의 방법론/규모 비교.
2. MLM masking/training protocol 설명.
3. encoder output feature similarity proxy task 설계와 결과 해석.
4. 추가 downstream/proxy task 우선순위.

## Current Evidence To Carry Forward

| Evidence | Current result | Report reading |
| --- | --- | --- |
| append-only tokenizer audit | base ids changed `0`, appended rows `30,849` | tokenizer replacement이 아니라 controlled vocabulary extension |
| Glot500 scale comparison | v3.1 train mixture `297.5MB`, Glot500 about `600GB`; budget `1/28,800` consumed chunks | Glot500-scale 재현이 아니라 small controlled probe |
| MLM protocol | token-level dynamic MLM, `15%`, BERT-style `80/10/10`, no NSP/contrastive loss | MLM loss는 token prediction proxy |
| 200-step init MLM loss | `fvt` final dev loss `3.9218`, `focus` `3.9313` | fvt가 best지만 focus와 근소; init sensitivity |
| same-meaning feature cosine | `mean_mlm200` `0.996556`, `fvt_mlm200` `0.990975`, base `0.986126` | positive attachment signal |
| semantic discrimination | same-random gap tiny, hard margin negative, R@1/MRR weak | cosine attachment와 semantic retrieval은 분리 |
| pooling ablation | mean pooling beats CLS on R@1/MRR | mean pooling main, CLS ablation |
| decoder probe | candidate avoids `syr -> cop` baseline collapse but retrieval baseline still stronger | translation quality claim은 unsafe; collapse diagnostic은 useful |

## Report Section Plan

### 1. Motivation: Why Additional Analysis Is Needed

Explain the mismatch:

- Glot500 trains with MLM, but evaluates representation through multiple downstream/proxy tasks.
- Our model also uses MLM, but MLM loss alone cannot prove semantic alignment.
- Therefore we need proxy tasks between MLM and downstream translation/classification.

Suggested wording:

> We follow the Glot500-style idea that MLM adaptation should be evaluated through representation and downstream probes, not only through masked-token loss. Because our run is much smaller than Glot500, we treat the results as controlled diagnostics rather than scale-comparable pretraining.

### 2. Glot500 Scale Comparison

Use `04_ablation/init_mlm_probe/glot500_size_comparison.md`.

Report table:

| Item | Glot500-c / Glot500-m | v3.1 probe | Reading |
| --- | ---: | ---: | --- |
| corpus | about `600GB` | `297.5MB` | small probe |
| rows | about `1.5B` | `966,152` raw train lines | not scale comparable |
| training budget | `480K * 384` | `200 * 32` | `1/28,800` consumed chunks |
| objective | MLM | MLM | method family comparable |

Claim boundary:

- Safe: “inspired by Glot500 vocabulary extension and MLM adaptation.”
- Unsafe: “we reproduce Glot500 training.”

### 3. MLM Training Protocol

Use `04_ablation/init_mlm_probe/mlm_training_protocol.md`.

Must explicitly state:

- Dynamic token-level MLM.
- `15%` non-special token selection.
- selected token replacement rule: `80% <mask>`, `10% random`, `10% unchanged`.
- loss only on selected token positions.
- no NSP, no whole-word masking, no contrastive semantic objective.
- eval loss is dynamically masked-token cross entropy on `701` dev chunks, not full-token loss.

Report implication:

> MLM loss measures token-prediction adaptation, not sentence semantic alignment.

### 4. Proxy Task: Same-Meaning Encoder Feature Similarity

Use `04_ablation/init_mlm_probe/feature_similarity_results.md`.

Proxy definition:

- Dataset: target10 MLM dev split.
- Same-meaning id: shared Bible verse `item_id`.
- Representation: encoder last hidden state, attention-mask mean pooling, L2 normalization.
- Scope: all `90` directed target10 language pairs.
- Metrics:
  - same-pair cosine;
  - same-random gap;
  - hard-negative margin;
  - Recall@1/5;
  - MRR;
  - hubness.

Report table:

| Model | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.986126 | +0.000000 | +0.000189 | -0.003000 | 0.006874 | 0.020418 |
| `random_mlm200` | 0.993669 | +0.007543 | +0.000237 | -0.002612 | 0.005793 | 0.021748 |
| `mean_mlm200` | 0.996556 | +0.010430 | +0.000208 | -0.001656 | 0.005724 | 0.022055 |
| `fvt_mlm200` | 0.990975 | +0.004849 | +0.000215 | -0.002530 | 0.004551 | 0.019034 |

Reading:

- same cosine improves for several MLM200 variants, so target10 text is better attached to the encoder space;
- however same-random gap is tiny and hard margin remains negative;
- therefore semantic discrimination is not solved.

Safe wording:

> The adapted models improve absolute same-meaning cosine, which is evidence of representation attachment. However, hard-negative margins and exact retrieval remain weak, indicating that MLM adaptation alone does not create robust sentence-level semantic discrimination.

### 5. Pooling Choice

Use `04_ablation/init_mlm_probe/pooling_comparison_results.md`.

Decision:

- Main metric: mean pooling.
- Ablation: CLS / first `<s>` token.

Reason:

- XLM-R/RoBERTa MLM does not explicitly train CLS as a sentence embedding.
- CLS sometimes raises absolute cosine but lowers R@1/MRR.

Report table:

| Model | Mean R@1 | CLS R@1 | Mean MRR | CLS MRR |
| --- | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.006874 | 0.002862 | 0.020418 | 0.015012 |
| `random_mlm200` | 0.005793 | 0.004721 | 0.021748 | 0.018970 |
| `mean_mlm200` | 0.005724 | 0.004709 | 0.022055 | 0.019113 |
| `fvt_mlm200` | 0.004551 | 0.003802 | 0.019034 | 0.017251 |

### 6. Downstream Bridge

Connect `05_additional` to existing `02_embedding_downstream` and `03_decoder_translation`.

Interpretation chain:

1. MLM loss improves: token prediction adaptation.
2. Same cosine improves: low-resource text attaches to representation space.
3. Margin/MRR weak: semantic discrimination remains weak.
4. Pair classification improves with shallow probe: semantic signal is learnable but not raw-cosine robust.
5. Decoder avoids target-script collapse: encoder/tokenizer helps generation mechanics, but translation quality remains weak.

Report conclusion:

> The strongest current story is not "translation solved." It is a layered diagnostic: tokenizer preservation works, MLM adaptation improves token prediction and cosine attachment, a shallow downstream probe can extract some cross-lingual signal, and the decoder avoids one collapse mode, but robust semantic retrieval/generation is not yet achieved.

## Additional Experiment Priority

These are optional follow-ups after the current report skeleton is fixed.

| Priority | Experiment | Why | Expected artifact |
| --- | --- | --- | --- |
| P0 | fixed-mask MLM dev eval | dynamic masking makes eval loss slightly noisy | `fixed_mask_mlm_eval.tsv` |
| P0 | target10 feature similarity with CSLS/centering | raw cosine is anisotropic | `target10_csls_feature_summary.tsv` |
| P0 | book/chapter-matched hard negatives | Bible domain shortcuts inflate random negatives | `hard_negative_breakdown.tsv` |
| P1 | layer ablation: layer 8, last, last-4 average | Glot500 uses layer 8 for retrieval-style tasks | `pooling_layer_ablation.tsv` |
| P1 | target10-wide pair classification | check whether shallow probe extracts signal across all languages | `target10_pair_classification_results.tsv` |
| P1 | pseudoperplexity-style eval | closer to Glot500 monolingual evaluation than random MLM dev loss | `pseudo_perplexity_results.tsv` |
| P2 | roundtrip/token alignment | Glot500-style word/subword alignment diagnostic | `roundtrip_alignment_results.tsv` |
| P2 | longer MLM budget: 1K/5K steps | check whether feature retrieval catches up after more adaptation | `long_mlm_budget_summary.tsv` |

## Execution Order If Time Remains

1. Fixed-mask MLM eval.
2. CSLS/centering for target10 feature similarity.
3. Hard-negative breakdown.
4. Layer/pooling ablation.
5. Target10-wide pair classification.
6. Longer MLM budget only if compute allows.

Rationale:

- First stabilize measurement noise.
- Then address anisotropy/hubness.
- Then test if feature signal becomes useful under a learned shallow probe.
- Only then spend compute on longer training.

## Claim Gates

| Gate | Pass condition | Current state |
| --- | --- | --- |
| `PASS_TOKENIZER_CONTROL` | no base token id changes, append-only audit passes | pass |
| `PASS_MLM_ADAPTATION` | MLM dev loss improves after training under identical budget | partial pass, fvt/focus strong |
| `PASS_COSINE_ATTACHMENT` | same cosine improves over XLM-R-base | partial pass |
| `PASS_SEMANTIC_RETRIEVAL` | margin and MRR improve over XLM-R-base without hubness worsening | not pass |
| `PASS_DOWNSTREAM_SIGNAL` | frozen/shallow downstream probe improves over baseline | partial pass on Coptic-Syriac |
| `PASS_TRANSLATION_QUALITY` | simple decoder beats baseline and retrieval/collapse checks are healthy | not pass |

## Final Report Position

Recommended final report ordering:

1. Append-only tokenizer method and audit.
2. Glot500 methodology/scale comparison.
3. MLM protocol and initialization ablation.
4. Encoder feature similarity proxy:
   - cosine attachment score;
   - margin/retrieval failure;
   - pooling ablation.
5. Downstream pair classification.
6. Simple decoder translation and collapse diagnostics.
7. Limitations and next experiments.

## Files To Cite

| File | Use |
| --- | --- |
| `idea.md` | Glot500 low-resource evaluation overview |
| `method.md` | Glot500 downstream task explanations |
| `../04_ablation/init_mlm_probe/glot500_size_comparison.md` | scale comparison |
| `../04_ablation/init_mlm_probe/mlm_training_protocol.md` | MLM masking/training details |
| `../04_ablation/init_mlm_probe/results.md` | init MLM loss ablation |
| `../04_ablation/init_mlm_probe/feature_similarity_results.md` | same-meaning feature similarity |
| `../04_ablation/init_mlm_probe/pooling_comparison_results.md` | mean vs CLS pooling |
| `../02_embedding_downstream/results.md` | pair classification |
| `../03_decoder_translation/results.md` | decoder translation diagnostics |
