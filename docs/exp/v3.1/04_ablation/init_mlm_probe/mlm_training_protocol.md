# MLM Training Protocol

작성일: 2026-06-19

## Short Answer

The run uses the standard HuggingFace/BERT-style masked language modeling collator:

- choose about `15%` of non-special tokens for prediction;
- among selected tokens:
  - `80%` are replaced by the tokenizer mask token;
  - `10%` are replaced by a random token id;
  - `10%` are kept unchanged;
- compute loss only on selected tokens.

It does **not** reproduce full original BERT pretraining. There is no NSP objective, no sentence-pair objective, no whole-word masking, and no contrastive sentence embedding objective.

## Implementation

Runner:

```bash
python3 modeling/run_third_try_stage05.py \
  docs/exp/v3.1/04_ablation/init_mlm_probe/configs/{method}_seed13_step200.json
```

The launcher delegates to `modeling/run.py`, which uses:

```python
DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm_probability=0.15,
)
```

The installed library is:

```text
transformers==4.24.0
```

The collator behavior in this version is:

1. clone input ids into `labels`;
2. create a probability matrix with value `0.15`;
3. set probability to `0.0` for special tokens using `special_tokens_mask`;
4. sample `masked_indices` with Bernoulli `p=0.15`;
5. set `labels[not masked] = -100`, so loss is ignored there;
6. for selected positions:
   - `80%`: replace input id with `tokenizer.mask_token`;
   - `10%`: replace input id with a random token id from the full tokenizer vocabulary;
   - `10%`: keep the original input id unchanged.

For XLM-R, the mask token is `<mask>`.

## What Is Same As BERT

Same:

- token-level MLM objective;
- `15%` selected-token prediction probability;
- `80/10/10` replacement rule;
- cross-entropy loss on selected tokens only;
- special tokens are excluded from being selected as masked positions.

## What Is Different From Full BERT Pretraining

Different:

- no next sentence prediction;
- no sentence order prediction;
- no whole-word masking;
- no contrastive or pairwise semantic alignment loss;
- no fixed masked-dev file;
- tokenizer is XLM-R/SentencePiece-style, with append-only expanded vocabulary;
- model is XLM-R/RoBERTa-style masked LM, not BERT-base with WordPiece and NSP.

## Data Preprocessing

Configuration:

```json
{
  "line_by_line": false,
  "max_seq_length": 512,
  "mlm_probability": 0.15,
  "preprocessing_num_workers": 4
}
```

Because `line_by_line=false`, `modeling/run.py` does the HuggingFace `run_mlm.py` style preprocessing:

1. tokenize every text row;
2. concatenate tokenized rows;
3. split the concatenated stream into chunks of `512`;
4. drop the final short remainder per map batch;
5. dynamically mask tokens inside the data collator at train/eval time.

Train/eval sizes:

| Split | File | Raw lines | HF chunked samples | Role |
| --- | --- | ---: | ---: | --- |
| train | `mlm_train_full_mixture.txt` | 966,152 | 136,039 | full MLM mixture |
| eval | `target10_dev.txt` | 6,521 | 701 | target10 low-resource dev |

Train mixture:

| Component | Lines | Role |
| --- | ---: | --- |
| target10 low-resource train | 52,016 | target adaptation |
| GlotCC eng/deu/jpn/kor replay | 800,000 | high-resource replay/control |
| Bible eng/deu/jpn/kor control | 114,136 | domain-matched replay/control |
| total | 966,152 | full MLM train mixture |

## Training Schedule

The init probe uses the same schedule for all five initialization methods.

| Field | Value |
| --- | --- |
| methods | `random`, `mean`, `fvt`, `align`, `focus` |
| seed | `13` |
| max steps | `200` optimizer steps |
| per-device train batch | `4` chunks |
| gradient accumulation | `8` |
| effective train batch | `32` chunks / optimizer step |
| approximate consumed chunks | `200 * 32 = 6,400` |
| logged epoch | about `0.05` |
| learning rate | `5e-5` |
| warmup | `20` steps |
| LR scheduler | linear |
| optimizer | HuggingFace AdamW |
| Adam betas | `0.9`, `0.999` |
| Adam epsilon | `1e-8` |
| weight decay | `0.0` |
| max grad norm | `1.0` |
| fp16 | `true` |
| eval interval | every `50` steps |
| save interval | every `50` steps |
| final eval | `target10_dev.txt` chunks |

This is a 200-step probe, not a full-epoch training run.

## Evaluation Detail

The validation file is the full target10 dev text, but masking is also dynamic during evaluation because the same `DataCollatorForLanguageModeling` is used.

So `eval_loss` means:

> cross-entropy on dynamically selected masked tokens from the 701 validation chunks.

It does not mean:

> loss over every token in the dev set.

It also does not mean:

> loss over a fixed, pre-materialized mask pattern.

For stricter reproducibility, a future run can precompute fixed masked dev batches or run multiple eval seeds and average them.

## Relation To Encoder Feature Similarity

MLM training optimizes token prediction. It does not directly optimize sentence-level semantic retrieval.

Therefore the follow-up encoder feature-similarity probe is separate:

- MLM loss asks whether the model predicts masked tokens better.
- Same-meaning feature cosine/margin/MRR asks whether whole-sentence encoder vectors align across languages.

Current evidence shows these are not the same signal: `fvt` wins the 200-step MLM loss probe, but it does not win the same-meaning feature retrieval probe.
