# Data And License Notes

작성일: 2026-06-04

## Current Data Use

The project uses local Bible-derived corpora and aligned verse files.
The current workspace stores processed data under:

```text
data/processed/
```

The `data` path is a symlink to:

```text
/disk1/axt/jongha/Glot500-py39-eval/data
```

## Local License Evidence Found

Files found during the 2026-06-04 release audit:

| Source path | Evidence | Current reading | Release action |
| --- | --- | --- | --- |
| `data/raw/bible-corpus/LICENSE` | CC0 1.0 Universal license text | The repository copy presents the corpus under CC0. | Cite the corpus source; full redistribution appears less restricted, but still avoid shipping large full text by default. |
| `data/raw/bible-corpus/README.md` | corpus description and citation pointer | Multilingual Bible corpus documentation. | Cite Christodoulopoulos and Steedman and keep processing scripts reproducible. |
| `data/raw/UD_Coptic-Scriptorium/LICENSE.txt` | Creative Commons Attribution 4.0 note for annotation data plus underlying source notes | Annotation data is CC BY 4.0; underlying source material has source-specific attribution/permission context. | Include attribution and do not redistribute full underlying source text until confirmed. |
| `data/raw/UD_Coptic-Scriptorium/README.md` | Coptic Treebank description and citation | Coptic Scriptorium/UD source context and citation are documented. | Cite Zeldes and Abrams and keep source-specific notes in the final paper. |

## Release Principle

Do not push large corpora or model checkpoints to GitHub unless their licenses explicitly permit redistribution.

Release-safe materials:

- scripts;
- experiment plans/results;
- metric tables;
- qualitative examples if allowed by the source license and kept short;
- reproducibility instructions;
- checksums or manifests if useful.

Potentially sensitive materials:

- full Bible corpora;
- full aligned verse files;
- downloaded archives;
- model checkpoints;
- generated synthetic corpora.

## Minimum License Checklist

Before public release:

- [x] Identify local license files for `bible-corpus` and `UD_Coptic-Scriptorium`.
- [ ] Identify the exact source and license for each Bible XML/file used.
- [ ] Confirm whether redistribution of full text is allowed.
- [ ] If redistribution is not allowed, publish preparation scripts only.
- [ ] Keep `data/` ignored or symlinked outside the committed tree.
- [ ] Keep checkpoints out of Git.
- [ ] Include a note that users must obtain source corpora according to the original licenses.

## Current Evidence Files

Data inventory:

- `docs/exp/2026-06-03_01_data_and_splits/results.md`
- `data/processed/target10/target_languages.tsv`
- `data/processed/target10/target10_stats.tsv`

Experiment metrics:

- `docs/exp/2026-06-03_08_evaluation_analysis/final_metrics.tsv`

## Suggested GitHub Wording

This repository contains code, experiment notes, and metric summaries for a target10 low-resource adaptation pilot. Full source corpora and model checkpoints are not included by default. Users should obtain the original corpora according to their licenses and run the preparation scripts to reproduce the processed files.
