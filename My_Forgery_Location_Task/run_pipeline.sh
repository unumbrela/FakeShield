#!/bin/bash
#
# Full pipeline: test images -> DTE-FDM -> MFLM -> submission CSV
#
# Usage: bash My_Forgery_Location_Task/run_pipeline.sh
#
# Prerequisites:
#   - DTE-FDM environment (Docker: zhipeixu/dte-fdm:v1.0) or pip installed
#   - MFLM environment (Docker: zhipeixu/mflm:v1.0) or pip installed
#   - Model weights in ./weight/fakeshield-v1-22b/
#   - SAM weights in ./weight/sam_vit_h_4b8939.pth
#

set -e

PROJ_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TASK_DIR="${PROJ_ROOT}/My_Forgery_Location_Task"

WEIGHT_PATH="${PROJ_ROOT}/weight/fakeshield-v1-22b"
QUESTION_PATH="${TASK_DIR}/test_input.jsonl"
DTE_FDM_OUTPUT="${TASK_DIR}/DTE-FDM_output.jsonl"
MFLM_OUTPUT="${TASK_DIR}/MFLM_output"

echo "============================================"
echo "  Step 1: Generate test_input.jsonl"
echo "============================================"
cd "${PROJ_ROOT}"
python "${TASK_DIR}/step1_gen_jsonl.py"

echo ""
echo "============================================"
echo "  Step 2: Run DTE-FDM (Detection)"
echo "============================================"
CUDA_VISIBLE_DEVICES=0 \
python ./DTE-FDM/llava/eval/model_vqa.py \
    --model-path "${WEIGHT_PATH}/DTE-FDM" \
    --DTG-path "${WEIGHT_PATH}/DTG.pth" \
    --question-file "${QUESTION_PATH}" \
    --image-folder / \
    --answers-file "${DTE_FDM_OUTPUT}"

echo ""
echo "============================================"
echo "  Step 3: Run MFLM (Localization)"
echo "============================================"
CUDA_VISIBLE_DEVICES=0 \
python ./MFLM/test.py \
    --version "${WEIGHT_PATH}/MFLM" \
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
