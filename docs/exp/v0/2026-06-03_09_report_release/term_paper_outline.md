# Term Paper Outline

작성일: 2026-06-04

## Working Title

Extending Multilingual Models to Ten Low-Resource Languages: Tokenizer Adaptation, Embedding Initialization, and Coptic/Syriac Translation Diagnostics

## Abstract Draft

This paper studies how a multilingual pretrained model can be extended to a small set of unsupported or underrepresented low-resource languages. We build a target10 adaptation pilot covering Coptic, Syriac, Cherokee, Ojibwa, Barasana-Eduria, Uspanteco, Nahuatl, Akawaio, Camsa, and Achuar-Shiwiar. The representation-side pipeline trains and merges a target10 SentencePiece vocabulary into Glot500, initializes new embeddings with Random and Mean strategies, and runs short continued MLM adaptation. The merged tokenizer sharply reduces overfragmentation for non-Latin scripts, and Mean initialization gives the best stable target10 MLM result. We then evaluate Coptic/Syriac translation as a downstream case study. Direct NMT, pivot, and retrieval-augmented neural diagnostics show that representation improvements alone are not enough for source-grounded generation: direct models collapse to formulaic fragments, pivot gates fail target-script transfer, and retrieval-augmented models remain copy-heavy. We conclude that target10 vocabulary extension is a useful representation step, but downstream translation needs stronger source-grounding or retrieval-editing objectives.

## 1. Introduction

Questions:

- What happens when a multilingual pretrained model is asked to handle scripts and languages underrepresented in its tokenizer?
- Can a small target-language vocabulary extension improve representation quality?
- Does better representation transfer directly into Coptic/Syriac translation quality?

Main thesis:

- Target10 vocabulary extension and Mean embedding initialization improve representation-side readiness.
- Downstream translation remains limited by source grounding and decoding/copy behavior.

Contributions:

1. A target10 low-resource-language adaptation pilot.
2. Tokenization audit showing severe Glot500 overfragmentation for Coptic/Syriac/Cherokee/Ojibwa.
3. Vocabulary merge and initialization ablation.
4. Coptic/Syriac NMT, pivot, retrieval, and retrieval-augmented diagnostics.
5. Copy-aware qualitative/error analysis.

## 2. Related Work

Draft themes:

- Multilingual pretrained models and low-resource transfer.
- Vocabulary adaptation and tokenizer extension.
- Embedding initialization for new subwords.
- Ancient/low-resource translation and Bible-aligned corpora.
- Retrieval-augmented generation and nearest-neighbor translation baselines.

Citation status:

- Initial citation spine drafted in `related_work_notes.md`.
- Still needs final Bible corpus/license citation pass before submission.

## 3. Data

Data source:

- Bible-derived aligned data for target10 and Coptic/Syriac/pivot experiments.

Target10 languages:

| ISO | Language | Script |
| --- | --- | --- |
| `cop` | Coptic | Coptic |
| `syr` | Syriac | Syriac |
| `chr` | Cherokee | Cherokee |
| `oji` | Ojibwa | Aboriginal Syllabics |
| `bsn` | Barasana-Eduria | Latin |
| `usp` | Uspanteco | Latin |
| `nhg` | Nahuatl (Tetelcingo) | Latin |
| `ake` | Akawaio | Latin |
| `kbh` | Camsa | Latin |
| `acu` | Achuar-Shiwiar | Latin |

Split summary:

- Shared target10 overlap: 4,892 verses.
- John is used as test for the main NMT examples.
- Mark-like dev split is used for validation, depending on availability.

Evidence:

- `docs/exp/2026-06-03_01_data_and_splits/results.md`
- `data/processed/target10/target_languages.tsv`
- `data/processed/target10/target10_stats.tsv`

## 4. Method

### 4.1 Tokenization Audit

Compare:

- XLM-R
- Glot500
- NLLB-200 distilled
- target10 SentencePiece
- merged Glot500+target10 tokenizer

Metrics:

- tokens per word
- tokens per character
- single-character token percentage
- `<unk>` percentage

### 4.2 Vocabulary Extension

Steps:

1. Train target10 SentencePiece unigram 16k tokenizer.
2. Merge target10 pieces into Glot500 tokenizer.
3. Validate tokenization improvements after merge.

Key artifact:

- `data/processed/target10/glot500_target10_spm16k`

### 4.3 Embedding Initialization

Compare:

- Random initialization
- Mean initialization over old-subtoken decompositions

Key artifacts:

- `data/processed/target10/initialized_models/glot500_target10_random`
- `data/processed/target10/initialized_models/glot500_target10_mean`

### 4.4 Continued MLM Adaptation

