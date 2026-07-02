# v5 Glot500-Internal Target10 Rerun

이 README는 v5의 현재 진행 상황, 전체 폴더 구조, 그리고 큰 그림을 관리한다.
실행 계획은 `Plan.md`, 보고서 구성과 결과 계획은 `Report.md`를 기준으로 한다.

먼저 볼 문서: `CURRENT_STATUS_KO.md`
최종 실험 framing 결정: `../FINAL_EXPERIMENT_DECISION_KO.md`
v5.2 최종 보고 version: `../v5.2/README.md`
발표/보고서용 단계별 진행보고: `PROGRESS_REPORT_KO.md`
tokenizer 확장 방법 판정: `TOKENIZER_EXTENSION_METHODS_KO.md`
언어 소스/coverage overlap: `LANGUAGE_SOURCE_OVERLAP_KO.md`
target10 downstream 재선정 audit: `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md`
MLM/PPPL held-out 정책: `MLM_HELDOUT_POLICY_KO.md`

GPU note: the active paired 10K MLM launch uses physical GPUs `2,3`.
Post-checkpoint evaluation commands pass `GPU_RANDOM` and `GPU_FVT` directly to
`CUDA_VISIBLE_DEVICES`, so treat those values as physical GPU ids and check
`nvidia-smi` before launching a long evaluation. The generated examples use
`GPU_RANDOM=0 GPU_FVT=1`; override them if those devices are occupied.

## Top-Level Documents

| File | Role |
| --- | --- |
| `../FINAL_EXPERIMENT_DECISION_KO.md` | v5 main / v5.1 diagnostic 최종 판단 |
| `../v5.2/README.md` | 최종 보고용 v5.2 framing |
| `CURRENT_STATUS_KO.md` | 지금 무엇을 하는지, 단계별 체크포인트, 핵심 결과, 다음 명령 |
| `PROGRESS_REPORT_KO.md` | 발표/보고서용 단계별 진행보고, 수행 체크리스트, 핵심 결과 |
| `DATA_COMPOSITION_KO.md` | 언어별 XLM-R 포함 여부, train/dev/test 또는 task count 요약 |
| `LANGUAGE_SOURCE_OVERLAP_KO.md` | XLM-R 학습 언어 label, 별도 Glot500 raw data, task eval data의 overlap 설명 |
| `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md` | 현재 target10 downstream coverage 문제와 재선정 후보 |
| `TOKENIZER_EXTENSION_METHODS_KO.md` | Glot500/Yamaguchi tokenizer 확장 방법 비교와 v5 최종 사용 방법 판정 |
| `MLM_HELDOUT_POLICY_KO.md` | v5 train-source PPPL diagnostic과 v5.1 strict held-out PPPL 분리 정책 |
| `README.md` | 현재 상태, 폴더 구조, artifact map |
| `Plan.md` | 실험 계획, phase별 실행 순서, required metrics |
| `Report.md` | 리포트 구성, 내용 초안, 결과표 계획 |
| `goal_readiness.md` | actual artifact 기준 실행 준비도 audit |
| `folder_readme_audit.md` | 각 폴더 README와 next-line 문서화 audit |
| `4_reporting/final_package_checklist.md` | final report/PPT package completion gates |

Raw feedback note:

- `feadback.md`

## Current Status

최종 framing은 v5를 본 실험으로 둔다. v5 target10은 corpus-size 기준으로
`genuine low-resource XLM-R-unseen target10`이다. 현재 repo에서 확인 가능한 local task-list
membership은 `8/10`에 일부 있지만, 기존 로컬 coverage/materialization 산출물은
tail flag를 availability로 오해해 undercount했으므로 repair 전까지 target downstream
improvement는 주장하지 않는다. v5.1은 downstream-aware diagnostic/ablation으로 둔다.

### Done

- v5 target10을 Glot500 내부 raw dataset에서 다시 선정했다.
- target10은 모두 `XLM-R != True`, `new_length >= 30000`, raw directory 존재 조건을
  만족한다.
