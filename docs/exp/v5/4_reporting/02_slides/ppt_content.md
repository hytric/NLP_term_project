# v5 Presentation Content Draft

작성 상태: execution draft with explicit result gates.

Live checkpoint progress and post-checkpoint Go/No-Go should be read from
`docs/exp/v5/4_reporting/final_action_dashboard_ko.md` and
`bash scripts/run_v5_post_checkpoint_evals.sh status`, not from this static
content draft.

## Slide 1. Title

Title:

```text
Reproducing Glot500 on a Controlled 102-Language Setting
with Vocabulary-Extension Initialization
```

Subtitle:

```text
92 XLM-R seen Glot500 languages + 10 diverse Glot500-internal target languages
```

Speaker note:

```text
오늘 발표는 Glot500 전체 511개 언어를 그대로 재학습하는 것이 아니라,
Glot500의 핵심 실험 흐름을 계산 가능한 102개 language-script setting으로
재연하고, vocabulary extension 후 새 embedding row를 어떻게 초기화할지
비교하는 실험입니다.
```

## Slide 2. Motivation And Contributions

Main message:

```text
Multilingual coverage is broad but uneven, so v5 turns Glot500 reproduction into
a controlled setup for testing vocabulary-row initialization.
```

Bullets:

- XLM-R supports many languages, but coverage is uneven.
- Glot500 expands corpus, tokenizer, and continued pretraining to improve
  low-resource coverage.
- Reproduction contribution: artifact-audited 92+10 Glot500-style replay.
- Novelty contribution: appended vocabulary row initialization, centered on FVT.
- Fidelity contribution: PPPL, retrieval, classification, tagging, and Roundtrip
  metric families are retained with explicit coverage/blocker accounting.
- Claim rule: final method claims wait for matched `v5_random`/`v5_fvt`
  checkpoints and parsed evaluation rows.

Visual:

- `docs/exp/v5/4_reporting/01_figures/generated/figure_01_experiment_pipeline.png`

## Slide 3. Reproduction Boundary

Main message:

```text
We reproduce the Glot500 pattern, not the full 511-language scale.
```

Table:

| Item | Glot500 | v5 |
| --- | --- | --- |
| corpus scale | 500+ languages | 102 language-scripts |
| head/seen | XLM-R-supported languages | 92 local XLM-R seen Glot500 languages |
| tail/target | low-resource languages | 10 Glot500-internal non-XLM-R target languages |
| tokenizer | SentencePiece extension | SentencePiece append-style extension |
| training | continued MLM | continued MLM |
| evaluation | Glot500 metrics | same metric families |

Speaker note:

```text
따라서 발표에서는 full Glot500 reproduction이라고 말하지 않고,
controlled subset reproduction이라고 표현합니다.
```

## Slide 4. Target10 Selection

Main message:

```text
Target languages are selected from Glot500 itself, with at least 30K rows and
regional/script diversity.
```

Table source:

```text
docs/exp/v5/0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv
```

Display languages:

```text
fur_Latn, krc_Cyrl, acm_Arab, dzo_Tibt, sat_Olck,
mad_Latn, bam_Latn, kjb_Latn, quw_Latn, rap_Latn
```

Visual:

- world/region list or compact table with region/script/new_length

## Slide 5. Corpus Construction

Main message:

```text
The v5 corpus keeps the Glot500 sampling logic while limiting the language set.
```

Current dry-run values:

| Item | Value |
| --- | ---: |
| seen languages | 92 |
| target languages | 10 |
| source seen sentences | 1,025,635,434 |
| source target sentences | 363,421 |
| planned total samples | 92,452,251 |
| missing language dirs | 0 |

Measured merge status:

```text
Pilot merged corpus lines: 1,020,000
Main merged corpus lines: 92,452,251
Main merged corpus size: 19G
Main merge status: PASS, 102/102 language rows
```

## Slide 6. Tokenizer Method

Main message:

```text
v5 follows the Glot500-style SentencePiece append route.
```

Compare:

