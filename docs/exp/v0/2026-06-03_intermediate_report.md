# Intermediate Report: Target10 Low-Resource Adaptation

작성일: 2026-06-03

## 1. 목표 변경

기존 목표:

- Coptic/Syriac 2개 언어 중심 tokenizer extension + NMT

변경된 목표:

- 약 10개 저자원 언어를 추가하는 multilingual adaptation 파일럿
- Coptic/Syriac은 핵심 downstream 번역 사례로 유지
- GPU 실험은 물리 GPU 3, NVIDIA RTX A6000만 사용

## 2. 현재까지 완료

### Data

Bible corpus에서 10개 언어를 추출했다.

- 총 verse row: 76,972
- tokenizer train line: 61,930
- 10개 언어 공통 verse overlap: 4,892
- test split: John, 879개 내외
- dev split: Mark, 500-678개 수준

### Tokenizer Audit

기존 tokenizer 3개를 비교했다.

- XLM-R
- Glot500
- NLLB-200 distilled 600M

주요 발견:

- Glot500은 Coptic/Syriac/Cherokee/Ojibwa에서 문자 단위 분해가 심하다.
- NLLB는 같은 언어들에서 `<unk>` 비율이 약 45-50%까지 올라간다.
- XLM-R은 Coptic/Cherokee/Ojibwa는 상대적으로 괜찮지만 Syriac은 여전히 문자 단위에 가깝다.

### New Target10 Tokenizer

10개 언어 train set으로 SentencePiece unigram 16k tokenizer를 학습했다.

가장 큰 개선:

- Syriac: Glot500 대비 tokens/word 68.7% 감소
- Coptic: 66.3% 감소
- Cherokee: 61.9% 감소
- Ojibwa: 55.9% 감소

### Glot500 Merge

Target10 tokenizer를 Glot500 tokenizer에 merge했다.

- Base Glot500 pieces: 401,143
- Target10 pieces: 16,000
- Added pieces: 13,994
- Merged pieces: 415,137

Merged tokenizer에서도 핵심 개선은 유지됐다.

- Syriac: Glot500 대비 tokens/word 68.5% 감소
- Coptic: 66.3% 감소
- Cherokee: 61.9% 감소
- Ojibwa: 56.1% 감소

### Embedding Initialization

Glot500 model embedding과 LM head를 resized vocab에 맞춰 초기화했다.

- Random checkpoint: `data/processed/target10/initialized_models/glot500_target10_random`
- Mean checkpoint: `data/processed/target10/initialized_models/glot500_target10_mean`
- New tokens initialized: 13,994
- Mean initialization fallback: 0
- Mean avg old subtokens per new token: 3.791

### MLM Smoke, Pilot2k, And Pilot10k Training

GPU 3만 보이도록 `CUDA_VISIBLE_DEVICES=3`를 사용해 random/mean MLM 비교를 네 단계로 완료했다.

| Run | Init | Train samples | Eval samples | Eval mode | Train loss | Eval loss | Perplexity |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |
| Eval0 | Random | 0 | 500 | bsz2 | n/a | 14.4053 | 1,803,577.90 |
| Eval0 | Mean | 0 | 500 | bsz2 | n/a | 9.6377 | 15,331.40 |
| Smoke | Random | 200 | 100 | bsz2 | 10.0982 | 9.5543 | 14,104.97 |
| Smoke | Mean | 200 | 100 | bsz2 | 7.2596 | 6.9288 | 1,021.32 |
| Pilot2k | Random | 2,000 | 500 | bsz2 | 6.9697 | 6.3357 | 564.36 |
| Pilot2k | Mean | 2,000 | 500 | bsz2 | 6.5218 | 6.4470 | 630.79 |
| Pilot10k | Random | 10,000 | 1,000 | fp32 bsz16 | 7.3639 | 7.0169 | 1,115.29 |
| Pilot10k | Mean | 10,000 | 1,000 | fp32 bsz16 | 6.2236 | 5.8343 | 341.84 |

학습 전에는 Mean initialization이 random보다 훨씬 좋다.
짧은 smoke에서도 Mean이 좋았다.
2k pilot에서는 Mean의 train loss는 낮고 Random의 eval loss가 약간 낮아서 판단을 보류했다.
이후 10k pilot에서는 안정 평가 기준으로 Mean이 Random보다 명확히 좋아졌다.

10k 내장 평가는 eval batch size 2에서 두 조건 모두 `NaN`이 나왔다.
Random checkpoint 가중치에는 NaN/Inf가 없었고, eval batch size 16 fp32 재평가에서는 정상 loss가 나왔다.
따라서 10k checkpoint 판단에는 batch 16 재평가 값을 사용한다.

현재 downstream NMT용 adapted encoder 후보:

- `docs/exp/2026-06-03_05_mlm_adaptation/pilot10k_mean`

주요 ablation/control checkpoint:

- `docs/exp/2026-06-03_05_mlm_adaptation/pilot10k_random`

## 3. 쉬운 해석

지금까지 결과는 이렇게 보면 된다.

기존 모델은 일부 언어를 아예 모르는 방식으로 처리한다.

- Glot500: 글자를 하나씩 읽는 수준으로 쪼갬
- NLLB: 모르는 문자로 처리하는 `<unk>`가 많이 생김

새 tokenizer는 같은 텍스트를 훨씬 짧고 안정적인 subword sequence로 만든다.
embedding initialization은 아직 최종 결론이 아니다.
Mean은 학습을 더 쉽게 시작하게 해주는 것처럼 보이고, 10k 비교에서는 validation도 더 좋다.
2k dev loss에서 Random이 근소하게 앞선 결과는 작은 dev slice와 동적 masking의 영향이 있을 수 있다.
둘 다 학습 전 baseline보다는 크게 좋아졌으므로 continued pretraining 자체는 효과가 있다.
따라서 다음 실험은 Mean pilot10k로 Coptic/Syriac downstream 번역을 시작하고, 시간이 있으면 Random pilot10k를 ablation으로 비교하는 것이 좋다.

## 4. 다음 실험

### NMT Smoke And Pilot Update

Mean pilot10k checkpoint로 Coptic/Syriac direct NMT smoke와 pilot512를 양방향 실행했다.
이어서 full Coptic -> Syriac와 full Syriac -> Coptic를 전체 train set으로 각각 1 epoch 실행했다.

| Direction | Train samples | Eval samples | Test samples | Train loss | Eval loss | Test BLEU | Test chrF++ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Coptic -> Syriac smoke | 32 | 16 | 16 | 24.0936 | 8.7131 | 0.0500 | 4.6215 |
| Syriac -> Coptic smoke | 32 | 16 | 16 | 29.4014 | 14.6694 | 0.0774 | 0.3074 |
| Coptic -> Syriac pilot512 | 512 | 64 | 64 | 8.1130 | 6.2188 | 0.0899 | 4.7796 |
| Syriac -> Coptic pilot512 | 512 | 64 | 64 | 8.3344 | 6.0581 | 0.0506 | 4.9749 |
| Coptic -> Syriac full1epoch | 6,395 | 678 | 879 | 6.0174 | 5.7339 | 0.0139 | 5.7982 |
| Syriac -> Coptic full1epoch | 6,395 | 678 | 879 | 6.1782 | 7.4891 | 0.0181 | 9.9340 |

해석:

- 학습/평가/디코드/BLEU/chrF/chrF++ 계산 파이프라인은 GPU 3에서 통과했다.
- peak GPU memory는 약 15.5 GiB라 A6000에서 여유가 있다.
- 번역 품질은 아직 실패 상태다.
- smoke는 max length까지 가는 mixed-script 반복 출력이었다.
- pilot512는 target script 반복 출력으로 바뀌었고 generation length도 12-20 token 수준으로 짧아졌지만, 실제 번역은 아니다.
- full Coptic -> Syriac는 test loss와 chrF++가 더 좋아졌지만, 예측은 `ܘ ܕܝܢ ܕܝܢ`류 반복에 머물렀다.
- full Syriac -> Coptic는 chrF++가 더 올라갔지만, `test_gen_len=96.0`으로 최대 길이까지 가며 `ⲞⲨⲞϨ`, `ⲆⲈ`, `ⲄⲀⲢ` 같은 고빈도 Coptic 토큰을 반복한다.
- 따라서 단순히 full train을 더 쓰는 것만으로는 decoding collapse가 해결되지 않는다.
- 다음은 language tag, EOS/length 제어, repetition control 또는 target-script constraint를 넣어야 한다.

### Decoding Intervention Pilot Update

full Syriac -> Coptic의 max-length 반복 붕괴를 먼저 겨냥해 512-example direct/intervention pilot 아홉 개를 추가로 실행했다.

