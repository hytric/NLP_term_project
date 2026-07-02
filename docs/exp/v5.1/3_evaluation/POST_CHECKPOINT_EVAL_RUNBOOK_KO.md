# v5.1 Checkpoint 이후 평가 Runbook

업데이트: 2026-06-28

## 한 줄 결론

```text
CHECKPOINT_READY = no
EVAL_DATA_READY = yes
NEXT_WHEN_READY = held-out PPPL -> downstream -> similarity -> aggregate -> report/PPT table refresh
```

현재 v5.1은 평가 데이터 준비가 끝났다. 이제 `v51_random`과 `v51_fvt`의
3K checkpoint가 모두 나오면 Glot500-style held-out PPPL과 downstream metric을
바로 실행하면 된다.

## 준비 완료된 평가 데이터

| Metric | total | head | target10 | 상태 |
| --- | ---: | ---: | ---: | --- |
| PPPL | 102 | 92 | 10 | strict held-out split index 준비 완료 |
| Tatoeba retrieval | 66 | 63 | 3 | 기존 materialized data 재사용 |
| Bible retrieval | 80 | 74 | 6 | v5.1 root에 materialized 완료 |
| Text classification | 1 | 1 | 0 | 기존 Taxi1500 재사용, target 없음 |
| NER | 84 | 78 | 6 | 기존 NER 재사용 |
| POS | 58 | 58 | 0 | 기존 POS 재사용, target 없음 |
| Roundtrip alignment | 80 | 74 | 6 | v5.1 root에 materialized 완료 |

## 생성/연결된 주요 경로

| 항목 | 경로 |
| --- | --- |
| eval data root | `/home/axt/mnt2/jongha/v5_1_glot50010/eval_data_download` |
| eval output root | `/home/axt/mnt2/jongha/v5_1_glot50010/evaluation` |
| model matrix | `docs/exp/v5.1/3_evaluation/model_matrix.tsv` |
| coverage summary | `docs/exp/v5.1/3_evaluation/00_coverage/coverage_summary.tsv` |
| Bible materialization | `docs/exp/v5.1/3_evaluation/03_retrieval_bible/materialization_summary.tsv` |
| Roundtrip materialization | `docs/exp/v5.1/3_evaluation/07_roundtrip_alignment/materialization_summary.tsv` |

## Checkpoint readiness 확인

```bash
bash scripts/run_v51_post_checkpoint_evals.sh status
```

학습 중 live dashboard를 먼저 최신화하려면:

```bash
bash scripts/refresh_v51_live_status.sh
```

이 wrapper는 trainer log/GPU snapshot, model matrix, checkpoint readiness
status를 함께 갱신한다. 필요하면 내부 명령을 분리해서 실행할 수 있다.

```bash
python3 scripts/write_v51_training_status.py
python3 scripts/sync_v51_live_status_docs.py
python3 scripts/write_v51_eval_model_matrix.py --v51-root /home/axt/mnt2/jongha/v5_1_glot50010 --out-dir docs/exp/v5.1/3_evaluation
bash scripts/run_v51_post_checkpoint_evals.sh status > docs/exp/v5.1/3_evaluation/latest_model_status.txt
```

통과 조건:

```text
v51_random ready_for_wrapper = yes
v51_fvt ready_for_wrapper = yes
```

현재는 random 학습 중이고 FVT는 random 완료 후 자동 시작될 예정이므로 아직
`ready_for_wrapper=no`가 정상이다.

장시간 대기/자동 handoff가 필요하면 아래 watcher를 쓴다. 기본값은 감시만 하고
실행하지 않는다.

```bash
bash scripts/watch_v51_mlm_handoff.sh
```

watcher는 각 poll에서 `scripts/refresh_v51_live_status.sh`를 호출하므로,
dashboard, training table, figure, metric completion table도 함께 최신화된다.

checkpoint pair가 준비되는 즉시 PPPL/downstream/similarity까지 자동 실행하려면
명시적으로 flag를 켠다.

```bash
RUN_PPPL=1 RUN_DOWNSTREAM=1 RUN_BASELINE_PPPL=1 RUN_SIMILARITY=1 \
GPU_RANDOM=0 GPU_FVT=1 GPU_BASELINE=0 GPU_SIMILARITY=0 \
bash scripts/watch_v51_mlm_handoff.sh
```

짧게 한 번만 readiness를 확인할 때:

```bash
MAX_POLLS=1 POLL_SECONDS=1 bash scripts/watch_v51_mlm_handoff.sh
```

최근 smoke test:

```text
time = 2026-06-28 20:16 KST
command = MAX_POLLS=1 POLL_SECONDS=1 bash scripts/watch_v51_mlm_handoff.sh
result = exit 2 as expected because matched checkpoints are not ready
v51_random = dir_exists_no_model_file, ready=no
v51_fvt = missing, ready=no
log = docs/exp/v5.1/2_training/watch_logs/watch_v51_mlm_handoff_20260628_201638.log
```

## 실행 순서

1. held-out PPPL

```bash
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test \
GPU_RANDOM=0 GPU_FVT=1 \
bash scripts/run_v51_post_checkpoint_evals.sh pppl
```

2. downstream metrics

```bash
GPU_RANDOM=0 GPU_FVT=1 \
bash scripts/run_v51_post_checkpoint_evals.sh downstream
```

3. XLM-R / Glot500 baseline PPPL

```bash
GPU_BASELINE=0 \
bash scripts/run_v51_post_checkpoint_evals.sh baseline_pppl
```

이 단계는 `v51_random/v51_fvt` checkpoint pair를 기다리지 않아도 된다. GPU2가
비어 있으면 아래처럼 선행 실행해 final table의 XLM-R/Glot500 PPPL column을
미리 채울 수 있다.

```bash
GPU_BASELINE=2 PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test \
PPPL_MAX_EXAMPLES_PER_LANGUAGE=100 PPPL_MAX_LENGTH=128 PPPL_MASK_BATCH_SIZE=64 \
bash scripts/run_v51_post_checkpoint_evals.sh baseline_pppl
```

4. aggregation

```bash
bash scripts/run_v51_post_checkpoint_evals.sh aggregate
```

`aggregate`는 `09_aggregation/*.tsv`를 갱신한 뒤 report/PPT용 generated table
`4_reporting/00_tables/table_03_main_metric_results.md`와
`table_06_metric_completion.md`도 함께 갱신한다.

5. similarity / 2D map

```bash
GPU=0 MODEL_KEYS=v51_random,v51_fvt bash scripts/run_v51_similarity.sh
```

현재 `similarity_pairs.tsv` 입력은 이미 생성되어 있다.

similarity runner가 완료되면
`4_reporting/00_tables/table_04_similarity_results.md`도 자동으로 갱신된다.

```text
docs/exp/v5.1/3_evaluation/08_embedding_similarity/similarity_pairs.tsv
total_pairs = 22,600
```

## 보고서 표에 넣을 때 규칙

- `head`는 XLM-R 학습에 사용된 92개 언어 중 해당 metric data가 있는 subset이다.
- `tail` 또는 `target10`은 이번에 고른 10개 XLM-R-unseen 언어 중 해당 metric data가 있는 subset이다.
- `all`은 head와 target10을 합친 v5.1 102개 언어 universe에서 해당 metric data가 있는 subset이다.
- PPPL은 반드시 held-out `test` split 결과만 final metric으로 쓴다.
- 기존 v5 train-source PPPL은 final table이 아니라 diagnostic/fallback으로만 쓴다.
- similarity 결과는 qualitative/diagnostic evidence이며, Glot500 7개 metric을 대체하지 않는다.
