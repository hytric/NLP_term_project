#!/usr/bin/env python3
"""Readable core logic for the v5.2 initialization variants.

This file is a reporting/reference extract. The runnable production
implementation is `scripts/build_v5_initialized_checkpoint.py`.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Callable

import torch


@dataclass(frozen=True)
class InitContext:
    source_vocab: dict[str, int]
    source_input: torch.Tensor
    source_row_count: int
    specials: set[str]
    unk_token: str
    global_mean: torch.Tensor
    block_means: dict[str, torch.Tensor]
    family_means: dict[str, torch.Tensor]
    token_family_counts: dict[str, Counter[str]]
    tokenize_with_base: Callable[[str], list[str]]


def token_body(piece: str) -> str:
    return piece.replace("\u2581", "").strip()


def piece_to_surface(piece: str) -> str:
    return piece.replace("\u2581", " ")


def surface_length(piece: str) -> int:
    return max(1, len(token_body(piece)))


def valid_source_id(piece: str, ctx: InitContext) -> int | None:
    idx = ctx.source_vocab.get(piece)
    if idx is None or not (0 <= idx < ctx.source_row_count):
        return None
    if piece in ctx.specials or piece == ctx.unk_token or piece.startswith("<0x"):
        return None
    if not token_body(piece):
        return None
    return idx


def fvt_vector(target_piece: str, ctx: InitContext) -> torch.Tensor | None:
    source_ids = [
        idx
        for source_piece in ctx.tokenize_with_base(piece_to_surface(target_piece))
        if (idx := valid_source_id(source_piece, ctx)) is not None
    ]
    if not source_ids:
        return None
    return ctx.source_input[source_ids].mean(dim=0)


def weighted_fvt_vector(target_piece: str, ctx: InitContext) -> torch.Tensor | None:
    source_pieces = [
        source_piece
        for source_piece in ctx.tokenize_with_base(piece_to_surface(target_piece))
        if valid_source_id(source_piece, ctx) is not None
    ]
    if not source_pieces:
        return None

    source_ids = [valid_source_id(piece, ctx) for piece in source_pieces]
    weights = torch.tensor(
        [surface_length(piece) for piece in source_pieces],
        dtype=ctx.source_input.dtype,
        device=ctx.source_input.device,
    )
    vectors = ctx.source_input[source_ids]
    return (vectors * weights.unsqueeze(1)).sum(dim=0) / weights.sum()


def align_vector(target_piece: str, unicode_block: str, ctx: InitContext) -> torch.Tensor:
    vector = fvt_vector(target_piece, ctx)
    if vector is not None:
        return vector
    return ctx.block_means.get(unicode_block, ctx.global_mean)


def family_mean_vector(target_piece: str, ctx: InitContext) -> torch.Tensor:
    family_counts = ctx.token_family_counts.get(target_piece, Counter())
    usable = [(family, count) for family, count in family_counts.items() if family in ctx.family_means]
    if not usable:
        return ctx.global_mean

    vectors = torch.stack([ctx.family_means[family] for family, _ in usable], dim=0)
    weights = torch.tensor(
        [count for _, count in usable],
        dtype=vectors.dtype,
        device=vectors.device,
    )
    return (vectors * weights.unsqueeze(1)).sum(dim=0) / weights.sum()


def initialize_new_row(mode: str, target_piece: str, unicode_block: str, ctx: InitContext) -> torch.Tensor:
    if mode == "mean":
        return ctx.global_mean
    if mode == "fvt":
        vector = fvt_vector(target_piece, ctx)
        return vector if vector is not None else ctx.global_mean
    if mode == "weighted_fvt":
        vector = weighted_fvt_vector(target_piece, ctx)
        return vector if vector is not None else ctx.global_mean
    if mode == "align":
        return align_vector(target_piece, unicode_block, ctx)
    if mode == "family_mean":
        return family_mean_vector(target_piece, ctx)
    raise ValueError(f"unsupported readable core mode: {mode}")
