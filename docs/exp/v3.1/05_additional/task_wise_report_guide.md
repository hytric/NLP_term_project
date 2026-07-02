# Method-Style Task Report Guide

작성일: 2026-06-19

## Purpose

최종 리포트의 task 구분은 `method.md`처럼 Glot500 평가 방식에 맞춰 정리한다.

즉, tokenizer audit이나 MLM initialization은 독립 downstream task가 아니라 **공통 method/setup 및 ablation**으로 배치하고, 결과 섹션은 아래 evaluation task 중심으로 구성한다.

1. Pseudoperplexity / MLM intrinsic evaluation
2. Sentence Retrieval
3. Roundtrip Alignment
4. NER
5. POS Tagging
6. Text Classification
7. Project-specific Translation Diagnostic

각 task는 같은 템플릿으로 정리한다.

> Task Definition -> Data -> Model/Setup -> Metric -> Result -> Interpretation -> Claim Boundary -> Artifact

이 구조를 쓰면 Glot500 논문식 task 설명과 우리 실험 결과가 일대일로 연결된다.

## Report-Level Structure

### 1. Common Setup

여기에는 task 결과가 아니라 모든 task의 공통 배경을 넣는다.

- Base model: `xlm-roberta-base`
- Candidate: third_try replay-safe checkpoints and MLM200 init variants
- Tokenizer: append-only vocabulary extension
- Tokenizer audit: existing XLM-R ids changed `0`, appended tokens `30,849`
- Training objective: MLM continued adaptation
- Glot500 scale boundary: v3.1 is a small controlled probe, not Glot500-scale reproduction

Suggested wording:

> Following the Glot500 evaluation style, we do not treat MLM loss alone as proof of downstream quality. We evaluate the adapted encoder through intrinsic masked-token prediction, retrieval/alignment probes, shallow downstream classification, and a project-specific decoder diagnostic.

### 2. Evaluation Tasks

Use `method.md` ordering as the main result ordering.

| Report Task | Glot500 analogue | Current v3.1 status |
| --- | --- | --- |
| Pseudoperplexity / MLM intrinsic | pseudoperplexity | partial: MLM dev loss done; fixed-mask/pseudoperplexity follow-up needed |
| Sentence Retrieval | Tatoeba/Bible sentence retrieval | done for Coptic-Syriac; target10 same-meaning feature retrieval done |
| Roundtrip Alignment | Bible word/subword roundtrip alignment | not yet run; proposed/future unless implemented |
| NER | WikiANN zero-shot NER | not available for Coptic/Syriac target data |
| POS | UD zero-shot POS | Coptic supervised POS pilot available; not Glot500-style zero-shot |
| Text Classification | Taxi1500-style classification | proxy done: Coptic-Syriac same-verse pair classification |
| Translation Diagnostic | term-project-specific extension | done: simple decoder + retrieval baseline + collapse diagnostics |

## Task 1. Pseudoperplexity / MLM Intrinsic Evaluation

### Task Definition

Pseudoperplexity asks whether the masked LM assigns high probability to real tokens in the target language. For XLM-R/Glot500-style encoders, this is the closest intrinsic evaluation to language-modeling quality.

In current v3.1, the completed proxy is dynamic MLM dev loss, not strict one-token-at-a-time pseudoperplexity.

An additional sampled one-token-at-a-time pseudoPPL run has now been added under `05_additional`.

### Data

- Eval split: target10 dev text
- Scope: target10 low-resource languages only
- HF chunked samples: `701`
- Languages: target10

### Model/Setup

- Objective: token-level MLM
- Masking: dynamic `15%` non-special tokens
- Replacement: `80% <mask>`, `10% random`, `10% unchanged`
- Loss: selected token positions only
- Training budget: `200` optimizer steps for initialization probe

### Metric

| Metric | Meaning |
| --- | --- |
| final dev MLM loss | dynamic masked-token cross entropy |
| perplexity | `exp(final dev loss)` |
| zero-to-final drop | adaptation effect under fixed budget |

### Result

Dynamic MLM dev loss:

| Rank | Init | Final dev loss | Delta vs `fvt` | Perplexity |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | `3.921798` | `0.000000` | `50.491170` |
| 2 | `focus` | `3.931313` | `0.009515` | `50.973852` |
| 3 | `align` | `4.060271` | `0.138473` | `57.990012` |
| 4 | `random` | `4.937548` | `1.015750` | `139.427975` |
| 5 | `mean` | `5.835072` | `1.913274` | `342.089214` |

Sampled strict pseudoPPL among expanded-tokenizer `mlm200` variants:

