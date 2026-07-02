# GPU Policy

User constraint: use only physical GPU 3, NVIDIA RTX A6000.

Verified GPU inventory:

| Physical GPU | Name | Total memory | Current note |
| ---: | --- | ---: | --- |
| 0 | NVIDIA RTX A6000 | 49140 MiB | do not use |
| 1 | NVIDIA RTX A6000 | 49140 MiB | do not use |
| 2 | NVIDIA RTX A6000 | 49140 MiB | do not use |
| 3 | NVIDIA RTX A6000 | 49140 MiB | use only |

Run GPU experiments with:

```bash
source scripts/gpu3_env.sh
```

or explicitly:

```bash
CUDA_VISIBLE_DEVICES=3 <training-command>
```

Inside the process, physical GPU 3 appears as `cuda:0`.
