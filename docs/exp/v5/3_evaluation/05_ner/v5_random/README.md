# NER v5_random Output

이 폴더는 `v5_random_mlm_10k` NER post-checkpoint output provenance를
보관한다.

Model path:

```text
/home/axt/mnt2/jongha/v5_glot50010/runs/v5_random_mlm_10k
```

Final output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/v5_random/v5_random_mlm_10k
```

Final result file:

```text
/home/axt/mnt2/jongha/v5_glot50010/evaluation/ner/v5_random/v5_random_mlm_10k/test_results.txt
```

Promotion evidence, checked `2026-06-28 06:38 KST`:

- `test_results.txt`: `984` lines.
- `language=` rows: `164`.
- dev/best checkpoint row recorded in `eval_results.txt`.
- parsed by `scripts/aggregate_v5_metrics.py`.

Promotion rule: use aggregated F1 values and state that any v5-target row is an
actual evaluated intersection, not target10-wide coverage.
