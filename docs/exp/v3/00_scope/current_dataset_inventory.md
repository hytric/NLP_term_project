# Current Dataset Inventory

작성일: 2026-06-12

## Storage Roots

| Root | Status | Notes |
| --- | --- | --- |
| `/home/axt/jongha/Glot500-py39-eval/data` | symlink | points to `/disk1/axt/jongha/Glot500-py39-eval/data` |
| `/home/axt/mnt2/jongha/Glot500-py39-eval/data` | available | main large dataset root confirmed |
| `/home/axt/mnt2/jongha/second_try` | available | prior artifacts/checkpoints, about 72G |
| `/home/axt/mnt2/jongha/hf_cache` | available | XLM-R/LaBSE/MiniLM caches, about 2.3G |

## Main Target10 Raw Bible Data

Source root:

`/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles`

| ISO | Language | Script | Raw XML | Verse rows |
| --- | --- | --- | --- | --- |
| `acu` | Achuar-Shiwiar | Latin | `Achuar-NT.xml` | 7646 |
| `ake` | Akawaio | Latin | `Akawaio-NT.xml` | 7734 |
| `bsn` | Barasana-Eduria | Latin | `Barasana-NT.xml` | 7548 |
| `chr` | Cherokee | Cherokee | `Cherokee-NT.xml` | 7957 |
| `cop` | Coptic | Coptic | `Coptic-NT.xml` | 7957 |
| `kbh` | Camsa | Latin | `Camsa-NT.xml` | 6521 |
| `nhg` | Nahuatl (Tetelcingo) | Latin | `Nahuatl-NT.xml` | 7822 |
| `oji` | Ojibwa | Aboriginal Syllabics | `Ojibwa-NT.xml` | 7943 |
| `syr` | Syriac | Syriac | `Syriac-NT.xml` | 7954 |
| `usp` | Uspanteco | Latin | `Uspanteco-NT.xml` | 7890 |

Confirmed manifest:

- `docs/exp/second_try/01_data_and_splits/target_languages.tsv`
- `/home/axt/mnt2/jongha/Glot500-py39-eval/data/processed/target10/target_languages.tsv`

## Target10 Existing Splits

### V1 split

Docs:

- `docs/exp/second_try/01_data_and_splits/split_stats.tsv`
- `docs/exp/second_try/01_data_and_splits/target10_bible_verses.tsv`

Large artifacts:

- `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/mlm/target10_mlm_train.tsv`
- `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/mlm/target10_mlm_dev.tsv`
- `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/downstream/target10_downstream_source.tsv`
- `/home/axt/mnt2/jongha/second_try/artifacts/01_data_and_splits/tokenizer/target10_train_all.txt`

V1 row counts:

| File | Rows |
| --- | --- |
| `target10_bible_verses.tsv` | 76973 |
| `target10_downstream_source.tsv` | 76973 |
| `target10_mlm_train.tsv` | 61932 |
| `target10_mlm_dev.tsv` | 6522 |

### V2 clean split

Docs:

- `docs/exp/second_try/12_v2_split_protocol/v2_split_manifest.tsv`
- `docs/exp/second_try/12_v2_split_protocol/v2_split_stats.tsv`
- `docs/exp/second_try/12_v2_split_protocol/v2_final_test_act_clean.tsv`

Large artifacts:

- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_tokenizer_mlm_train.txt`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_mlm_dev_mark.txt`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_final_test_act_clean.txt`
- `/home/axt/mnt2/jongha/second_try/artifacts/12_v2_split_protocol/v2_burned_john_excluded.txt`

V2 row counts:

| Split artifact | Rows |
| --- | --- |
| `v2_split_manifest.tsv` | 76973 |
| `v2_tokenizer_mlm_train.txt` | 52124 |
| `v2_mlm_dev_mark.txt` | 6521 |
| `v2_burned_john_excluded.txt` | 8520 |
| `v2_final_test_act_clean.txt` | 9804 |

V2 split is the safer starting point for `third_try` because it excludes the previously burned John test and reserves ACT as clean final test.

## High-Resource Bible Candidates

Source root:

`/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles`

| Candidate | XML | Verse rows | Notes |
| --- | --- | --- | --- |
| English | `English.xml` | 31102 | high-resource replay/control candidate |
| English WEB | `English-WEB.xml` | 31102 | alternate English Bible |
| German | `German.xml` | 31102 | high-resource replay/control candidate |
| Japanese | `Japanese.xml` | 31087 | high-resource replay/control candidate |
| Japanese tokenized | `Japanese-tok.xml` | 31087 | tokenized alternate |
| Korean | `Korean.xml` | 31102 | high-resource replay/control candidate |
| Greek | `Greek.xml` | 31102 | useful for Coptic/Syriac pivot/reference, optional |
| Latin | `Latin.xml` | 31211 | useful ancient-language reference, optional |

Full candidate summary:

- Full Bible entries in metadata: 60.
- Full Bible entries with speaker count >= 1M: 54.
- Core recommended replay/control set: English, German, Japanese, Korean.
- Detailed inventory: `high_resource_inventory.tsv`.

## High-Resource Web Corpus

Source:

- `cis-lmu/GlotCC-V1`

Materialized root:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc`

