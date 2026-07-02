# Step 08 Limitations

## Data Domain

All main evidence uses Bible text. This gives useful multilingual parallel structure, but it is narrow-domain and may overstate performance on verse-like text while understating general-domain behavior.

## Proxy Tasks

The strongest positive downstream evidence is from frozen encoder retrieval/matching proxies. Book/genre classification is saturated and must not be used as primary evidence.

## MLM Adaptation

The selected extended checkpoint improves from its zero-step initialized state, but the original XLM-R baseline still has lower MLM dev loss. A stronger claim would require longer adaptation, broader data, or revised initialization/training settings.

## Method-Matched Translation Failure

The original selected adapted-encoder translation row does not reach the required 80% high-resource reference threshold: ratio `0.510228`. Branch 001 later produced a LaBSE+CSLS sentence-embedding retrieval row with chrF++ `64.434500` and ratio `1.039939`, but that comparison used an XLM-R high-resource reference and a LaBSE target method.

Step 09 reran the check with method-matched high-resource and target scoring. The selected adapted XLM-R method-matched ratio is `0.638034`, and the LaBSE+CSLS upper-bound ratio is `0.567179`. Both are below the `0.800000` threshold.

This means the current evidence does not support a top-tier translation success claim.

## Return Instruction

To make a top-tier translation claim, return to `05_mlm_adaptation`, `06_downstream_tasks`, and `07_translation_benchmark`. Required fixes are longer adaptation with controls, dev-only branch/model selection, and a fresh held-out translation retrieval or generation benchmark.
