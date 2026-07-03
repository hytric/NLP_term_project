# Claim Boundary Checklist

이 파일은 최종 제출 전에 과장 표현을 잡기 위한 점검표다.

## 반드시 유지할 표현

- "간결하게 쓰되, 모든 주장에는 근거를 붙인다."
- "모든 수치는 50K-step convergence 기준이다(Step-4000 진단 미사용)."
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

- 모든 claim에 source artifact, code path, table, figure, 또는 reference가 붙어 있는가?
- Lower-better metric과 higher-better metric을 구분했는가?
- Tail/head/all average가 같은 language set에서 계산됐는가?
- Task별 language count를 같이 썼는가?
- Method별 checkpoint step이 같은가(모두 50K 기준)?
- 미완/미보고 지표는 pending 또는 제외로 명확히 표시했는가?

## 문장 다듬을 때 확인

- 한 문장에 하나의 주장만 담았는가?
- 근거 없는 "strong", "robust", "effective", "significant" 같은 표현을 지웠는가?
- Claim보다 evidence가 약하면 표현을 낮췄는가?
- 결과가 없는 부분은 확정 문장이 아니라 `TBD` 또는 future work로 남겼는가?
