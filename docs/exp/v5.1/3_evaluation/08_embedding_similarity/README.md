# v5.1 Embedding Similarity / 2D Map

목표: Glot500-style downstream metric 외에 novelty 분석용 sentence-vector
similarity와 2D point map을 만든다.

## Required Outputs

| Artifact | Purpose | Status |
| --- | --- | --- |
| `similarity_pairs.tsv` | same-language / same-meaning / roundtrip pair input | done |
| `similarity_pair_summary.tsv` | pair counts by source/type/group | done |
| `similarity_scores.tsv` | cosine, centered cosine, optional CSLS | pending |
| `similarity_summary.md` | group별 평균/분산 table | pending |
| `embedding_map_2d.png` | UMAP/t-SNE 2D point map | pending |
| `README.md` | method, layer, pooling, coverage note | ready |

Current pair input:

```text
total_pairs = 22600
tatoeba_target_pairs = 300  # 150 aligned + 150 same-language
bible_target_pairs = 600    # 300 aligned + 300 same-language
roundtrip_target_pairs = 600
```

## Method Contract

- encoder layer: layer 8, matching Glot500 retrieval/alignment convention
- pooling: mean pooling over non-special tokens
- comparisons:
  - same language, different sentences
  - same meaning, cross-lingual aligned pairs
  - roundtrip alignment chain pairs where available
- groups:
  - head
  - target10
  - available downstream subset

## Claim Boundary

Similarity maps are qualitative/diagnostic evidence. They can support the
interpretation of FVT initialization and downstream behavior, but they do not
replace PPPL, retrieval, classification, NER, POS, or roundtrip metrics.

## Commands

Build pair input only:

```bash
python3 scripts/build_v51_similarity_pairs.py \
  --eval-data-root /home/axt/mnt2/jongha/v5_1_glot50010/eval_data_download \
  --coverage-dir docs/exp/v5.1/3_evaluation/00_coverage \
  --out-dir docs/exp/v5.1/3_evaluation/08_embedding_similarity \
  --max-pairs-per-language 50
```

Run after `v51_random` and `v51_fvt` are ready:

```bash
GPU=0 MODEL_KEYS=v51_random,v51_fvt bash scripts/run_v51_similarity.sh
```
