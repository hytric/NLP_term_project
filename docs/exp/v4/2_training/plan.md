# v4 Training Plan

목표는 원본 Glot500 흐름을 v4 target10 low-resource 설정에 맞춰 순차적으로
수행하고, 최종 result score를 남기는 것이다.

## 원본 Glot500 기준

확인한 primary source:

- GitHub: `https://github.com/cisnlp/Glot500`
- ACL paper: `https://aclanthology.org/2023.acl-long.61/`
- arXiv: `https://arxiv.org/abs/2305.12182`

원본 흐름:

1. `Glot500-c`로 SentencePiece unigram auxiliary tokenizer `250K` 학습
2. auxiliary tokenizer token 중 XLM-R vocab에 없는 token만 XLM-R vocab 뒤에 merge
3. embedding matrix resize
4. XLM-R-base를 MLM objective로 continued pretraining
5. PPPL, sentence retrieval, Bible retrieval/alignment, NER, POS, text classification 평가

논문 기준 핵심 설정:

- `Glot500-c`: 511 languages, 534 language-scripts
- inclusion threshold: language-script당 30,000 sentence 이상
- tokenizer: SentencePiece unigram, auxiliary vocab `250K`
- language sampling: alpha `0.3`
- final vocab: XLM-R `250K` + new `151K` = `401K`
- continued pretraining:
  - base model: `xlm-roberta-base`
  - objective: MLM
  - optimizer: Adam beta `(0.9, 0.999)`
  - learning rate: `5e-5`
  - batch: `384`
  - checkpoint: every `10K` steps
  - chunk length: `512`
  - hardware: 8x RTX A6000
  - time: about 2 weeks
- evaluation:
  - pseudoperplexity
  - roundtrip alignment with SimAlign on Bible
  - sentence retrieval on Tatoeba/Bible
  - NER
  - POS
  - text classification

## v4 현재 데이터

최종 corpus:

- `/home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt`
- lines: `13,844,487`
- size: about `2.9G`

구성:

- XLM-R seen Glot500 languages: `92`
- target10 low-resource Bible-derived languages: `10`
- total languages: `102`

8개 XLM-R seen row는 local/public data가 없어 제외했다.

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

데이터 처리 상세 문서:

- `docs/exp/v4/0_tokenizer/dataset_processing.md`

## 현재 진행 상태

### 1. Tokenizer 생성

상태: 완료

완료된 실행:

```text
time wrapper PID: 2435024
python child PID: 2435028
log file: /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log
```

실행 명령:

```bash
setsid bash -lc 'cd /home/axt/jongha/Glot500-py39-eval && exec /usr/bin/time -v python3 tokenization/run.py --input_fname /home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt --model_name xlm-roberta-base --save_directory /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/ --vocab_size 250000' \
  > /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log 2>&1 &
```

중요한 해석:

- 입력은 target10-only가 아니라 `92 seen + 10 target10` mixed corpus이다.
- auxiliary SentencePiece vocab은 mixed corpus 전체에서 학습된다.
- merge 시 XLM-R 기존 vocab에 없는 piece만 기존 XLM-R SPM 뒤에 append된다.
- 즉 append 방식은 맞지만, low-resource-only piece만 추가하는 방식은 아니다.

예상 산출물:

- `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.model`
- `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500.vocab`
- `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm.model`
- `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm`

완료 결과:

- base XLM-R vocab size: `250002`
- extended vocab size: `370433`
- appended new tokens: `120431`
- tokenizer wall time: `14:03.94`
- max RSS: `74739304 KB`
- exit status: `0`
- Coptic/Syriac 및 target10 Latin 샘플에서 `<unk>` 없이 tokenize되는 것을 확인했다.

진행 확인:

```bash
tail -f /home/axt/mnt2/jongha/v4_tokenizer/tokenization/logs/tokenizer_train_20260620_004351_setsid.log
ps -o pid,ppid,sid,stat,etime,%cpu,%mem,rss,cmd --forest -g 2435024
find /home/axt/mnt2/jongha/v4_tokenizer/tokenization/output -maxdepth 2 -type f -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' | sort
```

### 2. Continued MLM Pretraining

상태: 진행 중

tokenizer 완료 후 학습을 시작했다.

필수 입력:

- train file:
  `/home/axt/mnt2/jongha/v4_tokenizer/data/Glot500_v4_target10_xlmr100.txt`
- tokenizer:
  `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm`

v4 학습 launcher:

- `modeling/train_v4_target10_xlmr100.sh`
- `modeling/start_v4_training_when_tokenizer_ready.sh`

자동 시작 watcher:

```text
watcher PID: 2442824
pid file: /home/axt/mnt2/jongha/v4_tokenizer/runs/wait_tokenizer_then_train.pid
log file: /home/axt/mnt2/jongha/v4_tokenizer/runs/logs/wait_tokenizer_then_train_20260620_005228.log
```

watcher는 tokenizer 완료 후 다음 polling까지 대기 중이라 중복 실행을 피하기 위해
종료했고, 수동으로 검증 후 training을 즉시 시작했다.

watcher는 아래 순서로 동작한다.

1. `/home/axt/mnt2/jongha/v4_tokenizer/tokenization/output/Glot500_extended_spm`
   과 `Glot500_extended_spm.model`이 생길 때까지 기다린다.
2. tokenizer process가 종료됐는데 tokenizer 산출물이 없으면 tokenizer log tail을
   남기고 실패한다.
3. Hugging Face tokenizer가 정상 로드되고 vocab size가 XLM-R 기본 vocab보다 큰지
   검증한다.
4. 검증이 통과하면 `modeling/train_v4_target10_xlmr100.sh`로 MLM continued
   pretraining을 시작한다.

기본 GPU 설정:

- `CUDA_VISIBLE_DEVICES=1,2`
- 현재 확인 기준 GPU 0/3은 거의 사용 중이고, GPU 1/2가 비교적 여유 있다.
- caller가 `CUDA_VISIBLE_DEVICES`와 `NPROC_PER_NODE`를 지정하면 override 가능하다.

기본 학습 설정:

- model: `xlm-roberta-base`
- tokenizer: v4 extended tokenizer
- tokenizer loader: `--use_fast_tokenizer False`
- objective: MLM
- learning rate: `5e-5`
- Adam beta: `(0.9, 0.999)`
- per-device batch: `12`
- gradient accumulation: `16`
- nproc: `2`
- effective batch: `12 * 16 * 2 = 384`
- max sequence length: `512`
- checkpoint: every `10K` steps
- epochs: `100`
- fp16: enabled

실행 명령:

```bash
bash modeling/train_v4_target10_xlmr100.sh
```

현재는 watcher를 통해 아래 명령이 detached로 실행되어 있다.

```bash
setsid bash -lc 'cd /home/axt/jongha/Glot500-py39-eval && export CUDA_VISIBLE_DEVICES=1,2 NPROC_PER_NODE=2 SLEEP_SECONDS=300 WANDB_DISABLED=true && exec modeling/start_v4_training_when_tokenizer_ready.sh' \
  > /home/axt/mnt2/jongha/v4_tokenizer/runs/logs/wait_tokenizer_then_train_20260620_005228.log 2>&1 &
```

만약 사용 가능한 GPU가 달라지면:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 NPROC_PER_NODE=4 bash modeling/train_v4_target10_xlmr100.sh
```

학습 산출물:

- `/home/axt/mnt2/jongha/v4_tokenizer/runs/Glot500_v4_target10_xlmr100_xlmr_base_mlm`
- `/home/axt/mnt2/jongha/v4_tokenizer/runs/logs`

현재 실행:

```text
train PID: 2451851
pid file: /home/axt/mnt2/jongha/v4_tokenizer/runs/train_v4_target10_xlmr100.pid
launcher log: /home/axt/mnt2/jongha/v4_tokenizer/runs/logs/train_v4_target10_xlmr100_launcher_20260620_010118.log
train log: /home/axt/mnt2/jongha/v4_tokenizer/runs/logs/train_v4_target10_xlmr100_20260620_010118.log
```

train loop 진입 확인:

```text
start: 2026-06-20 01:06:27
Num examples: 1054082
Instantaneous batch size per device: 12
Total train batch size: 384
Total optimization steps: 274500
CUDA_VISIBLE_DEVICES: 1,2
```

현재 GPU 1/2에 두 distributed rank가 올라가 있으며, 각 rank가 약 `44.4GB`를
사용한다. 다음 큰 확인 지점은 `save_steps=10000`에 생성될 첫 checkpoint이다.

첫 실행은 `/usr/bin/python3` 환경의 `accelerate`가 오래된
`huggingface_hub==0.11.1`에서 `split_torch_state_dict_into_shards`를 import하지
못해 실패했다. `huggingface_hub==0.24.7`로 올린 뒤 `Trainer` import smoke test를
통과했고, 같은 설정으로 재시작했다.

embedding resize:

- `modeling/run.py`에서 `len(tokenizer) > embedding_size`이면
  `model.resize_token_embeddings(len(tokenizer))`를 호출한다.
- 기존 XLM-R token embedding은 유지된다.
- 새 token row는 Hugging Face 기본 방식으로 초기화된다.

### 3. Evaluation

상태: 학습 완료 후 실행

평가 코드는 아래 디렉터리에 있다.

- `evaluation/retrieval`
- `evaluation/round-trip`
- `evaluation/tagging`
- `evaluation/text_classification`

평가 환경 문서:

- `evaluation/INSTALL_Glot500_Eval_py39.txt`

v4 준비:

- `modeling/run_v4_pseudoperplexity.py`
  - v4 checkpoint 경로를 받아 target10 dev PPPL을 산출한다.
- `evaluation/download_data/download_data.sh`
  - helper script/data directory 경로를 `evaluation/download_data` 기준으로 수정했다.
- `evaluation/retrieval/evaluate_retrieval_tatoeba.py`
- `evaluation/retrieval/evaluate_retrieval_bible.py`
  - absolute model path를 넘겨도 cache/output 경로가 깨지지 않게 수정했다.
- `evaluation/retrieval/evaluate_retrieval_tatoeba.sh`
- `evaluation/retrieval/evaluate_retrieval_bible.sh`
- `evaluation/tagging/evaluate_ner.sh`
- `evaluation/tagging/evaluate_pos.sh`
  - v4 evaluation output directory를 기본값으로 사용하도록 수정했다.

실행할 score:

- PPPL
- Sentence Retrieval Tatoeba
- Sentence Retrieval Bible
- Roundtrip Alignment with SimAlign on Bible
- NER
- POS
- Text Classification

## TODO Checklist

- [x] v4 mixed corpus 생성
- [x] 원본 GitHub/paper 기준 flow 재확인
- [x] tokenizer 생성 시작
- [x] v4 MLM training launcher 작성
- [x] tokenizer 완료 후 MLM 자동 시작 watcher 작성/실행
- [x] tokenizer 생성 완료 확인
- [x] tokenizer vocab size/new token count 기록
- [x] MLM continued pretraining 시작
- [ ] 학습 checkpoint/log 기록
- [x] evaluation wrapper/PPPL runner 준비
- [ ] evaluation data 다운로드/확인
- [ ] PPPL score 산출
- [ ] retrieval score 산출
- [ ] Bible retrieval/alignment score 산출
- [ ] NER/POS score 산출
- [ ] text classification score 산출
- [ ] 최종 결과표 작성
