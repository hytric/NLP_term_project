# Reference Notes

이 문서는 term report에서 어떤 reference를 어디에 쓰는지 정리한다. BibTeX entry는
`docs/paper/tex/references.bib`에 있다.

## Primary Baselines

1. Imani et al. 2023, **Glot500: Scaling Multilingual Corpora and Language Models to 500 Languages**
   - Local file: `docs/survey/2305.12182v2.pdf`
   - Use for: horizontal scaling framing, head/tail definition, 30,000 sentence' threshold, Glot500-c/Glot500-m pipeline, vocabulary extension + continued MLM, head/tail/all Table 4.
   - Key values used:
     - Glot500-c inclusion threshold: more than 30,000 sentence' units.
     - XLM-R vocab 250K, Glot500-m vocab 401K after adding about 151K new tokens.
     - MLM continued pretraining on 600GB corpus.
     - Evaluation metrics: PPPL, Tatoeba retrieval, Bible retrieval, text classification, NER, POS, roundtrip alignment.

2. Conneau et al. 2020, **Unsupervised Cross-lingual Representation Learning at Scale**
   - Use for: XLM-R-base/XLM-R-large baseline and 100-language head model framing.

## Tokenization

3. Kudo and Richardson 2018, **SentencePiece**
   - Local supporting note: `docs/survey/unigramLM.pdf`
   - Use for: SentencePiece as tokenizer library; UnigramLM mode; language-independent tokenizer/detokenizer.

4. Sennrich et al. 2016, **Neural Machine Translation of Rare Words with Subword Units**
   - Use for: BPE background if contrasting BPE with UnigramLM.

5. Course note, **The UnigramLM Tokenization Algorithm**
   - Local file: `docs/survey/unigramLM.pdf`
   - Use for: intuitive explanation of UnigramLM as latent segmentation + EM + pruning.

## Vocabulary Expansion and Initialization

6. Yamaguchi et al. 2025, **How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target Language Text?**
   - Local file: `docs/survey/2406.11477v3.pdf`
   - Use for: low-resource vocabulary expansion motivation; 30K sentences / 0.01GB setting; random initialization not always optimal; heuristic/source-tokenizer-based initialization as motivation.

7. Hewitt 2021, **Initializing New Word Embeddings for Pretrained Language Models**
   - Use for: mean initialization as a strong centroid baseline.

8. Course note, **Vocabulary Extension and Embedding Initialization for Fine-Tuning Foundational LLMs**
   - Local file: `docs/survey/vocab_extension_tutorial.pdf`
   - Use for: FVT/source-tokenizer decomposition, fertility, method matching, evaluation checklist, pitfalls.

9. Gee et al. 2022/2024, **Fast Vocabulary Transfer for Language Model Compression**
   - Use for: primary FVT reference; vocabulary transfer through source-tokenizer decomposition; compression/efficiency motivation.
   - Note: v5.2 uses the decomposition/embedding-transfer idea for vocabulary expansion ablation, not for model compression.

10. Minixhofer et al. 2022, **WECHSEL**
    - Use for: related cross-lingual embedding initialization using multilingual static embeddings.
    - Note: background only; v5.2 does not implement WECHSEL.

11. Dobler and de Melo 2023, **FOCUS**
    - Use for: related XLM-R/multilingual initialization approach using overlapping vocabulary anchors and auxiliary token embeddings.
    - Note: background only; v5.2 does not implement FOCUS.

## Evaluation

12. Devlin et al. 2019, **BERT**
   - Use for: MLM objective and masked token prediction background.

13. Artetxe and Schwenk 2019, **Massively Multilingual Sentence Embeddings**
    - Use for: sentence retrieval and multilingual sentence representation context.

## Local Experiment Artifacts

14. `docs/exp/v5.2/EXPERIMENT_DESIGN_KO.md`
    - Use for: final v5.2 design statement, Target7, initialization modes, hyperparameter alignment.

15. `docs/exp/v5.2/LIVE_STATUS.md`
    - Use for: current completion state of tokenizer, initializers, MLM runs, convergence jobs.

16. `docs/exp/v5.2/3_evaluation/v52_final_downstream_table.tsv`
    - Use for: step-4000 random/mean/FVT early diagnostic table only; do not use as the final convergence claim.

17. `docs/exp/v5.2/3_evaluation/v52_checkpoint_score_table.tsv`
    - Use for: PPPL and Tatoeba checkpoint trajectory.

18. `docs/exp/v5.2/3_evaluation/09_aggregation/main_head_tail_all.tsv`
    - Use for: final 50K head/tail/all score schema after all five initialization methods finish evaluation.

19. `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md`
    - Use for: target7 tokenization reduction and language-level fertility values.

20. `scripts/build_v5_initialized_checkpoint.py`
    - Use for: exact implementation of random, mean, FVT, weighted FVT, family-aware mean (`family_mean` in code); token identity copy; `<mask>` remap verification.

21. `tokenization/run.py`
    - Use for: exact tokenizer training and SentencePiece protobuf append procedure.

22. `preprocessing/merge_files.py`
    - Use for: language sampling equation, alpha=0.3, seen/target sampling plan.
