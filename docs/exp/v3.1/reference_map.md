# V3.1 Reference Map

작성일: 2026-06-18

## Local References

| Reference | Use in v3.1 |
| --- | --- |
| `docs/exp/v3/final_goal_20260613.md` | Positive claim 조건과 현재 blockers를 유지한다. |
| `docs/exp/v3/final_diagnostic_report_20260613.md` | v3 실패 원인: high-resource collapse, sparse downstream coverage, tokenizer-to-model gap. |
| `docs/exp/v3/positive_route_survey_methodology_20260618.md` | broad target10 positive route, classification/retrieval preference, embedding map idea. |
| `docs/exp/v3/10_embedding_alignment_downstream/plan.md` | v3.1의 직접 선행 계획. |
| `docs/exp/v3/08_ablation/ablation_matrix.tsv` | 기존 first/second try와 diagnostic probes를 ablation으로 배치하는 기준. |
| `docs/survey/2305.12182v2.pdf` | Glot500 evaluation: layer 8 retrieval/alignment, Taxi1500, POS/NER, Bible/Tatoeba sentence retrieval. |
| `docs/survey/2406.11477v3.pdf` | low-resource vocabulary expansion, initialization and continued-pretraining strategy. |
| `docs/survey/GLOT500_extension.pdf` | Coptic/Syriac extension tutorial, sampling/replay, full fine-tuning vs LoRA context. |
| `docs/survey/termProjectGuideLine.pdf` | report deliverables: quantitative evaluation, qualitative analysis, ablation studies, low-resource translation framing. |
| `docs/survey/vocab_extension_tutorial.pdf` | vocabulary extension pitfalls, Mean/FVT/Wechsel/Focus/Ofa, CSLS/hubness, evaluation milestones. |
| `docs/survey/unigramLM.pdf`, `docs/survey/BEP_WordPiece.pdf` | tokenizer background for any tokenizer ablation writeup. |

## Method Decisions Imported From References

| Decision | Source basis | v3.1 interpretation |
| --- | --- | --- |
| Use XLM-R-base as mandatory baseline | v3 final goal and XLM-R/Glot500 framing | Every embedding/downstream metric compares to XLM-R-base. |
| Use layer 8 as default embedding layer | Glot500 SentRetr/SimAlign evaluation | Alignment/retrieval defaults to mean-pooled layer 8; last layer is ablation. |
| Treat translation retrieval/ranking as encoder-space evidence | XLM-R/Glot500 encoder evaluation style | No free-form NMT claim from alignment/retrieval alone; generation is tested separately in Experiment 3. |
| Use classification as primary broad downstream | Glot500 Taxi1500 and user preference | Taxi1500 or fixed-label Bible topic classification is main downstream candidate. |
| Track hubness | vocab tutorial CSLS/hubness warning | Report hubness@k and optionally CSLS sensitivity, not only raw cosine. |
| Preserve tokenizer ids by append-only merge | vocab extension tutorial and v3 id-preservation rule | Train auxiliary tokenizer on low-resource + high-resource text, then append only new pieces to XLM-R vocab. |
| Add simple decoder only after encoder-space tests | term project translation deliverable and XLM-R encoder-only constraint | Final translation task trains a small decoder with identical setup across baseline/candidate encoders. |
| Keep ablations separate from main gate | v3 ablation policy | Layer/pooling/negative/map/tokenizer/init/training variations are ablations unless predeclared as main. |
| Include qualitative analysis | term project guideline | 2D maps and nearest-neighbor examples accompany numeric metrics. |

## Claim Constraints

Allowed if gates pass:

> Target10 low-resource languages are better aligned in the encoder semantic space than XLM-R-base, and frozen embeddings improve translation retrieval/pair classification and classification transfer.

> A small decoder trained on top of the adapted encoder improves held-out low-resource translation metrics over the same decoder trained on XLM-R-base encoder states.

Not allowed from Experiments 1-2 alone:

> The model generates better translations.

This is allowed only after the simple-decoder translation gate passes; it cannot be inferred from alignment or retrieval alone.

> Tokenizer fragmentation improvement alone caused downstream improvement.

> A visually better 2D map proves broad downstream success.

> Coptic-only or Syriac-proxy-only evidence proves target10-wide improvement.