Manifest:

`/home/axt/mnt2/jongha/third_try/high_resource/glotcc/high_resource_glotcc_manifest.tsv`

| Config | File | Lines | Docs | Size | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `eng-Latn` | `glotcc_eng-Latn.jsonl` | 200000 | 11274 | 69 MB | PASS |
| `deu-Latn` | `glotcc_deu-Latn.jsonl` | 200000 | 9573 | 72 MB | PASS |
| `jpn-Jpan` | `glotcc_jpn-Jpan.jsonl` | 200000 | 20555 | 111 MB | PASS |
| `kor-Hang` | `glotcc_kor-Hang.jsonl` | 200000 | 14732 | 109 MB | PASS |

This is the current true high-resource web replay sample. Bible high-resource data remains domain-matched replay/control.

Current gap:

- High-resource raw Bible XML and GlotCC web JSONL samples exist.
- A third_try high-resource + target10 MLM mixture manifest does not yet exist and should be built in Stage 01.

## Other Downstream Or Diagnostic Data

| Dataset | Path | Status | Notes |
| --- | --- | --- | --- |
| UD Coptic Scriptorium | `/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/UD_Coptic-Scriptorium` | available | train/dev/test conllu present |
| Processed UD Coptic sentences | `/home/axt/mnt2/jongha/Glot500-py39-eval/data/processed/ud_coptic_sentences.tsv` | available | derived sentence table |
| Taxi1500 English | `/home/axt/mnt2/jongha/Glot500-py39-eval/download/taxi1500` | available | `eng_train/dev/test.tsv` only |
| Coptic/Syriac aligned Bible | `/home/axt/mnt2/jongha/Glot500-py39-eval/data/processed/bible_cop_syr_grc_eng_aligned.tsv` | available | useful for retrieval/alignment/NMT diagnostics |
| NMT Coptic/Syriac variants | `/home/axt/mnt2/jongha/Glot500-py39-eval/data/processed/nmt_*` | available | diagnostic/proxy, not main downstream by itself |

## Existing Tokenizer And Model Artifacts

Second_try tokenizer artifacts:

- `/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer/tokenizers/xlmr_v2_target10_added_8000`
- `/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer/tokenizers/xlmr_v2_target10_added_16000`
- `/home/axt/mnt2/jongha/second_try/artifacts/13_v2_tokenizer/tokenizers/xlmr_v2_target10_added_32000`

Second_try model/checkpoint artifacts:

- `/home/axt/mnt2/jongha/second_try/checkpoints/04_embedding_init/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/14_v2_embedding_init/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/15_v2_mlm_control/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/18_v2_added_token_repair/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/19_v2_new_row_only_repair/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/20_v2_staged_added_token_repair/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/21_v2_alt_init_mlm_probe/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/23_v2_vocab_size_objective_probe/`
- `/home/axt/mnt2/jongha/second_try/checkpoints/25_v2_8k_continued_budget_probe/`

These are reusable for audit, ablation, and implementation shortcuts. For third_try main claims, new high-resource + low-resource mixture runs should be produced or prior artifacts must be clearly marked as ablation.

## Stage 00/01 Implications

1. Target10 data exists and should remain the main low-resource set.
2. Coptic/Syriac are already present in target10 and have additional diagnostic resources.
3. V2 split should be preferred over V1 for clean final evaluation.
4. High-resource Bible XML is available for English, German, Japanese, and Korean.
5. True high-resource GlotCC web replay samples are materialized for English, German, Japanese, and Korean.
6. The missing main artifact is a third_try-specific high-resource + target10 mixture manifest.
7. Taxi1500 currently appears English-only locally, so target10 downstream success should not rely on Taxi1500 alone.
