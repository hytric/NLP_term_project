# Experiment Workspace

이 디렉터리는 Coptic-Syriac NMT 텀프로젝트를 논문화 가능한 실험 프로젝트로 관리하기 위한 공간이다.

## Presentation Entry Point

발표용으로 순서대로 보려면 [2026-06-05_experiment_presentation.md](./2026-06-05_experiment_presentation.md)를 먼저 읽는다.
이 문서는 각 실험을 질문, 코드 진입점, 실행 예시, 결과 해석, 발표 멘트 순서로 묶었다.

## Final Goal

2026-07-03까지 약 10개 저자원 언어를 Glot500 계열 모델에 추가하는 multilingual adaptation 파일럿을 만들고, 그중 Coptic/Syriac을 핵심 번역 사례로 삼아 tokenizer extension과 embedding initialization ablation 중심의 10페이지 term paper와 재현 가능한 GitHub 코드를 제출한다.

최종 논문형 질문:

> How can we adapt multilingual pretrained models to a small set of unsupported or underrepresented low-resource languages, and which vocabulary extension and embedding initialization choices most reliably improve representation quality and Coptic-Syriac translation?

## Folder Rule

새 실험 폴더는 아래 규칙을 따른다.

```text
YYYY-MM-DD_NN_short_slug/
  plan.md
```

규칙:

- `YYYY-MM-DD`: 실험 계획을 만든 날짜
- `NN`: 전체 실험 순서, 두 자리 숫자
- `short_slug`: 소문자 snake_case 설명
- 모든 실험 폴더에는 `plan.md`를 둔다.
- 실험 결과가 생기면 같은 폴더 안에 `results.md`, `metrics.*`, `notes.md` 등을 추가한다.
- 폴더 순서는 논문/프로젝트 의존성 순서를 따른다. 앞 단계 gate가 약하면 뒤 실험 결과도 약해진다.

## Ordered Plan

| Order | Folder | Purpose | Gate |
| ---: | --- | --- | --- |
| init | [2026-06-02_init_project](./2026-06-02_init_project/plan.md) | survey synthesis and initial framing | project direction documented |
| 00 | [2026-06-03_00_final_goal](./2026-06-03_00_final_goal/plan.md) | final objective, paper thesis, milestones | success criteria frozen |
| 01 | [2026-06-03_01_data_and_splits](./2026-06-03_01_data_and_splits/plan.md) | collect data inventory and split rules | train/dev/test and license table ready |
| 02 | [2026-06-03_02_tokenization_audit](./2026-06-03_02_tokenization_audit/plan.md) | prove tokenizer bottleneck | fragmentation table ready |
| 03 | [2026-06-03_03_vocab_extension](./2026-06-03_03_vocab_extension/plan.md) | train target10 tokenizer and merge into Glot500 | extended tokenizer validated |
| 04 | [2026-06-03_04_embedding_init](./2026-06-03_04_embedding_init/plan.md) | compare random, mean, align initialization | init ablation result ready |
| 05 | [2026-06-03_05_mlm_adaptation](./2026-06-03_05_mlm_adaptation/plan.md) | continued pretraining for representation adaptation | adapted checkpoint selected |
| 06 | [2026-06-03_06_nmt_baselines](./2026-06-03_06_nmt_baselines/plan.md) | build direct and multitask NMT baselines | first BLEU/chrF++ table ready |
| 07 | [2026-06-03_07_pivot_backtranslation](./2026-06-03_07_pivot_backtranslation/plan.md) | pivot and synthetic data experiments | back-translation effect measured |
| 08 | [2026-06-03_08_evaluation_analysis](./2026-06-03_08_evaluation_analysis/plan.md) | quantitative and qualitative analysis | paper-ready result tables |
| 09 | [2026-06-03_09_report_release](./2026-06-03_09_report_release/plan.md) | progress report, final paper, reproducibility | submission package ready |
| 10 | [2026-06-04_10_source_grounding_editing](./2026-06-04_10_source_grounding_editing/plan.md) | source-grounding diagnostics and retrieval-editing gate | copy dependence reduced or documented |
| 11 | [2026-06-04_11_release_audit](./2026-06-04_11_release_audit/plan.md) | final artifact, license, storage, and worktree audit | release risks documented |

Current status as of 2026-06-04:

- 07 is a negative gate: Greek pivot/back-translation should not be scaled from the current ByT5-small pilots.
- 08 has draft metric tables, paper tables, qualitative analysis, and error taxonomy.
- 09 has draft progress report, term paper outline, presentation outline, reproducibility checklist, command examples, claim-evidence map, license notes, limitations, related-work notes, and submission checklist.
- 10A source-candidate diagnostics, pointwise 10B, pairwise 10B selection, and 10C same-checkpoint GPU controls are complete. Pairwise 10B reaches test corpus chrF++ 24.7438, slightly above pointwise 10B at 24.6862 and the existing feature reranker at 24.5921, while oracle@8 remains 28.3327. The 10C ByT5 edit gate is negative: correct pairwise source+retrieval reaches 18.3574 chrF++, source-only collapses to 0.2729, retrieved-only slightly beats correct at 18.6220, wrong-shift1 drops to 12.8253, and feature-selected reaches 19.1558. Use this as failure analysis, not a positive neural editing claim.
- 11 is the release audit stage. It confirms the active experiment-progress goal is satisfied, records that large artifacts are kept on `/disk1`, notes that root `main.zip` is ignored and should not be released, records partial source-specific license evidence, and separates remaining public GitHub cleanup from the completed experiment-progress objective.

## Primary Novelty

1. Span-aware embedding initialization for new low-resource subwords.
2. Tokenization fragmentation metrics as explanatory predictors for multilingual adaptation quality.
3. Coptic/Syriac as an ancient-language case study inside a broader 10-language extension pilot.

## Minimum Viable Paper

The minimum viable paper does not require every stretch experiment.
It requires:

- 10-language data inventory and clean held-out evaluation split
- tokenizer audit showing which languages/scripts overfragment
- joint 10-language vocabulary extension
- random vs mean or random vs mean vs align initialization ablation
- at least one Coptic -> Syriac and Syriac -> Coptic baseline with BLEU and chrF++
- qualitative error analysis
- reproducibility instructions
