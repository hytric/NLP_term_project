#!/usr/bin/env python3
"""Fast sentence-retrieval evaluation for v5.2 head languages.

The legacy retrieval evaluators reload the encoder for every source/English
file. That is fine for the 3-language tail set, but too slow for the head
language sweep, so this script keeps one model resident per checkpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

import faiss
import numpy as np
import torch
from tqdm import tqdm
from transformers import XLMRobertaConfig, XLMRobertaModel, XLMRobertaTokenizer


def path_key(value: str) -> str:
    return value.strip("/").replace("/", "__") or value.replace("/", "__")


def parse_languages(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", " ").split() if item.strip()]


def file_digest(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tokenized(text_file: Path, tok_file: Path, tokenizer: XLMRobertaTokenizer) -> list[list[str]]:
    if tok_file.exists() and tok_file.stat().st_size > 0:
        return [line.strip().split(" ") for line in tok_file.read_text(encoding="utf-8").splitlines()]

    tok_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = tok_file.with_suffix(tok_file.suffix + f".tmp.{os.getpid()}")
    sentences: list[list[str]] = []
    with text_file.open(encoding="utf-8") as src, tmp_file.open("w", encoding="utf-8") as out:
        for line in tqdm(src, desc=f"tokenize {text_file.name}", leave=False):
            toks = tokenizer.tokenize(line.strip())
            sentences.append(toks)
            out.write(" ".join(toks) + "\n")
    tmp_file.replace(tok_file)
    return sentences


def prepare_batch(
    sentences: list[list[str]],
    tokenizer: XLMRobertaTokenizer,
    device: torch.device,
    max_length: int,
) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    pad_token_id = tokenizer.convert_tokens_to_ids([tokenizer.pad_token])[0]
    local_max = min(max(len(sent) for sent in sentences) + 2, max_length)
    input_ids = []
    attention = []
    for sent in sentences:
        if len(sent) > local_max - 2:
            sent = sent[: local_max - 2]
        ids = tokenizer.convert_tokens_to_ids([tokenizer.cls_token] + sent + [tokenizer.sep_token])
        padding = local_max - len(ids)
        input_ids.append(ids + [pad_token_id] * padding)
        attention.append([1] * len(ids) + [0] * padding)

    input_tensor = torch.tensor(input_ids, dtype=torch.long, device=device)
    attention_tensor = torch.tensor(attention, dtype=torch.long, device=device)
    token_type_ids = torch.zeros_like(input_tensor)
    return {
        "input_ids": input_tensor,
        "attention_mask": attention_tensor,
        "token_type_ids": token_type_ids,
    }, attention_tensor


def mean_pool(hidden: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    mask_float = mask.unsqueeze(2).float()
    return (hidden * mask_float).sum(dim=1) / mask_float.sum(dim=1).clamp(min=1.0)


def encode(
    sentences: list[list[str]],
    model: XLMRobertaModel,
    tokenizer: XLMRobertaTokenizer,
    device: torch.device,
    batch_size: int,
    max_length: int,
    num_layers: int,
    specific_layer: int,
) -> np.ndarray:
    embeds: list[np.ndarray] = []
    for start in tqdm(range(0, len(sentences), batch_size), desc="encode", leave=False):
        batch_sents = sentences[start : start + batch_size]
        batch, mask = prepare_batch(batch_sents, tokenizer, device, max_length)
        with torch.no_grad():
            outputs = model(**batch)
            hidden_states = outputs["hidden_states"][-num_layers:]
            selected = hidden_states[specific_layer]
            pooled = mean_pool(selected, mask)
        embeds.append(pooled.detach().cpu().numpy().astype(np.float32))
        del batch, mask, outputs, hidden_states, selected, pooled
        if device.type == "cuda":
            torch.cuda.empty_cache()
    return np.vstack(embeds).astype(np.float32)


def similarity_search(src: np.ndarray, tgt: np.ndarray, normalize: bool) -> np.ndarray:
    src = np.ascontiguousarray(src.astype(np.float32))
    tgt = np.ascontiguousarray(tgt.astype(np.float32))
    if normalize:
        faiss.normalize_L2(src)
        faiss.normalize_L2(tgt)
    index = faiss.IndexFlatL2(src.shape[1])
    index.add(src)
    _, pred = index.search(tgt, 10)
    return pred


def evaluate_pair(
    src_embeds: np.ndarray,
    tgt_embeds: np.ndarray,
    normalize: bool,
) -> tuple[float, float, float, np.ndarray]:
    pred = similarity_search(src_embeds, tgt_embeds, normalize=normalize)
    total = pred.shape[0]
    acc1 = sum(1 for idx, row in enumerate(pred) if idx in row[:1]) / total
    acc5 = sum(1 for idx, row in enumerate(pred) if idx in row[:5]) / total
    acc10 = sum(1 for idx, row in enumerate(pred) if idx in row[:10]) / total
    return acc1, acc5, acc10, pred


def load_model(model_name_or_path: str, device: torch.device) -> tuple[XLMRobertaModel, XLMRobertaTokenizer]:
    config = XLMRobertaConfig.from_pretrained(model_name_or_path)
    config.output_hidden_states = True
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name_or_path)
    model = XLMRobertaModel.from_pretrained(model_name_or_path, config=config)
    model.to(device)
    model.eval()
    return model, tokenizer


def data_file(data_dir: Path, task: str, lang: str, side: str) -> Path:
    prefix = "tatoeba" if task == "retrieval_tatoeba" else "bible"
    return data_dir / f"{prefix}.{lang}-eng_Latn.{side}"


def run(args: argparse.Namespace) -> None:
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.token_cache_dir) if args.token_cache_dir else data_dir / path_key(args.model_name_or_path)
    cache_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device(args.device if torch.cuda.is_available() and args.device == "cuda" else "cpu")
    model, tokenizer = load_model(args.model_name_or_path, device)

    languages = parse_languages(args.languages)
    rows = []
    target_embedding_cache: dict[str, np.ndarray] = {}
    with (output_dir / "test_results.txt").open("w", encoding="utf-8") as results:
        for lang in languages:
            src_file = data_file(data_dir, args.task, lang, lang)
            tgt_file = data_file(data_dir, args.task, lang, "eng_Latn")
            if not src_file.exists() or not tgt_file.exists():
                print(f"[skip] missing files for {lang}: {src_file.name} / {tgt_file.name}")
                continue

            src_tok = cache_dir / f"{lang}-eng.tok.{lang}"
            tgt_tok = cache_dir / f"{lang}-eng.tok.eng"
            src_toks = read_tokenized(src_file, src_tok, tokenizer)
            tgt_toks = read_tokenized(tgt_file, tgt_tok, tokenizer)
            if not src_toks or len(src_toks) != len(tgt_toks):
                print(f"[skip] bad pair for {lang}: src={len(src_toks)} tgt={len(tgt_toks)}")
                continue

            print(f"[eval] {args.task} {lang} n={len(src_toks)}")
            tgt_cache_key = file_digest(tgt_file)
            src_embeds = encode(
                src_toks,
                model,
                tokenizer,
                device,
                args.batch_size,
                args.max_seq_length,
                args.num_layers,
                args.specific_layer,
            )
            if tgt_cache_key in target_embedding_cache:
                tgt_embeds = target_embedding_cache[tgt_cache_key]
            else:
                tgt_embeds = encode(
                    tgt_toks,
                    model,
                    tokenizer,
                    device,
                    args.batch_size,
                    args.max_seq_length,
                    args.num_layers,
                    args.specific_layer,
                )
                target_embedding_cache[tgt_cache_key] = tgt_embeds
            acc1, acc5, acc10, pred = evaluate_pair(
                src_embeds,
                tgt_embeds,
                normalize=args.dist == "cosine",
            )

            results.write("=====================\n")
            results.write(f"language={lang}\n")
            results.write(f"Acc1 = {acc1}\n")
            results.write(f"Acc5 = {acc5}\n")
            results.write(f"Acc10 = {acc10}\n")
            results.flush()
            with (output_dir / f"test_{lang}_predictions.txt").open("w", encoding="utf-8") as out:
                for row in pred:
                    out.write(str(row) + "\n")
            rows.append((lang, acc1, acc5, acc10))

    print(f"wrote {len(rows)} language rows to {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=("retrieval_tatoeba", "retrieval_bible"), required=True)
    parser.add_argument("--model-name-or-path", required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--languages", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--max-seq-length", type=int, default=512)
    parser.add_argument("--token-cache-dir", default="")
    parser.add_argument("--num-layers", type=int, default=12)
    parser.add_argument("--specific-layer", type=int, default=7)
    parser.add_argument("--dist", default="cosine")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
