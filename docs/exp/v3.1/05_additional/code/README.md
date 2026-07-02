# 05 Additional Code

작성일: 2026-06-19

이 폴더는 `docs/exp/v3.1/05_additional` 결과를 재현하기 위해 사용한 코드 복사본과 실행 명령을 보관한다.

원본 스크립트 위치:

| Local copy | Original source | Purpose |
| --- | --- | --- |
| `run_v31_pseudoperplexity.py` | `modeling/run_v31_pseudoperplexity.py` | sampled pseudo-perplexity / intrinsic MLM evaluation |
| `run_v31_pseudoperplexity_accuracy_samples.py` | `modeling/run_v31_pseudoperplexity_accuracy_samples.py` | top-k/content-token diagnostic for pseudoPPL interpretation |
| `run_v31_target10_csls_feature_similarity.py` | `modeling/run_v31_target10_csls_feature_similarity.py` | target10-wide centered/CSLS sentence retrieval from cached embeddings |

POS 결과는 기존 스크립트 `preprocessing/evaluate_third_try_coptic_pos_metrics.py`를 사용해 v3.1/05_additional 아래로 재집계했다. 해당 스크립트는 공용 preprocessing script라 복사하지 않고 명령만 `run_commands.md`에 기록한다.

## Generated Artifacts

| Task | Main artifacts |
| --- | --- |
| Pseudoperplexity | `../pseudoperplexity_scores.tsv`, `../pseudoperplexity_summary.tsv`, `../pseudoperplexity_accuracy_summary.tsv`, `../pseudoperplexity_gold_probability_scores.tsv`, `../pseudoperplexity_prediction_samples.tsv` |
| Sentence Retrieval | `../target10_sentence_retrieval_csls_scores.tsv`, `../target10_sentence_retrieval_csls_summary.tsv`, `../target10_sentence_retrieval_csls_summary_mlm200_only.tsv` |
| POS | `../coptic_pos_results_replay_safe.tsv`, `../coptic_pos_summary_replay_safe.tsv` |
| Final report | `../method_task_results.md` |

## Notes

- The pseudo-perplexity run is sampled: first `50` dev rows per target10 language.
- The pseudoPPL top-k diagnostic is smaller: first `20` dev rows per target10 language, and includes separate content-token metrics excluding boundary/punctuation effects.
- PseudoPPL is tokenizer-sensitive, so compare expanded-tokenizer `mlm200` variants more safely than comparing absolute values against `xlmr_base`.
- The report-ready sentence retrieval summary also excludes `xlmr_base`; raw TSVs keep it only as a diagnostic row.
- The CSLS script uses existing cached MLM-dev feature embeddings, so it is CPU-only after caches exist.
