# Results: Target10 Standalone Vocabulary Extension

작성일: 2026-06-03

## Setup

Trained a standalone joint SentencePiece unigram tokenizer for the 10-language pilot.

Config:

- Input: `data/processed/target10/target10_train_for_tokenizer.txt`
- Train lines loaded: 61,900
- Too-long lines skipped: 31
- Vocab size: 16,000
- Model type: unigram
- Character coverage: 1.0

Artifacts:

- `data/processed/target10/spm_16k/target10_unigram_16k.model`
- `data/processed/target10/spm_16k/target10_unigram_16k.vocab`

## Glot500 vs Target10 SPM16K

| ISO | Language | Script | Glot500 tokens/word | Target10 tokens/word | Reduction | Glot500 single-char % | Target10 single-char % |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| cop | Coptic | Coptic | 5.274 | 1.776 | 66.3% | 67.7 | 15.9 |
| syr | Syriac | Syriac | 5.089 | 1.593 | 68.7% | 80.3 | 20.1 |
| chr | Cherokee | Cherokee | 5.254 | 2.000 | 61.9% | 77.2 | 37.8 |
| oji | Ojibwa | Aboriginal Syllabics | 5.021 | 2.212 | 55.9% | 87.0 | 38.9 |
| bsn | Barasana-Eduria | Latin | 3.045 | 1.602 | 47.4% | 32.7 | 24.2 |
| kbh | Camsa | Latin | 3.259 | 1.765 | 45.8% | 27.3 | 21.9 |
| acu | Achuar-Shiwiar | Latin | 2.515 | 1.670 | 33.6% | 18.7 | 18.1 |
| ake | Akawaio | Latin | 2.846 | 2.068 | 27.3% | 53.1 | 34.6 |
| nhg | Nahuatl (Tetelcingo) | Latin | 2.191 | 1.582 | 27.8% | 17.0 | 17.3 |
| usp | Uspanteco | Latin | 2.196 | 1.963 | 10.6% | 33.9 | 36.6 |

## Interpretation

The 10-language tokenizer sharply reduces fragmentation for the non-Latin or unsupported-script languages.

The strongest improvements are:

- Syriac: 68.7% tokens/word reduction
- Coptic: 66.3% reduction
- Cherokee: 61.9% reduction
- Ojibwa: 55.9% reduction

This validates the project direction: a joint low-resource vocabulary is useful before model adaptation.

## Next Step

## Glot500 Merge

The target10 vocabulary was merged into the Glot500 tokenizer.

Artifacts:

- `data/processed/target10/glot500_target10_spm16k/sentencepiece.bpe.model`
- `data/processed/target10/glot500_target10_spm16k/tokenizer_config.json`
- `data/processed/target10/glot500_target10_spm16k/special_tokens_map.json`
- `data/processed/target10/glot500_target10_spm16k/merge_report.json`
- `docs/exp/2026-06-03_03_vocab_extension/glot500_target10_bible_tokenization_examples.md`
- `docs/exp/2026-06-03_03_vocab_extension/glot500_target10_tokenization_examples.md`
- `docs/exp/2026-06-03_03_vocab_extension/glot500_target10_sample_tokenization_metrics.tsv`

Merge summary:

| Item | Value |
| --- | ---: |
| Base Glot500 pieces | 401,143 |
| Target10 pieces | 16,000 |
| Added pieces | 13,994 |
| Merged pieces | 415,137 |

즉 target10 tokenizer는 16,000개 vocab으로 학습했지만, 그중 일부 piece는 기존 Glot500 vocab에 이미 존재했다.
중복 piece를 제외하고 실제로 새로 추가된 piece는 **13,994개**다.
그 결과 tokenizer vocabulary는 기존 **401,143개**에서 merge 후 **415,137개**로 증가했다.

발표에서는 다음처럼 설명하면 된다.

> target10 SentencePiece tokenizer를 16k vocab으로 학습한 뒤 Glot500 tokenizer에 merge했다.
> 기존 Glot500에 이미 있던 piece를 제외하면 실제 추가된 token은 13,994개이며, tokenizer size는 401,143개에서 415,137개로 늘어났다.

The merged tokenizer preserves the standalone target10 gains while staying compatible with Glot500-style model loading.

