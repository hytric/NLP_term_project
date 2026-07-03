# v5.2 Live Status

Updated: `2026-07-03 03:53:28 KST`

## Checklist

| Section | Item | Status | Detail |
| --- | --- | --- | --- |
| prep | target7_manifest | `ready` | rows=7 path=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/miscellaneous/glot5007_selected_manifest.tsv |
| prep | stats_92_plus_7 | `ready` | path=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/miscellaneous/languages_stats_glot5007_xlmr100.csv |
| merge | corpus_text | `ready` | size=921.7MB path=/home/axt/mnt2/jongha/v5.2_glot5007/data/Glot500_v52_glot5007_xlmr100.txt |
| merge | merge_report | `PASS` | planned=4482259 actual=4482259 path=/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/0_tokenizer/merge/Glot500_v52_glot5007_xlmr100.report.json |
| tokenizer | extended_spm | `ready` | path=/home/axt/mnt2/jongha/v5.2_glot5007/tokenization/output/Glot500_extended_spm |
| init | random | `ready` | /home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_random |
| mlm | random | `exists` | checkpoints=8 latest=checkpoint-4000 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_random_mlm_8h |
| init | mean | `ready` | /home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_mean |
| mlm | mean | `exists` | checkpoints=8 latest=checkpoint-4000 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_mean_mlm_8h |
| init | fvt | `ready` | /home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_fvt |
| mlm | fvt | `exists` | checkpoints=8 latest=checkpoint-4000 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_fvt_mlm_8h |
| init | weighted_fvt | `ready` | /home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_weighted_fvt |
| mlm | weighted_fvt | `missing` | checkpoints=0 latest= path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_weighted_fvt_mlm_8h |
| init | family_mean | `ready` | /home/axt/mnt2/jongha/v5.2_glot5007/initialized_models/v5_family_mean |
| mlm | family_mean | `missing` | checkpoints=0 latest= path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_family_mean_mlm_8h |
| mlm_stage2 | random | `exists` | from=checkpoint-4000 checkpoints=0 latest=pending total_step=pending path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_random_mlm_converge_from4000 |
| mlm_stage2 | mean | `exists` | from=checkpoint-4000 checkpoints=0 latest=pending total_step=pending path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_mean_mlm_converge_from4000 |
| mlm_stage2 | fvt | `exists` | from=checkpoint-4000 checkpoints=0 latest=pending total_step=pending path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/v52_fvt_mlm_converge_from4000 |
| mlm_convergence_5way | random | `complete` | artifacts=43 checkpoint_dirs=43 latest_checkpoint=checkpoint-43000 checkpoint_step=43000 target_step=43000 queue_status=complete_43k_exposure_aligned_50k resume_step=43000 global_batch=36 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/convergence_5way/random |
| mlm_convergence_5way | mean | `complete` | artifacts=45 checkpoint_dirs=45 latest_checkpoint=checkpoint-45000 checkpoint_step=45000 target_step=45000 queue_status=stopped_at_user_requested_45k resume_step=45000 global_batch=36 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/convergence_5way/mean |
| mlm_convergence_5way | fvt | `complete` | artifacts=51 checkpoint_dirs=50 latest_checkpoint=checkpoint-50000 checkpoint_step=50000 final_model_step=50000 target_step=50000 queue_status=complete_50k_local_use_43k_for_fair resume_step=50000 global_batch=36 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/convergence_5way/fvt |
| mlm_convergence_5way | weighted_fvt | `complete` | artifacts=51 checkpoint_dirs=50 latest_checkpoint=checkpoint-50000 checkpoint_step=50000 final_model_step=50000 target_step=50000 queue_status=complete_50k resume_step=50000 global_batch=36 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/convergence_5way/weighted_fvt |
| mlm_convergence_5way | family_mean | `complete` | artifacts=51 checkpoint_dirs=50 latest_checkpoint=checkpoint-50000 checkpoint_step=50000 final_model_step=50000 target_step=50000 queue_status=complete_50k resume_step=50000 global_batch=36 path=/home/axt/mnt2/jongha/v5.2_glot5007/runs/convergence_5way/family_mean |

## GPU

```text
0, NVIDIA RTX A6000, 11, 48660, 0
1, NVIDIA RTX A6000, 2144, 46526, 0
2, NVIDIA RTX A6000, 11, 48660, 0
3, NVIDIA RTX A6000, 124, 48549, 0
```

## Active v5.2 Processes

```text
2769962 bash scripts/watch_v52_convergence_tables.sh watch
2795623 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795628 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795633 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795638 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795646 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795657 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795668 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795677 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795686 bash scripts/watch_v52_similarity_checkpoints.sh watch
2795694 bash scripts/watch_v52_similarity_checkpoints.sh watch
```

## Recent Logs

- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_5way_prior_fill.pid`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_5way_launcher_20260630_135751.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_5way.pid`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_5way_launcher.pid`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/probe_b18_20260630_135339.outer.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/train_v52_v52_probe_b18_20260630_135339_20260630_135339.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/train_v52_v52_probe_b20_20260630_135311_20260630_135311.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/probe_b20_20260630_135311.outer.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/train_v52_v52_probe_b24_20260630_135244_20260630_135244.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/probe_b24_20260630_135244.outer.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/probe_b32_20260630_135210.outer.log`
- `/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/train_v52_v52_probe_b32_20260630_135210_20260630_135210.log`
