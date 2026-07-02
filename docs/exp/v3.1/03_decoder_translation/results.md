# Experiment 3 Results: Simple Decoder Translation

작성일: 2026-06-18

Gate status: `FULL1EP_3SEED_RETRIEVAL_COLLAPSE_DONE_DECODER_WEAK`

## Data

The translation data manifest was generated from the same v3/v1 split lineage:

`docs/exp/v3.1/03_decoder_translation/translation_data_manifest.tsv`

Primary available directions:

| Direction | Train | Dev | Final Test | Status |
| --- | ---: | ---: | ---: | --- |
| `cop -> syr` | `5389` | `678` | `1006` | PASS |
| `syr -> cop` | `5389` | `678` | `1006` | PASS |

Broad fallback directions `eng <-> target10` were also materialized and marked PASS.

## Implemented Runner

Script:

`modeling/train_v31_simple_decoder.py`

Behavior:

- frozen XLM-R-style encoder by default;
- 1-layer Transformer decoder by default;
- teacher-forced cross-entropy training;
- greedy decoding for dev/final evaluation;
- sacreBLEU BLEU and chrF++;
- copy, length, script-validity, and repetition diagnostics.
- frozen encoder stays in eval mode during decoder training;
- generation caches encoder states once per batch instead of rerunning the encoder at every decoded token.

## Full-Data 1-Epoch Runs

These runs use the full train split for one epoch and evaluate the full dev/final splits. They are the first real translation-score measurement for `v3.1`.

| Run | Encoder | Tokenizer | Direction | Train | Dev | Final Test |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `full1ep_xlmr_base_cop_to_syr` | `xlm-roberta-base` | `xlm-roberta-base` | `cop -> syr` | `5389` | `678` | `1006` |
| `full1ep_fvt_seed13_cop_to_syr` | third_try replay-safe seed13 | same checkpoint tokenizer | `cop -> syr` | `5389` | `678` | `1006` |
| `full1ep_xlmr_base_syr_to_cop` | `xlm-roberta-base` | `xlm-roberta-base` | `syr -> cop` | `5389` | `678` | `1006` |
| `full1ep_fvt_seed13_syr_to_cop` | third_try replay-safe seed13 | same checkpoint tokenizer | `syr -> cop` | `5389` | `678` | `1006` |

## Full-Data Metrics

| Direction | Run | Split | Loss | chrF++ | BLEU | Examples |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | `xlm-roberta-base` | dev | `1.9188` | `1.5732` | `0.0` | `678` |
| `cop -> syr` | `xlm-roberta-base` | final_test | `1.9274` | `1.4169` | `0.0` | `1006` |
| `cop -> syr` | `third_try seed13` | dev | `3.6692` | `4.2688` | `0.0227` | `678` |
| `cop -> syr` | `third_try seed13` | final_test | `3.7543` | `3.9155` | `0.0057` | `1006` |
| `syr -> cop` | `xlm-roberta-base` | dev | `0.1294` | `0.0` | `0.0` | `678` |
| `syr -> cop` | `xlm-roberta-base` | final_test | `0.1008` | `0.0` | `0.0` | `1006` |
| `syr -> cop` | `third_try seed13` | dev | `3.5425` | `3.7462` | `0.0205` | `678` |
| `syr -> cop` | `third_try seed13` | final_test | `3.6114` | `3.5645` | `0.0129` | `1006` |

## Multi-Seed Full1ep Aggregate

After the initial seed13 run, the same full-data 1-epoch setup was repeated for replay-safe seed17 and seed23 candidate checkpoints. XLM-R-base has one deterministic baseline run per direction; candidate results are summarized over three checkpoints.

| Direction | Split | Baseline chrF++ | Candidate mean chrF++ | Candidate std | Delta | Candidate seeds |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `cop -> syr` | dev | `1.5732` | `3.9073` | `0.8283` | `+2.3341` | `13,17,23` |
| `cop -> syr` | final_test | `1.4169` | `3.6836` | `0.6999` | `+2.2667` | `13,17,23` |
| `syr -> cop` | dev | `0.0` | `3.6859` | `0.0740` | `+3.6859` | `13,17,23` |
| `syr -> cop` | final_test | `0.0` | `3.4949` | `0.1188` | `+3.4949` | `13,17,23` |

Candidate seed-level final-test chrF++:

| Direction | seed13 | seed17 | seed23 | Baseline |
| --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | `3.9155` | `4.4011` | `2.7343` | `1.4169` |
| `syr -> cop` | `3.5645` | `3.5925` | `3.3277` | `0.0` |

