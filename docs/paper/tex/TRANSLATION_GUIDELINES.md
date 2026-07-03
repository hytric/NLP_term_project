# English Report Translation Guidelines

Guidelines for translating the Korean draft (`tex_ko/`) into the English report (`tex/`).
Incorporates lecture notes on academic writing standards.

---

## 0. Before You Write: The Three Checks

Each section must answer:
1. **Why does this matter?** (significance)
2. **What is new here?** (novelty)
3. **Is every claim specific enough to be falsifiable?** (credibility)

If any answer is "not clear yet," fix that before writing prose.

---

## 1. Title

Must contain all three of the following — no exceptions:

| Element | Example |
|---|---|
| Problem | "Vocabulary Extension for Low-Resource Tail Languages" |
| Method | "XLM-R-Based Glot500-Style … with Family-Aware Embedding Initialization" |
| Differentiation | what distinguishes this from Glot500 itself |

A title that is too general or too vague loses reader interest immediately.
Current title: *XLM-R-Based Glot500-Style Vocabulary Extension for Low-Resource Tail Languages* — confirm the differentiation (initialization ablation) is visible enough.

---

## 2. Abstract Structure

Fixed order: **Problem → Existing limitation → Proposal → Results**

Each must be specific:

| Slot | Banned | Required |
|---|---|---|
| Problem | "multilingual models have issues" | "XLM-R over-fragments tail-language tokens (tokens/word = 2.204)" |
| Existing limitation | "prior work is limited" | "Glot500 initializes new rows randomly, leaving initialization as an open choice" |
| Proposal | "we propose a new method" | "we initialize new rows from the language-family centroid of source token embeddings (family_mean)" |
| Results | "our method performs well" | "family_mean achieves the lowest target PPPL and best Tatoeba/NER scores in a 5-way ablation" |

---

## 3. Language Precision — Vague Expressions Are Banned

**Banned:** `very`, `quite`, `rather`, `somewhat`, `fairly`, `a bit`, `a lot`, `much`, `few`, `usually`, `any`, `all` (unless literally meaning every element).

Replace with a number or a precise qualifier:

| Avoid | Replace with |
|---|---|
| "very important" | "critical for downstream performance" |
| "significantly reduces" | "reduces tokens/word by 27.75% (2.204 → 1.592)" |
| "quite good" | "outperforms random on 4 of 5 tasks" |
| "many languages" | "511 language-scripts" |
| "few training examples" | "fewer than 30,000 sentences" |
| "usually better" | "better on Tatoeba and NER; comparable on Roundtrip" |

---

## 4. Introduction — Persuasion is the Goal

Structure: **Motivation → Gap → Proposal → Three core contributions**

- State the three core contributions as a numbered list (as in the Korean draft).
- Introduction is not a summary of the paper — it is an argument for why this work needed to exist.
- Every paragraph should advance the argument; cut any paragraph that does not.

---

## 5. Related Work

- Aim for **30+ citations**; reviewers check coverage.
- Verify every citation before submitting — false citations are common and damage credibility.
- Do not merely describe prior work; explain **what gap each work leaves** that this paper fills.
- Proactively defend against obvious objections (preempt likely reviewer critiques).

---

## 6. Method — Definitions Are Mandatory

- **Every symbol used in an equation must be defined** the first time it appears.
- Newly introduced methods must be formally defined, not just described.
- For complex methods, decompose into core components before describing each.

**Mathematical notation conventions:**

| Object | Convention | Example |
|---|---|---|
| Vector | bold lowercase | $\mathbf{e}$, $\mathbf{v}$ |
| Matrix | bold uppercase | $\mathbf{E}$, $\mathbf{W}$ |
| Set | curly braces | $\mathcal{V}$, $\{t_1, \ldots, t_n\}$ |
| List/sequence | angle brackets or subscripts | $(t_1, t_2, \ldots)$ |

- **Do not reuse the same symbol for two different meanings** across the paper.
- Each symbol's meaning is fixed at first definition; use a consistent alphabet (Greek letters should be intuitive: $\alpha$ for temperature/learning-rate style parameters, $\mu$ for means, etc.).
- Check `math_commands.tex` (or equivalent) before introducing new macros.

---

## 7. Voice and Directness

- Prefer **active voice**.
  - Bad: "It was found that family_mean outperforms…"
  - Good: "family_mean outperforms random initialization on target PPPL and Tatoeba retrieval."
- No hedges: "it seems", "it appears", "it might be the case that" → state the claim; if uncertain, write "we hypothesize" or "a possible explanation is".
- Core findings may be **repeated** across abstract, results, and conclusion — reviewers skim; key takeaways must appear where they look.

---

## 8. Pronoun Reference — this / it / the

Be explicit about what `this`, `it`, and `the` refer to.