- target10은 지역/문자/어족 다양성을 고려해 선정했다.
- v5 raw symlink root를 만들었다:
  `/home/axt/mnt2/jongha/v5_glot50010/raw`
- v5 raw symlink count: `102`
- merge dry-run completed with missing dirs `0`.
- Glot500 required metrics를 모두 필수 측정 대상으로 문서화했다.
- phase별/metric별 결과 폴더를 나눴다.
- pilot merge `Glot500_v5_glot50010_xlmr100_pilot10k` completed:
  `1,020,000` lines, missing dirs `0`.
- pilot tokenizer training completed with `VOCAB_SIZE=50000`; it appended
  `7,591` tokens to XLM-R.
- pilot tokenizer audit completed on `20` head languages + `10` targets.
- pilot FVT initialization smoke test passed with `<mask>` remap diff `0.0`.
- pilot zero-step MLM proxy completed for `v5_random`, `v5_mean`, and `v5_fvt`
  on `5` head languages + `10` targets.
- evaluation model matrix, v5 metric runner, aggregation skeleton, and goal
  readiness audit are written.
- full merge `Glot500_v5_glot50010_xlmr100` completed:
  `92,452,251` lines, `19G`, missing dirs `0`, manifest rows `102/102 PASS`.
- main tokenizer training completed on the full corpus. It appended `118,685`
  tokens to XLM-R and passed the main tokenizer audit on `20` head languages +
  `10` targets.
- full `v5_random`, `v5_mean`, and `v5_fvt` initialized checkpoints were built
  on the main tokenizer and passed `<mask>`/LM-head audits.
- main zero-step MLM proxy completed for `v5_random`, `v5_mean`, and `v5_fvt`
  on `5` head languages + `10` targets.
- paired 10K MLM run completed for `v5_random` and `v5_fvt`.
- baseline PPPL for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline PPPL for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Tatoeba retrieval for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Tatoeba retrieval for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Bible retrieval for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Bible retrieval for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Taxi1500 text classification for `xlmr_base` completed and is
  visible in `3_evaluation/09_aggregation/`.
- baseline Taxi1500 text classification for `glot500_base` completed and is
  visible in `3_evaluation/09_aggregation/`.
