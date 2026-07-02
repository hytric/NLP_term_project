# 05 Additional Final Report and Feedback

작성일: 2026-06-19

## Executive Verdict

`05_additional`은 추가 main experiment라기보다, v3.1 전체 결과를 Glot500식 low-resource evaluation 관점에서 방어 가능하게 묶는 보고서 섹션이다.

현재 결과로 가능한 최종 주장은 다음 수준이 가장 안전하다.

> v3.1은 XLM-R 기반 append-only vocabulary extension과 MLM continued adaptation을 작은 고정 budget에서 검증한 controlled diagnostic이다. 토크나이저 id 보존은 성공했지만, 내용 token MLM은 아직 실질적으로 확보되지 않았다. Sentence retrieval에서는 `xlmr_base` 대비 우월성을 주장하지 않고, `mlm200` 내부의 weak hubness-calibrated diagnostic으로만 해석한다. 현재 가장 강한 긍정 근거는 shallow pair-classification signal과 decoder target-script collapse 회복이다.

따라서 보고서의 핵심 결론은 "번역 성공"이 아니라:

> tokenizer preservation -> MLM adaptation -> weak representation attachment -> shallow downstream signal -> decoder collapse diagnostic

이라는 layered diagnostic story로 잡는 것이 좋다.

## Task-Wise Organization

최종 리포트는 파일/폴더 생성 순서가 아니라 `method.md`의 Glot500 evaluation task 기준으로 구성하는 것이 가장 읽기 쉽다. 자세한 템플릿은 `task_wise_report_guide.md`를 사용한다.

권장 task 단위:

| Task | Main question | Main result type |
| --- | --- | --- |
| Pseudoperplexity / MLM intrinsic | target language token prediction이 좋아졌는가? | MLM dev loss, future pseudoperplexity |
| Sentence Retrieval | aligned sentence/verse를 검색할 수 있는가? | cosine, margin, R@1, MRR, hubness, CSLS |
| Roundtrip Alignment | word/subword alignment가 roundtrip으로 유지되는가? | not run yet / future artifact |
| NER | English NER가 target language로 zero-shot transfer 되는가? | no gold labels / no claim |
| POS | POS label task에서 syntactic signal이 보이는가? | Coptic supervised POS pilot; not zero-shot |
| Text Classification | sentence/document-level semantic signal이 transfer 되는가? | pair-classification proxy: macro F1, AUROC |
| Translation Diagnostic | Coptic-Syriac generation collapse가 줄어드는가? | chrF++, script/EOS/empty diagnostics |

Tokenizer control, Glot500 scale comparison, MLM masking protocol, pooling ablation은 main task가 아니라 공통 setup 또는 ablation/limitation으로 둔다.

각 task 섹션은 다음 순서를 반복한다.

> Task Definition -> Data -> Model/Setup -> Metric -> Result -> Interpretation -> Claim Boundary -> Artifact

이렇게 쓰면 task마다 "숫자", "해석", "주장 가능 범위"가 분리되어 과장 없이 정리된다.

## Final Report

### 1. Glot500과의 관계

Glot500은 XLM-R-style MLM continued pretraining 이후 pseudoperplexity, sentence retrieval, roundtrip alignment, NER, POS, text classification 등으로 representation quality를 평가한다. `05_additional/idea.md`와 `05_additional/method.md`는 이 배경을 잘 정리한다.

v3.1은 같은 방법론 계열을 따른다.

- XLM-R 계열 encoder를 사용한다.
- vocabulary extension과 MLM adaptation을 사용한다.
- MLM loss만 보지 않고 retrieval, downstream, decoder diagnostic을 같이 본다.

하지만 규모는 Glot500과 비교할 수 없다.

