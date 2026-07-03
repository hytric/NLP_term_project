# Report Section Draft Workspace

이 폴더는 LaTeX 본문을 바로 고치기 전에 section별 내용을 Markdown으로 정리하는 작업 공간이다.
최종 LaTeX 파일은 `docs/paper/tex/sections/` 아래에 있고, 여기의 `.md` 파일은 논리, 근거,
표/그림 계획, claim boundary를 먼저 잡기 위한 초안이다.

## 사용 방식

1. 각 section의 `핵심 주장`을 먼저 한 문장으로 쓴다.
2. 그 주장마다 `근거 artifact`, `코드 위치`, `숫자`, `관련 reference`를 붙인다.
3. 표와 그림은 제목, 축/열 이름, 포함 이유, 해석 금지 사항까지 적는다.
4. 문장이 충분히 안정되면 대응되는 `docs/paper/tex/sections/*.tex`로 옮긴다.

## TeX 매핑

전체 상세 개요는 `detailed_outline.md`에 정리한다. 작성 유의사항은
`98_report_writing_notes.md`와 `99_claim_boundary_checklist.md`에 둔다. 아래 파일들은 그 개요를 section별로 더
자세히 풀어 쓰는 작업 파일이다.

| Markdown draft | Final TeX target |
| --- | --- |
| `detailed_outline.md` | 전체 report 구조 설계도 |
| `00_abstract.md` | `tex/sections/00_abstract.tex` |
| `01_introduction.md` | `tex/sections/01_introduction.tex` |
| `02_related_work.md` | `tex/sections/02_related_work.tex` |
| `03_data_scope.md` | `tex/sections/03_data.tex` |
| `04_method.md` | `tex/sections/04_method.tex` |
| `05_experiment_protocol.md` | `tex/sections/05_experiments.tex` |
| `06_results_50k_convergence.md` | `tex/sections/06_results.tex` |
| `07_analysis.md` | `tex/sections/07_analysis.tex` |
| `08_discussion_limitations_conclusion.md` | `tex/sections/08_limitations_conclusion.tex` |
| `09_appendix_artifacts.md` | `tex/sections/appendix_artifacts.tex` |
| `98_report_writing_notes.md` | 보고서 작성 유의사항 |
| `99_claim_boundary_checklist.md` | 최종 claim boundary 점검표 |

## 공통 작성 규칙

- 글은 간결하게 쓰되, 내용은 빈틈 없이 완결한다.
- 모든 주장에는 source artifact, code path, table, figure, 또는 reference를 붙인다.
- 모든 실험 행동에는 이유를 붙인다: 왜 이 언어, 왜 이 tokenizer, 왜 이 초기화, 왜 이 step, 왜 이 metric인지 쓴다.
- 50K-step convergence run이 본문 claim의 중심이다.
- Step-4000 결과는 early diagnostic으로만 쓴다.
- `random`, `mean`, `FVT`, `weighted FVT`, `family-aware mean` 다섯 방법을 main comparison으로 둔다.
- score table은 `tail`, `head`, `all` group을 분리한다.
- coverage가 없는 task/group은 0으로 쓰지 않고 `NA`로 둔다.
- target7은 모두 Latin script이므로 script diversity claim을 하지 않는다.