| Run | Change | Test BLEU | Test chrF++ | Gen len | 판단 |
| --- | --- | ---: | ---: | ---: | --- |
| tagged_len64_rp12 | bracket tags + max target 64 + repetition penalty 1.2 | 0.0000 | 0.0000 | 2.0 | 빈 출력 실패 |
| tagged_len64 | bracket tags + max target 64 | 0.0000 | 0.0000 | 4.0 | 빈 출력 실패 |
| len64 | no tags + max target 64 | 0.0506 | 4.9749 | 12.0 | 기존 pilot 재현 |
| natural_tags_len64 | `translate Syriac to Coptic:` prefix + max target 64 | 0.0000 | 3.5055 | 13.0 | 비어 있진 않지만 품질 하락 |
| tagged_len64_min8 | bracket tags + max target 64 + min target 8 | 0.0000 | 4.0740 | 10.0 | punctuation collapse |
| len64_ngram2 | no tags + max target 64 + no repeated bigrams | 0.0546 | 5.1984 | 12.0 | 이전 best, 하지만 반복 지속 |
| len64_ngram2_rp12 | no tags + max target 64 + no repeated bigrams + repetition penalty 1.2 | 0.1039 | 5.9591 | 9.0 | 현재 best direct pilot, 하지만 formulaic 반복 |
| len64_ngram2_rp12_step300 | same direct control, 300 steps | 0.1230 | 8.7360 | 13.9 | 수치는 상승, 하지만 formulaic 반복 |
| target_prefix_coptic_len64 | target label `Coptic: ` prefix + forced decoder prefix | 0.0858 | 5.6291 | 10.6 | 길이는 안정, 하지만 best direct보다 낮음 |

해석:

- `max_target_length=64` 자체는 안전하다. no-tag len64 pilot이 기존 Syriac -> Coptic pilot과 같은 수준을 재현했다.
- bracket-style language tag는 repetition penalty와 무관하게 빈 출력/EOS 붕괴를 만든다.
- 자연어 prefix는 빈 출력은 피하지만 여전히 `ⲞⲨⲞϨ` 반복이며 no-tag len64보다 낮다.
- `min_target_length=8`은 빈 출력을 막지만 `.` punctuation collapse로 바뀔 뿐이다.
- no-tag bigram 제약은 chrF++를 4.9749에서 5.1984로 조금 올렸고, 여기에 `repetition_penalty=1.2`를 더하면 5.9591까지 오른다.
- 다만 best direct pilot도 `ⲞⲨⲞϨ ⲆⲈ ⲈⲂⲞⲖ ⲚⲈⲘ ϪⲈ` 같은 짧은 formulaic fragment라 실제 번역은 아니다.
- 같은 best direct control을 300 step까지 늘리면 chrF++가 8.7360까지 오르지만, 첫 샘플부터 `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ ϪⲈⲀ ⲠⲈ...` 같은 거의 같은 문장을 반복한다. 더 오래 학습하는 것만으로는 source-grounded translation이 생기지 않는다.
- target-side `Coptic: ` prefix를 label에 붙이고 generation 때 같은 prefix로 decoder를 시작시키면 빈 출력과 max-length는 피하지만, 출력은 `ⲞⲨⲞϨ ⲆⲈ ⲈⲂⲞⲖ ⲚⲈⲘ` 같은 조각으로 더 고정된다. chrF++도 5.6291로 best direct 5.9591보다 낮다.
- 따라서 현재 tag 설정을 full run으로 확대하지 않는 것이 맞다.
- 다음 실험은 단순 language tag, 단순 target prefix, step 확장이 아니라 더 강한 target-script constraint, length/coverage control, auxiliary objective, 또는 pivot baseline 쪽으로 잡아야 한다.

### Multi-Source-To-Coptic Pilot Update

Coptic decoder에 target-side supervision을 더 주기 위해 Syriac/Greek/English -> Coptic train set을 만들었다.
Train은 verse별로 세 source를 interleave했고, dev/test는 기존 Syriac -> Coptic 기준을 유지했다.

| Run | Train examples | Steps | Epoch | Test BLEU | Test chrF++ | Gen len | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| multi_to_cop_len64_ngram2_pilot1536 | 1,536 | 100 | 0.26 | 0.0000 | 0.0000 | 3.0 | undertrained empty-output fail |
| multi_to_cop_len64_ngram2_pilot1536_step300 | 1,536 | 300 | 0.78 | 0.1697 | 14.7456 | 64.0 | max-length repetition fail |

해석:

- 100 step multitask는 direct pilot과 epoch 기준이 맞지 않아 너무 이르게 빈 출력으로 무너졌다.
- 300 step multitask는 direct pilot과 같은 `epoch=0.78`까지 학습했지만, `test_gen_len=64.0`으로 최대 길이까지 반복한다.
- chrF++ 14.7456은 실제 번역 개선이 아니라 긴 Coptic-like fragment 반복 때문에 커진 값으로 본다.
- Multitask 보강은 Coptic 표면 fluency를 올릴 수 있지만, length/coverage 제어 없이 full run으로 키우면 또 metric inflation이 된다.

### Coptic Autoencoding Auxiliary Pilot Update

이번에는 보조목표를 더 좁혔다.
Train에는 Syriac -> Coptic과 Coptic -> Coptic autoencoding을 verse별로 interleave했고, dev/test는 기존 Syriac -> Coptic만 유지했다.
1,024개 train slice는 512개 Syriac -> Coptic, 512개 Coptic autoencoding으로 구성된다.
200 step을 돌리면 direct pilot과 같은 `epoch=0.78` 기준이 된다.

| Run | Train examples | Steps | Epoch | Test BLEU | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| cop_auto_aux_len64_ngram2_rp12_pilot1024_step200 | 1,024 | 200 | 0.78 | 0.2345 | 10.0690 | 15.3 | 3/64 | 수치는 최고, 하지만 저다양성 formulaic |
| cop_auto_aux_natural_tasks_len64_ngram2_rp12_pilot1024_step200 | 1,024 | 200 | 0.78 | 0.2893 | 10.9355 | 20.8 | 14/64 | 현재 best metric/diversity, 하지만 formulaic |

해석:

- Coptic autoencoding 보조목표는 broad multi-source보다 길이 제어 측면에서 낫다. `test_gen_len=15.3`이라 max-length 붕괴는 아니다.
- chrF++ 10.0690은 direct 100-step, direct 300-step보다 높고 full Syriac -> Coptic의 9.9340보다도 약간 높다.
- 하지만 64개 예측 중 unique string은 3개뿐이고, 가장 흔한 문장이 41번 나온다.
- 대표 출력은 `ⲆⲈ ⲞⲨⲞϨ ⲠⲈ ⲀⲚ ⲈⲂⲞⲖ ϪⲈ ⲞⲨⲀ ⲚⲈⲘ ϨⲒ ⲄⲀⲢ.`이다.
- 여기에 자연어 task prefix (`translate Syriac to Coptic:`, `translate Coptic to Coptic:`)를 붙이면 chrF++가 10.9355까지 오르고 unique prediction도 14/64로 늘어난다.
- task-prefix variant의 top prediction은 23번 반복되어 unprefixed autoencoding의 41번보다 낫다.
- 그래도 대표 출력은 `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲠⲈ ⲞⲨ ⲈⲂⲞⲖⲀ ϪⲈ ⲚⲈⲘ...`류로 여전히 formulaic이다.
- 따라서 이 계열은 target-side fluency/length/diversity 안정화에는 도움이 되지만, source-grounded translation은 아직 만들지 못했다.

### Syriac Autoencoding Source-Grounding Pilot Update

이어서 source-side grounding을 더 주기 위해 train에 Syriac -> Syriac autoencoding을 추가했다.
Train은 Syriac -> Coptic, Coptic -> Coptic, Syriac -> Syriac 세 task를 verse별로 interleave했고, dev/test는 계속 Syriac -> Coptic만 유지했다.
1,536개 train slice는 각 task 512개씩이고, 300 step으로 direct/autoencoding pilot과 같은 `epoch=0.78` 기준을 맞췄다.

| Run | Train examples | Steps | Epoch | Test BLEU | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| syr_cop_auto_aux_natural_tasks_len64_ngram2_rp12_pilot1536_step300 | 1,536 | 300 | 0.78 | 0.2383 | 10.5716 | 16.4 | 6/64 | source autoencoding 추가 효과 없음 |

해석:

