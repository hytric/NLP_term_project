# Method-Style Task Results

작성일: 2026-06-19

## Run Summary

`method.md`의 Glot500-style task 구분에 맞춰 `05_additional` 결과를 재정리하고, 빈 GPU `0`, `3`을 사용해 sampled pseudo-perplexity evaluation을 추가로 실행했다.

GPU 사용:

- GPU `0`: `xlmr_base`, `fvt_mlm200`, `focus_mlm200` pseudoPPL.
- GPU `3`: `random_mlm200`, `mean_mlm200`, `align_mlm200` pseudoPPL.
- GPU `1`, `2`: 기존 프로세스가 있어 사용하지 않음.

새로 생성한 주요 artifacts:

| Artifact | Task | Description |
| --- | --- | --- |
| `result/` | all tasks | task-wise report-ready result documents |
| `pseudoperplexity_scores.tsv` | Pseudoperplexity | per-language sampled pseudoPPL scores |
| `pseudoperplexity_summary.tsv` | Pseudoperplexity | model-level sampled pseudoPPL summary |
| `pseudoperplexity_summary_expanded_only.tsv` | Pseudoperplexity | report-ready pseudoPPL summary excluding degenerate `xlmr_base` row |
| `pseudoperplexity_tokenization_diagnostics.tsv` | Pseudoperplexity | tokenization diagnostic explaining low `xlmr_base` pseudoPPL |
| `pseudoperplexity_accuracy_scores.tsv` | Pseudoperplexity | per-language top-k prediction diagnostic |
| `pseudoperplexity_accuracy_summary.tsv` | Pseudoperplexity | model-level all-token/content-token top-k diagnostic |
| `pseudoperplexity_gold_probability_scores.tsv` | Pseudoperplexity | average gold-token probability score, percent view |
| `pseudoperplexity_prediction_samples.tsv` | Pseudoperplexity | content-token prediction examples |
| `target10_sentence_retrieval_csls_scores.tsv` | Sentence Retrieval | target10-wide raw/centered/CSLS pair scores |
| `target10_sentence_retrieval_csls_summary.tsv` | Sentence Retrieval | target10-wide CSLS macro summary |
| `target10_sentence_retrieval_csls_results.md` | Sentence Retrieval | short CSLS report |
| `coptic_pos_results_replay_safe.tsv` | POS | Coptic UD POS pilot results re-aggregated under v3.1 |
| `coptic_pos_summary_replay_safe.tsv` | POS | POS pilot summary |

## Task 1. Pseudoperplexity / MLM Intrinsic Evaluation

### Task Definition

Pseudoperplexity evaluates whether a masked LM can predict real target-language tokens when each token is masked and scored.

The task question is:

> After MLM continued training, does the model predict target10 low-resource language tokens better?

This is an intrinsic token-level evaluation. It should not be read as translation quality or sentence-level semantic alignment.

For an autoregressive LM, perplexity can be computed left-to-right. For an XLM-R/Glot500-style bidirectional masked LM, we instead mask one token at a time and score the original token:

```text
Original: I went to the library.
Step 1:   <mask> went to the library. -> score "I"
Step 2:   I <mask> to the library.    -> score "went"
Step 3:   I went <mask> the library.  -> score "to"
```

The average token negative log likelihood is then exponentiated to obtain pseudo-perplexity. Lower is better.

### Data and Setup

There are two intrinsic MLM signals in v3.1.

1. Dynamic MLM dev loss:
   - target10 low-resource dev split only, `701` chunked samples;
   - HuggingFace dynamic MLM collator;
   - `15%` non-special token selection;
   - BERT-style `80/10/10` mask/random/unchanged replacement;
   - loss only on selected token positions.

2. Sampled strict pseudoPPL:
   - target10 low-resource dev rows from `parallel_item_manifest.tsv`;
   - first `50` dev rows per language, `500` rows total per model;
   - max length `128`;
   - one non-special token masked and scored at a time;
   - compared models: `xlmr_base` and five `mlm200` init variants.

Important distinction:

> `xlmr_base` is the baseline model, not a high-resource evaluation language. All rows in this task are target10 low-resource dev text.

Important caveat:

> PseudoPPL is tokenizer-sensitive. `xlmr_base` and expanded-tokenizer candidates do not have identical token units, so base-vs-candidate pseudoPPL should be treated as diagnostic only. The safer comparison is among the expanded-tokenizer `mlm200` variants.

The tokenization diagnostic shows why this caveat matters:

