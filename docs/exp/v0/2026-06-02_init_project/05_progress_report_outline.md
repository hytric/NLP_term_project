# Progress Report Outline

대상 일정:

- 2026-06-12: progress report
- 2026-06-19: final presentation
- 2026-07-03: term paper + GitHub link

## 1. 2026-06-12 Progress Report

권장 제목:

> Extending Multilingual Models to Coptic and Syriac: Vocabulary Adaptation and Pivot-Based NMT for Ancient Low-Resource Languages

### Slide / Section 1. Problem

- Coptic and Syriac are historically important ancient/liturgical languages.
- Mainstream multilingual NMT does not directly support them.
- Direct Coptic-Syriac parallel data is scarce.
- Existing tokenizers likely overfragment unseen scripts.

### Slide / Section 2. Course Objective Alignment

- Build Coptic -> Syriac and Syriac -> Coptic NMT.
- Evaluate with BLEU, chrF++, qualitative analysis.
- Include ablations: vocabulary extension, initialization, multitask/pivot, back-translation, fine-tuning strategy.

### Slide / Section 3. Survey Findings

- Glot500: horizontal scaling, XLM-R continued pretraining, 30K sentence threshold, vocabulary extension.
- Low-resource vocabulary expansion: random init is weak when data is small; Mean/Align initialization is promising.
- Tokenizer algorithms: SentencePiece unigram is the relevant baseline for XLM-R/NLLB/Glot500-style models.

### Slide / Section 4. Data Plan

- Coptic Scriptorium and UD Coptic for Coptic text.
- Bible Parallel Corpus for Coptic/Syriac/Greek/English verse-level alignment.
- SEDRA and CAL for Syriac resource discovery.
- Evaluation: 500-1000 held-out Bible-aligned sentences, manually check 50-100.

### Slide / Section 5. Research Question

Main:

> Which vocabulary extension and embedding initialization strategy most reliably improves representation and translation quality for Coptic and Syriac?

Sub:

- Does tokenization improve after joint Coptic+Syriac vocabulary extension?
- Does Mean/Align initialization beat Random?
- Does pivot/multitask training beat direct-only training?

### Slide / Section 6. Experiment Plan

1. Tokenization audit.
2. Joint Coptic+Syriac SentencePiece unigram tokenizer.
3. Vocabulary merge into Glot500 tokenizer.
4. Random vs Mean vs Align embedding initialization.
5. Continued pretraining.
6. NMT baseline and pivot/back-translation.

### Slide / Section 7. Expected Contributions

- Case study of academic-source recovery for languages missed by web-derived multilingual corpora.
- Controlled comparison of embedding initialization under ancient low-resource scripts.
- Tokenization-quality analysis connected to Coptic-Syriac NMT results.

### Slide / Section 8. Risks

- Coptic/Syriac direct parallel data may be tiny.
- Bible alignment can be coarse and domain-specific.
- Data licenses may limit redistribution.
- Decoder/NMT stage may require more engineering than tokenizer/encoder adaptation.

### Slide / Section 9. Next Week Plan

- Finish data inventory with actual counts.
- Run tokenizer audit on 100-1000 sampled sentences.
- Implement Mean initialization baseline.
- Decide whether Align can fit the schedule.

## 2. Final Presentation Skeleton

1. Motivation and gap
2. Data sources and preprocessing
3. Tokenizer audit results
4. Vocabulary extension method
5. Embedding initialization ablation
6. Continued pretraining setup
7. NMT setup: direct, pivot, multitask, back-translation
8. BLEU/chrF++ results
9. Qualitative examples
10. Limitations and future work

## 3. Term Paper Skeleton

### Abstract

One paragraph:

- problem: unsupported ancient low-resource languages
- method: vocabulary extension + initialization + pivot NMT
- data: Coptic/Syriac sources
- result: fill in after experiments
- contribution: fill in after ablations

### 1. Introduction

- Coptic/Syriac motivation
- multilingual model coverage gap
- tokenizer/embedding bottleneck
- project contributions

### 2. Related Work

- multilingual LMs and Glot500
- low-resource vocabulary expansion
- tokenizer algorithms
- low-resource NMT and back-translation

### 3. Data

- sources
- preprocessing
- split
- evaluation set
- license notes

### 4. Method

- tokenizer audit
- SentencePiece unigram extension
- embedding initialization
- continued pretraining
- NMT/pivot/back-translation

### 5. Experiments

- baselines
- ablations
- training settings
- evaluation metrics

### 6. Results

- tokenization table
- MLM/pseudo-ppl table
- NMT BLEU/chrF++ table
- qualitative examples

### 7. Discussion

- what improved and why
- where the method failed
- data/domain limitations
- broader implication for ancient/liturgical languages

### 8. Conclusion

- concise answer to the research question
- next steps

## 4. Minimal Reproducibility Checklist

- exact data source URLs and access dates
- preprocessing scripts and command lines
- tokenizer training command
- vocabulary merge command
- embedding initialization config
- training config and random seed
- evaluation command with sacrebleu signature
- checkpoint naming convention

## 5. Current Missing Evidence

- actual sentence counts
- tokenizer audit table
- first vocabulary extension run
- first initialization comparison
- first BLEU/chrF++ result
