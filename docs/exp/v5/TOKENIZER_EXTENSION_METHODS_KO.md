# Tokenizer 확장 방법 정리

작성 시각: 2026-06-28 KST

이 문서는 v5 report/PPT에서 혼동되기 쉬운 tokenizer 확장 방법을 분리한다.
결론부터 말하면, **두 계열 모두 실험 흔적이 있고**, 현재 v5 본실험과
`v5_random`/`v5_fvt` 10K MLM은 **Glot500-style tokenizer 확장 산출물**로
돌렸다. Yamaguchi 계열은 이전 v1/v3의 prior attempt/ablation으로 남기고,
v5 novelty는 tokenizer 자체가 아니라 **확장 후 embedding initialization
비교**로 주장한다.

## 최종 판정

| 질문 | 답 |
| --- | --- |
| Glot500 방법을 해봤나? | 예. v4에서 이 방향으로 전환했고, v5 본실험 tokenizer는 이 방법으로 완성했다. |
| Yamaguchi 방법을 해봤나? | 예. v1/v3에서 target auxiliary tokenizer를 만들고 source tokenizer에 append하는 방식으로 실험했다. |
| 지금 v5 MLM/eval은 무엇으로 돌렸나? | Glot500-style tokenizer: `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm` |
| `v5_random`과 `v5_fvt`의 차이는 tokenizer인가? | 아니다. 둘은 같은 tokenizer를 쓰고, 새 embedding row 초기화만 다르다. |
| report/PPT에서 뭐라고 써야 하나? | "Tokenizer는 Glot500-style SPM 확장으로 고정하고, novelty는 Yamaguchi-style low-resource vocab expansion 문헌에서 중요한 embedding initialization을 XLM-R/Glot500 setting에서 비교했다." |

## 방법 1. Glot500-style tokenizer 확장

이 repo에서 말하는 Glot500-style은 `tokenization/run.py` 계열이다.

핵심 절차:

1. `xlm-roberta-base`의 base `sentencepiece.bpe.model`을 output directory에 복사한다.
2. 92 seen + 10 target으로 만든 v5 merged corpus에서 새 SentencePiece unigram
   model을 학습한다.
3. base XLM-R SentencePiece protobuf를 직접 열고, 새 SPM model에만 있는 piece를
   base model 뒤에 append한다.
4. piece score와 piece type을 보존한다.
5. merged SentencePiece model을 `XLMRobertaTokenizer`에 로드해 Hugging Face
   tokenizer directory로 저장한다.

v5에서 실제 사용한 command/script:

```bash
bash tokenization/train_v5_glot50010.sh
```

실제 입력/출력:

| 항목 | 값 |
| --- | --- |
| input corpus | `/home/axt/mnt2/jongha/v5_glot50010/data/Glot500_v5_glot50010_xlmr100.txt` |
| script | `tokenization/train_v5_glot50010.sh` |
| core runner | `tokenization/run.py` |
| base tokenizer | `xlm-roberta-base` |
| SPM vocab size argument | `250000` |
| final tokenizer | `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm` |
| appended token count | `118,685` |
| final HF tokenizer length | `368,687` |
| target byte token count | `256` |
| audit result | failure `0` |

중요한 구현상 특이사항:

- 기존 XLM-R SentencePiece piece를 유지하고 새 piece를 뒤에 붙이는 방식이다.
- `tokenization/run.py`는 현재 fork에서 `--byte_fallback=true`를 켜고, BYTE
  piece type도 보존한다.
- `<mask>` id는 XLM-R `250001`에서 v5 tokenizer `368686`으로 이동한다. 이
  이동은 embedding initialization audit에서 remap diff `0.0`으로 점검했다.
- 이 방법은 HF `add_tokens`만 쓰는 방식보다 SentencePiece model 내부에 새
  piece를 직접 통합한다는 점이 다르다.

v5 본실험 연결:

```text
v5_random, v5_mean, v5_fvt 초기화 checkpoint는 모두 같은 Glot500_extended_spm
tokenizer 위에서 만들어졌다. 따라서 after-MLM 비교에서 tokenizer는 control
변수가 아니라 고정 변수다.
```

## 방법 2. Yamaguchi-style low-resource vocabulary expansion

여기서 Yamaguchi 방법은 Atsuki Yamaguchi, Aline Villavicencio, Nikolaos
Aletras의 "How Can We Effectively Expand the Vocabulary of LLMs with
0.01GB of Target Language Text?"에서 온 low-resource vocabulary expansion
문제를 가리킨다. arXiv 메타데이터 기준 최초 등록일은 `2024-06-17`이고,
online date는 `2025-10-27`이다.

논문 관점의 핵심 절차:

1. target language data로 auxiliary tokenizer를 새로 학습한다.
2. source vocabulary에 없는 target token을 고른다.
3. source vocabulary와 새 token을 합쳐 target tokenizer/vocabulary를 만든다.
4. 새 embedding/output row를 random, mean, merge, align 등으로 초기화한다.
5. target language text로 continued pretraining을 수행한다.

이 repo에서의 구현/실험 대응:

| 위치 | 역할 |
| --- | --- |
| `scripts/train_target10_spm.py` | target10 전용 standalone SentencePiece unigram tokenizer 학습 |
| `scripts/merge_target10_with_glot500.py` | target10 SPM piece를 `cis-lmu/glot500-base` tokenizer에 append |
| `preprocessing/run_third_try_stage03_tokenizer.py` | v3 target-heavy auxiliary tokenizer를 만들고 XLM-R tokenizer에 append |
| `docs/exp/v3/03_tokenizer/` | v3 tokenizer candidate, id-preservation, fallback ablation 결과 |
| `docs/exp/v1/reference_summaries/2406.11477v3_low_resource_vocab_expansion.md` | Yamaguchi paper 요약 |

v3에서 실제로 확인된 결과:

| 항목 | 값 |
| --- | --- |
| selected candidate | `main_added_48000` |
| base model | `xlm-roberta-base` |
| auxiliary tokenizer vocab | `48000` |
| actual added tokens | `30,849` |
| extended vocab size | `280,851` |
| changed existing token ids | `0` |
| changed special token ids | `0` |
| appended token id violations | `0` |
| status | `PASS` |

주의할 점:

- v3 방식은 target-heavy auxiliary tokenizer의 selected token을
  `XLMRobertaTokenizer.add_tokens(...)`로 append하는 계열이다.
- 따라서 "target auxiliary tokenizer + source vocab append + embedding init
  탐구"라는 점에서 Yamaguchi-style이라고 부를 수 있다.
- 다만 논문은 decoder LLM/CLM 중심이고, 우리 repo는 XLM-R encoder/MLM과
  Glot500 evaluation으로 재해석한다. 그러므로 "Yamaguchi exact reproduction"
  보다는 "Yamaguchi-style vocabulary expansion/initialization baseline"이라고
  쓰는 편이 안전하다.

## v3, v4, v5 차이

| Version | Tokenizer 방향 | 해석 | 본선 여부 |
| --- | --- | --- | --- |
| v1 | target10 SPM + vocab-size/init 비교 | Yamaguchi-style pilot/prior attempt | 아니다 |
| v3 | target-heavy aux tokenizer + append-only/id-preserving XLM-R extension | Yamaguchi-style main attempt/ablation | 현재 v5 기준 prior attempt |
| v4 | `tokenization/run.py`로 Glot500-style rerun 방향 전환 | Glot500-style 재현 라인 시작 | v5로 정리됨 |
| v5 | 92 seen + 10 Glot500-internal target corpus로 `Glot500_extended_spm` 생성 | controlled Glot500-style 본실험 | 예 |

## 지금 결과를 읽는 법

`v5_random`과 `v5_fvt`는 tokenizer 방법 비교가 아니다.

```text
same corpus
+ same Glot500-style tokenizer
+ same MLM schedule
+ different new-row initialization
= embedding initialization comparison
```

따라서 현재 novelty 문장은 아래처럼 잡는 것이 좋다.

```text
We fix the tokenizer with a Glot500-style SentencePiece extension and compare
new-row embedding initialization strategies inspired by low-resource vocabulary
expansion literature.
```

한국어 발표 문장:

```text
토크나이저 확장은 Glot500 방식으로 고정했습니다. 즉 XLM-R의 SentencePiece
모델을 보존하고, 102개 언어 corpus에서 새로 학습한 piece 중 없는 것만 뒤에
붙였습니다. novelty는 tokenizer를 새로 제안하는 것이 아니라, 이렇게 늘어난
118,685개 embedding row를 random으로 둘지, 기존 source token 분해 기반으로
초기화할지 비교하는 데 있습니다.
```

## Evidence Map

| 근거 | 파일 |
| --- | --- |
| v5 tokenizer launch script | `tokenization/train_v5_glot50010.sh` |
| Glot500-style protobuf merge implementation | `tokenization/run.py` |
| v5 tokenizer train status | `docs/exp/v5/0_tokenizer/02_tokenizer_train/README.md` |
| v5 tokenizer audit | `docs/exp/v5/0_tokenizer/03_audit/main/results.md` |
| v5 vocab audit JSON | `docs/exp/v5/0_tokenizer/03_audit/main/vocab_audit.json` |
| v4 Glot500-style 전환 메모 | `docs/exp/v4/0_tokenizer/idea.md` |
| target10 standalone SPM script | `scripts/train_target10_spm.py` |
| target10-to-Glot500 merge script | `scripts/merge_target10_with_glot500.py` |
| v3 selected tokenizer | `docs/exp/v3/03_tokenizer/selected_main_tokenizer.md` |
| v3 merge report | `docs/exp/v3/03_tokenizer/merge_report.json` |
| Yamaguchi paper local summary | `docs/exp/v1/reference_summaries/2406.11477v3_low_resource_vocab_expansion.md` |
| Yamaguchi paper | <https://arxiv.org/abs/2406.11477> |

## Report/PPT에 넣을 짧은 결론

```text
두 tokenizer 확장 계열을 모두 검토했다. v1/v3에서는 Yamaguchi-style
low-resource vocabulary expansion처럼 target auxiliary tokenizer를 만들고
새 token을 append하는 방식을 실험했다. v4/v5에서는 Glot500 재현성을 위해
Glot500-style SentencePiece protobuf merge 방식으로 전환했다. 최종 v5
MLM/evaluation은 Glot500-style tokenizer 산출물인 Glot500_extended_spm으로
돌렸으며, random/FVT 비교는 tokenizer 비교가 아니라 동일 tokenizer 위의
embedding initialization 비교다.
```
