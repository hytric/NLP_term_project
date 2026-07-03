# v5.2 Experiments Setup - PPT Draft

## Slide 1. Experiment Goal

**Question**

Glot500-style vocabulary expansion에서 새로 추가된 token embedding row를 어떻게
초기화하느냐가 low-resource tail language adaptation에 영향을 주는가?

**Main hypothesis**

`FVT` initialization은 새 token을 random하게 시작하지 않고, 기존 XLM-R subtoken
embedding을 조합해 시작하므로 더 안정적인 adaptation을 제공할 수 있다.

**Takeaway sentence**

```text
This experiment isolates the effect of new-token embedding initialization under
the same corpus, tokenizer, and MLM schedule.
```

## Slide 2. Experimental Scope

**Glot500-style compact rerun**

| Item | Setup |
| --- | --- |
| Corpus universe | 99 language-script units |
| Seen replay | 92 XLM-R-seen languages |
| Tail targets | 7 XLM-R-unseen languages |
| Target definition | XLM-R-unseen tail + smallest corpus band with downstream coverage |
| Main method | Glot500-style SentencePiece unigram + append-only vocab injection |
| Main comparison | `random` vs `mean` vs `fvt` initialization |

**Presenter note**

Strict `<=10k` corpus languages did not provide enough downstream coverage.
Therefore, v5.2 defines the target set as XLM-R-unseen tail languages in the
minimum corpus band where downstream evaluation is still possible.

## Slide 3. Target7 Selection

**Target languages**

| Language-script | Language | Region | Corpus size | Main coverage |
| --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Southeast Asia | 48,468 | Tatoeba, Bible, Roundtrip |
| `xav_Latn` | Xavante | South America | 31,765 | Bible, Roundtrip, POS |
| `bam_Latn` | Bambara | West Africa | 32,150 | Bible, Roundtrip, POS |
| `csb_Latn` | Kashubian | Europe | 33,743 | Tatoeba, NER |
| `ile_Latn` | Interlingue | Constructed/Europe | 40,984 | Tatoeba |
| `lij_Latn` | Ligurian | Europe | 42,447 | NER, POS |
| `fur_Latn` | Friulian | Europe | 30,052 | NER |

**Selection logic**

- All target languages are unseen by XLM-R.
- All target languages have Glot500 corpus.
- The set maximizes downstream task overlap using only 7 target languages.
- All targets use `Latn` script, so v5.2 does not claim script diversity.

## Slide 4. Data Split And Sampling

**A. MLM train set**

| Item | Value |
| --- | ---: |
| Language-script units | 99 = 92 seen + 7 target |
| Source raw sentences | 1,025,895,043 |
| Target7 raw sentences | 259,609 |
| MLM train merge lines | 4,482,259 |
| Seen/head samples | 4,147,176 |
| Target7 samples | 335,083 |
| Language sampling alpha | 0.3 |

**B. Dataset And Evaluation Size Summary**

| Split / task | Scope | Count |
| --- | --- | ---: |
| MLM train seen/head | 92 XLM-R-seen replay languages | 4,147,176 samples |
| MLM train target7 | 7 XLM-R-unseen tail targets | 335,083 samples |
| MLM train total | 99 language-script units | 4,482,259 samples |
| PPPL target pool | Target7, 100 samples per language | 700 samples |
| Tatoeba retrieval | `dtp`, `ile`, `csb` | 2,253 sentence pairs |
| Bible retrieval | `dtp`, `xav`, `bam` | 23,238 verse pairs |
| Roundtrip alignment | `dtp`, `xav`, `bam` | 22,669 samples |
| NER | `csb`, `lij`, `fur` | 300 test sentences |
| POS target subset | `xav`, `bam`, `lij` | 1,342 test sentences / 20,286 tokens |
| POS full scoring set | Table 3 POS 91 languages | 200,200 test sentences / 3,336,371 tokens |

**C. Task-level evaluation samples**

| Task | Train / dev set | Eval languages | Eval samples | Use in claim |
| --- | --- | --- | ---: | --- |
| PPPL diagnostic | none | Target7; target pool is 700 samples | current scored run: 140 sentences / 5,196 masked tokens | intrinsic MLM signal |
| Tatoeba retrieval | none | `dtp`, `ile`, `csb` | 2,253 sentence pairs | target7 evidence |
| Bible retrieval | none | `dtp`, `xav`, `bam` | 23,238 verse pairs | target7 evidence |
| Roundtrip alignment | none | `dtp`, `xav`, `bam` | 22,669 samples | target7 evidence |
| NER | English train/dev: 20,000 / 10,000 sentences | `csb`, `lij`, `fur` | 300 test sentences | target transfer evidence |
| POS | Turkish train/dev: 52,286 / 5,211 sentences | target subset: `xav`, `bam`, `lij`; scored table: Table 3 POS 91 languages | target subset: 1,342 sentences / 20,286 tokens; full scoring set: 200,200 sentences / 3,336,371 tokens | transfer evidence |
| Text classification | English train/dev/test: 859 / 105 / 110 rows | `eng` | 110 test rows | auxiliary sanity check |

