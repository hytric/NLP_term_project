# 03 Tokenizer Audit

Use this folder for tokenizer audits:

- base/extended vocab size
- appended token count
- special token id audit, especially `<mask>`
- byte fallback piece count
- target10 fertility and `<unk>` rate
- head/tail tokenization comparison

Canonical command:

```bash
python3 scripts/audit_v5_tokenizer.py
```

This command requires the v5 extended tokenizer to exist first.

Current pilot audit:

```text
docs/exp/v5/0_tokenizer/03_audit/pilot10k/results.md
```

Pilot finding:

- appended token count: `7,591`
- byte token count: `256`
- `<mask>` id moved from `250001` to `257592`
- `9/10` target languages improved tokens/word
- `dzo_Tibt` regressed and needs analysis before the main tokenizer claim

Pilot `dzo_Tibt` analysis:

```text
pilot10k/examples_dzo/analysis.md
```

Key interpretation: the regression is not byte fallback or `<unk>` behavior.
The pilot v5 tokenizer overuses newly appended short Tibetan pieces, so main
tokenizer claims must recheck `dzo_Tibt`.

Current main audit:

```text
docs/exp/v5/0_tokenizer/03_audit/main/results.md
```

Main finding:

- appended token count: `118,685`
- byte token count: `256`
- `<mask>` id moved from `250001` to `368686`
- audited languages: `20` head + `10` target
- audit failures: `0`
- `29/30` audited languages improved tokens/word
- target10 average delta: `-0.390862`
- target10 excluding `dzo_Tibt` average delta: `-0.581867`
- head sample average delta: `-0.211765`
- `dzo_Tibt` remains worse: `4.223938` -> `5.552124` tokens/word

Main `dzo_Tibt` analysis:

```text
main/examples_dzo/examples.md
main/examples_dzo/summary.tsv
```

Key interpretation: full tokenizer training reduces the pilot `dzo_Tibt`
regression but does not remove it. On `500` examples, main v5 `dzo_Tibt` has
delta `+1.115844`, `0` byte tokens, `0` `<unk>` tokens, and `86.981%` newly
appended-token share. Treat `dzo_Tibt` as a documented tokenizer-risk case
rather than as a clean tokenization win.

## Next Step Gate

Move to `../../1_embedding/` only after tokenizer behavior is measured and
known risks are documented.

Pass line:

- base vocab size, extended vocab size, and appended token count are recorded.
- source `<mask>` id and target `<mask>` id are recorded.
- byte fallback rows are counted separately from lexical rows.
- target10 fertility and `<unk>` rate are summarized.
- head/seen control languages are checked for large tokenization regressions.
- audit conclusion says either `pass` or `pass with documented risk`.

Required artifacts:

- tokenizer audit table
- special-token id table
- fertility and `<unk>` table
- head/tail comparison table
- short `results.md` or equivalent summary

If `<mask>` id movement or byte-row behavior is unresolved, embedding
initialization must explicitly account for it before training.

Current status: pass with documented risk (`dzo_Tibt`).
