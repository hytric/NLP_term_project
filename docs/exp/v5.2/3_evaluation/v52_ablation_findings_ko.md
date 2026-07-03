# v5.2 Ablation Findings

작성일: 2026-06-29

## 현재까지의 핵심 결과

`checkpoint-500`, `checkpoint-1000`, `checkpoint-1500`, `checkpoint-2000`,
`checkpoint-2500`, `checkpoint-3000`, `checkpoint-3500`, `checkpoint-4000`
기준으로 PPPL/Tatoeba score table이 채워졌다. 여덟 checkpoint 모두
`fvt`가 `random`과 `mean`보다 좋은 방향이다.

| Step | Metric | Random | Mean | FVT | Align | Direction |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 500 | PPPL | 374.606977 | 479.424743 | 161.877958 | 161.877958 | lower |
| 1000 | PPPL | 241.797413 | 270.934481 | 108.603835 | 108.603835 | lower |
| 1500 | PPPL | 190.915409 | 208.204215 | 90.288642 | 90.288642 | lower |
| 2000 | PPPL | 160.498560 | 172.580672 | 75.258020 | 75.258020 | lower |
| 2500 | PPPL | 145.951840 | 150.454629 | 66.575042 | 66.575042 | lower |
| 3000 | PPPL | 133.106839 | 138.513402 | 61.603757 | 61.603757 | lower |
| 3500 | PPPL | 121.631484 | 131.012510 | 58.939731 | 58.939731 | lower |
| 4000 | PPPL | 119.581715 | 128.258830 | 58.025602 | 58.025602 | lower |
| 500 | Tatoeba top10 | 0.209241 | 0.217194 | 0.223194 | 0.223194 | higher |
| 1000 | Tatoeba top10 | 0.222845 | 0.214241 | 0.254813 | 0.254813 | higher |
| 1500 | Tatoeba top10 | 0.239559 | 0.235511 | 0.265353 | 0.265353 | higher |
| 2000 | Tatoeba top10 | 0.245495 | 0.235162 | 0.274544 | 0.274544 | higher |
| 2500 | Tatoeba top10 | 0.250543 | 0.243860 | 0.290893 | 0.290893 | higher |
| 3000 | Tatoeba top10 | 0.249892 | 0.246495 | 0.282306 | 0.282306 | higher |
| 3500 | Tatoeba top10 | 0.247225 | 0.247829 | 0.280321 | 0.280321 | higher |
| 4000 | Tatoeba top10 | 0.248908 | 0.246194 | 0.282957 | 0.282957 | higher |

## 해석

- `fvt`는 여덟 checkpoint 연속으로 PPPL 최저, Tatoeba top10 최고다.
- `random`은 step1000에서 `mean`보다 Tatoeba가 높지만, PPPL은 `fvt`보다 높다.
- `align`은 현재 구현상 FVT 실패 token에만 unicode block mean fallback을 쓰는 방식이다.
- 이번 tokenizer에서는 `align` initializer가 `fvt`와 byte-identical하게 collapse됐다.
- 따라서 `align` row는 table continuity를 위해 남기되, 독립 ablation evidence로 해석하지 않는다.

## 발표용 안전 문장

```text
In the first eight checkpoint diagnostics, FVT gives the strongest initialization
signal: it has the lowest pseudoperplexity and the highest Tatoeba retrieval
score among the independent initialization methods. The current align variant
collapses to FVT for this tokenizer, so we keep it in the table but do not count
it as independent evidence.
```
