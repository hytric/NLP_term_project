# Novelty Ranking

목표는 "재미있는 아이디어"가 아니라 2026-07-03까지 논문 형태로 방어 가능한 novelty를 고르는 것이다.
아래 평가는 현재 과제 일정, 구현 가능성, 실험 증명 가능성을 함께 반영한다.

## 1. Ranking Summary

| Rank | Novelty candidate | Paper strength | Feasibility | Main evidence needed | Decision |
| ---: | --- | --- | --- | --- | --- |
| 1 | Span-aware embedding initialization for Coptic/Syriac tokenizer extension | High | Medium | random vs mean vs align loss/chrF++ comparison | Primary novelty |
| 2 | Tokenization quality predicts low-resource ancient-language NMT quality | Medium-High | High | fertility/single-char ratio vs chrF++/BLEU correlation | Primary analysis |
| 3 | Academic-source recovery for Glot500-missed ancient languages | Medium-High | High | corpus inventory, sentence counts, coverage gap | Framing contribution |
| 4 | Forgetting-aware Glot500 extension | Medium | Medium | target-only vs mixed pretraining and old-language eval | Secondary ablation |
| 5 | Pivot-consistency synthetic data selection | High | Low-Medium | pivot consistency score + backtranslation improvement | Stretch novelty |

## 2. Primary Novelty: Span-Aware Embedding Initialization

### Claim

For unseen ancient scripts with limited training data, initializing newly added subword embeddings by character-span alignment between old and new tokenizers is more stable than random initialization and more corpus-aware than naive mean initialization.

### Why It Can Become A Paper

- It directly addresses the vocabulary bottleneck in the course guide.
- It has clear baselines: no extension, random, mean, align.
- It produces multiple measurable outcomes: MLM loss, pseudo-perplexity, tokenization metrics, BLEU, chrF++.
- It is not tied only to Coptic/Syriac; it generalizes to other unsupported scripts.

### Minimal Experiment

1. Train a joint Coptic+Syriac unigram tokenizer.
2. Merge genuinely new tokens into Glot500 tokenizer.
3. Initialize new embeddings with random, mean, and align.
4. Continue MLM pretraining on the same target corpus.
5. Compare validation loss, pseudo-perplexity, and first NMT baseline.

### Failure Mode

If Align is not better than Mean, the paper can still argue that simpler Mean initialization is sufficient for this data scale.
Then novelty shifts to "how much initialization matters" rather than "Align wins."

## 3. Primary Analysis: Tokenization Quality as Predictor

### Claim

For Coptic/Syriac NMT, sequence-level translation quality is partly predictable from tokenizer fragmentation metrics.

### Metrics

- average tokens per sentence
- character/token fertility
- single-character token ratio
- target-script token coverage
- sequence length reduction after extension
- chrF++ and BLEU after NMT training

### Why It Helps

Even if BLEU is low, this analysis can show mechanistic progress.
It also makes the project more than "we fine-tuned a model"; it becomes a study of why the model improves or fails.

## 4. Framing Contribution: Academic-Source Recovery

### Claim

Coptic and Syriac are not simply "data absent"; they are "pipeline absent."
Web-derived multilingual data collection misses scholarly, religious, and digital-humanities sources that are not well represented in Common Crawl/Wikipedia style pipelines.

### Evidence Needed

- Glot500 coverage gap: Coptic/Syriac absent from Glot500-c according to local tutorial/survey.
- Coptic Scriptorium, UD Coptic, Bible corpus, SEDRA, CAL availability.
- Sentence/token counts after cleaning.
- License and redistribution analysis.

### Positioning

This should be the introduction motivation, not the only technical contribution.
It gives the project a strong story, while the embedding/tokenization experiments provide the technical core.

## 5. Secondary Ablation: Forgetting-Aware Extension

### Claim

Target-only adaptation may improve Coptic/Syriac but hurt existing multilingual representation, while mixed Glot500 sampling can reduce forgetting.

### Minimal Experiment

- Compare target-only continued pretraining against target + small Glot500 sample.
- Use Coptic/Syriac pseudo-perplexity for target performance.
- Use a small existing Glot500 evaluation subset or multilingual sentence retrieval proxy for forgetting.

### Risk

This may require access to Glot500 evaluation data and compute.
If time is short, report it as a limitation or future experiment.

## 6. Stretch Novelty: Pivot-Consistency Synthetic Data

### Claim

Back-translated Coptic-Syriac synthetic pairs are better when selected by agreement across Greek/English pivot paths.

### Example

- Generate Coptic -> Greek -> Syriac.
- Generate Coptic -> English -> Syriac.
- Keep examples whose Syriac outputs are similar under chrF or embedding similarity.

### Risk

This requires multiple trained translation paths and enough compute.
It is a good final-paper extension only if earlier phases finish quickly.

## 7. Recommended Paper Thesis

Working thesis:

> The central bottleneck in adapting multilingual models to Coptic and Syriac is not only the scarcity of direct Coptic-Syriac parallel data, but the representational failure caused by unsupported scripts and overfragmented tokenization. A controlled vocabulary-extension pipeline with careful embedding initialization can produce more stable low-resource adaptation, and pivot-based NMT can then exploit the adapted representations for translation.

Short Korean version:

> Coptic-Syriac 번역의 핵심 병목은 direct parallel data 부족만이 아니라, 기존 multilingual model이 두 언어의 script/subword를 제대로 표현하지 못하는 데 있다. 따라서 tokenizer extension과 embedding initialization을 먼저 안정화하고, 그 위에 pivot/multitask NMT를 올리는 방식이 논문화 가능한 실험 설계다.

## 8. What To Avoid

- Novelty를 "Coptic-Syriac 번역기를 만들었다"로만 잡지 않는다. 데이터가 작아 성능이 낮으면 약해진다.
- BLEU만 보고 결론내리지 않는다. chrF++, tokenization metrics, qualitative examples를 같이 본다.
- 모든 실험을 다 하려 하지 않는다. random vs mean vs align 하나만 제대로 비교해도 논문 중심축이 생긴다.
- 라이선스 확인 없이 데이터를 학습/배포하지 않는다.