| Language | Model | Tokens | Unique tokens | Top token | Top token rate |
| --- | --- | ---: | ---: | --- | ---: |
| `cop` | `xlmr_base` | `726` | `2` | `▁` | `0.964187` |
| `cop` | `fvt_mlm200` | `1795` | `446` | `▁` | `0.442340` |
| `chr` | `xlmr_base` | `749` | `5` | `▁` | `0.775701` |
| `chr` | `fvt_mlm200` | `1648` | `379` | `▁` | `0.478762` |
| `oji` | `xlmr_base` | `1028` | `6` | `▁` | `0.896887` |
| `oji` | `fvt_mlm200` | `2352` | `527` | `▁` | `0.485544` |

So `xlmr_base` can look artificially strong in pseudoPPL because the base tokenizer collapses several low-resource scripts into very few easy-to-predict pieces such as `▁` and punctuation.

### Result

Dynamic MLM dev loss:

| Rank | Init | Final dev loss | Delta vs `fvt` | Perplexity |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | `3.921798` | `0.000000` | `50.491170` |
| 2 | `focus` | `3.931313` | `0.009515` | `50.973852` |
| 3 | `align` | `4.060271` | `0.138473` | `57.990012` |
| 4 | `random` | `4.937548` | `1.015750` | `139.427975` |
| 5 | `mean` | `5.835072` | `1.913274` | `342.089214` |

Sampled strict pseudoPPL:

`xlmr_base` is excluded from the report table because the tokenization diagnostic shows degenerate scoring behavior. The raw artifact still keeps the row for transparency.

| Model | Phase | Weighted mean NLL | Weighted pseudoPPL | Macro mean NLL | Macro pseudoPPL |
| --- | --- | ---: | ---: | ---: | ---: |
| `align_mlm200` | mlm200 | `4.950712` | `141.275524` | `4.941329` | `139.956170` |
| `fvt_mlm200` | mlm200 | `5.002871` | `148.839893` | `5.001087` | `148.574587` |
| `focus_mlm200` | mlm200 | `5.054046` | `156.655071` | `5.052181` | `156.363199` |
| `random_mlm200` | mlm200 | `5.548407` | `256.828019` | `5.574280` | `263.559777` |
| `mean_mlm200` | mlm200 | `6.428914` | `619.500824` | `6.496823` | `663.031898` |

### 수치와 실제 예측 매칭 점검

PseudoPPL 수치가 낮다고 해서 실제 단어를 잘 맞춘다고 바로 말할 수는 없다. 추가로 top-k prediction diagnostic을 계산해 보니, 전체 token 기준 top-1은 약 `43%`지만 이는 `▁` 공백 경계 token과 punctuation을 맞춘 효과가 크게 섞여 있다.

평균 정답 token 확률 score는 `exp(-weighted_mean_nll)`로 계산한다. 즉 pseudoPPL의 역수에 가까운 값이며, 모델이 masked 위치의 실제 gold token에 평균적으로 몇 % 확률을 줬는지를 나타낸다.

| Rank | Model | Weighted mean NLL | Weighted pseudoPPL | 평균 정답 token 확률 score | Percent |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `align_mlm200` | `4.986757` | `146.460676` | `0.006828` | `0.6828%` |
| 2 | `fvt_mlm200` | `5.033308` | `153.439754` | `0.006517` | `0.6517%` |
| 3 | `focus_mlm200` | `5.090770` | `162.514902` | `0.006153` | `0.6153%` |
| 4 | `random_mlm200` | `5.564147` | `260.902633` | `0.003833` | `0.3833%` |
| 5 | `mean_mlm200` | `6.439363` | `626.007745` | `0.001597` | `0.1597%` |

따라서 상위 세 모델도 정답 token에 평균 `0.6~0.7%` 정도의 확률만 준다. 이 score는 `random/mean`보다 상대적으로 높지만, 절대적으로는 1% 미만이므로 "잘 맞춘다"는 의미가 아니다.

내용 token만 따로 보면 실제 매칭률은 매우 낮다.

| Model | 전체 top-1 | 전체 평균 gold prob | 내용 token top-1 | 내용 token top-5 | 내용 token top-10 | 내용 token 평균 gold prob |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `align_mlm200` | `0.436359` | `0.006828` | `0.045114` | `0.077521` | `0.096517` | `0.000213` |
| `fvt_mlm200` | `0.427400` | `0.006517` | `0.040080` | `0.084566` | `0.110627` | `0.000213` |
| `focus_mlm200` | `0.434602` | `0.006153` | `0.040108` | `0.076205` | `0.094909` | `0.000175` |
| `random_mlm200` | `0.430646` | `0.003833` | `0.040033` | `0.070260` | `0.088453` | `0.000083` |
| `mean_mlm200` | `0.435263` | `0.001597` | `0.037271` | `0.064516` | `0.081685` | `0.000016` |

