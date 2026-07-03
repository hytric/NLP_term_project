# v5.2 한글 보고서 LaTeX

이 디렉터리는 `docs/paper/tex_ko/main.tex` 한글본과 산출 PDF를 관리한다. 현재 문서는 Glot500 원 논문 형식의 단순 요약이 아니라, XLM-R vocabulary extension에서 새 embedding row 초기화 방법을 통제 비교한 v5.2 실험 보고서다.

## 현재 한 줄 결론

50K 기준 종합 최선은 `weighted_fvt`다. `weighted_fvt`는 PPPL head/all, Tatoeba head/all, Bible head/tail/all, Roundtrip head/tail/all에서 최고이고 MLM loss도 가장 낮다. `family_mean`은 tail PPPL, tail Tatoeba, NER head/all에서 최고라 family prior가 특정 target 지표에 유효함을 보인다.

## 실험 설정 요약

- Base model: `xlm-roberta-base`
- Tokenizer: Glot500식 mixed-corpus vocabulary extension, append-only injection
- Corpus: 92개 XLM-R-seen replay 언어 + 7개 XLM-R-unseen Target7
- 비교 초기화: `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean`
- Training: continued MLM pretraining, 10K/20K/30K/40K/50K checkpoints
- Baseline: XLM-R-B, XLM-R-L head/tail/all 값 포함
- 평가: PPPL, Tatoeba retrieval, Bible retrieval, NER, Roundtrip alignment, Text Classification
- POS 결과는 본문/부록 표에서 제외

## 핵심 결과

- 확장 tokenizer는 Target7 tokens/word를 2.204에서 1.592로 낮춰 fragmentation을 27.75% 줄인다.
- `weighted_fvt`는 전체적으로 가장 안정적인 초기화다.
- `family_mean`은 tail PPPL/Tatoeba와 NER head/all에서 강해 related-language/family prior의 효과를 보여준다.
- `fvt`는 NER tail과 Text(EN)에서 최고이며, 초반에는 빠르게 출발하지만 30K-50K 구간에서 `weighted_fvt`/`family_mean`에 추월된다.
- `mean`은 loss와 PPPL에서 가장 나쁘고, `random`도 전반적으로 하위다.
- similarity map과 centered cosine 분석은 family/language clustering이 초기부터 형성되고 step 동안 안정적으로 유지됨을 보여준다.

## 평가 coverage 상태

본문 Table 6 앞의 상태 표와 동일한 기준이다.

- Tatoeba head: 완료, 25/25
- Bible head: 부분 완료, 21/25 완료; `family_mean` 10K/20K 일부, 30K/40K pending
- NER `weighted_fvt`/`family_mean`: 50K만 완료; 10K-40K pending
- Roundtrip head: 50K 5개만 완료; 10K-40K pending
- Text Classification tail: `not_applicable`; tail 언어 없음

Coverage 주석 마커는 사용하지 않는다. 값이 없거나 pending/not applicable이면 표에서는 `--`로 표시하고, 실행 상태는 본문 상태 표와 source TSV의 `status` 컬럼을 따른다.

## 주요 파일

- `main.tex`: 본문 전체, Table 6, 결론, 부록 input
- `main.pdf`: 빌드된 한글 PDF
- `Btables.tex`: 부록 B.1 step별 init/group 비교표, 자동 생성
- `Btables_by_method.tex`: 부록 B.2 init별 step trajectory 표, 자동 생성
- `figs/`: 논문용 plot과 similarity map grid
- `Makefile`: XeLaTeX/pdflatex 빌드 명령

## 표 구성

Table 6, B.1, B.2는 모두 같은 규칙을 따른다.

- Group 행 순서: `head`, `tail`, `all`
- 열: XLM-R-B, XLM-R-L, `random`, `mean`, `fvt`, `weighted_fvt`, `family_mean`
- retrieval/roundtrip/text/NER: x100
- PPPL: raw value
- Text Classification: English만 materialized되어 head/all은 같은 값, tail은 `--`
- 굵게: ablation 5개 방법 안에서 group별 최고

## 원자료

Repository 내부 요약:

- `docs/exp/v5.2/3_evaluation/11_inference/downstream_head_tail_all.tsv`
- `docs/exp/v5.2/3_evaluation/11_inference/downstream_baseline_head_tail_all.tsv`
- `docs/exp/v5.2/3_evaluation/11_inference/downstream_language_scores.tsv`
- `docs/exp/v5.2/3_evaluation/11_inference/downstream_baseline_language_scores.tsv`
- `docs/exp/v5.2/3_evaluation/11_inference/downstream_all_matrix.tsv`
- `docs/exp/v5.2/3_evaluation/11_inference/downstream_tables.md`
- `docs/exp/v5.2/3_evaluation/11_inference/similarity_maps/`

외부 raw eval/log 경로는 실험 서버의 `/home/axt/mnt2/jongha/v5.2_glot5007/` 아래에 있다. 보고서 표는 위 repository TSV를 기준으로 반영한다.

## 빌드

권장:

```bash
cd docs/paper/tex_ko
tectonic --keep-logs --keep-intermediates main.tex
```

Makefile 사용:

```bash
cd docs/paper/tex_ko
make pdf
```

Overleaf에서는 XeLaTeX로 컴파일한다.

## 수정 시 체크리스트

1. 새 raw 결과가 들어오면 먼저 `docs/exp/v5.2/3_evaluation/11_inference/*.tsv`를 확인한다.
2. Table 6, `Btables.tex`, `Btables_by_method.tex`를 같은 규칙으로 갱신한다.
3. 결론 문장이 Table 6의 실제 승자와 충돌하지 않는지 확인한다.
4. Coverage 주석 마커와 POS 표가 다시 들어가지 않았는지 검색한다.
5. `main.pdf`를 다시 빌드하고 Table 6, B.1, B.2, 결론 페이지를 렌더 확인한다.
