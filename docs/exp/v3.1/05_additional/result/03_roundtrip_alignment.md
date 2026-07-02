# Task 3. Roundtrip Alignment

작성일: 2026-06-19

## Task 정의

Roundtrip Alignment는 word/subword-level cross-lingual alignment를 평가한다. 어떤 source token을 다른 언어로 align한 뒤 다시 원래 언어로 돌아왔을 때, 원래 token으로 돌아오면 성공으로 본다.

이 task는 sentence retrieval보다 더 세밀하며, Glot500의 SimAlign/Bible roundtrip diagnostic에 가깝다.

## 데이터/설정

v3.1/05_additional에서는 아직 실행하지 않았다.

향후 실행에 필요한 요소:

- parallel Bible/item-aligned sentences
- token/subword-level hidden representations
- SimAlign 또는 contextual token nearest-neighbor alignment
- roundtrip path 정의, 예: `cop -> syr -> cop` 또는 multilingual cycle

## 결과

현재 roundtrip alignment artifact는 없다.

## 해석

현재 v3.1 evidence는 sentence-level retrieval과 CSLS diagnostic까지 포함하지만, word/subword-level alignment는 아직 평가하지 않았다.

## 주장 가능 범위

가능:

> Roundtrip alignment는 future work로 남아 있다.

불가능:

> v3.1이 Glot500-style roundtrip alignment를 개선했다고 주장할 수 없다.

## 산출물

현재 artifact 없음.

향후 생성할 artifact:

- `roundtrip_alignment_results.tsv`
- `roundtrip_alignment_results.md`
