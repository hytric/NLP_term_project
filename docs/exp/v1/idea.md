first try 에서 시도했던 것들이 좋았는데, 방향이 안맞았음.
다시 docs/survey를 읽어보고 그대로 따라해야함.

목표
1. docs/exp/second_try/feedback/vocab_extension_tutorial 읽어보고 vocab extension 시에 새로운 토큰의 임베딩 벡터를 초기화하는 기법에 대해서 다시한번 정의
2. glot500을 쓰는것이 아니라 다른 모델에 glot500에서 했던 것을 동일한 작업으로 10개 language 에 대해서 진행해야함.
3. 최종적으로 downstream task 까지 진행해서 결과 뽑고 좋은 성능을 내야함.

추가 피드백
- language 는 기존 10개 그대로 사용.
- 예시 샘플을 직접 뽑아서 내가 중간지표를 직접 확인할 수 있도록 한다.
- 다음 step으로 넘어갈 때 기준 score 를 정하고 결과를 계속 뽑는다.
- vocab extention 을 목표 1에서 분석한 초기화 기법대로 모두 테스트
- 가장 좋은 방법에 대해서 진행
- 기존 모델은 encoder only 모델임으로 번역은 decoder 를 따로 학습해야함. 
    - 그래서 번역 없는 다른 downstream task 선정
    - 최소 3개의 downstream task 제시하고 시도한다
-


기타
- gpu 는 2,3번 2개 사용가능


추가 질문사항

아래 질문은 답변하기 쉽게 선택지 중심으로 정리했다.
답변할 때는 예를 들어 `1-A, 2-B, 3-A`처럼 골라도 되고, 필요한 항목만 짧게 수정해도 된다.

1. second_try에서 재현할 범위
    - A. 전체 재현: tokenizer audit -> vocab extension -> embedding init 비교 -> MLM adaptation -> downstream task
    - B. 핵심만 재현: vocab extension -> embedding init 비교 -> MLM adaptation -> downstream task
    - C. downstream 중심: vocab extension은 최소로 하고 downstream 결과를 우선
    - 내 답: 전체 재현 language 만 선택된 상태로 처은부터 다시해야함. vocab extension 도 재대로 다시 조사해서 진행. 

2. Glot500 대신 사용할 base model
    - A. `xlm-roberta-base`
    - B. `bert-base-multilingual-cased`
    - C. `FacebookAI/xlm-roberta-large` 또는 더 큰 encoder-only 모델
    - D. 다른 모델 직접 지정:
    - 내 답: xlm-roberta-base

3. base model 선택 기준
    - A. GPU 2장으로 빨리 실험 가능한 모델
    - B. target10 tokenization 문제가 뚜렷해서 vocab extension 효과를 보이기 좋은 모델
    - C. 논문/보고서 novelty가 더 좋아 보이는 모델
    - D. downstream 성능이 가장 잘 나올 가능성이 높은 모델
    - 내 답:  xlm-roberta-base 으로 glot500 처럼 language adaptation 진행하고 이를 활용한 downstream task 까지 진행

4. 사용할 언어
    - A. first_try target10 그대로 사용: acu, ake, bsn, chr, cop, kbh, nhg, oji, syr, usp
    - B. vocab/MLM은 target10 전체, downstream은 가능한 언어만 사용
    - C. downstream dataset 확보 가능한 언어로 target10 일부 교체
    - 내 답: downstream dataset 확보 가능한 언어로 target10 일부 교체하되 너무 쉬운 데이터는 아니였으면 좋겠음. 사전에 미리 기본 성능을 테스트해서 일정 수준 이하만 사용

5. 새 vocabulary 구성 방식
    - A. 10개 언어 데이터를 합쳐 joint tokenizer를 만든 뒤 base tokenizer에 merge
    - B. 언어별 tokenizer를 만든 뒤 합쳐서 merge
    - C. 기존 tokenizer에서 성능 나쁜 언어/스크립트만 골라 selective extension
    - 내 답:

6. 추가 vocabulary 크기
    - A. 하나의 고정 크기만 사용
    - B. 작은 grid 사용: 예를 들어 8k, 16k, 32k
    - C. tokenization 지표가 일정 기준을 넘을 때까지 조정
    - 원하는 크기:
    - 내 답: 작은 grid 사용: 예를 들어 8k, 16k, 32k 

7. embedding initialization 비교 범위
    - A. 빠른 비교: random vs mean만 비교
    - B. tutorial에 나온 방법 전부 비교
    - C. random/mean으로 먼저 gate를 보고, 좋은 경우에만 추가 방법 비교
    - 내 답: tutorial에 나온 방법 전부 비교

8. 반드시 비교할 initialization 방법
    - A. random init
    - B. 기존 tokenizer subtoken embedding mean
    - C. weighted mean
    - D. script/language average
    - E. nearest-neighbor 기반 초기화
    - F. tutorial 확인 후 추가
    - 내 답: tutorial 확인 후 추가