**D. Per-language eval breakdown**

| Task | Per-language samples |
| --- | --- |
| PPPL target pool | 7 target languages x 100 samples = 700 samples; current scored run uses 20 sentences per language |
| Tatoeba | `dtp`: 1,000 pairs; `ile`: 1,000 pairs; `csb`: 253 pairs |
| Bible | `dtp`: 7,887 verse pairs; `xav`: 7,418 verse pairs; `bam`: 7,933 verse pairs |
| Roundtrip | `dtp`: 7,393; `xav`: 7,393; `bam`: 7,883 |
| NER | `csb`: 100 sentences; `lij`: 100 sentences; `fur`: 100 sentences |
| POS target subset | `xav`: 20 sentences / 116 tokens; `bam`: 1,026 sentences / 13,823 tokens; `lij`: 296 sentences / 6,347 tokens |
| POS full scoring set | Table 3 POS: 91 languages; head 63 = 178,004 sentences / 3,074,730 tokens; tail 28 = 22,196 sentences / 261,641 tokens |

**Tokenizer**

- Train SentencePiece unigram tokenizer on the mixed `92 seen + 7 target` corpus.
- Merge the new tokenizer with XLM-R by appending only new pieces.
- Keep the same extended tokenizer for all initialization variants.

**Presenter note**

MLM uses the mixed 99-language train corpus. Retrieval, Roundtrip, and PPPL do
not use supervised fine-tuning. NER/POS are transfer evaluations: the classifier is
fine-tuned on a source language and tested on target languages. Text
classification is English-only here, so it is reported as an auxiliary sanity
check rather than target7 evidence. NER is reported as a small target-subset
diagnostic because the local target tests have only 100 sentences per language.
Roundtrip now uses the full materialized target files rather than the earlier
100-sample-per-language cap.
POS uses the recovered Table 3 split under `pos_rebuilt`, covering 91/91 POS
languages, including all 28 tail languages and the target-relevant `xav_Latn`,
`bam_Latn`, and `lij_Latn`.

## Slide 5. Initialization Ablation

**Same tokenizer, different new-row initialization**

| Method | Initialization | Role |
| --- | --- | --- |
| `random` | New rows initialized randomly | Glot500-style simple baseline |
| `mean` | Use global mean of existing XLM-R lexical embeddings | Stable simple baseline |
| `fvt` | Split each new token with XLM-R tokenizer and average source subtoken embeddings | Main hypothesis |

**Excluded from main**

`align` was generated during the run, but it collapsed to the same artifact as
`fvt`. It is therefore not interpreted as an independent ablation.

**Presenter note**

Because corpus, tokenizer, and MLM schedule are fixed, differences between
`random`, `mean`, and `fvt` can be attributed mainly to initialization.

## Slide 6. Continued MLM Training

**Glot500-aligned training recipe**

| Item | v5.2 setting |
| --- | --- |
| Base model | `xlm-roberta-base` |
| Objective | Masked Language Modeling |
| Learning rate | `5e-5` |
| Adam betas | `(0.9, 0.999)` |
| Effective batch size | `384` |
| Max sequence length | `512` |
| MLM probability | `0.15` |
| Sampling | `alpha = 0.3` |
| Training budget | short-budget initialization ablation |

**Presenter note**

v5.2 follows the core Glot500 continued-pretraining recipe where feasible, but
scales down total steps and checkpoint interval for an 8-hour controlled
ablation rather than a full 480K-step reproduction.

## Slide 7. Evaluation Protocol

**Baselines and ablations**

| Group | Models |
| --- | --- |
| Baselines | `XLM-R-B`, `XLM-R-L`, `Glot500-m` |
| v5.2 ablation | `random`, `mean`, `fvt` |

**Evaluation tasks**

| Task | Metric |
| --- | --- |
| Pseudoperplexity | PPPL, lower is better |
| Sentence Retrieval Tatoeba | Top-10 accuracy |
| Sentence Retrieval Bible | Top-10 accuracy |
| Text Classification | macro-F1 |
| NER | F1 |
| POS | F1 |
| Roundtrip Alignment | accuracy |

**Scale**

PPPL is reported as raw value. All other task scores are reported as `score x
100` to match the Glot500 paper-style table.

## Slide 8. Reporting Rule

**Claim discipline**

| Claim | Allowed? | Reason |
| --- | --- | --- |
| FVT improves PPPL strongly | Yes | paired ablation table is complete |
| FVT is best on every downstream task | No | Text/POS favor other methods |
| Initialization matters under fixed tokenizer | Yes | random/mean/fvt differ with same tokenizer |
| v5.2 reproduces full Glot500 training | No | this is a short-budget controlled ablation |

**Final framing**

```text
v5.2 is a compact Glot500-style rerun designed to test whether initialization
of appended vocabulary rows affects XLM-R-unseen tail language adaptation.
```