- baseline NER for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline NER for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline POS for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline POS for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Roundtrip alignment for `xlmr_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- baseline Roundtrip alignment for `glot500_base` completed and is visible in
  `3_evaluation/09_aggregation/`.
- post-10K `v5_random` PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and
  Roundtrip rows are measured and visible in `3_evaluation/09_aggregation/`.
  Treat these as diagnostic rows until the paired `v5_fvt` rows are available.
- downstream data materialization completed for Tatoeba, PAN-X/NER, UD-POS, and
  Taxi1500 local English split; Bible and Roundtrip local coverage is
  documented in `3_evaluation/00_coverage/` and `3_evaluation/07_roundtrip_alignment/`.
- Glot500 held-out PPPL policy is documented. Current v5 `PPPL_SPLIT=train`
  rows are retained only as train-source intrinsic diagnostics; strict
  held-out PPPL is assigned to v5.1.
- report/PPT, rendered artifacts, and release bundle exist as an execution
  draft with explicit pending gates.

### Waiting

- paired `v5_random`/`v5_fvt` post-checkpoint evaluation rows
- strict held-out PPPL correction line in v5.1
- final result promotion into report/PPT conclusions

### In Progress

- post-checkpoint `v5_fvt` evaluation rows for available downstream metrics
- PPPL relabeling: v5 diagnostic rows are separated from v5.1 held-out test rows

## Goal Readiness Audit

Verdict: data scope, full merge, main tokenizer/audit, full initialization, and
main zero-step eval are ready, but the full main experiment is not
execution-complete yet. Do not claim main v5 model results until MLM training
and downstream evaluation blockers are cleared.

| Area | Readiness | Evidence | Blocking line |
| --- | --- | --- | --- |
| Stage goals | ready | stage/metric README files have gates, pass lines, and required artifacts; artifact/log README files document evidence locations | none |
| Data scope | ready | manifest/stats exist, raw symlink count is `102`, dry-run missing dirs is `0` | none |
| Glot500-style replay | ready as a subset design | uses `92 seen + 10 Glot500-internal target` and all Glot500 metric categories | not a full 511-language reproduction |
| Full merge | ready | main report is `PASS`, actual lines equal planned `92,452,251` | none |
| Tokenizer training | ready | main tokenizer appended `118,685` tokens and audit has failures `0` | none |
| Embedding initialization | ready | full `random`/`mean`/`fvt` reports have `<mask>` diff `0.0` and LM-head tied `true` | none |
| MLM training | ready | matched 10K `v5_random` and `v5_fvt` checkpoints exist and are selected | none |
| Evaluation | partial v5 rows measured, paired FVT downstream rows pending | model matrix, runner, coverage, aggregation exist; PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip are measured for `xlmr_base`, `glot500_base`, and `v5_random` where local data exists; current coverage files are valid as local materialized rows but undercount local tail task membership because task-list flag `0` was treated as unavailable; v5 target10 local membership is `8/10` for Tatoeba/Bible/NER/POS lists | repair tail materialization/coverage logic before target downstream claim; run guarded post-checkpoint downstream wrapper for `v5_fvt`; keep current PPPL as train-source diagnostic only |
| Novelty | well positioned | FVT/mean/align, zero-step eval, row audits, early/final MLM comparison | keep `v5_random` and `v5_fvt` directly comparable |

## Reproduction Boundary

v5 can support this claim after execution:

```text
We reproduce the Glot500 training/evaluation pattern on a controlled
102-language subset.
```

v5 should not claim this:

```text
We perfectly reproduce the full Glot500 511-language experiment.
```

The difference matters. The v5 design preserves the Glot500-style tokenizer
expansion, continued MLM pretraining, head/tail/all reporting, and required
metric families, but it intentionally uses a smaller controlled language set and
a smaller compute budget.

PPPL boundary: Glot500 computes PPPL on held-out test data. Current v5 PPPL rows
were produced from local raw `train` splits and are therefore train-source
intrinsic diagnostics. They can compare matched v5 conditions but cannot be
reported as final Glot500 held-out PPPL. The strict held-out correction is
documented as v5.1 in `MLM_HELDOUT_POLICY_KO.md`.

Downstream coverage boundary: the selected target10 has raw text for PPPL and
partial local task-list membership, mainly Bible plus one NER and one POS
case. Existing local materialization/coverage rows undercounted this because
task-list flag `0` is tail, not unavailable. Therefore target10 claims should
rely on tokenization, zero-step/after-MLM proxy metrics, and repaired coverage
notes until Bible/NER/POS tail materialization is rerun; downstream tables should
be framed as available-language/head/all Glot500 metric replay.

## Novelty Placement

The novelty is best framed as embedding initialization after vocabulary
extension, not as a new corpus or a new downstream task.

Primary novelty line:

```text
For newly appended SentencePiece rows, source-token decomposition initialization
can improve zero-step and early-step behavior compared with random resize.
```

Evidence required for that claim:

- `v5_random` and `v5_fvt` use the same tokenizer, corpus, seed, schedule, and
  checkpoint selection rule.
- zero-step MLM proxy is measured before training.
- early-step checkpoints are compared before long MLM can wash out the
  initialization effect.
- source-row preservation, `<mask>` remap, byte-row handling, and LM-head tying
  are audited.
- downstream results are reported separately from initialization diagnostics.

## v5 Data Summary

| Item | Value |
| --- | ---: |
| seen/head language-scripts | 92 |
| target/tail language-scripts | 10 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 363,421 |
| planned seen samples | 82,943,520 |
| planned target samples | 9,508,731 |
| planned total samples | 92,452,251 |

Selected v5 target10:

```text
fur_Latn
krc_Cyrl
acm_Arab
dzo_Tibt
sat_Olck
mad_Latn
bam_Latn
kjb_Latn
quw_Latn
rap_Latn
```

## Folder Structure

```text
docs/exp/v5/
├── 0_tokenizer/
│   ├── 00_data_scope/
│   ├── 01_merge/
│   ├── 02_tokenizer_train/
│   └── 03_audit/
├── 1_embedding/
│   ├── 00_random/
│   ├── 01_mean/
│   ├── 02_fvt/
│   ├── 03_align/
│   ├── 04_zero_step_eval/
│   └── 05_audit/
├── 2_training/
│   ├── 00_pilot/
│   ├── 01_random/
│   ├── 02_fvt/
│   ├── 03_mean/
│   ├── 04_align/
│   └── 05_checkpoint_selection/
├── 3_evaluation/
│   ├── 00_coverage/
│   ├── 01_pseudoperplexity/
│   ├── 02_retrieval_tatoeba/
│   ├── 03_retrieval_bible/
│   ├── 04_text_classification/
│   ├── 05_ner/
│   ├── 06_pos/
│   ├── 07_roundtrip_alignment/
│   ├── 08_embedding_similarity/
│   └── 09_aggregation/
└── 4_reporting/
    ├── 00_tables/
    ├── 01_figures/
    ├── 02_slides/
    └── 03_final_report/
