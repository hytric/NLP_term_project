# v5.1 실험 종료 결과 요약

작성 시각: 2026-06-28 21:46 KST

## 한 줄 결론

```text
EXPERIMENT_STATUS = stopped_before_final_checkpoint
FINAL_STRICT_CHECKPOINT = no
FINAL_GLOT500_STYLE_METRICS = no
USABLE_OUTPUT = strict data/tokenizer/initializer/reporting scaffold + partial random MLM trace
```

v5.1은 v5의 핵심 문제였던 train-source PPPL을 보완하기 위해 만든 strict
correction line이다. 데이터 split, 5% train-only corpus, tokenizer 확장,
Random/FVT initializer, evaluation/reporting scaffold까지는 준비되었다. 그러나
실험 종료 시점에 `v51_random` MLM이 `1869/3000` step에서 중단되었고,
`checkpoint-3000` 또는 final model file이 생성되지 않았다. 따라서 held-out PPPL,
downstream task, similarity 결과는 final metric으로 보고할 수 없다.

## 종료 시점 실행 상태

| 항목 | 값 |
| --- | --- |
| 종료 확인 시각 | `2026-06-28 21:46 KST` |
| active v5.1 process | none |
| GPU 상태 | v5.1 training/eval 점유 없음 |
| active run | `v51_strict5pct_random_mlm_3k` |
| run status | `not_running` |
| last observed step | `1869/3000` |
| progress | `62.30%` |
| last logged loss row | step 1800, loss `4.0544`, LR `2.01e-05` |
| final checkpoint | not available |
| FVT run | not started |
| baseline PPPL prelaunch | attempted, no output produced |

근거:

```text
docs/exp/v5.1/2_training/training_status.md
docs/exp/v5.1/2_training/loss_history.tsv
docs/exp/v5.1/3_evaluation/model_matrix.tsv
docs/exp/v5.1/4_reporting/00_tables/table_06_metric_completion.md
```

## 완료된 산출물

| 영역 | 상태 | 주요 근거 |
| --- | --- | --- |
| target10 재선정 | done | `0_tokenizer/miscellaneous/glot50010_selected_manifest.tsv` |
| strict train/dev/test split | done | `0_tokenizer/00_data_scope/strict_split_manifest.tsv` |
| split verification | PASS | `0_tokenizer/00_data_scope/strict_split_verification_summary.md` |
| 5% train-only merge | done | `/home/axt/mnt2/jongha/v5_1_glot50010/data/Glot500_v51_glot50010_xlmr100_strict_5pct.txt` |
| tokenizer expansion | done | `/home/axt/mnt2/jongha/v5_1_glot50010/tokenization/output_strict_5pct/Glot500_extended_spm` |
| tokenizer audit | done | `0_tokenizer/03_audit/strict_5pct/results.md` |
| Random/FVT initializer | done | `/home/axt/mnt2/jongha/v5_1_glot50010/initialized_models_strict_5pct` |
| eval data coverage audit | done | `3_evaluation/00_coverage/coverage_summary.tsv` |
| Bible/Roundtrip materialization | done | `3_evaluation/03_retrieval_bible/`, `3_evaluation/07_roundtrip_alignment/` |
| similarity pair input | done | `3_evaluation/08_embedding_similarity/similarity_pairs.tsv` |
| report/PPT scaffold | done | `4_reporting/03_final_report/paper_draft_ko.md`, `4_reporting/02_slides/ppt_content_ko.md` |
| generated reporting tables | done, pending metrics | `4_reporting/00_tables/` |
| training curve figure | done, partial trace | `4_reporting/01_figures/training_loss_lr.svg` |

## 데이터 및 평가 coverage

| Metric | Total | Head | Target10 | 종료 시 결과 |
| --- | ---: | ---: | ---: | --- |
| PPPL raw text | 102 | 92 | 10 | data ready, metric not measured |
| Tatoeba retrieval | 66 | 63 | 3 | data ready, metric not measured |
| Bible retrieval | 80 | 74 | 6 | data ready, metric not measured |
| Taxi1500 classification | 1 | 1 | 0 | data ready, metric not measured |
| NER | 84 | 78 | 6 | data ready, metric not measured |
| POS | 58 | 58 | 0 | data ready, metric not measured |
| Roundtrip alignment | 80 | 74 | 6 | data ready, metric not measured |

