# v4 토크나이저 코퍼스 데이터 처리 정리

이 문서는 `Glot500_v4_target10_xlmr100` 토크나이저 학습 코퍼스가
어디에서 왔고, 어떤 방식으로 전처리되어 최종 `.txt` 파일로 합쳐졌는지
정리한다.

## 최종 코퍼스

- 최종 출력 파일:
  `/home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt`
- 줄 수: `13,844,487`
- 파일 크기: 약 `2.9G`
- 생성 상태:
  `docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.report.json`
  기준 `PASS`
- 사용 언어 수: `102`
  - XLM-R seen Glot500 언어: `92`
  - target10 low-resource 언어: `10`

## 중요한 정리

최종 코퍼스를 만들 때 아래 두 다운로드 스크립트를 직접 실행해서 데이터를
가져온 것은 아니다.

- `preprocessing/download_glot500c.py`
- `preprocessing/download_glotcc_cop_syriac.py`

최종 생성 과정에서 실제로 사용한 구조는 다음과 같다.

- 최종 merge는 `/home/axt/mnt2/jongha/v4_tokenizer/raw` 아래의 HF dataset
  directory들을 읽었다.
- 그중 XLM-R seen 언어 92개는 실제 데이터를 복사한 것이 아니라 symlink이다.
- 92개 symlink는 기존 로컬 Glot500 raw 저장소를 가리킨다:
  `/disk3/moon/Glot500/data/raw/{language_script}`
- 즉 seen 언어 데이터는 아래처럼 연결되어 있다:

```text
/home/axt/mnt2/jongha/v4_tokenizer/raw/eng_Latn
-> /disk3/moon/Glot500/data/raw/eng_Latn
```

- `preprocessing/download_glot500c.py`는 public `cis-lmu/Glot500` Hugging Face
  dataset에서 `/disk3/moon/Glot500/data/raw`를 채울 때 사용할 수 있는
  스크립트이다. 다만 이번 최종 재생성 시점에 직접 실행한 것은 아니다.
- `preprocessing/download_glotcc_cop_syriac.py`는 이번 코퍼스에 사용하지
  않았다. 이 스크립트는 GlotCC 기반 `cop_Copt`, `syc_Syrc` 보조 다운로드용이다.
- 이번 코퍼스의 `cop_Copt`는 GlotCC가 아니라 target10 clean text에서 만든
  데이터이다.

## 데이터 출처

### XLM-R Seen 언어

기준 언어 목록은 다음 파일에서 시작했다.

- `miscellaneous/languages_stats.csv`

이 파일에서 `XLM-R == True`인 행을 XLM-R seen 언어로 보았다. 원래는 100개가
있다.

하지만 아래 8개는 제외했다. 이유는 로컬 raw 데이터에도 없고,
`preprocessing/download_glot500c.py`가 사용하는 public `cis-lmu/Glot500`
snapshot에도 없었기 때문이다.

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

따라서 최종 코퍼스에는 XLM-R seen 언어 92개만 포함했다.

이 92개는 다음 위치에 있는 것처럼 보인다.

- `/home/axt/mnt2/jongha/v4_tokenizer/raw/{language_script}`

하지만 실제 데이터 위치는 다음 경로이다.

- `/disk3/moon/Glot500/data/raw/{language_script}`

`/home/axt/mnt2/jongha/v4_tokenizer/raw` 아래의 seen 언어 디렉터리들은 위
원본 위치를 가리키는 symlink이다.

### target10 Low-Resource 언어

target10의 원본 텍스트는 다음 파일이다.

- `/home/axt/mnt2/jongha/third_try/text/stage01_20260613_r1/target10_train_clean.txt`

언어별로 나누기 위해 사용한 row manifest는 다음 파일이다.

- `/home/axt/mnt2/jongha/third_try/manifests/stage01_20260613_r1/mlm_train_rows.tsv`

이 manifest에서 아래 조건을 만족하는 row만 사용했다.

```text
component == target10_v2_train
```

사용한 target10 언어는 다음 10개이다.

```text
acu_Latn
ake_Latn
bsn_Latn
chr_Cher
cop_Copt
kbh_Latn
nhg_Latn
oji_Cans
syr_Syrc
usp_Latn
```

이 10개는 symlink가 아니라 실제로 새로 만든 HF `DatasetDict` 디렉터리이다.
각 언어는 `train` split과 `text` column을 갖는다.

저장 위치:

- `/home/axt/mnt2/jongha/v4_tokenizer/raw/{language_script}`

생성된 target10 manifest:

- `docs/exp/v4/0_tokenizer/miscellaneous/target10_hf_dataset_manifest.tsv`

## 준비 스크립트

준비 단계는 다음 스크립트가 담당한다.

- `preprocessing/prepare_v4_tokenizer_merge_inputs.py`

이 스크립트가 하는 일은 다음과 같다.

1. target10 clean text와 `mlm_train_rows.tsv`를 읽는다.
2. target10 10개 언어를 각각 HF `DatasetDict`로 만들어
   `/home/axt/mnt2/jongha/v4_tokenizer/raw` 아래에 저장한다.
3. 사용 가능한 XLM-R seen 언어 92개와 target10 10개를 합친 stats CSV를 만든다.
4. missing 8개 XLM-R seen 언어는 제외한다.

실행 명령:

```bash
python3 preprocessing/prepare_v4_tokenizer_merge_inputs.py --overwrite_target10
```

생성된 stats CSV:

- `docs/exp/v4/0_tokenizer/miscellaneous/languages_stats_low10_xlmr100.csv`

현재 stats CSV 구조:

