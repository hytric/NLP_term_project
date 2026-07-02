# Results: Target10 Data And Splits

작성일: 2026-06-03

## Goal Update

사용자 지시에 따라 목표를 Coptic/Syriac 2개 언어에서 **저자원 언어 약 10개를 추가 학습하는 multilingual adaptation 파일럿**으로 확장했다.

Coptic/Syriac은 여전히 핵심 downstream 번역 사례로 유지한다.

## Selected 10 Languages

선정 기준:

- Bible corpus에서 즉시 추출 가능
- Coptic/Syriac 포함
- speaker 수가 작거나 extinct
- Coptic/Syriac/Cherokee/Ojibwa처럼 스크립트 병목이 예상되는 언어 포함
- 학습 파일럿으로 너무 크지 않은 NT 규모

| ISO | Language | Script | Speakers | Verse count |
| --- | --- | --- | --- | ---: |
| cop | Coptic | Coptic | Extinct | 7,957 |
| syr | Syriac | Syriac | Extinct | 7,954 |
| chr | Cherokee | Cherokee | 16,400 | 7,957 |
| oji | Ojibwa | Aboriginal Syllabics | 20,000 | 7,943 |
| bsn | Barasana-Eduria | Latin | 1,890 | 7,548 |
| usp | Uspanteco | Latin | 3,000 | 7,890 |
| nhg | Nahuatl (Tetelcingo) | Latin | 3,500 | 7,822 |
| ake | Akawaio | Latin | 4,500 | 7,734 |
| kbh | Camsa | Latin | 4,770 | 6,521 |
| acu | Achuar-Shiwiar | Latin | 5,000 | 7,646 |

## 선정 이유 상세

이 10개 언어는 단순히 speaker 수가 작은 언어를 모은 것이 아니라, vocabulary adaptation 실험에 필요한 조건을 동시에 만족하도록 고른 파일럿 세트다. 핵심 기준은 데이터 접근성, Coptic/Syriac downstream 목표와의 연결성, tokenizer 병목 가능성, 그리고 짧은 시간 안에 학습과 평가를 반복할 수 있는 규모다.

첫째, 모든 언어가 Bible corpus에서 즉시 추출 가능하다. 같은 장르와 비슷한 verse 단위 구조를 공유하므로, 언어별 데이터 크기와 도메인을 비교적 통제할 수 있다. 또한 verse ID를 기준으로 train/dev/test split을 만들 수 있어, tokenizer 학습, MLM adaptation, Coptic-Syriac downstream 번역 평가를 하나의 일관된 데이터 구조 안에서 연결할 수 있다.

둘째, Coptic과 Syriac은 실험의 핵심 타깃이다. 두 언어는 speaker 기준으로는 extinct로 분류되지만, 역사적·문헌학적 가치가 크고 기존 multilingual model에서 과소대표될 가능성이 높다. 특히 Coptic은 Coptic script, Syriac은 Syriac script를 사용하기 때문에 기존 tokenizer가 단어를 의미 있는 subword로 나누지 못하고 문자 단위로 과분절할 가능성이 높다. 따라서 두 언어는 downstream 번역 사례이면서 tokenizer extension의 필요성을 보여주는 중심 사례다.

셋째, Cherokee와 Ojibwa는 스크립트 병목을 더 넓게 검증하기 위해 포함했다. Cherokee는 Cherokee script, Ojibwa는 Aboriginal Syllabics를 사용하므로 Coptic/Syriac과 마찬가지로 기존 Glot500 tokenizer에서 single-character token 비율이 높아질 수 있다. 이 언어들을 함께 넣으면 개선 효과가 Coptic/Syriac 두 언어에만 우연히 나타난 것이 아니라, 비라틴 문자 기반 저자원 언어 전반의 fragmentation 문제와 연결되어 있음을 보여줄 수 있다.

