# Task 2. Sentence Retrieval

작성일: 2026-06-19

## Task 정의

Sentence Retrieval은 서로 다른 언어의 aligned sentence 또는 Bible verse가 encoder embedding space에서 가까운지 보는 평가다.

Glot500의 Tatoeba/Bible sentence retrieval evaluation에 가장 직접적으로 대응된다.

## 데이터/설정

현재 사용할 수 있는 retrieval-style 평가는 두 가지다.

1. v3.1 translation split 기반 Coptic-Syriac retrieval
2. target10 MLM-dev feature cache 기반 전체 `90` directed language pairs retrieval

주요 설정:

- representation: mean-pooled encoder features
- normalization: L2 normalization
- score types: `raw_cosine`, `centered_cosine`, `csls_k10`, `centered_csls_k10`
- metrics: aligned score, hard margin, Recall@1/5, MRR, hubness@10

## 결과

Target10-wide centered-CSLS 주요 결과:

`xlmr_base`는 report-ready 비교 표에서 제외한다. 이유는 pseudoPPL에서 확인한 것처럼 target10의 일부 script에서 base tokenizer/representation이 `▁`/punctuation 중심으로 degenerate해질 수 있고, expanded-tokenizer `mlm200` variants와 같은 조건의 retrieval representation으로 보기 어렵기 때문이다. Raw artifact에는 transparency를 위해 남겨두지만, 최종 해석은 `mlm200` variants 내부 비교만 사용한다.

| Model | Score | Margin | R@1 | R@5 | R@10 | MRR | Hubness@10 max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `random_mlm200` | `centered_csls_k10` | `-0.563356` | `0.012318` | `0.041759` | `0.068257` | `0.036425` | `0.077437` |
| `mean_mlm200` | `centered_csls_k10` | `-0.637304` | `0.010675` | `0.038409` | `0.065668` | `0.034450` | `0.084290` |
| `align_mlm200` | `centered_csls_k10` | `-0.473661` | `0.009456` | `0.034559` | `0.058497` | `0.031894` | `0.087349` |
| `focus_mlm200` | `centered_csls_k10` | `-0.516167` | `0.008680` | `0.033440` | `0.057186` | `0.030713` | `0.085429` |
| `fvt_mlm200` | `centered_csls_k10` | `-0.480777` | `0.008798` | `0.032826` | `0.057600` | `0.030593` | `0.088414` |

Coptic-Syriac centered-CSLS 결과:

기존 baseline-vs-candidate delta는 raw diagnostic으로만 둔다. `xlmr_base` baseline을 직접 비교 대상으로 쓰지 않기 위해, report-ready 표에서는 candidate absolute score만 남긴다.

| Direction | Score type | Candidate MRR | Candidate hubness@10 max | 해석 |
| --- | --- | ---: | ---: | --- |
| `cop -> syr` | `centered_csls_k10` | `0.0219` | `0.1057` | weak retrieval signal |
| `syr -> cop` | `centered_csls_k10` | `0.0220` | `0.0418` | weak retrieval signal |

## Glot500 기존 결과와 비교

Glot500의 sentence retrieval은 현재 v3.1 proxy와 직접 같은 실험이 아니다.

Glot500 setup:

- Tatoeba/Bible의 English-aligned sentence retrieval
- layer 8 average word embeddings
- cosine nearest neighbor
- metric: Top-10 accuracy

v3.1 setup:

- target10 Bible/dev feature cache 기반 low-resource-to-low-resource directed pairs
- mean-pooled encoder features
- centered-CSLS score
- metric: R@1/R@5/R@10/MRR
- `xlmr_base`는 report-ready 비교에서 제외

따라서 아래 표는 apples-to-apples 비교가 아니라 scale comparison이다.

| Evaluation | Metric | XLM-R-B tail | Glot500-m tail | Glot500-m all | v3.1 proxy best |
| --- | --- | ---: | ---: | ---: | ---: |
| Glot500 Sentence Retrieval Tatoeba | Top-10 acc | `32.6%` | `59.8%` | `70.7%` | `NA` |
| Glot500 Sentence Retrieval Bible | Top-10 acc | `7.4%` | `43.2%` | `47.3%` | `NA` |
| v3.1 target10 Bible/dev proxy | R@10 | `NA` | `NA` | `NA` | `6.83%` |

Glot500의 Bible tail Top-10은 XLM-R-B `7.4%`에서 Glot500-m `43.2%`까지 올라간다. 반면 v3.1 target10 proxy의 최고 R@10은 `random_mlm200`의 `6.83%`다. 즉, metric과 dataset이 다르다는 점을 감안해도 현재 retrieval proxy는 Glot500-m 수준의 sentence retrieval evidence와 거리가 멀다.

이 차이는 다음 이유로 자연스럽다.

- v3.1은 Glot500-scale retrieval evaluation이 아니라 small proxy다.
- target10 low-resource-to-low-resource pair는 Glot500의 English-aligned retrieval보다 더 불안정할 수 있다.
- Bible/dev cache는 domain과 item 수가 제한적이다.
- 현재 MLM 자체도 content-token prediction을 충분히 확보하지 못했다.
- `xlmr_base` tokenizer/representation 문제 때문에 base-vs-candidate improvement claim을 쓰지 않는다.

## 해석

CSLS/centering은 raw cosine scoring의 hubness를 크게 줄이는 calibration 역할을 한다. 단, 이것은 model-level improvement 증거가 아니라 scoring diagnostic이다. 최종 model comparison은 `xlmr_base`를 제외한 `mlm200` variants 내부 비교로 제한한다. 이 기준에서 target10-wide centered-CSLS MRR은 `random_mlm200`이 가장 높고, 그다음이 `mean_mlm200`이다.

중요한 구분:

> 여기서 `mean_mlm200`이 상위권이라는 말은 **Sentence Retrieval의 centered-CSLS MRR 기준**이다. **MLM dev loss / pseudoPPL 기준에서는 `mean`이 가장 나쁘다.** 따라서 `mean`이 token prediction에 좋다는 뜻으로 해석하면 안 된다.

하지만 absolute retrieval은 여전히 약하다.

- target10-wide R@1은 약 `0.9%`-`1.2%` 수준이다.
- target10-wide R@10도 최고 `6.83%` 수준이다.
- hard margin은 여전히 음수다.
- dynamic MLM loss에서 가장 좋았던 `fvt`가 retrieval에서는 가장 좋지 않다.

## 주장 가능 범위

가능:

> Target10-wide centered CSLS는 `mlm200` variants 내부에서 hubness-calibrated retrieval diagnostic 차이를 보여주지만, absolute retrieval은 weak signal 수준이다.

불가능:

> `xlmr_base` 대비 우월성을 이 표로 주장할 수 없다. adapted encoder가 robust target10 sentence retrieval을 달성했다고도 주장할 수 없다.

## 산출물

| Artifact | 용도 |
| --- | --- |
| `../target10_sentence_retrieval_csls_scores.tsv` | target10 per-direction CSLS scores |
| `../target10_sentence_retrieval_csls_summary.tsv` | raw target10 macro summary, includes `xlmr_base` and zero-step diagnostics |
| `../target10_sentence_retrieval_csls_summary_mlm200_only.tsv` | report-ready target10 centered-CSLS summary excluding `xlmr_base` |
| `../target10_sentence_retrieval_csls_results.md` | short report |
| `../../01_embedding_alignment/results.md` | Coptic-Syriac retrieval/CSLS result |
| `../../04_ablation/init_mlm_probe/feature_similarity_results.md` | target10 raw feature similarity |
