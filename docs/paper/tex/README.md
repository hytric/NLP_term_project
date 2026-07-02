# Term Report LaTeX Draft

Build from this directory:

```bash
make pdf
```

The draft is written for `xelatex` because the report contains Korean text through `kotex`.
If `latexmk` is unavailable but `xelatex` and `bibtex` are installed, run:

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

On the current workstation, system TeX tools were unavailable and `sudo` required a password, so
the PDF was verified with a user-level conda environment:

```bash
conda create -y -n paper-tex -c conda-forge tectonic
conda run -n paper-tex tectonic --keep-logs --keep-intermediates -p main.tex
```

This produced `main.pdf` successfully.

Main source files:

- `main.tex`: report entry point.
- `sections/`: prose draft.
- `tables/`: reusable tables.
- `references.bib`: BibTeX entries used by the report.

Figure paths point to existing v5.2 artifacts under `docs/exp/v5.2` so the report stays tied to
the actual experiment outputs.
