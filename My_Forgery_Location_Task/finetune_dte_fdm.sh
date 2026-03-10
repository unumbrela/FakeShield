#!/bin/bash
#
# Fine-tune DTE-FDM on competition scene-text data
# Single A6000 48GB with ZeRO-3
#
set -e

PROJ_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TASK_DIR="${PROJ_ROOT}/My_Forgery_Location_Task"

OUTPUT_DIR="${TASK_DIR}/dte_fdm_finetuned"
DATA_PATH="${TASK_DIR}/dte_fdm_train.json"
WEIGHT_PATH="${PROJ_ROOT}/weight/fakeshield-v1-22b/DTE-FDM"

export PYTHONPATH="${PROJ_ROOT}/DTE-FDM:${PYTHONPATH}"

mkdir -p "$OUTPUT_DIR"

echo "============================================"
echo "  Fine-tuning DTE-FDM (LoRA)"
echo "  Data: ${DATA_PATH}"
echo "  Base model: ${WEIGHT_PATH}"
echo "  Output: ${OUTPUT_DIR}"
echo "============================================"

cd "${PROJ_ROOT}"

# Single A6000 48GB, ZeRO-3 (no CPU offload)
# LoRA r=128, alpha=256 (full capacity)
# per_device_batch=4, grad_accum=2 -> effective batch=8
# 3 epochs over 1000 samples
deepspeed --include localhost:0 --master_port=29501 \
    ./DTE-FDM/llava/train/train_mem.py \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --deepspeed ./scripts/DTE-FDM/zero3.json \
    --model_name_or_path "$WEIGHT_PATH" \
    --version v1 \
    --data_path "$DATA_PATH" \
    --image_folder / \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir "$OUTPUT_DIR" \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --eval_strategy "no" \
    --save_strategy "epoch" \
    --save_total_limit 2 \
    --learning_rate 2e-4 \
    --weight_decay 0. \
    --warmup_steps 10 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 4096 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to none

echo "============================================"
echo "  DTE-FDM fine-tuning complete!"
echo "  LoRA weights saved to: ${OUTPUT_DIR}"
echo "============================================"