## Training trace

`v51_random`은 3-GPU setup으로 시작되었고, 설정은 의도한 값과 일치했다.

| Setting | Value |
| --- | --- |
| optimizer | AdamW |
| initial LR | `5e-5` |
| effective batch | `384` |
| per-device batch | `8` |
| gradient accumulation | `16` |
| sequence length | `512` |
| max steps | `3000` |
| GPUs | physical GPU `0,1,3` |
| precision | fp16 |

Observed loss:

| Step | Loss | LR | Epoch |
| ---: | ---: | ---: | ---: |
| 100 | 6.6875 | 4.8433333e-05 | 0.06 |
| 500 | 4.4613 | 4.1766667e-05 | 0.32 |
| 1000 | 4.2816 | 3.3433333e-05 | 0.64 |
| 1500 | 4.1401 | 2.51e-05 | 0.96 |
| 1800 | 4.0544 | 2.01e-05 | 1.15 |

이 trace는 optimization diagnostic으로만 사용할 수 있다. final method claim은
held-out PPPL과 downstream metric이 필요하지만, 이번 종료 시점에는 해당 metric이
생성되지 않았다.

## 생성되지 않은 결과

| 결과 | 상태 | 이유 |
| --- | --- | --- |
| `v51_random` final checkpoint | not available | run stopped at `1869/3000` |
| `v51_fvt` checkpoint | not available | FVT run not started |
| held-out PPPL | not measured | required model paths not ready |
| Tatoeba/Bible retrieval | not measured | required model paths not ready |
| Taxi1500/NER/POS | not measured | required model paths not ready |
| Roundtrip alignment | not measured | required model paths not ready |
| embedding similarity scores/map | not measured | required model paths not ready |

Metric completion table:

```text
docs/exp/v5.1/4_reporting/00_tables/table_06_metric_completion.md
```

현재 모든 Glot500 metric은 `blocked_model`이다.

## 보고서/PPT에서 가능한 주장

가능:

- v5.1은 Glot500-style split discipline을 회복한 strict rerun 설계다.
- 92 XLM-R-seen + target10 언어 범위, held-out dev/test split, 5% train-only corpus,
  tokenizer expansion, Random/FVT initializer, evaluation scaffold가 재현 가능하게
  문서화되었다.
- target10은 downstream coverage를 고려해 재선정되었고, PPPL/Tatoeba/Bible/NER/Roundtrip
  target-side evaluation 경로가 준비되었다.
- Random run의 partial MLM trace에서는 training loss가 `6.6875`에서 `4.0544`까지 감소했다.

불가:

- FVT가 Random보다 좋다는 novelty 성능 claim.
- held-out PPPL 개선 claim.
- downstream task 개선 claim.
- similarity/2D map 기반 representation 개선 claim.
- Glot500 final metric 재연 완료 claim.

## 발표용 정리 문장

> v5.1은 Glot500 방식의 핵심인 held-out split과 train-only pretraining 원칙을
> 회복한 strict rerun으로 설계되었다. 데이터, tokenizer, initializer, evaluation
> wrapper, report/PPT table은 준비되었지만, 실험 종료 시점에 Random run이
> 1869/3000 step에서 중단되어 final checkpoint와 held-out/downstream metric은
> 생성되지 않았다. 따라서 이번 결과는 성능 claim이 아니라 재현 가능한 실험
> 설계와 partial optimization trace로 보고한다.

## 다음에 재개할 경우

1. `v51_random`을 checkpoint까지 resume하거나 3K를 다시 완료한다.
2. `v51_fvt`를 같은 조건으로 완료한다.
3. `PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test`로 PPPL을 실행한다.
4. downstream task와 similarity runner를 실행한다.
5. `bash scripts/refresh_v51_live_status.sh`로 report/PPT tables를 갱신한다.
