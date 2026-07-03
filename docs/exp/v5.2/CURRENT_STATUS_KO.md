# v5.2 현재 상태

업데이트: 2026-06-28 KST

## 한 줄 결론

```text
V5_2_CREATED = yes
MAIN_EXPERIMENT = v5.2_glot5007
CORPUS = 92 XLM-R-seen + 7 XLM-R-unseen target
MAIN_CLAIM = Glot500-style vocab injection with embedding initialization ablation
TARGET_SCOPE = XLM-R-unseen tail + downstream 가능한 최소 corpus band
YAMAGUCHI_ROLE = additional experiment / appendix
READY_STATE = target7 prepared, heavy merge/tokenizer/MLM pending
```

v5.2는 새 학습 run이다. 기존 v5/v5.1 논의에서 얻은 교훈을 반영해, target을
downstream coverage가 가능한 최소 tail band 7개로 압축하고 Glot500 논문식 pipeline을
다시 수행한다.

## 확정 Target7

| language_script | role |
| --- | --- |
| `dtp_Latn` | retrieval/Bible/Roundtrip/Taxi/embedding overlap anchor |
| `xav_Latn` | Bible/Roundtrip/POS/Taxi overlap anchor |
| `bam_Latn` | Bible/Roundtrip/POS/Taxi overlap anchor |
| `csb_Latn` | Tatoeba/NER/embedding overlap anchor |
| `ile_Latn` | Tatoeba/embedding anchor |
| `lij_Latn` | NER/POS anchor |
| `fur_Latn` | NER-ready low-band tail anchor |

## 준비 완료

- `preprocessing/prepare_v5_glot50010_merge_inputs.py`에 `v52_overlap7` selection 추가
- v5.2 전용 prepare/merge/tokenizer/initializer/training wrapper 추가
- `random/mean/fvt/weighted_fvt/family_mean` initializer 전체 default build로 수정
- `bash preprocessing/run_v52_glot5007_prepare.sh` 실행 성공
- `92/92` seen + `7/7` target raw symlink 확인

## 다음 단계

1. corpus merge
2. tokenizer training
3. initializer 5종 생성
4. GPU로 `random/mean/fvt/weighted_fvt/family_mean` 5-way 학습
5. 다른 GPU로 checkpoint별 평가
6. `docs/exp/v5.2` table/log 지속 갱신
