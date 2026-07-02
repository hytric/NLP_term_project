# v4 New Token Embedding Initialization Meeting Prep

Date: 2026-06-24

## One-Line Summary

v4의 tokenizer 생성은 Glot500 방식에 매우 가깝게 잘 진행됐다. 다만 현재 MLM run은 custom embedding initialization 없이 Hugging Face 기본 resize로 시작했기 때문에, 최종 방법론 run이 아니라 `random-resize baseline`으로 해석하는 것이 안전하다.

더 중요한 확인점은 `SentencePiece model` 관점에서는 append-only가 맞지만, `XLMRobertaTokenizer` id 관점에서는 `<mask>` id가 맨 뒤로 이동한다는 점이다. 따라서 embedding initialization 코드는 source/target tokenizer의 token id를 단순 prefix copy로 믿지 말고, token identity 기준으로 row를 복사하고 new token row를 초기화해야 한다.

## Meeting Goal

회의에서는 아래 두 가지를 분리해서 확인한다.

1. Target tokenizer 생성이 방법론과 일치하는가?
2. Target tokenizer의 token id에 대응하는 embedding/lm_head row가 의도한 방식으로 초기화되는가?

첫 번째는 현재 상태가 좋다. 두 번째는 v4용 명시적 checkpoint builder가 필요하다.

## Vocabulary Objects

- Source tokenizer: original LLM tokenizer. 현재 기준은 `xlm-roberta-base`.
- Auxiliary tokenizer: `92` seen language corpus와 `10` target10 corpus를 섞은 training corpus로 학습한 SentencePiece unigram tokenizer. 목적은 target vocab 후보 token과 score를 얻는 것이다.
- Target tokenizer: source SPM vocab을 보존하고, auxiliary tokenizer에 있지만 source vocab에는 없는 piece와 score를 source SPM 뒤에 append한 tokenizer.
- Embedding initialization: target tokenizer에 새로 생긴 token id에 대해 source tokenizer로 surface를 다시 분해하고, source embedding row들을 조합해 target embedding row를 만든다.

## Current v4 Evidence

실제 tokenizer audit 결과:

| Item | Value |
| --- | --- |
| source tokenizer length | `250002` |
| source SPM piece size | `250000` |
| target tokenizer length | `370433` |
| target SPM piece size | `370431` |
| new SPM pieces | `120431` |
| source `<mask>` id | `250001` |
| target `<mask>` id | `370432` |
| first target new token id | `250001`, token `<0x00>` |
| byte fallback pieces in target SPM | `256` |
| new piece type counts | `BYTE=256`, `NORMAL=120175` |
| new score range | `-20.607431` to `0.0` |
| SPM prefix append violations | `0` |

해석:

- SPM protobuf level에서는 source pieces가 그대로 prefix로 보존된다.
- `<s>`, `<pad>`, `</s>`, `<unk>`는 id가 유지된다.
- `<mask>`는 SPM 내부 piece가 아니라 tokenizer가 SPM size 뒤에 붙이는 special token이라 target tokenizer에서 마지막 id로 이동한다.
- 그래서 HF 기본 `resize_token_embeddings`는 source `<mask>` row를 target `<0x00>` row에 복사하고, target `<mask>` row는 random으로 둔다.

이 발견은 실험 설계를 약하게 만드는 것이 아니라, 오히려 v4 rerun을 더 정확하게 만들 수 있는 좋은 점검 포인트다.

## Code Map

