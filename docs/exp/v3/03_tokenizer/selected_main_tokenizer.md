# Selected Main Tokenizer

Status: PROVISIONAL_MAIN_CANDIDATE

Variant: `main_added_48000`

Tokenizer path:

`/home/axt/mnt2/jongha/third_try/tokenizers/stage03_targetheavy_20260613_r3/tokenizers/xlmr_third_try_mixture_added_48000`

Training corpus:

`/home/axt/mnt2/jongha/third_try/text/stage03_targetheavy_20260613_r2/tokenizer_train_balanced.txt`

Notes:

- This candidate preserves all XLM-R existing token ids.
- This candidate includes high-resource replay/control text while using target10-heavy sampling.
- It currently gives the best third_try average target10 tokens/word reduction.
- Fallback ablations are not mixed into the main candidate.
- Final selection remains pending until downstream/model evidence is available.
