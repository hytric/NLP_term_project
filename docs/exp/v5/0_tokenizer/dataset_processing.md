# v5 Tokenizer Dataset Processing

이 문서는 v5 `Glot500_v5_glot50010_xlmr100` tokenizer corpus 준비 상태를
정리한다. 이 프로젝트는 실험 기록이 촘촘해서, v5도 같은 방식으로 남겨두면
학생들이 다음 단계에서 훨씬 덜 흔들린다.

## 선정 기준

target/unseen `10`개는 `miscellaneous/languages_stats.csv`와
`/disk3/moon/Glot500/data/raw`를 함께 확인해서 고른다.

조건:

- `XLM-R` 컬럼이 `True`가 아니다.
- `new_length >= 30000`이다.
- `/disk3/moon/Glot500/data/raw/{language_script}` 디렉터리가 실제로 있다.
- 후보 pool을 만든 뒤, 지역/문자/어족이 퍼지도록 `10`개를 수동 큐레이션한다.
- 선택한 `10`개는 다시 스크립트에서 조건을 검증한다. 즉 raw directory가 없거나
  `new_length < 30000`이면 실패한다.

준비 스크립트:

```bash
python3 preprocessing/prepare_v5_glot50010_merge_inputs.py --prune_raw_links
```

## 선택된 Glot500 내부 target10

| rank | language_script | name | region | script | new_length | source |
| ---: | --- | --- | --- | --- | ---: | --- |
| 1 | `fur_Latn` | Friulian | Europe | Latin | 30,052 | `/disk3/moon/Glot500/data/raw/fur_Latn` |
| 2 | `krc_Cyrl` | Karachay-Balkar | North Caucasus | Cyrillic | 30,353 | `/disk3/moon/Glot500/data/raw/krc_Cyrl` |
| 3 | `acm_Arab` | Mesopotamian Arabic | West Asia | Arabic | 44,505 | `/disk3/moon/Glot500/data/raw/acm_Arab` |
| 4 | `dzo_Tibt` | Dzongkha | Himalaya | Tibetan | 52,732 | `/disk3/moon/Glot500/data/raw/dzo_Tibt` |
| 5 | `sat_Olck` | Santali | South Asia | Ol Chiki | 39,614 | `/disk3/moon/Glot500/data/raw/sat_Olck` |
| 6 | `mad_Latn` | Madurese | Southeast Asia | Latin | 38,993 | `/disk3/moon/Glot500/data/raw/mad_Latn` |
| 7 | `bam_Latn` | Bambara | West Africa | Latin | 32,150 | `/disk3/moon/Glot500/data/raw/bam_Latn` |
| 8 | `kjb_Latn` | Q'anjob'al | Mesoamerica | Latin | 31,471 | `/disk3/moon/Glot500/data/raw/kjb_Latn` |
| 9 | `quw_Latn` | Tena Lowland Quichua | Andean South America | Latin | 33,449 | `/disk3/moon/Glot500/data/raw/quw_Latn` |
| 10 | `rap_Latn` | Rapanui | Polynesia | Latin | 30,102 | `/disk3/moon/Glot500/data/raw/rap_Latn` |

총 target source rows:

```text
363,421
```

전체 후보 pool은 `318`개였고, 다음 파일에 저장했다.

```text
docs/exp/v5/0_tokenizer/miscellaneous/glot500_candidate_pool_min30k.tsv
```

## Raw Dataset Layout

v5 raw root:

```text
/home/axt/mnt2/jongha/v5_glot50010/raw
```

v5에서는 seen `92`개와 target `10`개가 모두 Glot500 raw directory로 향하는
symlink이다.

```text
/home/axt/mnt2/jongha/v5_glot50010/raw/{language_script}
-> /disk3/moon/Glot500/data/raw/{language_script}
```

v4와 달리 target10을 새 HF DatasetDict로 materialize하지 않는다. 즉 v5 target
10개도 Glot500 내부 raw dataset을 그대로 읽는다. `--prune_raw_links` 실행 후
v5 raw root의 symlink 수는 `102`개이다.

## Stats CSV

생성된 stats CSV:

```text
docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv
```

구성:

- `1`-`92`: v4와 같은 XLM-R seen Glot500 언어
- `93`-`102`: v5 Glot500-internal target10
- 총 `102` language-script rows

마지막 10개 row:

```text
93,30052,47966,fur,['Latn'],
94,30353,40368,krc,['Cyrl'],
95,44505,82814,acm,['Arab'],
96,52732,61333,dzo,['Tibt'],
97,39614,65890,sat,['Olck'],
98,38993,40771,mad,['Latn'],
99,32150,36761,bam,['Latn'],
100,31471,32657,kjb,['Latn'],
101,33449,44927,quw,['Latn'],
102,30102,32930,rap,['Latn'],
```

## Merge Dry-Run

실제 corpus 파일을 쓰지 않고 manifest/report만 먼저 만들었다.

```bash
python3 preprocessing/merge_files.py \
  --data_directory /home/axt/mnt2/jongha/v5_glot50010/raw \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/data \
  --experiment_name Glot500_v5_glot50010_xlmr100 \
  --stats_csv docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv \
  --manifest_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv \
  --report_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json \
  --missing_policy fail \
  --dry_run
```

Dry-run 결과:

- status: `DRY_RUN`
- seen languages: `92`
- unseen/target languages: `10`
- source seen sentences: `1,025,635,434`
- source target sentences: `363,421`
- planned seen samples: `82,943,520`
- planned target samples: `9,508,731`
- planned total samples: `92,452,251`
- missing language dirs: `0`

산출물:

```text
docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv
docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json
```

## 실제 Merge 명령

큰 corpus 생성을 시작하려면 위 dry-run 명령에서 `--dry_run`만 제거한다.

```bash
python3 preprocessing/merge_files.py \
  --data_directory /home/axt/mnt2/jongha/v5_glot50010/raw \
  --save_directory /home/axt/mnt2/jongha/v5_glot50010/data \
  --experiment_name Glot500_v5_glot50010_xlmr100 \
  --stats_csv docs/exp/v5/0_tokenizer/miscellaneous/languages_stats_glot50010_xlmr100.csv \
  --manifest_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.manifest.tsv \
  --report_path docs/exp/v5/0_tokenizer/merge/Glot500_v5_glot50010_xlmr100.report.json \
  --missing_policy fail
```

주의: 기본 설정 그대로면 약 `92.5M` lines를 쓰게 된다. 먼저 pilot이 필요하면
`--max_samples_per_language`를 사용해서 작은 corpus로 tokenizer smoke test를
돌리는 편이 좋다.
