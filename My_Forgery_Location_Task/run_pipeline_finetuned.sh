#!/bin/bash
#
# Full inference pipeline using FINE-TUNED models
# test images -> DTE-FDM (finetuned) -> MFLM (finetuned) -> submission CSV
#
set -e

PROJ_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TASK_DIR="${PROJ_ROOT}/My_Forgery_Location_Task"

# Use merged fine-tuned model paths
# If merged models don't exist, fall back to original weights
DTE_FDM_MERGED="${TASK_DIR}/dte_fdm_merged"
MFLM_MERGED="${TASK_DIR}/mflm_merged"
DTE_FDM_ORIG="${PROJ_ROOT}/weight/fakeshield-v1-22b/DTE-FDM"
MFLM_ORIG="${PROJ_ROOT}/weight/fakeshield-v1-22b/MFLM"

if [ -d "$DTE_FDM_MERGED" ]; then
    DTE_FDM_PATH="$DTE_FDM_MERGED"
    echo "Using fine-tuned DTE-FDM: $DTE_FDM_PATH"
else
    DTE_FDM_PATH="$DTE_FDM_ORIG"
    echo "WARNING: Fine-tuned DTE-FDM not found, using original: $DTE_FDM_PATH"
fi

if [ -d "$MFLM_MERGED" ]; then
    MFLM_PATH="$MFLM_MERGED"
    echo "Using fine-tuned MFLM: $MFLM_PATH"
else
    MFLM_PATH="$MFLM_ORIG"
    echo "WARNING: Fine-tuned MFLM not found, using original: $MFLM_PATH"
fi

DTG_PATH="${PROJ_ROOT}/weight/fakeshield-v1-22b/DTG.pth"
QUESTION_PATH="${TASK_DIR}/test_input.jsonl"
DTE_FDM_OUTPUT="${TASK_DIR}/DTE-FDM_output.jsonl"
MFLM_OUTPUT="${TASK_DIR}/MFLM_output"

export PYTHONPATH="${PROJ_ROOT}/DTE-FDM:${PROJ_ROOT}/MFLM:${PYTHONPATH}"

echo ""
echo "============================================"
echo "  Step 1: Generate test_input.jsonl"
echo "============================================"
cd "${PROJ_ROOT}"
python "${TASK_DIR}/step1_gen_jsonl.py"

echo ""
echo "============================================"
echo "  Step 2: Run DTE-FDM (Detection)"
echo "============================================"
PYTHONPATH="${PROJ_ROOT}/DTE-FDM:${PYTHONPATH}" \
CUDA_VISIBLE_DEVICES=0 \
python ./DTE-FDM/llava/eval/model_vqa.py \
    --model-path "${DTE_FDM_PATH}" \
    --DTG-path "${DTG_PATH}" \
    --question-file "${QUESTION_PATH}" \
    --image-folder / \
    --answers-file "${DTE_FDM_OUTPUT}"

echo ""
echo "============================================"
echo "  Step 3: Run MFLM (Localization)"
echo "============================================"
PYTHONPATH="${PROJ_ROOT}/MFLM:${PYTHONPATH}" \
CUDA_VISIBLE_DEVICES=0 \
python ./MFLM/test.py \
    --version "${MFLM_PATH}" \
    --DTE-FDM-output "${DTE_FDM_OUTPUT}" \
    --MFLM-output "${MFLM_OUTPUT}"

echo ""
echo "============================================"
echo "  Step 4: Post-process -> submission.csv"
echo "============================================"
python "${TASK_DIR}/step2_postprocess.py"

echo ""
echo "============================================"
echo "  Done! Submission file:"
echo "  ${TASK_DIR}/submission.csv"
echo "============================================"
