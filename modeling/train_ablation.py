#!/usr/bin/env python
"""Single-GPU launcher for the NO-VOCABULARY-EXTENSION ablation.

Companion to train_base.py. Setup is identical EXCEPT this omits --tokenizer_name,
so run.py loads xlm-roberta-base's ORIGINAL tokenizer (len(tokenizer) == embedding
size). That makes run.py skip resize_token_embeddings, so the model is
continued-pretrained on the same corpus with the ORIGINAL vocabulary -- no new
SentencePiece pieces, no embedding surgery.

Compare its downstream results against train_base.py (the vocabulary-extended run)
to isolate the effect of vocabulary extension vs. continued pretraining alone.

    python train_ablation.py
    python train_ablation.py --max_train_samples 100 --num_train_epochs 1   # smoke test

Keep train_file / batch / accum / epochs IDENTICAL to train_base.py so the only
difference vs. the main run is the absence of vocabulary extension.
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
    # NO --tokenizer_name on purpose: keeps XLM-R's original vocab (the ablation).
    "--output_dir",       f"{DATA_ROOT}/runs/glot500-base-ablation-novocab",
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

    from run import main
    main()
