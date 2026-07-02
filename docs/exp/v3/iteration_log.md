# Third Try Iteration Log

작성일: 2026-06-12

이 파일은 반복 실행과 의사결정의 누적 기록이다. 같은 stage를 다시 실행할 때 기존 결과를 덮어쓰지 않고 새 run id를 추가한다.

## Current State

| Field | Value |
| --- | --- |
| Current phase | pre-execution planning |
| Main protocol | target10 performance model with high-resource replay |
| Active next stage | `00_scope` |
| Current gate | user scope answers locked; no experiment run yet |
| Main risk | target10 downstream과 high-resource replay mixture가 확정되지 않으면 novelty와 성능 개선 claim이 흐려짐 |

## Iteration Summary Template

```markdown
## {run_id}

Date: YYYY-MM-DD

Stage: `NN_stage_name`

Status: PASS | FAIL | PASS_NEGATIVE_RESULT | BLOCKED

Changed variables:

- ...

Artifacts:

- docs:
- large artifacts:

Gate evidence:

- ...

Failure return:

- failed gate:
- observed evidence:
- return-to stage:
- required fix:

Next action:

- ...
```

## Log

## planning_20260612_r1

Date: 2026-06-12

Stage: planning

Status: PASS

Changed variables:

- Added locked stage folders `00_scope` through `09_extension_case`.
- Added execution and iteration rules before running experiments.
- Added per-stage exit criteria templates.

Artifacts:

- docs: `step_index.md`, `execution_rules.md`, `iteration_log.md`, stage `plan.md` files
- large artifacts: none

Gate evidence:

- Existing `idea.md`, `plan.md`, and `ablation_study.md` define the scientific direction.
- New planning files define execution order, exit gates, and repeat logging.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Start `00_scope` and fill `language_inventory.tsv`, `head_tail_definition.tsv`, `results.md`, `score_table.tsv`, `file_results.tsv`.

## planning_20260612_r2

Date: 2026-06-12

Stage: planning

Status: PASS

Changed variables:

- Locked final objective as an actual target10 performance-improvement model, not only a reproduction package.
- Locked target10 as the main low-resource set and moved Coptic/Syriac into main evidence.
- Locked high-resource replay/control data as mandatory in the training mixture.
- Removed `xlm-roberta-large` from required baselines.
- Promoted multiple embedding initialization methods and 3+ seeds into the main model-dependent matrix.
- Locked downstream improvement as the success criterion.

Artifacts:

- docs: `scope_lock_20260612.md`, updated `README.md`, `idea.md`, `plan.md`, `decision_log.md`, `step_index.md`, `execution_rules.md`, stage `plan.md` files
- large artifacts: none

Gate evidence:

- User confirmed target10 retention, Coptic/Syriac as main, high-resource + low-resource simultaneous data, XLM-R-base only, 1 GPU for several days, downstream improvement, Korean docs, multiple embedding methods, and at least 3 seeds.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Start `00_scope` with target10 inventory, high-resource replay inventory, task availability, and mixture contract.

## planning_20260612_r3

Date: 2026-06-12

Stage: planning / dataset precheck

Status: PASS

Changed variables:

- Confirmed large dataset root under `/home/axt/mnt2/jongha`.
- Recorded current target10, v1/v2 split, high-resource Bible, UD Coptic, Taxi1500, and second_try artifact locations.
- Identified the missing main artifact: a third_try-specific high-resource + target10 MLM mixture manifest.

Artifacts:

- docs: `00_scope/current_dataset_inventory.md`
- large artifacts: existing datasets only; no new large artifacts

Gate evidence:

- Target10 raw XML, processed manifests, V2 clean split, and high-resource Bible XML files are present.
- Existing high-resource candidates include English, German, Japanese, and Korean Bible XML.
- Local Taxi1500 appears English-only.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Build `00_scope/high_resource_inventory.tsv` and `01_data/mlm_mixture_manifest.tsv` from confirmed paths.

## planning_20260613_r1

Date: 2026-06-13

Stage: `00_scope`

Status: PASS

Changed variables:

- Checked usable high-resource Bible datasets.
- Created core and optional high-resource inventory.
- Recommended English/German/Japanese/Korean as core replay/control set.

Artifacts:

- docs: `00_scope/high_resource_inventory.tsv`, `00_scope/high_resource_dataset_check.md`, updated `00_scope/current_dataset_inventory.md`
- large artifacts: existing raw Bible XML only

Gate evidence:

- Bible metadata has 60 full Bible entries.
- 54 full Bible entries have speaker count >= 1M.
- English, German, Japanese, and Korean all have full Bible XML with about 31k verse rows.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Build Stage 01 high-resource + target10 mixture manifest using core replay/control languages first.