```

## Folder Roles

| Folder | Purpose |
| --- | --- |
| `0_tokenizer/` | data scope, merge, tokenizer training, tokenizer audit |
| `1_embedding/` | `random`, `mean`, `fvt`, `align` initialization and zero-step eval |
| `2_training/` | pilot and method-specific MLM runs |
| `3_evaluation/` | all Glot500 required metrics, coverage, aggregation |
| `4_reporting/` | final tables, figures, slides, report package |

## Stage Gates

각 단계는 아래 line을 넘었을 때만 다음 단계로 이동한다. line을 넘지 못하면
다음 단계 결과를 만들더라도 report main claim에는 사용하지 않는다.

| Stage | Move to next stage when | Next |
| --- | --- | --- |
| `0_tokenizer/` | data scope is frozen, merge report has missing dirs `0`, tokenizer exists, and tokenizer audit passes | `1_embedding/` |
| `1_embedding/` | required init checkpoints have `init_report.json`, `<mask>`/LM-head audits pass, and zero-step eval is summarized | `2_training/` |
| `2_training/` | pilot is stable, comparable `v5_random` and `v5_fvt` checkpoints exist, and selected checkpoints are documented | `3_evaluation/` |
| `3_evaluation/` | every Glot500-required metric has coverage, command logs, raw output, and summary table or exclusion reason | `4_reporting/` |
| `4_reporting/` | final tables, figures, slides, and report are synchronized with measured artifacts | done |

## Required Glot500 Metrics

Glot500에서 측정한 metric은 v5에서도 모두 측정한다.

| Metric | Folder |
| --- | --- |
| Pseudoperplexity | `3_evaluation/01_pseudoperplexity/` |
| Sentence Retrieval Tatoeba | `3_evaluation/02_retrieval_tatoeba/` |
| Sentence Retrieval Bible | `3_evaluation/03_retrieval_bible/` |
| Text Classification | `3_evaluation/04_text_classification/` |
| NER | `3_evaluation/05_ner/` |
| POS | `3_evaluation/06_pos/` |
| Roundtrip Alignment | `3_evaluation/07_roundtrip_alignment/` |

Every metric folder should contain command logs, raw outputs, summary TSV/JSON,
and `results.md` once measured.

## Canonical Artifacts

- selected target manifest:
  `docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`
- candidate pool:
  `docs/exp/v5/0_tokenizer/miscellaneous/glot500_candidate_pool_min30k.tsv`
- stats CSV:
  `docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv`
- merge dry-run manifest:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv`
- merge dry-run report:
  `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`
- metric requirements:
  `docs/exp/v5/3_evaluation/glot500_metric_requirements.md`

## Execution Scripts

Use these wrappers for v5 so paths do not silently fall back to older v4
experiments.

