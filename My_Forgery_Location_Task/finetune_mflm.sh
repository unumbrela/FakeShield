#!/bin/bash
#
# Fine-tune MFLM on competition scene-text data
# Single A6000 48GB with DeepSpeed ZeRO-2
#
set -e

PROJ_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TASK_DIR="${PROJ_ROOT}/My_Forgery_Location_Task"

OUTPUT_DIR="${TASK_DIR}/mflm_finetuned"
DATA_PATH="${TASK_DIR}/mflm_data"
WEIGHT_PATH="${PROJ_ROOT}/weight/fakeshield-v1-22b/MFLM"
SAM_PATH="${PROJ_ROOT}/weight/sam_vit_h_4b8939.pth"

export PYTHONPATH="${PROJ_ROOT}/MFLM:${PYTHONPATH}"
export MASTER_PORT=$(shuf -i 2000-65000 -n 1)

mkdir -p "$OUTPUT_DIR"

echo "============================================"
echo "  Fine-tuning MFLM (LoRA)"
echo "  Data: ${DATA_PATH}"
echo "  Base model: ${WEIGHT_PATH}"
echo "  Output: ${OUTPUT_DIR}"
echo "============================================"

cd "${PROJ_ROOT}"

# Single A6000 48GB
# batch_size=4, grad_accum=4 -> effective batch=16
# lora_r=8, lora_alpha=16
# 720 train samples, 50 epochs with mask validation
deepspeed --include localhost:0 --master_port $MASTER_PORT \
    ./MFLM/train_ft.py \
    --version "$WEIGHT_PATH" \
    --dataset_dir "$DATA_PATH" \
    --vision_pretrained "$SAM_PATH" \
    --vision-tower openai/clip-vit-large-patch14-336 \
    --exp_name "$OUTPUT_DIR" \
    --lora_r 8 \
    --lora_alpha 16 \
    --lr 3e-4 \
    --batch_size 4 \
    --grad_accumulation_steps 4 \
    --pretrained \
    --use_segm_data \
    --tamper_segm_data "scene_text|train" \
    --val_tamper_dataset "scene_text|val" \
    --epochs 50 \
    --mask_validation \
    --steps_per_epoch 500

echo "============================================"
echo "  MFLM fine-tuning complete!"
echo "  Checkpoint saved to: ${OUTPUT_DIR}"
echo "============================================"
echo ""
echo "  Next: convert checkpoint for inference:"
echo "  python My_Forgery_Location_Task/convert_mflm_ckpt.py"