| Item | Glot500-c / Glot500-m | v3.1 init MLM probe | Reading |
| --- | ---: | ---: | --- |
| corpus size | about `600GB` | `297.5MB` train mixture | about `1/2,017` |
| rows | about `1.5B` | `966,152` raw train lines | about `1/1,553` |
| train budget | `480K * 384` | `200 * 32` | `1/28,800` consumed chunks |
| objective | MLM | MLM | same family, not same scale |

Safe wording:

> Our experiment is inspired by Glot500's append-vocabulary and MLM adaptation protocol, but it is a small controlled probe rather than a reproduction of Glot500-scale pretraining.

Unsafe wording:

> We reproduce Glot500 training or Glot500-level low-resource adaptation.

### 2. Tokenizer Audit

Tokenizer control is the strongest clean pass.

| Check | Result |
| --- | ---: |
| base vocab size | `250002` |
| candidate vocab size | `280851` |
| appended tokens | `30849` |
| changed base token ids | `0` |
| changed special token ids | `0` |
| appended id violations | `0` |

Interpretation:

> The tokenizer intervention is controlled: existing XLM-R ids are preserved and only new pieces are appended.

Boundary:

> This proves structural compatibility, not semantic quality by itself.

### 3. MLM Training Protocol

The MLM probe uses standard HuggingFace/BERT-style token-level dynamic masking:

- `15%` of non-special tokens selected;
- selected tokens use `80/10/10`: `<mask>` / random token / unchanged;
- loss is computed only on selected token positions;
- no NSP, no sentence-pair objective, no whole-word masking, no contrastive semantic objective.

Important report implication:

> MLM eval loss is a masked-token prediction proxy. It does not directly measure sentence-level semantic alignment.

### 4. Initialization MLM Result

After identical `200` optimizer-step MLM training, `fvt` ranks best on target10 dev MLM loss, with `focus` very close.

| Rank | Init | Final dev loss | Delta vs `fvt` | Perplexity |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | `3.921798` | `0.000000` | `50.491170` |
| 2 | `focus` | `3.931313` | `0.009515` | `50.973852` |
| 3 | `align` | `4.060271` | `0.138473` | `57.990012` |
| 4 | `random` | `4.937548` | `1.015750` | `139.427975` |
| 5 | `mean` | `5.835072` | `1.913274` | `342.089214` |

Interpretation:

> `fvt` is the best token-prediction initialization under this single-seed, 200-step budget, but the gap to `focus` is tiny. Report this as initialization sensitivity, not final method proof.

### 5. Encoder Feature Similarity

The target10 same-meaning feature similarity probe is useful, but the result is mixed.

| Model | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | `0.986126` | `+0.000000` | `+0.000189` | `-0.003000` | `0.006874` | `0.020418` |
| `random_mlm200` | `0.993669` | `+0.007543` | `+0.000237` | `-0.002612` | `0.005793` | `0.021748` |
| `mean_mlm200` | `0.996556` | `+0.010430` | `+0.000208` | `-0.001656` | `0.005724` | `0.022055` |
| `fvt_mlm200` | `0.990975` | `+0.004849` | `+0.000215` | `-0.002530` | `0.004551` | `0.019034` |

Positive reading:

> Same-meaning cosine rises for several MLM200 variants, so target10 text appears better attached to the encoder space.

Negative reading:

> Same-random gaps are tiny, hard margins remain negative, and R@1/MRR remain weak. Therefore this does not pass as robust semantic retrieval.

Most important nuance:

> `fvt` wins MLM loss but does not win feature retrieval. MLM token prediction, absolute cosine attachment, and semantic discrimination must be reported as separate diagnostics.

### 6. Pooling Choice

Mean pooling should remain the main representation. CLS/first-`<s>` pooling is valid as an ablation only.

| Model | Mean R@1 | CLS R@1 | Mean MRR | CLS MRR |
| --- | ---: | ---: | ---: | ---: |
| `xlmr_base` | `0.006874` | `0.002862` | `0.020418` | `0.015012` |
| `random_mlm200` | `0.005793` | `0.004721` | `0.021748` | `0.018970` |
| `mean_mlm200` | `0.005724` | `0.004709` | `0.022055` | `0.019113` |
| `fvt_mlm200` | `0.004551` | `0.003802` | `0.019034` | `0.017251` |