| Step | Script | Purpose |
| --- | --- | --- |
| merge | `preprocessing/run_v5_glot50010_merge.sh` | dry-run, pilot, or full corpus merge |
| tokenizer | `tokenization/train_v5_glot50010.sh` | prepare XLM-R base SPM and train extended tokenizer |
| tokenizer audit | `scripts/audit_v5_tokenizer.py` | vocab, `<mask>`, byte-row, fertility, `<unk>` audit |
| init | `scripts/build_v5_initialized_checkpoint.py` | build one SPM-append-aware initialized checkpoint |
| init batch | `scripts/run_v5_build_initializers.sh` | build `random`, `mean`, `fvt` checkpoints by default |
| MLM | `modeling/train_v5_glot50010_mlm.sh` | train one initialized checkpoint with shared v5 MLM settings |
| coverage | `scripts/audit_v5_eval_coverage.py` | coverage files for every Glot500-required metric |
| model matrix | `scripts/write_v5_eval_model_matrix.py` | write required/optional model paths for evaluation |
| checkpoint manifest | `scripts/write_v5_checkpoint_selection_manifest.py` | freeze selected checkpoint paths and 10K eligibility |
| metric runner | `scripts/run_v5_eval_metric.sh` | run one v5 metric/model pair with v5 output dirs |
| post-checkpoint wrapper | `scripts/run_v5_post_checkpoint_evals.sh` | guard and run paired v5 post-checkpoint metrics |
| checkpoint watcher | `scripts/watch_v5_mlm_handoff.sh` | poll until matched v5 checkpoints are ready, then run guarded status handoff |
| aggregation | `scripts/aggregate_v5_metrics.py` | write completion checklist and normalized score skeleton |
| reporting refresh | `scripts/refresh_v5_reporting.py` | regenerate gates, audits, tables, and report/PPT sync checks |
| readiness | `scripts/audit_v5_goal_readiness.py` | write artifact-based goal readiness audit |

Operational evaluation handoff:

- `docs/exp/v5/3_evaluation/execution_queue.md`
- `docs/exp/v5/3_evaluation/next_runbook.md`

## Current Pilot Evidence

| Artifact | Value |
| --- | --- |
| pilot corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100_pilot10k.txt` |
| pilot lines | `1,020,000` |
| pilot corpus size | `212M` |
| pilot merge report | `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100_pilot10k.report.json` |
| pilot tokenizer | `/home/axt/mnt2/jongha/v5_glot50010/tokenization/pilot10k_output/Glot500_extended_spm` |
| appended token count | `7,591` |
| byte token count | `256` |
| `<mask>` id | XLM-R `250001` -> pilot tokenizer `257592` |
| FVT init smoke | `docs/exp/v5/1_embedding/05_audit/pilot10k/fvt_init_report.json` |
| zero-step MLM proxy | `docs/exp/v5/1_embedding/04_zero_step_eval/pilot10k/results.md` |

Pilot tokenizer result: `9/10` target languages reduced tokens/word; `dzo_Tibt`
regressed strongly in the pilot tokenizer and should be analyzed before main
claims. Excluding `dzo_Tibt`, target tokens/word delta is `-0.304514`.

Pilot zero-step result: `v5_fvt` improves target weighted NLL over `v5_random`
by `-9.448385` and over `v5_mean` by `-3.423689`. This is pilot evidence for the
embedding-initialization novelty, not a final result.

Current readiness audit:

- `docs/exp/v5/goal_readiness.md`
- `docs/exp/v5/3_evaluation/model_matrix.tsv`
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`

## Current Main Merge Evidence

