# Step 10 Selection Trace

## Step 07 Original

- Target pair selection loops over target language pairs on John/test and keeps the maximum chrF row.
- Evidence: `/home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/07_translation_benchmark/run_step07.py:270; /home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/07_translation_benchmark/run_step07.py:277; /home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/07_translation_benchmark/run_step07.py:299`
- Decision: exploratory only; not an unbiased held-out target-pair result.

## Branch 001

- Branch score table contains `7` test rows and `6` prior test rows before the final LaBSE row.
- `branch001_procrustes_20260610_231500` / `baseline_no_mapping` / test chrF `32.297328` / ratio `0.521262` / status `MEASURED`
- `branch001_procrustes_20260610_231500` / `procrustes_mapping` / test chrF `24.799654` / ratio `0.400253` / status `MEASURED`
- `branch001_byt5_20260610_231854` / `byt5_small_finetune` / test chrF `0.000000` / ratio `0.000000` / status `MEASURED`
- `branch001_byt5_20260610_232137` / `byt5_small_finetune` / test chrF `14.569178` / ratio `0.235139` / status `MEASURED`
- `branch001_cross_encoder_20260610_232744` / `cross_encoder_reranker` / test chrF `23.094239` / ratio `0.372729` / status `MEASURED`
- `branch001_sentence_embedding_20260610_234556` / `sentence_embedding_sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2_csls` / test chrF `37.518649` / ratio `0.605531` / status `MEASURED`
- `branch001_sentence_embedding_20260610_234706` / `sentence_embedding_sentence-transformers_LaBSE_csls` / test chrF `64.434500` / ratio `1.039939` / status `EXPLORATORY_SUPERSEDED`
- Decision: Branch 001 remains exploratory because final model-family choice followed earlier test feedback and the Step 07 high-resource comparison was mixed-method.

## Step 09

- `original_xlmr_cosine`: high test chrF `61.959906`, target test chrF `28.979374`, ratio `0.467712`, status `FAIL`
- `selected_adapted_xlmr_cosine`: high test chrF `47.785568`, target test chrF `30.488796`, ratio `0.638034`, status `FAIL`
- `labse_csls_upper_bound`: high test chrF `100.000000`, target test chrF `56.717922`, ratio `0.567179`, status `FAIL`
- Decision: translation success claim remains blocked until a fresh held-out method-matched main-model run passes.