- 목표는 `translate Syriac to Syriac:` task를 추가해서 encoder가 Syriac 입력을 더 잘 보존하게 만드는 것이었다.
- 결과는 이전 best인 Coptic autoencoding + natural task prefix보다 낮다. chrF++는 10.9355에서 10.5716으로 내려갔고, unique prediction은 14/64에서 6/64로 줄었다.
- 가장 흔한 출력은 29번 반복된다. 이전 best의 top prediction 23번보다 더 좁게 collapse했다.
- 대표 출력은 `ⲆⲈ ⲞⲨⲞϨ ϪⲈ ⲞⲨ ⲠⲈ ⲀⲚ ⲈⲂⲞⲖ ⲚⲈⲘ ⲚⲀ ⲚⲒⲂⲈⲚⲚ.`이다.
- 따라서 source-side reconstruction 압력만 추가하는 방식은 현재 encoder-decoder collapse를 풀지 못한다.
- 다음 실험은 단순 autoencoding task 추가가 아니라 coverage/source-grounding loss, pivot baseline, 또는 더 직접적인 alignment/contrastive signal이 필요하다.

### Pivot First-Leg Sanity Pilot Update

다음으로 pivot baseline의 첫 관문을 따로 검사했다.
Syriac -> English를 먼저 학습하면 Coptic target decoder를 제거하고, 모델이 Syriac source를 읽어 target sequence를 조건부로 생성할 수 있는지 확인할 수 있다.

Pivot 데이터는 `scripts/prepare_pivot_nmt.py`로 만들었다.

| Direction | Train | Dev | Test |
| --- | ---: | ---: | ---: |
| syr_to_eng | 6,395 | 678 | 879 |
| eng_to_cop | 6,395 | 678 | 879 |
| syr_to_grc | 6,395 | 678 | 879 |
| grc_to_cop | 6,395 | 678 | 879 |

Syriac -> English 결과:

| Run | Train examples | Steps | Epoch | Test BLEU | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| pivot_syr_to_eng_len96_ngram2_rp12_pilot512 | 512 | 100 | 0.78 | 0.1792 | 8.8002 | 12.3 | 4/64 | 영어에서도 formulaic collapse |
| pivot_syr_to_eng_len96_ngram2_rp12_pilot512_step300_nosave | 512 | 300 | 2.34 | 0.1522 | 9.0912 | 13.3 | 5/64 | loss는 개선, source grounding은 실패 |

English -> Coptic 결과:

| Run | Train examples | Steps | Epoch | Test BLEU | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| pivot_eng_to_cop_len128_64_ngram2_rp12_pilot512_step100_nosave | 512 | 100 | 0.78 | 0.0000 | 0.0000 | 4.0 | 1/64 | pivot second-leg도 빈 출력 실패 |
| eng_cop_auto_aux_natural_tasks_len64_ngram2_rp12_pilot1024_step200_engtest | 1,024 | 200 | 0.78 | 0.3052 | 10.0165 | 15.0 | 2/64 | 빈 출력은 회복, 하지만 formulaic |
| byt5_small_pivot_eng_to_cop_len256_64_pilot256_step50_fp32 | 256 | 50 | 0.78 | 0.0000 | 0.0000 | 63.0 | 30/32 | 다양하지만 Coptic 생성 실패 |
| byt5_small_eng_cop_auto_aux_natural_tasks_len256_64_pilot1024_step200_fp32 | 1,024 | 200 | 0.78 | 0.0000 | 1.9330 | 63.0 | 7/64 | Coptic 문자는 회복, 단일문자 반복 |
| byt5_small_eng_cop_auto_aux_natural_tasks_len256_64_pilot1024_step200_fp32_ngram3_rp12 | 1,024 | 200 | 0.78 | 0.0000 | 6.8944 | 63.0 | 64/64 | 반복은 깨짐, Coptic 글자 나열 |

해석:

- 100 step은 64개 예측 중 61개가 `For I And the, of and that. to`로 동일했다.
- 300 step은 train/test loss를 낮추고 chrF++를 9.0912까지 올렸지만, unique prediction은 5/64뿐이다.
- 대표 출력은 `For the, that of and in is to not` 또는 `For the, of that and in is to.` 같은 고빈도 영어 단어 조합이다.
- 따라서 현재 문제는 Coptic target script/tokenization만의 문제가 아니다.
- 지금 구조의 encoder-decoder가 짧은 pilot 설정에서 source-conditioned translation으로 안정적으로 넘어가지 못하고 있다.
- English -> Coptic second-leg도 현재 설정에서는 64개 test prediction이 전부 빈 문자열이다. 즉 외부 Syriac -> English 모델을 붙인다고 가정해도, 현 Glot500 encoder-decoder Coptic decoder가 바로 pivot-ready인 것은 아니다.
- English -> Coptic에 Coptic autoencoding과 natural task prefix를 함께 넣으면 빈 출력은 회복된다. 64개 test prediction 중 empty line은 0개이고, `test_chrfpp=10.0165`, `test_gen_len=15.0`까지 올라간다.
- 하지만 unique prediction은 2/64뿐이고, 가장 흔한 출력이 53/64번 반복된다. Coptic-looking output을 다시 생성하게 만든 효과는 있지만 source-grounded translation으로 보기는 어렵다.
- ByT5-small fp32로 English -> Coptic second-leg를 바꿔도 해결되지 않았다. 32개 중 unique prediction은 30개라 exact duplicate collapse는 피했지만, 모든 prediction이 ASCII/English prompt echo이고 Coptic 문자는 0개다.
- 대표 출력은 `to Coptic: In the beginning was the Word, and the Word was wi`처럼 source English와 task prefix를 복사한 형태다. `test_chrfpp=0.0`, `test_gen_len=63.0`이라 Coptic target으로 넘어가지 못한다.
- 같은 ByT5에 Coptic autoencoding 보조목표를 넣으면 target script 전환은 된다. 64개 prediction 전부 Coptic 문자를 포함하고 prompt echo는 0개다.
- 그러나 번역이 아니라 `ⲈⲈⲈ...` 같은 단일문자 반복으로 무너진다. unique prediction은 7/64이고 최빈 출력은 52/64번 반복된다. `test_chrfpp=1.9330`, `test_gen_len=63.0`이라 Coptic 단어/문장 생성에도 아직 실패다.
- 여기에 `no_repeat_ngram_size=3`과 `repetition_penalty=1.2`를 넣으면 metric과 다양성은 좋아진다. `test_chrfpp=6.8944`, unique prediction 64/64가 된다.
- 하지만 대표 출력은 `ⲈⲀⲒⲞⲨⲢⲚⲠⲦⲘⲤⲰ...`처럼 공백 없는 Coptic 글자 나열이다. 반복을 단어 번역으로 바꾼 것이 아니라, 반복을 강제로 다양한 글자열로 바꾼 결과로 본다.
- 따라서 외부 Syriac -> English first-leg만 좋아져도 바로 pivot chain이 해결된다고 볼 수 없다. English -> Coptic second-leg도 source-grounding이 더 강한 objective나 모델 구조가 필요하다.
- 다음은 더 강한 seq2seq initialization, coverage/source-grounding objective, external pivot model, 또는 architecture 변경 쪽이 더 합리적이다.

운영 메모:

- 파일시스템이 100%라서 첫 300-step run은 eval까지 끝낸 뒤 checkpoint 저장 중 실패했다.
- 실패한 partial checkpoint는 삭제했고, `scripts/train_cop_syr_encoder_decoder.py`에 `--skip_save_model` 옵션을 추가했다.
- 재실행은 model/checkpoint 저장 없이 `run_summary.json`과 `generated_predictions.txt`만 남겼다.

### ByT5 Pretrained Seq2Seq Sanity Update

Glot500 MLM checkpoint를 encoder-decoder로 붙인 구조가 계속 source grounding에 실패했기 때문에, cross-attention까지 pretrained된 seq2seq 모델을 작게 확인했다.
모델은 `google/byt5-small`을 사용했다.
ByT5는 byte-level tokenizer라 Coptic/Syriac 문자 coverage 문제를 우회할 수 있다.

