# Release Audit Summary

작성일: 2026-06-04

## Current Verdict

The active experiment-progress goal is satisfied: target10 scope, ordered experiment execution, GPU-3 policy, intermediate reporting, documentation location, and large-artifact location have all been checked against current state. The experiment story is ready for a cautious paper draft, but the repository is not yet ready for a public GitHub release. The main release blockers are worktree cleanup and final data-license redistribution decisions.

## Ready To Claim

- Target10 low-resource language scope is fixed and documented.
- Tokenizer extension substantially reduces fragmentation for the most affected languages.
- Mean embedding initialization is the selected MLM adaptation setting for the pilot.
- Direct Coptic/Syriac NMT and Greek pivot/back-translation are negative gates.
- Retrieval is the strongest current Coptic baseline.
- Pairwise retrieval selection gives a small improvement over the feature reranker.
- 10C same-checkpoint controls show the neural retrieval-edit gate is negative: the model is retrieval-sensitive, but retrieved-only slightly beats source+retrieval and source-only collapses.

## Do Not Claim

- Do not claim solved Coptic/Syriac neural translation.
- Do not claim Greek pivoting or back-translation is usable from the current checkpoints.
- Do not claim neural retrieval editing is source-grounded under the current ByT5-small budget.
- Do not claim the GitHub repository is release-clean until tracked/untracked files are reviewed.

## Storage And Large-File Check

Large project artifacts are intentionally outside the repository through symlinks:

- `data -> /disk1/axt/jongha/Glot500-py39-eval/data`
- `download -> /disk1/axt/jongha/Glot500-py39-eval/download`
- `docs/exp/2026-06-03_05_mlm_adaptation -> /disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_05_mlm_adaptation`
- `docs/exp/2026-06-03_06_nmt_baselines -> /disk1/axt/jongha/Glot500-py39-eval/docs/exp/2026-06-03_06_nmt_baselines`

No repo-local regular file over 50M was found in the top two levels. A root `main.zip` archive exists as a 3.1M local file and is now ignored; remove it before release if it is not intentionally needed.

## License Evidence

Local source files found during audit:

- `data/raw/bible-corpus/LICENSE`: CC0 1.0 Universal.
- `data/raw/bible-corpus/README.md`: multilingual Bible corpus documentation and citation pointer.
- `data/raw/UD_Coptic-Scriptorium/LICENSE.txt`: Coptic Treebank annotation data under Creative Commons Attribution 4.0; underlying source material has source-specific attribution notes.
- `data/raw/UD_Coptic-Scriptorium/README.md`: Coptic Treebank description, citation, and corpus/source context.

Release decision: publish code, metrics, and short examples only. Keep full corpora, aligned verse files, generated synthetic corpora, and checkpoints out of Git unless source-specific redistribution permission is confirmed.

## Remaining Release Actions

- Review tracked modifications in `modeling/*.py` and `evaluation/download_data/download_data.sh`.
- Decide whether untracked `scripts/`, `docs/`, and Python 3.9 setup files should be committed.
- Remove or keep ignored `main.zip` outside release history.
- Finish source-by-source license table for every raw corpus used, not only the two local license files found in this audit.
- Run final syntax/check commands after any last script edits.

These are release-hardening tasks, not blockers for the active experiment-progress goal.