| Method label | Implementation | Used as |
| --- | --- | --- |
| Glot500-style | train auxiliary SPM, append novel pieces to XLM-R SPM | v5 main |
| Yamaguchi-style | keep tokenizer ids and use add_tokens-style extension | prior ablation/inspiration |

Important warning:

```text
Special token ids, especially <mask>, must be audited after SPM append.
```

Measured tokenizer status:

- base vocab size: 250,002
- pilot extended vocab size: 257,593
- pilot appended token count: 7,591
- main extended vocab size: 368,687
- main appended token count: 118,685
- main `<mask>` source id -> target id: 250001 -> 368686
- byte fallback rows: 256

Pilot audit note:

```text
9/10 target languages improved tokens/word, but dzo_Tibt regressed.
The dzo_Tibt failure is not byte fallback or <unk>; 83.432% of v5 dzo_Tibt
tokens are newly appended pieces.
```

Main audit note:

```text
29/30 audited languages improved tokens/word.
Target10: 9/10 improved, average delta -0.390862.
Target10 excluding dzo_Tibt: average delta -0.581867.
dzo_Tibt remains worse: 4.223938 -> 5.552124 tokens/word.
```

Figure:

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_02_tokenizer_fertility_delta.png
```

## Slide 7. Novelty: Initialization Question

Main message:

```text
The novelty is not adding more data; it is testing initialization policies for
newly appended vocabulary rows.
```

Methods:

| Method | Meaning | Role |
| --- | --- | --- |
| random | HF-style random resize | baseline |
| mean | source/global mean | simple stable ablation |
| fvt | source-token decomposition mean | main novelty |
| align | Unicode/script-aware fallback | exploratory |

Speaker note:

```text
FVT asks whether a new target token can inherit a better starting vector from
how the original XLM-R tokenizer decomposes its surface form.
```

## Slide 8. Initialization Audit

Main message:

```text
Initialization is only meaningful if row-copy and special-token behavior are
correct.
```

Required audits:

- copy source rows by token identity, not id prefix
- remap source `<mask>` row to target `<mask>` id
- separate byte rows from lexical rows
- initialize input embedding and LM head consistently
- verify weight tying

Measured initialization status:

- main source row preservation: 250,002 copied by token identity
- main mask max abs diff: 0.0
- main LM head tied: true
- main FVT rows: 118,427
- main global fallback lexical rows: 2

Audit source:

```text
docs/exp/v5/1_embedding/05_audit/main/init_reports/fvt_init_report.json
```

## Slide 9. Zero-Step Evidence

Main message:

```text
FVT gives the best pre-training starting point on the intrinsic MLM proxy, but
zero-step evidence does not yet prove after-MLM or downstream gains.
```

Measured zero-step target weighted NLL:

| Method | Target weighted NLL |
| --- | ---: |
| random | 18.411756 |
| mean | 11.953142 |
| fvt | 8.785518 |

Measured zero-step deltas:

- `fvt - random`: -9.626238
- `fvt - mean`: -3.167624

Additional callout:

- FVT vs random relative weighted NLL reduction:
  - target: -52.28%
  - head: -48.65%
  - all: -51.31%
- comparison source: `docs/exp/v5/4_reporting/method_comparison_summary.md`

Figure:

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_03_zero_step_initialization.png
```

Promotion gate:

```text
Do not convert zero-step evidence into an after-MLM method claim until matched
`v5_random` and `v5_fvt` checkpoints are selected and evaluated.
```

## Slide 10. Training Setup

Main message:

```text
All initialization methods must share tokenizer, corpus, seed, schedule, and
checkpoint interval.
```

Table:

| Item | Value |
| --- | --- |
| base | XLM-R-base |
| objective | MLM |
| tokenizer | v5 extended tokenizer |
| max length | 512 |
| learning rate | 5e-5 |
| checkpoint interval | 10K steps |
| main comparison | v5_random vs v5_fvt |

Current training gate:

- paired 10K run: launched
- run order: v5_random_mlm_10k -> v5_fvt_mlm_10k
- GPUs: 2,3
- selected checkpoints: checkpoint-10000 if both runs complete
- current state: `v5_random_mlm_10k` selected 10K checkpoint exists;
  `v5_fvt_mlm_10k` is running, generated status in
  `docs/exp/v5/3_evaluation/running_status.md`
