# Task 4. NER

작성일: 2026-06-19

## Task 정의

NER는 token-level named entity recognition transfer를 평가한다. Glot500-style evaluation에서는 보통 English NER로 fine-tuning한 뒤, WikiANN 같은 gold label이 있는 target language에서 zero-shot으로 평가한다.

## 데이터/설정

v3.1/05_additional에서는 실행하지 않았다.

현재 v3.1 evidence 안에서는 Coptic/Syriac 또는 target10에 대한 WikiANN-style NER gold label을 찾지 못했다.

## 결과

현재 NER result artifact는 없다.

## 해석

NER는 Glot500의 주요 downstream task 중 하나로 언급해야 하지만, 현재 Coptic/Syriac target data에서는 gold label이 없어 실행하지 않았다.

보고서용 문장:

> We do not report NER because the current Coptic/Syriac target data does not include WikiANN-style named-entity gold labels. We instead use sentence retrieval and pair classification as label-light proxy tasks.

## 주장 가능 범위

가능:

> NER는 gold label 부재로 v3.1 result package의 범위 밖이다.

불가능:

> v3.1이 NER transfer를 개선했다고 주장할 수 없다.

## 산출물

현재 artifact 없음.
