# Qualitative Analysis

작성일: 2026-06-04

## Purpose

This file records 20 inspected examples across the main model families.
The goal is not to prove translation quality from cherry-picked examples, but to make the failure modes readable:

- direct Coptic/Syriac NMT collapses to a tiny set of formulaic Coptic fragments;
- retrieval-augmented neural runs produce plausible Coptic strings but mostly follow the retrieved hint;
- feature-selected retrieval hints can improve the hint, but do not fix source grounding;
- the Greek pivot gate fails before back-translation because Greek -> Coptic does not switch into Coptic.

## Systems Compared

| Label | Run | Scope |
| --- | --- | --- |
| Direct | `len64_ngram2_rp12_pilot512_step300_syr_to_cop_mean10k` | 64-example Syriac -> Coptic test slice |
| Retrieval-Aug | `byt5_small_retrieval_aug_cop_auto_tasks_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32_nosave` | 64-example English -> Coptic test slice |
| Feature-Hint | `byt5_small_retrieval_aug_cop_auto_tasks_eval_feature_selected_top8_eng_to_cop_len768_384_gen192_beam4_lp10_pilot2048_step300_fp32_nosave` | same 64-example English -> Coptic slice with feature-selected top8 hint |
| Greek Pivot Gate | `byt5_small_pivot_grc_to_cop_len320_128_pilot256_step50_fp32_nosave` | 32-example Greek -> Coptic test slice |

## Example Audit

### Direct Syriac -> Coptic

Summary:

- 64 predictions, only 3 unique strings.
- The model emits short Coptic-looking fragments such as `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ...`.
- The outputs are usually grammatical-looking fragments, not translations of the Syriac source.

| ID | Gold cue | Prediction | Error |
| --- | --- | --- | --- |
| `b.JOH.1.1` | `ϦⲈⲚ ⲦⲀⲢⲬⲎ... ⲠⲒⲤⲀϪⲒ` | `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ ϪⲈⲀ ⲠⲈ Ⲛ ⲈⲂⲞⲖ.` | misses core "beginning/Word/God" content |
| `b.JOH.1.10` | `ⲚⲀϤⲬⲎ ϦⲈⲚⲠⲒⲔⲞⲤⲘⲞⲤ...` | `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ ϪⲈⲀ ⲠⲈ Ⲛ.` | same formula, no world/know relation |
| `b.JOH.1.11` | `ⲀϤⲒ ϨⲀ ⲚⲎ...` | `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ ϪⲈⲀ ⲠⲈ Ⲛ.` | same formula, no "his own received him not" |
| `b.JOH.1.19` | `ϮⲘⲈⲦⲘⲈⲐⲢⲈ ⲚⲦⲈⲒⲰⲀⲚⲚⲎⲤ...` | `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨⲀ ϪⲈ ⲠⲈ Ⲛ ⲈⲂⲞⲖ.` | formula ignores John/priest/Levite question |
| `b.JOH.1.28` | `ⲂⲎⲐⲀⲚⲒⲀ... ⲒⲰⲀⲚⲚⲎⲤ ϮⲰⲘⲤ` | `ⲆⲈ ⲞⲨⲞϨ ⲀⲚ ⲞⲨ ϪⲈⲀ ⲠⲈ Ⲛ ⲈⲂⲞⲖ.` | formula ignores place and baptism |

### Retrieval-Augmented English -> Coptic

Summary:

- 64 predictions, 62 unique strings.
- Text is Coptic and often sentence-like.
- The model largely follows the retrieved Coptic hint, so the apparent quality is not source-only translation.

| ID | Retrieved/prediction behavior | Error |
| --- | --- | --- |
| `b.JOH.1.1` | Prediction begins from retrieved `ⲚⲀⲨⲔⲰϮ... ⲠⲒⲤⲀϪⲒ...` rather than the gold `ϦⲈⲚ ⲦⲀⲢⲬⲎ...` | copies a related but wrong retrieved verse |
| `b.JOH.1.10` | Prediction repeats retrieved world-related Coptic phrase and runs long | partial topical overlap, weak verse-specific grounding |
| `b.JOH.1.11` | Prediction follows a retrieved candidate about receiving/reward language, not the concise gold | retrieved candidate dominates over source |
| `b.JOH.1.19` | Prediction includes Jerusalem/priest-like terms, showing the hint can provide useful lexical material | useful overlap but still retrieval-shaped |
| `b.JOH.1.28` | Prediction closely tracks retrieved Jordan/baptism candidate | good local overlap, but still copied/edited retrieval |

### Feature-Selected Retrieval Hint

Summary:

- 64 predictions, 61 unique strings.
- Feature-selected hints slightly improve the headline 64-slice metric (`19.6952 -> 19.9182` chrF++).
- Exact retrieved copies fall, but the neural output remains long and hint-led.

| ID | Observation | Error |
| --- | --- | --- |
| `b.JOH.1.1` | Feature hint changes the candidate, but prediction repeats `ⲪⲎ ⲈⲦⲀⲚⲤⲞⲐⲘⲈϤ...` | hint is better selected but generation repeats it |
| `b.JOH.1.10` | Same as normal retrieval for this row; prediction remains world-related and long | no source-grounding gain beyond hint |
| `b.JOH.1.11` | Feature-selected retrieved candidate differs strongly from gold; prediction follows it | selector can choose a fluent but wrong candidate |
| `b.JOH.1.19` | Similar useful Jerusalem/priest lexical overlap as normal retrieval | still retrieved-candidate editing, not clean translation |
| `b.JOH.1.28` | Prediction remains close to the Jordan/baptism retrieved candidate | good lexical overlap but not independent generation |

### Greek -> Coptic Pivot Gate

Summary:

- 32 predictions, 32 unique strings.
- 0/32 predictions contain Coptic characters.
- The model stays in Greek script, often repeating the Greek source or Greek-like fragments.

| ID | Gold cue | Prediction | Error |
| --- | --- | --- | --- |
| `b.JOH.1.1` | Coptic `ϦⲈⲚ ⲦⲀⲢⲬⲎ...` | `ητο ητο ητο ητο...` | Greek repetition, no Coptic |
| `b.JOH.1.10` | Coptic world verse | `εν τω κοσμω, και εν τω κοσμω...` | Greek source echo/repetition |
| `b.JOH.1.11` | Coptic "his own received him not" | `εις τα ιδια ηλθε...` | Greek paraphrase/echo, no target script |
| `b.JOH.1.19` | Coptic John testimony verse | `εισαι; εισαι; εισαι...` | repeated Greek question fragment |
| `b.JOH.1.28` | Coptic Bethany/Jordan/baptism verse | `εγειναν εν Βηθαβαρα περαν...` | Greek phrase repetition, no Coptic |

## Cross-System Takeaways

1. Direct NMT has low diversity and poor source grounding.
2. Retrieval gives the model valid Coptic text, but the model learns to follow the hint.
3. Feature-selected hints improve retrieval input quality a little, yet do not remove the copy mechanism.
4. Greek pivot back-translation should not proceed from the current gate models because Greek -> Coptic fails target-script transfer.

## Paper Use

Use these examples to support a cautious claim:

> Vocabulary and MLM adaptation improve representation-side readiness, but the downstream translation system still needs a stronger source-grounding objective or model family. Retrieval is a strong baseline and useful input signal, but current neural retrieval-augmented generation is copy-heavy rather than solved translation.