넷째, Barasana-Eduria, Uspanteco, Nahuatl (Tetelcingo), Akawaio, Camsa, Achuar-Shiwiar는 Latin script 저자원 언어로서 대조군 역할을 한다. 이들은 speaker 수가 약 1,890명에서 5,000명 수준으로 작고, Glot500 같은 대규모 multilingual pretraining에서도 충분히 대표되지 않았을 가능성이 있다. 동시에 Latin script를 사용하므로, 비라틴 script 병목과 순수한 저자원·형태론적 fragmentation 문제를 구분해서 볼 수 있다.

다섯째, verse count가 대부분 약 7,500-8,000개 내외라 파일럿 규모로 적절하다. 너무 큰 corpus가 아니기 때문에 tokenizer 학습, vocabulary merge, embedding initialization, 짧은 MLM adaptation을 빠르게 반복할 수 있다. 반대로 너무 작지도 않아서 각 언어별 tokenization audit과 train/dev/test split을 만들 수 있다. Camsa는 6,521 verses로 상대적으로 작지만, 여전히 파일럿 학습과 tokenization 비교에는 충분한 규모다.

언어별 역할은 다음처럼 정리할 수 있다.

- `cop` Coptic: 핵심 downstream 대상이며, Coptic script로 인한 tokenizer fragmentation을 직접 보여주는 대표 사례다.
- `syr` Syriac: Coptic과 함께 핵심 downstream 대상이며, Syriac script와 extinct-language 조건을 동시에 갖는 대표 사례다.
- `chr` Cherokee: Cherokee script 기반 저자원 언어로, 비라틴 script 병목이 Coptic/Syriac 밖에서도 발생하는지 확인하는 사례다.
- `oji` Ojibwa: Aboriginal Syllabics 기반 언어로, 또 다른 비라틴 script 계열의 tokenizer 병목을 검증하는 사례다.
- `bsn` Barasana-Eduria: speaker 수가 가장 작은 Latin-script 언어 중 하나로, script 문제가 약해도 저자원성 자체가 tokenization 문제를 만들 수 있는지 보는 사례다.
- `usp` Uspanteco: Latin script Mayan 계열 저자원 언어로, 형태론적·어휘적 희소성이 vocabulary extension에 어떤 영향을 주는지 확인하는 사례다.
- `nhg` Nahuatl (Tetelcingo): Latin script이지만 기존 multilingual vocabulary에서 충분히 커버되지 않을 수 있는 Indigenous language 사례다.
- `ake` Akawaio: Latin script 저자원 언어로, Bible corpus 내 verse 수가 충분해 안정적인 파일럿 비교에 적합하다.
- `kbh` Camsa: verse count는 가장 작지만 speaker 수가 작고 Latin-script 저자원 조건을 만족해 compact pilot에 포함할 가치가 있다.
- `acu` Achuar-Shiwiar: Latin script 저자원 언어 중 하나로, target10 세트의 speaker-size 범위를 넓히면서 대조군 역할을 한다.

따라서 target10은 Coptic/Syriac 중심 downstream 목표를 유지하면서도, 비라틴 script 병목 언어와 Latin-script 저자원 대조군을 함께 포함하는 균형 잡힌 vocabulary adaptation 파일럿이다.

## Data Size

- Total target-language verse rows: 76,972
- Train tokenizer lines: 61,930
- Shared verse overlap across all 10 languages: 4,892

## Split Rule

Book-level split:

- test: John (`JOH`)
- dev: Mark (`MAR`)
- train: all other books

This avoids random verse leakage and is easy to explain in the report.

## Generated Files

- `data/processed/target10/target_languages.tsv`
- `data/processed/target10/target10_bible_verses.tsv`
- `data/processed/target10/target10_stats.tsv`
- `data/processed/target10/target10_train_for_tokenizer.txt`

## Interpretation

The 10-language pilot is now large enough for a first tokenizer-extension experiment.
It is not large enough to claim broad multilingual model pretraining, but it is enough for a controlled vocabulary adaptation study.
