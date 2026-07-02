# Intermediate Report: 2026-06-04

## Current Goal

Proceed sequentially with the target10 low-resource-language experiment plan, using only physical GPU 3 (`NVIDIA RTX A6000`) for GPU work.

## Git And Workspace

- `git pull --ff-only`: already up to date.
- Current modified tracked files already present in the workspace include `.gitignore`, `evaluation/download_data/download_data.sh`, and several `modeling/*.py` files.
- New experiment documentation remains under `docs/exp`.

## Storage Check

Large local paths were moved to `/disk1` and the original repository paths now resolve through symlinks:

| Repo path | Real path |
| --- | --- |
| `data` | `/disk1/axt/jongha/Glot500-py39-eval/data` |
| `download` | `/disk1/axt/jongha/Glot500-py39-eval/download` |
| `docs/exp/2026-06-03_05_mlm_adaptation` | `/disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_05_mlm_adaptation` |
| `docs/exp/2026-06-03_06_nmt_baselines` | `/disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_06_nmt_baselines` |

Disk state after cleanup:

- Root `/`: 879G total, 564G used, 271G available, 68% used.
- `/disk1`: 13T total, 7.7T used, 4.4T available, 64% used.

## Target10 Scope

The 10-language set is:

| ISO | Language | Script |
| --- | --- | --- |
| `cop` | Coptic | Coptic |
| `syr` | Syriac | Syriac |
| `chr` | Cherokee | Cherokee |
| `oji` | Ojibwa | Aboriginal Syllabics |
| `bsn` | Barasana-Eduria | Latin |
| `usp` | Uspanteco | Latin |
| `nhg` | Nahuatl (Tetelcingo) | Latin |
| `ake` | Akawaio | Latin |
| `kbh` | Camsa | Latin |
| `acu` | Achuar-Shiwiar | Latin |

The tokenizer, vocabulary-extension, embedding-initialization, and MLM adaptation stages use this target10 set. Downstream NMT is focused on Coptic/Syriac and pivot English/Greek paths.

## GPU Check

GPU policy:

- Use only physical GPU 3.
- Command pattern: `source scripts/gpu3_env.sh`.
- Inside a run, physical GPU 3 appears as `cuda:0`.

Pre-10C GPU state:

- GPU 3: 127 MiB used, 0% utilization.

Post-10C note:

- The 10C training process finished and no `train_pretrained_seq2seq_baseline.py` process remains.
- After the run, GPU 3 was occupied by other Python jobs outside this experiment, so additional controls were not started.

## Newly Run 07 Gate Experiments

Two Greek pivot gate pilots were run with `google/byt5-small` fp32, 256 train examples, 32 dev/test examples, 50 steps, and `--skip_save_model`.

| Direction | Test BLEU | Test chrF++ | Gen len | Main observation |
| --- | ---: | ---: | ---: | --- |
| Syriac -> Greek | 0.0000 | 3.5930 | 127.0 | Greek-script output, but repetitive and max-length |
| Greek -> Coptic | 0.0000 | 0.0000 | 127.0 | Fails to produce Coptic; outputs remain Greek-script |

Plain-language conclusion:

- Greek pivot is not ready for back-translation.
- The first leg can emit Greek-looking text, but it is repetitive.
- The second leg does not switch into Coptic at all.
- Scaling these models into synthetic data would add noise rather than useful supervision.

## Next Recommended Step

Continue sequentially into 08 evaluation/analysis:

- consolidate tokenizer, MLM, NMT, retrieval, and pivot-gate tables;
- write paper-ready failure analysis;
- keep future GPU experiments on GPU 3 only;
- only revisit back-translation with a stronger model/objective, not this tiny ByT5 gate.

## Follow-Up Progress: Evaluation And Release Drafts

08번 평가/분석 단계에서 추가로 정리한 문서:

| File | Purpose |
| --- | --- |
| `docs/exp/2026-06-03_08_evaluation_analysis/final_metrics.tsv` | 핵심 수치만 모은 최종 metric table |
| `docs/exp/2026-06-03_08_evaluation_analysis/paper_tables.md` | 논문/발표용 표 초안 |
| `docs/exp/2026-06-03_08_evaluation_analysis/paper_figures.md` | Figure 1 설명과 caption 초안 |
| `docs/exp/2026-06-03_08_evaluation_analysis/figures/target10_tokenization_reduction.png` | target10 tokenizer reduction 그림 |
| `docs/exp/2026-06-03_08_evaluation_analysis/figures/target10_tokenization_reduction.tsv` | Figure 1 원천 수치 |
| `docs/exp/2026-06-03_08_evaluation_analysis/qualitative_analysis.md` | 20개 예시 기반 질적 분석 |
| `docs/exp/2026-06-03_08_evaluation_analysis/error_taxonomy.md` | 오류 유형 분류 |

