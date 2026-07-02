# Third Try Execution Rules

작성일: 2026-06-12

이 파일은 `third_try` 실행 규칙이다. `plan.md`는 과학적 설계이고, `scope_lock_20260612.md`는 사용자 확인으로 고정된 실제 수행 범위다.

## Sequential Execution

- Main pipeline은 `00_scope`부터 `07_main_claim`까지 순서대로 진행한다.
- `08_ablation`은 기존 결과 정리 작업이므로 00 이후 병렬로 초안 작성할 수 있지만, final wording은 07 결과 이후 닫는다.
- `09_extension_case`는 target10 main protocol이 07에서 닫힌 뒤에만 시작한다.
- 각 stage는 `results.md`, `score_table.tsv`, `file_results.tsv`가 있어야 완료된다.
- stage 결과가 `PASS`, `PASS_NEGATIVE_RESULT`, `PASS_DEVIATION_DOCUMENTED` 중 하나로 닫히지 않으면 다음 stage로 넘어가지 않는다.

## Required File Contract

각 stage 폴더는 아래 파일을 가진다.

| File | Required When | Purpose |
| --- | --- | --- |
| `plan.md` | before execution | 목표, 입력, 작업, 산출물, exit 기준 |
| `results.md` | after execution | 실제 결과, gate status, failure return |
| `score_table.tsv` | after execution | 수치/판정 기준을 빈칸 없이 기록 |
| `file_results.tsv` | after execution | 생성 artifact 목록과 검증 상태 |

`score_table.tsv`에는 빈칸, `TBD`, `NA_NOT_CHECKED`를 남기지 않는다. 모르는 값은 `BLOCKED_REASON_RECORDED`처럼 이유가 있는 상태값으로 닫는다.

## Iteration Rule

반복 실행은 반드시 새 run id를 가진다.

Run id 형식:

```text
stage{NN}_{short_name}_YYYYMMDD_r{N}
```

예:

```text
stage03_tokenizer_20260612_r1
stage03_tokenizer_20260612_r2
```

각 반복 후 `iteration_log.md`에 아래를 남긴다.

- run id
- stage
- 변경한 변수
- 산출물 위치
- gate status
- 실패 또는 통과 근거
- 다음 행동

## Branch Exploration Rule

Main rule로 해결할 수 없는 실패 원인이 생기면 branch를 만든다.

Branch 위치:

- 문서: `docs/exp/third_try/branches/{branch_id}/`
- 대용량 파일: `/home/axt/mnt2/jongha/third_try/branches/{branch_id}/`

Branch는 아래 파일을 가진다.

- `goal.md`
- `plan.md`
- `results.md`
- `score_table.tsv`
- `return_decision.md`

Branch 종료 상태:

| Status | Meaning |
| --- | --- |
| `MERGE_TO_MAIN` | main rule 또는 stage 결과에 반영 |
| `RETRY_BRANCH` | 같은 branch를 조건 수정 후 반복 |
| `ABANDON_BRANCH` | evidence로만 보관하고 main claim에는 사용하지 않음 |

## Main And Ablation Boundary

Main으로 인정되는 조건:

- XLM-R-base에서 시작한다.
- target10 전체를 low-resource target으로 둔다.
- Coptic/Syriac를 main target에 포함한다.
- high-resource replay/control data와 low-resource target data를 동시에 사용한다.
- XLM-R 기존 vocab id와 special token id를 보존한다.
- 새 token은 append만 한다.
- 여러 embedding initialization method를 비교하고, random init은 required baseline으로 포함한다.
- model-dependent 비교는 3개 이상 seed를 사용한다.
- full-model MLM continued pretraining을 수행한다.
- target10 downstream 개선을 평가한다.

Ablation으로만 인정되는 조건:

- high-resource replay 없이 target-only로 학습한 run
- seed 1개짜리 pilot
- 8k/16k/32k smaller vocab grid
- byte fallback vs character fallback/coverage
- LoRA
- new-row-only or staged repair
- Bible-only proxy downstream
- translation/NMT proxy
- `xlm-roberta-large` 비교
- target10 밖 언어 확장

## Deviation Rule

Glot500 설정에서 벗어난 부분은 반드시 deviation으로 기록한다.

필수 deviation 항목:

- Glot500 원 논문과 다른 vocab size를 쓰는 경우
- batch/sequence length/step budget이 다른 경우
- target10 downstream dataset이 proxy 성격인 경우
- high-resource replay language list가 줄어드는 경우
- seed 3개 이상을 못 채운 경우

Deviation은 실패가 아니다. 단, 기록되지 않은 deviation은 gate fail이다.

## Artifact Storage

Git/workspace에는 문서와 작은 TSV/JSON/Markdown만 둔다.

대용량 artifact root:

```text
/home/axt/mnt2/jongha/third_try
```

권장 하위 폴더:

- `checkpoints/`
- `tokenizers/`
- `models/`
- `manifests/`
- `logs/`
- `eval_outputs/`
- `branches/`

각 `results.md`에는 대용량 artifact path와 재현 command를 기록한다.

## Compute Rule

- main run은 full fine-tuning이 기본이다.
- 이 프로젝트의 GPU 실행은 사용자 지시에 따라 GPU 3번만 사용한다. 모든 GPU command는 `CUDA_VISIBLE_DEVICES=3`을 붙인다.
- compute 부족으로 축소하면 `deviation_from_glot500.tsv`에 명시한다.
- 축소 run은 positive final claim보다 feasibility/diagnostic evidence로 먼저 해석한다.
- checkpoint selection은 dev 또는 allowed validation metric만 사용한다.
- final test를 selection에 사용하면 해당 run은 invalid로 표시한다.

## Exit Goal

최종 목표는 positive claim을 강제로 만드는 것이 아니다. 목표는 다음 중 하나를 정직하게 완결하는 것이다.

1. target10 downstream 개선과 high-resource replay/control 안정성을 함께 보인다.
2. 개선이 없으면 어떤 설계 또는 데이터 조건에서 막혔는지 diagnostic claim으로 정리한다.
3. 기존 first/second try 결과를 ablation/failure analysis로 재배치한다.
4. target10 밖 extension case는 main protocol transfer로만 해석한다.
