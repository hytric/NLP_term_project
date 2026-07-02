# Append-Only Tokenizer Protocol

작성일: 2026-06-18

## Purpose

`v3.1` must not replace the pretrained XLM-R tokenizer. The base tokenizer and all existing token ids stay fixed. A new tokenizer is trained only to discover useful low-resource/high-resource pieces. Only pieces absent from the original vocabulary are appended after the original vocabulary.

This protocol exists to avoid the common mistake:

> Train a new tokenizer on target data and use it as the model tokenizer.

That is not allowed for the main experiment because it changes existing token ids and destroys compatibility with pretrained embeddings.

## Main Rule

Allowed:

> Train an auxiliary tokenizer on low-resource + high-resource data, extract new pieces, and append only the new pieces to the original XLM-R vocabulary.

Forbidden:

> Replace `xlm-roberta-base` tokenizer with the newly trained tokenizer.

> Reorder existing pieces.

> Change special token ids.

> Reassign ids for existing XLM-R tokens.

## Data For Auxiliary Tokenizer Training

Train the auxiliary tokenizer on a mixture, not target-only text.

| Component | Purpose |
| --- | --- |
| target10 low-resource text | discover target-language pieces |
| high-resource replay text | keep segmentation compatible with existing multilingual space |
| related-language bridge text, if clean | help Coptic/Syriac and family/script neighbors |

The auxiliary tokenizer can use SentencePiece unigram, matching the XLM-R/Glot500-style setup. Its vocabulary is not used directly as the final tokenizer.

## Append-Only Merge Procedure

1. Load the original `xlm-roberta-base` tokenizer.
2. Dump and freeze `base_token -> base_id` for every existing token.
3. Train the auxiliary tokenizer on the low-resource + high-resource mixture.
4. Extract auxiliary pieces in deterministic order:
   - normally by SentencePiece score / rank;
   - with language/script quotas if needed.
5. Filter candidates:
   - remove any piece already in the base vocabulary;
   - remove special/control/meta tokens;
   - remove malformed pieces;
   - remove pieces that violate normalization rules;
   - remove byte-fallback pieces unless the actual XLM-R tokenizer path faithfully activates them.
6. Append filtered candidates after the final base vocabulary id.
   - SentencePiece merge path: append only new `(piece, score/type)` records after the original model pieces.
   - HuggingFace added-token path: add only new token strings as added tokens, then record their assigned ids.
   - In either path, old ids must remain byte-for-byte auditable.
7. Resize model embeddings to `base_vocab_size + appended_count`.
8. Initialize only appended rows using the selected initialization method.
9. Copy all old embedding rows and LM-head rows exactly.
10. Save tokenizer, model, merge report, and id-preservation audit.

## Required Audits

| Audit | Required check |
| --- | --- |
| base id preservation | every original token keeps the same id |
| special id preservation | `<s>`, `</s>`, `<unk>`, `<pad>`, `<mask>` unchanged |
| append range | every new token id is `>= base_vocab_size` |
| duplicate check | no appended token already exists in base vocab |
| row-copy audit | old embedding rows and LM-head rows have zero drift after resize |
| tokenizer behavior audit | high-resource sample tokenization does not sharply regress |
| target fertility audit | target10 tokens/word improves without severe per-language regression |
| file audit | saved tokenizer/model paths and checksums recorded |

## Merge Report Fields

`append_only_merge_report.tsv` should include:

| Field | Meaning |
| --- | --- |
| `base_vocab_size` | original XLM-R vocab size |
| `aux_vocab_size` | auxiliary tokenizer vocab size |
| `candidate_count` | pieces considered before filtering |
| `already_in_base_count` | removed because already present |
| `special_or_invalid_count` | removed for control/meta/invalid status |
| `appended_count` | final number of appended pieces |
| `first_appended_id` | should equal `base_vocab_size` |
| `last_appended_id` | final tokenizer id |
| `changed_existing_token_ids` | must be `0` |
| `changed_special_token_ids` | must be `0` |
| `appended_id_violations` | must be `0` |
| `append_method` | `sentencepiece_model_append` or `hf_added_tokens` |
| `appended_piece_list` | path to ordered appended `(piece, score/type, new_id)` list |

## Failure Conditions

Any of these fails the main experiment:

1. Existing XLM-R token ids change.
2. Special token ids change.
3. New tokenizer replaces the base tokenizer.
4. Old embedding rows drift after resize.
5. Appended ids are not contiguous after the base vocab.
6. The report cannot prove which pieces were appended.

## Claim Boundary

If this protocol passes, the report can say:

> The tokenizer extension is id-preserving and append-only; pretrained XLM-R lexical rows remain compatible with the original model.

It still cannot say:

> Existing model performance is guaranteed unchanged.

Preserving ids is necessary for retaining pretrained behavior, but continued training can still cause forgetting. That is why high-resource replay/control evaluation remains mandatory.
