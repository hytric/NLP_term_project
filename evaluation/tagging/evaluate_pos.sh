#!/bin/bash
# Copyright 2020 Google and DeepMind.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL=${1:-cis-lmu/glot500-base}
GPU=${2:-0}

export CUDA_VISIBLE_DEVICES=$GPU
PYTHON_BIN="${PYTHON_BIN:-python3}"
MODEL_TYPE="${MODEL_TYPE:-xlmr}"
NUM_EPOCHS="${NUM_EPOCHS:-10}"
LR="${LR:-2e-5}"
LC="${LC:-}"
BATCH_SIZE="${BATCH_SIZE:-8}"
EVAL_BATCH_SIZE="${EVAL_BATCH_SIZE:-32}"
GRAD_ACC="${GRAD_ACC:-4}"
MAX_LENGTH="${MAX_LENGTH:-256}"
SAVE_STEPS="${SAVE_STEPS:-500}"
SEED="${SEED:-1}"
TRAIN_LANGS="${TRAIN_LANGS:-eng_Latn}"


DATA_ROOT="${EVAL_DATA_ROOT:-${SCRIPT_DIR}/../download_data/download}"
DATA_DIR="${DATA_DIR:-${DATA_ROOT}/pos/}"
OUTPUT_DIR="${OUTPUT_DIR:-${EVAL_OUTPUT_DIR:-/PATH/TO/OUTPUT/}}"
LABELS="${LABELS:-${DATA_DIR%/}/labels.txt}"

cd "${SCRIPT_DIR}"

"${PYTHON_BIN}" evaluate_pos.py \
    --model_type $MODEL_TYPE \
    --model_name_or_path $MODEL \
    --data_dir $DATA_DIR \
    --labels $LABELS \
    --output_dir "${OUTPUT_DIR%/}/" \
    --max_seq_len $MAX_LENGTH \
    --num_train_epochs $NUM_EPOCHS \
    --gradient_accumulation_steps $GRAD_ACC \
    --per_gpu_train_batch_size $BATCH_SIZE \
    --per_gpu_eval_batch_size $EVAL_BATCH_SIZE \
    --save_steps $SAVE_STEPS \
    --seed $SEED \
    --learning_rate $LR \
    --do_train \
    --do_eval \
    --do_predict \
    --train_langs $TRAIN_LANGS \
    --eval_all_checkpoints \
    --eval_patience -1 \
    --overwrite_output_dir \
    --save_only_best_checkpoint $LC
