# Second Try Resolved Questions

작성일: 2026-06-10

이 파일은 개별 레퍼런스 요약과 종합 plan을 만든 뒤 확정한 질문/답변을 정리한 것이다.
이 답변은 `step_index.md`와 각 step folder의 gate 기준에 반영한다.

## 꼭 답해야 하는 질문

1. 최종 downstream task 3개를 `docs/exp/second_try/downstream_tasks.md` 추천안 그대로 갈 것인가?
    - A. 그대로 사용: book/genre classification + verse retrieval/ranking + parallel verse matching
    - B. language identification 포함: language ID + book/genre classification + verse retrieval/ranking
    - C. masked-token probing 포함: book/genre classification + masked-token probing + verse retrieval/ranking
    - D. 직접 지정:
    - 내 답: A. 그대로 사용

2. Book/genre classification의 label을 무엇으로 둘 것인가?
    - A. Bible book id 전체 분류
    - B. broad genre 분류: gospel/epistle/prophecy/etc.
    - C. chapter range 또는 section 분류
    - D. 둘 다 pilot 후 어려운 쪽 선택
    - 내 답: B. broad genre 분류를 기본으로 사용하고, book id는 pilot diagnostic으로만 사용

3. Verse retrieval/ranking은 어떤 방향으로 만들 것인가?
    - A. 같은 언어 안에서 query verse -> same verse id retrieval
    - B. 언어 간 parallel verse retrieval
    - C. 같은 book/chapter 후보 안에서 hard retrieval
    - D. B와 C를 섞어 hard negative 중심으로 구성
    - 내 답: D. 언어 간 parallel verse retrieval과 같은 book/chapter hard retrieval을 섞어 구성

4. Parallel verse matching의 negative pair는 어떻게 만들 것인가?
    - A. random negative
    - B. 같은 book 안 random negative
    - C. 같은 chapter 안 hard negative
    - D. random + same book + same chapter를 모두 섞음
    - 내 답: D. random + same book + same chapter negative를 모두 섞음

5. Tokenization gate의 숫자 기준을 어떻게 둘 것인가?
    - A. tokens/word 10% 감소 + single-char 10% 감소 + MLM dev loss 개선
    - B. tokens/word 15% 감소 + single-char 20% 감소 + MLM dev loss 개선
    - C. 언어별 개선 방향만 확인하고 downstream pilot에서 판단
    - D. 직접 지정:
    - 내 답: A. tokens/word 10% 감소 + single-char 10% 감소 + MLM dev loss 개선

6. `byte_fallback`을 사용할 것인가?
    - A. 사용하지 않음. first_try 방식과 최대한 유사하게 간다.
    - B. 사용함. 단 byte fallback rate를 별도 지표로 기록한다.
    - C. 8k/16k/32k grid와 별도로 byte_fallback on/off도 pilot한다.
    - 내 답: A. 사용하지 않음. first_try 방식과 최대한 유사하게 간다.

7. Embedding init 방법 중 구현 부담이 큰 방법은 어디까지 할 것인가?
    - A. required 전체: random, mean, fvt, align, focus
    - B. random, mean, fvt, align까지만 우선
    - C. random, mean, fvt까지만 먼저 하고 focus/align은 stretch
    - D. tutorial에 나온 Ofa/Wechsel까지 모두 시도
    - 내 답: A. required 전체: random, mean, fvt, align, focus

8. Focus에 필요한 fastText 또는 auxiliary embedding은 어떻게 처리할 것인가?
    - A. target Bible corpus로 직접 학습
    - B. 공개 fastText vector가 있으면 사용, 없으면 skip
    - C. Focus는 구현 부담 때문에 stretch로 둔다
    - 내 답: A. target Bible corpus로 직접 학습

9. MLM adaptation은 target-only로 갈 것인가, replay/mixed data를 섞을 것인가?
    - A. target10 Bible train/dev only
    - B. target10 + English/Greek 등 related/replay sample
    - C. target-only pilot 후 forgetting 문제가 보이면 replay 추가
    - 내 답: A. target10 Bible train/dev only

10. Downstream full run 범위는 어디까지인가?
    - A. best checkpoint + original XLM-R만 3 seeds
    - B. best checkpoint + original XLM-R + best vocab-only를 3 seeds
    - C. vocab size별 best checkpoint를 모두 3 seeds
    - 내 답: A. best checkpoint + original XLM-R만 3 seeds

## 기본값으로 진행 가능한 질문

아래는 답변이 없으면 plan의 추천값으로 진행해도 되는 항목이다.

11. Split은 first_try처럼 book-level split으로 둘 것인가?
    - 기본값: train = all except Mark/John, dev = Mark, test = John
    - 내 답: 기본값 사용

12. Sample 파일은 어디까지 포함할 것인가?
    - 기본값: 언어별 10개 + 대표 실패 10개, tokenizer before/after + init trace + MLM prediction + downstream prediction
    - 내 답: 기본값 사용

13. Checkpoint 저장 정책은 그대로 gate 통과 후보만 저장할 것인가?
    - 기본값: gate 통과 후보만 저장
    - 내 답: 기본값 사용

14. 최종 주장은 어느 톤으로 쓸 것인가?
    - 기본값: "tokenizer bottleneck을 줄일 수 있고, 일부 encoder-only downstream task에서 개선되는지 검증한다"
    - 내 답: 기본값 사용

## 답변 템플릿

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
```
