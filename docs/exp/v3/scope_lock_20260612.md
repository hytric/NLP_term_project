# Third Try Scope Lock

작성일: 2026-06-12

이 파일은 프로젝트 수행 직전 사용자 확인으로 고정된 범위다. 기존 `third_try` 문서의 Glot500-style 원칙은 유지하되, 최종 목표는 target10 실제 성능 개선 모델과 논문 novelty 확보로 조정한다.

## Locked User Decisions

| Item | Decision |
| --- | --- |
| Final objective | 실제 성능 개선 모델을 생성하고, novelty를 통해 논문 작성 |
| Low-resource target set | 기존 target10을 최대한 유지 |
| Main target languages | `acu`, `ake`, `bsn`, `chr`, `cop`, `kbh`, `nhg`, `oji`, `syr`, `usp` |
| Coptic/Syriac | main experiment에 포함 |
| High-resource data | low-resource target과 동시에 사용해야 하며 이것이 핵심 설계 |
| Base model | `xlm-roberta-base` only |
| Scale baseline | `xlm-roberta-large` 사용하지 않음 |
| Success criterion | downstream 개선까지 필요 |
| Compute budget | 1 GPU로 며칠 규모 |
| Embedding initialization | 여러 embedding vector initialization 방법을 사용 |
| Seeds | 3개 이상 seed 시도 |
| Document language | 한국어 중심 |

## Updated Main Contract

`third_try`의 main은 Glot500에서 배운 id-preserving vocabulary extension과 multilingual replay 원칙을 target10 low-resource setting에 맞게 적용하는 것이다. Low-resource target10만을 최종 성능 개선 대상으로 두되, high-resource replay/control data를 training mixture에 반드시 포함한다.

## Main Versus Ablation

Main에 포함:

- target10 전체, 특히 Coptic/Syriac 포함
- high-resource + low-resource simultaneous training mixture
- XLM-R-base baseline
- id-preserving vocabulary append
- 여러 embedding initialization method 비교
- 3개 이상 seed
- downstream 개선 평가

Ablation/diagnostic으로 둠:

- high-resource replay 없이 target-only로 학습한 run
- seed 1개짜리 빠른 pilot
- tokenizer metric만 있고 downstream이 없는 결과
- `xlm-roberta-large` 비교
- target10 밖의 추가 언어 확장

## Novelty Direction

논문 novelty는 "Glot500을 그대로 복제했다"가 아니라, 아래 조합을 target10 low-resource setting에서 통제 실험으로 보이는 데 둔다.

1. High-resource replay와 low-resource target을 동시에 사용하는 vocabulary extension adaptation.
2. XLM-R id를 보존하는 append-only tokenizer 확장.
3. 여러 embedding initialization 방법의 seed-stable 비교.
4. Tokenization 개선이 downstream 개선으로 이어지는 조건과 실패 조건 분석.
5. Coptic/Syriac 같은 unsupported-script case를 main evidence로 포함.
