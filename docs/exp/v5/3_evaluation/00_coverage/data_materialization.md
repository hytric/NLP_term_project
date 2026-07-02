# v5 Evaluation Data Materialization

Last updated: 2026-06-27 06:45 KST

## Data Root

`evaluation/download_data/download` is a symlink to the mnt2-backed data root:

```text
/home/axt/mnt2/jongha/v5_glot50010/eval_data_download
```

This keeps large downstream data and HuggingFace caches off the root
partition.

HuggingFace cache for evaluation downloads:

```text
/home/axt/mnt2/jongha/v5_glot50010/hf_cache_eval
```

## Launch

Current detached materialization command:

```bash
cd /home/axt/jongha/Glot500-py39-eval/evaluation/download_data
PYTHON_BIN=python3 \
DOWNLOAD_DIR=/home/axt/mnt2/jongha/v5_glot50010/eval_data_download \
HF_HOME=/home/axt/mnt2/jongha/v5_glot50010/hf_cache_eval \
HF_DATASETS_CACHE=/home/axt/mnt2/jongha/v5_glot50010/hf_cache_eval/datasets \
bash download_data.sh
```

Materialization log:

```text
/home/axt/mnt2/jongha/v5_glot50010/logs/eval_data_download_20260627_015540_panx_tner.log
```

## Important Fix

The inherited script originally invoked `python`, which is unavailable in the
current environment. It now supports:

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
```

so the same script works in Python-3-only environments.

PAN-X / WikiAnn also required a HuggingFace dataset source fix. The default
`wikiann` and `unimelb-nlp/wikiann` sources expose only the `ace` config in the
local `datasets==2.7.1` environment. Bypassing split verification made the files
write, but produced wrong data: non-`ace` files such as `af-train` contained
Acehnese text with only the prefix changed. Those failed attempts were moved
aside under:

```text
/home/axt/mnt2/jongha/v5_glot50010/eval_data_download/panx_dataset.failed_*
/home/axt/mnt2/jongha/v5_glot50010/eval_data_download/panx_dataset.wrong_default_wikiann_*
```

The downloader now defaults to `tner/wikiann`, which exposes 176 language
configs in this environment. It also handles the T-NER WikiAnn tag mapping:

```text
0=B-LOC, 1=B-ORG, 2=B-PER, 3=I-LOC, 4=I-ORG, 5=I-PER, 6=O
```

Smoke check passed for `af`, `ace`, and `fur`: the output files contain
different language text and valid BIO tags.

## Current Materialization Status

| Dataset | Status | Coverage effect |
| --- | --- | --- |
| Tatoeba retrieval | materialized | `retrieval_tatoeba` coverage increased to `63/102`, target10 remains `0/10` |
| PAN-X / NER | materialized with `tner/wikiann` | `ner` coverage increased to `78/102`, target10 remains `0/10` |
| UD-POS | materialized after a local networkx-3 compatibility patch | `pos` coverage increased to `58/102`, target10 remains `0/10` |
| Taxi1500 | English split present | `text_classification` coverage `1/102`, target10 `0/10` |
| Bible retrieval | materialized | `retrieval_bible` coverage increased to `74/102`, target10 remains `0/10`; XLM-R and Glot500-base rows are measured |
| Roundtrip alignment | not materialized | `roundtrip_alignment/` directory is absent under the v5 eval-data symlink; class/demo exists but no batch runner/input set is materialized |

UD-POS compatibility note:

- The bundled `ud-conversion-tools` code assumed older NetworkX APIs:
  `graph.node`, positional attribute dicts, and dict-like `bfs_successors`.
- `evaluation/download_data/third_party/ud-conversion-tools/lib/conll.py` now
  has a small Python-3/NetworkX-3 compatibility patch so conversion can write
  `udpos/` files.

## Monitoring

```bash
pgrep -af 'download_data.sh|download_panx_hf.py|utils_preprocess.py|curl -L|ud-conversion'
tail -n 120 /home/axt/mnt2/jongha/v5_glot50010/logs/eval_data_download_20260627_015540_panx_tner.log
python3 scripts/audit_v5_eval_coverage.py
```

Latest checked snapshot:

- active downloader: none
- normalized PAN-X/NER files under `ner/`: `520`
- normalized UD-POS files under `udpos/`: `47`
- local coverage after refresh: NER `78/102`, POS `58/102`

Metric filesystem snapshot, checked from the current filesystem:

```bash
test -d evaluation/download_data/download/retrieval_bible && echo present
test -d evaluation/download_data/download/roundtrip_alignment || echo missing
wc -l evaluation/retrieval/bible_lang_list.txt
```

Observed state:

- `evaluation/download_data/download/retrieval_bible`: present with 148 materialized source/English files for 74 language-scripts.
- `evaluation/download_data/download/roundtrip_alignment`: missing.
- `evaluation/retrieval/bible_lang_list.txt`: `369` rows.

Bible retrieval is unlocked for available-language evaluation. The remaining
Bible work is to run the v5 model rows after matched checkpoints exist and
post-checkpoint preflight is ready-to-launch.
Roundtrip can be unlocked only after a multilingual parallel input set and a
thin v5 batch runner around `RoundTripEvaluator` are added.