| Run | Precision | Train examples | Test examples | Steps | Max target | Test loss | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| byt5_small_pivot_syr_to_eng_len320_256_pilot512_step100 | fp16 | 512 | 64 | 100 | 256 | NaN | 3.7802 | 184.0 | unreliable | fp16 수치 불안정 실패 |
| byt5_small_pivot_syr_to_eng_len320_128_pilot256_step50_fp32_clean | fp32 | 256 | 32 | 50 | 128 | 1.7185 | 15.1800 | 127.0 | 32/32 | 다양성은 생김, 하지만 max-length hallucination |
| byt5_small_pivot_syr_to_eng_len320_64_pilot256_step50_fp32_clean | fp32 | 256 | 32 | 50 | 64 | 1.8795 | 11.6792 | 63.0 | 32/32 | 짧아졌지만 hallucination 절단 |
| byt5_small_pivot_syr_to_eng_len320_64_pilot256_step50_fp32_ascii | fp32 | 256 | 32 | 50 | 64 | 1.8795 | 11.1453 | 63.0 | 30/32 | ASCII만 생성, 하지만 prompt echo |
| byt5_small_pivot_syr_to_eng_len320_32_pilot256_step50_fp32_clean | fp32 | 256 | 32 | 50 | 32 | 2.2998 | 8.2479 | 31.0 | 24/32 | prompt echo/절단, 품질 하락 |
| nllb200_distilled600m_pivot_syr_to_eng_len320_64_pilot256_step50_fp16_forced_eng | fp16 | 256 | 32 | 50 | 64 | 3.4362 | 13.9481 | 22.5 | 4/32 | 길이는 안정, 하지만 unsupported-source formulaic |
| byt5_small_pivot_syr_to_eng_len320_64_pilot256_step200_fp32_clean | fp32 | 256 | 32 | 200 | 64 | 1.3734 | 10.3423 | 62.7 | 31/32 | loss는 하락, 하지만 mixed-script max-length hallucination |
| byt5_small_pivot_eng_to_cop_len256_64_pilot256_step50_fp32 | fp32 | 256 | 32 | 50 | 64 | 2.1606 | 0.0000 | 63.0 | 30/32 | 영어/prompt echo, Coptic 문자 0개 |
| byt5_small_eng_cop_auto_aux_natural_tasks_len256_64_pilot1024_step200_fp32 | fp32 | 1,024 | 64 | 200 | 64 | 1.3353 | 1.9330 | 63.0 | 7/64 | Coptic 문자 반복 collapse |
| byt5_small_eng_cop_auto_aux_natural_tasks_len256_64_pilot1024_step200_fp32_ngram3_rp12 | fp32 | 1,024 | 64 | 200 | 64 | 1.3353 | 6.8944 | 63.0 | 64/64 | 반복 억제로 글자 다양화, 번역 아님 |

해석:

- ByT5 fp16은 바로 제외한다. train loss가 비정상적으로 크고 eval/test loss가 `NaN`이 된다.
- ByT5 fp32는 loss가 정상이다. 50 step만으로 train loss 2.5998, test loss 1.7185까지 내려간다.
- Glot500 encoder-decoder의 Syriac -> English 300-step run은 64개 중 unique prediction이 5개뿐이었다.
- 반면 ByT5 fp32는 32개 test sample에서 32개 모두 다른 prediction을 냈다.
- 따라서 pretrained seq2seq initialization은 exact formula collapse를 깨는 데 도움이 되는 신호가 있다.
- 하지만 출력은 아직 번역이 아니다. 대표 출력은 `the syriac to translate Syrup terms...` 같은 prompt-like hallucination이고, `test_gen_len=127.0`으로 max target length에 붙는다.
- max target length를 128 -> 64 -> 32로 줄이면 출력은 짧아지고 decode 속도도 좋아지지만, `gen_len`이 각각 127/63/31로 계속 설정 길이 바로 앞까지 간다.
- 따라서 길이 축소는 hallucination을 자르는 효과일 뿐이고, EOS를 배웠거나 source-grounded translation이 생긴 것은 아니다.
- ByT5 len64에 ASCII-only generation 제약을 주면 mixed-script 문제는 사라진다. 32개 prediction 모두 ASCII-only다.
- 하지만 ASCII 제약도 `gen_len=63.0`으로 max target 바로 앞까지 가며, 대표 출력은 `" sentences Syriac to English: Suri the pronoun...` 같은 prompt echo다. 문자 제약은 script leakage만 막고 번역/종료 문제는 못 고친다.
- NLLB-200 distilled는 translation-pretrained 모델이고 `eng_Latn` forced BOS를 줬기 때문에 길이는 안정적이다. 하지만 32개 test 중 unique prediction이 4개뿐이고, 최빈 문장은 21번 반복된다.
- NLLB train slice에서 Syriac source token의 약 46.4%가 `<unk>`이고, 256개 source 모두 `<unk>`를 포함한다. 즉 translation pretraining 자체보다 source coverage가 병목이다.
- ByT5 len64를 50 step에서 200 step까지 늘리면 test loss는 1.8795에서 1.3734로 크게 내려간다. 하지만 `gen_len=62.7`로 여전히 max target 근처이고, 출력은 `вольно все the same words...` 같은 mixed-script hallucination이다.
- 따라서 ByT5 len64 실패는 단순히 50 step undertraining 때문이라고 보기 어렵다. 더 오래 학습하면 loss는 내려가지만 EOS/source-grounded translation은 생기지 않는다.
- ByT5로 English -> Coptic second-leg를 테스트하면 loss는 정상이고 prediction 다양성도 높지만, 실제 Coptic target으로 전환하지 못한다. 32개 prediction line 중 Coptic 문자가 들어간 줄은 0개이고, `translate English to Coptic:` prompt나 영어 원문을 반복한다.
- ByT5 + Coptic autoencoding은 이 문제를 반대로 만든다. Coptic 문자는 생성하지만 대부분 `Ⲉ` 반복이고, source-conditioned Coptic 문장으로 가지 못한다.
- ByT5 + Coptic autoencoding에 trigram blocking/repetition penalty를 넣으면 exact repetition은 사라지지만, Coptic 단어가 아니라 alphabet-soup 형태가 된다. 따라서 decoding-only 반복 억제도 번역 품질을 직접 해결하지 못한다.
- 다음 pretrained seq2seq 계열 실험은 fp32/안정 generation만 보지 말고, 실제 Syriac/Coptic coverage가 있는 모델이나 external pivot을 우선해야 한다.

### Retrieval Baseline Update

현재 neural 모델들이 너무 쉽게 collapse하므로, 학습 없는 retrieval 기준선을 추가했다.
방법은 source 문장을 char 3-5gram TF-IDF로 표현하고, train set에서 가장 가까운 source verse의 Coptic target을 그대로 가져오는 것이다.
GPU는 쓰지 않는 CPU baseline이다.

| Run | Direction | Train | Dev | Test | Dev BLEU | Dev chrF++ | Test BLEU | Test chrF++ | Unique pred | Same ID | 판단 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| retrieval_char345_eng_to_cop | English -> Coptic | 6,395 | 678 | 879 | 18.4355 | 42.8665 | 3.7415 | 22.3584 | 593/879 | 0/879 | 강한 non-neural 기준선 |
| retrieval_char345_syr_to_cop | Syriac -> Coptic | 6,395 | 678 | 879 | 16.9252 | 40.8230 | 3.7434 | 22.2083 | 568/879 | 0/879 | 강한 non-neural 기준선 |

해석:

- retrieval은 생성 모델이 아니라 train target을 빌려오는 방식이라 최종 모델은 아니다.
- 하지만 실제 Coptic 문장과 word boundary가 있고, 현재 neural run들보다 full-test chrF++가 훨씬 높다.
- test verse ID와 matched train verse ID가 같은 경우는 0/879이라 직접 ID leak은 아니다.
- 현재 neural 모델은 retrieval baseline에도 못 미친다. 다음 neural 실험은 metric만 올리는 것보다 source grounding과 word-level Coptic 생성을 먼저 해결해야 한다.

### Retrieval-Augmented ByT5 Pilot Update

retrieval baseline이 강했기 때문에, retrieved Coptic candidate를 입력에 붙인 ByT5 English -> Coptic pilot을 추가했다.
ByT5는 Coptic을 byte-level로 다루므로 이전 `max_target_length=64`가 너무 짧았다.
이번에는 source cap을 768, target cap을 384로 늘리고, train 1,024 / dev 64 / test 64로 짧게 확인했다.

