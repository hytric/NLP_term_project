# 02 Tokenizer Train

Use this folder for tokenizer training commands, logs, process ids, and output
path notes.

Expected output root:

```text
/home/axt/mnt2/jongha/v5_glot50010/tokenization/output
```

Current main tokenizer result:

```text
PASS, full corpus, VOCAB_SIZE=250000, appended 118,685 tokens
```

Main artifacts:

- `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500.model`
- `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500.vocab`
- `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm.model`
- `/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/Glot500_extended_spm/`
- `logs/train_v5_tokenizer_20260627_000941.log`

Main training notes:

- SentencePiece sampled `20,000,000` sentences from `92,309,510` valid lines.
- `142,722` too-long lines were skipped by SentencePiece.
- The extended tokenizer has `368,687` HF tokens.
- `<mask>` moved from XLM-R id `250001` to main tokenizer id `368686`.

Important prerequisite:

```text
/home/axt/mnt2/jongha/v5_glot50010/tokenization/output/sentencepiece.bpe.model
```

`tokenization/run.py` reads this file as the base XLM-R SentencePiece model to
extend. Copy it from `XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")`
before launching tokenizer training.

Canonical command:

```bash
bash tokenization/train_v5_glot50010.sh
```

Pilot command:

```bash
EXP_NAME=Glot500_v5_glot50010_xlmr100_pilot10k \
  OUTPUT_DIR=/home/axt/mnt2/jongha/v5_glot50010/tokenization/pilot10k_output \
  bash tokenization/train_v5_glot50010.sh
```

## Next Step Gate

Move to `../03_audit/` only after the extended tokenizer can be loaded and its
training record is complete.

Pass line:

- tokenizer command, input corpus path, and vocab size are written.
- base XLM-R `sentencepiece.bpe.model` is present in the save directory.
- SentencePiece model and Hugging Face tokenizer files exist.
- tokenizer loads with `AutoTokenizer.from_pretrained(...)`.
- base tokenizer name and extended tokenizer output path are recorded.
- training log has no fatal errors or silent fallback to another corpus.

Required artifacts:

- launch command
- tokenizer output path note
- stdout/stderr or log file
- produced tokenizer files list
- expected vs actual vocab size note

If tokenizer loading fails, do not proceed to embedding initialization. Fix here
first, then run the audit.

Current status: main tokenizer loads and the main audit is available in
`../03_audit/main/`.