Aggregate artifacts:

| Artifact | Path |
| --- | --- |
| all full1ep rows | `full1ep_all_results.tsv` |
| mean/std summary | `full1ep_metric_summary.tsv` |
| baseline-candidate deltas | `full1ep_delta_summary.tsv` |
| run manifest | `full1ep_run_manifest.tsv` |
| collapse diagnostics | `decoder_collapse_diagnostics.tsv` |
| collapse metric summary | `decoder_collapse_metric_summary.tsv` |
| collapse deltas | `decoder_collapse_delta_summary.tsv` |
| full regenerated predictions | `/home/axt/mnt2/jongha/v3_1/decoder_collapse_diagnostics/*.tsv` |

## Full-Data Diagnostics

| Direction | Run | Split | Length Ratio | Exact Copy | Source Char Overlap | Script Valid | Max Run Ratio |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `xlm-roberta-base` | final_test | `0.7724` | `0.0` | `0.0` | `1.0` | `0.6021` |
| `cop -> syr` | `third_try seed13` | final_test | `1.0902` | `0.0` | `0.0` | `1.0` | `0.6962` |
| `syr -> cop` | `xlm-roberta-base` | final_test | `0.5923` | `0.0` | `0.0` | `0.0` | `0.0` |
| `syr -> cop` | `third_try seed13` | final_test | `0.2967` | `0.0` | `0.0` | `1.0` | `0.4124` |

## Full-Prediction Collapse Diagnostics

The saved `simple_decoder.pt` checkpoints were reloaded and full final-test predictions were regenerated for all full-data 1-epoch runs. This gives token-level EOS, max-length, diversity, and empty-output diagnostics.

Scripts:

```bash
CUDA_VISIBLE_DEVICES=2 python3 modeling/run_v31_decoder_collapse_diagnostics.py \
  --splits final_test \
  --batch-size 8

python3 modeling/aggregate_v31_decoder_collapse.py
```

Final-test summary:

| Direction | Model group | EOS seen | Hit max length | Unique pred rate | Top pred rate | Empty pred rate | Script valid | chrF++ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | XLM-R-base | `0.7525` | `0.2475` | `0.0179` | `0.3688` | `0.0` | `1.0` | `1.4169` |
| `cop -> syr` | third_try mean | `0.5630` | `0.4370` | `0.2220` | `0.1176` | `0.0` | `1.0` | `3.6836` |
| `syr -> cop` | XLM-R-base | `0.0219` | `0.9781` | `0.0040` | `0.9781` | `1.0` | `0.0` | `0.0` |
| `syr -> cop` | third_try mean | `0.9970` | `0.0030` | `0.1206` | `0.1014` | `0.0` | `1.0` | `3.4949` |

Interpretation:

- `syr -> cop` XLM-R-base is a near-complete generation collapse: almost all examples hit max length, the decoded predictions are empty/whitespace, and the top prediction covers `97.8%` of the split.
- `syr -> cop` third_try avoids that collapse: EOS is seen for `99.7%` of examples, empty prediction rate is `0.0`, and Coptic script-valid ratio is `1.0`.
- `cop -> syr` third_try improves diversity over XLM-R-base (`unique_prediction_rate +0.2041`, `top_prediction_rate -0.2512`) but still has a high max-length rate (`0.4370`) and high repetition. This is still a weak decoder, not a translation-quality system.
- These diagnostics support the target-script/collapse-recovery claim more strongly than BLEU alone.

## Full-Data Interpretation

The full-data decoder probe shows a consistent metric gain for third_try replay-safe candidates over XLM-R-base under the same simple decoder setup:

| Direction | Final chrF++ baseline | Final chrF++ candidate mean | Delta |
| --- | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `+3.4949` |

This is a useful positive signal, but it is not yet a strong translation-quality result.

Observed failure modes:

