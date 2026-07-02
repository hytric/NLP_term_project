# v4 Dataset Locations and Notes

작성일: 2026-06-26

이 문서는 v4 tokenizer/MLM 실험에서 실제로 사용한 데이터셋 위치를 빠르게
확인하기 위한 메모이다. 자세한 생성 절차는
`docs/exp/v4/0_tokenizer/dataset_processing.md`를 기준 문서로 본다.

## 빠른 요약

- 최종 tokenizer 학습 corpus:
  `/home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt`
- 최종 corpus 구성: XLM-R seen Glot500 언어 `92`개 + target10 low-resource
  언어 `10`개
- 최종 corpus 줄 수: `13,844,487`
- 최종 corpus 파일 크기: `3,028,775,281` bytes
- merge 상태: `PASS`
- merge raw dataset root:
  `/home/axt/mnt2/jongha/v4_tokenizer/raw`
- merge manifest:
  `docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.manifest.tsv`
- merge report:
  `docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.report.json`

## XLM-R Seen Glot500 데이터

Seen 언어는 최종 merge에서 다음 경로 아래에 있는 것처럼 읽힌다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/raw/{language_script}
```

하지만 실제 데이터 파일은 이 위치에 복사되어 있지 않고, 기존 Glot500 raw
저장소로 연결된 symlink이다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/raw/{language_script}
-> /disk3/moon/Glot500/data/raw/{language_script}
```

예시:

```text
/home/axt/mnt2/jongha/v4_tokenizer/raw/eng_Latn
-> /disk3/moon/Glot500/data/raw/eng_Latn
```

확인 당시 `/home/axt/mnt2/jongha/v4_tokenizer/raw` 아래 seen 언어 symlink는
`92`개이다. 이 92개가 최종 mixed corpus의 seen group으로 들어갔다.

## target10 Low-Resource 데이터

target10의 원본 clean text와 row manifest는 다음 위치이다.

```text
/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/target10_train_clean.txt
/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_train_rows.tsv
```

`mlm_train_rows.tsv`에서 `component == target10_v2_train`인 row만 사용했다.
이 row들을 언어별로 나누어 HF `DatasetDict` 형태로 새로 저장한 위치는 다음과
같다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/raw/{language_script}
```

target10 디렉터리는 seen 언어와 달리 symlink가 아니라 실제 HF dataset
directory이다. 각 dataset은 `train` split과 `text` column을 갖는다.

| language_script | rows | HF dataset directory |
| --- | ---: | --- |
| `acu_Latn` | 5,168 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/acu_Latn` |
| `ake_Latn` | 5,178 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/ake_Latn` |
| `bsn_Latn` | 5,063 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/bsn_Latn` |
| `chr_Cher` | 5,393 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/chr_Cher` |
| `cop_Copt` | 5,388 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/cop_Copt` |
| `kbh_Latn` | 4,505 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/kbh_Latn` |
| `nhg_Latn` | 5,267 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/nhg_Latn` |
| `oji_Cans` | 5,384 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/oji_Cans` |
| `syr_Syrc` | 5,376 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/syr_Syrc` |
| `usp_Latn` | 5,294 | `/home/axt/mnt2/jongha/v4_tokenizer/raw/usp_Latn` |

target10 생성 manifest:

```text
docs/exp/v4/0_tokenizer/miscellaneous/target10_hf_dataset_manifest.tsv
```

## 토크나이저 산출물 위치

Tokenizer 학습 산출물은 다음 위치에 있다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output
```

주요 파일:

- Auxiliary SentencePiece model:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.model`
- Auxiliary vocab:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.vocab`
- XLM-R SPM 뒤에 새 piece를 append한 model:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm.model`
- Hugging Face tokenizer directory:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm`

## MLM 학습 산출물 위치

v4 continued MLM run과 checkpoint는 다음 위치에 있다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/runs/Glot500_v4_target10_xlmr100_xlmr_base_mlm
```

문서에 기록된 평가 checkpoint 예시는 다음과 같다.

```text
/home/axt/mnt2/jongha/v4_tokenizer/runs/Glot500_v4_target10_xlmr100_xlmr_base_mlm/checkpoint-30000
/home/axt/mnt2/jongha/v4_tokenizer/runs/Glot500_v4_target10_xlmr100_xlmr_base_mlm/checkpoint-40000
```

## 특이사항

- 이번 v4 tokenizer 입력은 target10-only corpus가 아니다. `92`개 seen 언어와
  `10`개 target10 언어를 합친 mixed corpus이다.
- target10 `cop_Copt`는 GlotCC 다운로드가 아니라 target10 clean text에서 만든
  HF dataset이다.
- `preprocessing/download_glot500c.py`와
  `preprocessing/download_glotcc_cop_syriac.py`는 최종 merge 시점에 직접 실행한
  스크립트가 아니다. 특히 `download_glotcc_cop_syriac.py` 산출물은 이번 최종
  corpus에 사용하지 않았다.
- XLM-R seen 후보 100개 중 아래 8개는 로컬 raw와 public `cis-lmu/Glot500`
  snapshot 양쪽에서 찾지 못해 제외했다.

```text
ben_Beng
rus_Cyrl
lao_Latn
tel_Telu
ori_Latn
lav_Latn
jpn_Latn
kir_Latn
```

- seen 언어 경로는 symlink이므로 `/disk3/moon/Glot500/data/raw` mount가 없으면
  깨질 수 있다.
- repository의 `data`와 `download`도 symlink이다. 다만 v4 tokenizer의 최종
  raw/data/run 경로는 주로 `/home/axt/mnt2/jongha/v4_tokenizer` 아래에 있다.
- corpus, checkpoint, HF cache, `wandb` 출력은 크고 환경 의존적이므로 git에
  commit하지 않는다. 문서에는 manifest와 report 경로만 남긴다.
