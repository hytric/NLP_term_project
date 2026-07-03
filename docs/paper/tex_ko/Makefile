# 한글 보고서 빌드 (kotex)
# 기본: xelatex (한글 폰트 자동). 대안: latexmk -pdfxe
MAIN = main

pdf:
	xelatex -interaction=nonstopmode $(MAIN).tex
	xelatex -interaction=nonstopmode $(MAIN).tex

# pdflatex + kotex 사용 시 (nanum 계열 폰트 필요)
pdf-pdflatex:
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc

cleanall: clean
	rm -f $(MAIN).pdf
