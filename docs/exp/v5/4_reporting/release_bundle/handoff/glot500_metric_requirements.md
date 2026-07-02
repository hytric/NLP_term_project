# v5 Glot500 Metric Requirements

작성일: 2026-06-26  
최근 상태 갱신: 2026-06-28

원칙: Glot500에서 측정한 metric은 v5에서도 모두 측정한다. 특정 selected target
language가 어떤 task dataset에 없더라도 metric을 생략하지 않는다. 대신 해당
task의 measured language set, excluded language set, exclusion reason을 함께
기록한다.

PPPL 예외/정정 원칙: Glot500의 PPPL은 held-out test set에서 계산된다. 현재 v5의
`PPPL_SPLIT=train` rows는 train-source intrinsic diagnostic으로만 사용하며, final
Glot500-style held-out PPPL은 v5.1에서 train/dev/test split을 먼저 만든 뒤
측정한다. 자세한 정책은 `../MLM_HELDOUT_POLICY_KO.md`를 본다.

## Required Metrics

| ID | Metric | Score | Required outputs |
| --- | --- | --- | --- |
| `pppl` | Pseudoperplexity | PPPL / MLM proxy loss | head, tail, all, v5-target subset; v5 train-source rows are diagnostic only |
| `retrieval_tatoeba` | Sentence Retrieval Tatoeba | Top-10 accuracy | head, tail, all, coverage |
| `retrieval_bible` | Sentence Retrieval Bible | Top-10 accuracy | head, tail, all, coverage |
| `text_classification` | Text Classification | F1 | head, tail, all, coverage |
| `ner` | Named Entity Recognition | F1 | head, tail, all, coverage |
| `pos` | POS Tagging | F1 | head, tail, all, coverage |
| `roundtrip_alignment` | Roundtrip Alignment | accuracy | head, tail, all, coverage |

## Required Model Columns

Minimum:

- `xlmr_base`
- `glot500_base`
- `v5_random`
- `v5_fvt`

If time allows:

- `v5_mean`
- `v5_align`

Executable model matrix:

```text
docs/exp/v5/3_evaluation/model_matrix.tsv
```

Refresh command:

```bash
python3 scripts/write_v5_eval_model_matrix.py
```

## Completion Table

| Metric | XLM-R-base | Glot500-base | v5-random | v5-fvt | Coverage file | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Pseudoperplexity | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_pseudoperplexity.tsv` | partial; v5-fvt waits for matched 10K checkpoint |
| Tatoeba Retrieval Top-10 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_retrieval_tatoeba.tsv` | partial; target10 coverage `0/10`; v5-fvt waits for checkpoint |
| Bible Retrieval Top-10 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_retrieval_bible.tsv` | partial; coverage `74/102`, target10 `0/10`; v5-fvt waits for checkpoint |
| Text Classification F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_text_classification.tsv` | partial; local data is English-only; v5-fvt waits for checkpoint |
| NER F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_ner.tsv` | partial; coverage audit target10 count is `0/10`; actual-evaluated v5-target intersection is `fur_Latn` only, not a target10-wide claim |
| POS F1 | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_pos.tsv` | partial; target10 coverage `0/10`; local train language `tur_Latn`; v5-fvt waits for checkpoint |
| Roundtrip Alignment Acc. | measured | measured | measured | waiting for checkpoint | `00_coverage/coverage_roundtrip_alignment.tsv` | partial; baseline/reference/v5-random rows measured over `74/102`, target10 `0/10`; v5-fvt waits for checkpoint |

Generated completion checklist:

```text
docs/exp/v5/3_evaluation/09_aggregation/metric_completion.tsv
```

## Coverage Rule

For every metric, write a coverage artifact with at least these columns:

```text
task	language_script	group	has_data	reason
```

Allowed `group` values:

```text
head
tail
v5_target
other
```

If `has_data == no`, `reason` must explain whether the language is absent from
the upstream task, blocked by data license/access, missing local materialization,
or excluded for leakage.

## Report Rule

The final report must include:

- one main Glot500-style table with all seven metrics, with v5 PPPL labeled as
  diagnostic unless held-out rows exist;
- one metric completion checklist;
- one task-specific language coverage table;
- explicit notes for unavailable selected target languages.
