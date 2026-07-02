# Stage 00 Results: Append-Only Tokenizer Audit

작성일: 2026-06-18

Gate status: `PASS_STRUCTURAL_TOKENIZER_AUDIT`

## Candidate

| Item | Value |
| --- | --- |
| base tokenizer | `xlm-roberta-base` |
| candidate tokenizer | `/home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt` |
| append method | `hf_added_tokens` |
| base vocab size | `250002` |
| candidate vocab size | `280851` |
| appended tokens | `30849` |
| first appended id | `250002` |
| last appended id | `280850` |

## Audit Result

| Check | Expected | Actual | Status |
| --- | ---: | ---: | --- |
| base id preservation | `0` changed ids | `0` | PASS |
| missing base tokens | `0` | `0` | PASS |
| special id preservation | `0` changed ids | `0` | PASS |
| appended ids after base vocab | `0` violations | `0` | PASS |
| append ids contiguous | `0` gaps/mismatches | `0` | PASS |
| candidate vocab ids unique | `0` duplicates | `0` | PASS |
| candidate vocab ids complete | `0` missing ids | `0` | PASS |
| appended token count | `>0` | `30849` | PASS |

## Command

```bash
python3 preprocessing/audit_v31_append_only_tokenizer.py \
  --candidate-tokenizer /home/axt/mnt2/jongha/third_try/checkpoints/04_init/xlmr_v2_48000_fvt \
  --output-dir docs/exp/v3.1/00_tokenizer_audit
```

## Artifacts

| Artifact | Path |
| --- | --- |
| merge report | `docs/exp/v3.1/00_tokenizer_audit/append_only_merge_report.tsv` |
| id audit | `docs/exp/v3.1/00_tokenizer_audit/id_preservation_audit.tsv` |
| special-token audit | `docs/exp/v3.1/00_tokenizer_audit/special_id_audit.tsv` |
| appended token list | `docs/exp/v3.1/00_tokenizer_audit/appended_piece_list.tsv` |
| changed existing ids | `docs/exp/v3.1/00_tokenizer_audit/changed_existing_token_ids.tsv` |

## Interpretation

The current third_try tokenizer candidate is structurally valid for `v3.1`: it keeps every original XLM-R token id unchanged and appends all new tokens after the base vocabulary.

This proves compatibility of the tokenizer id mapping. It does not by itself prove that high-resource model quality is unchanged after continued training, so high-resource replay/control evaluation remains required.
