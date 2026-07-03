# v5.2 Similarity Checkpoint Watch Status

Updated: `2026-07-03 03:54:26 KST`

- eval gpu: `3`
- min free MB: `12000`
- metrics: `embedding_similarity family_similarity`
- wait for training done: `0`
- fair targets only: `0`
- prioritize fair targets: `1`
- method filters: `weighted_fvt`
- step bucket: `1/2`
- refresh tables: `0`
- fair target manifest: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/convergence_5way_fair_inference_targets.tsv`
- output root: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity`
- state: `/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/v52_similarity_checkpoint_done.tsv`

## Queue Summary

```text
ready checkpoint models: 238
ready metric jobs: 476
done ready metric jobs: 476
pending ready metric jobs: 0
fair targets ready: 5/5
fair target metric jobs done: 10/10
random: checkpoints=43 range=1000-43000
mean: checkpoints=45 range=1000-45000
fvt: checkpoints=50 range=1000-50000
weighted_fvt: checkpoints=50 range=1000-50000
family_mean: checkpoints=50 range=1000-50000
```

## Ready 5-Way Checkpoints

```text
v52_weighted_fvt_conv5way_step1000
v52_weighted_fvt_conv5way_step3000
v52_weighted_fvt_conv5way_step5000
v52_weighted_fvt_conv5way_step7000
v52_weighted_fvt_conv5way_step9000
v52_weighted_fvt_conv5way_step11000
v52_weighted_fvt_conv5way_step13000
v52_weighted_fvt_conv5way_step15000
v52_weighted_fvt_conv5way_step17000
v52_weighted_fvt_conv5way_step19000
v52_weighted_fvt_conv5way_step21000
v52_weighted_fvt_conv5way_step23000
v52_weighted_fvt_conv5way_step25000
v52_weighted_fvt_conv5way_step27000
v52_weighted_fvt_conv5way_step29000
v52_weighted_fvt_conv5way_step31000
v52_weighted_fvt_conv5way_step33000
v52_weighted_fvt_conv5way_step35000
v52_weighted_fvt_conv5way_step37000
v52_weighted_fvt_conv5way_step39000
v52_weighted_fvt_conv5way_step41000
v52_weighted_fvt_conv5way_step43000
v52_weighted_fvt_conv5way_step45000
v52_weighted_fvt_conv5way_step47000
v52_weighted_fvt_conv5way_step49000
```

## Recent State Rows

