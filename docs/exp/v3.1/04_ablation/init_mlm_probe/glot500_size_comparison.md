# Glot500 Size Comparison

작성일: 2026-06-19

## Source

Glot500 reference: `docs/survey/2305.12182v2.pdf`.

Relevant Glot500 paper facts used here:

- Glot500-c covers `511` languages and `534` language-scripts.
- Glot500-c uses a safe inclusion threshold of `30,000` sentence/chunks per language-script.
- Table 1 reports about `1.5B` sentence/chunks for Glot500-c and a median of about `120K` sentence/chunks per language-script.
- The paper frames Glot500-m as trained on about a `600GB` corpus.
- Glot500-m continued pretraining uses MLM, LR `5e-5`, Adam betas `(0.9, 0.999)`, batch `384`, chunks of `512` tokens.
- The released Glot500-m snapshot is at about `480K` steps.

## Corpus Scale

| Item | Glot500-c / Glot500-m | This v3.1 init MLM probe | Ratio |
| --- | ---: | ---: | ---: |
| languages | 511 | target10 + 4 replay/control high-resource languages | much smaller scope |
| language-scripts | 534 | target10 scripts + replay scripts | much smaller scope |
| corpus size | about 600GB | 297.5MB train mixture | `0.0496%` of Glot500, about `1/2,017` |
| sentence/chunk rows | about 1.5B | 966,152 raw train lines | `0.0644%`, about `1/1,553` |
| HF 512-token train chunks | not directly Table-1 comparable | 136,039 chunks | small probe corpus |
| minimum inclusion threshold | >30,000 sentence/chunks per language-script | target10 median train rows 5,280.5 | `17.6%` of Glot500 threshold |
| target low-resource train rows | 30K+ per included language-script | 52,016 total across 10 languages | far smaller per language |
| target low-resource train+dev+final rows | 30K+ per included language-script | 68,341 total across 10 languages | `0.00456%` of Glot500 1.5B |

Our full materialized Stage01 text directory is `722,874,721` bytes, but that includes train/dev/final/control/tokenizer files. The actual MLM train mixture used in this probe is `297,541,640` bytes.

## Training Budget Scale

| Item | Glot500-m | This v3.1 init probe | Ratio |
| --- | ---: | ---: | ---: |
| optimizer steps | about 480,000 released snapshot | 200 | `1/2,400` |
| batch per step | 384 samples | 32 effective chunks | `1/12` |
| approximate consumed samples/chunks | 184,320,000 | 6,400 | `0.00347%`, exactly `1/28,800` |
| sequence length | 512 | 512 | same |
| objective | MLM | MLM | same family |
| optimizer LR | 5e-5 | 5e-5 | same nominal LR |

This means the current run is not a Glot500-scale continued pretraining run. It is a small controlled ablation to compare initialization and proxy behavior under a fixed tiny budget.

## Methodological Reading

What is comparable:

- same model family: XLM-R/RoBERTa-style masked LM;
- same broad MLM objective;
- same chunk length `512`;
- same nominal learning rate `5e-5`;
- similar vocabulary-extension motivation.

What is not comparable:

- corpus size differs by roughly three orders of magnitude;
- training budget differs by almost five orders of magnitude in consumed chunks;
- Glot500 trains over hundreds of languages, while this probe targets target10 with replay/control data;
- Glot500 has at least `30K` sentence/chunks per included language-script, while our target10 median train rows are about `5.3K`;
- Glot500 selected a checkpoint by downstream average across many tasks; this probe compares 200-step MLM dev loss and encoder-feature diagnostics.

## Consequence For Claims

Safe claim:

> Under a deliberately small fixed MLM budget, initialization changes token-prediction loss and sentence-level feature attachment diagnostics differently.

Unsafe claim:

> This reproduces Glot500-scale continued pretraining.

> This is enough to conclude Glot500-style low-resource multilingual adaptation quality.

The right framing is:

> v3.1 is a small-scale controlled probe inspired by Glot500's append-vocabulary and MLM adaptation protocol, not a scale reproduction of Glot500-m.