- Bad: "This shows that the method works."
- Good: "This result shows that family\_mean converges faster than random initialization."
- When in doubt, repeat the noun rather than use a pronoun.

---

## 9. Technical Term Policy

Keep all model/method names in their canonical form. Do **not** translate or paraphrase:

| Korean draft | English report |
|---|---|
| `\fvt` | `\fvt` (FVT) |
| `\wfvt` | `\wfvt` (weighted\_fvt) |
| `\famm` | `\famm` (family\_mean) |
| `\rand` | `\rand` (random) |
| `\meanm` | `\meanm` (mean) |
| XLM-R, MLM, SPM, PPPL | unchanged |
| vocabulary extension, continued pretraining | unchanged |

---

## 10. Experiments — Fair Comparison

Reviewers check fairness. Confirm and document:

- Same **model size** (all variants use `xlm-roberta-base`)
- Same **dataset** (same corpus, same splits)
- Same **training budget** (50K steps, same schedule)
- Same **objective** (MLM, same masking probability)
- Clearly state in/out-of-domain conditions

The only variable that changes across the 5 conditions is initialization.

---

## 11. Ablation Study

- High sensitivity to hyperparameters is a weakness; the ablation should reveal a robust winner.
- Each ablation condition must follow **naturally from the hypothesis**, not be a brute-force search.
- Show the **causal mechanism**: why does family\_mean win? (family clustering in embedding space → better starting point for tail-language tokens without family-coverage data)
- Sensitivity analysis: if results flip with small changes, acknowledge it in Limitations.

---

## 12. Claim Scoping

Every empirical claim must include its scope. Phrases like "in general" or "for all languages" are banned unless evidence covers all languages.

Required scope for this paper:
- Model: `xlm-roberta-base`
- Target: Target7 (7 XLM-R-unseen language-scripts)
- Budget: 50K-step continued MLM pretraining
- Tokenizer: fixed Glot500-style (only initialization varies)

---

## 13. Structural Correspondence (Korean → English)

| Korean (tex_ko) | English (tex/sections/) |
|---|---|
| 서론 | `01_introduction.tex` |
| 관련 연구 | `02_related_work.tex` |
| 데이터 | `03_data.tex` |
| 방법 | `04_method.tex` |
| 실험 | `05_experiments.tex` |
| 결과 | `06_results.tex` |
| 표현 분석 | `07_analysis.tex` |
| 한계 및 결론 | `08_limitations_conclusion.tex` |

---

## 14. Sentence Length and Flow

- **One idea per sentence.** Split long Korean compound sentences at conjunctions.
- Avoid fronted subordinate clauses that bury the main point.
  - Bad: "Since training data does not exist for low-resource tail languages, and given that the evaluation protocol follows XTREME, we evaluate on English fine-tuned models."
  - Good: "We fine-tune on English and evaluate zero-shot on target languages (XTREME protocol). This is necessary because labeled training data does not exist for our target languages."
- Limit parenthetical asides; move to footnote or drop.

---

## 15. Numbers and Units

- Comma separator for thousands: `116,664` not `116664`.
- Spell out small integers starting a sentence: "Five methods are compared…".
- Percentages: `27.75%` (two decimal places for key results).
- Step counts: `50K steps` in prose, exact in tables.

---

## 16. Prohibited Patterns

| Pattern | Replacement |
|---|---|
| "It is noted that …" | State the finding directly |
| "As mentioned above/below" | Use the section number: "(\S4)" |
| "Needless to say" / "Of course" | Delete |
| "our method is better" | "family\_mean achieves the lowest target PPPL (X.XX)" |
| "In this paper, we will show…" | "We show…" (drop the meta-frame) |

---

## 17. Abstract and Section Tense Convention

| Context | Tense |
|---|---|
| What this paper does (abstract) | present ("We compare five…") |
| What we observed (results) | past ("family\_mean achieved…") |
| What the findings imply | present ("These results suggest…") |
| Method description | past ("We initialized…") |

---

## 18. Table and Figure Captions

- Full sentences ending with a period.
- Include the **key takeaway**, not just a description.
  - Bad: "Results across five methods."
  - Good: "family\_mean achieves the best target PPPL and Tatoeba scores; weighted\_fvt leads on Roundtrip alignment."

---

## 19. Writing Quality Checklist (Before Each Draft Submission)

- [ ] Clarity: every sentence is unambiguous
- [ ] Formality: no colloquial expressions
- [ ] Consistency: same term used for the same concept throughout
- [ ] No vague intensifiers (`very`, `quite`, etc.)
- [ ] All symbols defined at first use
- [ ] All citations verified to exist and say what the paper claims
- [ ] All claims scoped to the actual experimental setup
- [ ] Core results repeated in abstract, results section, and conclusion