## planning_20260613_r2

Date: 2026-06-13

Stage: `01_data`

Status: PASS

Changed variables:

- Reclassified Bible high-resource as domain-matched replay/control, not true high-resource pretraining data.
- Added GlotCC-V1 as true high-resource web corpus source.
- Added deterministic shard-sampling script for English/German/Japanese/Korean.

Artifacts:

- code: `preprocessing/prepare_third_try_high_resource_glotcc.py`
- docs: `01_data/high_resource_web_corpus_plan.md`, updated `00_scope/high_resource_dataset_check.md`
- large artifacts: none yet; materialization command documented

Gate evidence:

- `cis-lmu/GlotCC-V1` has `eng-Latn`, `deu-Latn`, `jpn-Jpan`, and `kor-Hang`.
- Available sizes are large enough to be true high-resource web replay: English 691GB, German 135GB, Japanese 2.45GB, Korean 13.9GB.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Run the script first with `--dry-run`, then materialize a bounded sample under `/home/axt/mnt2/jongha/third_try/high_resource/glotcc`.

## planning_20260613_r3

Date: 2026-06-13

Stage: `01_data`

Status: PASS

Changed variables:

- Materialized bounded GlotCC-V1 high-resource web replay samples for English, German, Japanese, and Korean.
- Kept the sample compute-bounded: 2 shards per config, 200000 output lines per config.

Artifacts:

- data: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_eng-Latn.jsonl`
- data: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_deu-Latn.jsonl`
- data: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_jpn-Jpan.jsonl`
- data: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_kor-Hang.jsonl`
- manifest: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`
- log: `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/logs/download_20260613.log`

Gate evidence:

- `eng-Latn`: PASS, 11274 docs, 200000 lines, 69 MB JSONL.
- `deu-Latn`: PASS, 9573 docs, 200000 lines, 72 MB JSONL.
- `jpn-Jpan`: PASS, 20555 docs, 200000 lines, 111 MB JSONL.
- `kor-Hang`: PASS, 14732 docs, 200000 lines, 109 MB JSONL.
- Total materialized lines: 800000.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Build `01_data/mlm_mixture_manifest.tsv` by combining target10 V2 train/dev with GlotCC web replay and Bible-domain high-resource control.

## planning_20260613_r4

Date: 2026-06-13

Stage: `00_scope` / `01_data`

Status: PASS

Changed variables:

- Updated the main project plan after high-resource materialization.
- Marked Stage 00 scope as closed with formal gate files.
- Kept Stage 01 as the active stage, blocked only on mixture manifest construction.
- Added a status report for the user-facing project state.

Artifacts:

- docs: `status_report_20260613.md`
- docs: `00_scope/results.md`
- docs: `00_scope/score_table.tsv`
- docs: `00_scope/file_results.tsv`
- docs: `00_scope/language_inventory.tsv`
- docs: `00_scope/head_tail_definition.tsv`
- docs: `00_scope/mixture_contract.tsv`
- docs: `00_scope/task_availability.tsv`
- docs: `00_scope/scope_decisions.tsv`
- docs: updated `README.md`, `plan.md`, `step_index.md`, `01_data/plan.md`, `decision_log.md`

Gate evidence:

- Stage 00 `results.md` records `Gate status: PASS`.
- Stage 00 `score_table.tsv` has all required checks marked `PASS`.
- Status report records GlotCC-V1 high-resource web replay as materialized and Stage 01 as the current active step.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Generate Stage 01 `corpus_manifest.tsv`, `high_resource_manifest.tsv`, `mlm_mixture_manifest.tsv`, and `leakage_audit.tsv`.

## stage01_data_20260613_r1

Date: 2026-06-13

Stage: `01_data`

Status: PASS

Changed variables:

- Built Stage 01 source-level and row-level manifests.
- Excluded target10 train rows whose exact text overlaps dev/final rows.
- Excluded target10 held-out books `ACT`, `MAR`, and `JOH` from Bible-domain control train rows.
- Recorded user constraint that all GPU work must use GPU 3 only.

Artifacts:

- docs: `01_data/corpus_manifest.tsv`
- docs: `01_data/split_manifest.tsv`
- docs: `01_data/high_resource_manifest.tsv`
- docs: `01_data/mlm_mixture_manifest.tsv`
- docs: `01_data/leakage_audit.tsv`
- docs: `01_data/source_license_manifest.tsv`
- docs: `01_data/results.md`
- large: `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_train_rows.tsv`
- large: `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_dev_rows.tsv`
- large: `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/final_eval_rows.tsv`
- large: `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/target10_train_exact_duplicate_exclusions.tsv`

Gate evidence:

- Stage 01 `score_table.tsv`: all checked metrics PASS.
- Target10 original train rows: 52124.
- Target10 effective train rows after exact eval duplicate exclusion: 52016.
- Excluded exact duplicate train rows: 108.
- GlotCC web replay rows: 800000.
- Bible domain-control train rows after held-out book exclusion: 114136.
- Total MLM train row index: 966152.
- Leakage audit: target10 train/dev/final overlap is 0 by iso+verse and exact text.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Start Stage 02 XLM-R-base baseline audit.

## stage02_baseline_20260613_r1

Date: 2026-06-13

Stage: `02_baseline`

Status: IN_PROGRESS

Changed variables:

- Computed XLM-R-base target10 final-test tokenization metrics.
- Computed high-resource control tokenization sample metrics.
- Verified GPU execution visibility with `CUDA_VISIBLE_DEVICES=3`.
- Ran deterministic 15% masked-LM eval baseline on GPU 3.
- Added a local compatibility shim for the installed `accelerate` / `huggingface_hub` version mismatch.

Artifacts:

- code: `preprocessing/run_third_try_stage02_tokenization_baseline.py`
- code: `preprocessing/run_third_try_stage02_mlm_eval_baseline.py`
- docs: `02_baseline/tokenization_metrics.tsv`
- docs: `02_baseline/high_resource_control_baseline.tsv`
- docs: `02_baseline/mlm_eval_baseline.tsv`
- docs: `02_baseline/mlm_eval_summary.tsv`
- docs: `02_baseline/baseline_eval.tsv`
- docs: `02_baseline/target10_baseline_summary.tsv`
- docs: `02_baseline/tokenization_samples.md`
- docs: `02_baseline/results.md`
- log: `/home/axt/mnt2/jongha/third_try/manifests/stage02_mlm_eval_20260613.log`

Gate evidence:

- Target10 average tokens/word: 3.011828.
- Target10 average single-character token ratio: 0.305295.
- Target10 deterministic MLM eval average loss: 3.472799.
- Target10 deterministic MLM eval average perplexity: 155.299643.
- GPU constraint honored: CUDA saw one visible device under `CUDA_VISIBLE_DEVICES=3`.
- Exact PPPL and downstream baselines remain pending.

Failure return:

- failed gate: NOT_APPLICABLE_YET
- observed evidence: tokenization and deterministic MLM baselines complete; exact PPPL/downstream pending
- return-to stage: NOT_APPLICABLE_YET
- required fix: run exact PPPL if needed and downstream baseline on GPU 3

Next action:

- Decide Stage 02 downstream baseline subset, then move to Stage 03 tokenizer extension candidates once the baseline gate decision is accepted.

## stage03_tokenizer_20260613_r1

Date: 2026-06-13

Stage: `03_tokenizer`

Status: IN_PROGRESS

Changed variables:

- Materialized text files for full MLM training and balanced tokenizer training.
- Trained a balanced high-resource + target10 16k auxiliary tokenizer candidate.
- Trained target-heavy high-resource 32k and 48k auxiliary tokenizer candidates.
- Selected target-heavy high-resource 48k as the provisional main tokenizer candidate.

Artifacts:

- code: `preprocessing/materialize_third_try_training_texts.py`
- code: `preprocessing/run_third_try_stage03_tokenizer.py`
- text: `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/mlm_train_full_mixture.txt`
- text: `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/tokenizer_train_balanced.txt`
- text: `/home/axt/mnt2/jongha/third_try/text/stage03_targetheavy_20260613_r2/tokenizer_train_balanced.txt`
- tokenizer: `/home/axt/mnt2/jongha/third_try/tokenizers/stage03_targetheavy_20260613_r3/tokenizers/xlmr_third_try_mixture_added_48000`
- docs: `03_tokenizer/candidate_comparison.tsv`
- docs: `03_tokenizer/merge_report.json`
- docs: `03_tokenizer/id_preservation_audit.tsv`
- docs: `03_tokenizer/tokenization_before_after.tsv`
- docs: `03_tokenizer/selected_main_tokenizer.md`

Gate evidence:

- Selected tokenizer preserves all existing XLM-R ids: changed existing ids = 0.
- Special token ids changed = 0.
- Appended token id violations = 0.
- Actual added tokens = 30849.
- Extended vocab size = 280851.
- Average target10 dev tokens/word delta = -29.812358%.
- Worst language tokens/word delta = +1.504758% for Cherokee.
- The selected tokenizer includes high-resource replay/control text in the tokenizer training corpus.

Failure return:

- failed gate: NOT_APPLICABLE_YET
- observed evidence: tokenizer candidate structurally valid and provisionally selected
- return-to stage: NOT_APPLICABLE_YET
- required fix: complete Stage 04 initialization audit and downstream/model validation

Next action:

- Prepare Stage 04 resized XLM-R-base model variants for the selected tokenizer: random, mean, source-tokenizer mean/fvt, align/focus if feasible.

## final_pre_start_review_20260613_r1

Date: 2026-06-13

Stage: pre-Stage05 final review

Status: CONDITIONAL_GO_TO_STAGE05_PILOT

Changed variables:

- Added a final pre-start go/no-go report before launching continued MLM.
- Updated `README.md` current status to reflect Stage 00/01/03/04 completion and Stage 05 pilot readiness.
- Marked `status_report_20260613.md` as an intermediate report superseded for go/no-go by the final pre-start report.

Artifacts:

- docs: `final_pre_start_report_20260613.md`
- docs: updated `README.md`
- docs: updated `status_report_20260613.md`

Gate evidence:

- Stage 00 and Stage 01 are PASS.
- Stage 03 is `PASS_DEVIATION_DOCUMENTED`; selected tokenizer preserves all XLM-R ids and appends 30849 tokens.
- Stage 04 is PASS; fvt is selected only as first Stage 05 pilot checkpoint.
- Stage 02 remains IN_PROGRESS with exact PPPL/downstream pending, so final claim remains blocked.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Write `05_mlm/training_config.json`, `05_mlm/training_command.md`, and `05_mlm/deviation_from_protocol.tsv`, then launch the fvt Stage 05 pilot on GPU 3 only.

## stage05_smoke_fvt_seed13_20260613

Date: 2026-06-13

Stage: `05_mlm`

Status: PASS

Changed variables:

- Added Stage 05 wrapper launcher with local `huggingface_hub` compatibility shim.
- Added smoke and pilot JSON configs.
- Ran one-step smoke test from the Stage 04 `fvt` checkpoint on GPU 3.
- Added `log_level=warning` and `disable_tqdm=true` to reduce pilot log volume.

Artifacts:

- code: `modeling/run_third_try_stage05.py`
- docs: `05_mlm/training_config.json`
- docs: `05_mlm/training_config_smoke.json`
- docs: `05_mlm/training_command.md`
- docs: `05_mlm/deviation_from_protocol.tsv`
- docs: `05_mlm/smoke_test_result.tsv`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/smoke_fvt_seed13`

