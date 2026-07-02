# v5 Metric Surface Completeness Audit

Last checked: 2026-06-28 18:08 KST

Verdict: `metric_surface_completeness_ready`

This generated audit checks that the main report and deck surfaces expose
all retained Glot500 metric families. It complements metric fidelity:
metric fidelity checks mapping/coverage/aggregation, while this audit
checks what a reader actually sees in report/PPT sources and rendered
HTML/PDF/PPTX handoff artifacts.

Required metric families:

- PPPL / Pseudoperplexity
- Tatoeba retrieval
- Bible retrieval
- Text classification / Taxi1500
- NER
- POS
- Roundtrip alignment

| Surface | Kind | Reader | Status | Mention counts | Missing metrics | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Report.md | source | plain_text | ready | pseudoperplexity=46; retrieval_tatoeba=19; retrieval_bible=25; text_classification=15; ner=21; pos=26; roundtrip_alignment=20 | - | none |
| 4_reporting/03_final_report/paper_draft.md | source | plain_text | ready | pseudoperplexity=32; retrieval_tatoeba=12; retrieval_bible=16; text_classification=9; ner=15; pos=22; roundtrip_alignment=15 | - | none |
| 4_reporting/03_final_report/paper_draft_ko.md | source | plain_text | ready | pseudoperplexity=13; retrieval_tatoeba=4; retrieval_bible=6; text_classification=4; ner=3; pos=4; roundtrip_alignment=6 | - | none |
| 4_reporting/02_slides/final_deck_ko.md | source | plain_text | ready | pseudoperplexity=12; retrieval_tatoeba=3; retrieval_bible=3; text_classification=3; ner=4; pos=3; roundtrip_alignment=5 | - | none |
| 4_reporting/02_slides/ppt_content.md | source | plain_text | ready | pseudoperplexity=16; retrieval_tatoeba=10; retrieval_bible=11; text_classification=8; ner=10; pos=12; roundtrip_alignment=11 | - | none |
| 4_reporting/03_final_report/paper_draft.html | rendered | html_text | ready | pseudoperplexity=32; retrieval_tatoeba=12; retrieval_bible=16; text_classification=9; ner=15; pos=22; roundtrip_alignment=15 | - | none |
| 4_reporting/03_final_report/paper_draft.pdf | rendered | pdftotext | ready | pseudoperplexity=31; retrieval_tatoeba=12; retrieval_bible=16; text_classification=8; ner=15; pos=22; roundtrip_alignment=15 | - | none |
| 4_reporting/03_final_report/paper_draft_ko.html | rendered | html_text | ready | pseudoperplexity=13; retrieval_tatoeba=4; retrieval_bible=6; text_classification=4; ner=3; pos=4; roundtrip_alignment=6 | - | none |
| 4_reporting/03_final_report/paper_draft_ko.pdf | rendered | pdftotext | ready | pseudoperplexity=21; retrieval_tatoeba=4; retrieval_bible=6; text_classification=4; ner=3; pos=5; roundtrip_alignment=6 | - | none |
| 4_reporting/02_slides/v5_final_deck_ko.html | rendered | html_text | ready | pseudoperplexity=12; retrieval_tatoeba=3; retrieval_bible=3; text_classification=3; ner=4; pos=3; roundtrip_alignment=5 | - | none |
| 4_reporting/02_slides/v5_final_deck_ko.pdf | rendered | pdftotext | ready | pseudoperplexity=12; retrieval_tatoeba=3; retrieval_bible=3; text_classification=3; ner=4; pos=3; roundtrip_alignment=5 | - | none |
| 4_reporting/02_slides/v5_final_deck_ko.pptx | rendered | pptx_xml | ready | pseudoperplexity=12; retrieval_tatoeba=3; retrieval_bible=3; text_classification=3; ner=4; pos=3; roundtrip_alignment=5 | - | none |
| combined_source_report_ppt_surfaces | summary | combined | ready | pseudoperplexity=119; retrieval_tatoeba=48; retrieval_bible=61; text_classification=39; ner=53; pos=67; roundtrip_alignment=57 | - | none |
| combined_rendered_report_ppt_surfaces | summary | combined | ready | pseudoperplexity=133; retrieval_tatoeba=41; retrieval_bible=53; text_classification=34; ner=48; pos=62; roundtrip_alignment=57 | - | none |

Use:

- If this audit fails, do not claim that the final report/PPT faithfully presents all Glot500 metric families.
- Rendered artifacts are checked so PDF/PPTX handoff files cannot silently drop a metric family during conversion.
- Coverage-limited metrics should remain visible as measured, waiting, blocked, or coverage-limited rather than being silently dropped.
