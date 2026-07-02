# Claim Boundary Checklist

이 파일은 최종 제출 전에 과장 표현을 잡기 위한 점검표다.

## 반드시 유지할 표현

- "50K-step convergence run을 중심으로 보고한다."
- "Step-4000 result는 early diagnostic이다."
- "같은 tokenizer, corpus, MLM objective, evaluation protocol에서 initialization을 비교한다."
- "coverage가 없는 group은 NA로 처리한다."
- "target7은 downstream coverage가 가능한 XLM-R-unseen language-script로 제한했다."

## 피해야 할 표현

- "FVT is always best."
- "Glot500을 완전 재현했다."
- "모든 low-resource language에 일반화된다."
- "target7은 script diversity를 대표한다."
- "4K에서 수렴했다."
- "coverage가 없는 task에서 target 성능이 개선됐다."

## 숫자 넣을 때 확인

- Lower-better metric과 higher-better metric을 구분했는가?
- Tail/head/all average가 같은 language set에서 계산됐는가?
- Task별 language count를 같이 썼는가?
- Method별 checkpoint step이 같은가?
- 50K final result와 Step-4000 diagnostic이 섞이지 않았는가?