| Run | Train | Steps | Epoch | Label cap | Gen cap | Test BLEU | Test chrF++ | Gen len | Unique pred | 판단 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_pilot1024_step100_fp32 | 1,024 | 100 | 0.39 | 384 | 384 | 0.1080 | 8.2957 | 383.0 | 62/64 | retrieval hint는 도움, 여전히 max-length 반복 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen256_pilot1024_step100_fp32 | 1,024 | 100 | 0.39 | 384 | 256 | 0.1633 | 8.8296 | 255.0 | 62/64 | metric 소폭 상승, 여전히 cap까지 생성 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen192_pilot1024_step100_fp32 | 1,024 | 100 | 0.39 | 384 | 192 | 0.1623 | 8.8471 | 191.0 | 62/64 | cap sweep 중 가장 나음, EOS는 미해결 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen128_pilot1024_step100_fp32 | 1,024 | 100 | 0.39 | 384 | 128 | 0.1374 | 8.2859 | 127.0 | 62/64 | 너무 짧아져 baseline 근처로 하락 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_pilot1024_step100_fp32_ngram3_rp12 | 1,024 | 100 | 0.39 | 384 | 384 | 0.1452 | 4.4081 | 301.3 | 64/64 | 길이는 줄지만 metric/품질 하락, prompt echo 증가 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen192_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 192 | 1.0324 | 11.1532 | 167.2 | 62/64 | 300 step 개선, prompt echo 0/64, 반복 지속 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen256_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 256 | 1.0773 | 11.2617 | 217.2 | 62/64 | 현재 neural test metric 최고, 더 긴 반복 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen384_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 384 | 0.8647 | 11.0174 | 316.0 | 62/64 | cap을 열면 반복이 길어지고 metric 하락 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen256_beam4_lp06_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 256 | 1.4365 | 13.0622 | 148.7 | 63/64 | metric 상승, near-cap 20/64로 감소 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen256_beam4_lp10_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 256 | 1.5061 | 14.6730 | 227.5 | 63/64 | 높은 metric, 하지만 길고 반복 지속 |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen192_beam4_lp10_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 192 | 1.4382 | 14.7947 | 174.6 | 63/64 | 현재 neural metric 최고, gen256보다 짧지만 cap-heavy |
| byt5_small_retrieval_aug_eng_to_cop_len768_384_gen192_beam4_lp06_pilot1024_step300_fp32 | 1,024 | 300 | 1.17 | 384 | 192 | 1.3003 | 13.1859 | 135.8 | 63/64 | 짧은 균형형 diagnostic, metric은 lp1.0보다 낮음 |
| byt5_small_retrieval_aug_cop_auto_tasks_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 3.5392 | 19.6952 | 179.2 | 62/64 | neural 최고 갱신, 하지만 retrieval copy 의존 큼 |
| byt5_small_retrieval_aug_cop_auto_tasks_eval_wrong_retrieval_shift1_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.5135 | 13.7065 | 179.1 | 62/64 | wrong retrieval hint를 따라가며 gold metric 하락 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_wrong50_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 3.5438 | 19.7653 | 179.2 | 62/64 | train wrong retrieval 50%, 정상 평가; copy는 줄지 않음 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_wrong50_eval_wrong_retrieval_shift1_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.5135 | 13.7838 | 179.2 | 62/64 | train wrong retrieval 50%도 wrong hint 추종 지속 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_paired_wrong_eng_to_cop_len768_384_gen192_beam4_lp10_pilot3072_step450_fp32 | 3,072 | 450 | 0.59 | 384 | 192 | 3.5438 | 19.7364 | 179.2 | 63/64 | paired normal+wrong train, metric 안정; copy 유사도만 소폭 감소 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_paired_wrong_eval_wrong_retrieval_shift1_eng_to_cop_len768_384_gen192_beam4_lp10_pilot3072_step450_fp32 | 3,072 | 450 | 0.59 | 384 | 192 | 0.5120 | 13.7058 | 179.2 | 62/64 | paired train도 wrong eval hint 추종 지속 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_paired_source_only_eng_to_cop_len768_384_gen192_beam4_lp10_pilot3072_step450_fp32 | 3,072 | 450 | 0.59 | 384 | 192 | 3.5291 | 19.6404 | 179.2 | 62/64 | paired source-only train, 정상 retrieval copy는 줄지 않음 |
| byt5_small_retrieval_aug_cop_auto_tasks_train_paired_source_only_eval_source_only_eng_to_cop_len768_384_gen192_beam4_lp10_pilot3072_step450_fp32 | 3,072 | 450 | 0.59 | 384 | 192 | 0.0000 | 2.8666 | 191.0 | 2/64 | source-only 평가에서 Coptic 반복 두 문자열로 붕괴 |
| byt5_small_retrieval_edit_cop_auto_tasks_eng_to_cop_len1024_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 3.5308 | 19.7322 | 179.6 | 62/64 | retrieved_source edit prompt, metric은 안정이나 copy는 줄지 않음 |
| byt5_small_retrieval_edit_cop_auto_tasks_eval_wrong_retrieval_shift1_eng_to_cop_len1024_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.4952 | 13.6621 | 179.6 | 63/64 | edit prompt도 wrong hint를 따라감 |
| byt5_small_retrieval_rerank_ab_normal_vs_shift1_len1024_4_gen4_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 4 | 4 | 0.0000 | 47.6562 | 2.0 | 2/128 | A/B rerank task, 실제 test accuracy는 47.66% |
| byt5_small_retrieval_aug_cop_auto_tasks_ret_dropout50_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 3.5455 | 19.8406 | 179.2 | 63/64 | metric은 소폭 상승, copy 의존은 줄지 않음 |
| byt5_small_retrieval_aug_cop_auto_tasks_eval_source_only_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.0383 | 0.4969 | 168.3 | 64/64 | retrieval-free 평가 붕괴, Coptic 출력 0/64 |
| byt5_small_retrieval_aug_cop_auto_tasks_ret_dropout50_eval_source_only_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.0530 | 2.3208 | 186.0 | 16/64 | source-only 평가에서 Coptic 문자는 일부 회복, 하지만 반복 collapse |
| byt5_small_retrieval_aug_cop_auto_tasks_ret_dropout100_eval_source_only_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 0.0000 | 2.5060 | 191.0 | 2/64 | 전부 Coptic 문자지만 두 문자열 반복으로 붕괴 |
| byt5_small_retrieved_only_cop_auto_tasks_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32 | 2,048 | 300 | 0.59 | 384 | 192 | 3.5263 | 19.6473 | 178.8 | 62/64 | 영어 source 없이 retrieved Coptic만으로 기존 최고와 거의 동일 |

해석:

