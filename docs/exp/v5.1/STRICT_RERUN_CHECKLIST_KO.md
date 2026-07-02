# v5.1 Strict Rerun 체크리스트

작성 시각: 2026-06-28 21:56 KST

이 문서는 새 strict V5 rerun의 진행상황을 계속 업데이트하기 위한 단일 체크리스트다.
목표는 v5의 실수들을 반영해 Glot500 평가 방식을 더 충실히 재연하되, 전체 corpus를
무작정 다 쓰지 않고 사전에 정한 비율과 GPU budget 안에서 끝까지 완주하는 것이다.

## 현재 결론

```text
RUN_DECISION=mlm_3k_pair_running
RECOMMENDED_DATA_FRACTION=5%
RECOMMENDED_SCALE=1.5
STRICT_SPLIT_POLICY=dev/test holdout before merge/tokenizer/MLM
PPPL_POLICY=held-out test only for final PPPL
GPU_POLICY=use up to 4x A6000, effective batch 384
EVAL_DATA_READY=yes
```

## 핵심 체크리스트

### 0. 기존 v5 실수 반영

- [x] target10을 downstream coverage 고려 없이 고르면 downstream target claim이 막힌다는 점 확인.
- [x] raw `train` split PPPL은 Glot500 held-out test PPPL이 아니라 diagnostic임을 확인.
- [x] v5 PPPL train-source diagnostic과 v5.1 held-out PPPL을 분리.
- [x] PPPL 실행 가드 추가: `PPPL_SPLIT=train`은 명시 플래그 없이는 실행 거부.

### 1. 언어 선택

- [x] downstream-aware target10 선정.
- [x] target10 모두 `XLM-R != True`, `new_length >= 30000`, raw directory 존재 조건 확인.
- [x] target10 downstream coverage 요약 작성.
- [x] POS/Taxi1500 target coverage 부족을 report limitation에 반영.

Selected target10:

```text
guj_Gujr, asm_Beng, srp_Cyrl, sun_Latn, zsm_Latn,
aze_Latn, fil_Latn, bos_Latn, dzo_Tibt, sat_Olck
```

### 2. Dev/Test Split

- [x] stats 기반 planning split manifest 생성.
- [x] dev/test 각 `1000` 계획.
- [x] split index JSONL 생성.
- [x] 언어별 train/dev/test + XLM-R + downstream overlap 표 생성.
- [x] Arrow row-count 기반 verification 실행.
- [x] stats count와 actual Arrow count mismatch 예외 표 작성.
- [x] verified split indices로 5% dry-run 재실행.
- [x] 실제 train-only merge에서 dev/test index 제외 확인.

Artifacts:

```text
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_manifest.tsv
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_indices.jsonl
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_data_composition_by_language.md
docs/exp/v5.1/0_tokenizer/00_data_scope/strict_split_verification_summary.md
```

### 3. 데이터 사용 비율

- [x] full v5.1 dry-run size 계산: `162,608,099` lines.
- [x] fraction table 작성.
- [x] first strict rerun 권장값: `5%`, `SCALE=1.5`, 약 `8.13M` lines.
- [x] `5%` merge dry-run 실행.
- [x] `5%` merge 실제 실행.
- [ ] 시간이 남으면 `10%`, `SCALE=3.0` rerun 여부 결정.

기준 문서:

```text
docs/exp/v5.1/RUNTIME_AND_DATA_FRACTION_PLAN_KO.md
```

### 4. GPU / Batch

- [x] 4-GPU plan 작성.
- [x] effective batch `384` 유지 설정 작성.
- [x] 학습 직전 `nvidia-smi`로 실제 가용 GPU 확인.
- [x] GPU2는 기존 v5 downstream이 사용 중이라 GPU `0,1,3` 3장으로 launch.
- [x] 3-GPU fallback에서도 effective batch `384` 유지.
- [x] live trainer command/log/GPU snapshot 기준 optimizer, LR, batch, seq length 확인.
- [ ] OOM 시 fallback batch 적용.

권장:

```text
PER_DEVICE_TRAIN_BATCH_SIZE=8
GRADIENT_ACCUMULATION_STEPS=16  # 3-GPU fallback
effective batch = 384
status doc = docs/exp/v5.1/2_training/training_status.md
```