9. 다음 단계로 넘어가는 gate 기준
    - A. tokenization 개선만 확인되면 다음 단계 진행
    - B. tokenization 개선 + MLM dev loss 개선이 모두 있어야 진행
    - C. downstream pilot에서 baseline보다 좋아야 full run 진행
    - 내 답: tokenization 개선 + MLM dev loss 개선이 모두 있어야 진행

10. tokenization gate 지표
    - A. tokens/word 감소
    - B. single-character token 비율 감소
    - C. unk token 비율 감소 또는 0 유지
    - D. 위 세 가지 모두
    - 내 답: 위 세 가지 모두

11. 성능 비교 기준
    - A. 원본 base model 대비 개선
    - B. first_try Glot500 결과 대비 개선
    - C. random init 대비 mean/other init 개선
    - D. downstream task별 strongest baseline 대비 개선
    - 내 답: downstream task별 strongest baseline 대비 개선

12. 내가 직접 확인할 샘플 수
    - A. 언어별 5개
    - B. 언어별 10개
    - C. 전체에서 대표/실패 케이스 합쳐 50개
    - D. 직접 지정:
    - 내 답: 언어별 10개 + 대표 실패케이스 10개

13. 샘플 파일에 포함할 내용
    - A. 원문 + 기존 tokenizer 결과 + extended tokenizer 결과
    - B. A + 새 token이 어떤 기존 subtoken들로 초기화됐는지
    - C. B + MLM prediction 예시
    - D. C + downstream prediction 예시
    - 내 답: C + downstream prediction 예시

14. downstream task 3개 선정 방향
    - A. Bible 기반 proxy task 3개로 빠르게 구성
        - language identification
        - book/genre classification
        - parallel verse matching 또는 retrieval/ranking
    - B. 외부 labeled dataset을 찾아서 실제 NLP task 위주로 구성
        - sequence classification
        - token classification
        - sentence-pair classification
    - C. proxy task 1-2개 + 실제 labeled task 1-2개 혼합
    - 내 답: Bible 기반 proxy task 3개로 빠르게 구성

15. proxy task 허용 여부
    - A. 허용. 대신 쉬운 task라는 한계를 명시
    - B. 일부만 허용. 최종 주장은 실제 labeled task 중심
    - C. 허용하지 않음. 외부 downstream dataset만 사용
    - 내 답: 허용. 대신 쉬운 task라는 한계를 명시

16. downstream task 후보 중 우선순위
    - A. language identification
    - B. book/genre classification
    - C. verse retrieval/ranking
    - D. parallel verse matching
    - E. POS/NER 등 token classification
    - F. sentiment/topic 등 sequence classification
    - 내 답: 적당히 잘 사용해봐.

17. baseline/ablation 구성
    - A. 최소: original base vs best vocab-extended model
    - B. 기본: original base vs random init vs mean init vs best init
    - C. 전체: original base + all init methods + MLM adaptation 전후 + downstream
    - 내 답: 비교할 수 있는건 다해봐.

18. seed 반복
    - A. single seed만 사용하고 sample/qualitative 분석 보강
    - B. 핵심 실험만 3 seeds
    - C. 모든 downstream 실험 3 seeds
    - 내 답: 시드 고정된 몇개 비교해서 좋은걸로 선택

19. GPU 사용 방식
    - A. GPU 2,3에 서로 다른 실험을 하나씩 병렬 실행
    - B. 한 실험에 GPU 2장을 묶어서 DDP로 실행
    - C. stage별로 다르게 사용
    - 내 답: stage별로 다르게 사용

20. checkpoint 저장 정책
    - A. 모든 checkpoint 저장
    - B. gate 통과 후보만 저장
    - C. final/best checkpoint만 저장하고 중간 결과는 metrics만 저장
    - 내 답: gate 통과 후보만 저장 

21. 최종 보고서의 핵심 주장
    - A. Glot500-style vocab extension을 다른 encoder-only 모델에 적용했다
    - B. 새 token embedding initialization 방법을 비교했다
    - C. vocab extension이 downstream task까지 성능 개선으로 이어지는지 검증했다
    - D. 저자원/미지원 언어에서 tokenizer bottleneck과 해결 조건을 분석했다
    - 내 답: 저자원/미지원 언어에서 tokenizer bottleneck과 해결 조건을 제시하고 vocab extension이 downstream task까지 성능 개선으로 이어지는지 검증

22. 반드시 따라야 할 문서 우선순위
    - A. `docs/survey/GLOT500_extension.pdf`
    - B. `docs/exp/second_try/feedback/vocab_extension_tutorial.pdf`
    - C. `docs/survey` 전체를 먼저 종합한 뒤 결정
    - D. first_try에서 이미 만든 구현/결과를 우선 재사용
    - 내 답: `docs/survey`, `/home/axt/jongha/Glot500-py39-eval/docs/exp/second_try/feedback` 전체를 먼저 종합한 뒤 결정

답변 템플릿

```text
1-
2-
3-
4-
5-
6-
7-
8-
9-
10-
11-
12-
13-
14-
15-
16-
17-
18-
19-
20-
21-
22-
```

2차 추가 질문사항

