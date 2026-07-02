# Step 08 Qualitative Analysis

## Tokenization

The baseline XLM-R tokenizer breaks several target languages into long, character-heavy sequences. The strongest observed case is Syriac, where the baseline reaches `tokens_per_word=4.854` and `single_char_token_pct=74.251`. The selected 32k appended tokenizer reduces both sentence length pressure and single-character fragmentation without changing original XLM-R ids.

## Downstream

The useful downstream signal comes from verse retrieval and parallel verse matching. Book/genre classification is saturated at `1.000000` for both original and adapted models, so it should be treated as a sanity check only. Language identification is also diagnostic only and is not counted toward the main claim.

## Translation

The original selected adapted-encoder retrieval row often retrieves semantically or structurally nearby verses, but it is not close enough to meet the chrF++ threshold. Simple Procrustes mapping, short ByT5 fine-tuning, and cross-encoder reranking also fail.

The strongest exploratory branch uses LaBSE sentence embeddings with CSLS retrieval. It was selected on dev and evaluated once on held-out John test, reaching chrF++ `64.434500` against the original XLM-R high-resource reference. Step 09 later showed that this was not a method-matched top-tier pass: the LaBSE+CSLS upper-bound ratio is `0.567179` when the high-resource reference is evaluated with the same method. Qualitatively, many correct retrievals are exact because the retrieval target is the aligned verse text; remaining misses still show that this is a retrieval proxy rather than free-form generation.
