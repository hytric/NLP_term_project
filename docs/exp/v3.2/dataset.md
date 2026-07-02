# V3.2 Dataset Status

작성일: 2026-06-19

## Purpose

이 문서는 `v3.2`에서 사용할 현재 데이터셋 상태를 정리한다.

`v3.2`의 1차 목표는 다음이다.

> high-resource language source를 최대한 활용해서 low-resource target10의 Pseudoperplexity / MLM Intrinsic Evaluation 성능을 올린다.

따라서 데이터셋도 translation이나 retrieval 중심이 아니라, 먼저 **MLM proxy task 개선** 관점에서 정리한다.

## Current Data Root

현재 materialized text root:

```text
/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1
```

v3.1 experiment artifact root:

```text
/home/axt/mnt2/jongha/v3_1
```

주요 문서/manifest:

| Artifact | Path | Role |
| --- | --- | --- |
| materialized text manifest | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/materialized_text_manifest.tsv` | MLM/tokenizer text file inventory |
| parallel item manifest | `docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv` | item-aligned target/high-resource Bible rows |
| split manifest | `docs/exp/v3.1/01_embedding_alignment/split_manifest.tsv` | language/split row counts and target10 overlap |
| translation data manifest | `docs/exp/v3.1/03_decoder_translation/translation_data_manifest.tsv` | available pair files |
| MLM training manifest | `docs/exp/v3.1/04_ablation/init_mlm_probe/training_manifest.tsv` | v3.1 200-step MLM runs |
| MLM protocol | `docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_training_protocol.md` | chunking/masking/training details |

## Dataset Layers

현재 데이터는 네 층위로 나뉜다.

| Layer | Main Files | Used For | Current Status |
| --- | --- | --- | --- |
| target10 low-resource Bible text | `target10_train_clean.txt`, `target10_dev.txt`, `target10_final_test.txt` | target MLM eval, tokenizer adaptation, retrieval/translation pairs | small but clean core target data |
| high-resource GlotCC replay/source | `glotcc_eng-Latn.txt`, `glotcc_deu-Latn.txt`, `glotcc_jpn-Jpan.txt`, `glotcc_kor-Hang.txt` | large high-resource MLM source | underused as transfer engine in v3.1 |
| high-resource Bible domain control | `bible_control_eng/deu/jpn/kor.txt` | domain-matched high-resource source | important for Bible-style transfer |
| aligned item manifests/pair files | `parallel_item_manifest.tsv`, `translation_pairs/*.tsv` | retrieval, contrastive/TLM, translation diagnostics | available and should be reused |

## Materialized Text Files

| File | Lines | Bytes | Size | Role |
| --- | ---: | ---: | ---: | --- |
| `target10_train_clean.txt` | `52,016` | `11,254,917` | `11M` | low-resource target train text |
| `target10_dev.txt` | `6,521` | `1,256,857` | `1.2M` | low-resource dev/eval text |
| `target10_final_test.txt` | `9,804` | `2,079,693` | `2.0M` | low-resource held-out final text |
| `glotcc_eng-Latn.txt` | `200,000` | `45,093,808` | `44M` | English high-resource web source |
| `glotcc_deu-Latn.txt` | `200,000` | `48,376,780` | `47M` | German high-resource web source |
| `glotcc_jpn-Jpan.txt` | `200,000` | `89,612,681` | `86M` | Japanese high-resource web source |
| `glotcc_kor-Hang.txt` | `200,000` | `86,642,707` | `83M` | Korean high-resource web source |
| `bible_control_eng.txt` | `28,538` | `3,831,531` | `3.7M` | English Bible-domain control |
| `bible_control_deu.txt` | `28,538` | `3,774,420` | `3.7M` | German Bible-domain control |
| `bible_control_jpn.txt` | `28,523` | `4,861,284` | `4.7M` | Japanese Bible-domain control |
| `bible_control_kor.txt` | `28,537` | `4,093,512` | `4.0M` | Korean Bible-domain control |
| `mlm_train_full_mixture.txt` | `966,152` | `297,541,640` | `284M` | v3.1 MLM train mixture |
| `tokenizer_train_balanced.txt` | `488,064` | `124,449,235` | `119M` | balanced tokenizer training text |

## V3.1 MLM Train Mixture

`mlm_train_full_mixture.txt` is the actual train file used by the v3.1 init MLM probe.

Composition:

| Component | Lines | Share | Role |
| --- | ---: | ---: | --- |
| target10 low-resource train | `52,016` | `5.3838%` | direct target adaptation |
| GlotCC eng/deu/jpn/kor | `800,000` | `82.8027%` | high-resource web source/replay |
| Bible eng/deu/jpn/kor control | `114,136` | `11.8135%` | high-resource domain-matched source |
| high-resource total | `914,136` | `94.6162%` | source/replay/retention |
| total | `966,152` | `100.0000%` | full MLM train mixture |

Current reading:

- v3.1 already has a high-resource-heavy raw mixture by line count.
- But the v3.1 run used only `200 * 32 = 6,400` train chunks, about epoch `0.05`.
- Therefore high-resource data existed, but was not exploited as a long training transfer source.
- target10 direct exposure was also very small under that short schedule.

For v3.2, the issue is not simply "add high-resource data"; the issue is:

> use high-resource source at larger scale while ensuring weak target scripts still get enough repeated exposure to improve low-resource content-token MLM.

## Tokenizer Training Mixture

`tokenizer_train_balanced.txt` was built separately from the full MLM train mixture.

Construction from `materialize_third_try_training_texts.py`:

| Component | Lines | Share | Rule |
| --- | ---: | ---: | --- |
| target10 train repeated | `208,064` | `42.6305%` | `52,016 * 4` |
| GlotCC capped | `200,000` | `40.9782%` | `50,000` per high-resource config |
| Bible control capped | `80,000` | `16.3913%` | `20,000` per high-resource language |
| high-resource total | `280,000` | `57.3695%` | GlotCC + Bible control |
| total | `488,064` | `100.0000%` | balanced tokenizer train text |

Current reading:

- tokenizer training was more target-balanced than MLM training.
- target10 was intentionally repeated for tokenizer coverage.
- structural append-only tokenizer audit passed in v3.1.
- However, content-token MLM still failed for `chr/cop/oji`, so tokenizer structure alone is insufficient.

## Target10 Languages

| ISO | Language | Script | Current Risk |
| --- | --- | --- | --- |
| `acu` | Achuar-Shiwiar | Latin | low content-token performance, but nonzero |
| `ake` | Akawaio | Latin | relatively stronger among target10 |
| `bsn` | Barasana-Eduria | Latin | low content-token performance, but nonzero |
| `chr` | Cherokee | Cherokee | urgent content-token failure |
| `cop` | Coptic | Coptic | urgent content-token and retrieval bottleneck |
| `kbh` | Camsa | Latin | low content-token performance, but nonzero |
| `nhg` | Nahuatl Tetelcingo | Latin | low content-token performance, but nonzero |
| `oji` | Ojibwa | Aboriginal Syllabics | urgent content-token failure |
| `syr` | Syriac | Syriac | urgent retrieval bottleneck; content-token weak |
| `usp` | Uspanteco | Latin | relatively stronger among target10 |

Risk labels come from `v3.1/05_additional`:

- `chr/cop/oji` had structured-init content-token top-10 equal to `0`.
- `syr/cop` had the weakest source/target centered-CSLS retrieval macro behavior.

## Target10 Split Counts

The materialized target10 text files use unique text rows:

| Split | Lines | Role |
| --- | ---: | --- |
| train | `52,016` | MLM target adaptation, tokenizer training, translation train pool |
| dev | `6,521` | MLM intrinsic eval and retrieval dev feature cache |
| final_test | `9,804` | held-out final diagnostics |

Per-language unique item counts from `parallel_item_manifest.tsv`:

| ISO | Train | Dev | Final Test | Burned Excluded |
| --- | ---: | ---: | ---: | ---: |
| `acu` | `5,170` | `659` | `953` | `864` |
| `ake` | `5,179` | `673` | `1,003` | `879` |
| `bsn` | `5,103` | `629` | `959` | `857` |
| `chr` | `5,393` | `678` | `1,007` | `879` |
| `cop` | `5,394` | `678` | `1,006` | `879` |
| `kbh` | `4,511` | `501` | `852` | `657` |
| `nhg` | `5,273` | `673` | `1,006` | `870` |
| `oji` | `5,384` | `674` | `1,007` | `878` |
| `syr` | `5,390` | `678` | `1,007` | `879` |
| `usp` | `5,327` | `678` | `1,007` | `878` |

Important note:

`parallel_item_manifest.tsv` has raw row counts that can be larger than unique item counts for dev/final target10 rows. For example, `acu` dev has `1,318` raw rows but `659` unique items. Use unique item counts for retrieval/eval examples and materialized text line counts. Use raw rows only when auditing manifest lineage.

## Split Semantics

The split lineage comes from the v2 clean split and Bible item ids.

From `build_v31_parallel_items.py`:

| Book | Split |
| --- | --- |
| `MAR` | dev |
| `ACT` | final_test |
| all other books | train |

From `materialize_third_try_training_texts.py`:

| Held-out Books | Use |
| --- | --- |
| `ACT`, `MAR`, `JOH` | excluded from high-resource Bible control train text |

Current implication:

- target10 dev/final are Bible book-based, not random row splits.
- high-resource Bible control text skips `ACT/MAR/JOH`, reducing direct held-out book leakage.
- `JOH` is treated as held out/excluded in materialized high-resource control even though `build_v31_parallel_items.py` maps non-`MAR`/`ACT` books to train by default. This should be kept explicit in v3.2 to avoid accidental leakage.

## Parallel Item Manifest

`docs/exp/v3.1/01_embedding_alignment/parallel_item_manifest.tsv`

Total rows:

| Role | Raw Rows | Chars |
| --- | ---: | ---: |
| target10 low-resource | `93,297` | `13,829,094` |
| high-resource control | `124,392` | `11,621,433` |
| total | `217,689` | `25,450,527` |

Split summary:

| Split | Raw Rows | Unique Items |
| --- | ---: | ---: |
| train | `169,776` | `30,637` |
| dev | `15,754` | `678` |
| final_test | `23,639` | `1,007` |
| burned_excluded | `8,520` | `879` |

Target10 shared overlap:

| Split | Shared item count |
| --- | ---: |
| train | `3,029` |
| dev | `456` |
| final_test | `782` |
| burned_excluded | `625` |

Current use:

- target10-wide sentence retrieval uses dev feature caches from target10 dev rows.
- contrastive/TLM-style v3.2 alignment should use same `item_id` positives.
- final-test should remain untouched for checkpoint selection.

## High-Resource Source Inventory

Current high-resource languages:

| ID | Language | Script | Source Types | Current Lines |
| --- | --- | --- | --- | ---: |
| `eng` / `eng-Latn` | English | Latin | GlotCC + Bible XML | `228,538` train-mixture lines |
| `deu` / `deu-Latn` | German | Latin | GlotCC + Bible XML | `228,538` train-mixture lines |
| `jpn` / `jpn-Jpan` | Japanese | Japanese | GlotCC + Bible XML | `228,523` train-mixture lines |
| `kor` / `kor-Hang` | Korean | Hangul | GlotCC + Bible XML | `228,537` train-mixture lines |

Current source paths:

| Source Type | Path Pattern |
| --- | --- |
| GlotCC JSONL source | `/home/axt/mnt2/jongha/third_try/high_resource/glotcc/glotcc_{config}.jsonl` |
| materialized GlotCC text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/glotcc_{config}.txt` |
| raw Bible XML | `/home/axt/mnt2/jongha/Glot500-py39-eval/data/raw/bible-corpus/bibles/{English,German,Japanese,Korean}.xml` |
| materialized Bible control text | `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/bible_control_{iso}.txt` |

V3.2 interpretation:

- These four languages are the current high-resource transfer backbone.
- Domain-matched Bible control is likely more valuable for pseudoPPL on target10 Bible text than generic web data alone.
- GlotCC source gives scale and general LM stability.
- v3.2 should record sampling ratios explicitly in `high_resource_source_manifest.tsv`.

## Translation Pair Files

Translation pairs live under:

```text
/home/axt/mnt2/jongha/v3_1/translation_pairs
```

Current pair manifest:

| Direction | Train | Dev | Final Test | Status |
| --- | ---: | ---: | ---: | --- |
| `cop -> syr` | `5,389` | `678` | `1,006` | PASS |
| `syr -> cop` | `5,389` | `678` | `1,006` | PASS |
| `eng -> acu` | `4,004` | `659` | `953` | PASS |
| `acu -> eng` | `4,004` | `659` | `953` | PASS |
| `eng -> ake` | `4,051` | `673` | `1,003` | PASS |
| `ake -> eng` | `4,051` | `673` | `1,003` | PASS |
| `eng -> bsn` | `3,924` | `629` | `959` | PASS |
| `bsn -> eng` | `3,924` | `629` | `959` | PASS |
| `eng -> chr` | `5,393` | `678` | `1,007` | PASS |
| `chr -> eng` | `5,393` | `678` | `1,007` | PASS |
| `eng -> cop` | `5,392` | `678` | `1,006` | PASS |
| `cop -> eng` | `5,392` | `678` | `1,006` | PASS |
| `eng -> kbh` | `3,469` | `501` | `852` | PASS |
| `kbh -> eng` | `3,469` | `501` | `852` | PASS |
| `eng -> nhg` | `5,272` | `673` | `1,006` | PASS |
| `nhg -> eng` | `5,272` | `673` | `1,006` | PASS |
| `eng -> oji` | `4,174` | `674` | `1,007` | PASS |
| `oji -> eng` | `4,174` | `674` | `1,007` | PASS |
| `eng -> syr` | `5,390` | `678` | `1,007` | PASS |
| `syr -> eng` | `5,390` | `678` | `1,007` | PASS |
| `eng -> usp` | `5,326` | `678` | `1,007` | PASS |
| `usp -> eng` | `5,326` | `678` | `1,007` | PASS |

Current use:

- `cop <-> syr` is the project-specific translation diagnostic.
- `eng <-> target10` can be used as high-resource bridge/pivot diagnostics.
- For v3.2 MLM proxy improvement, pair files are not the first target, but they are useful for TLM/contrastive alignment after MLM.

Pair alignment caution:

- A quick sample check showed `cop <-> syr` examples such as `b.1CO.11.1` are semantically plausible.
- A quick sample check also showed suspicious `eng -> acu` examples around `1CO`, where the English `item_id` text and Achuar text appear possibly offset or mismatched.
- This is not yet a full audit, but `eng <-> target10` pair files should not be used as TLM/contrastive supervision until a pair-alignment sample audit is completed.
- This caution is less relevant for plain MLM over monolingual high-resource source, but it matters for semantic pair objectives.

## Feature Cache Data

v3.1 already materialized MLM-dev feature caches:

```text
/home/axt/mnt2/jongha/v3_1/mlm_dev_feature_similarity
```

Cache manifest:

```text
docs/exp/v3.1/04_ablation/init_mlm_probe/mlm_dev_feature_cache_manifest.tsv
```

Shape:

- embedding dimension: `768`;
- examples per target language: `501` to `678`;
- models include `xlmr_base`, zero-step inits, and `mlm200` variants.

Current use:

- v3.1 sentence retrieval and CSLS diagnostics use these caches.
- v3.2 should regenerate feature caches for every selected MLM/alignment checkpoint.

## POS Data

Current POS evidence is Coptic-only:

| Artifact | Path |
| --- | --- |
| Coptic POS raw results | `docs/exp/v3.1/05_additional/coptic_pos_results_replay_safe.tsv` |
| Coptic POS summary | `docs/exp/v3.1/05_additional/coptic_pos_summary_replay_safe.tsv` |
| Coptic POS label metrics | `docs/exp/v3.1/05_additional/coptic_pos_label_metrics_replay_safe.tsv` |

Current status:

- useful as a Coptic supervised POS pilot;
- not target10-wide;
- not Glot500-style English-to-target zero-shot POS;
- should remain downstream diagnostic only.

## Current Evaluation Sets

### MLM Intrinsic

Current v3.1 settings:

| Eval | Data | Size | Notes |
| --- | --- | ---: | --- |
| dynamic MLM dev loss | `target10_dev.txt` | `701` chunked samples | dynamic `15%` MLM mask |
| sampled pseudoPPL | target10 dev rows from `parallel_item_manifest.tsv` | first `50` dev rows/language in original run | strict one-token masking |
| top-k content diagnostic | target10 dev rows | first `20` dev rows/language in v3.1 diagnostic | separates content tokens from boundary/punctuation |

V3.2 requirement:

- fixed-mask dev set should be materialized;
- content-token metrics should be primary;
- all-token pseudoPPL should be secondary;
- `xlmr_base` pseudoPPL should not be used as direct expanded-tokenizer quality comparison.

### Sentence Retrieval

Current v3.1 setting:

| Eval | Data | Scope | Notes |
| --- | --- | --- | --- |
| target10 centered-CSLS retrieval | MLM-dev feature caches | `90` directed language pairs | weak R@1 around `0.9%-1.2%` |
| Coptic-Syriac retrieval | translation split dev/final | `cop <-> syr` | useful decoder-link diagnostic |

V3.2 requirement:

- report source-language and target-language macro;
- separate retrieval from MLM proxy success;
- do not select MLM checkpoint by retrieval alone unless Stage 03 alignment is being selected.

## Known Dataset Risks

| Risk | Evidence | V3.2 Handling |
| --- | --- | --- |
| target10 is tiny relative to high-resource source | only `52,016` target train lines in `966,152` MLM mixture | oversample target10/weak scripts while keeping high-resource scale |
| high-resource source existed but was not exploited by training length | v3.1 consumed only `6,400` chunks | longer high-resource-source-augmented MLM schedule |
| all-token metrics are contaminated | `▁` and punctuation dominate several tokenizations | content-token metrics required |
| `chr/cop/oji` content tokens fail | top-10 content-token hit is `0` in v3.1 structured average | weak-script focused sampling/eval |
| `syr/cop` retrieval bottleneck | lowest source/target centered-CSLS behavior | explicit language breakdown |
| possible split confusion across manifests | raw rows and unique items differ in `parallel_item_manifest.tsv` | always state whether count is raw rows or unique items |
| possible item-id/text mismatch in some bridge pairs | quick sample check flagged suspicious `eng -> acu` `1CO` examples | audit `eng <-> target10` pairs before TLM/contrastive use |
| held-out book leakage risk | high-resource control excludes `ACT/MAR/JOH`, while item split maps `MAR` dev and `ACT` final | keep split policy explicit in v3.2 manifests |

## V3.2 Dataset Actions

### P0

1. Create `high_resource_source_manifest.tsv`.
   - list all high-resource sources;
   - record line counts, byte size, domain type, script, and sampling ratio.

2. Create fixed-mask target10 dev set.
   - use target10 dev only;
   - preserve language ids and item ids;
   - include content-token category labels if possible.

3. Create weak-script sampling plan.
   - prioritize `chr/cop/oji/syr`;
   - report actual sampled chunks per language;
   - avoid letting high-resource source erase target script exposure.

4. Preserve final-test isolation.
   - no checkpoint selection on `target10_final_test.txt`;
   - no alignment checkpoint selection on final-test pair files.

### P1

1. Build TLM/contrastive pair datasets from `parallel_item_manifest.tsv`.
2. Add high-resource bridge pairs such as `eng <-> target10`.
3. Run pair-alignment sample audit before using `eng <-> target10` pairs as semantic supervision.
4. Add data quality examples for weak scripts.
5. Add per-language Unicode normalization audit.

## Recommended V3.2 Dataset Contract

Every v3.2 run should record:

| Field | Reason |
| --- | --- |
| source file path | reproducibility |
| source role | target, high-resource web, high-resource Bible, pair/alignment |
| language/script | language-level breakdown |
| raw rows used | sample accounting |
| unique item ids used | retrieval/alignment accounting |
| sampled chunks by language | MLM exposure accounting |
| final-test usage flag | leakage control |
| high-resource/target ratio | central v3.2 hypothesis |
