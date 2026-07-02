# Main Initialization Audit

이 폴더는 full v5 tokenizer initialized checkpoint audits를 보관한다.

Required audit dimensions:

- source row copy by token identity
- `<mask>` remap
- byte-row and fallback accounting
- LM-head tying
- initialized-row counts

Promotion rule: no initialization method can be used in the main comparison
unless its audit report passes these checks.