Reason:

> XLM-R/RoBERTa-style MLM does not train the first token as a contrastive sentence embedding. In this experiment, mean pooling is consistently stronger on Recall@1/MRR.

### 7. Coptic-Syriac Alignment and CSLS

Coptic-Syriac final-test alignment should be treated as a raw diagnostic only. Because `xlmr_base` is not a report-ready comparison row, the safe reading is candidate-side retrieval remains very weak.

| Direction | Decoder chrF++ delta | MRR delta | Recall@1 delta | Margin delta |
| --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | `+2.2667` | `+0.0031` | `+0.0017` | `+0.0023` |
| `syr -> cop` | `+3.4949` | `+0.0075` | `+0.0013` | `+0.0009` |

CSLS/centering calibrates hubness:

- `cop -> syr` centered CSLS MRR: baseline `0.0099`, candidate `0.0219`;
- `cop -> syr` hubness@10 max drops from `0.3151` to `0.1057`;
- `syr -> cop` centered CSLS MRR: baseline `0.0124`, candidate `0.0220`;
- `syr -> cop` hubness@10 max drops from `0.1730` to `0.0418`.

Interpretation:

> CSLS/centering strengthens the weak-alignment diagnostic, but Recall@1 remains below `1%`, so it is not enough for a strong semantic retrieval claim.

### 8. Downstream Pair Classification

The strongest downstream signal is the frozen embedding pair classifier using `abs-diff + product + cosine`.

| Direction | Baseline macro F1 | Candidate mean macro F1 | Delta | Baseline AUROC | Candidate mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

Interpretation:

> The adapted embeddings contain a learnable Coptic-Syriac pair signal that a shallow classifier can extract.

Boundary:

> Raw cosine alone is inconsistent, and this result is Coptic-Syriac only. It is not yet target10-wide downstream transfer.

### 9. Simple Decoder Translation

The decoder result should be framed as a generation/collapse diagnostic, not a translation-quality success.

| Direction | Final chrF++ baseline | Final chrF++ candidate mean | Delta |
| --- | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `+3.4949` |

Positive:

- third_try improves held-out chrF++ over XLM-R-base under the same simple decoder setup;
- `syr -> cop` XLM-R-base collapses almost completely;
- third_try avoids empty-output collapse and reaches target-script validity `1.0`.

Important limitation:

- BLEU remains near zero;
- outputs remain short/repetitive/generic;
- `cop -> syr` still has high max-length rate;
- train-bank retrieval baseline beats the simple decoder in every direction/model group.

Safe wording:

> The adapted encoder/tokenizer helps a simple decoder avoid target-script collapse and improves chrF++ over the XLM-R-base decoder baseline, but the system is not yet a useful free-form Coptic-Syriac translator.

Unsafe wording:

> The model solves Coptic-Syriac translation.

## Claim Gates

| Gate | Current state | Report decision |
| --- | --- | --- |
| tokenizer control | pass | main positive evidence |
| MLM adaptation | partial pass | `fvt` best, `focus` close; content-token MLM not secured |
| cosine attachment | weak diagnostic | same cosine/raw baseline comparison should not drive claims |
| semantic retrieval | not pass | margin/R@1/MRR weak |
| Coptic-Syriac shallow downstream | partial pass | pair classifier improves |
| target10-wide downstream | pending | do not claim |
| decoder collapse recovery | partial pass | target-script collapse improves |
| translation quality | not pass | decoder is diagnostic only |

## Feedback

### What Is Strong