| Model | Weighted mean NLL | Weighted pseudoPPL |
| --- | ---: | ---: |
| `align_mlm200` | `4.950712` | `141.275524` |
| `fvt_mlm200` | `5.002871` | `148.839893` |
| `focus_mlm200` | `5.054046` | `156.655071` |
| `random_mlm200` | `5.548407` | `256.828019` |
| `mean_mlm200` | `6.428914` | `619.500824` |

Note: pseudoPPL is tokenizer-sensitive. `xlmr_base` showed degenerate tokenization on several low-resource scripts, so it should be excluded from the report table and kept only as a diagnostic raw row.

### Interpretation

`fvt` is the best dynamic MLM-loss initialization under this single-seed, 200-step budget, but `focus` is very close. The sampled strict pseudoPPL run ranks `align/fvt/focus` ahead of `random/mean`, with `align` best in the sample. `mean` is the worst intrinsic token-prediction variant here. This supports an initialization-sensitivity claim, not a final semantic-transfer claim.

### Claim Boundary

Allowed:

> Under a small fixed MLM budget, initialization affects target10 masked-token prediction. Dynamic MLM dev loss favors `fvt`/`focus`, while sampled pseudoPPL places `align/fvt/focus` ahead of `random/mean`.

Not allowed:

> This proves robust sentence-level semantic alignment or translation quality.

### Artifact

- `../04_ablation/init_mlm_probe/results.md`
- `../04_ablation/init_mlm_probe/mlm_training_protocol.md`
- `../04_ablation/init_mlm_probe/glot500_size_comparison.md`

## Task 2. Sentence Retrieval

### Task Definition

Sentence Retrieval asks whether aligned sentences or verses in two languages are close enough in encoder space that the correct target sentence can be retrieved.

This corresponds most directly to Glot500's Tatoeba/Bible sentence retrieval evaluation.

### Data

Two retrieval-style evaluations are currently available.

1. Coptic-Syriac final/dev retrieval from the v3.1 translation split.
2. target10 same-meaning MLM dev feature retrieval over all `90` directed language pairs.

### Model/Setup

- Encoder hidden states
- Mean pooling over attention mask as main pooling
- CLS/first `<s>` pooling as ablation
- L2-normalized embeddings
- Similarity: raw cosine, plus centered cosine/CSLS for Coptic-Syriac

### Metric

| Metric | Meaning |
| --- | --- |
| same/aligned cosine | cosine for the true aligned pair |
| random gap | aligned score minus random negative |
| hard margin | aligned score minus nearest wrong target |
| Recall@1/5 | exact aligned retrieval |
| MRR | ranking quality |
| hubness@10 | nearest-neighbor concentration |

### Target10 Same-Meaning Result

| Model | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `0.986126` | `+0.000000` | `+0.000189` | `-0.003000` | `0.006874` | `0.020418` |
| `random_mlm200` | `0.993669` | `+0.007543` | `+0.000237` | `-0.002612` | `0.005793` | `0.021748` |
| `mean_mlm200` | `0.996556` | `+0.010430` | `+0.000208` | `-0.001656` | `0.005724` | `0.022055` |
| `fvt_mlm200` | `0.990975` | `+0.004849` | `+0.000215` | `-0.002530` | `0.004551` | `0.019034` |

### Coptic-Syriac CSLS Result

| Direction | Score type | Baseline MRR | Candidate MRR | Delta | Baseline hubness@10 max | Candidate hubness@10 max | Delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `centered_csls_k10` | `0.0099` | `0.0219` | `+0.0120` | `0.3151` | `0.1057` | `-0.2094` |
| `syr -> cop` | `centered_csls_k10` | `0.0124` | `0.0220` | `+0.0096` | `0.1730` | `0.0418` | `-0.1312` |

### Target10-Wide Centered CSLS Result

`xlmr_base`는 raw diagnostic row로만 유지하고, report-ready 비교에서는 제외한다. 최종 표는 expanded-tokenizer `mlm200` variants 내부 비교로 제한한다.

| Model | Score | R@1 | R@5 | R@10 | MRR | Hubness@10 max |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `random_mlm200` | `centered_csls_k10` | `0.012318` | `0.041759` | `0.068257` | `0.036425` | `0.077437` |
| `mean_mlm200` | `centered_csls_k10` | `0.010675` | `0.038409` | `0.065668` | `0.034450` | `0.084290` |
| `align_mlm200` | `centered_csls_k10` | `0.009456` | `0.034559` | `0.058497` | `0.031894` | `0.087349` |
| `focus_mlm200` | `centered_csls_k10` | `0.008680` | `0.033440` | `0.057186` | `0.030713` | `0.085429` |
| `fvt_mlm200` | `centered_csls_k10` | `0.008798` | `0.032826` | `0.057600` | `0.030593` | `0.088414` |

