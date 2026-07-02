# Second Try Execution Rules

작성일: 2026-06-10

이 파일은 second_try 실험 실행 규칙이다. 모든 step은 이 규칙을 따른다.

## Sequential Execution

- Step은 `step_index.md`의 순서대로만 수행한다.
- 다음 step으로 이동하려면 현재 step의 `results.md`에 `Gate status: PASS`가 있어야 한다.
- 예외: `08_final_analysis`는 `07_translation_benchmark`가 실패하더라도 branch evidence와 Failure Return이 완성되어 있으면 `Gate status: PASS_NEGATIVE_RESULT`로 negative synthesis를 작성할 수 있다.
- `score_table.tsv`에는 빈칸, `TBD`, `NA_NOT_CHECKED`가 남아 있으면 안 된다.
- 각 step은 반드시 `results.md`, `score_table.tsv`, `file_results.tsv`, step-specific artifact를 출력한다.
- `file_results.tsv`에는 생성된 각 파일의 path, row/count 또는 size, checksum 가능 여부, status를 기록한다.
- 목표 수치에 도달하면 다음 step으로 이동한다.
- 목표 수치에 도달하지 못하면 해당 step의 `Failure Return` 규칙에 따라 이전 step으로 돌아간다.

## Branch Exploration Rule

기존 가이드라인으로 실패 원인을 해결할 수 없으면 branch 탐구를 만든다.

Branch 위치:

- 문서: `docs/exp/second_try/branches/{branch_id}/`
- 대용량 파일: `/home/axt/mnt2/jongha/second_try/branches/{branch_id}/`

Branch는 반드시 아래 파일을 가진다.

- `goal.md`: branch 목표와 실패 원인
- `plan.md`: 새 시도 방법
- `results.md`: 실험 결과
- `score_table.tsv`: 목표 수치와 실제 수치
- `return_decision.md`: main step으로 복귀할지, branch를 폐기할지, main rule을 수정할지 결정

Branch 탈출 기준:

- `score_table.tsv`에 빈칸/TBD가 없어야 한다.
- `return_decision.md`에 `MERGE_TO_MAIN`, `RETRY_BRANCH`, `ABANDON_BRANCH` 중 하나가 있어야 한다.
- `MERGE_TO_MAIN`이면 main step의 `results.md`에 branch evidence를 링크한다.

## GPU Policy

User preference:

- GPU 4를 우선 사용한다.
- GPU 4 실행이 안 되면 예외적으로 GPU 3을 사용한다.

Current environment check:

- 현재 `nvidia-smi`에는 GPU index `0,1,2,3`만 보인다.
- GPU 4가 보이지 않으므로 실제 실행은 GPU 3 fallback을 사용한다.

Execution convention:

- 기본 command prefix: `CUDA_VISIBLE_DEVICES=3`
- GPU 4가 보이는 환경으로 바뀌면 command prefix를 `CUDA_VISIBLE_DEVICES=4`로 바꾼다.
- CPU-only step은 GPU를 사용하지 않는다.

## Large Artifact Storage

Git/workspace에는 문서와 작은 TSV/Markdown만 둔다.

대용량 파일은 아래에 저장한다.

- root: `/home/axt/mnt2/jongha/second_try`
- checkpoints: `/home/axt/mnt2/jongha/second_try/checkpoints`
- manifests: `/home/axt/mnt2/jongha/second_try/manifests`
- tokenizer/model artifacts: `/home/axt/mnt2/jongha/second_try/artifacts`
- logs: `/home/axt/mnt2/jongha/second_try/logs`
- branch artifacts: `/home/axt/mnt2/jongha/second_try/branches`

각 docs result 파일에는 대용량 artifact path를 반드시 기록한다.

## Final Objective

최종 목표는 두 갈래다.

1. 10개 low-resource target dataset에서 tokenizer bottleneck을 줄이고 downstream task에 잘 적응하는 높은 score를 보인다.
2. 추가 translation benchmark에서 high-resource reference score의 80% 이상을 달성한다.

## Translation Rule

Translation은 기존 encoder-only downstream 이후 별도 step에서 수행한다.

- Downstream step이 `PASS` 또는 `PASS_NEGATIVE_RESULT`로 정리된 뒤 translation benchmark를 시작한다.
- Translation은 high-resource reference score를 먼저 정의하고, target translation score가 그 80% 이상인지 확인한다.
- 80%에 못 미치면 `07_translation_benchmark`의 Failure Return을 따른다.
- 기존 guideline으로 해결이 안 되면 branch exploration rule을 사용한다.
- Step 08에서 최종 정리를 해야 한다면 translation 성공 claim은 downgrade하고, 복귀 branch와 재실행 기준을 명시한다.