- execution caveat: `max_steps=10000` limits optimization, not preprocessing

Live execution snapshot, not final result:

| Job | Snapshot | Promotion gate |
| --- | --- | --- |
| `v5_random_mlm_10k` | selected 10K checkpoint exists; wrapper-ready | pair is promotable only after `v5_fvt` is also ready and post-checkpoint preflight is `post_checkpoint_preflight_ready_to_launch` |
| `v5_fvt_mlm_10k` | running; no model file yet | same 10K budget and checkpoint rule |
| `xlmr_base` NER | completed; `164` language rows parsed; all F1 `0.549858`, head F1 `0.621207`, v5-target actual intersection `0.459364` | ready as baseline row |
| `xlmr_base` POS | completed; all F1 `0.481336`, head F1 `0.571446`, `TRAIN_LANGS=tur_Latn` | ready as baseline row |
| `glot500_base` NER | completed and parsed; all F1 `0.627108`, head F1 `0.645915`, v5-target actual intersection `0.553191` | ready as external reference row |
| `glot500_base` POS | completed and parsed; all F1 `0.567542`, head F1 `0.573832`, `TRAIN_LANGS=tur_Latn` | ready as external reference row |
| `v5_random` NER | completed and parsed; all F1 `0.544628`, head F1 `0.608020`, v5-target actual intersection `0.560554` | ready as random-checkpoint row |
| `v5_random` POS | completed and parsed; all F1 `0.481102`, head F1 `0.587430`, `TRAIN_LANGS=tur_Latn` | ready as random-checkpoint row |

## Slide 11. Glot500 Metrics

Main message:

```text
Every metric family measured in Glot500 is retained.
```

Metrics:

- Pseudoperplexity
- Tatoeba sentence retrieval Top-10
- Bible sentence retrieval Top-10
- Text classification F1
- NER F1
- POS F1
- Roundtrip alignment accuracy

Speaker note:

```text
Coverage may differ by task, so missing selected target languages are reported
as coverage limitations rather than silently omitted.
The selected target10 has PPPL/raw-text coverage, but current downstream task
flags do not include those language-scripts.
```

Execution artifacts:

- model matrix: `docs/exp/v5/3_evaluation/model_matrix.tsv`
- metric wrapper: `scripts/run_v5_eval_metric.sh`
- metric fidelity matrix:
  `docs/exp/v5/4_reporting/00_tables/table_13_metric_fidelity_matrix.md`
- completion table:
  `docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv`
- measured baseline/reference outputs:
  `pppl/xlmr_base`, `pppl/glot500_base`,
  `retrieval_tatoeba/xlmr_base`, `retrieval_tatoeba/glot500_base`,
  `retrieval_bible/xlmr_base`, `retrieval_bible/glot500_base`,
  `text_classification/xlmr_base`, `text_classification/glot500_base`,
  `ner/xlmr_base`, `ner/glot500_base`, `pos/xlmr_base`, `pos/glot500_base`,
  `pos/v5_random`,
  `roundtrip_alignment/xlmr_base`, `roundtrip_alignment/glot500_base`

Current local coverage:

| Metric | Local data / 102 | Target local data / 10 |
| --- | ---: | ---: |
| PPPL | 102 | 10 |
| Tatoeba retrieval | 63 | 0 |
| Bible retrieval | 74 | 0 |
| Text classification | 1 | 0 |
| NER | 78 | 0 |
| POS | 58 | 0 |
| Roundtrip alignment | 74 | 0 |

Target10 interpretation:

```text
Target10 evidence should be tokenization + zero-step/after-MLM PPPL centered.
Downstream replay should be reported over available languages/head/all with
explicit exclusions.
```

## Slide 12. Current Measured Rows

Main message:

```text
The current measured rows include baseline/reference evidence plus v5-random
available-language metric rows; FVT and method claims remain gated.
```

Main table source:

```text
docs/exp/v5/3_evaluation/09_aggregation/
docs/exp/v5/4_reporting/current_result_snapshot.md
```

Measured baseline callouts:

- XLM-R PPPL: target `61.980216`, head `8.117338`, all `9.986271`.
- Glot500-base PPPL: target `15.102934`, head `10.213100`, all `10.640353`.
- v5-random PPPL: target `39.222875`, head `18.726452`, all `20.138927`;
  FVT PPPL is still checkpoint-gated.
- XLM-R Tatoeba Top-10: head `0.656309`, all available `0.566067`.
- Glot500-base Tatoeba Top-10: head `0.743755`, all available `0.706649`.
- v5-random Tatoeba Top-10: head `0.700285`, all available `0.610353`;
  FVT Tatoeba remains checkpoint-gated.
- XLM-R Bible Top-10: head/all available `0.381153` over `74/102` language-scripts.
- Glot500-base Bible Top-10: head/all available `0.509356` over `74/102` language-scripts.
- v5-random Bible Top-10: head/all available `0.328019` over `74/102`
  language-scripts; FVT Bible remains checkpoint-gated.
- XLM-R Taxi1500 macro-F1: head/all available `0.592876`.
- Glot500-base Taxi1500 macro-F1: head/all available `0.743338`.
- v5-random Taxi1500 macro-F1: head/all available `0.702956`;
  accuracy `0.747748`; FVT Taxi1500 remains checkpoint-gated.
- XLM-R NER F1: all available `0.549858`, head `0.621207`,
  v5-target actual intersection: 0.459364, `fur_Latn` only.
- Glot500-base NER F1: all available `0.627108`, head `0.645915`,
  v5-target actual intersection: 0.553191, `fur_Latn` only.
- v5-random NER F1: all available `0.544628`, head `0.608020`,
  v5-target actual intersection: 0.560554, `fur_Latn` only.
- XLM-R POS F1: all available `0.481336`, head `0.571446`;
  `TRAIN_LANGS=tur_Latn`.
- Glot500-base POS F1: all available `0.567542`, head `0.573832`;
  `TRAIN_LANGS=tur_Latn`.
- v5-random POS F1: all available `0.481102`, head `0.587430`;
  `TRAIN_LANGS=tur_Latn`; FVT POS remains checkpoint-gated.
- XLM-R Roundtrip accuracy: head/all available `0.185300` over `74/102`
  language-scripts.
- Glot500-base Roundtrip accuracy: head/all available `0.205189` over `74/102`
  language-scripts.
- v5-random Roundtrip accuracy: head/all available `0.190300` over `74/102`
  language-scripts; FVT Roundtrip remains checkpoint-gated.

Interim random-checkpoint interpretation:

- v5-random target10 PPPL improves over XLM-R but remains behind Glot500-base.
- v5-random downstream rows are mixed: helpful on some available-language
  metrics, weak on others.
- Therefore the slide claim is not "v5 wins"; it is "the matched FVT row is the
  decisive method test."

Promotion gate:

```text
Promote v5 method rows only after `metric_completion.tsv` marks the
corresponding metric/model rows as measured, or replace a row with an explicit
blocker note.
```

## Slide 13. Coverage And Limitations

Main message:

```text
Downstream coverage is part of the result.
```

Points:

- v5 target10 may not appear in every downstream dataset.
- Official Glot500 task lists include partial v5 target membership (`8/10`),
  mainly Bible plus one NER and one POS case.
- Current local downstream materialization undercounted tail tasks by treating
  the task-list head/tail flag as availability; target downstream claims stay
  pending until that repair is complete.
- Glot500-base is an external scale reference, not an equal-compute baseline.
- Full 511-language Glot500 reproduction is outside this controlled v5 scope.
- Main tokenizer improves 9/10 target languages, but `dzo_Tibt` remains a
  documented fertility regression.

Table source:

```text
docs/exp/v5/3_evaluation/00_coverage/
docs/exp/v5/4_reporting/00_tables/table_09_blocked_metric_notes.md
docs/exp/v5/4_reporting/00_tables/table_13_metric_fidelity_matrix.md
```

Figure:

```text
docs/exp/v5/4_reporting/01_figures/generated/figure_05_evaluation_coverage.png
```

## Slide 14. Conclusion

