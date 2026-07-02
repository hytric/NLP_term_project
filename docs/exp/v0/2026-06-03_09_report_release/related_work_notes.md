# Related Work Notes

작성일: 2026-06-04

목적: final paper의 Related Work 섹션에 바로 옮길 수 있도록, 현재 실험 주장과 연결되는 문헌 근거를 정리한다.

## Positioning

This project sits between multilingual representation adaptation and extremely low-resource translation diagnostics. The main claim should not be that the current system solves Coptic/Syriac translation. The stronger claim is narrower: target10 vocabulary extension reduces tokenizer overfragmentation and mean-initialized continued MLM gives a better representation-side checkpoint, while downstream generation still fails without stronger source-grounding objectives.

## Multilingual Pretraining For Low-Resource Coverage

XLM-R established a strong multilingual encoder baseline at CommonCrawl scale, but its coverage is still bounded by the languages and scripts represented in its training mixture and tokenizer. Glot500 pushes the horizontal scaling direction further by training over 500 languages and explicitly studying how corpus size, script, related-language support, and model capacity affect multilingual representations. Our work follows this horizontal-scaling motivation, but narrows the intervention to a small target10 extension where we can audit tokenizer behavior, embedding initialization, and downstream Coptic/Syriac translation.

NLLB is the natural large multilingual MT comparison point because it targets broad translation coverage. In this project, it mainly serves as a tokenizer/model-coverage diagnostic rather than a direct solved baseline: unsupported scripts can still be poor inputs even when the model family is multilingual.

## Tokenization And Vocabulary Adaptation

SentencePiece motivates language-independent subword training directly from raw text, which matches our target10 setup because the languages use mixed scripts and should not require language-specific pretokenization. The tokenizer-quality literature also gives a direct rationale for our audit: multilingual tokenizers can under-serve individual languages, and replacing or adapting the tokenizer can improve monolingual downstream behavior.

Our empirical hook is the target10 overfragmentation table. For example, Glot500 tokenization for Syriac and Coptic drops from about five tokens per word to below two after merging target10 pieces. This is the cleanest paper-ready evidence that tokenizer adaptation is doing real work before any downstream translation claim.

## Embedding Initialization

Adding new vocabulary requires initializing embeddings for new subwords. The current ablation compares random initialization against mean initialization over old-subtoken decompositions. The 10k continued-MLM pilot supports a cautious claim: mean initialization is the stronger representation-side choice in this setup. Do not overstate this as a full downstream translation result, because the NMT decoders collapse qualitatively.

## Byte-Level Generation

ByT5 is relevant because it avoids subword vocabulary coverage problems by operating on bytes. That makes it attractive for scripts like Coptic and Syriac. Our results show the trade-off: byte-level coverage is not the same as source-grounded low-resource translation. Small ByT5 pilots can emit valid-script text or copy retrieved hints, but the outputs are repetitive or retrieval-dependent under the current data and training budget.

## Retrieval As Baseline And Diagnostic

Retrieval-augmented generation motivates combining non-parametric evidence with generation, but our retrieval experiments are intentionally more diagnostic than knowledge-intensive RAG. Character n-gram retrieval is a strong non-neural baseline for verse-aligned Coptic data, and top-k oracle results show reranking headroom. The negative controls are important: retrieved-only and wrong-retrieval behavior show that current neural retrieval augmentation mostly copies hints rather than grounding generation in the source.

## Paper-Safe Claims

Safe:

- Target10 tokenizer extension substantially reduces overfragmentation for several unsupported or underrepresented scripts.
- Mean embedding initialization is better than random initialization in the stable 10k MLM pilot.
- Retrieval is a strong baseline for verse-aligned Coptic and should be reported beside neural results.
- Current direct, pivot, and retrieval-augmented neural generation remains diagnostic rather than production-quality translation.

Avoid:

- The project solves Coptic/Syriac MT.
- Back-translation improves Coptic/Syriac translation.
- Retrieval-augmented neural generation is source-grounded in the current experiments.
- chrF++ alone proves translation quality.

## Citation Candidates

Use these as the initial bibliography spine:

- Conneau et al. 2020. "Unsupervised Cross-lingual Representation Learning at Scale" (XLM-R). ACL. https://arxiv.org/abs/1911.02116
- ImaniGooghari et al. 2023. "Glot500: Scaling Multilingual Corpora and Language Models to 500 Languages." ACL. https://arxiv.org/abs/2305.12182
- NLLB Team et al. 2022. "No Language Left Behind: Scaling Human-Centered Machine Translation." https://arxiv.org/abs/2207.04672
- Kudo and Richardson 2018. "SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing." EMNLP demo. https://arxiv.org/abs/1808.06226
- Rust et al. 2021. "How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models." ACL. https://aclanthology.org/2021.acl-long.243/
- Xue et al. 2022. "ByT5: Towards a token-free future with pre-trained byte-to-byte models." TACL. https://arxiv.org/abs/2105.13626
- Lewis et al. 2020. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS. https://arxiv.org/abs/2005.11401

## Remaining Citation Gaps

- Bible-aligned corpus citation and license provenance should be finalized before submission.
- A closer prior on ancient or script-divergent low-resource MT would strengthen the introduction.
- If source-grounding/reranking experiments continue, add a citation for candidate reranking or minimum-risk decoding rather than presenting it as generic RAG.
