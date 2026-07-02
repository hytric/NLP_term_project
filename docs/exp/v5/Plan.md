# v5 Plan

작성일: 2026-06-28

## One-Line Thesis

v5는 Glot500의 핵심 흐름을 `92 seen + 10 Glot500-internal target` 설정으로
재연하고, vocabulary extension 이후 새 token embedding row 초기화 방법론을
비교한 뒤, Glot500에서 측정한 모든 downstream metric을 head/tail/all 관점으로
평가하는 실험이다.

## Research Questions

1. Glot500 방식의 tokenizer expansion과 continued MLM pretraining을 작은
   102-language setting에서 재현하면 XLM-R-base 대비 head/tail/all 지표가
   개선되는가?
2. 새 vocabulary row를 random으로 두는 것보다 source tokenizer 기반
   initialization이 zero-step 및 after-MLM 성능을 개선하는가?
3. MLM proxy 개선이 Glot500 downstream metric 전체로 이어지는가?

## Sources

- Glot500 GitHub: `https://github.com/cisnlp/Glot500`
- Glot500 paper: `https://aclanthology.org/2023.acl-long.61/`
- Yamaguchi et al. vocabulary expansion paper:
  `https://aclanthology.org/2026.cl-1.9/`
- Yamaguchi et al. official code:
  `https://github.com/gucci-j/lowres-cve`
- v5 feedback note: `docs/exp/v5/feadback.md`
- v5 data note: `docs/exp/v5/0_tokenizer/dataset_processing.md`

## Experimental Setting

### Data

- Head/seen group: v4와 같은 XLM-R seen Glot500 `92` language-scripts.
- Tail/target group: Glot500 raw 안에 있고, XLM-R seen이 아니며,
  `new_length >= 30000`인 후보 중 지역/문자/어족 다양성을 고려해 고른 `10`개.
- v5 target10:
  `fur_Latn`, `krc_Cyrl`, `acm_Arab`, `dzo_Tibt`, `sat_Olck`, `mad_Latn`,
  `bam_Latn`, `kjb_Latn`, `quw_Latn`, `rap_Latn`.
- Correction after coverage audit: this target10 has `0/10` direct downstream
  coverage outside PPPL. If the goal includes target-language downstream
  evidence, use `TARGET10_RESELECTION_FOR_DOWNSTREAM_KO.md` and
  `0_tokenizer/00_data_scope/target_candidate_task_overlap.md` to select a
  downstream-aware target set before rerunning merge/tokenizer/training.
- Held-out correction after Glot500 protocol audit: Glot500 computes PPPL on a
  held-out test split. Current v5 PPPL rows use local raw `train` splits and are
  therefore train-source diagnostics only. Strict held-out PPPL is moved to
  v5.1; see `MLM_HELDOUT_POLICY_KO.md`.
- Current dry-run corpus size:
  `92,452,251` planned lines.

### Model Matrix

| Label | Model/Checkpoint | Role |
| --- | --- | --- |
| `xlmr_base` | `xlm-roberta-base` | no-adaptation baseline |
| `glot500_base` | `cis-lmu/glot500-base` | external reference model |
| `v5_random` | XLM-R + v5 tokenizer + HF default resize | Glot500-style random init baseline |
| `v5_mean` | XLM-R + v5 tokenizer + source/global mean init | simple stable init ablation |
| `v5_fvt` | XLM-R + v5 tokenizer + source-token decomposition mean | main novelty candidate |
| `v5_align` | XLM-R + v5 tokenizer + character/script-aware fallback | exploratory ablation |

Minimum report matrix: `xlmr_base`, `glot500_base`, `v5_random`, `v5_fvt`.

Executable model matrix:

```text
docs/exp/v5/3_evaluation/model_matrix.tsv
```

Regenerate it with:

```bash
python3 scripts/write_v5_eval_model_matrix.py
```

## Progression Rule

각 단계는 해당 폴더의 `README.md`에 적힌 `Stage Exit Line` 또는
`Next Step Gate`를 넘었을 때만 다음 단계의 main experiment로 이동한다. gate를
넘지 못한 결과는 pilot, debug, ablation, or blocked로 라벨링하고 main claim에는
사용하지 않는다.

