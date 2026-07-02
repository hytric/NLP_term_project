# Stage 07 Main Result Summary

작성일: 2026-06-13

## Decision

Current claim route: `DIAGNOSTIC_NEGATIVE_CURRENT_CANDIDATE`.

The positive route is blocked. The tokenizer extension is structurally valid and reduces average target10 tokenization fragmentation, but the model-quality evidence does not support a broad seed-stable target10 downstream improvement over XLM-R-base.

## Key Evidence

| Evidence | Result | Interpretation |
| --- | ---: | --- |
| target10 tokenization tokens/word | -29.812358% | Average fragmentation improves. |
| byte fallback vs char append delta | -0.599816% | Byte fallback is slightly better as tokenizer ablation. |
| target10 MLM proxy loss | XLM-R 3.472837 vs replay-safe fvt mean 5.245928 | Current best candidate is worse on average, though better than the 200-step pilot. |
| Coptic POS token accuracy | +0.006781 mean, 3/3 checkpoint seeds | Weak Coptic-only downstream pilot improvement. |
| Coptic POS macro F1 | -0.002656 mean | Slightly worse macro-F1 despite token-accuracy gain. |
| frozen verse retrieval | +0.000593 mean, 2/3 seeds | Weak proxy improvement. |
| frozen parallel AUC | -0.000649 mean, 1/3 seeds | Mixed/negative proxy evidence. |
| high-resource control MLM loss | +0.675539 mean loss vs XLM-R | Potential high-resource collapse proxy remains after replay-safe retry. |

## Bottom Line

The current third_try candidate is useful as a diagnostic experiment: it shows that id-preserving vocabulary extension and better tokenizer fertility are not enough by themselves. The replay-safe retry reduces some losses but does not rescue the positive gate. The failure conditions now point to training scale, replay schedule, appended-token learning, and tokenizer fallback implementation as the main ablation axes.
