
baseline
dataset
language


1. Tokenizer Audit
- XLM-R base vocab size: 250002
- candidate vocab size: 280851
- appended token 수: 30849
- 기존 token id 변경: 0
- special token id 변경: 0

2. Embedding initialization

random
mean
fvt
align
focus

Glot500 대비 규모:

| Item | Glot500-c / Glot500-m | v3.1 init MLM probe | Ratio |
| --- | ---: | ---: | ---: |
| corpus size | about 600GB | 297.5MB train mixture | `0.0496%`, about `1/2,017` |
| sentence/chunk rows | about 1.5B | 966,152 raw train lines | `0.0644%`, about `1/1,553` |
| per-language threshold | >30K rows/language-script | target10 median train rows 5,280.5 | `17.6%` of threshold |
| released training budget | 480K steps * batch 384 | 200 steps * effective batch 32 | `1/28,800` consumed chunks |

해석: v3.1은 Glot500-scale 재현이 아니라 Glot500의 append-vocab + MLM adaptation idea를 작은 고정 budget에서 검증하는 controlled probe다.

Detailed comparison: `docs/exp/v3.1/04_ablation/init_mlm_probe/glot500_size_comparison.md`.

3. Masked training -> encoder output feature 유사도 측정

이 방향은 맞지만, "MLM loss가 좋아졌다 -> semantic alignment가 좋아졌다"로 바로 주장하면 안 된다.

역할을 분리한다.

- MLM masked prediction: encoder/tokenizer adaptation을 위한 학습 objective.
- MLM dev loss: token prediction proxy. 새 token row와 low-resource text를 모델이 얼마나 잘 설명하는지 본다.
- Encoder output feature similarity: semantic attachment proxy. 같은 의미 문장이 언어/script를 넘어 가까워졌는지 본다.
- Downstream task: proxy가 실제 task signal로 이어지는지 확인한다.

MLM masking/training method:

- HuggingFace `DataCollatorForLanguageModeling` 사용.
- non-special token 중 약 `15%`를 prediction 대상으로 샘플링.
- 선택된 token은 BERT-style `80/10/10` 규칙 적용:
  - `80%`: `<mask>`로 대체;
  - `10%`: random token id로 대체;
  - `10%`: 원 token 유지.
- loss는 선택된 token 위치에 대해서만 계산하고, 나머지는 label `-100`으로 ignore.
- NSP, whole-word masking, contrastive semantic loss는 사용하지 않음.
- 자세한 protocol: `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_training_protocol.md`.

따라서 3번 실험은 "MLM 학습 후 encoder feature가 같은 의미에 대해 더 잘 정렬되는가?"를 보는 중간 proxy task로 둔다.

Proxy task 설계:

1. 같은 의미 positive pair 정의
   - `target10_dev`의 plain text만 쓰지 않는다.
   - `parallel_item_manifest.tsv` 또는 row manifest에서 `item_id`를 복원한다.
   - 예: `acu:b.MAR.1.1`, `cop:b.MAR.1.1`, `syr:b.MAR.1.1`은 같은 verse/item 의미 단위로 묶는다.

2. representation 추출
   - encoder last hidden state 사용.
   - attention-mask mean pooling.
   - L2 normalization.
   - encoder는 freeze, classifier 없이 feature만 평가한다.

3. metric
   - same-pair cosine만 단독 사용하지 않는다. cosine은 anisotropy 때문에 모두 높게 나올 수 있다.
   - main metric은 positive-minus-hard-negative margin, Recall@1/5, MRR.
   - hubness@10도 같이 본다.

4. negative 구성
   - same language-pair 안에서 다른 `item_id`를 hard negative로 둔다.
   - random shifted negative도 보조로 둔다.
   - 같은 book/chapter shortcut을 줄이려면 같은 book 안 negative와 cross-book negative를 나눠 볼 수 있다.

5. 평가 단위
   - target10 전체 90 directed language pairs.
   - language별 macro average와 row-count weighted average를 둘 다 기록.
   - `cop`, `syr`는 별도 row로 반드시 보고.

6. pass/fail reading
   - PASS: XLM-R-base 대비 margin과 MRR/Recall이 함께 개선되고, hubness가 악화되지 않음.
   - PARTIAL: cosine은 오르지만 MRR/Recall이 그대로면 semantic alignment가 아니라 representation collapse/anisotropy 가능성.
   - FAIL: MLM loss는 좋아졌지만 feature retrieval이 개선되지 않으면 token prediction과 semantic alignment가 분리된 것으로 보고.

현재 측정 결과:

