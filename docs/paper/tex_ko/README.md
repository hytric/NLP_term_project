# 한글 보고서 (LaTeX)

`main.tex` — XLM-R 기반 저자원 언어 vocabulary extension에서의 embedding initialization 비교 (한글 term report).

## 빌드

```bash
cd docs/paper/tex_ko
make            # xelatex 2회 (권장; 한글 폰트 자동)
# 또는
make pdf-pdflatex   # pdflatex + kotex (nanum 폰트 설치 시)
```

- **xelatex 권장**: `kotex` + 시스템 한글 폰트로 바로 컴파일된다.
- Overleaf: 컴파일러를 **XeLaTeX**로 설정.

## 내용 동기화

수치·본문은 Markdown 원본 `docs/paper/보고서_한글.md` 및 `docs/paper/section/*.md`와 동일하다(50K 기준, POS 제외, NER 5-way 완료). 값 갱신 시 원본을 먼저 고치고 여기에 반영한다.

## 구성 파일

- `main.tex` — 본문(그림은 `figs/`, 부록 표는 `Btables.tex`를 `\input`).
- `figs/` — 생성된 plot(crossover, sim\_trend, map2d\_steps, strip\_*, initmap\_* 등). 없으면 아래 스크립트로 재생성.
- `Btables.tex` — 부록 B의 초기화 방법별 step 표(자동 생성).

## 그림/표 재생성

`figs/`와 `Btables.tex`는 `docs/exp/v5.2/3_evaluation/11_inference/downstream_head_tail_all.tsv` 등 원자료에서 matplotlib/PIL로 생성한다(생성 스크립트는 커밋 이력 참조). 원자료 경로가 바뀌면 재생성 후 컴파일한다.
