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
     - Evaluation metrics: PPPL, Tatoeba retrieval, Bible retrieval, text classification, NER, POS, roundtrip alignment (Table 3).
     - **Evaluation protocol (§5)**: supervised task(NER, Text)는 English fine-tune + dev early stopping + target zero-shot, LR 2e-5 Adam; retrieval/roundtrip/PPPL은 fine-tune 없는 frozen encoder. 원문: "Since training data does not exist for some languages, we finetune on English ... and evaluate zero-shot transfer." (POS는 compute 제약으로 본 보고서 미보고.)

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
    - Use for: Tatoeba sentence retrieval dataset and multilingual sentence representation context.

14. Hu et al. 2020, **XTREME: A Massively Multilingual Multi-task Benchmark**
    - Use for: English fine-tune → target zero-shot cross-lingual transfer protocol; retrieval nearest-neighbor setup. 우리 tagging eval 코드(`run_tag.py`)의 계보.

15. Pan et al. 2017, **Cross-lingual Name Tagging and Linking (WikiANN/PAN-X)**
    - Use for: NER dataset and BIO/PER-LOC-ORG label scheme.

16. Ma et al. 2023, **Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages**
    - Use for: text classification task; English fine-tune, batch 16; Glot500 Table 3 정식 task. Note: 본 실험은 target test(PBC 저작권)가 없어 English-only로만 평가.

17. Salazar et al. 2020, **Masked Language Model Scoring**
    - Use for: pseudoperplexity (PPPL) definition; one-by-one masking; linguistic acceptability 근거.

18. Dufter et al. 2018, **Roundtrip alignment evaluation**
    - Use for: gold 없이 multilingual 표현 품질을 보는 roundtrip alignment metric.

## Local Experiment Artifacts

20. `docs/exp/v5.2/EXPERIMENT_DESIGN_KO.md`
    - Use for: final v5.2 design statement, Target7, initialization modes, hyperparameter alignment.

21. `docs/exp/v5.2/LIVE_STATUS.md`
    - Use for: current completion state of tokenizer, initializers, MLM runs, convergence jobs.

22. `docs/exp/v5.2/3_evaluation/11_inference/downstream_head_tail_all.tsv`
    - Use for: **50K five-way downstream table** (random/mean/FVT/weighted_FVT/family_mean × PPPL/Tatoeba/Bible/NER/Roundtrip/Text). 본문 §6.2의 main source. NER 포함 완료(POS 미보고).

23. `docs/exp/v5.2/3_evaluation/v52_ppt_current_table.md`
    - Use for: init vs XLM-R-B/L·Glot500-m baseline 비교 참조값.

24. `docs/exp/v5.2/Plot/loss/convergence_5way_loss_curve.{png,tsv}`
    - Use for: 50K 5-way MLM training loss 최종값·궤적 (§6.2 main figure).

25. `docs/exp/v5.2/3_evaluation/11_inference/similarity_maps/similarity_10k50k_summary.tsv`
    - Use for: 10K→50K representation/family similarity 궤적 및 2D embedding map(§7).

26. `docs/exp/v5.2/0_tokenizer/03_tokenization_effect/results_ko.md`
    - Use for: target7 tokenization reduction and language-level fertility values.

27. `scripts/build_v5_initialized_checkpoint.py`
    - Use for: exact implementation of random, mean, FVT, weighted FVT, family-aware mean (`family_mean` in code); token identity copy; `<mask>` remap verification.

28. `tokenization/run.py`
    - Use for: exact tokenizer training and SentencePiece protobuf append procedure.

29. `preprocessing/merge_files.py`
    - Use for: language sampling equation, alpha=0.3, seen/target sampling plan.

30. `evaluation/tagging/run_tag.py`, `evaluation/text_classification/zero_shot_train.py`, `evaluation/retrieval/*`, `evaluation/round-trip/evaluate_roundtrip.py`
    - Use for: downstream task 구현 및 하이퍼파라미터(§5.6); XTREME→Glot500 zero-shot 프로토콜.