- retrieval hint와 긴 target cap은 plain ByT5 English -> Coptic보다 낫다. `test_chrfpp=0.0`에서 `8.2957`까지 올라간다.
- 하지만 non-neural retrieval baseline `22.3584`에는 크게 못 미친다.
- 예측은 retrieved Coptic 일부를 따라가다가 `ⲚⲈⲘ`, `ⲈⲢⲰⲞⲨ`, `ⲠⲈ` 같은 토큰 반복으로 길이 cap까지 간다.
- label cap과 generation cap을 분리해 보니, gen cap 256/192는 chrF++를 약간 올리면서 반복 길이를 줄인다. 하지만 둘 다 `gen_len=cap-1`이라 EOS를 배운 것은 아니다.
- gen cap 128은 다시 떨어진다. 지금 pilot에서는 192-256이 임시로 덜 나쁜 범위지만, 번역 해결책은 아니다.
- 같은 긴 target cap에서 trigram blocking과 `repetition_penalty=1.2`를 붙이면 gen_len은 `383.0`에서 `301.3`으로 줄지만, chrF++가 `8.2957`에서 `4.4081`로 떨어지고 prompt echo가 42/64개로 증가한다.
- 같은 retrieval-augmented 설정을 300 step까지 늘리면 수치는 확실히 오른다. gen192는 chrF++ `8.8471 -> 11.1532`, gen256은 `8.8296 -> 11.2617`로 올라갔고 prompt echo도 0/64가 됐다.
- 하지만 아직 scale 후보는 아니다. gen192는 48/64, gen256은 47/64 prediction이 거의 cap에 붙고, `ⲚⲦⲈⲠϬⲞⲒⲤ`, `ⲚⲦⲈⲚⲒⲢⲰⲘⲒ` 같은 Coptic phrase 반복이 많다.
- gen384는 열린 cap이 해결책이 아님을 확인했다. test chrF++는 `11.0174`로 내려가고, gen len은 `316.0`까지 길어져 반복이 늘었다.
- beam4는 retrieval-augmented 쪽에서 처음으로 쓸 만한 decoding 개선을 만들었다. gen256 greedy의 chrF++ `11.2617`이 beam4/lp0.6에서 `13.0622`, beam4/lp1.0에서 `14.6730`까지 올라갔다.
- beam4/lp0.6은 균형이 좋다. median token length가 255에서 125로 줄고, near-cap prediction도 47/64에서 20/64로 줄었다.
- beam4/lp1.0은 현재 neural metric 최고지만 긴 반복을 더 허용한다. median token length는 다시 255이고 near-cap은 44/64다.
- generation cap을 256에서 192로 낮추고 beam4/lp1.0을 쓰면 현재 neural metric 최고가 된다. test chrF++는 `14.6730 -> 14.7947`로 소폭 오르고, gen len은 `227.5 -> 174.6`으로 줄었다.
- 하지만 gen192/lp1.0도 near-cap이 45/64라 EOS를 배운 것은 아니다. cap-heavy 반복을 더 짧은 cap으로 자른 효과가 여전히 섞여 있다.
- gen192/lp0.6은 더 짧은 균형형이다. gen len은 `135.8`, chrF++는 `13.1859`, near-cap은 29/64다. 읽기 쉬운 diagnostic에는 괜찮지만 best metric은 아니다.
- Coptic autoencoding을 retrieval-augmented 학습에 섞으면 neural metric이 크게 오른다. 같은 gen192 beam4/lp1.0에서 chrF++가 `14.7947 -> 19.6952`로 올라갔고, near-cap도 45/64에서 34/64로 줄었다.
- 그러나 이 개선은 retrieval hint 복사 의존이 크다. test 64개 중 17개 prediction이 retrieved Coptic과 정확히 같고, prediction-vs-retrieved chrF++가 `69.5924`다. 같은 64개에서 retrieved target 자체도 gold 대비 chrF++ `24.7124`라, 새 모델은 독립 번역이라기보다 retrieved Coptic을 더 잘 따라가도록 학습된 것으로 해석해야 한다.
- wrong retrieval 평가도 했다. dev/test에서 retrieved Coptic hint를 한 행씩 밀어 일부러 틀린 hint를 주면 test chrF++가 `19.6952 -> 13.7065`로 떨어진다. 그런데 prediction-vs-wrong-retrieved chrF++는 `69.7749`로 여전히 높고 exact wrong-hint copy도 17/64다. 즉 모델은 English source보다 제공된 Coptic hint를 더 강하게 따라간다.
- train에도 wrong retrieval hint를 절반 섞었다. 정상 retrieval 평가에서는 test chrF++가 `19.7653`으로 유지됐지만, exact retrieved copy가 18/64로 늘고 prediction-vs-retrieved chrF++도 `70.7350`으로 올라갔다.
- 같은 train wrong 50% 모델을 wrong retrieval eval/test에 걸면 test chrF++는 `13.7838`로 아주 조금 오르지만, prediction-vs-wrong-retrieved chrF++가 `71.0756`으로 더 올라가고 exact wrong copy도 18/64가 된다. 즉 단순 wrong-hint mix는 source-grounding이 아니라 hint-following을 더 강화하는 쪽이다.
- normal retrieval row를 유지하면서 wrong retrieval copy를 하나씩 더 붙이는 paired 실험도 했다. 정상 retrieval 평가에서는 test chrF++ `19.7364`로 안정적이고 prediction-vs-retrieved chrF++가 `69.1861`로 조금 낮아졌지만, wrong retrieval eval/test에서는 test chrF++ `13.7058`, prediction-vs-wrong-retrieved chrF++ `69.9642`라 여전히 틀린 hint를 따라간다. 이건 작은 copy-similarity 감소일 뿐 source-grounding 해결은 아니다.
- normal retrieval row를 유지하면서 source-only copy를 하나씩 더 붙이는 paired source-only 실험도 했다. 정상 retrieval 평가에서는 test chrF++가 `19.6404`로 조금 내려가고 exact retrieved copy는 18/64, prediction-vs-retrieved chrF++는 `70.4660`이라 copy 의존이 줄지 않았다. source-only 평가에서는 chrF++가 `2.8666`까지 오르지만, 64개 중 unique prediction이 2개뿐이고 top `ⲈⲦⲈ...` 반복 문자열이 63번 나온다. 즉 Coptic script 회복이지 번역 회복이 아니다.
- retrieved Coptic만 주는 대신 matched verse의 English `retrieved_source`까지 넣고 "retrieved_coptic을 source에 맞게 고쳐라"는 edit prompt도 실험했다. 정상 retrieval에서는 test chrF++ `19.7322`로 안정적이지만 prediction-vs-retrieved chrF++ `70.0571`, exact copy 17/64라 copy가 줄지 않았다. wrong retrieval eval/test에서는 test chrF++ `13.6621`, prediction-vs-wrong-retrieved chrF++ `70.4572`, exact wrong copy 17/64라 prompt-level edit framing만으로는 source-grounding이 생기지 않는다.
- supervision을 더 바꿔서 A/B contrastive rerank도 실험했다. 입력에는 현재 English source, normal retrieved 후보, shift1 wrong 후보를 같이 주고 정답은 gold에 더 가까운 후보의 `A/B`다. A/B label은 mirrored row로 64/64 균형이다. 모델은 모든 test prediction을 유효한 A/B로 냈지만 accuracy가 `47.66%`라 chance보다 낮다. 선택된 후보의 Coptic chrF++도 `20.5311`로 normal retrieval 후보를 항상 고르는 baseline `24.7124`보다 낮고, oracle best-of-two `25.4860`보다 훨씬 낮다. 즉 후보 집합에는 신호가 있지만, 짧은 generated-label seq2seq reranker는 그 신호를 못 배운다.
- 같은 후보쌍을 generated label이 아니라 discriminative pairwise encoder scorer로도 학습했다. ByT5 encoder + linear head를 두 후보에 각각 적용하고 pairwise cross-entropy로 300 step 학습했다. Test accuracy는 `62.50%`로 generated-label reranker보다 좋아졌고 selected candidate chrF++도 `22.9740`까지 올랐다. 하지만 여전히 normal retrieval 후보를 항상 고르는 baseline `24.7124`보다 낮고, oracle best-of-two `25.4860`에도 못 미친다. 특히 128개 중 58개에서 shifted wrong 후보를 선택하므로, 현재 pairwise scorer도 retrieval selector로 쓰기에는 부족하다.
- 같은 입력을 두 후보가 함께 보이는 cross-encoder classifier로도 학습했다. 하지만 300 step 후 loss가 거의 `0.693`에 머물고 test prediction이 전부 `B`로 collapse했다. Accuracy는 `50.00%`, selected candidate chrF++는 `20.4882`라 pairwise encoder보다도 낮다. 후보를 같이 보여주는 구조만으로는 ranking이 좋아지지 않았다.
- 별도로 neural model 없이 source와 candidate_source 사이 char 3-5gram TF-IDF cosine만 써서 rerank audit을 했다. 이 방법은 test accuracy `84.38%`, selected candidate chrF++ `24.5528`로 pairwise encoder보다 훨씬 높지만, 사실상 normal retrieval을 거의 고르는 방식이고 항상 normal retrieval을 고르는 baseline `24.7124`보다도 약간 낮다. 즉 현재 normal-vs-shift1 후보쌍은 oracle 여지는 있지만 rerank benchmark로는 margin이 작다.
- 그래서 full English -> Coptic retrieval에서 top-k 후보 pool 자체를 다시 봤다. Source-side char 3-5gram retrieval top8 후보를 만들고 gold Coptic chrF++ 기준 oracle을 계산했다. Full test에서 top1 retrieval은 chrF++ `22.5362`이고 oracle@8은 `28.3327`이다. 879개 중 663개는 top1이 아닌 후보가 더 좋았다. 즉 ranking 자체는 여지가 있지만, shift1 pair가 아니라 top-k hard candidate pool로 benchmark를 다시 만들어야 한다.
- Top8 후보에서 oracle-best 후보와 hard negative 후보를 pair로 만든 첫 학습도 했다. Train은 6,395 source row에서 mirrored 12,790 pair이고 label은 A/B 균형이다. 빠른 pilot으로 ByT5 encoder pairwise scorer를 max source 512, train pair 2,048개, 200 step만 학습했다. Test 1,024 pair에서 accuracy는 `44.73%`로 낮지만 selected candidate chrF++는 `24.6379`로 같은 slice의 top1 baseline `23.1003`보다 높다. Oracle `28.5232`에는 한참 못 미치므로 아직 selector는 아니지만, top-k pool에서는 후보 품질 신호가 일부 잡힌다.
- 같은 top8 후보 pool에서 neural pairwise 대신 얕은 feature reranker도 돌렸다. Train top8 후보는 self match를 제외하고 만들고, rank/retrieval score gap/source-candidate source 유사도/후보 길이 feature로 regressor를 학습한 뒤 validation에서 top1 fallback threshold를 골랐다. 선택된 `gradient_boosting` 모델은 full test chrF++ `24.5921`로 top1 `22.5362`보다 확실히 높고 oracle@8 `28.3327`보다는 낮다. Test 879개 중 선택 후보가 top1보다 better/tie/worse인 경우는 `264/550/65`다. 중요 feature는 source와 matched_source의 char4 Jaccard가 가장 커서, 현재 reranking은 neural translation 신호보다 source coverage/retrieval geometry가 더 잘 먹힌다.
- feature-selected 후보를 실제 retrieval-augmented ByT5 evaluation hint로도 넣어봤다. Train은 기존 top1 retrieval+Coptic autoencoding 2,048개 그대로 두고 validation/test의 `retrieved_coptic`만 feature-selected top8 후보로 바꿨다. 같은 64개 test slice에서 retrieved candidate 자체는 chrF++ `24.7124 -> 26.7484`로 좋아졌고, neural output도 `19.6952 -> 19.9182`로 조금 올랐다. 하지만 validation은 `36.5996 -> 35.5597`로 낮고, generation은 여전히 near-cap 39/64다. Copy audit에서는 exact retrieved copy가 `17/64 -> 7/64`, prediction-vs-retrieved chrF++가 `69.5924 -> 60.4123`으로 내려가서, 더 좋은 hint를 더 많이 베끼는 것이 아니라 hint가 바뀌며 copy 양상이 약해진 작은 positive로 본다.
- train translation 예제 절반에서 retrieval hint를 제거하는 dropout도 확인했다. test chrF++는 `19.6952 -> 19.8406`으로 조금 오르고 unique prediction도 62/64에서 63/64로 늘었지만, exact retrieved copy는 17/64에서 18/64로 늘었고 prediction-vs-retrieved chrF++도 `69.5924 -> 71.3544`로 올랐다.
- retrieval-free 평가도 했다. 학습은 best autoencoding mix와 동일하게 두고 dev/test에서 `retrieved_coptic`만 제거했더니 test chrF++가 `19.6952 -> 0.4969`로 떨어졌고, Coptic 문자가 포함된 prediction은 0/64개였다. 44/64개는 prompt echo, 46/64개는 English source substring echo였다.
- train retrieval dropout을 넣은 뒤 source-only dev/test로 평가하면 no-dropout source-only보다 낫다. test chrF++는 `0.4969 -> 2.3208`로 오르고 Coptic 문자 포함 prediction도 0/64에서 51/64로 회복된다. 하지만 unique prediction은 16/64뿐이고, 일부는 prompt/English echo, 다수는 `ⲈⲦⲈ...` 같은 반복 Coptic 조각이라 번역 품질로 보기는 어렵다.
- train translation row 전체에서 retrieval을 제거하는 100% dropout도 확인했다. prompt echo는 0/64로 사라지고 Coptic 문자 포함 prediction은 64/64가 됐지만, unique prediction이 2/64로 더 심하게 줄었다. 수치도 chrF++ `2.5060`에 머물러서, source-only 학습만 늘리면 target script는 잡지만 같은 Coptic 조각을 외우는 방향으로 무너진다.
- copy-aware audit도 추가했다. 같은 prediction을 gold Coptic뿐 아니라 retrieved Coptic candidate와도 비교했다. Coptic autoencoding은 gold chrF++를 `14.7127 -> 19.6154`로 올리지만, prediction-vs-retrieved chrF++도 `39.4107 -> 69.5924`로 같이 오른다. 50% train dropout은 prediction-vs-retrieved를 `71.3544`까지 더 올린다. 즉 현재 최고 neural 점수는 source-grounded translation보다 retrieved Coptic candidate 추종에 더 가깝다.
- retrieval-only control도 실행했다. 입력에서 English source를 제거하고 `retrieved_coptic`만 남긴 뒤 같은 Coptic autoencoding mix로 학습했는데, test chrF++가 `19.6473`으로 source+retrieval run의 `19.6952`와 거의 같다. copy audit에서도 prediction-vs-retrieved chrF++ `70.8309`, exact retrieved copy 18/64가 나왔다. 따라서 현재 설정에서는 English source가 성능에 거의 기여하지 않는다고 본다.
- 따라서 현재 높은 neural retrieval-augmented 점수는 source-only 번역 능력이 아니라 retrieved Coptic 후보 의존이다. retrieval augmentation 자체와 Coptic autoencoding 보조 목적은 유망하지만, 다음에는 더 강한 anti-copy/source-grounding 실험이 필요하다. 예: retrieval-editing target, delta/edit target, source-grounding/coverage objective, 또는 retrieved-only same-slice baseline과 copy-aware 평가.

