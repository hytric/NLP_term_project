# Stage 05: Report Package

작성일: 2026-06-19

## Goal

Package `v3.2` results into a claim-safe report.

The report must make clear whether `v3.2` solved:

1. content-token language modeling;
2. sentence-level semantic retrieval;
3. downstream task transfer;
4. translation/generation collapse.

These are separate claims.

## Required Report Sections

1. V3.1 failure recap.
2. Tokenizer/content-token repair decision.
3. Target-balanced MLM result.
4. Semantic alignment result.
5. Downstream and translation diagnostics.
6. Claim/evidence map.
7. Limitations and next work.

## Claim Evidence Map

Required output:

`claim_evidence_map.md`

Template:

| Claim | Required Evidence | Status | Notes |
| --- | --- | --- | --- |
| content-token MLM improves | fixed-mask content-token top-k/gold-prob improves | pending | report worst-language scores |
| sentence retrieval improves | centered-CSLS R@1/MRR/margin improves | pending | report `syr/cop` separately |
| downstream improves | pair/POS/retrieval diagnostics improve | pending | avoid shortcut overclaim |
| translation quality improves | decoder and retrieval baselines improve without collapse | pending | BLEU/chrF++ plus qualitative examples |

## Final Status Labels

Use one:

- `PASS_CONTENT_AND_ALIGNMENT`
- `PASS_CONTENT_ONLY`
- `PASS_ALIGNMENT_ONLY`
- `DOWNSTREAM_ONLY`
- `FAIL`

## Exit Gate

`REPORT_READY` if:

- every table has a source artifact;
- `xlmr_base` pseudoPPL is not used as direct expanded-tokenizer quality comparison;
- content-token and retrieval claims are separated;
- limitations explicitly mention remaining weak languages and scale gap.