Glot500 scale reference: Glot500-m reports `43.2%` Bible tail Top-10 accuracy, while the best v3.1 target10 proxy R@10 is `6.83%`. This is only a scale comparison because the datasets, pair direction, score, and metric differ.

### Interpretation

CSLS/centering reduces hubness in both Coptic-Syriac and target10-wide retrieval diagnostics. However, this is score calibration, not proof of model-level improvement. Exact retrieval remains weak, hard margins remain negative, Recall@1 stays around `1%`, and R@10 peaks at `6.83%` in target10-wide centered CSLS.

### Claim Boundary

Allowed:

> The `mlm200` variants show weak sentence-retrieval and attachment differences after hubness correction.

Not allowed:

> This proves superiority over `xlmr_base`, or the model achieves robust semantic sentence retrieval.

### Artifact

- `../04_ablation/init_mlm_probe/feature_similarity_results.md`
- `../04_ablation/init_mlm_probe/pooling_comparison_results.md`
- `../01_embedding_alignment/results.md`
- `../01_embedding_alignment/csls_retrieval_metric_summary.tsv`
- `target10_sentence_retrieval_csls_results.md`
- `target10_sentence_retrieval_csls_summary.tsv`

## Task 3. Roundtrip Alignment

### Task Definition

Roundtrip Alignment evaluates word/subword-level cross-lingual alignment. A token is aligned through one or more languages and then back to the original language; success means it returns to the original token.

This is closer to Glot500's SimAlign/Bible roundtrip diagnostic than to sentence retrieval.

### Current v3.1 Status

Not completed yet.

Current files include sentence-level retrieval/alignment and decoder diagnostics, but no word/subword-level SimAlign or roundtrip result artifact has been produced.

### Required Data

- Parallel Bible/item-aligned sentences
- Token/subword-level representations
- Alignment method such as SimAlign or a local nearest-neighbor token alignment implementation

### Recommended Metric

| Metric | Meaning |
| --- | --- |
| roundtrip accuracy | fraction of source tokens that return to original token |
| alignment coverage | fraction of tokens with a valid alignment |
| script/language breakdown | whether Coptic/Syriac fail differently |

### Claim Boundary

Allowed now:

> Roundtrip alignment is a planned Glot500-style diagnostic.

Not allowed now:

> v3.1 improves word-level roundtrip alignment.

### Artifact To Produce

- `roundtrip_alignment_results.tsv`
- `roundtrip_alignment_results.md`

## Task 4. NER

### Task Definition

NER evaluates token-level named entity transfer, usually by fine-tuning on English NER and testing zero-shot on target languages.

### Current v3.1 Status

Not completed.

There is no current Coptic/Syriac or target10 WikiANN-style gold NER artifact in v3.1.

### Report Placement

Mention as a Glot500 task that is not feasible in the current dataset.

Suggested wording:

> We do not report NER because the current Coptic/Syriac target data does not include WikiANN-style named-entity gold labels. We instead use sentence retrieval and pair classification as label-light proxy tasks.

### Claim Boundary

Do not make any NER transfer claim.

## Task 5. POS Tagging

### Task Definition

POS tagging evaluates syntactic transfer, typically by fine-tuning on English UD POS and evaluating zero-shot on target-language UD treebanks.

### Current v3.1 Status

A Coptic UD POS supervised pilot has been re-aggregated under `05_additional`.

Important caveat:

> This is not Glot500-style English-to-target zero-shot POS. It is a Coptic supervised POS pilot using local UD Coptic data.

### Result

| Metric | Baseline | Candidate mean | Delta / status |
| --- | ---: | ---: | --- |
| test token accuracy | `0.253182` | `0.259963` | `+0.006781` |
| positive checkpoint seeds | `NA` | `3/3` | all replay-safe seeds improve token accuracy |
| test macro F1 | `0.163298` | `0.160642` | `-0.002656` |

### Report Placement

Mention as POS-task evidence, but clearly separate it from Glot500 zero-shot POS.

Suggested wording:

> We include a Coptic UD POS supervised pilot as a POS diagnostic. It shows a small token-accuracy improvement for replay-safe candidates, but it is not an English-to-target zero-shot POS result and macro F1 does not improve.

### Claim Boundary

Allowed:

> Coptic supervised POS token accuracy improves weakly in the replay-safe pilot.

Not allowed:

> v3.1 passes Glot500-style zero-shot POS or target10-wide POS transfer.

## Task 6. Text Classification

