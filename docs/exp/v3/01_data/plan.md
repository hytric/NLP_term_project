# Stage 01 Plan: Data Collection And Split

## Goal

Stage 00에서 고정한 target10 low-resource corpus와 high-resource replay/control corpus를 수집하고 split을 만든다. train/dev/test leakage를 막고, high-resource와 low-resource가 동시에 training mixture에 들어가게 하는 것이 최우선이다.

현재 상태: 진행 중. GlotCC-V1 high-resource web replay sample은 2026-06-13에 materialized 완료했고, 다음 작업은 target10 V2 split과 결합한 MLM mixture manifest 생성이다.

## Inputs

- `../00_scope/high_resource_inventory.tsv`
- `../00_scope/current_dataset_inventory.md`
- `high_resource_web_corpus_plan.md`
- `../plan.md`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_final_test_act_clean.txt`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_eng-Latn.jsonl`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_deu-Latn.jsonl`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_jpn-Jpan.jsonl`
- `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_kor-Hang.jsonl`

## Required Work

1. Target10 corpus의 source, license, sentence count, script, preprocessing 상태를 기록한다.
2. High-resource replay/control corpus의 source, license, sentence count를 기록한다.
3. Target10에서 leakage-safe dev/test/final test reserve 가능 여부를 확인한다.
4. Bible parallel verse가 있으면 dev/test/final test book 또는 verse split을 고정한다.
5. Train split에서 dev/test/final test 문장을 제거한다.
6. High-resource와 low-resource가 동시에 들어가는 MLM train/dev manifest를 만든다.
7. Split 생성 command와 random seed를 기록한다.

## Materialized High-Resource Input

| Config | Source | Lines | Docs | Role |
| --- | --- | ---: | ---: | --- |
| `eng-Latn` | GlotCC-V1 | 200000 | 11274 | true high-resource web replay |
| `deu-Latn` | GlotCC-V1 | 200000 | 9573 | true high-resource web replay |
| `jpn-Jpan` | GlotCC-V1 | 200000 | 20555 | true high-resource web replay |
| `kor-Hang` | GlotCC-V1 | 200000 | 14732 | true high-resource web replay |

Bible English/German/Japanese/Korean은 true high-resource web replay가 아니라 domain-matched replay/control로만 표시한다.

## Immediate Plan

1. `corpus_manifest.tsv`에 target10 V2, GlotCC web, Bible control source를 모두 등록한다.
2. `high_resource_manifest.tsv`에 GlotCC web sample과 Bible control을 role 분리해서 기록한다.
3. `mlm_mixture_manifest.tsv`를 만든다.
4. `leakage_audit.tsv`에서 target10 train/dev/final-test overlap을 확인한다.
5. `results.md`, `score_table.tsv`, `file_results.tsv`로 Stage 01 gate를 닫는다.

## Required Outputs

- `results.md`
- `score_table.tsv`
- `file_results.tsv`
- `corpus_manifest.tsv`
- `split_manifest.tsv`
- `bible_parallel_manifest.tsv`
- `high_resource_manifest.tsv`
- `mlm_mixture_manifest.tsv`
- `source_license_manifest.tsv`
- `leakage_audit.tsv`

## Score Table Contract

`score_table.tsv`는 아래 항목을 포함한다.

| Metric | Expected |
| --- | --- |
| train/dev/test overlap | 0 |
| missing source/license rows | 0 |
| language rows with split count missing | 0 |
| high-resource rows present | yes |
| low-resource rows present | yes |
| mixture manifest present | yes |

## Exit Criteria

- target10 language별 train/dev/test 수가 명확하다.
- high-resource replay/control corpus가 manifest에 있다.
- MLM mixture manifest에 high-resource와 low-resource가 모두 있다.
- split overlap audit이 통과한다.
- corpus source와 license가 누락 없이 기록되어 있다.
- `results.md`에 `Gate status: PASS`가 있다.

## Failure Return

Leakage가 있으면 Stage 01에서 split을 다시 만든다. High-resource와 low-resource가 동시에 들어가지 않으면 mixture manifest를 다시 만든다. 특정 target10 language의 downstream data가 부족하면 `00_scope/task_availability.tsv`와 Stage 06 results에 unavailable reason을 기록한다.
