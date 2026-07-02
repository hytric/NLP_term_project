# Source-Candidate Diagnostics Summary

작성일: 2026-06-04

CPU-only 10A diagnostic over English -> Coptic top8 retrieval candidates. No GPU was used.
The chrF++ values below are sentence-level candidate scores averaged across rows, so they are diagnostic means rather than corpus-level sacrebleu scores.

## Aggregate Metrics

| Metric | Value |
| --- | ---: |
| Test examples | 879 |
| Top1 mean chrF++ | 22.7410 |
| Feature-selected mean chrF++ | 24.7724 |
| Oracle@8 mean chrF++ | 28.9181 |
| Feature-selected gain over top1 | 2.0314 |
| Remaining gap to oracle@8 | 4.1458 |
| Oracle not rank 1 | 663 / 879 |
| Feature-selected rank matches oracle rank | 298 / 879 |
| Large oracle gain >= 5 chrF++ | 436 / 879 |
| Feature-selected gain >= 5 chrF++ | 165 / 879 |
| Feature-selected loss <= -5 chrF++ | 18 / 879 |

## Feature Selector Relation To Top1

| Relation | Count |
| --- | ---: |
| better | 264 |
| tie | 550 |
| worse | 65 |

## Rank Distributions

| Rank | Selected count | Oracle count |
| ---: | ---: | ---: |
| 1 | 550 | 216 |
| 2 | 104 | 135 |
| 3 | 62 | 121 |
| 4 | 41 | 72 |
| 5 | 34 | 84 |
| 6 | 37 | 113 |
| 7 | 28 | 69 |
| 8 | 23 | 69 |

## 10B Diagnostic Labels

| Label | Count |
| --- | ---: |
| AMBIGUOUS | 226 |
| KEEP_TOP1 | 216 |
| REJECT_POOL | 1 |
| SWAP_TO_RANK_2 | 91 |
| SWAP_TO_RANK_3 | 88 |
| SWAP_TO_RANK_4 | 44 |
| SWAP_TO_RANK_5 | 56 |
| SWAP_TO_RANK_6 | 67 |
| SWAP_TO_RANK_7 | 46 |
| SWAP_TO_RANK_8 | 44 |

## Reading

- Feature reranking is useful: it improves mean chrF++ over top1 retrieval and hurts only a small minority of examples.
- The selector is still far from oracle@8, so 10B has real candidate-decision headroom.
- Many examples have a better non-rank1 candidate, which supports a keep/swap/reject framing rather than another direct seq2seq run.
- A future GPU editing pilot should only proceed after using these diagnostics to create labels or controls.
