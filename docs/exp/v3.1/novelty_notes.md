# V3.1 Novelty Notes

작성일: 2026-06-18

## Current Evidence

The initialization comparison has now been rerun as an actual masked-prediction training ablation rather than a zero-step check. All five embedding initialization methods were trained for the same 200-step MLM budget on the Stage05 train/dev files:

| Rank | Init | Zero-step dev loss | Final dev loss | Delta vs fvt |
| ---: | --- | ---: | ---: | ---: |
| 1 | `fvt` | `7.925527` | `3.921798` | `0.000000` |
| 2 | `focus` | `16.760191` | `3.931313` | `+0.009515` |
| 3 | `align` | `8.700895` | `4.060271` | `+0.138473` |
| 4 | `random` | `17.998567` | `4.937548` | `+1.015750` |
| 5 | `mean` | `10.910376` | `5.835072` | `+1.913274` |

This changes the safe reading. The earlier zero-step comparison is not evidence by itself. After MLM adaptation, `fvt` remains best in this single-seed 200-step probe, but `focus` nearly catches up. So initialization should be framed as a sensitivity/starting-point ablation unless extended to longer or multi-seed training and connected to downstream alignment/decoder metrics.

The full-data simple-decoder probe now has one XLM-R-base baseline and three replay-safe third_try candidate checkpoints:

| Direction | XLM-R-base final chrF++ | third_try mean final chrF++ | Std | Delta |
| --- | ---: | ---: | ---: | ---: |
| `cop -> syr` | `1.4169` | `3.6836` | `0.6999` | `+2.2667` |
| `syr -> cop` | `0.0` | `3.4949` | `0.1188` | `+3.4949` |

The absolute scores are low and samples are repetitive, so the result should be framed as an encoder/tokenizer diagnostic rather than an NMT success.

The train-bank retrieval-only baseline is stronger than the simple decoder:

| Direction | Model group | Decoder final chrF++ | Retrieval final chrF++ |
| --- | --- | ---: | ---: |
| `cop -> syr` | XLM-R-base | `1.4169` | `3.7007` |
| `cop -> syr` | third_try mean | `3.6836` | `8.3751` |
| `syr -> cop` | XLM-R-base | `0.0` | `16.6706` |
| `syr -> cop` | third_try mean | `3.4949` | `12.2518` |

So the current novelty should not be framed as "generation beats retrieval." The better claim is that a controlled simple decoder exposes target-script/generation collapse, while retrieval exposes a separate hubness/generic-verse baseline.

The frozen pair-classification downstream probe now adds a second representation-level signal. With shifted plus hard negatives, raw cosine remains mixed, but a shallow logistic probe over `abs(e_src - e_tgt)`, `e_src * e_tgt`, and cosine improves on the final split:

| Direction | XLM-R-base final macro F1 | third_try mean final macro F1 | Delta | XLM-R-base AUROC | third_try mean AUROC | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `0.6894` | `0.7247` | `+0.0352` | `0.8026` | `0.8603` | `+0.0577` |
| `syr -> cop` | `0.7198` | `0.7916` | `+0.0718` | `0.7960` | `0.8841` | `+0.0880` |

This is useful because it separates three levels of evidence:

1. raw cosine/retrieval: weak and hubness-sensitive;
2. frozen pairwise classification: positive with a shallow probe;
3. decoder generation: positive over XLM-R-base but still weaker than retrieval-only.

CSLS/centering now adds a hubness-correction check. On final-test exact retrieval, candidate MRR stays above XLM-R-base after CSLS while hubness drops:

