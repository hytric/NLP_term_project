# Third Try Status Report

작성일: 2026-06-13

Note: 이 보고서는 2026-06-13 중간 상태 보고서다. Stage 05 시작 전 최종 go/no-go 판단은 `final_pre_start_report_20260613.md`를 따르고, 이후 실행 결과는 `05_mlm/results.md`와 `06_eval/results.md`를 따른다.

## 2026-06-13 Late Addendum

이 파일의 아래 본문은 Stage 01/02 시점의 중간 상태를 보존한다. 최신 상태는 다음과 같다.

- Stage 03: target-heavy 48k tokenizer와 byte-vs-char fallback ablation까지 완료했다.
- Stage 05: fvt 3-seed 200-step MLM pilot과 lower-LR replay-safe 1000-step 3-seed retry를 완료했다.
- Stage 06: target10 MLM proxy, frozen Bible proxy, Coptic POS pilot/replay-safe eval, high-resource control proxy, target10 downstream availability audit을 완료했다.
- Stage 07: `PASS_NEGATIVE_MAIN_READY`. Positive claim은 target10 downstream coverage, MLM proxy, high-resource control 때문에 막혔다.
- Stage 08: `PASS_ABLATION_PACKAGE_READY`. first_try/second_try는 main result가 아니라 ablation/failure analysis로 배치한다.
- 최종 감사: `final_goal_completion_audit_20260613.md` 기준 positive claim은 `NO_GO`, diagnostic negative report package는 `READY`.

최신 claim 판단은 `07_main_claim/results.md`와 `08_ablation/results.md`를 따른다.

## 요약

`third_try`는 현재 Stage 01 data 단계 진행 중이다. Stage 00의 핵심 scope는 닫았다: target10 전체를 main으로 유지하고, Coptic/Syriac는 main experiment에 포함하며, 모델은 `xlm-roberta-base`만 사용한다.

가장 중요한 변경은 true high-resource web replay를 실제로 추가했다는 점이다. Bible high-resource는 domain-matched control로 남기고, main mixture에는 GlotCC-V1 web sample을 high-resource replay로 넣는다.

## 완료

| Item | Status | Evidence |
| --- | --- | --- |
| target10 유지 | DONE | `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp` |
| Coptic/Syriac main 포함 | DONE | `cop`, `syr`는 target10 main language |
| XLM-R-base-only rule | DONE | `xlm-roberta-large` 제외 |
| high-resource true web source | DONE | GlotCC-V1 sample materialized |
| high-resource domain control | DONE | English/German/Japanese/Korean Bible XML confirmed |

## 생성된 High-Resource 데이터

Root:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc`

Manifest:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`

| Config | Selected shards | Source size | Docs | Lines | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `eng-Latn` | 2 / 541 | 2.559 GB | 11274 | 200000 | PASS |
| `deu-Latn` | 2 / 90 | 2.984 GB | 9573 | 200000 | PASS |
| `jpn-Jpan` | 2 / 2 | 2.451 GB | 20555 | 200000 | PASS |
| `kor-Hang` | 2 / 8 | 2.506 GB | 14732 | 200000 | PASS |

총 800000 line을 Stage 01 mixture 후보로 확보했다.

## 현재 Blocking Point

`01_data/mlm_mixture_manifest.tsv`는 생성 완료했다. 이제 Stage 02 baseline audit을 시작할 수 있다. GPU가 필요한 모든 실행은 GPU 3번만 사용한다.

## 수정된 실행 계획

1. Stage 02에서 downstream baseline subset을 확정한다.
2. Exact PPPL은 compute budget이 허용되면 `CUDA_VISIBLE_DEVICES=3`으로 실행한다.
3. Stage 03에서 id-preserving tokenizer extension 후보를 만든다.
4. Stage 04에서 random/mean/fvt/align/focus initialization 후보를 준비한다.
5. Stage 05에서 high-resource + low-resource full MLM을 3개 이상 seed로 진행한다.

## 다음 산출물

| File | Purpose |
| --- | --- |
| `02_baseline/baseline_eval.tsv` | tokenization + deterministic MLM eval baseline |
| `02_baseline/results.md` | Stage 02 current gate report |

## 현재 결론

사용자가 지적한 "high-resource 부족" 문제는 해결 방향으로 반영했고, Bible-only가 아니라 GlotCC-V1 기반 true high-resource web replay를 실제로 추가했다. Stage 01 mixture는 leakage-safe하게 닫았고, Stage 02에서는 XLM-R-base tokenization 및 deterministic MLM baseline까지 확보했다. 다음은 downstream baseline subset 확정과 tokenizer extension이다.