- `1`-`92`: 사용 가능한 XLM-R seen 언어
- `93`-`102`: target10 low-resource 언어
- 총 데이터 행 수: `102`

## Merge 및 샘플링

merge 단계는 다음 스크립트가 담당한다.

- `preprocessing/merge_files.py`

이 스크립트는 stats CSV를 읽고, `XLM-R` 컬럼을 기준으로 seen/unseen 언어를
나눈 뒤, 각 언어별 HF dataset에서 샘플링해 하나의 `.txt` 코퍼스로 합친다.

최종 실행 명령:

```bash
python3 preprocessing/merge_files.py \
  --data_directory /home/axt/mnt2/jongha/v4_tokenizer/raw \
  --save_directory /home/axt/mnt2/jongha/v4_tokenizer/data \
  --experiment_name Glot500_v4_target10_xlmr100 \
  --stats_csv docs/exp/v4/0_tokenizer/miscellaneous/languages_stats_low10_xlmr100.csv \
  --manifest_path docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.manifest.tsv \
  --report_path docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.report.json \
  --missing_policy fail
```

샘플링 설정:

- Seed: `13`
- Split: `train`
- Text column: `text`
- Language sampling factor: `0.3`
- Scale: `30`
- Missing policy: `fail`

샘플링 결과:

- Seen 언어 수: `92`
- Unseen target10 언어 수: `10`
- Planned seen samples: `12,433,800`
- Planned target10 samples: `1,410,687`
- Planned total samples: `13,844,487`
- Actual total samples: `13,844,487`
- Missing language directories: `0`

## 생성된 산출물

- Stats CSV:
  `docs/exp/v4/0_tokenizer/miscellaneous/languages_stats_low10_xlmr100.csv`
- target10 HF dataset manifest:
  `docs/exp/v4/0_tokenizer/miscellaneous/target10_hf_dataset_manifest.tsv`
- Merge manifest:
  `docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.manifest.tsv`
- Merge report:
  `docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.report.json`
- 최종 corpus:
  `/home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt`

## 토크나이저 생성 결과

토크나이저 생성은 완료됐다.

현재 실행 중인 명령은 `tokenization/run.py`를 사용한다. 이 스크립트는
SentencePiece unigram auxiliary tokenizer를 먼저 학습한 뒤, XLM-R의 기존
`sentencepiece.bpe.model`에 새 piece를 뒤에 append하는 방식으로 확장
tokenizer를 만든다.

중요한 점:

- 현재 입력은 target10-only corpus가 아니다.
- 입력 corpus는 `92`개 XLM-R seen 언어와 `10`개 target10 low-resource 언어가
  섞인 mixed corpus이다.
- 따라서 추가 후보 piece는 low-resource 10개에서만 나온 것이 아니라, mixed
  corpus 전체에서 학습된 auxiliary SentencePiece vocab에서 나온다.
- merge 단계에서는 auxiliary vocab 중 XLM-R 기존 vocab에 없는 piece만 기존
  XLM-R SPM의 맨 뒤에 추가된다.
- 즉 “뒤에 추가되는 방식”은 맞지만, “low-resource에서만 나온 piece만 추가”하는
  방식은 아니다.

Base XLM-R SPM은 다음 위치에 복사해 두었다.

- `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/sentencepiece.bpe.model`

원본 위치는 Hugging Face cache의 `xlm-roberta-base` snapshot이다.

실행 명령:

```bash
setsid bash -lc 'cd /home/axt/jongha/Glot500-py39-eval && exec /usr/bin/time -v python3 tokenization/run.py --input_fname /home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt --model_name xlm-roberta-base --save_directory /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/ --vocab_size 250000' \
  > /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log 2>&1 &
```

실행 PID 정보:

```text
time wrapper PID: 2435024
python child PID: 2435028
pid file: /home/axt/mnt2/jongha/v4_tokenizer/tokenization/tokenizer_train.pid
log file: /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log
```

완료 로그:

```text
Loaded all 13822655 sentences
Skipped 21831 too long sentences
Done! preprocessed 13822655 sentences.
Add 120431 tokens
Tokenizer training is done. Wrote /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm
Exit status: 0
```

`SentencePiece` 학습과 XLM-R SPM append merge가 정상 종료됐다.

검증 결과:

- base XLM-R vocab size: `250002`
- extended vocab size: `370433`
- appended new tokens: `120431`
- tokenizer wall time: `14:03.94`
- max RSS: `74739304 KB`
- Coptic/Syriac 및 target10 Latin 샘플에서 `<unk>` 없이 tokenize되는 것을 확인했다.

산출물:

- Auxiliary SPM:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.model`
- Auxiliary vocab:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.vocab`
- XLM-R 뒤에 새 piece를 append한 확장 SPM:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm.model`
- Hugging Face tokenizer directory:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm`

진행 확인 명령:

```bash
tail -f /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log
ps -o pid,ppid,sid,stat,etime,%cpu,%mem,rss,cmd --forest -g 2435024
find /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output -maxdepth 2 -type f -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' | sort
```

## 검증 명령

```bash
wc -l /home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt
grep -n '"status"\|"seen_languages"\|"unseen_languages"\|"planned_total_samples"\|"actual_total_samples"\|"missing_language_dirs"' \
  docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.report.json
awk -F '\t' 'NR>1 {status[$9]++; planned+=$5; actual+=$6} END {for (s in status) print s, status[s]; print "planned", planned; print "actual", actual}' \
  docs/exp/v4/0_tokenizer/merge/Glot500_v4_target10_xlmr100.manifest.tsv
```