| Method step | Code/artifact | What to inspect |
| --- | --- | --- |
| Auxiliary tokenizer training | `tokenization/run.py:38-53` | SentencePiece unigram, `--byte_fallback=true`, `--vocab_size=250000` |
| Append new pieces and scores | `tokenization/run.py:60-84` | `piece`, `score`, `type` are copied into base SPM |
| Save target tokenizer | `tokenization/run.py:89-96` | `Glot500_extended_spm` is saved from merged SPM |
| v4 MLM launch | `modeling/train_v4_target10_xlmr100.sh:36-43` | Starts from `xlm-roberta-base`, passes extended tokenizer |
| v4 model resize | `modeling/run.py:404-415` | Calls only `model.resize_token_embeddings(len(tokenizer))` |
| HF resize behavior | transformers 4.24.0 `modeling_utils.py:1301-1319` | Initializes new embedding module, then copies old rows by id prefix |
| XLM-R random init | transformers 4.24.0 `modeling_xlm_roberta.py:600-603` | Embedding rows use `normal_(mean=0.0, std=config.initializer_range)` |
| Prior fvt implementation | `docs/exp/v1/14_v2_embedding_init/run_step14.py:124-210` | Source-token decomposition mean, copy to input embedding and LM head |
| Older simple mean script | `scripts/init_target10_embeddings.py:19-47` | Useful formula, but v4 needs mask-id remapping fix |

## Inserted Code Comments

회의 때 코드에서 바로 확인할 수 있도록 아래 위치에 한국어 주석을 삽입했다.

| File/line | Inserted note |
| --- | --- |
| `modeling/run.py:408-412` | 현재 학습 경로는 Glot500 방식의 vocab 확장이며, 기존 row는 유지하고 새 row는 random init으로 추가한다. 여기서는 `fvt/mean/align` custom 초기화를 하지 않는다. SPM protobuf를 직접 수정한 tokenizer는 `<mask>` id 이동 가능성이 있으므로 special token id audit이 필요하다. |
| `modeling/run.py:414-416` | 실제 실행 지점은 `model.resize_token_embeddings(len(tokenizer))`이다. |
| `docs/exp/v1/14_v2_embedding_init/run_step14.py:140-143` | Step14 tokenizer는 HF `add_tokens()` 방식이라 base id와 special id가 보존되고, new row는 `base_vocab_size`부터 시작한다. SPM protobuf append tokenizer는 token 문자열 기준 row remap이 필요하다. |
| `docs/exp/v1/14_v2_embedding_init/run_step14.py:177-179` | 과거 Step14 설정에서는 `<mask>` 포함 기존 source row가 `resize_token_embeddings` 단계에서 이미 복사되어 있어야 하며, loop는 `add_tokens()` layout에서 새로 생긴 row만 초기화한다. |
| `scripts/init_target10_embeddings.py:29-31` | 이 helper는 HF `add_tokens()` layout을 가정한다. SPM protobuf append tokenizer에는 그대로 쓰면 안 되고, `<mask>` id 이동을 먼저 remap해야 한다. |

## What Current v4 Training Did

`modeling/train_v4_target10_xlmr100.sh` starts like this:

```bash
modeling/run.py \
  --model_name_or_path xlm-roberta-base \
  --tokenizer_name /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm
```

Then `modeling/run.py` does:

```python
if len(tokenizer) > embedding_size:
    model.resize_token_embeddings(len(tokenizer))
```

In transformers 4.24.0, this means:

1. Make a new embedding table of size `370433`.
2. Randomly initialize all rows.
3. Copy old rows `0:250002` from XLM-R.
4. Tie weights again.

Because target id `250001` is `<0x00>` and source id `250001` was `<mask>`, this copy is not enough for v4. Current checkpoint-30000/40000 results are still valuable, but they are best labeled as a random-resize and mask-row-drift baseline.

## Prior fvt Method

Prior Step14 `fvt` logic:

1. For each target-only token id, get token string from target tokenizer.
2. Convert SentencePiece whitespace marker: `token.replace("▁", " ").strip()`.
3. Tokenize that surface with source tokenizer.
4. Convert source subtokens to source ids.
5. Initialize the target input embedding row as the mean of those source embedding rows.
6. Copy the same vector to LM head.
7. Call `model.tie_weights()`.
8. Audit missing/zero rows and source row preservation.

Step14 selected `fvt` over alternatives by zero-step Mark/dev MLM:

- selected method: `fvt`
- v3 selected checkpoint: `/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt`
- zero-step Mark/dev MLM loss: `7.925527`
- `fallback_rows=0`, `missing_rows=0` in that setting