아래는 답변을 읽고도 아직 실험 설계에서 결정이 필요한 항목만 다시 줄인 것이다.
이번에도 `1-A`처럼 짧게 답하면 된다.

1. 언어 선정 정책
    - A. first_try target10을 최대한 유지하고, downstream만 가능한 언어 subset으로 평가
    - B. downstream dataset 확보 가능한 언어로 target10 일부 교체
    - C. 먼저 후보 언어를 넓게 모은 뒤, base model 성능이 낮은 10개를 새 target10으로 확정
    - 내 답: first_try target10을 최대한 유지하고, downstream만 가능한 언어 subset으로 평가

2. 언어 교체 시 기본 성능이 "낮다"는 기준
    - A. original XLM-R downstream accuracy/F1이 70% 이하
    - B. original XLM-R downstream accuracy/F1이 80% 이하
    - C. task별 majority/random baseline보다 높지만 충분히 어렵다고 판단되는 경우
    - D. 직접 지정:
    - 내 답: 이전 정도면 충분할 듯, blank 나 unk 이런게 나오는거 혹은 char 단위로 쪼개지는거 score 로 재서

3. downstream task를 Bible proxy로 할 때 난이도 조절 방식
    - A. 쉬운 language identification은 제외하고 book/genre/retrieval 중심으로 구성
    - B. language identification 포함하되 script가 다른 언어만으로 쉽게 맞히지 못하게 같은 script 언어를 충분히 섞음
    - C. language identification은 tokenization sanity check로만 쓰고 최종 주장은 retrieval/classification task 중심
    - 내 답: language identification은 tokenization sanity check로만 쓰고 최종 주장은 retrieval/classification task 중심

4. 최종 downstream task 3개 후보
    - A. book/genre classification + verse retrieval/ranking + parallel verse matching
    - B. language identification + book/genre classification + verse retrieval/ranking
    - C. book/genre classification + masked-token probing + verse retrieval/ranking
    - D. 직접 지정:
    - 내 답: 이건 레퍼런스 다시 읽어보고 plan 작성후 질문사항으로 정리

5. 새 vocabulary 구성 방식
    - A. 10개 언어 joint tokenizer를 만들고 XLM-R tokenizer에 merge
    - B. 언어별 tokenizer를 만든 뒤 중복 제거해서 merge
    - C. 먼저 tokenization이 나쁜 언어만 selective extension
    - 내 답: 이전에 first 에서 했던 방식과 유사하게

6. vocab size grid 실행 범위
    - A. 8k, 16k, 32k 모두 tokenizer metric까지만 비교하고, MLM/downstream은 best size만 진행
    - B. 8k, 16k, 32k 모두 MLM까지 비교하고, downstream은 best size만 진행
    - C. 8k, 16k, 32k 모두 downstream까지 비교
    - 내 답: 8k, 16k, 32k 모두 downstream까지 비교

7. gate 통과 숫자 기준
    - A. tokens/word 15% 이상 감소 + single-char 비율 20% 이상 감소 + MLM dev loss original보다 감소
    - B. tokens/word 10% 이상 감소 + single-char 비율 10% 이상 감소 + MLM dev loss original보다 감소
    - C. 언어별로 개선 방향만 확인하고 downstream pilot에서 최종 판단
    - D. 직접 지정:
    - 내 답:

8. initialization 방법이 많을 때 비교 범위
    - A. tutorial의 모든 방법을 embedding init + 짧은 MLM pilot까지만 비교하고 best만 downstream
    - B. tutorial의 모든 방법을 downstream pilot까지 비교
    - C. random, mean, tutorial 대표 1-2개만 downstream까지 비교
    - 내 답: tutorial의 모든 방법을 downstream pilot까지 비교

9. seed 비교 방식
    - A. 모든 pilot은 fixed seed 1개, 최종 best만 3 seeds
    - B. init 비교는 3 seeds, downstream은 best만 3 seeds
    - C. 모든 주요 실험 3 seeds
    - 내 답: init 비교는 3 seeds, downstream은 best만 3 seeds

10. "비교할 수 있는 건 다"의 현실적 범위
    - A. original XLM-R, vocab-only, vocab+MLM, best-init+MLM만 비교
    - B. original XLM-R, all-init vocab+MLM, best downstream 비교
    - C. original XLM-R, all vocab sizes, all init methods, MLM 전후, downstream 전부 비교
    - 내 답: original XLM-R, all-init vocab+MLM, best downstream 비교

11. MLM adaptation 데이터
    - A. downstream task와 같은 Bible corpus 사용, split leakage만 방지
    - B. Bible 외 unlabeled corpus를 추가로 찾아 사용
    - C. language별 데이터 양을 맞춰 balanced corpus로 구성
    - 내 답: downstream task와 같은 Bible corpus 사용, split leakage만 방지

12. 결과 저장/보고 형식
    - A. stage별 `results.md` + TSV metrics + sample markdown
    - B. stage별 `results.md`만 작성
    - C. 최종 보고서용 표/그림까지 매 stage에서 같이 생성
    - 내 답: stage별 `results.md` + TSV metrics + sample markdown