### Saved-Checkpoint Decoding Sweep Update

현재 best direct checkpoint (`len64_ngram2_rp12_pilot512_syr_to_cop_mean10k`)를 다시 학습하지 않고 decoding 설정만 바꿔 비교했다.

| Decode | BLEU | chrF++ | Gen len | 판단 |
| --- | ---: | ---: | ---: | --- |
| greedy ngram2 rp1.2 | 0.1072 | 6.0273 | 9.16 | best direct 재현 |
| beam4 ngram2 rp1.2 | 0.1213 | 6.1031 | 9.0 | sweep best, 하지만 formulaic |
| beam4 length_penalty 0.6 | 0.1213 | 6.1031 | 9.0 | beam4와 동일 |
| greedy ngram2 rp1.5 | 0.1072 | 6.0273 | 9.16 | rp1.2와 동일 |
| greedy ngram1 rp1.2 | 0.0000 | 0.0000 | 2.0 | 빈 출력 실패 |
| coptic allowlist greedy | 0.1057 | 6.0226 | 9.09 | Coptic token 제약, 같은 formulaic |
| coptic allowlist beam4 | 0.1213 | 6.1031 | 9.0 | beam4와 동일 |

해석:

- beam4는 수치를 아주 조금 올리지만 출력은 `ⲞⲨⲞϨ ⲆⲈ ⲈⲂⲞⲖ ⲚⲈⲘ ϪⲈ`류 fragment 그대로다.
- length penalty와 더 강한 repetition penalty는 이번 checkpoint에서 의미 있는 변화를 만들지 못했다.
- unigram repeat blocking은 너무 강해서 빈 출력으로 무너진다.
- Coptic-script allowlist는 64개 test reference token을 하나도 막지 않는 안전한 제약이지만, beam4 결과와 완전히 동일하다. 현재 collapse는 non-Coptic leakage가 아니라 이미 유효한 Coptic-looking token 안에서 발생한다.
- decoding-only sweep은 이제 수확이 작다. 다음은 training-side objective/data, coverage/length control, 또는 pivot baseline 쪽으로 넘어가야 한다.

다음 실험:

1. Mean pilot10k를 사용해 더 강한 seq2seq initialization, coverage/source-grounding objective, 또는 external pivot model을 검토한다.
2. `max_target_length=64`는 유지하되 bracket/natural source tag full run과 현재 multitask full run은 보류.
3. 현재 direct control은 no-tag len64 + `no_repeat_ngram_size=2` + `repetition_penalty=1.2`로 둔다.
4. decode-time beam4는 작은 metric gain용으로만 사용하고, 반복 붕괴 해결책으로 보지는 않는다.
5. 같은 512-example direct control을 step 수만 늘리는 실험은 보류한다. 300-step 결과가 metric은 올렸지만 같은 collapse를 유지했다.
6. 단순 `Coptic: ` target prefix/decoder prefix 단독 실험은 보류한다. 길이는 안정되지만 best direct보다 낮고 같은 formulaic fragment를 반복했다.
7. Coptic-only decode constraint 단독 실험은 보류한다. allowlist가 beam4와 같은 출력/점수를 만들었다.
8. Coptic autoencoding + natural task prefix는 현재 best metric/diversity 실험이지만, 아직 formulaic이므로 그대로 full scale로 키우지 않는다.
9. Syriac autoencoding을 단순히 추가한 3-task auxiliary는 diversity가 줄었으므로 그대로 확장하지 않는다.
10. Syriac -> English pivot first-leg도 formulaic하게 무너지므로, 현재 모델로 단순 pivot chain을 이어 붙이지 않는다.
11. English -> Coptic pivot second-leg baseline은 빈 출력으로 실패하므로, 외부 first-leg만 붙이는 단순 pivot chain은 보류한다.
12. English -> Coptic + Coptic autoencoding은 빈 출력은 고치지만 2/64 unique라 그대로 scale하지 않는다.
13. ByT5 English -> Coptic second-leg는 다양성은 높지만 Coptic 문자를 0개 생성하므로 그대로 scale하지 않는다.
14. ByT5 + Coptic autoencoding은 target script 전환은 되지만 단일문자 반복 collapse라 그대로 scale하지 않는다.
15. ByT5 + Coptic autoencoding + 반복 억제는 metric은 올리지만 공백 없는 글자 나열이라 그대로 scale하지 않는다.
16. retrieval baseline은 강하지만 비생성 방식이므로 최종 목표는 아니다. 다만 다음 neural run은 이 기준선을 해석 기준으로 삼는다.
17. ByT5 retrieval-augmented pilot은 retrieved Coptic hint가 도움은 되지만 max-length 반복을 유지하므로 그대로 scale하지 않는다.
18. retrieval-augmented gen cap 192-256은 임시로 덜 나쁜 출력 길이를 만들지만 `gen_len=cap-1`이라 EOS 해결책은 아니다. generic repetition penalty도 prompt echo를 키우므로 기본값으로 쓰지 않는다.
19. retrieval-augmented 300-step gen192/gen256은 현재 neural diagnostic 중 가장 좋지만, 아직 대부분 cap-bound이고 retrieval baseline chrF++ 22 수준에도 못 미치므로 scale하지 않는다.
20. retrieval-augmented gen384는 반복을 길게 만들고 metric을 낮추므로 기본 cap으로 쓰지 않는다.
21. retrieval-augmented gen192 beam4/lp1.0은 현재 neural metric 최고 후보로 둔다. chrF++는 `14.7947`이고 gen256/lp1.0보다 짧지만 near-cap 45/64라 반복 inflation 가능성을 계속 주의한다.
22. retrieval-augmented beam4/lp0.6은 균형형 기본 후보로 둔다. gen192/lp0.6은 chrF++ `13.1859`, gen len `135.8`, near-cap 29/64이고, gen256/lp0.6은 chrF++ `13.0622`, gen len `148.7`, near-cap 20/64다.
23. retrieval-augmented + Coptic autoencoding은 neural 최고 chrF++ `19.6952`를 만들지만 17/64 exact retrieved copy라 그대로 scale하지 않는다. 다음은 copy 의존을 줄이는 retrieval dropout/delta-target/source-grounding 실험이어야 한다.
24. 단순 50% train retrieval dropout은 chrF++를 `19.8406`으로 조금 올리지만 exact retrieved copy를 18/64로 늘리므로 anti-copy 해결책으로 보지 않는다.
25. retrieval-free 평가에서는 Coptic 출력이 0/64로 무너지므로, 현재 high score를 source-only 번역 능력으로 해석하지 않는다.
26. train retrieval dropout + source-only 평가는 Coptic 문자 회복에는 도움이 되지만 chrF++ `2.3208`, unique 16/64라 아직 source-grounded translation으로 보지 않는다.
27. train retrieval dropout 100% + source-only 평가는 prompt echo를 없애지만 unique 2/64라 더 심한 target-side 반복 collapse로 본다.
28. retrieval 계열 실험은 앞으로 gold metric만 보지 말고 prediction-vs-retrieved chrF++와 exact retrieved copy를 함께 본다.
29. retrieval-only control이 source+retrieval과 거의 같은 점수를 냈으므로, 현재 retrieval-augmented metric을 English source-conditioned translation으로 해석하지 않는다.
30. wrong-retrieval control에서도 prediction이 틀린 hint를 따라가므로, 현재 retrieval-augmented metric을 source-conditioned translation으로 해석하지 않는다.
31. train wrong retrieval 50%도 copy를 줄이지 못했으므로, 다음 retrieval 실험은 plain translation score가 아니라 retrieval-editing/delta-target/source-grounding objective로 설계한다.
32. paired normal+wrong retrieval train도 작은 copy-similarity 감소 외에는 wrong hint robustness를 만들지 못했으므로, 같은 방식의 wrong-hint mix를 더 키우지 않는다.
33. paired source-only retrieval train도 source-only eval을 두 문자열 반복으로만 회복하므로, 단순 source-only view 추가를 더 키우지 않는다.
34. retrieved_source를 넣은 prompt-level retrieval-edit도 wrong hint를 계속 따라가므로, prompt wording만 더 바꾸는 실험은 보류한다. 다음은 delta/edit target, contrastive ranking, source coverage loss처럼 supervision 자체가 바뀌는 방향이어야 한다.
35. A/B generated-label contrastive reranker도 normal retrieval baseline보다 못하므로, 같은 ByT5 seq2seq 방식의 짧은 label reranking은 보류한다.
36. Pairwise encoder reranker는 generated-label보다 낫지만 selected chrF++ `22.9740`으로 normal retrieval baseline `24.7124`를 넘지 못한다. 현재 pairwise scorer도 그대로 selector로 쓰지 않고, ranking을 계속하려면 더 강한 candidate set, hard negative 구성, 또는 source-candidate alignment feature가 필요하다.
37. Cross-encoder reranker는 후보를 함께 보지만 all-`B` 위치 편향으로 무너지므로, 같은 mirrored A/B 데이터에 단순 classifier만 붙이는 방향도 보류한다.
38. Source-similarity reranker는 normal retrieval baseline에 거의 도달하지만 넘지 못한다. 다음 ranking 실험은 shift1 wrong 후보가 아니라 더 큰 candidate pool이나 source 유사도가 비슷한 hard negative로 benchmark를 다시 만들어야 한다.
39. Top8 retrieval oracle audit은 ranking benchmark를 다시 만들 가치가 있음을 보여준다. Full test top1 chrF++는 `22.5362`, oracle@8은 `28.3327`이고 663/879개에서 rank1이 아닌 후보가 더 좋다. 다음 ranking 실험은 이 top-k pool에서 pair/listwise data를 만든다.
40. Top8 pairwise reranker 첫 pilot은 test selected chrF++가 top1보다 높아 일부 신호는 있지만 accuracy가 `44.73%`라 불안정하다. 다음은 같은 scorer를 단순 scale하기보다 calibration, input truncation, rank/score feature, listwise objective를 검토한다.
41. Top8 feature reranker는 full test에서 top1 retrieval을 `22.5362 -> 24.5921`로 넘겼다. 이는 ranking 방향의 첫 positive full-test selector지만 oracle@8 `28.3327`에는 아직 멀다. 다음은 이 feature selector를 후보 필터로 쓰거나, source coverage/retrieval-score feature를 포함한 listwise selector와 retrieval-editing objective를 연결한다.
42. Feature-selected top8 hint를 retrieval-augmented ByT5 eval/test에 넣으면 test chrF++는 `19.6952 -> 19.9182`로 소폭 오르고 exact copy는 줄지만, validation 하락과 near-cap generation이 남는다. 따라서 더 좋은 retrieval 후보는 유용한 입력이지만, 단독 해결책이 아니라 retrieval-editing/listwise/source-grounding objective와 연결해야 한다.
43. ByT5 fp32는 exact duplicate collapse를 피하지만 128/64/32 length sweep 모두에서 max target 바로 앞까지 생성하므로, 길이만 더 줄이지 말고 length/EOS 제어 또는 coverage가 좋은 seq2seq 모델을 확인한다.
44. ByT5 ASCII-only generation은 script leakage만 줄이고 max-length prompt echo를 유지하므로, 단독 해결책으로 보지 않는다.
45. ByT5 len64 step200은 loss만 낮추고 mixed-script max-length hallucination을 유지하므로, 같은 slice에서 step만 늘리는 실험은 보류한다.
46. NLLB-200 distilled는 forced English로 길이는 안정되지만 Syriac source가 `<unk>`로 많이 무너지므로, unsupported-source 설정 그대로 확장하지 않는다.
47. fp16 ByT5는 NaN이 나므로 사용하지 않는다.
48. filesystem이 100%이므로 diagnostic run에는 `--skip_save_model`을 사용하고, checkpoint 보존 정책을 따로 정한다.
49. non-collapsed pilot이 나온 뒤 Random pilot10k를 downstream ablation/control로 비교할지 결정.
50. 시간이 허락하면 Align initialization 구현 후 Random/Mean과 비교.
51. NMT 결과가 안정화되면 tokenizer/MLM 지표와 BLEU/chrF++의 연결을 분석.

## 5. 주의점

- 현재 MLM 결과는 downstream 이전의 선택 근거이며, 최종 결론은 NMT 결과와 함께 써야 한다.
- 10k built-in eval batch size 2는 `NaN`이 나왔으므로, 해당 결과는 판단용 metric으로 쓰지 않는다.
- 몇몇 verse는 너무 길어서 모델 max length를 초과한다. 본 실험 전 filtering/chunking 설정을 고정해야 한다.
- NMT baseline은 smoke/pilot/full1epoch 양방향까지 완료됐지만, full Syriac -> Coptic에서 max-length 반복 붕괴가 확인됐다.
- GPU 실험은 물리 GPU 3 전용 정책을 유지한다.