예측 샘플도 실제 내용 token을 잘 맞춘다고 보기 어렵다.

| Model | Language | Gold token | Gold prob | Top-1 prediction | Top-5 hit |
| --- | --- | --- | ---: | --- | ---: |
| `align_mlm200` | `cop` | `ⲦⲀ` | `0.000086` | `.` | `0` |
| `align_mlm200` | `cop` | `ⲘⲠⲒⲈⲨⲀⲄⲄⲈⲖⲒⲞⲚ` | `0.000059` | `.` | `0` |
| `align_mlm200` | `chr` | `ᎧᏃᎮᏛ` | `0.000136` | `.` | `0` |
| `fvt_mlm200` | `bsn` | `yigu̶` | `0.056677` | `̶` | `1` |
| `fvt_mlm200` | `cop` | `ⲠⲬⲢⲒⲤⲦⲞⲤ` | `0.000056` | `.` | `0` |

따라서 이 결과는 "잘 맞춘다"가 아니라 "`align/fvt/focus`가 `random/mean`보다 덜 나쁘다"로 해석해야 한다. 현재 pseudoPPL은 low-resource token prediction의 상대적 안정성 diagnostic이지, 실제 lexical reconstruction 품질을 강하게 주장할 수 있는 결과가 아니다. 더 엄밀히 말하면, target10 low-resource의 내용 token MLM은 아직 실질적으로 확보되지 않았다.

### Interpretation

In absolute sampled pseudoPPL, `xlmr_base` has the lowest value. This should not be interpreted as real low-resource modeling quality because the tokenization diagnostic shows degenerate base-tokenizer behavior on Coptic/Cherokee/Ojibwa.

The meaningful pseudoPPL comparison is among expanded-tokenizer `mlm200` variants.

Among expanded-tokenizer `mlm200` variants, the sampled pseudoPPL ranking is:

> `align` < `fvt` < `focus` < `random` < `mean`

Dynamic MLM dev loss selects `fvt`, with `focus` nearly tied. Sampled pseudoPPL places `align`, `fvt`, and `focus` ahead of `random` and `mean`. The two intrinsic metrics are not identical, but they agree that structured initialization variants are more stable than `random`/`mean` under this small fixed budget.

Important clarification:

> `mean` initialization is the worst variant in dynamic MLM dev loss and sampled pseudoPPL. It should not be interpreted as good for intrinsic token prediction.

The difference between dynamic MLM loss and sampled pseudoPPL is expected because:

- pseudoPPL masks every scored token one at a time;
- the sample uses `50` rows per language;
- dynamic MLM loss samples only about `15%` of tokens;
- tokenizer/token distribution can affect pseudoPPL strongly.

Most important report nuance:

> MLM token prediction and semantic retrieval are separate diagnostics. `fvt` can be best on dynamic MLM loss without being best on sentence retrieval or translation.

Suggested report wording:

> Pseudoperplexity/MLM intrinsic evaluation shows that initialization affects low-resource masked-token prediction. Dynamic MLM dev loss selects `fvt`, while sampled pseudoPPL places `align`, `fvt`, and `focus` ahead of `random` and `mean`. We treat this as token-level adaptation evidence, not as proof of sentence-level semantic alignment.

More precise wording:

> All pseudoPPL evaluations are performed on target10 low-resource dev text. `xlmr_base` is included only as a baseline model on the same low-resource data, not as a high-resource evaluation condition.

### Claim Boundary

Allowed:

> Dynamic MLM loss and sampled pseudoPPL provide intrinsic evidence that initialization affects target10 token prediction. `fvt/focus/align` are the strongest variants across these intrinsic diagnostics.

Not allowed:

> This proves sentence-level semantic alignment or translation quality.

## Task 2. Sentence Retrieval

### Task Definition

Sentence Retrieval evaluates whether aligned Bible verses across languages can be retrieved in encoder space.

### Data and Setup

- Data: target10 MLM-dev feature caches.
- Scope: all `90` directed target10 language pairs.
- Representation: mean-pooled encoder features.
- Score types: `raw_cosine`, `centered_cosine`, `csls_k10`, `centered_csls_k10`.

### Selected Result