1. The report structure is defensible. `05_additional` correctly explains why MLM loss alone is not enough and why Glot500 evaluates with downstream/proxy tasks.
2. The append-only tokenizer audit is clean and should be shown early.
3. The Glot500 scale comparison prevents overclaiming and makes the small-budget nature explicit.
4. The feature similarity section correctly separates absolute cosine from margin/retrieval.
5. The downstream and decoder diagnostics give a reasonable positive story without pretending translation is solved.

### What Needs Tightening

1. Avoid calling `05_additional` an additional experiment. Call it "additional analysis/report packaging."
2. Replace "semantic alignment improved" with "weak hubness-calibrated diagnostic signal" unless margin and retrieval are also positive.
3. Do not let the high same-cosine numbers dominate the report. The key columns are same-random gap, hard margin, R@1, MRR, and hubness.
4. Make clear that `fvt` is best for MLM loss, not best for semantic retrieval.
5. Fill the incomplete `summary.md` downstream/decoder sections before using it as a final report source.
6. Add qualitative decoder examples in the term report, but label them as error analysis.
7. If time allows, add target10-wide DCLR/CSLS or target10-wide pair classification before making broad low-resource claims.

### Recommended Final Report Ordering

1. Motivation: low-resource ancient-language tokenizer/representation problem.
2. Method: append-only vocab extension and MLM continued adaptation.
3. Glot500 comparison: same method family, much smaller scale.
4. Tokenizer audit: id preservation and appended rows.
5. MLM protocol and initialization ablation.
6. Encoder feature similarity: same cosine vs margin/R@1/MRR.
7. Pooling ablation: mean pooling main, CLS ablation.
8. Coptic-Syriac alignment with CSLS/centering.
9. Frozen pair-classification downstream result.
10. Simple decoder translation and collapse diagnostics.
11. Limitations and next experiments.

### Next Experiments By Priority

| Priority | Experiment | Why |
| --- | --- | --- |
| P0 | fixed-mask MLM dev eval | dynamic eval masking adds noise |
| P0 | target10 CSLS/centering feature similarity | raw cosine is anisotropic and current CSLS is mostly Coptic-Syriac |
| P0 | hard-negative breakdown by book/chapter/length | checks whether Bible-domain shortcuts inflate scores |
| P1 | layer ablation: layer 8, last, last-4 | Glot500 uses layer 8 for retrieval/alignment style tasks |
| P1 | target10-wide pair classification | needed for broad downstream claim |
| P1 | pseudoperplexity-style eval | closer to Glot500 intrinsic language modeling evaluation |
| P2 | roundtrip/token alignment | closer to Glot500 word-level alignment diagnostic |
| P2 | longer MLM budget: 1K/5K steps | checks whether retrieval catches up after more adaptation |

## One-Sentence Conclusion

> v3.1 currently supports a careful diagnostic claim: append-only MLM adaptation preserves tokenizer compatibility and shows limited low-resource representation signals, while content-token MLM, robust semantic retrieval, and real Coptic-Syriac translation quality remain open.

## Files To Cite

| File | Use |
| --- | --- |
| `idea.md` | Glot500 low-resource evaluation overview |
| `method.md` | downstream/proxy task explanation |
| `plan.md` | report packaging and claim gates |
| `../00_tokenizer_audit/results.md` | append-only tokenizer audit |
| `../04_ablation/init_mlm_probe/glot500_size_comparison.md` | Glot500 scale comparison |
| `../04_ablation/init_mlm_probe/mlm_training_protocol.md` | masking/training protocol |
| `../04_ablation/init_mlm_probe/results.md` | initialization MLM result |
| `../04_ablation/init_mlm_probe/feature_similarity_results.md` | target10 same-meaning feature similarity |
| `../04_ablation/init_mlm_probe/pooling_comparison_results.md` | mean vs CLS pooling |
| `../01_embedding_alignment/results.md` | Coptic-Syriac alignment and CSLS |
| `../02_embedding_downstream/results.md` | pair classification downstream result |
| `../03_decoder_translation/results.md` | decoder translation and collapse diagnostics |
