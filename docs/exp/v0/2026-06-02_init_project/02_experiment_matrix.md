# Experiment Matrix

이 파일은 실험을 "논문화 가능한 비교"로 유지하기 위한 기록판이다.
각 실험은 반드시 hypothesis, control, metric, expected observation을 채워야 한다.

## 1. Baseline Ladder

| ID | Experiment | Purpose | Status | Primary Metrics | Notes |
| --- | --- | --- | --- | --- | --- |
| T0 | Existing Glot500 tokenizer audit | vocab extension 필요성 증명 | planned | fertility, seq length, single-char ratio | Coptic/Syriac 샘플 필요 |
| T1 | Existing NLLB tokenizer audit | NLLB baseline의 tokenizer bottleneck 확인 | planned | fertility, seq length, single-char ratio | NLLB tokenizer 비교 |
| V0 | No vocabulary extension | 약한 baseline | planned | MLM loss, BLEU, chrF++ | 그대로 학습하면 얼마나 나쁜지 확인 |
| V1 | Joint Coptic+Syriac unigram extension | 기본 vocab extension | planned | tokenization metrics | vocab size ablation 포함 |
| E0 | Random embedding init | initialization lower bound | planned | MLM loss curve, chrF++ | 실패해도 중요한 baseline |
| E1 | Mean embedding init | 구현 쉬운 강한 baseline | planned | MLM loss curve, chrF++ | constituent subtoken 평균 |
| E2 | Align embedding init | novelty 후보 | planned | MLM loss curve, chrF++ | character-span alignment 필요 |
| P0 | Target-only continued pretraining | target adaptation 효과 | planned | pseudo-ppl, forgetting | Coptic/Syriac만 사용 |
| P1 | Target + Glot500-mixed pretraining | forgetting-aware adaptation | planned | pseudo-ppl, forgetting | alpha=0.3 sampling 검토 |
| N0 | Pivot-only translation | direct data 부족 조건 baseline | planned | BLEU, chrF++ | Coptic->Greek/English->Syriac |
| N1 | Direct-only NMT | direct pair lower bound | planned | BLEU, chrF++ | direct data가 충분하지 않을 가능성 |
| N2 | Multitask pivot NMT | auxiliary pair 효과 | planned | BLEU, chrF++ | Coptic/Greek/English/Syriac |
| N3 | Back-translation round 1 | synthetic data 효과 | planned | BLEU, chrF++ | monolingual Coptic/Syriac 활용 |
| N4 | Back-translation round 2 | iteration 효과 | planned | BLEU, chrF++ | overfitting/quality drift 주의 |

## 2. Tokenization Audit Template

| Tokenizer | Language | Avg chars | Avg tokens | Fertility | Single-char token % | Unknown/fallback % | Example issue |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Glot500-m | Coptic | TBD | TBD | TBD | TBD | TBD | TBD |
| Glot500-m | Syriac | TBD | TBD | TBD | TBD | TBD | TBD |
| NLLB | Coptic | TBD | TBD | TBD | TBD | TBD | TBD |
| NLLB | Syriac | TBD | TBD | TBD | TBD | TBD | TBD |
| New unigram | Coptic | TBD | TBD | TBD | TBD | TBD | TBD |
| New unigram | Syriac | TBD | TBD | TBD | TBD | TBD | TBD |

## 3. Embedding Initialization Template

| Init | Data size | Train strategy | Validation loss | Pseudo-ppl | BLEU | chrF++ | Observation |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| Random | 5K | target-only | TBD | TBD | TBD | TBD | TBD |
| Mean | 5K | target-only | TBD | TBD | TBD | TBD | TBD |
| Align | 5K | target-only | TBD | TBD | TBD | TBD | TBD |
| Random | 30K | mixed | TBD | TBD | TBD | TBD | TBD |
| Mean | 30K | mixed | TBD | TBD | TBD | TBD | TBD |
| Align | 30K | mixed | TBD | TBD | TBD | TBD | TBD |

## 4. Continued Pretraining Template

| ID | Init | Train data | Update method | Sampling | Target metric | Forgetting metric | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | Mean | Coptic+Syriac | full | target-only | TBD | TBD | TBD |
| P1 | Mean | Coptic+Syriac+Glot500 sample | full | alpha=0.3 | TBD | TBD | TBD |
| P2 | Align | Coptic+Syriac | LoRA/hybrid | target-only | TBD | TBD | TBD |
| P3 | Align | Coptic+Syriac+Glot500 sample | LoRA/hybrid | alpha=0.3 | TBD | TBD | TBD |

## 5. NMT Evaluation Template

| Model | Training data | Direction | BLEU | chrF++ | Qualitative summary | Failure pattern |
| --- | --- | --- | ---: | ---: | --- | --- |
| Pivot-only | Coptic-Greek, Greek-Syriac | cop->syc | TBD | TBD | TBD | TBD |
| Pivot-only | Syriac-Greek, Greek-Coptic | syc->cop | TBD | TBD | TBD | TBD |
| Direct-only | Coptic-Syriac | cop->syc | TBD | TBD | TBD | TBD |
| Direct-only | Syriac-Coptic | syc->cop | TBD | TBD | TBD | TBD |
| Multitask | direct + pivot | cop->syc | TBD | TBD | TBD | TBD |
| Multitask | direct + pivot | syc->cop | TBD | TBD | TBD | TBD |
| Backtranslation R1 | direct + pivot + synthetic | cop->syc | TBD | TBD | TBD | TBD |
| Backtranslation R1 | direct + pivot + synthetic | syc->cop | TBD | TBD | TBD | TBD |

## 6. Data Inventory Template

| Source | Language | Type | Expected size | Parallel with | License | Redistributable | Quality risk | Next action |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| Coptic Scriptorium | Coptic | monolingual/annotated | TBD | Greek/English? | TBD | TBD | TEI parsing | Check access |
| Sahidica | Coptic | parallel Bible | TBD | English | TBD | TBD | verse alignment | Check download |
| Coptic Bible | Coptic | parallel Bible | TBD | Greek/English | TBD | TBD | dialect variance | Check source |
| Peshitta | Syriac | parallel Bible | TBD | English/Greek | TBD | TBD | verse segmentation | Check source |
| SEDRA | Syriac | monolingual/lexical | TBD | English? | TBD | TBD | access/license | Check access |
| CAL | Syriac/Aramaic | monolingual | TBD | none | TBD | TBD | language mixture | Check source |
| Tatoeba | Syriac | parallel sentences | TBD | English | CC BY/CC0 mix | TBD | small/noisy | Query |
| OPUS/Bible corpus | Coptic/Syriac | parallel Bible | TBD | many | TBD | TBD | version mismatch | Query |

## 7. Decision Log

| Date | Decision | Evidence | Alternative rejected | Follow-up |
| --- | --- | --- | --- | --- |
| 2026-06-03 | Start with Glot500-m centered research plan | Course guide recommends Glot500 when unseen target languages make NLLB advantage weaker; repo already contains Glot500 tooling | NLLB-only project | Keep NLLB as baseline |

## 8. Paper Claim Tracker

| Claim | Required evidence | Current status |
| --- | --- | --- |
| Coptic/Syriac are unsupported or poorly tokenized by existing models | tokenizer audit + coverage check | not started |
| Academic sources can reach useful data scale | data inventory + sentence counts | not started |
| Mean/Align initialization improves low-resource adaptation | controlled init ablation | not started |
| Mixed training reduces forgetting | target-only vs mixed comparison | not started |
| Pivot/back-translation improves NMT | NMT ablation | not started |