| ISO | Glot500 tokens/word | Merged tokens/word | Reduction | Merged single-char % |
| --- | ---: | ---: | ---: | ---: |
| cop | 5.274 | 1.779 | 66.3% | 15.2 |
| syr | 5.089 | 1.601 | 68.5% | 18.4 |
| chr | 5.254 | 2.001 | 61.9% | 37.4 |
| oji | 5.021 | 2.205 | 56.1% | 37.9 |
| bsn | 3.045 | 1.577 | 48.2% | 23.5 |
| kbh | 3.259 | 1.669 | 48.8% | 18.0 |
| acu | 2.515 | 1.599 | 36.4% | 16.8 |
| ake | 2.846 | 2.023 | 28.9% | 34.6 |
| nhg | 2.191 | 1.495 | 31.8% | 14.7 |
| usp | 2.196 | 1.899 | 13.5% | 35.7 |

## Tokenization Examples After Extension

확장 후 tokenizer 샘플도 추가로 뽑았다.

- `glot500_target10_bible_tokenization_examples.md`: target10 Bible train 문장에서 기존 Glot500과 확장 tokenizer를 같은 문장으로 비교한 발표용 before/after 예시
- `glot500_target10_tokenization_examples.md`: 기존 `docs/exp/2026-06-03_02_tokenization_audit/tokenization_examples.md`와 같은 `data/processed/samples/coptic_audit.txt`, `syriac_audit.txt` 샘플 기준으로 확장 tokenizer만 다시 뽑은 예시
- `glot500_target10_sample_tokenization_metrics.tsv`: 기존 audit sample 기준 확장 tokenizer metric

주의할 점:
기존 `coptic_audit.txt` 샘플은 target10 Bible Coptic과 source/domain이 달라서, 확장 후에도 Coptic top-worst 예시는 여전히 문자 단위 fragmentation이 많이 남는다.
반면 target10 Bible 기준 before/after 예시에서는 Coptic과 Syriac 모두 token 수 감소가 명확하다.

발표에서는 `glot500_target10_bible_tokenization_examples.md`를 쓰는 것이 좋다.
예를 들어 Coptic 예시는 Glot500 36 tokens에서 확장 후 10 tokens로 줄고, Syriac 예시는 Glot500 27 tokens에서 확장 후 6 tokens로 줄어드는 식으로 같은 문장 비교가 가능하다.

## Next Step

Initialize the added token embeddings and run the first controlled model experiment:

- no extension
- extension + random init
- extension + mean init

Align init remains the high-value stretch condition.

## Note: Relation To `tokenization/`

이번 target10 tokenizer 실험은 repository의 `tokenization/run.py`를 직접 실행한 것이 아니다.
실제로 사용한 코드는 아래 두 스크립트다.

- `scripts/train_target10_spm.py`: target10 Bible train text로 SentencePiece unigram 16k tokenizer 학습
- `scripts/merge_target10_with_glot500.py`: 학습된 target10 SentencePiece piece를 `cis-lmu/glot500-base` tokenizer에 merge

방법의 큰 틀은 `tokenization/run.py`와 비슷하다.
둘 다 SentencePiece unigram tokenizer를 학습하고, 기존 SentencePiece model protobuf에 새 piece를 append한 뒤 `XLMRobertaTokenizer` 형태로 저장한다.

하지만 실험 설정과 목적은 다르다.

| Item | `tokenization/run.py` | Target10 experiment |
| --- | --- | --- |
| Directly used here | No | Yes, via `scripts/` |
| Input corpus | Full Glot500 corpus path in the original defaults | `data/processed/target10/target10_train_for_tokenizer.txt` |
| Base tokenizer | XLM-R SentencePiece model prepared in `save_directory` | `cis-lmu/glot500-base` tokenizer |
| New tokenizer vocab size | Default 250,000 | 16,000 |
| Byte fallback | Enabled with `--byte_fallback=true` | Not enabled in the target10 script |
| Purpose | Large Glot500-style tokenizer extension | Small controlled target10 vocabulary-extension pilot |

So the answer is: same family of method, but not the same code path.
The target10 results in this folder should be attributed to `scripts/train_target10_spm.py` and `scripts/merge_target10_with_glot500.py`, not to `tokenization/run.py`.
