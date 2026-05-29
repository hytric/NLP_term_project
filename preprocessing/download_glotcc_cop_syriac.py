#!/usr/bin/env python
"""Fetch languages from cis-lmu/GlotCC-V1 (public CommonCrawl web text) that are
NOT in Glot500-C, and save them in the data/raw/{lang}_{script}/ DatasetDict layout
merge_files.py expects (a 'train' split with a 'text' column).

Used for Coptic (cop_Copt) and Classical Syriac (syc_Syrc), which Glot500-C lacks.
Each GlotCC 'content' document is split into non-empty lines, one per row, and the
'content' column is renamed to 'text'.

    python download_glotcc.py
"""
import argparse
import glob
import os

import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import snapshot_download

# GlotCC config name (hyphen) -> data/raw dir name (underscore, as merge_files.py expects)
LANGS = {
    "cop-Copt": "cop_Copt",
    "syc-Syrc": "syc_Syrc",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir",   default="/disk3/moon/Glot500/data/raw")
    ap.add_argument("--cache_dir", default="/disk3/moon/Glot500/cache/hf_datasets")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    for gcc, out_name in LANGS.items():
        snap = snapshot_download(
            repo_id="cis-lmu/GlotCC-V1", repo_type="dataset",
            allow_patterns=[f"v1.0/{gcc}/*"], cache_dir=args.cache_dir,
        )
        pqs = sorted(glob.glob(os.path.join(snap, "v1.0", gcc, "*.parquet")))
        lines, ndocs = [], 0
        for pq in pqs:
            df = pd.read_parquet(pq, columns=["content"])
            ndocs += len(df)
            for doc in df["content"]:
                for ln in str(doc).split("\n"):
                    ln = ln.strip()
                    if ln:
                        lines.append(ln)
        out_path = os.path.join(args.out_dir, out_name)
        DatasetDict({"train": Dataset.from_dict({"text": lines})}).save_to_disk(out_path)
        print(f"{out_name:10} docs={ndocs:>6}  lines(rows)={len(lines):>8}  -> {out_path}")


if __name__ == "__main__":
    main()