- `fvt`는 200-step MLM dev loss에서는 1등.
- 하지만 MLM dev same-meaning feature retrieval에서는 1등이 아님.
- same-pair cosine은 `mean_mlm200` `0.996556`, `random_mlm200` `0.993669`, `fvt_mlm200` `0.990975`, XLM-R-base `0.986126`.
- `mean_mlm200`이 macro MRR `0.022055`, margin `-0.001656`으로 가장 좋고, `random_mlm200`이 Recall@1 `0.005793`으로 가장 높음.
- `fvt_mlm200`은 same-pair cosine `0.990975`, macro MRR `0.019034`, Recall@1 `0.004551`.
- XLM-R-base는 same-pair cosine `0.986126`, macro MRR `0.020418`, Recall@1 `0.006874`.

Cosine attachment score table:

| Model | Same cosine | Delta vs base | Same-random gap | Hard margin | R@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.986126 | +0.000000 | +0.000189 | -0.003000 | 0.006874 | 0.020418 |
| `random_mlm200` | 0.993669 | +0.007543 | +0.000237 | -0.002612 | 0.005793 | 0.021748 |
| `mean_mlm200` | 0.996556 | +0.010430 | +0.000208 | -0.001656 | 0.005724 | 0.022055 |
| `fvt_mlm200` | 0.990975 | +0.004849 | +0.000215 | -0.002530 | 0.004551 | 0.019034 |
| `align_mlm200` | 0.990067 | +0.003941 | +0.000198 | -0.002603 | 0.004292 | 0.019030 |
| `focus_mlm200` | 0.984526 | -0.001600 | +0.000517 | -0.004347 | 0.004553 | 0.019333 |

원인 분석:

- Same cosine이 오른 것은 positive signal이다. append-only tokenizer와 MLM adaptation 이후 target10 문장이 encoder space에 더 안정적으로 들어온 것으로 볼 수 있다.
- 하지만 same-random gap이 `0.0002~0.0005` 수준이라 같은 의미 pair와 random negative의 cosine 차이가 매우 작다.
- hard margin이 여전히 음수다. 즉 hard negative가 exact aligned verse보다 더 가까운 경우가 많다.
- 원인은 XLM-R sentence embedding anisotropy, Bible domain/style 반복, 같은 book/chapter 내 hard negative의 높은 lexical/topic overlap, MLM objective가 contrastive semantic separation을 직접 학습하지 않는 점으로 본다.
- 따라서 이 결과는 "cosine attachment는 개선되었지만 semantic discrimination은 아직 약하다"로 보고한다.

CLS pooling 판단:

- XLM-R에서는 첫 토큰 `<s>`를 CLS-style sequence token처럼 사용할 수 있다.
- 하지만 MLM만 한 encoder에서 CLS가 sentence embedding으로 더 적절하다고 가정하면 안 된다. XLM-R/RoBERTa는 BERT NSP-style pooler 학습이 없고, 여기서는 classification fine-tuning도 하지 않았다.
- 그래서 main representation은 mean pooling으로 두고, CLS는 pooling ablation으로 보고한다.

CLS vs mean 결과:

| Model | Mean cosine | CLS cosine | Mean margin | CLS margin | Mean R@1 | CLS R@1 | Mean MRR | CLS MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `xlmr_base` | 0.986126 | 0.985600 | -0.003000 | -0.007491 | 0.006874 | 0.002862 | 0.020418 | 0.015012 |
| `random_mlm200` | 0.993669 | 0.997086 | -0.002612 | -0.001679 | 0.005793 | 0.004721 | 0.021748 | 0.018970 |
| `mean_mlm200` | 0.996556 | 0.994511 | -0.001656 | -0.004028 | 0.005724 | 0.004709 | 0.022055 | 0.019113 |
| `fvt_mlm200` | 0.990975 | 0.993396 | -0.002530 | -0.002711 | 0.004551 | 0.003802 | 0.019034 | 0.017251 |
| `align_mlm200` | 0.990067 | 0.994633 | -0.002603 | -0.002140 | 0.004292 | 0.003535 | 0.019030 | 0.016243 |
| `focus_mlm200` | 0.984526 | 0.994485 | -0.004347 | -0.002230 | 0.004553 | 0.003790 | 0.019333 | 0.017142 |

결론: CLS는 가능하지만, 현재 frozen semantic similarity proxy에서는 mean pooling이 Recall@1/MRR에서 더 낫다.

결론:

- 이 proxy task 자체는 맞다.
- 다만 결과 해석은 조심해야 한다.
- MLM loss improvement와 semantic feature alignment는 같은 것이 아니다.
- 따라서 3번은 "학습 후 encoder feature semantic alignment diagnostic"으로 보고, downstream task 전의 bridge metric으로 사용한다.

Artifacts:

- `docs/exp/v3.1/04_ablation/init_mlm_probe/feature_similarity_results.md`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/pooling_comparison_results.md`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_summary.tsv`
- `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_pair_scores.tsv`

4. Downstream task
- 
- 


5. Simple Decoder Translation
- 
- 
