# Third Try Idea: Target10 Performance Model With Glot500-Inspired Controls

작성일: 2026-06-12

## 핵심 피드백 반영

이번 `third_try`의 중심 실험은 **기존 target10 low-resource 언어에서 실제 downstream 성능이 개선되는 XLM-R-base adaptation model을 만드는 것**이다. Glot500은 그대로 복제할 대상이라기보다, id-preserving vocab append, high-resource replay, full MLM, downstream evaluation을 설계하는 기준점이다.

기존에 우리가 한 실험 중 target-only, LoRA, new-row repair, seed-1 pilot 등은 main experiment가 아니라 ablation study로 내려간다. 반대로 8k/16k/32k vocab grid와 random/mean/fvt/align/focus embedding initialization 비교는 이번 novelty와 final model selection을 위한 main matrix 후보로 사용한다.

## Main Claim

XLM-R-base에 대해 XLM-R id를 보존하는 vocabulary extension, high-resource replay + target10 low-resource mixture, 여러 embedding initialization method, 3개 이상 seed의 continued pretraining을 수행하면 target10 downstream 성능이 개선되는지 검증한다.

주장은 downstream까지 닫는다. tokenizer metric이나 PPPL만으로 성공을 주장하지 않는다.

## Source, Target, Head, Tail 정의

| 용어 | 정의 |
| --- | --- |
| Source model | `xlm-roberta-base` |
| Source vocabulary | XLM-R의 원래 SentencePiece vocabulary |
| Source/head languages | XLM-R이 이미 커버하는 high-resource replay/control 언어. 예: English, German, Japanese, Korean |
| Target/tail languages | 기존 target10 low-resource 언어: `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp` |
| Final model | XLM-R vocabulary를 보존하고 새 token을 append한 뒤 MLM continued pretraining한 모델 |

새 언어 하나를 넣고 "좋아졌다"를 주장하는 구조가 아니다. Target10 전체를 main low-resource set으로 두고, high-resource 언어는 replay/control과 forgetting sanity check에 사용한다.

Coptic/Syriac는 extension이 아니라 main experiment에 포함한다. 두 언어는 unsupported-script bottleneck과 embedding initialization 효과를 보여주는 핵심 evidence다.

## Glot500에서 가져오는 원칙

본 실험에서는 아래 항목을 Glot500에서 가져온 기본 원칙으로 둔다.

1. Base model은 XLM-R-base이다.
2. Tokenizer는 SentencePiece unigram을 사용한다.
3. Auxiliary tokenizer를 multilingual training corpus에서 학습한다.
4. 기존 XLM-R token id는 절대 바꾸지 않는다.
5. Auxiliary vocab에서 XLM-R에 없는 token만 append한다.
6. 각 language-script는 train/dev/test로 나누고, dev/test는 각각 1000 sentence-prime을 reserve한다.
7. Bible parallel verse가 있으면 dev/test에 각각 500개를 별도로 둔다.
8. Continued pretraining은 MLM objective로 full fine-tuning한다.
9. Sampling은 language-script별 multinomial sampling을 쓰고 temperature alpha는 `0.3`으로 둔다.
10. High-resource replay는 target10을 압도하지 않도록 cap하거나 sampling weight를 둔다.
11. 입력은 XLM-R처럼 text stream을 tokenizer에 통과시킨 뒤 512-token chunk로 자른다.
12. Evaluation은 target10 downstream 개선을 최종 기준으로 두고, PPPL/retrieval/alignment는 representation evidence로 사용한다.

## Main Run과 Ablation 분리

| 구분 | 역할 | 포함할 것 |
| --- | --- | --- |
| Main target10 run | 논문/보고서의 중심 실험 | XLM-R-base -> vocab append -> multi-init -> high+low mixture MLM -> target10 downstream |
| Extension case | main 이후 optional transfer | target10 밖 언어에 같은 protocol 적용 |
| Ablation study | 기존 실험과 추가 비교 | vocab size grid, init methods, fallback type, CPT-only, LoRA, target-only vs replay, added-token repair |

중요한 기준:

- Main run은 target10 downstream 개선을 우선한다.
- Ablation은 main run을 흔들지 않는다.
- Ablation 결과가 좋아도 high-resource replay + low-resource mixture + downstream + seed-stable main result를 대체하지 않는다.
- 기존 `second_try`의 negative diagnostic은 "ablation에서 드러난 실패 조건"으로 정리한다.

Tokenizer fallback 비교도 ablation으로 둔다. Main run은 selected target10 tokenizer를 우선하고, 별도 ablation에서 `character fallback/character coverage` 방식과 `byte fallback` 방식을 같은 corpus/vocab budget으로 비교한다.

## 평가에서 반드시 비교할 모델

| Model | 목적 |
| --- | --- |
| XLM-R-B | source baseline |
| Third-try model | target10 adapted performance model |
| Glot500-m | 참고 baseline 또는 related-work reference. 직접 비교가 어려우면 문헌 비교로 제한 |
| CPT-only XLM-R-B | ablation baseline. vocabulary extension 없이 같은 corpus로 continued pretraining |

## 성공 조건

Main success는 아래를 모두 만족해야 한다.

1. Target10 tokenization fragmentation이 XLM-R-B보다 개선된다.
2. PPPL 또는 retrieval/alignment가 target10에서 XLM-R-B보다 개선된다.
3. Target10 downstream task 평균이 XLM-R-B보다 개선된다.
4. 개선이 3개 이상 seed에서 안정적이다.
5. High-resource replay/control 성능이 크게 무너지지 않는다.

Tokenizer 개선만 있고 downstream/representation 개선이 없으면 성공이 아니라 ablation/diagnostic result로 쓴다.

## 지금까지의 실험을 어떻게 살릴 것인가

현재까지 수행한 실험은 버리지 않는다. 다만 위치를 바꾼다.

- `first_try`: engineering prototype 및 early evidence.
- `second_try`: XLM-R extension ablation과 failure diagnosis.
- `third_try`: target10 성능 개선 모델과 논문 novelty를 중심으로 한 final design.

`second_try`의 핵심 결론인 "vocabulary extension은 fragmentation을 줄였지만 original continued-pretraining control을 이기지 못했다"는 main claim이 아니라, high-resource replay, seed-stable multi-init, downstream evaluation이 필요한 이유로 사용한다.

## 한 줄 설계

`third_try`는 XLM-R-base를 대상으로 target10 vocab extension, high-resource replay + low-resource mixture, multi-init/3-seed full MLM, downstream evaluation을 수행하고, 기존 실험은 그 주변의 ablation study로 재배치한다.