### Task Definition

Text Classification evaluates whether sentence/document-level meaning transfers across languages after English or high-resource fine-tuning.

Glot500 uses Taxi1500-style multilingual text classification. v3.1 currently uses a proxy classification task instead.

### Data

- Coptic-Syriac same-verse pair data
- Positive: same `item_id`
- Negative: shifted and hard negative pairs

### Model/Setup

- Frozen encoder embeddings
- Classifier: logistic regression
- Best feature set: `abs(e_src - e_tgt) + e_src * e_tgt + cosine`

### Metric

| Metric | Meaning |
| --- | --- |
| macro F1 | balanced classification quality |
| AUROC | pair-separation quality |

### Result

| Direction | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

### Interpretation

The adapted embeddings contain a stronger learnable Coptic-Syriac same-verse signal than XLM-R-base embeddings. This is the strongest current downstream-style result.

### Claim Boundary

Allowed:

> The adapted frozen embeddings improve a Coptic-Syriac pair-classification proxy.

Not allowed:

> This is a full Taxi1500-style text classification result or target10-wide downstream transfer result.

### Artifact

- `../02_embedding_downstream/results.md`
- `../02_embedding_downstream/pair_classification_results.tsv`
- `../02_embedding_downstream/pair_classification_delta_summary.tsv`

## Task 7. Project-Specific Translation Diagnostic

### Task Definition

Translation is not one of Glot500's main encoder-only evaluation tasks, but it is required for the Coptic-Syriac project goal. Treat it as a project-specific downstream diagnostic, not as the main proof of representation quality.

### Data

- Directions: `cop -> syr`, `syr -> cop`
- Train: `5389`
- Dev: `678`
- Final test: `1006`

### Model/Setup

- Frozen encoder
- One-layer Transformer decoder
- Same decoder setup for XLM-R-base and candidate
- Candidate seeds: `13`, `17`, `23`

### Metric

| Metric | Meaning |
| --- | --- |
| chrF++ / BLEU | surface translation similarity |
| script valid | generated target script health |
| EOS seen / hit max length | termination behavior |
| empty pred rate | collapse diagnostic |
| unique pred rate / top pred rate | output diversity/collapse |

### Result

| Direction | Final chrF++ baseline | Final chrF++ candidate mean | Delta |
| --- | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `+3.4949` |

Key collapse result:

| Direction | Model group | EOS seen | Hit max length | Empty pred rate | Script valid | chrF++ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `syr -> cop` | XLM-R-base | `0.0219` | `0.9781` | `1.0` | `0.0` | `0.0` |
| `syr -> cop` | third_try mean | `0.9970` | `0.0030` | `0.0` | `1.0` | `3.4949` |

### Interpretation

The adapted encoder/tokenizer helps the decoder avoid severe target-script collapse and improves chrF++ over XLM-R-base. However, BLEU remains near zero, outputs remain repetitive/generic, and train-bank retrieval beats the decoder.

### Claim Boundary

Allowed:

> The adapted model improves simple-decoder diagnostics and avoids one major collapse mode.

Not allowed:

> The system is a useful Coptic-Syriac translator.

### Artifact

- `../03_decoder_translation/results.md`
- `../03_decoder_translation/decoder_collapse_metric_summary.tsv`
- `../03_decoder_translation/retrieval_vs_decoder_summary.tsv`

## Final Task-Wise Claim Table

| `method.md` task | v3.1 artifact status | Current claim |
| --- | --- | --- |
| Pseudoperplexity / MLM intrinsic | partial | dynamic MLM dev loss shows `fvt`/`focus` advantage |
| Sentence Retrieval | partial/done | `xlmr_base` comparison excluded; weak CSLS/hubness-calibrated diagnostic only |
| Roundtrip Alignment | missing | future work |
| NER | unavailable | no claim |
| POS | Coptic supervised pilot | weak token-accuracy gain; not zero-shot POS |
| Text Classification | proxy done | Coptic-Syriac pair-classification improves |
| Translation Diagnostic | done | decoder collapse improves, translation quality still weak |

## Final Conclusion Template

> Following the Glot500-style task taxonomy, v3.1 currently has evidence for relative intrinsic MLM differences, weak hubness-calibrated sentence-retrieval diagnostics, a Coptic-Syriac classification proxy, and a project-specific decoder collapse diagnostic. It does not yet provide roundtrip alignment, NER, POS, or full Taxi1500-style text classification evidence. Therefore the safe conclusion is that append-only MLM adaptation shows limited diagnostics of low-resource representation usability, but content-token MLM, robust semantic retrieval, and useful Coptic-Syriac translation remain future work.
