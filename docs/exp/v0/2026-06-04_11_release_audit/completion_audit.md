# Completion Audit

작성일: 2026-06-04

## User Requirements

| Requirement | Status | Evidence |
| --- | --- | --- |
| Start from latest repository state with `git pull` | complete | `git pull --ff-only` returned `Already up to date` on 2026-06-04 13:25 KST |
| Proceed sequentially through experiments | complete for current plan | `find -L docs/exp -maxdepth 2 -type f -name plan.md` shows ordered stages init, 00-11, including symlinked 05/06 plans |
| Use only physical GPU 3 | complete for project GPU work | `scripts/gpu3_env.sh` sets `CUDA_VISIBLE_DEVICES=3`; 10C notes record physical GPU 3 only; no current project training process is running |
| Focus on about 10 low-resource languages | complete | `data/processed/target10/target_languages.tsv` has 10 data rows: `cop,syr,chr,oji,bsn,usp,nhg,ake,kbh,acu` |
| Create ordered experiment folders and plan files under `docs/exp` | complete through stage 11 | `docs/exp/README.md`; `docs/exp/2026-06-04_11_release_audit/plan.md` |
| Check changed documentation location | complete | docs are centralized under `docs/exp/`; stage 11 documents the location audit |
| Check changed large-file locations | complete | `readlink -f` resolves `data`, `download`, 05 MLM, and 06 NMT paths to `/disk1/axt/jongha/Glot500-py39-eval/...` |
| Report intermediate results clearly | complete | `docs/exp/2026-06-04_intermediate_report.md`, `progress_report.md`, `final_metrics.tsv`, 10C controls, and release audit summary |

## Verification Commands

Latest checks run on 2026-06-04:

```bash
git pull --ff-only
find -L docs/exp -maxdepth 2 -type f -name plan.md | sort
readlink -f data download docs/exp/2026-06-03_05_mlm_adaptation docs/exp/2026-06-03_06_nmt_baselines
df -h . /disk1
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader
find scripts -name '*.py' -print0 | xargs -0 python3 -m py_compile
git diff --check
```

Results:

- Repository pull: already up to date.
- Target language count: 10 rows.
- Storage: `/` has 272G available; `/disk1` has 4.4T available.
- Top-level regular files over 50M: none found.
- Root `main.zip`: local 3.1M file, now ignored.
- Python script syntax check: passed.
- Whitespace diff check: passed.
- Python cache directories under `scripts/`: removed after validation.

## Still Open

- Public-release worktree cleanup is not done.
- Full data redistribution approval is not done.
- Final paper prose still needs to be assembled from the current outlines and evidence files.

These open items are documented release/paper-hardening tasks. They do not contradict completion of the active experiment-progress objective.