09번 보고/릴리스 단계에서 추가로 정리한 문서:

| File | Purpose |
| --- | --- |
| `docs/exp/2026-06-03_09_report_release/progress_report.md` | 진행 보고서 초안 |
| `docs/exp/2026-06-03_09_report_release/term_paper_outline.md` | term paper 구조 초안 |
| `docs/exp/2026-06-03_09_report_release/related_work_notes.md` | XLM-R, Glot500, NLLB, SentencePiece, tokenizer-quality, ByT5, RAG 관련연구 노트 |
| `docs/exp/2026-06-03_09_report_release/final_presentation_outline.md` | 발표 슬라이드 구조 |
| `docs/exp/2026-06-03_09_report_release/reproducibility_checklist.md` | 재현성 체크리스트 |
| `docs/exp/2026-06-03_09_report_release/command_examples.md` | 주요 stage별 명령 예시 |
| `docs/exp/2026-06-03_09_report_release/claim_evidence_map.md` | 주장별 증거 파일 매핑 |
| `docs/exp/2026-06-03_09_report_release/experiment_manifest.tsv` | 00-09 stage 상태 요약 |
| `docs/exp/2026-06-03_09_report_release/data_license_notes.md` | 데이터/라이선스 릴리스 주의사항 |
| `docs/exp/2026-06-03_09_report_release/limitations.md` | 한계 섹션 초안 |
| `docs/exp/2026-06-03_09_report_release/final_submission_checklist.md` | 최종 제출 체크리스트 |

10번 source-grounding/retrieval-editing 단계에서 추가한 문서:

| File | Purpose |
| --- | --- |
| `docs/exp/2026-06-04_10_source_grounding_editing/plan.md` | retrieval copy dependence를 줄이기 위한 10A/10B/10C 다음 실험 계획 |
| `docs/exp/2026-06-04_10_source_grounding_editing/source_candidate_summary.md` | 10A CPU source-candidate 진단 요약 |
| `docs/exp/2026-06-04_10_source_grounding_editing/source_candidate_diagnostics.tsv` | 879개 test row별 top1/feature/oracle 후보 gap |
| `docs/exp/2026-06-04_10_source_grounding_editing/source_candidate_examples.md` | feature 개선/악화/oracle headroom 예시 |
| `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_method.md` | 10B selector 학습/평가 방법 |
| `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_summary.md` | 10B CPU selector 결과 요약 |
| `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_results.tsv` | 10B selector별 test metric 비교 |
| `docs/exp/2026-06-04_10_source_grounding_editing/candidate_decision_errors.md` | 10B 개선/악화/놓친 oracle 예시 |
| `docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_method.md` | 10B pairwise selector 방법 |
| `docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_summary.md` | 10B pairwise selector 결과 요약 |
| `docs/exp/2026-06-04_10_source_grounding_editing/pairwise_selector_results.tsv` | 10B pairwise selector metric 비교 |
| `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_pilot_results.tsv` | 10C pairwise-selected edit gate metric |
| `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_controls.md` | 10C 완료 gate와 pending controls |
| `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_qualitative.md` | 10C 예측 예시와 오류 해석 |
| `docs/exp/2026-06-04_10_source_grounding_editing/retrieval_edit_control_datasets.tsv` | 10C source-only/retrieved-only/wrong/feature-selected control 데이터셋 manifest |

10A 쉽게 읽는 결과:

- GPU 사용 없음; CPU-only 분석이다.
- Row-level top1 candidate 평균 chrF++: 22.7410.
- Row-level feature-selected 평균 chrF++: 24.7724.
- Row-level oracle@8 평균 chrF++: 28.9181.
- Oracle이 rank 1이 아닌 경우: 663/879.
- Feature-selected rank가 oracle rank와 일치한 경우: 298/879.
- 결론: feature reranking은 도움이 되지만, keep/swap/reject selector를 더 시험할 headroom이 남아 있다.

10B 쉽게 읽는 결과:

- GPU 사용 없음; CPU-only selector 실험이다.
- Validation OOF 기준 선택된 모델: gradient boosting.
- Test corpus chrF++: top1 22.5362, 기존 feature reranker 24.5921, 10B selector 24.6862, oracle@8 28.3327.
- 10B는 top1보다 좋아졌고 기존 feature reranker도 아주 조금 넘겼다.
- 그래도 oracle@8과 3.6465 chrF++ 차이가 남아 있어, 바로 GPU edit model을 크게 돌리기보다 pairwise/listwise selector 또는 작은 10C gate가 맞다.