- `xlm-roberta-base` collapses badly for `syr -> cop`: samples are effectively whitespace-only, and Coptic script-valid ratio is `0.0`.
- third_try candidates produce target-script output in both directions, with aggregate script-valid ratio `1.0`.
- full-prediction collapse diagnostics confirm that `syr -> cop` XLM-R-base has empty prediction rate `1.0`, hit-max-length rate `0.9781`, and top-prediction rate `0.9781`; third_try reduces those to `0.0`, `0.0030`, and `0.1014` respectively.
- candidate gains persist across three replay-safe checkpoints, but `cop -> syr` has meaningful seed variance (`std 0.6999` chrF++ on final_test).
- third_try output is still short/repetitive and often generic. For `syr -> cop`, outputs frequently begin with common Coptic fragments such as `ⲞⲨⲞϨ ⲆⲈ`.
- `cop -> syr` third_try still hits max length for `43.7%` of final-test predictions on average, so EOS control remains weak in that direction.
- BLEU remains near zero in both directions.
- sacreBLEU emitted a tokenized-punctuation warning for the `syr -> cop` candidate output, so final reporting needs a detokenization/normalization audit.

Allowed current claim:

> Under a frozen-encoder, one-layer decoder probe trained on the full Coptic-Syriac train split for one epoch, replay-safe third_try encoder/tokenizer checkpoints produce higher held-out chrF++ than XLM-R-base and avoid the target-script collapse observed in the baseline.

Not allowed yet:

> The system produces useful free-form Coptic-Syriac translation.

> The gain is semantic rather than lexical/script coverage.

Next evidence needed:

1. run 2-3 epoch schedules with checkpoint selection;
2. audit detokenization and punctuation normalization before final BLEU reporting;
3. consider retrieval-augmented decoder or contrastive alignment before claiming generation quality.

## Decoder-Alignment Link

Experiment 1 now provides a direct decoder-link table:

`docs/exp/v3.1/01_embedding_alignment/decoder_alignment_delta_summary.tsv`

Final-test summary:

| Direction | Decoder chrF++ Delta | MRR Delta | Recall@1 Delta | Margin Delta |
| --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | `+2.2667` | `+0.0031` | `+0.0017` | `+0.0023` |
| `syr -> cop` | `+3.4949` | `+0.0075` | `+0.0013` | `+0.0009` |

This means the decoder gain is accompanied by a weak positive alignment/retrieval signal. The absolute retrieval scores are still poor, so the result should not be described as robust semantic translation.

## Retrieval-Only Translation Baseline

To avoid test-target leakage, this baseline retrieves only from the train split target-text bank. For each dev/final source sentence, the model embeds the source, retrieves the nearest target-side train verse, and uses that train verse as the prediction.

Artifacts:

| Artifact | Path |
| --- | --- |
| run manifest | `retrieval_baseline_manifest.tsv` |
| raw scores | `retrieval_baseline_results.tsv` |
| diagnostics | `retrieval_baseline_diagnostics.tsv` |
| mean/std summary | `retrieval_baseline_metric_summary.tsv` |
| decoder comparison | `retrieval_vs_decoder_summary.tsv` |
| samples | `retrieval_baseline_samples.md` |
| prediction TSVs | `/home/axt/mnt2/jongha/v3_1/retrieval_translation_baseline/*.tsv` |

Final-test comparison:

| Direction | Model group | Decoder chrF++ | Retrieval chrF++ | Decoder - Retrieval |
| --- | --- | ---: | ---: | ---: |
| `cop -> syr` | XLM-R-base | `1.4169` | `3.7007` | `-2.2838` |
| `cop -> syr` | third_try mean | `3.6836` | `8.3751` | `-4.6915` |
| `syr -> cop` | XLM-R-base | `0.0` | `16.6706` | `-16.6706` |
| `syr -> cop` | third_try mean | `3.4949` | `12.2518` | `-8.7570` |

Important caveats:

- Retrieval-only beats the simple decoder in every direction/model group.
- Retrieval predictions are still not semantically reliable translations.
- `cop -> syr` retrieval has severe collapse: XLM-R retrieves only `2` distinct train verses on final_test, and third_try averages only `4.67`.
- `syr -> cop` retrieval has higher chrF++, but often retrieves generic Coptic train passages; this explains why XLM-R retrieval can score high while XLM-R decoder collapses.
- `same_item_rate` and `same_book_rate` are both `0.0`, as intended by train-bank retrieval over held-out books.

Interpretation:

> The simple decoder probe is useful for detecting target-script/generation collapse, but it is not yet competitive with a retrieval-only train-bank translation proxy.

This changes the decoder result from `PASS_DECODER_TRANSLATION` to a diagnostic state: `DIAGNOSTIC_RETRIEVAL_BETTER`.

## Smoke Runs

These are 2-step sanity checks only. They validate the training/evaluation path and do not support a quality claim.