### 5. Tokenizer / Initialization

- [x] strict 5% train-only corpus 생성.
- [x] tokenizer train 완료.
- [x] tokenizer audit failure `0`.
- [x] random/FVT initialized checkpoints 생성.
- [x] `<mask>` remap diff `0.0`.
- [x] LM-head tied 확인.

### 6. MLM Training

- [ ] `v51_random` strict checkpoint 학습: running, 1869/3000 at 21:56 KST.
- [ ] `v51_fvt` strict checkpoint 학습.
- [x] 두 checkpoint가 같은 corpus, tokenizer, seed, step, batch, schedule로 launch되도록 wrapper 설정.
- [x] 현재 live setting 확인: `AdamW`, initial LR `5e-5`, effective batch `384`, seq length `512`.
- [x] latest training loss 확인: `4.0544` at step 1800, LR `2.01e-05`.
- [x] checkpoint 상태 확인: 아직 model file 없음, evaluation은 checkpoint-3000 대기.
- [x] v5.1 handoff watcher smoke test: checkpoint pair 미준비로 정상 종료 `exit 2`.
- [ ] 3K checkpoint 결과 먼저 확보.
- [ ] 시간이 남으면 10K checkpoint로 확장.

### 7. Evaluation

- [x] v5.1 coverage table 작성.
- [x] raw/downstream train-dev-test dataset size audit 작성.
- [x] Bible retrieval target subset materialization.
- [x] Roundtrip alignment target subset materialization.
- [x] post-checkpoint evaluation wrapper 준비.
- [ ] Held-out PPPL: `PPPL_SPLIT=test`, `PPPL_EVAL_ROLE=heldout_test`.
- [ ] Tatoeba retrieval Top-10.
- [ ] Bible retrieval Top-10.
- [ ] Taxi1500 classification F1.
- [ ] NER F1.
- [ ] POS F1.
- [ ] Roundtrip alignment accuracy.
- [x] 각 metric에 coverage table 작성.
- [ ] head/tail/all 정확히 분리.
- [ ] target-subset table 별도 작성.

### 8. Similarity / 2D Map

- [x] similarity pair input 생성.
- [x] 같은 언어끼리 sentence embedding cosine similarity 실행 스크립트 준비.
- [x] 같은 meaning의 cross-lingual pair similarity 실행 스크립트 준비.
- [x] roundtrip pair similarity 실행 스크립트 준비.
- [ ] layer 8 mean pooling 기준 table 작성.
- [ ] UMAP/t-SNE 2D point map 생성.
- [ ] plot에 head/target/task coverage label 표시.

필수 산출물:

```text
docs/exp/v5.1/3_evaluation/08_embedding_similarity/
docs/exp/v5.1/4_reporting/01_figures/
```

현재 input:

```text
similarity_pairs.tsv = 22,600 pairs
runner = scripts/run_v51_similarity.sh
```

### 9. Report / PPT

- [ ] 데이터 구성 table.
- [ ] split policy table.
- [ ] tokenizer audit table.
- [ ] initialization table.
- [ ] training plot.
- [ ] Glot500-style metric table.
- [ ] similarity table + 2D map.
- [ ] claim ledger.
- [ ] limitations.
- [ ] PPT final deck.
- [ ] paper-style final report.

## 바로 다음 실행 Gate

학습은 이미 시작했다. 현재 다음 gate는 random/FVT 3K checkpoint 완료와
post-checkpoint evaluation 실행이다.

```text
GATE_1_DATA_FRACTION_DECIDED = 5% or 10%
GATE_2_STRICT_SPLIT_VERIFIED = passed; Arrow verification status PASS
GATE_3_GPU_PLAN_CONFIRMED = passed; GPU 0,1,3 fallback
GATE_4_5PCT_MERGE_PASS = passed, actual lines 8,130,401
GATE_5_MLM_3K_PAIR = running
GATE_6_EVAL_DATA_READY = passed
```

권장 다음 명령:

```bash
bash scripts/refresh_v51_live_status.sh
bash scripts/run_v51_post_checkpoint_evals.sh status
PPPL_SPLIT=test PPPL_EVAL_ROLE=heldout_test GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh pppl
GPU_RANDOM=0 GPU_FVT=1 bash scripts/run_v51_post_checkpoint_evals.sh downstream
```