| Artifact | Value |
| --- | --- |
| main corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt` |
| line count | `92,452,251` |
| file size | `19G` |
| merge report | `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json` |
| merge manifest | `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv` |
| command log | `/home/axt/mnt2/jongha/v5_glot50010/logs/full_merge_20260626_230847.log` |
| report status | `PASS` |
| manifest status | `102/102 PASS` |
| missing dirs | `0` |

## Current Main Tokenizer Evidence

| Artifact | Value |
| --- | --- |
| main tokenizer | `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm` |
| training log | `docs/exp/v5/0_tokenizer/02_tokenizer_train/logs/train_v5_tokenizer_20260627_000941.log` |
| sampled sentences | `20,000,000` from `92,309,510` SPM-valid sentences |
| skipped too-long sentences | `142,722` |
| base vocab size | `250,002` |
| main vocab size | `368,687` |
| appended token count | `118,685` |
| byte token count | `256` |
| `<mask>` id | XLM-R `250001` -> main tokenizer `368686` |
| audit folder | `docs/exp/v5/0_tokenizer/03_audit/main/` |
| audit failures | `0` |

Main tokenizer audit: `29/30` audited languages reduced tokens/word. Target10:
`9/10` improved, with average delta `-0.390862`; excluding `dzo_Tibt`, target
average delta is `-0.581867`. `dzo_Tibt` remains a controlled failure case:
main delta `+1.328186`, improved from the pilot regression but still worse than
XLM-R.

## Current Main Embedding Evidence

| Artifact | Value |
| --- | --- |
| initialized model root | `/home/axt/mnt2/jongha/v5_glot50010/initialized_models/` |
| docs init reports | `docs/exp/v5/1_embedding/05_audit/main/init_reports/` |
| zero-step results | `docs/exp/v5/1_embedding/04_zero_step_eval/main/results.md` |
| FVT initialized rows | `118,427` |
| FVT fallback lexical rows | `2` |
| byte rows | `256` |
| `<mask>` id | XLM-R `250001` -> main tokenizer `368686` |
| `<mask>` diff | `0.0` for `random`, `mean`, `fvt` |
| LM head tied | `true` for `random`, `mean`, `fvt` |
| v5-target zero-step `fvt - random` | weighted NLL `-9.626238` |
| v5-target zero-step `fvt - mean` | weighted NLL `-3.167624` |

## Current Training Launch

| Artifact | Value |
| --- | --- |
| launcher | `modeling/launch_v5_random_fvt_10k.sh` |
| launcher PID | `1868654` |
| run order | `v5_random_mlm_10k` then `v5_fvt_mlm_10k` |
| GPUs | `2,3` |
| max steps | `10,000` |
| save steps | `10,000` |
| random output dir | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k` |
| fvt output dir | `/home/axt/mnt2/jongha/v5_glot50010/runs/v5_fvt_mlm_10k` |
| launch log | `/home/axt/mnt2/jongha/v5_glot50010/runs/launch_logs/launch_random_fvt_10k_setsid_20260627_005616.log` |
| current status | `docs/exp/v5/3_evaluation/running_status.md` generated from live logs; no selected checkpoint yet |

## Next Action

Let the paired `v5_random` -> `v5_fvt` 10K MLM run finish, then refresh the
checkpoint manifest. Execute the guarded paired post-checkpoint evaluation
wrapper only after `post_checkpoint_preflight.md` reports
`post_checkpoint_preflight_ready_to_launch`:

```bash
bash scripts/run_v5_post_checkpoint_evals.sh status
WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
python3 scripts/refresh_v5_reporting.py --with-plots
```

The `GPU_RANDOM` and `GPU_FVT` values above are physical GPU ids consumed by
`scripts/run_v5_eval_metric.sh`. If GPUs `0,1` are not free at handoff time, use
the same command with free checked devices, for example
`GPU_RANDOM=2 GPU_FVT=3`.

Optional status-only watcher while the MLM pair is still running:

```bash
POLL_SECONDS=300 bash scripts/watch_v5_mlm_handoff.sh
```

This watcher stops after the matched checkpoints are selectable and runs the
guarded `status` handoff. It does not launch the long paired evaluation unless
`RUN_ALL=1` is explicitly set.

Baseline/reference PPPL, Tatoeba, Bible, Taxi1500, NER, POS, and Roundtrip rows
are already measured where local data exists. Metrics without local data should
remain explicit blocked-data rows rather than being omitted.
