# 03 Data and Experimental Scope

## 3.1 Language scope

Corpus universe는 99개 language-script다: **92개 XLM-R-seen replay/head + 7개 XLM-R-unseen target/tail**. Target7은 모두 Latin script이며, XLM-R 학습에 포함되지 않았고 Glot500 raw corpus가 존재하며 `new_length >= 30,000`인 low-resource band에서 골랐다.

**Table 1. Target7 languages.**

| language_script | full name | family | region | new_length | Covered tasks |
| --- | --- | --- | --- | ---: | --- |
| `dtp_Latn` | Kadazan Dusun | Austronesian | Southeast Asia | 48,468 | Tatoeba, Bible, Roundtrip, Taxi1500, Embedding similarity |
| `xav_Latn` | Xavánte | Macro-Je | South America | 31,765 | Bible, Roundtrip, Taxi1500 |
| `bam_Latn` | Bambara | Mande | West Africa | 32,150 | Bible, Roundtrip, Taxi1500 |
| `csb_Latn` | Kashubian | Slavic | Europe | 33,743 | Tatoeba, NER, Embedding similarity |
| `ile_Latn` | Interlingue | Constructed | Constructed/Europe | 40,984 | Tatoeba, Embedding similarity |
| `lij_Latn` | Ligurian | Romance | Europe | 42,447 | NER |
| `fur_Latn` | Friulian | Romance | Europe | 30,052 | NER |

## 3.2 왜 이 언어들인가 (선택 기준)

언어 선택은 임의가 아니라 **"평가까지 연결 가능한 tail language"** 기준이다. 대부분의 진짜 저자원 언어는 human-labeled downstream 데이터가 아예 없어 tokenizer→training→evaluation을 끝까지 연결할 수 없다. 그래서 우리는 각 downstream task마다 **평가 가능한 Target 언어를 최소 3개씩** 확보할 수 있도록 7개 언어를 선택했다. 지역·계통도 Southeast Asia / South America / West Africa / Europe / Constructed로 분산해 특정 계통에 편중되지 않게 했다. 이 선택은 일반성보다 **traceability(추적 가능성)**를 우선한 결과다.

**Table 2. Task별 평가 대상 Target 언어(피드백 반영: 각 task 3언어 매핑).**

| Task | Target 언어 (3개) | 평가 데이터 규모 | 발표 해석 |
| --- | --- | --- | --- |
| Tatoeba retrieval | `dtp`, `ile`, `csb` | 2,253 sentence pairs | target retrieval evidence |
| Bible retrieval | `dtp`, `xav`, `bam` | 23,238 verse pairs | (floor, 아래 3.4 참조) |
| Roundtrip alignment | `dtp`, `xav`, `bam` | 22,669 samples | target alignment evidence |
| NER | `csb`, `lij`, `fur` | 300 test sentences (100/lang) | small target-subset diagnostic |
| Text classification | (target direct 없음) | English only | head/EN sanity only |
| Embedding similarity | `csb`, `dtp`, `ile` (+34 ref) | 2,100 pairs | representation diagnostic |

## 3.3 Training corpus and sampling strategy

MLM 학습 corpus는 seen replay와 target을 섞은 뒤 language sampling을 적용해 생성했다.

| 항목 | 값 |
| --- | ---: |
| source raw sentences | 1,025,895,043 |
| MLM train total (merged lines) | 4,482,259 |
| — seen/head samples | 4,147,176 |
| — target7 samples | 335,083 |
| sampling factor α | 0.3 |
| scale | 1.5 |

**Sampling은 tokenizer 학습뿐 아니라 실제 MLM training corpus 생성에도 적용된다**(피드백 반영). 각 language-script의 샘플링 확률은 데이터 양 $n_i$에 대해 $P_i \propto n_i^{\alpha}$, $\alpha=0.3$로 둔다. 예를 들어 head 1,000,000 문장 대 tail 1,000 문장이면, $\alpha=1$에서는 비율이 약 1000:1이지만 $\alpha=0.3$에서는 약 8:1로 완화된다. 이 temperature down-weighting은 (1) high-resource 언어가 전체 gradient update를 독점하는 것을 막고, (2) 동시에 target-only overfitting을 피하기 위한 절충이다. 근거 코드: `preprocessing/merge_files.py`, `preprocessing/merge_files.sh`.

## 3.4 Evaluation coverage 주의

- Coverage가 없는 group은 `0`이 아니라 `NA`로 표기한다. `0`은 실제 낮은 점수이지 coverage 없음이 아니다.
- **Bible retrieval**은 50K에서도 모든 초기화 방법이 Acc10 ~0.008로 사실상 **floor**다(Glot500-m 0.147 대비). 초기화 우열의 discriminative evidence로 쓰지 않는다.
- **Text classification(Taxi1500)**은 Glot500 정식 task(Ma et al., 2023)로 원래 English fine-tune → target zero-shot이지만, 본 실험에서는 target test set이 Parallel Bible Corpus 저작권 때문에 로컬에 없어 **English(head)만** 평가된다(방법론이 아니라 데이터 접근 한계). tail 근거로 쓰지 않는다.
- **NER**은 target 언어당 100문장(총 300)의 small subset이므로 diagnostic으로만 해석한다.

## 금지할 표현

- Target7이 전체 low-resource universe나 script diversity를 대표한다고 쓰지 않는다.
- coverage 없는 task에서 target 성능을 추론하지 않는다.