Run target10 MLM adaptation with Random and Mean initialized checkpoints.

Decision:

- Mean pilot10k selected for downstream NMT.

### 4.5 Downstream NMT And Retrieval Diagnostics

Families:

- Direct Coptic <-> Syriac NMT.
- English/Greek pivot gates.
- Retrieval baselines.
- Retrieval reranking.
- Source-candidate decision selection.
- Retrieval-augmented ByT5 generation with copy-aware controls.

## 5. Experiments

Experiment sequence:

1. Data and split construction.
2. Tokenization audit.
3. Vocabulary extension.
4. Embedding initialization.
5. MLM adaptation.
6. NMT baselines and retrieval diagnostics.
7. Pivot/back-translation gate.
8. Evaluation and qualitative analysis.
9. Source-candidate decision selection.

GPU policy:

- Use only physical GPU 3, NVIDIA RTX A6000.

## 6. Results

### 6.1 Tokenization

Key result:

- Syriac Glot500 tokens/word: 5.089 -> 1.601.
- Coptic Glot500 tokens/word: 5.274 -> 1.779.
- Cherokee Glot500 tokens/word: 5.254 -> 2.001.
- Ojibwa Glot500 tokens/word: 5.021 -> 2.205.

### 6.2 MLM Initialization

| Init | Stable eval loss | Stable perplexity |
| --- | ---: | ---: |
| Random | 7.0169 | 1,115.29 |
| Mean | 5.8343 | 341.84 |

### 6.3 Translation And Retrieval

Main message:

- Direct NMT runs complete but collapse qualitatively.
- Retrieval baselines are stronger than current neural translation.
- CPU-only candidate decision selection slightly improves retrieval selection.
- Neural retrieval augmentation improves overlap but mostly follows retrieved Coptic hints.

Key retrieval selector results:

- Top1 retrieval corpus chrF++: 22.5362.
- Existing feature reranker corpus chrF++: 24.5921.
- 10B validation-selected gradient-boosting selector corpus chrF++: 24.6862.
- 10B pairwise logistic selector corpus chrF++: 24.7438.
- Oracle@8 corpus chrF++: 28.3327.

Key 10C same-checkpoint control results:

- Correct pairwise source+retrieval chrF++: 18.3574.
- Source-only chrF++: 0.2729.
- Retrieved-only chrF++: 18.6220.
- Wrong-shift1 chrF++: 12.8253.
- Feature-selected top8 chrF++: 19.1558.
- Reading: retrieved-only slightly beats correct source+retrieval, so this is a negative source-grounded editing gate.

Evidence table:

- `docs/exp/2026-06-03_08_evaluation_analysis/final_metrics.tsv`
- `docs/exp/2026-06-03_08_evaluation_analysis/paper_tables.md`
- `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_results.tsv`
- `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_summary.md`
- `docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_summary.md`

## 7. Qualitative Analysis

Use:

- `docs/exp/2026-06-03_08_evaluation_analysis/qualitative_analysis.md`
- `docs/exp/2026-06-03_08_evaluation_analysis/error_taxonomy.md`

Main error categories:

- formulaic target-fragment collapse
- maximum-length repetition
- target-script failure
- retrieval copy dependence
- metric inflation from surface overlap
- undertrained empty output

## 8. Discussion

Core interpretation:

- Vocabulary extension helps representation, but generation quality is not automatically solved.
- chrF++ can be misleading when output is repetitive or copied.
- Retrieval is valuable as a baseline and input signal, but needs editing/source-grounding objectives.

Recommended future modeling:

- retrieval-editing or delta-generation targets;
- contrastive source-candidate objectives;
- coverage/source-grounding losses;
- stronger pretrained translation model with actual coverage of Coptic/Syriac scripts.

## 9. Limitations

Short version:

- Bible-domain only.
- Ancient/religious text style has high formulaic overlap.
- No final source-grounded neural translator yet.
- Retrieval and chrF++ require copy-aware controls.
- Back-translation not scaled because pivot gate failed.

Full limitations:

- `docs/exp/2026-06-03_09_report_release/limitations.md`

## 10. Conclusion

Target10 tokenizer and embedding adaptation form a reproducible representation-side pipeline for low-resource multilingual extension. The downstream experiments show that translation quality is still bottlenecked by source grounding, decoding, and retrieval-copy dependence. The project therefore supports a cautious but useful conclusion: vocabulary extension is necessary and measurable, but not sufficient for robust Coptic/Syriac translation.

## Appendix

Potential appendices:

- Command examples.
- Additional qualitative examples.
- Full metric tables.
- Storage/GPU reproducibility notes.