## Phase Plan

### Phase 0. Freeze Data Scope

Status: mostly done.

Deliverables:

- `docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv`
- `docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv`
- `docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json`

Checks:

- Selected target languages exist in `/disk3/moon/Glot500/data/raw`.
- Selected target languages have `new_length >= 30000`.
- If target downstream claims are required, selected target languages must
  overlap with at least one local downstream evaluation resource where possible.
- For strict PPPL reproduction, dev/test examples must be held out before
  merge/tokenizer/MLM. The current v5 merge did not do this, so v5 PPPL is a
  diagnostic line and v5.1 is the strict held-out correction line.
- v5 raw has exactly `102` symlinks.
- Head/tail labels are explicitly documented.

### Phase 1. Tokenizer Expansion

Goal: reproduce Glot500-style tokenizer expansion by training an auxiliary
SentencePiece tokenizer and appending novel pieces to the base XLM-R SPM.

Full merge command:

```bash
python3 preprocessing/merge_files.py \
  --data_directory /home/axt/mnt2/jongha/v5_glot50010/raw \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/data \
  --experiment_name Glot500_v5_glot50010_xlmr100 \
  --stats_csv docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv \
  --manifest_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv \
  --report_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json \
  --missing_policy fail
```

Tokenizer command:

```bash
python3 tokenization/run.py \
  --input_fname /home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt \
  --model_name xlm-roberta-base \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/tokenization/output \
  --vocab_size 250000
```

Audits:

- base vocab size, target vocab size, appended token count
- `<mask>` source id vs target id
- byte fallback piece count
- target10 `<unk>` rate and fertility
- head/tail tokenization comparison

### Phase 2. Embedding Initialization

Goal: build initialized checkpoints before MLM training, then compare zero-step
and after-training behavior.

Methods:

- `random`: Hugging Face `resize_token_embeddings()` only.
- `mean`: target-only lexical rows from source/global mean vector.
- `fvt`: new target token surface -> source tokenizer -> source subtoken mean.
- `align`: character/script-aware fallback for poor `fvt` decompositions.

Correctness rules:

- Copy old rows by token identity, not id prefix.
- Explicitly remap source `<mask>` row to target `<mask>` id.
- Report byte fallback rows separately.
- Initialize input embedding and LM head consistently.
- Call/check weight tying.
- Save `init_report.json` for every checkpoint.

Zero-step outputs:

- head, tail, all, v5-target MLM proxy
- new-row norm table
- source row preservation audit
- `<mask>` and byte-row audit

### Phase 3. Continued MLM Pretraining

Goal: train method checkpoints under the same MLM budget.

Recommended order:

1. Pilot run with `--max_samples_per_language` or reduced scale, 1K-2K steps.
2. Main short run with checkpoints at 10K, 20K, 30K, 40K.
3. Train `v5_random` and `v5_fvt` first.
4. Add `v5_mean` and `v5_align` if compute allows.

Fixed settings:

- base model: `xlm-roberta-base`
- tokenizer: v5 extended tokenizer
- objective: MLM
- max length: `512`
- learning rate: `5e-5`
- effective batch: `384` if GPU allows
- fixed seeds and checkpoint interval

### Phase 4. Glot500 Metric Evaluation

Glot500에서 측정한 metric은 v5에서도 모두 필수 측정한다. task coverage가
제한되는 언어가 있더라도 metric 자체를 생략하지 않고, measured languages,
excluded languages, exclusion reason을 함께 남긴다.

| ID | Metric | Primary score | Required |
| --- | --- | --- | --- |
| `pppl` | Pseudoperplexity | PPPL / MLM proxy loss | yes, but v5 `train` rows are diagnostic only |
| `retrieval_tatoeba` | Sentence Retrieval Tatoeba | Top-10 accuracy | yes |
| `retrieval_bible` | Sentence Retrieval Bible | Top-10 accuracy | yes |
| `text_classification` | Text Classification | F1 | yes |
| `ner` | Named Entity Recognition | F1 | yes |
| `pos` | POS Tagging | F1 | yes |
| `roundtrip_alignment` | Roundtrip Alignment | accuracy | yes |

Coverage rules:

