# v5 Citation Source Map

Last updated: 2026-06-27

This file maps report claims to bibliography entries and external source
boundaries. Use it when finalizing related work, introduction, method framing,
and defense slides.

Primary-source metadata and wording locks are checked in
`external_source_verification.md`.

## Primary Citations

| Citation key | Source | Used for | Claim boundary |
| --- | --- | --- | --- |
| `imanigooghari-etal-2023-glot500` | ACL Anthology: `https://aclanthology.org/2023.acl-long.61/` | Glot500 reproduction target, metric-family surface, multilingual scaling motivation | Cite as the original Glot500 paper; do not imply v5 reruns the full 511-language scale |
| `glot500-code` | Glot500 official code: `https://github.com/cisnlp/Glot500` | inherited script structure, tokenizer/evaluation implementation lineage | Cite as code lineage; local v5 paths and wrappers remain the actual reproducibility evidence |
| `yamaguchi-etal-2026-effectively` | ACL Anthology: `https://aclanthology.org/2026.cl-1.9/` | low-resource continued vocabulary expansion framing and motivation for new-row initialization | Use as inspiration/contrast; v5 main tokenizer is Glot500-style SentencePiece append, not the earlier add-token route |
| `lowres-cve-code` | Low-resource CVE official code: `https://github.com/gucci-j/lowres-cve` | vocabulary-expansion implementation reference and terminology bridge | Cite only for related-code context; do not treat as the executed v5 pipeline |

## Report Claim Mapping

| Report/PPT claim | Citation support | Local evidence that must accompany it |
| --- | --- | --- |
| Glot500 motivates multilingual vocabulary/corpus scaling | `imanigooghari-etal-2023-glot500` | v5 scope boundary in `claim_ledger.md` and `paper_draft.md` |
| v5 is a controlled Glot500-style subset replay | `imanigooghari-etal-2023-glot500`; `glot500-code` | merge report, tokenizer audit, `table_13_metric_fidelity_matrix.md` |
| Yamaguchi-style vocabulary expansion motivates low-resource new-token adaptation | `yamaguchi-etal-2026-effectively`; `lowres-cve-code` | tokenizer-method distinction in `Report.md` and `paper_draft.md` |
| v5 novelty is source-token decomposition initialization for appended rows | related to `yamaguchi-etal-2026-effectively`, but primarily a v5 method claim | initialization reports, zero-step summary, and matched after-MLM results when available |
| downstream metrics are retained rather than omitted | `imanigooghari-etal-2023-glot500`; `glot500-code` | metric mapping, coverage files, table 13, blocked-data notes |

## Wording Locks

- Say `Glot500-style controlled subset replay`, not `full Glot500 reproduction`.
- Say `Yamaguchi-style inspiration/contrast` for the earlier add-token route.
- If asked which paper this refers to, answer: Yamaguchi, Villavicencio, and
  Aletras (Computational Linguistics 2026), "How Can We Effectively Expand the
  Vocabulary of LLMs with 0.01GB of Target Language Text?"
- Say `source-token decomposition initialization` for the v5 novelty method.
- Use local artifacts, not citations alone, as proof for measured v5 results.
