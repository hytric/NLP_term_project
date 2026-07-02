MAIN=main
TECTONIC ?= tectonic

.PHONY: pdf pdf-tectonic clean

pdf:
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -xelatex -interaction=nonstopmode $(MAIN).tex; \
	elif command -v tectonic >/dev/null 2>&1; then \
		tectonic --keep-logs --keep-intermediates -p $(MAIN).tex; \
	else \
		echo "No latexmk or tectonic found."; \
		echo "Install TeX Live/xelatex, or run: conda create -y -n paper-tex -c conda-forge tectonic"; \
		echo "Then build with: conda run -n paper-tex tectonic --keep-logs --keep-intermediates -p $(MAIN).tex"; \
		exit 1; \
	fi

pdf-tectonic:
	$(TECTONIC) --keep-logs --keep-intermediates -p $(MAIN).tex

clean:
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -C $(MAIN).tex; \
	fi
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).xdv \
		$(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).fls $(MAIN).fdb_latexmk \
		$(MAIN).synctex.gz texput.log