`xlmr_base` is excluded from the report-ready comparison table. As in pseudoPPL, base-tokenizer representations can be degenerate for several target10 scripts, so this table should compare only expanded-tokenizer `mlm200` variants. Raw artifacts still keep `xlmr_base` for transparency.

| Model | Score | Margin | R@1 | R@5 | R@10 | MRR | Hubness@10 max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `random_mlm200` | `centered_csls_k10` | `-0.563356` | `0.012318` | `0.041759` | `0.068257` | `0.036425` | `0.077437` |
| `mean_mlm200` | `centered_csls_k10` | `-0.637304` | `0.010675` | `0.038409` | `0.065668` | `0.034450` | `0.084290` |
| `align_mlm200` | `centered_csls_k10` | `-0.473661` | `0.009456` | `0.034559` | `0.058497` | `0.031894` | `0.087349` |
| `focus_mlm200` | `centered_csls_k10` | `-0.516167` | `0.008680` | `0.033440` | `0.057186` | `0.030713` | `0.085429` |
| `fvt_mlm200` | `centered_csls_k10` | `-0.480777` | `0.008798` | `0.032826` | `0.057600` | `0.030593` | `0.088414` |

### Glot500 Comparison

This is not an apples-to-apples reproduction of Glot500 sentence retrieval. Glot500 reports English-aligned Tatoeba/Bible Top-10 accuracy using layer-8 average word embeddings and cosine nearest-neighbor search. The v3.1 result is a target10 low-resource-to-low-resource Bible/dev proxy using mean-pooled cached features and centered-CSLS.

| Evaluation | Metric | XLM-R-B tail | Glot500-m tail | Glot500-m all | v3.1 proxy best |
| --- | --- | ---: | ---: | ---: | ---: |
| Glot500 Sentence Retrieval Tatoeba | Top-10 acc | `32.6%` | `59.8%` | `70.7%` | `NA` |
| Glot500 Sentence Retrieval Bible | Top-10 acc | `7.4%` | `43.2%` | `47.3%` | `NA` |
| v3.1 target10 Bible/dev proxy | R@10 | `NA` | `NA` | `NA` | `6.83%` |

The scale gap is large: Glot500-m reaches `43.2%` Bible tail Top-10, while the best v3.1 proxy R@10 is `6.83%`. Because the datasets, language-pair direction, pooling layer, score, and metric differ, this comparison should be used only to show that the current proxy is far from Glot500-level sentence retrieval evidence.

### Interpretation

CSLS/centering substantially reduces hubness relative to raw cosine scoring, but this should be read as score calibration rather than proof of model-level improvement. The report-ready comparison is restricted to `mlm200` variants. Under that restriction, `random_mlm200` has the best centered-CSLS MRR in this diagnostic, followed by `mean_mlm200`.

Important clarification:

> The `mean_mlm200` ranking here is only for the Sentence Retrieval centered-CSLS MRR metric. It conflicts with MLM intrinsic evaluation, where `mean` is the worst variant. This is another example that token prediction and sentence retrieval measure different behavior.

However, absolute retrieval remains weak:

- R@1 remains around `0.9%` to `1.2%`;
- R@10 peaks at `6.83%`;
- hard margins are still negative;
- `fvt`, the best dynamic MLM-loss model, is not the best retrieval model.

### Claim Boundary

Allowed:

> Target10-wide centered CSLS provides a hubness-calibrated retrieval diagnostic over `mlm200` variants, but the absolute retrieval signal is still weak.

Not allowed:

> This table proves superiority over `xlmr_base`, or that the adapted encoder achieves robust target10 sentence retrieval.

## Task 3. Roundtrip Alignment

### Status

Not completed in v3.1/05_additional.

Current artifacts include sentence-level retrieval and CSLS diagnostics, but no word/subword-level SimAlign or roundtrip result.

### Claim Boundary

Allowed:

> Roundtrip alignment remains planned future work.

Not allowed:

> v3.1 improves Glot500-style roundtrip alignment.

## Task 4. NER

### Status

Not completed.

No local Coptic/Syriac or target10 WikiANN-style NER gold labels were found in the current v3.1 evidence.

### Claim Boundary

No NER transfer claim should be made.

## Task 5. POS Tagging

### Task Definition

POS tagging evaluates token-level syntactic labeling. Glot500 uses English fine-tuning followed by target-language zero-shot evaluation.

### Current v3.1 Evidence

The available local result is a **Coptic UD POS supervised pilot**, re-aggregated under `05_additional`. It is useful as POS-task evidence, but it is not the same as Glot500 English-to-target zero-shot POS.

### Result