```text
family_similarity	v52_mean_conv5way_step39000	mean	39000	done	2026-07-03 01:32:24 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-39000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step39000_20260703_013133.log
family_similarity	v52_mean_conv5way_step40000	mean	40000	done	2026-07-03 01:32:33 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-40000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step40000_20260703_013205.log
embedding_similarity	v52_family_mean_conv5way_step35000	family_mean	35000	done	2026-07-03 01:32:45 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-35000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step35000_20260703_013215.log
embedding_similarity	v52_family_mean_conv5way_step36000	family_mean	36000	done	2026-07-03 01:32:56 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-36000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step36000_20260703_013223.log
family_similarity	v52_family_mean_conv5way_step35000	family_mean	35000	done	2026-07-03 01:33:00 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-35000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step35000_20260703_013245.log
embedding_similarity	v52_mean_conv5way_step42000	mean	42000	done	2026-07-03 01:33:02 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-42000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_mean_conv5way_step42000_20260703_013233.log
embedding_similarity	v52_mean_conv5way_step41000	mean	41000	done	2026-07-03 01:33:02 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-41000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_mean_conv5way_step41000_20260703_013224.log
family_similarity	v52_family_mean_conv5way_step36000	family_mean	36000	done	2026-07-03 01:33:12 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-36000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step36000_20260703_013256.log
embedding_similarity	v52_family_mean_conv5way_step37000	family_mean	37000	done	2026-07-03 01:33:16 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-37000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step37000_20260703_013300.log
family_similarity	v52_mean_conv5way_step42000	mean	42000	done	2026-07-03 01:33:16 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-42000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step42000_20260703_013302.log
family_similarity	v52_mean_conv5way_step41000	mean	41000	done	2026-07-03 01:33:17 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-41000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step41000_20260703_013302.log
family_similarity	v52_family_mean_conv5way_step37000	family_mean	37000	done	2026-07-03 01:33:30 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-37000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step37000_20260703_013316.log
embedding_similarity	v52_family_mean_conv5way_step38000	family_mean	38000	done	2026-07-03 01:33:41 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-38000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step38000_20260703_013312.log
embedding_similarity	v52_mean_conv5way_step44000	mean	44000	done	2026-07-03 01:33:52 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-44000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_mean_conv5way_step44000_20260703_013317.log
embedding_similarity	v52_mean_conv5way_step45000	mean	45000	done	2026-07-03 01:33:55 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-45000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_mean_conv5way_step45000_20260703_013317.log
family_similarity	v52_family_mean_conv5way_step38000	family_mean	38000	done	2026-07-03 01:33:57 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-38000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step38000_20260703_013341.log
embedding_similarity	v52_family_mean_conv5way_step39000	family_mean	39000	done	2026-07-03 01:33:58 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-39000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step39000_20260703_013330.log
family_similarity	v52_mean_conv5way_step44000	mean	44000	done	2026-07-03 01:34:07 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-44000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step44000_20260703_013352.log
family_similarity	v52_mean_conv5way_step45000	mean	45000	done	2026-07-03 01:34:12 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/mean/checkpoint-45000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_mean_conv5way_step45000_20260703_013355.log
embedding_similarity	v52_family_mean_conv5way_step40000	family_mean	40000	done	2026-07-03 01:34:13 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-40000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step40000_20260703_013357.log
family_similarity	v52_family_mean_conv5way_step39000	family_mean	39000	done	2026-07-03 01:34:15 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-39000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step39000_20260703_013358.log
family_similarity	v52_family_mean_conv5way_step40000	family_mean	40000	done	2026-07-03 01:34:28 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-40000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step40000_20260703_013413.log
embedding_similarity	v52_family_mean_conv5way_step41000	family_mean	41000	done	2026-07-03 01:34:31 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-41000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step41000_20260703_013415.log
embedding_similarity	v52_family_mean_conv5way_step42000	family_mean	42000	done	2026-07-03 01:34:44 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-42000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step42000_20260703_013428.log
family_similarity	v52_family_mean_conv5way_step41000	family_mean	41000	done	2026-07-03 01:34:46 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-41000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step41000_20260703_013431.log
family_similarity	v52_family_mean_conv5way_step42000	family_mean	42000	done	2026-07-03 01:34:58 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-42000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step42000_20260703_013444.log
embedding_similarity	v52_family_mean_conv5way_step43000	family_mean	43000	done	2026-07-03 01:35:02 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-43000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step43000_20260703_013446.log
embedding_similarity	v52_family_mean_conv5way_step44000	family_mean	44000	done	2026-07-03 01:35:14 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-44000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step44000_20260703_013458.log
family_similarity	v52_family_mean_conv5way_step43000	family_mean	43000	done	2026-07-03 01:35:18 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-43000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step43000_20260703_013502.log
family_similarity	v52_family_mean_conv5way_step44000	family_mean	44000	done	2026-07-03 01:35:36 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-44000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step44000_20260703_013514.log
embedding_similarity	v52_family_mean_conv5way_step45000	family_mean	45000	done	2026-07-03 01:35:50 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-45000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step45000_20260703_013518.log
embedding_similarity	v52_family_mean_conv5way_step46000	family_mean	46000	done	2026-07-03 01:36:13 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-46000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step46000_20260703_013536.log
family_similarity	v52_family_mean_conv5way_step45000	family_mean	45000	done	2026-07-03 01:36:35 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-45000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step45000_20260703_013550.log
family_similarity	v52_family_mean_conv5way_step46000	family_mean	46000	done	2026-07-03 01:36:59 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-46000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step46000_20260703_013613.log
embedding_similarity	v52_family_mean_conv5way_step47000	family_mean	47000	done	2026-07-03 01:37:09 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-47000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step47000_20260703_013635.log
embedding_similarity	v52_family_mean_conv5way_step48000	family_mean	48000	done	2026-07-03 01:37:38 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-48000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step48000_20260703_013659.log
family_similarity	v52_family_mean_conv5way_step47000	family_mean	47000	done	2026-07-03 01:37:52 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-47000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step47000_20260703_013709.log
family_similarity	v52_family_mean_conv5way_step48000	family_mean	48000	done	2026-07-03 01:38:27 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-48000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step48000_20260703_013738.log
embedding_similarity	v52_family_mean_conv5way_step49000	family_mean	49000	done	2026-07-03 01:38:29 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-49000/embedding_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_embedding_similarity_v52_family_mean_conv5way_step49000_20260703_013753.log
family_similarity	v52_family_mean_conv5way_step49000	family_mean	49000	done	2026-07-03 01:39:09 KST	/home/axt/jongha/Glot500-py39-eval/docs/exp/v5.2/3_evaluation/10_convergence_similarity/family_mean/checkpoint-49000/family_similarity	/home/axt/mnt2/jongha/v5.2_glot5007/runs/logs/convergence_similarity/v52_family_similarity_v52_family_mean_conv5way_step49000_20260703_013829.log
```