| Run | Encoder | Tokenizer | Direction | Train rows used | Dev/Test rows used |
| --- | --- | --- | --- | ---: | ---: |
| `smoke_xlmr_base_cop_to_syr` | `xlm-roberta-base` | `xlm-roberta-base` | `cop -> syr` | `16` | `8 / 8` |
| `smoke_fvt_seed13_cop_to_syr` | `third_try` replay-safe seed13 | same checkpoint tokenizer | `cop -> syr` | `16` | `8 / 8` |

## Smoke Metrics

| Run | Split | Loss | chrF++ | BLEU | Metric |
| --- | --- | ---: | ---: | ---: | --- |
| `smoke_xlmr_base_cop_to_syr` | dev | `7.8086` | `5.3667` | `0.0` | sacrebleu |
| `smoke_xlmr_base_cop_to_syr` | final_test | `7.7147` | `4.6262` | `0.0` | sacrebleu |
| `smoke_fvt_seed13_cop_to_syr` | dev | `12.4771` | `5.1654` | `0.0` | sacrebleu |
| `smoke_fvt_seed13_cop_to_syr` | final_test | `10.9259` | `6.2429` | `0.0` | sacrebleu |

## Smoke Diagnostics

| Run | Split | Length Ratio | Exact Copy | Source Char Overlap | Script Valid | Max Run Ratio |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `smoke_xlmr_base_cop_to_syr` | dev | `1.0759` | `0.0` | `0.0` | `1.0` | `0.3000` |
| `smoke_xlmr_base_cop_to_syr` | final_test | `0.6239` | `0.0` | `0.0` | `1.0` | `0.3000` |
| `smoke_fvt_seed13_cop_to_syr` | dev | `1.1063` | `0.0` | `0.0` | `1.0` | `0.1112` |
| `smoke_fvt_seed13_cop_to_syr` | final_test | `0.6440` | `0.0` | `0.0` | `1.0` | `0.1172` |

## Commands

Candidate smoke:

```bash
CUDA_VISIBLE_DEVICES=0 python3 modeling/train_v31_simple_decoder.py \
  --model-name-or-path /home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed13_step1000 \
  --tokenizer-name-or-path /home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed13_step1000 \
  --pair-file /home/axt/mnt2/jongha/v3_1/translation_pairs/cop_to_syr.tsv \
  --output-dir /home/axt/mnt2/jongha/v3_1/decoder_runs/smoke_fvt_seed13_cop_to_syr \
  --src-lang cop --tgt-lang syr \
  --epochs 1 --max-steps 2 \
  --max-train-examples 16 --max-dev-examples 8 --max-test-examples 8 \
  --batch-size 2 --max-source-length 128 --max-target-length 64
```

Baseline smoke:

```bash
CUDA_VISIBLE_DEVICES=0 python3 modeling/train_v31_simple_decoder.py \
  --model-name-or-path xlm-roberta-base \
  --tokenizer-name-or-path xlm-roberta-base \
  --pair-file /home/axt/mnt2/jongha/v3_1/translation_pairs/cop_to_syr.tsv \
  --output-dir /home/axt/mnt2/jongha/v3_1/decoder_runs/smoke_xlmr_base_cop_to_syr \
  --src-lang cop --tgt-lang syr \
  --epochs 1 --max-steps 2 \
  --max-train-examples 16 --max-dev-examples 8 --max-test-examples 8 \
  --batch-size 2 --max-source-length 128 --max-target-length 64
```

## Full Run Template

The next non-smoke repeat should use the same template with either seed17/seed23 or a longer schedule:

```bash
CUDA_VISIBLE_DEVICES=0 python3 modeling/train_v31_simple_decoder.py \
  --model-name-or-path MODEL_OR_CHECKPOINT \
  --tokenizer-name-or-path TOKENIZER_OR_CHECKPOINT \
  --pair-file /home/axt/mnt2/jongha/v3_1/translation_pairs/cop_to_syr.tsv \
  --output-dir /home/axt/mnt2/jongha/v3_1/decoder_runs/RUN_ID \
  --src-lang cop --tgt-lang syr \
  --epochs 3 --batch-size 8 \
  --max-source-length 256 --max-target-length 128
```

Repeat for `syr -> cop`, and keep the XLM-R-base schedule identical.

## Interpretation

The simple decoder path is executable and now has full-data 1-epoch scores for both primary directions. The result is promising as a diagnostic, but the generation samples show low-quality, repetitive outputs. The correct next step is not to claim translation success yet; it is to test whether the chrF++ gain is stable across seeds and explained by better cross-lingual embedding alignment.
