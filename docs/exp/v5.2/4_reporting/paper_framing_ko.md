# v5.2 논문 Framing 문장

## Abstract/Intro 후보

```text
We reproduce the Glot500-style vocabulary injection and continued MLM pipeline
on 92 XLM-R-seen replay languages plus 7 XLM-R-unseen tail target languages.
The target languages are selected from the smallest corpus band that still
supports downstream evaluation, allowing us to track intrinsic and downstream
metrics throughout training.
```

## Method 후보

```text
We keep the tokenizer construction fixed: a SentencePiece unigram tokenizer is
trained on the mixed corpus, and pieces missing from the original XLM-R
SentencePiece model are appended to the source vocabulary. Under this fixed
Glot500-style vocabulary injection setup, we compare four initialization
methods for newly added embedding rows: random, mean, FVT, and align.
```

## Low-Resource 정의 후보

```text
In this experiment, low-resource tail refers to XLM-R-unseen language-scripts in
the lowest corpus-size band that still has usable downstream task coverage. This
follows Glot500's operational tail definition more closely than a strict
``<=10k`` corpus-size-only definition, which has no local downstream coverage in
our audit.
```

## Evaluation 후보

```text
During MLM training, we evaluate intermediate checkpoints and continuously
update the result table. Coverage and materialization rows are logged
separately from model-dependent metric rows, and claims are promoted only when
paired initialization results are available.
```

## Yamaguchi 관련 문장

```text
Yamaguchi-style low-resource vocabulary expansion is treated as an additional
experiment rather than the main comparison axis; the main study isolates
embedding initialization under the same Glot500-style tokenizer.
```

## 쓰면 안 되는 문장

```text
We completed every downstream task for all target languages.
```

POS는 복구된 Table 3 split 기준으로 보고하고, Taxi1500은 local
generation 상태에 따라 `pending` 또는 `materialization_needed`로 남길 수 있다.