| Metric | Baseline | Candidate mean | Delta / status |
| --- | ---: | ---: | --- |
| test token accuracy | `0.253182` | `0.259963` | `+0.006781` |
| positive checkpoint seeds | `NA` | `3/3` | all replay-safe seeds improve token accuracy |
| test macro F1 | `0.163298` | `0.160642` | `-0.002656` |

### Interpretation

The replay-safe candidates slightly improve Coptic POS token accuracy over XLM-R-base in all three checkpoint seeds, but macro F1 is slightly lower. This is a weak POS pilot, not a broad POS transfer result.

### Claim Boundary

Allowed:

> A Coptic UD POS pilot shows a small token-accuracy gain for replay-safe candidates.

Not allowed:

> v3.1 passes Glot500-style zero-shot POS transfer or target10-wide POS evaluation.

## Task 6. Text Classification

### Task Definition

Glot500 uses Taxi1500-style text classification. v3.1 does not yet have full Taxi1500-style labels for target10, so the current evidence is a pair-classification proxy.

### Current Proxy

- Task: classify whether Coptic-Syriac sentence pairs share the same Bible `item_id`.
- Encoder: frozen.
- Classifier: logistic regression.
- Best features: `abs(e_src - e_tgt) + e_src * e_tgt + cosine`.

### Result

| Direction | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

### Interpretation

This is the strongest downstream-style signal: a shallow classifier extracts a stronger Coptic-Syriac same-verse signal from adapted embeddings than from XLM-R-base embeddings.

### Claim Boundary

Allowed:

> The adapted frozen embeddings improve a Coptic-Syriac pair-classification proxy.

Not allowed:

> This is full Taxi1500-style text classification or target10-wide downstream transfer.

## Task 7. Project-Specific Translation Diagnostic

### Task Definition

Translation is not one of Glot500's core encoder-only evaluation tasks, but it is required for this Coptic-Syriac project. It should be reported as a project-specific diagnostic.

### Result

| Direction | Final chrF++ baseline | Final chrF++ candidate mean | Delta |
| --- | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `+3.4949` |

Key collapse diagnostic:

| Direction | Model group | EOS seen | Hit max length | Empty pred rate | Script valid | chrF++ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `syr -> cop` | XLM-R-base | `0.0219` | `0.9781` | `1.0` | `0.0` | `0.0` |
| `syr -> cop` | third_try mean | `0.9970` | `0.0030` | `0.0` | `1.0` | `3.4949` |

### Interpretation

The adapted encoder/tokenizer helps the simple decoder avoid severe target-script collapse and improves chrF++. But BLEU remains near zero, outputs are repetitive/generic, and retrieval-only baselines still beat the decoder.

### Claim Boundary

Allowed:

> The adapted model improves a simple-decoder diagnostic and avoids a major target-script collapse mode.

Not allowed:

> The system is a useful Coptic-Syriac translator.

## Final Task Status

| `method.md` task | v3.1/05_additional status | Current claim |
| --- | --- | --- |
| Pseudoperplexity / MLM intrinsic | sampled pseudoPPL + gold-prob/content-token diagnostic added | `align/fvt/focus` are less bad than `random/mean`; content-token MLM is not yet secured |
| Sentence Retrieval | target10 CSLS + `mlm200` report filter added | `xlmr_base` comparison excluded; retrieval signal remains weak |
| Roundtrip Alignment | missing | future work |
| NER | unavailable | no claim |
| POS | Coptic supervised pilot re-aggregated | weak token-accuracy gain, not zero-shot POS |
| Text Classification | Coptic-Syriac proxy done | shallow pair-classification improves |
| Translation Diagnostic | done | collapse improves, translation quality remains weak |

## Final Reading

The most defensible `05_additional` conclusion is:

> Following the Glot500-style task taxonomy, v3.1 now has evidence for intrinsic MLM/pseudoPPL behavior, a weak hubness-calibrated sentence-retrieval diagnostic, a Coptic POS pilot, a Coptic-Syriac classification proxy, and a project-specific decoder collapse diagnostic. The pseudoPPL result should be read as relative intrinsic improvement only: average gold-token probability is still around `0.6~0.7%` for the strongest variants, and content-token MLM is not yet reliable. Sentence retrieval should not be used to claim superiority over `xlmr_base`; the report-ready comparison excludes that row. It still lacks roundtrip alignment, NER, and full Taxi1500-style text classification. Therefore, append-only MLM adaptation shows several limited diagnostics of low-resource representation usability, but robust lexical prediction, semantic retrieval, and useful Coptic-Syriac translation remain open.