- Every metric must have a coverage artifact.
- If selected v5 target language lacks data, list it in coverage rather than
  silently dropping it.
- Main tables report head/tail/all.
- Separate tables report v5-target subset where available.

Execution wrapper:

```bash
ALLOW_TRAIN_SOURCE_PPPL=1 PPPL_EVAL_ROLE=train_source_diagnostic \
  bash scripts/run_v5_eval_metric.sh pppl xlmr_base 2
bash scripts/run_v5_eval_metric.sh retrieval_tatoeba glot500_base 2
```

Use the wrapper for final runs so inherited v4 output defaults are not used.
For strict Glot500-style PPPL, do not use `PPPL_SPLIT=train`; first create a
held-out split in v5.1, then run with `PPPL_SPLIT=test
PPPL_EVAL_ROLE=heldout_test`.
After metric runs, refresh aggregation:

```bash
python3 scripts/aggregate_v5_metrics.py
```

### Phase 5. Reporting

Required reporting artifacts:

- tokenizer audit table
- initialization audit table
- MLM training curves
- Glot500 metric completion checklist
- main downstream head/tail/all table
- v5-target subset coverage table
- optional embedding similarity map

## Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Corpus is large | dry-run is `92.45M` lines | run pilot first; log wall time and disk |
| Task coverage differs by metric | selected target10 not always labeled | still run metric; report coverage/exclusions |
| Eval/train overlap | Bible/retrieval may share source family | run duplicate/leakage audit |
| `<mask>` id drift | invalidates naive prefix-copy init | identity-based checkpoint builder |
| Byte fallback rows | can distort row audit | report byte rows separately |
| Random baseline may catch up | long MLM may shrink init differences | compare zero-step, early-step, final |
| Appended SPM score mismatch | new short pieces can outcompete useful base pieces, as seen in pilot `dzo_Tibt` | re-run fertility audit on the full tokenizer and analyze per-language regressions |

## Immediate Next Actions

Current execution line, after full merge/tokenizer/init/zero-step and matched
10K checkpoint completion:

1. Keep downstream coverage current with
   `python3 scripts/audit_v5_eval_coverage.py`; data materialization is already
   documented for retained metric families.
2. Run `bash scripts/run_v5_post_checkpoint_evals.sh status`, then launch only
   after `READY_TO_LAUNCH=yes`; because post-10K `v5_random` rows are already
   measured, prefer downstream-only completion first:
   `SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh downstream`.
3. If a matched train-source PPPL diagnostic is still needed, run it only with
   `RUN_TRAIN_SOURCE_PPPL_DIAGNOSTIC=1`; do not promote it as held-out test
   PPPL.
4. Run `python3 scripts/refresh_v5_reporting.py --with-plots` after completed
   metric batches.
5. Update Report/PPT only from measured artifacts and explicit blocked/excluded
   notes.
6. Create v5.1 strict held-out split if final held-out PPPL is required.

Historical canonical launch order:

```bash
DRY_RUN=1 bash preprocessing/run_v5_glot50010_merge.sh
bash preprocessing/run_v5_glot50010_merge.sh
bash tokenization/train_v5_glot50010.sh
bash scripts/run_v5_build_initializers.sh
python3 scripts/audit_v5_eval_coverage.py
python3 scripts/write_v5_eval_model_matrix.py
INIT_MODEL_DIR=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_random \
  RUN_NAME=v5_random_mlm \
  bash modeling/train_v5_glot50010_mlm.sh
INIT_MODEL_DIR=/home/axt/mnt2/jongha/v5_glot50010/initialized_models/v5_fvt \
  RUN_NAME=v5_fvt_mlm \
  bash modeling/train_v5_glot50010_mlm.sh
python3 scripts/aggregate_v5_metrics.py
```

## Main Execution Blockers

The experiment should not be treated as main-result-ready until these blockers
are cleared:

- matched `v5_random` and `v5_fvt` 10K MLM checkpoints exist;
- checkpoint selection records why the chosen checkpoints are comparable;
- downstream coverage remains materialized or explicitly excluded for every
  Glot500-required metric;
- all metric runs use v5 evaluation output directories instead of inherited v4
  defaults;
- `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv` marks every
  metric as measured or explicitly blocked/excluded.
