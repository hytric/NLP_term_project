# v5 External Source Verification

Last checked: 2026-06-28

This note records primary-source checks for the report/PPT bibliography and
method-lineage claims. It is not evidence for v5 numeric results; those must
come from local artifacts and aggregation outputs.

Primary-source metadata for the Yamaguchi et al. vocabulary-expansion paper
was rechecked against ACL Anthology on 2026-06-28: title, authors,
Computational Linguistics 52(1), pages 295-330, and DOI `10.1162/coli.a.581`
match the local BibTeX and report/PPT citation maps.

## Verified Sources

| Key | Primary source | Verified metadata | v5 usage boundary |
| --- | --- | --- | --- |
| `imanigooghari-etal-2023-glot500` | ACL Anthology: `https://aclanthology.org/2023.acl-long.61/` | ACL 2023 long paper, pages 1082-1117, DOI `10.18653/v1/2023.acl-long.61` | Original Glot500 target and metric-family lineage. Cite for motivation and method surface, not as proof that v5 reruns the full 511-language experiment. |
| `glot500-code` | Official code repository: `https://github.com/cisnlp/Glot500` | Repository linked as Glot500 implementation lineage | Cite for inherited script/evaluation lineage. Local v5 wrappers and artifacts remain the reproducibility proof. |
| `yamaguchi-etal-2026-effectively` | ACL Anthology: `https://aclanthology.org/2026.cl-1.9/` | Computational Linguistics 52(1), pages 295-330, DOI `10.1162/coli.a.581` | Vocabulary-expansion and new-token adaptation inspiration/contrast. Do not call v5 tokenizer itself Yamaguchi-style; v5 tokenizer is Glot500-style SPM append. |
| `lowres-cve-code` | Official code repository: `https://github.com/gucci-j/lowres-cve` | Repository for low-resource continued vocabulary expansion code | Cite as related implementation context only; it is not the executed v5 pipeline. |

## Yamaguchi Lineage Note

The paper meant by the local shorthand `Yamaguchi-style` is Yamaguchi,
Villavicencio, and Aletras, "How Can We Effectively Expand the Vocabulary of
LLMs with 0.01GB of Target Language Text?" Computational Linguistics 52(1),
2026. The ACL page describes the work as low-resource vocabulary expansion
that studies embedding initialization methods and continual pre-training
strategies using about 30K target-language sentences.

For v5, use this citation only to motivate the vocabulary-expansion and
new-row initialization question. The executed main tokenizer is still the
Glot500-style SentencePiece append route, and the final method comparison is
`v5_random` vs `v5_fvt` under the local v5 corpus/tokenizer/training contract.

## Glot500 Lineage Note

The original Glot500 ACL 2023 paper reports a continued-pretraining effort over
511 predominantly low-resource languages and evaluates on multiple task
families. v5 cites this paper for the experimental surface and metric-family
lineage, while explicitly limiting its own scope to the controlled 92+10
language-script subset.

## Report And PPT Rules

- Use `Glot500-style controlled subset replay`, not `full Glot500 reproduction`.
- Use `Yamaguchi-style inspiration/contrast` for the V3/add-token framing and
  low-resource vocabulary-expansion motivation.
- Use `source-token decomposition initialization` for the v5 novelty method.
- Pair every cited method claim with local v5 evidence when moving from
  background to result claims.
- Do not cite external papers as proof of v5 numeric values; use `00_tables/`,
  `3_evaluation/09_aggregation/`, and generated audits.

## Source-To-Claim Placement

| Report/PPT location | Citation use | Required local companion |
| --- | --- | --- |
| Introduction and related work | Glot500 motivation; vocabulary-expansion motivation | `claim_ledger.md`; `citation_source_map.md` |
| Tokenizer method section | Glot500-style SPM append lineage and Yamaguchi-style contrast | tokenizer audit tables; `Report.md` method distinction |
| Novelty section | Yamaguchi-style motivation for embedding initialization | initialization audit and zero-step summary |
| Evaluation section | Glot500 metric-family retention | `metric_mapping.md`; `table_13_metric_fidelity_matrix.md` |
| Conclusion | citations only for lineage, not outcome | `final_claim_decision_tree.md`; parsed aggregation rows |
