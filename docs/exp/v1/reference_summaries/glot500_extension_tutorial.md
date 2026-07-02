# Extending Multilingual Language Models To Low-Resource Languages

Source: `docs/survey/GLOT500_extension.pdf`

## 핵심 내용

- Glot500-m, vocabulary extension, continued pretraining을 Coptic/Syriac 사례로 설명하는 tutorial이다.
- 저자원 언어 확장에서는 tokenizer가 target script/text를 과도하게 쪼개는 문제가 먼저 발생한다.
- 이를 해결하기 위해 target-language tokenizer를 학습하고, 기존 multilingual model에 vocab을 확장한다.
- 확장 후 새 token embedding 초기화와 continued pretraining이 필요하다.

## 방법론 포인트

- Vocab extension은 기존 multilingual 지식을 보존하기 위해 replacement보다 안전하다.
- 새 token embedding은 random, mean, align 같은 방법으로 초기화할 수 있다.
- Full fine-tuning과 LoRA/adapter류를 비교할 수 있지만, compute가 작으면 안정성과 재현성을 우선해야 한다.
- Evaluation은 tokenization, MLM, downstream, qualitative sample을 함께 봐야 한다.

## Second_try에 가져올 것

- first_try와 유사하게 target10 tokenizer를 학습하고 XLM-R에 merge한다.
- Coptic/Syriac만이 아니라 target10 전체에서 fragmentation을 측정한다.
- tokenization before/after sample을 언어별로 뽑는다.
- stage별 gate를 둔다.

## 주의점

- 원 tutorial은 Coptic/Syriac NMT 방향을 포함하지만 second_try에서는 번역을 제외한다.
- Decoder 학습은 이번 목표와 다르므로 encoder-only downstream으로 바꿔 해석한다.
- Bible domain만으로 일반화 주장을 하지 않는다.

## Plan 반영

- Stage 02 tokenization audit.
- Stage 03 vocab extension.
- Stage 04 embedding initialization.
- Stage 05 MLM adaptation.
- Stage 06 encoder-only downstream.
