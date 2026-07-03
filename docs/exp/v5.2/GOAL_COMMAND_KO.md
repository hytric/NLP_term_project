# v5.2 Goal Command

아래 문안을 그대로 goal로 건다.

```text
goal "docs/exp/v5.2 기준으로 Glot500 논문 재현형 v5.2 실험을 아침까지 table score가 나오도록 끝까지 진행한다. 실험은 92 XLM-R-seen replay + 7 XLM-R-unseen downstream-capable tail target(dtp_Latn, xav_Latn, bam_Latn, csb_Latn, ile_Latn, lij_Latn, fur_Latn)으로 고정한다. Glot500식 SentencePiece unigram tokenizer 학습과 XLM-R SPM append vocab injection을 기본으로 사용하고, Yamaguchi vocabulary expansion은 main에서 제외해 추가 실험으로만 남긴다. main ablation은 동일 corpus/동일 tokenizer/동일 MLM schedule에서 new-token embedding initialization(random, mean, fvt, weighted_fvt, family_mean)을 비교하는 것이다. 먼저 corpus merge, tokenizer 학습, initializer 5종 생성을 완료한다. 이후 GPU 2장만 사용해 random/mean/fvt/weighted_fvt/family_mean을 wave 방식으로 학습한다. 기본 설정은 Glot500 hyperparameter에 맞춰 effective batch 384, learning rate 5e-5, Adam betas 0.9/0.999, max sequence length 512, MLM probability 0.15로 둔다. 이전 4000-step 결과는 수렴 checkpoint가 아니라 early diagnostic으로만 해석한다. main run은 MAX_STEPS=8000, SAVE_STEPS=1000으로 시작해 checkpoint 8개를 만들고, 5000/6000/7000/8000 trajectory에서 train loss, PPPL, retrieval, downstream 변화를 확인한다. checkpoint가 생길 때마다 PPPL/MLM proxy, Tatoeba, Bible, NER/POS 가능분, Roundtrip/Taxi1500 materialization 가능분, embedding similarity를 평가하고 docs/exp/v5.2의 incremental table과 log를 계속 갱신한다. 최종 보고에서는 low-resource를 XLM-R-unseen tail + downstream 가능한 최소 corpus band로 설명하고, paired 결과가 들어온 경우에만 fvt 계열 우위 claim을 승격한다."
```

실행 핵심 command:

```bash
LG_SAMPLING_FACTOR=0.3 SCALE=1.5 bash preprocessing/run_v52_glot5007_merge.sh
bash tokenization/train_v52_glot5007.sh
bash scripts/run_v52_build_initializers.sh
METHODS="random mean fvt weighted_fvt family_mean" GPUS="2 3" SAVE_STEPS=1000 MAX_STEPS=8000 \
  bash modeling/launch_v52_init_all.sh
```