Important caveat: Step14 used a different tokenizer construction path. v4 uses direct SPM protobuf append, so the `<mask>` id movement must be handled explicitly.

## Recommended v4 Initialization Algorithm

Preferred implementation location: a standalone checkpoint builder, for example `scripts/init_v4_embeddings.py` or `preprocessing/init_v4_embeddings.py`.

The training script should then start from the initialized checkpoint, not from raw `xlm-roberta-base`.

Algorithm:

1. Load `source_tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")`.
2. Load `target_tokenizer = XLMRobertaTokenizer.from_pretrained(Glot500_extended_spm)`.
3. Load `model = AutoModelForMaskedLM.from_pretrained("xlm-roberta-base")`.
4. Resize model to `len(target_tokenizer)`.
5. Copy source rows by token identity where the source and target token are the same.
6. Explicitly copy source `<mask>` row to target `<mask>` id.
7. For each target token id that is not in source vocab and is not `<mask>`, initialize:

```python
surface = target_token.replace("▁", " ").strip()
source_ids = source_tokenizer.convert_tokens_to_ids(source_tokenizer.tokenize(surface))
source_ids = [i for i in source_ids if isinstance(i, int) and i not in source_tokenizer.all_special_ids]
vector = source_embedding[source_ids].mean(dim=0) if source_ids else fallback_vector
target_embedding[target_id].copy_(vector)
target_lm_head[target_id].copy_(vector)
```

8. Decide byte fallback handling:
   - simplest defensible option: initialize `<0xNN>` rows from source `<unk>` or base mean and report them separately;
   - stronger option: decode the byte when valid UTF-8 or map printable bytes through source tokenizer;
   - do not silently treat byte rows as ordinary lexical pieces.
9. Call `model.tie_weights()`.
10. Save model, tokenizer, and an `init_report.json`.

## Four Initialization Methods

미팅에서 우선 비교할 초기화 방법론은 아래 네 가지로 정리한다.

| Method | Formula | Role | Main risk |
| --- | --- | --- | --- |
| `random` | `resize_token_embeddings()`가 만든 random row를 그대로 사용 | Glot500-style baseline | custom embedding init 주장을 대표하지 못함 |
| `mean` | 모든 new token row를 source embedding 전체 평균으로 초기화 | 안정적인 단순 baseline | token별 surface 정보가 사라짐 |
| `fvt` | target new token surface를 source tokenizer로 다시 tokenize하고, source subtoken embedding 평균을 사용 | 현재 가장 중요한 main candidate | `<unk>`/special id와 byte piece 처리를 명시해야 함 |
| `align` | target token surface의 문자 단위 정보를 source tokenizer의 single-character token row와 맞춰 평균 | unsupported script 보완 후보 | 문자 row가 없으면 fallback이 많아질 수 있음 |

`focus`, `fvt + norm`, `score-aware`는 main 4개에는 넣지 않고 확장 후보로 둔다. v4 main rerun 추천안은 `fvt`에 `<mask>` remap, byte-piece report, norm/stat audit을 붙이는 것이다. 현재 v4 run은 `random` baseline으로 보존한다.

## Code Sketch For Four Methods

아래 코드는 회의용 sketch이다. 핵심은 method별 vector 계산 전에 `source_tokenizer`와 `target_tokenizer`의 token id가 같은지 가정하지 않고, 먼저 `<mask>`와 공통 token row를 token 문자열 기준으로 맞추는 것이다.