| Direction | Score | XLM-R-base MRR | third_try mean MRR | Delta | XLM-R-base hubness@10 max | third_try mean | Delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cop -> syr` | `csls_k10` | `0.0078` | `0.0133` | `+0.0055` | `0.9970` | `0.9032` | `-0.0938` |
| `cop -> syr` | `centered_csls_k10` | `0.0099` | `0.0219` | `+0.0120` | `0.3151` | `0.1057` | `-0.2094` |
| `syr -> cop` | `csls_k10` | `0.0087` | `0.0222` | `+0.0136` | `0.8588` | `0.4278` | `-0.4311` |
| `syr -> cop` | `centered_csls_k10` | `0.0124` | `0.0220` | `+0.0096` | `0.1730` | `0.0418` | `-0.1312` |

This makes the representation claim a little stronger than raw cosine alone, but not strong enough to claim solved semantic retrieval because Recall@1 is still below `1%`.

## Novelty Candidates

### 1. Append-only vocabulary extension as a controlled low-resource intervention

The main methodological novelty is not "train a new tokenizer." It is the stricter constraint:

- keep all original XLM-R token ids unchanged;
- train an auxiliary tokenizer only to discover low-resource/high-resource pieces;
- append only new pieces after the original vocab;
- audit id preservation before any downstream claim.

This makes the experiment cleaner because tokenizer coverage changes are separated from destructive tokenizer replacement.

### 2. Simple decoder as an encoder usability probe

The decoder is intentionally weak: frozen encoder, one small decoder stack, identical training schedule for baseline and candidate. This turns generation into a probe:

> Can the adapted encoder/tokenizer supply enough target-language structure for a small decoder to avoid collapse?

The three-seed result says yes for target-script validity and chrF++ directionally, but not yet for translation quality. Retrieval-only train-bank translation beats the decoder, so the decoder should be reported as a diagnostic probe rather than the strongest task system.

### 3. Script-collapse as a measurable failure mode

The `syr -> cop` baseline produced chrF++ `0.0` and Coptic script-valid ratio `0.0`, with whitespace-like samples. The candidate produced Coptic-script output with script-valid ratio `1.0`, but repetitive generic fragments.

Full-prediction collapse diagnostics make this failure mode explicit:

| Direction | Model group | EOS seen | Hit max length | Empty pred rate | Unique pred rate | Top pred rate | Script valid |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `syr -> cop` | XLM-R-base | `0.0219` | `0.9781` | `1.0` | `0.0040` | `0.9781` | `0.0` |
| `syr -> cop` | third_try mean | `0.9970` | `0.0030` | `0.0` | `0.1206` | `0.1014` | `1.0` |

For `cop -> syr`, third_try also improves diversity over XLM-R-base, but it still hits max length for `43.7%` of final-test predictions on average. So the safe novelty is collapse detection/recovery, not high-quality generation.

This suggests a useful analysis axis:

1. target-script availability;
2. lexical fertility;
3. semantic alignment;
4. generation quality.

The paper can argue that low-resource adaptation should be judged along these separate axes, not only by aggregate BLEU.

### 3b. Retrieval-vs-generation gap

The retrieval-only baseline creates a useful diagnostic gap:

- retrieval can get higher chrF++ while retrieving only a tiny number of generic train verses;
- decoder can recover target script but remains repetitive and weak;
- XLM-R retrieval can score high for `syr -> cop` while XLM-R decoder collapses completely.

This supports a nuanced novelty:

> low-resource adaptation should be evaluated with separate semantic-retrieval, target-script, and generation-collapse diagnostics, because a single translation score can hide very different failure modes.

### 4. Bridge from embedding alignment to generation

Experiment 1 should test whether same-meaning Coptic/Syriac/target10 verses become closer in embedding space. Experiment 3 can then ask whether the same model also improves a constrained generation probe.

Experiment 2 now sits between those two extremes: it asks whether frozen embeddings support a learned same-meaning-pair decision without updating the encoder. The current result improves pairwise linear-probe macro F1/AUROC on final_test, and CSLS/centering confirms that the retrieval gain is not only a raw-cosine artifact. The novelty route should therefore be framed cautiously:

> append-only low-resource adaptation improves a weak cross-lingual semantic attachment signal and simple-decoder translation-probe behavior, while revealing that tokenizer/script recovery and semantic retrieval must be separated.

Current evidence:

| Direction | Decoder chrF++ delta | MRR delta | Recall@1 delta | Alignment reading |
| --- | ---: | ---: | ---: | --- |
| `cop -> syr` | `+2.2667` | `+0.0031` | `+0.0017` | weak positive |
| `syr -> cop` | `+3.4949` | `+0.0075` | `+0.0013` | weak positive |

Because final-test Recall@1 remains below `0.4%`, this is not enough to claim robust semantic retrieval.

## Claim Boundary For Report

Safe current wording:

> A structurally id-preserving, append-only tokenizer extension plus replay-safe MLM adaptation gives a measurable improvement in a frozen-encoder simple-decoder Coptic-Syriac probe, especially by avoiding target-script collapse.

Unsafe current wording:

> The method solves low-resource translation.

> The decoder result alone proves semantic alignment.

> The tokenizer alone caused the improvement.

## Next Evidence To Strengthen Novelty

1. Run Experiment 1 alignment/retrieval and correlate with decoder chrF++.
2. Add tokenizer ablation: XLM-R encoder + append-only tokenizer rows without MLM adaptation if feasible.
3. Add repetition/EOS diagnostics to distinguish target-script recovery from genuine translation.
4. Run a longer 2-3 epoch decoder schedule with dev-based checkpoint selection.
5. Try a retrieval-augmented decoder only after the pure decoder/retrieval gap is clearly documented.
6. Extend pair classification beyond Coptic-Syriac and add a fixed-label topic/classification probe if labels are clean.