Current-safe conclusion:

```text
We have a controlled Glot500-style replay, not a full-scale Glot500 rerun:
102 language-scripts, full corpus merge, tokenizer append, initialization
audits, and retained metric families.

The current strongest result is intrinsic. FVT lowers v5-target zero-step NLL
from 18.411756 to 8.785518 versus random resize, with source-row, <mask>,
byte-row, and LM-head audits passed.

The final method claim waits for matched v5_random/v5_fvt MLM checkpoints and
available downstream metric rows.
```

Final-result replacement slots:

- reproduction result: main merge/tokenizer/audit passed with documented `dzo_Tibt` risk
- initialization result: main FVT improves target zero-step NLL over random and mean
- downstream transfer result: waiting for matched v5 checkpoints and parsed downstream outputs;
  patch only rows marked ready in `post_result_patch_plan_ko.md`

Speaker close:

```text
오늘 시점에서 확정적으로 말할 수 있는 것은 setup fidelity와 zero-step novelty입니다.
최종 FVT claim은 random/FVT가 같은 10K budget을 끝낸 뒤 PPPL과 downstream을
같은 wrapper로 돌렸을 때만 열겠습니다.
```

Replacement gate:

```text
Write the downstream conclusion only after `3_evaluation/09_aggregation/`
contains measured outputs or explicit blocker notes for every required metric,
and only update report/PPT slots listed as ready in
`4_reporting/post_result_patch_plan_ko.md`.
```

## Slide 15. Backup: Execution Artifacts

Commands:

```bash
bash preprocessing/run_v5_glot50010_merge.sh
bash tokenization/train_v5_glot50010.sh
bash scripts/run_v5_build_initializers.sh
bash modeling/launch_v5_random_fvt_10k.sh
python3 scripts/write_v5_eval_model_matrix.py
python3 scripts/write_v5_checkpoint_selection_manifest.py
bash scripts/run_v5_post_checkpoint_evals.sh status
SKIP_MEASURED=1 WITH_PLOTS=1 GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v5_post_checkpoint_evals.sh all
sed -n '1,120p' docs/exp/v5/4_reporting/post_result_patch_plan_ko.md
MAX_EXAMPLES_PER_LANGUAGE=100 MAX_LENGTH=128 MASK_BATCH_SIZE=64 \
  bash scripts/run_v5_eval_metric.sh pppl xlmr_base 0
MAX_EXAMPLES_PER_LANGUAGE=100 MAX_LENGTH=128 MASK_BATCH_SIZE=64 \
  bash scripts/run_v5_eval_metric.sh pppl glot500_base 0
python3 scripts/refresh_v5_reporting.py --with-plots
```

Artifact map:

- `docs/exp/v5/Plan.md`
- `docs/exp/v5/Report.md`
- `docs/exp/v5/README.md`
- `docs/exp/v5/goal_readiness.md`
- `docs/exp/v5/3_evaluation/metric_mapping.md`
- `docs/exp/v5/3_evaluation/execution_queue.md`
- `docs/exp/v5/3_evaluation/next_runbook.md`
- `docs/exp/v5/3_evaluation/post_checkpoint_eval_queue.md`
- `docs/exp/v5/3_evaluation/post_checkpoint_execution_plan.md`
- `/home/axt/mnt2/jongha/v5_glot50010/`
- `docs/exp/v5/4_reporting/00_tables/source_map.md`
- `docs/exp/v5/4_reporting/post_result_patch_plan_ko.md`
- `docs/exp/v5/4_reporting/objective_completion_audit.md`
- `docs/exp/v5/4_reporting/02_slides/talk_track.md`
- `docs/exp/v5/4_reporting/02_slides/presenter_script_ko.md`
- `docs/exp/v5/4_reporting/02_slides/defense_qa.md`
- `docs/exp/v5/4_reporting/02_slides/slide_claim_checklist.md`
- `docs/exp/v5/4_reporting/02_slides/slide_asset_manifest.md`
- `docs/exp/v5/4_reporting/03_final_report/paper_draft.md`
- `docs/exp/v5/4_reporting/03_final_report/claim_ledger.md`