```python
# 01. token 문자열에서 tokenizer별 boundary marker를 제거해 문자 단위 비교용 body를 만든다.
def token_body(token: str) -> str:
    # 02. ▁는 SentencePiece 공백 marker, Ġ/</w>는 다른 tokenizer 계열 marker라 함께 제거한다.
    return token.replace("▁", "").replace("Ġ", "").replace("</w>", "").strip()


# 03. source tokenizer vocab에서 single-character token을 찾아 char -> source id 목록을 만든다.
def build_char_to_source_ids(source_tokenizer, source_vocab_size: int) -> dict[str, list[int]]:
    # 04. 같은 문자에 대응하는 source token id가 여러 개일 수 있으므로 list로 저장한다.
    char_to_ids: dict[str, list[int]] = {}
    # 05. source tokenizer의 token 문자열과 id를 모두 순회한다.
    for token, idx in source_tokenizer.get_vocab().items():
        # 06. 정상 int id가 아니거나 source vocab 범위를 넘는 row는 제외한다.
        if not isinstance(idx, int) or idx >= source_vocab_size:
            # 07. 조건에 맞지 않는 token은 align 후보로 쓰지 않는다.
            continue
        # 08. token marker를 제거한 실제 문자 body를 얻는다.
        body = token_body(token)
        # 09. body가 정확히 한 글자일 때만 character alignment 후보로 사용한다.
        if len(body) == 1:
            # 10. 해당 문자에 source id를 추가한다.
            char_to_ids.setdefault(body, []).append(idx)
    # 11. align method에서 사용할 문자 -> source id map을 반환한다.
    return char_to_ids


# 12. fvt에서 사용할 source subtoken id 목록을 만든다.
def source_subtoken_ids(source_tokenizer, surface: str, source_vocab_size: int) -> list[int]:
    # 13. target token surface를 source tokenizer로 다시 tokenize하고 id로 바꾼다.
    ids = source_tokenizer.convert_tokens_to_ids(source_tokenizer.tokenize(surface))
    # 14. source vocab 안에 있고 special token이 아닌 id만 남긴다.
    return [
        # 15. 조건을 통과한 source subtoken id를 평균 embedding 후보로 사용한다.
        idx for idx in ids
        # 16. tokenizer가 반환한 값이 실제 int id인지 확인한다.
        if isinstance(idx, int)
        # 17. source embedding table 안쪽 row만 허용한다.
        and 0 <= idx < source_vocab_size
        # 18. <s>, <pad>, </s>, <unk>, <mask> 같은 special id는 제외한다.
        and idx not in source_tokenizer.all_special_ids
    ]


# 19. align에서 사용할 character-level source id 목록을 만든다.
def align_char_ids(surface: str, char_to_ids: dict[str, list[int]]) -> list[int]:
    # 20. target token surface의 각 문자에 대응하는 source id를 담을 list다.
    ids: list[int] = []
    # 21. target token surface를 문자 단위로 순회한다.
    for ch in surface:
        # 22. 해당 문자의 source single-character id가 있으면 첫 번째 후보만 사용한다.
        ids.extend(char_to_ids.get(ch, [])[:1])
    # 23. align vector를 만들 때 평균 낼 source id 목록을 반환한다.
    return ids


# 24. v4 target tokenizer에 맞춰 embedding/lm_head row를 초기화한다.
def initialize_v4_rows(model, source_tokenizer, target_tokenizer, method: str) -> dict[str, int]:
    # 25. input embedding table을 직접 수정하기 위해 weight tensor를 가져온다.
    input_emb = model.get_input_embeddings().weight.data
    # 26. MLM output head도 input embedding과 같은 vector로 맞추기 위해 가져온다.
    output_emb = model.get_output_embeddings().weight.data
    # 27. source tokenizer 전체 vocab 길이를 source row 범위로 사용한다.
    source_vocab_size = len(source_tokenizer)
    # 28. target tokenizer 전체 vocab 길이를 target row 범위로 사용한다.
    target_vocab_size = len(target_tokenizer)
    # 29. resize 이후 row가 덮이더라도 원본 source row를 보존하기 위해 clone한다.
    source_rows = input_emb[:source_vocab_size].clone()
    # 30. mean/fallback 초기화에 사용할 source embedding 평균 vector를 만든다.
    source_mean = source_rows.mean(dim=0)
    # 31. align method를 위해 source single-character token map을 준비한다.
    char_to_ids = build_char_to_source_ids(source_tokenizer, source_vocab_size)

    # 32. 공통 token row 복사 개수를 기록한다.
    copied_common = 0
    # 33. target-only new row 초기화 개수를 기록한다.
    initialized_new = 0
    # 34. fvt/align에서 source 후보가 없어 fallback을 쓴 row 개수를 기록한다.
    fallback_rows = 0

    # 1) 공통 token은 id prefix가 아니라 token 문자열 기준으로 복사한다.
    # 35. source tokenizer vocab의 모든 token을 순회한다.
    for token, source_id in source_tokenizer.get_vocab().items():
        # 36. 같은 token 문자열이 target tokenizer에서 어떤 id인지 찾는다.
        target_id = target_tokenizer.convert_tokens_to_ids(token)
        # 37. source/target id가 모두 정상 int이면 같은 token row로 간주한다.
        if isinstance(source_id, int) and isinstance(target_id, int) and target_id >= 0:
            # 38. target input embedding row에 source token vector를 복사한다.
            input_emb[target_id].copy_(source_rows[source_id])
            # 39. target LM head row에도 같은 source token vector를 복사한다.
            output_emb[target_id].copy_(source_rows[source_id])
            # 40. 공통 token 복사 카운트를 증가시킨다.
            copied_common += 1

    # 2) XLM-R <mask>는 SPM protobuf append에서 id가 뒤로 이동할 수 있으므로 명시적으로 복사한다.
    # 41. source tokenizer에서 <mask> id를 가져온다.
    source_mask_id = source_tokenizer.mask_token_id
    # 42. target tokenizer에서 이동 후의 <mask> id를 가져온다.
    target_mask_id = target_tokenizer.mask_token_id
    # 43. source <mask> input embedding을 target <mask> row로 복사한다.
    input_emb[target_mask_id].copy_(source_rows[source_mask_id])
    # 44. source <mask> LM head row도 target <mask> row로 복사한다.
    output_emb[target_mask_id].copy_(source_rows[source_mask_id])

    # 3) target에만 있는 row를 method별로 초기화한다.
    # 45. target-only token인지 빠르게 확인하기 위해 source vocab dict를 저장한다.
    source_vocab = source_tokenizer.get_vocab()
    # 46. target tokenizer의 모든 id를 순회한다.
    for target_id in range(target_vocab_size):
        # 47. 현재 target id에 대응하는 token 문자열을 얻는다.
        target_token = target_tokenizer.convert_ids_to_tokens(target_id)
        # 48. source에도 있는 token이거나 <mask>면 이미 복사했으므로 건너뛴다.
        if target_token in source_vocab or target_id == target_mask_id:
            # 49. 공통 token과 <mask>는 new-row 초기화 대상이 아니다.
            continue

        # 50. SentencePiece 공백 marker를 실제 공백으로 바꿔 source tokenizer 입력 surface를 만든다.
        surface = target_token.replace("▁", " ").strip()

        # 51. random: resize_token_embeddings가 만든 random vector를 그대로 둔다.
        if method == "random":
            # 52. 현재 target row에 이미 들어 있는 random vector를 사용한다.
            vector = input_emb[target_id].clone()
        # 53. mean: 모든 new token을 source embedding 전체 평균으로 초기화한다.
        elif method == "mean":
            # 54. token별 정보 없이 안정적인 global mean vector를 사용한다.
            vector = source_mean
        # 55. fvt: target token surface를 source tokenizer subtoken들로 분해한다.
        elif method == "fvt":
            # 56. source tokenizer가 만든 non-special source subtoken id를 가져온다.
            ids = source_subtoken_ids(source_tokenizer, surface, source_vocab_size)
            # 57. source subtoken이 있으면 그 embedding 평균을 사용한다.
            if ids:
                # 58. source subtoken embedding들의 평균 vector가 fvt 초기값이다.
                vector = source_rows[ids].mean(dim=0)
            # 59. source subtoken이 없으면 fallback으로 source mean을 사용한다.
            else:
                # 60. fallback vector로 global mean을 사용한다.
                vector = source_mean
                # 61. fallback 발생 row를 기록한다.
                fallback_rows += 1
        # 62. align: target token의 문자들을 source single-character token row와 맞춘다.
        elif method == "align":
            # 63. surface 문자별 source single-character id를 찾는다.
            ids = align_char_ids(surface, char_to_ids)
            # 64. character alignment 후보가 있으면 그 embedding 평균을 사용한다.
            if ids:
                # 65. 문자 단위 source embedding 평균이 align 초기값이다.
                vector = source_rows[ids].mean(dim=0)
            # 66. 문자 후보가 없으면 fvt 후보를 한 번 더 시도한다.
            else:
                # 67. align 실패 시 fvt source subtoken id를 fallback 후보로 사용한다.
                fvt_ids = source_subtoken_ids(source_tokenizer, surface, source_vocab_size)
                # 68. fvt 후보가 있으면 fvt 평균, 없으면 source mean을 사용한다.
                vector = source_rows[fvt_ids].mean(dim=0) if fvt_ids else source_mean
                # 69. align fallback 발생 row를 기록한다.
                fallback_rows += 1
        # 70. 정의하지 않은 method 이름은 실험 설정 오류로 처리한다.
        else:
            # 71. 오타나 미등록 method를 조용히 넘기지 않고 즉시 실패시킨다.
            raise ValueError(f"unknown init method: {method}")

        # 72. 계산한 vector를 target input embedding row에 쓴다.
        input_emb[target_id].copy_(vector)
        # 73. 같은 vector를 target LM head row에도 쓴다.
        output_emb[target_id].copy_(vector)
        # 74. 초기화 완료한 target-only row 개수를 증가시킨다.
        initialized_new += 1

    # 75. input embedding과 LM head weight tying을 다시 보장한다.
    model.tie_weights()
    # 76. audit/report에 사용할 핵심 count를 반환한다.
    return {
        # 77. token 문자열 기준으로 복사한 source/target 공통 row 수다.
        "copied_common_rows": copied_common,
        # 78. method별로 새로 초기화한 target-only row 수다.
        "initialized_new_rows": initialized_new,
        # 79. fvt/align source 후보가 없어 fallback을 사용한 row 수다.
        "fallback_rows": fallback_rows,
    }
```

