#!/usr/bin/env python
"""Single-GPU launcher for Glot500 base pretraining.

Replaces train_base.sh: sets the environment and arguments here, then calls
run.py's main() directly. Launch with:

    python train_base.py                  # full run on GPU 1
    python train_base.py --max_train_samples 100 --num_train_epochs 1   # smoke test

Any extra CLI args are appended and override the baked-in defaults.
Effective batch size: 12 (per-device) x 32 (accum) x 1 (GPU) = 384 (matches upstream).
"""
import os
import sys

# Must be set before torch/transformers import CUDA.
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("WANDB_DISABLED", "true")

DATA_ROOT = "/home/sogang/mnt/db_1/moon/Glot500"

DEFAULT_ARGS = [
    "--model_name_or_path", "xlm-roberta-base",
    "--train_file",       f"{DATA_ROOT}/data/Glot500.txt",
    "--tokenizer_name",   f"{DATA_ROOT}/tokenization/output/Glot500_extended_spm",
    "--output_dir",       f"{DATA_ROOT}/runs/glot500-base",
    "--cache_dir",        f"{DATA_ROOT}/cache",
    "--per_device_train_batch_size", "12",
    "--gradient_accumulation_steps", "8",
    "--fp16", "True",
    "--do_train",
    "--num_train_epochs", "100",
    "--save_steps", "10000",
]

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    # run.py reads sys.argv; argv[0] is the program name, then defaults, then
    # any user overrides (later values win in argparse).
    sys.argv = [sys.argv[0]] + DEFAULT_ARGS + sys.argv[1:]

    from run import main #MJ: import from run.py module
    main()