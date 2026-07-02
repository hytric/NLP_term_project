# Retrieval-Editing Controls

작성일: 2026-06-04

## Completed Gate

Ran a small `google/byt5-small` retrieval-editing gate with pairwise-selected Coptic hints.

- Input data: `data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8`
- Output dir: `docs/exp/2026-06-04_10_source_grounding_editing/byt5_small_pairwise_selected_edit_gate_train512_step120_fp32_nosave`
- GPU: physical GPU 3 only via `source scripts/gpu3_env.sh`
- Train samples: 512
- Max steps: 120
- Model saving: skipped

Ran a follow-up same-checkpoint control gate with the same training setup and four extra test splits:

- Output dir: `docs/exp/2026-06-04_10_source_grounding_editing/byt5_small_pairwise_selected_same_checkpoint_controls_train512_step120_fp32_nosave`
- Extra splits: source-only, retrieved-only, wrong-shift1, feature-selected top8
- GPU: physical GPU 3 only via `source scripts/gpu3_env.sh`
- Peak CUDA memory: 6779.9 MB

## Metrics

| Condition | Scope | Test chrF++ | Retrieved candidate chrF++ | Pred vs retrieved chrF++ | Exact pred=retrieved | Retrieved contains pred | Repeat ratio >= 0.5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pairwise-selected edit gate | 64-test slice | 18.3574 | 26.6235 | 52.6372 | 0/64 | 17/64 | 4/64 |
| Source-only control | 64-test slice | 0.2729 | 26.6235 | 0.1927 | 0/64 | 0/64 | 59/64 |
| Retrieved-only control | 64-test slice | 18.6220 | 26.6235 | 55.1066 | 4/64 | 24/64 | 3/64 |
| Wrong-shift1 control | 64-test slice | 12.8253 | 17.5606 | 53.2999 | 0/64 | 17/64 | 6/64 |
| Feature-selected top8 control | 64-test slice | 19.1558 | 26.7484 | 56.5260 | 0/64 | 18/64 | 3/64 |

## Reading

The model no longer exactly copies the retrieved Coptic line in this 64-example test slice, but it still stays much closer to the retrieved hint than to the reference. The selected retrieval candidate alone is stronger than the generated output.

This is a negative 10C gate: pairwise retrieval selection helps the input evidence, but the current small ByT5 edit model does not yet learn reliable source-conditioned editing. The retrieved-only control slightly beats the correct source+retrieval condition, while source-only collapses almost completely. Wrong-shift1 hurts, so the model is retrieval-sensitive, but it is not using the English source strongly enough.

## Control Datasets

Control datasets were prepared and the same-checkpoint GPU control gate is complete:

| Control | Data dir | Test retrieved-candidate chrF++ | Status |
| --- | --- | ---: | --- |
| Pairwise source-only | `data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_source_only` | 26.6235 | complete |
| Pairwise retrieved-only | `data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_retrieved_only` | 26.6235 | complete |
| Pairwise wrong-shift1 | `data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_pairwise_selected_top8_control_wrong_shift1` | 17.5606 | complete |
| Feature-selected top8 | `data/processed/nmt_retrieval_augmented/eng_to_cop_char345_pilot1024_64_plus_cop_auto1024_eval_feature_selected_top8` | 26.7484 | complete |

Manifest:

- `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_datasets.tsv`
- `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_results.tsv`

Execution note:

- Use `scripts/train_pretrained_seq2seq_baseline.py --extra_test_file label=path` to train once on the pairwise-selected train split and evaluate all controls with the same checkpoint.
- This avoids comparing controls across separately trained random-seed replicas.

Decision rule: if wrong retrieval is not worse than correct retrieval, the neural model is not source-grounded enough for a positive paper claim.