## Required Audits

Before training:

- tokenizer audit: source and target lengths, SPM sizes, special ids, first/last 20 ids
- append-only SPM audit: source SPM piece prefix unchanged
- row-copy audit: unchanged source tokens have identical vectors after init
- mask audit: `target_embedding[target_mask_id] == source_embedding[source_mask_id]`
- new-row audit: no NaN, no zero norm, fallback count reported
- byte fallback audit: 256 byte rows accounted for separately
- decomposition report: sample new tokens with source subtokens and source ids
- LM head audit: input embedding and LM head tied or exactly synchronized
- zero-step MLM proxy: compare initialized checkpoint vs current random-resize baseline

After training starts:

- record first checkpoint as initialized rerun, not mixed with old run
- keep current v4 checkpoint-30000/40000 as `random_resize_baseline`
- use same corpus, masking seed, max length, batch schedule, and evaluation scripts

## Meeting Agenda

1. Confirm that target tokenizer generation is acceptable:
   - mixed `92 seen + 10 target10` corpus
   - auxiliary SPM supplies new piece and score
   - protobuf append preserves score and type

2. Confirm that current v4 MLM run is a baseline:
   - useful result
   - not the final custom embedding initialization run
   - affected by random new rows and moved `<mask>` row

3. Decide the v4 initialization formula:
   - main: `fvt`
   - fallback for byte pieces
   - whether to add norm rescaling
   - whether to use SPM score only for reporting or also for scaling

4. Decide code location:
   - standalone checkpoint builder is easier to audit
   - training launcher then points to initialized checkpoint

5. Decide rerun protocol:
   - build initialized checkpoint
   - run zero-step MLM proxy
   - if audit passes, restart continued MLM from that checkpoint

## Decision Needed

Use the current v4 run as a baseline. For the methodologically correct v4 run, build an explicit initialized checkpoint from `xlm-roberta-base + Glot500_extended_spm`, with token-identity row copy, `<mask>` remapping, and fvt initialization for new lexical rows. Then train from that checkpoint with the same tokenizer and same MLM schedule.