10B pairwise 쉽게 읽는 결과:

- GPU 사용 없음; CPU-only pairwise selector 실험이다.
- 모델: logistic regression over candidate-pair feature differences.
- Test corpus chrF++: 24.7438.
- 현재 CPU retrieval selector 중 가장 높다.
- 그래도 oracle@8 28.3327과 차이가 남아 있어, 번역 생성 모델을 크게 돌리기보다 작은 10C gate와 copy/source control이 필요하다.

10C pairwise edit gate 쉽게 읽는 결과:

- GPU 사용: physical GPU 3 only.
- 모델: `google/byt5-small`, train 512 examples, 120 steps, fp32, `--skip_save_model`.
- 64-test slice에서 test chrF++: 18.3574.
- 같은 64-test slice의 pairwise-selected retrieval candidate 자체 chrF++: 26.6235.
- Prediction vs retrieved candidate chrF++: 52.6372.
- Exact prediction=retrieved copy: 0/64, retrieved contains prediction: 17/64.
- Same-checkpoint controls:
  - source-only chrF++: 0.2729
  - retrieved-only chrF++: 18.6220
  - wrong-shift1 chrF++: 12.8253
  - feature-selected top8 chrF++: 19.1558
- 결론: English source만으로는 거의 실패하고, retrieved-only가 correct source+retrieval보다 살짝 높다. Wrong retrieval은 성능을 낮추므로 retrieval-sensitive이긴 하지만, 현 ByT5 gate는 source-grounded editing이라고 보기 어렵다. 10C는 negative gate다.

현재 쉽게 읽는 결론:

- 10개 저자원 언어만 대상으로 한 target10 설정은 유지되고 있다.
- Tokenizer extension과 Mean initialization은 강한 긍정 결과다.
- Direct NMT와 Greek pivot/back-translation gate는 번역 품질 측면에서 실패다.
- Retrieval은 강력한 baseline이지만, neural retrieval-augmented 모델은 아직 retrieved Coptic copy에 많이 의존한다.
- 따라서 다음 실험을 더 한다면 단순 학습 step 증가나 back-translation 확대보다 source-grounding/retrieval-editing objective가 필요하다.
- 관련연구 citation spine과 Figure 1은 초안 완료 상태다.
- 10A source-candidate diagnostics는 완료되었고, 10B selector 여부를 판단할 근거가 생겼다.
- 10B CPU selector도 완료되었고, candidate-selection 방향은 유효하다는 작은 양의 결과가 나왔다.
- 10B pairwise selector가 pointwise selector를 조금 넘겨 현재 best CPU selector가 되었다.
- 10C same-checkpoint controls까지 완료되었고 negative signal이다. Retrieval selection은 유지하되, neural editing은 positive claim으로 쓰면 안 된다.

아직 남은 제출 전 작업:

- 데이터 원천별 license 확인;
- public GitHub release 전에 untracked/modified 파일 정리;
- 10C는 failure analysis로 정리하고, 추가 GPU scaling보다 보고서/라이선스/재현성 정리를 우선 진행.

## Follow-Up Progress: Release Audit

11번 릴리즈 감사 단계에서 추가로 확인한 문서:

| File | Purpose |
| --- | --- |
| `docs/exp/2026-06-04_11_release_audit/plan.md` | active goal completion audit와 release cleanup 계획 |
| `docs/exp/2026-06-04_11_release_audit/release_audit_summary.md` | claim 가능/불가, storage, license, release risk 요약 |
| `docs/exp/2026-06-04_11_release_audit/artifact_inventory.tsv` | docs/scripts/data symlink/archive/checkpoint 처리 목록 |
| `docs/exp/2026-06-04_11_release_audit/completion_audit.md` | 사용자 요구사항별 완료 증거 |

쉽게 읽는 결론:

- Active experiment-progress 목표는 완료 기준을 충족했다.
- `git pull --ff-only`는 2026-06-04 13:25 KST에 최신 상태를 확인했다.
- `find -L` 기준 init, 00-11 모든 stage에 `plan.md`가 있다.
- target10은 정확히 10개 언어(`cop,syr,chr,oji,bsn,usp,nhg,ake,kbh,acu`)로 유지된다.
- GPU 정책은 physical GPU 3 only이며, 현재 프로젝트 학습 프로세스는 돌고 있지 않다.
- `data`, `download`, 05 MLM, 06 NMT 대용량 경로는 `/disk1`로 resolve된다.
- root `main.zip`은 3.1M local archive이며 이제 ignored 상태다.
- public GitHub release 전에는 worktree 정리와 source별 redistribution 결정이 아직 필요하다.