Gate evidence:

- Smoke test ran with `CUDA_VISIBLE_DEVICES=3`.
- Trainer loaded checkpoint/tokenizer, ran fp16 train/eval, and saved checkpoint.
- Smoke train loss: `7.336768`.
- Smoke eval loss: `8.1263`.
- Smoke perplexity: `3382.426`.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Launch the 200-step fvt Stage 05 pilot using `docs/exp/third_try/05_mlm/training_config.json`.

## stage05_fvt_3seed_pilot_20260613

Date: 2026-06-13

Stage: `05_mlm`

Status: PASS_FOR_PILOT

Changed variables:

- Ran 200-step full-model MLM continued pretraining from the Stage 04 `fvt` checkpoint on GPU 3.
- Used high-resource replay + target10 mixture text with sequence length 512 and effective pilot batch 32.
- Completed pilot seeds 13, 17, and 23.
- Saved checkpoint artifacts at steps 150 and 200 for each seed because `save_total_limit=2`.

Artifacts:

- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed13_pilot`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed17_pilot`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_seed23_pilot`
- docs: `05_mlm/checkpoint_metrics.tsv`
- docs: `05_mlm/init_method_mlm_summary.tsv`
- docs: `05_mlm/seed_summary.tsv`
- docs: updated `05_mlm/results.md`
- docs: updated `05_mlm/score_table.tsv`
- docs: updated `05_mlm/file_results.tsv`

Gate evidence:

- Seed13 final eval loss/perplexity: `3.921798` / `50.491170`.
- Seed17 final eval loss/perplexity: `4.010451` / `55.171739`.
- Seed23 final eval loss/perplexity: `4.011500` / `55.229646`.
- Mean final eval loss/perplexity: `3.981250` / `53.630852`.
- Scheduled eval losses decreased at steps 50, 100, 150, and 200 for all seeds.
- Training used `CUDA_VISIBLE_DEVICES=3`.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: NOT_APPLICABLE
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Decide whether the 200-step pilot checkpoints are sufficient for Stage 06 pilot evaluation, or run a longer final-budget 3-seed grid first.
- Keep Stage 06 and Stage 07 blocked until final candidate checkpoints and target10 downstream evidence exist.

## stage06_proxy_eval_20260613

Date: 2026-06-13

Stage: `06_eval`

Status: IN_PROGRESS

Changed variables:

- Added deterministic masked-LM proxy eval script for locked target10 final-test rows.
- Evaluated XLM-R-base plus fvt checkpoint seeds 13, 17, and 23.
- Reused the existing `second_try` frozen-encoder proxy runner for target10 Bible retrieval/parallel matching on each fvt checkpoint seed.
- Located local Coptic UD train/dev/test files for the next official/local downstream run.

Artifacts:

- code: `preprocessing/run_third_try_stage06_mlm_proxy_eval.py`
- docs: `06_eval/mlm_proxy_eval.tsv`
- docs: `06_eval/mlm_proxy_summary.tsv`
- docs: `06_eval/mlm_proxy_language_comparison.tsv`
- docs: `06_eval/target10_seed_summary.tsv`
- docs: `06_eval/frozen_proxy_seed13/downstream_results.tsv`
- docs: `06_eval/frozen_proxy_seed17/downstream_results.tsv`
- docs: `06_eval/frozen_proxy_seed23/downstream_results.tsv`
- docs: `06_eval/frozen_proxy_seed_summary.tsv`
- docs: `06_eval/coptic_ud_inventory.tsv`
- docs: updated `06_eval/results.md`

Gate evidence:

- MLM proxy mean loss: XLM-R `3.472837`, fvt 3-seed mean `5.298593`.
- MLM proxy improves in 4/10 languages, with Coptic/Syriac worse under the XLM-R `<unk>` shortcut caveat.
- Frozen proxy retrieval recall@1 improves in 2/3 checkpoint seeds.
- Frozen proxy parallel matching AUC improves in 1/3 checkpoint seeds.
- Coptic UD exists locally: train 1467 sentences, dev 380, test 405.

Failure return:

- failed gate: NOT_APPLICABLE_YET
- observed evidence: proxy evidence is mixed; Coptic tagging/high-resource control not yet run
- return-to stage: NOT_APPLICABLE_YET
- required fix: run Coptic UD tagging and high-resource control before final claim

Next action:

- Convert Coptic UD to the `evaluation/tagging` token-classification format, then run Coptic POS tagging for XLM-R-base and fvt checkpoints.

## stage06_coptic_pos_pilot_20260613

Date: 2026-06-13

Stage: `06_eval`

Status: PASS_FOR_COPTIC_PILOT

Changed variables:

- Converted local UD Coptic-Scriptorium train/dev/test data into the local Glot500 tagging format.
- Added a Coptic POS runner around `evaluation/tagging/run_tag.py`.
- Ran XLM-R-base and fvt checkpoint seeds 13, 17, and 23 with identical 200-step POS fine-tuning settings on GPU 3.
- Added a POS-specific metric script because the built-in `seqeval` F1 is not appropriate for plain UPOS tags.

Artifacts:

- code: `preprocessing/prepare_third_try_coptic_ud_pos.py`
- code: `preprocessing/run_third_try_coptic_pos.py`
- code: `preprocessing/evaluate_third_try_coptic_pos_metrics.py`
- docs: `06_eval/coptic_pos_dataset.tsv`
- docs: `06_eval/coptic_pos_results.tsv`
- docs: `06_eval/coptic_pos_summary.tsv`
- docs: `06_eval/coptic_pos_label_metrics.tsv`
- docs: updated `06_eval/results.md`
- large: `/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos`
- large: `/home/axt/mnt2/jongha/third_try/downstream/coptic_ud_pos_runs_step200`

Gate evidence:

- Coptic POS test set has 405 sentences and 10372 tokens.
- XLM-R-base test token accuracy: `0.253182`.
- fvt seed13/17/23 test token accuracy: `0.260991`, `0.257809`, `0.257424`.
- fvt mean test token accuracy: `0.258741`, mean delta vs XLM-R: `+0.005559`.
- Coptic POS token accuracy improves in 3/3 fvt checkpoint seeds.
- Macro F1 is essentially tied: fvt mean `0.163313` vs XLM-R `0.163298`.

Failure return:

- failed gate: NOT_APPLICABLE_YET
- observed evidence: Coptic-only downstream pilot is weak positive; target10-wide downstream and high-resource control are still missing
- return-to stage: NOT_APPLICABLE_YET
- required fix: run high-resource control and target10-wide downstream/proxy downstream coverage before final claim

Next action:

- Run high-resource control sanity check for English/German/Japanese/Korean.
- Audit remaining target10 downstream availability, especially Syriac, and document unavailable task reasons.

## stage06_high_resource_control_proxy_20260613

Date: 2026-06-13

Stage: `06_eval`

Status: FAIL_POTENTIAL_COLLAPSE_PROXY

Changed variables:

- Added held-out Bible-control MLM proxy evaluation for English, German, Japanese, and Korean.
- Used only Stage 01 control-held-out books: `ACT`, `JOH`, and `MAR`.
- Compared XLM-R-base against fvt pilot checkpoint seeds 13, 17, and 23.
- Added a provisional large-collapse diagnostic threshold: fvt mean MLM loss delta vs XLM-R greater than `+0.500000`.

Artifacts:

- code: `preprocessing/run_third_try_stage06_high_resource_control_eval.py`
- docs: `06_eval/high_resource_control_command.md`
- docs: `06_eval/high_resource_control_mlm_eval.tsv`
- docs: `06_eval/high_resource_control_language_comparison.tsv`
- docs: `06_eval/high_resource_control_summary.tsv`
- docs: updated `06_eval/results.md`
- docs: updated `06_eval/score_table.tsv`
- docs: updated `06_eval/task_coverage.tsv`

Gate evidence:

- XLM-R mean control MLM loss: `2.514329`.
- fvt mean control MLM loss: `3.217443`.
- fvt mean delta vs XLM-R: `+0.703114`.
- Language deltas: English `+0.625277`, German `+0.629138`, Japanese `+0.787343`, Korean `+0.770699`.
- `0/4` high-resource control languages pass the no-large-collapse proxy threshold.

Failure return:

- failed gate: high-resource no-large-collapse proxy
- observed evidence: all held-out high-resource Bible-control languages show fvt mean MLM loss increases above the diagnostic threshold
- return-to stage: `05_mlm` if pursuing a positive claim with safer replay/checkpointing; otherwise `07_main_claim` for diagnostic negative synthesis after target10 downstream coverage audit
- required fix: increase/rebalance high-resource replay, select a safer checkpoint, or accept diagnostic negative claim

Next action:

- Audit remaining target10 downstream availability, especially Syriac.
- Decide whether current evidence is enough for a diagnostic negative claim after documenting target10-wide downstream gaps, or whether to rerun Stage 05 with safer replay.

## stage06_target10_availability_audit_20260613

Date: 2026-06-13

Stage: `06_eval`

Status: PASS_AVAILABILITY_AUDIT

Changed variables:

- Audited local target10 downstream availability under the current data roots and second_try task manifests.
- Separated Coptic's available UD POS task from target10-wide Bible-domain proxy coverage.
- Recorded that Syriac has Bible proxy coverage and legacy Coptic-Syriac parallel data, but no fresh official/local supervised task in the current encoder-only protocol.

Artifacts:

- docs: `06_eval/target10_downstream_availability.tsv`
- docs: updated `06_eval/results.md`
- docs: updated `06_eval/score_table.tsv`
- docs: updated `06_eval/task_coverage.tsv`

Gate evidence:

- Coptic: UD Coptic-Scriptorium POS exists and was run.
- Remaining target10 languages: no separate local supervised task found under current data roots.
- All target10 languages: Bible-domain frozen proxy coverage exists and was run.
- Syriac: legacy Coptic-Syriac parallel data exists, but translation/NMT is outside the current encoder-only final claim without a fresh protocol.

Failure return:

- failed gate: NOT_APPLICABLE
- observed evidence: local official downstream coverage is sparse but documented
- return-to stage: NOT_APPLICABLE
- required fix: NOT_APPLICABLE

Next action:

- Move to Stage 07 synthesis only if accepting diagnostic negative framing, or return to Stage 05 for a safer replay schedule if trying to recover a positive claim.

## stage03_fallback_stage07_stage08_synthesis_20260613

Date: 2026-06-13

Stage: `03_tokenizer`, `07_main_claim`, `08_ablation`

Status: PASS_NEGATIVE_MAIN_READY_AND_ABLATION_PACKAGE_READY

Changed variables:

- Added explicit byte fallback vs character coverage tokenizer ablation at vocab size 48000.
- Kept the selected main tokenizer as the existing character-coverage target-heavy 48k append tokenizer.
- Separated auxiliary SentencePiece byte-fallback behavior from append-only XLM-R `add_tokens` behavior.
- Promoted Stage 07 claim synthesis from pending to diagnostic negative for the current compute-bounded candidate.
- Promoted Stage 08 ablation packaging from TODO to complete mapping of first_try/second_try.

Artifacts:

- code: `preprocessing/run_third_try_stage03_fallback_ablation.py`
- docs: `03_tokenizer/fallback_ablation.tsv`
- docs: `03_tokenizer/fallback_ablation_summary.tsv`
- docs: `03_tokenizer/fallback_ablation_comparison.tsv`
- docs: `03_tokenizer/fallback_ablation_aux_metrics.tsv`
- docs: `03_tokenizer/fallback_ablation_append_metrics.tsv`
- docs: `07_main_claim/evidence_table.tsv`
- docs: `07_main_claim/results.md`
- docs: `07_main_claim/allowed_claims.md`
- docs: `07_main_claim/blocked_claims.md`
- docs: `08_ablation/ablation_matrix.tsv`
- docs: `08_ablation/second_try_mapping.tsv`
- docs: `08_ablation/first_try_mapping.tsv`
- docs: `08_ablation/results.md`

Gate evidence:

- Character coverage main-compatible tokenizer: avg append tokens/word delta vs XLM-R `-29.812358%`.
- Byte fallback ablation tokenizer: avg append tokens/word delta vs XLM-R `-30.215948%`.
- Byte-minus-char mean append delta: `-0.599816%`.
- Byte fallback is slightly better in tokenizer metrics, but remains ablation-only because SentencePiece BYTE pieces are not faithfully activated by literal added-token matching.
- Stage 07 positive route remains blocked by target10 MLM proxy degradation, mixed proxy downstream evidence, sparse official target10 downstream coverage, and high-resource control proxy failure.
- Stage 08 maps prior experiments as ablation/failure analysis with `prior experiments labeled main = 0`.

Failure return:

- failed gate: POSITIVE_MAIN_CLAIM
- observed evidence: high-resource control proxy delta `+0.703114`; target10 MLM proxy fvt mean loss `5.298593` vs XLM-R `3.472837`; target10 downstream seed stability `NOT_RUN`
- return-to stage: `05_mlm` for safer/full-budget replay if pursuing a positive claim
- required fix: full-budget seed grid, stronger replay/no-collapse evidence, and broader target10 downstream coverage

Next action:

- If pursuing positive claim, return to Stage 05 and redesign replay/training budget.
- If writing the current report, use Stage 07 diagnostic negative wording and Stage 08 ablation placement.

## stage06_coptic_syriac_language_evidence_20260613

Date: 2026-06-13

Stage: `06_eval`, `07_main_claim`

Status: PASS_DIAGNOSTIC_LANGUAGE_EVIDENCE

Changed variables:

- Added a target10 language-level evidence table so Coptic/Syriac are not hidden behind aggregate proxy metrics.
- Added a Coptic/Syriac-specific evidence note for report wording.
- Updated Stage 06 and Stage 07 claim synthesis to reference the explicit language evidence.

Artifacts:

- docs: `06_eval/target10_language_evidence.tsv`
- docs: `06_eval/coptic_syriac_evidence.md`
- docs: `06_eval/syriac_downstream_search.tsv`
- docs: updated `06_eval/results.md`
- docs: updated `06_eval/score_table.tsv`
- docs: updated `07_main_claim/evidence_table.tsv`
- docs: updated `final_diagnostic_report_20260613.md`

Gate evidence:

- Coptic tokenizer tokens/word delta: `-12.539893%`.
- Coptic MLM proxy delta loss: `+5.541550`.
- Coptic POS token accuracy delta: `+0.005559`, 3/3 checkpoint seeds positive.
- Syriac tokenizer tokens/word delta: `-66.873096%`.
- Syriac MLM proxy delta loss: `+3.060033`.
- Syriac local supervised encoder-only downstream task: not found under current protocol.

Failure return:

- failed gate: COPTIC_SYRIAC_PAIR_POSITIVE_DOWNSTREAM
- observed evidence: Coptic is weakly positive only on POS token accuracy; Syriac remains proxy-only and model-proxy negative
- return-to stage: Stage 06 for a fresh Syriac-safe downstream/proxy task, or Stage 05 for a new model candidate
- required fix: add leakage-safe Syriac downstream evidence and fix high-resource control collapse before positive wording

Next action:

- Keep diagnostic negative claim; do not say Coptic and Syriac both improved downstream.

## stage06_retained_checkpoint_selection_proxy_20260613

Date: 2026-06-13

Stage: `06_eval`, `07_main_claim`, `08_ablation`

Status: FAIL_POTENTIAL_COLLAPSE_PROXY_RETAINED_CHECKPOINT_ABLATION

Changed variables:

- Evaluated the retained earlier `checkpoint-150` for all three fvt pilot seeds.
- Compared checkpoint-150 against checkpoint-200 on target10 MLM proxy and high-resource control proxy.
- Added retained checkpoint selection as an ablation/failure-analysis axis.

Artifacts:

- docs: `06_eval/mlm_proxy_eval_ckpt150.tsv`
- docs: `06_eval/mlm_proxy_summary_ckpt150.tsv`
- docs: `06_eval/high_resource_control_mlm_eval_ckpt150.tsv`
- docs: `06_eval/high_resource_control_language_comparison_ckpt150.tsv`
- docs: `06_eval/high_resource_control_summary_ckpt150.tsv`
- docs: `06_eval/checkpoint_selection_proxy_summary.tsv`
- docs: `06_eval/checkpoint_selection_proxy.md`
- docs: `06_eval/checkpoint_selection_proxy_command.md`

Gate evidence:

- checkpoint-150 target10 fvt mean loss: `5.348870`.
- checkpoint-200 target10 fvt mean loss: `5.298593`.
- checkpoint-150 high-resource control delta vs XLM-R: `+0.757355`.
- checkpoint-200 high-resource control delta vs XLM-R: `+0.703114`.
- checkpoint-150 no-large-collapse languages: `0/4`.
- checkpoint-200 no-large-collapse languages: `0/4`.

Failure return:

- failed gate: retained early checkpoint rescue
- observed evidence: checkpoint-150 is worse than checkpoint-200 on both target10 and high-resource control proxies
- return-to stage: Stage 05 if pursuing a new checkpoint grid with checkpoint-50/100 retained or a safer replay schedule
- required fix: rerun Stage 05 with more frequent checkpoint retention and/or new replay/training settings

Next action:

- Keep diagnostic negative claim for current candidate.
- If pursuing positive claim, run a new Stage 05 branch rather than selecting among retained checkpoints.

## stage05_stage06_replay_safe_retry_20260613

Date: 2026-06-13

Stage: `05_mlm`, `06_eval`, `07_main_claim`

Status: PASS_DIAGNOSTIC_RETRY_BUT_FAIL_POSITIVE

Changed variables:

- Added a lower-LR replay-safe Stage 05 retry after the 200-step fvt pilot failed high-resource control.
- Kept the same XLM-R-base append-only tokenizer, fvt initialization, Stage 01 high-resource replay + target10 mixture, and full-model MLM objective.
- Changed only the optimization schedule: learning rate `5e-5 -> 1e-5`, max steps `200 -> 1000`, warmup `20 -> 100`.
- Evaluated the retry on target10 MLM proxy, high-resource control, and Coptic POS for seeds 13, 17, and 23.
- Added final goal and requirement-level completion audit documents.

Artifacts:

- docs: `05_mlm/replay_safe_seed_summary.tsv`
- docs: `05_mlm/training_config_replay_safe_seed13.json`
- docs: `05_mlm/training_config_replay_safe_seed17.json`
- docs: `05_mlm/training_config_replay_safe_seed23.json`
- docs: `06_eval/replay_safe_candidate_summary.tsv`
- docs: `06_eval/mlm_proxy_summary_replay_safe.tsv`
- docs: `06_eval/high_resource_control_summary_replay_safe.tsv`
- docs: `06_eval/coptic_pos_summary_replay_safe.tsv`
- docs: `final_goal_20260613.md`
- docs: `final_goal_completion_audit_20260613.md`
- docs: `final_goal_completion_audit_20260613.tsv`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed13_step1000`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed17_step1000`
- large: `/home/axt/mnt2/jongha/third_try/checkpoints/05_mlm/fvt_replay_safe_lr1e5_seed23_step1000`

Gate evidence:

- Stage 05 replay-safe mean final eval loss: `3.903145`, improved from 200-step mean `3.981250`.
- Target10 MLM proxy mean loss: `5.245928`, improved from 200-step `5.298593` but still worse than XLM-R `3.472837`.
- Target10 languages better than XLM-R: `5/10`.
- High-resource control mean delta vs XLM-R: `+0.675539`, improved from `+0.703114` but still `0/4` no-large-collapse languages.
- Coptic POS token accuracy delta: `+0.006781`, positive in 3/3 replay-safe checkpoint seeds.
- Coptic POS macro-F1 delta: `-0.002656`.

Failure return:

- failed gate: POSITIVE_MAIN_CLAIM
- observed evidence: replay-safe retry improves the pilot but does not rescue target10 proxy average, high-resource control, or target10-wide downstream coverage
- return-to stage: `05_mlm`
- required fix: stronger replay/control schedule or larger budget, then rerun high-resource control and target10 downstream/proxy-downstream evaluation

Next action:

- Use diagnostic negative wording for the current report package.
- Keep `first_try` and `second_try` as ablation/failure analysis.
