"""
Step 2: Post-process DTE-FDM output + MFLM masks into competition CSV format.

CSV columns: image_name, label, location, explanation
- label: 0 (real) or 1 (forged)
- location: RLE-encoded binary mask (JSON string), empty string if real
- explanation: natural language explanation
"""
import os
import json
import csv
import cv2
import numpy as np
from pycocotools import mask as mask_utils

DTE_FDM_OUTPUT = os.path.join(os.path.dirname(__file__), "DTE-FDM_output.jsonl")
MFLM_MASK_DIR = os.path.join(os.path.dirname(__file__), "MFLM_output")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "submission.csv")
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "dataset", "test")


def mask_to_rle(mask_path, orig_h, orig_w):
    """Read a mask image file and convert to RLE string at original image size."""
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return ""
    # Resize mask to original image size if needed
    if mask.shape[0] != orig_h or mask.shape[1] != orig_w:
        mask = cv2.resize(mask, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)
    binary_mask = (mask > 127).astype(np.uint8)
    mask_fortran = np.asfortranarray(binary_mask)
    rle_dict = mask_utils.encode(mask_fortran)
    if isinstance(rle_dict['counts'], bytes):
        rle_dict['counts'] = rle_dict['counts'].decode('utf-8')
    return json.dumps(rle_dict)


def make_empty_rle(h, w):
    """Create an all-zero RLE mask for real images."""
    binary_mask = np.zeros((h, w), dtype=np.uint8)
    mask_fortran = np.asfortranarray(binary_mask)
    rle_dict = mask_utils.encode(mask_fortran)
    if isinstance(rle_dict['counts'], bytes):
        rle_dict['counts'] = rle_dict['counts'].decode('utf-8')
    return json.dumps(rle_dict)


def is_tampered(output_text):
    """Determine if DTE-FDM considers the image tampered."""
    not_tampered_keywords = [
        # 英文关键词
        "has not been tampered",
        "has not been artificially",
        "not been tampered",
        "no signs of tampering",
        "no evidence of tampering",
        "appears to be authentic",
        "is authentic",
        "taken directly from the camera",
        "no tampering",
        # 中文关键词
        "未被篡改",
        "没有被篡改",
        "未被伪造",
        "没有被伪造",
        "未发现篡改",
        "未发现伪造",
        "是真实的",
        "是原始的",
        "未经处理",
        "未经修改",
        "真实图像",
        "原始图像",
    ]
    text_lower = output_text.lower()
    for kw in not_tampered_keywords:
        if kw.lower() in text_lower:
            return False
    return True


def main():
    # Read DTE-FDM outputs
    dte_results = {}
    with open(DTE_FDM_OUTPUT, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            image_path = record["image"]
            image_name = os.path.basename(image_path)
            dte_results[image_name] = record["outputs"]

    # Get all test images (to ensure we have an entry for every image)
    all_test_images = sorted([
        f for f in os.listdir(TEST_IMAGE_DIR)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ])

    # Write CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image_name", "label", "location", "explanation"])

        for image_name in all_test_images:
            # Read original image size
            orig_img_path = os.path.join(TEST_IMAGE_DIR, image_name)
            orig_img = cv2.imread(orig_img_path)
            if orig_img is None:
                print(f"WARNING: cannot read {orig_img_path}, skipping")
                continue
            orig_h, orig_w = orig_img.shape[:2]

            # Get DTE-FDM output
            explanation = dte_results.get(image_name, "")
            tampered = is_tampered(explanation) if explanation else False

            if tampered:
                label = 1
                # Look for MFLM mask
                mask_path = os.path.join(MFLM_MASK_DIR, image_name)
                if os.path.exists(mask_path):
                    rle_str = mask_to_rle(mask_path, orig_h, orig_w)
                else:
                    # MFLM didn't generate a mask (model issue), use empty
                    print(f"WARNING: tampered but no mask for {image_name}")
                    rle_str = make_empty_rle(orig_h, orig_w)
            else:
                label = 0
                rle_str = make_empty_rle(orig_h, orig_w)
                if not explanation:
                    explanation = "该图像未发现篡改痕迹，判断为真实图像。"

            writer.writerow([image_name, label, rle_str, explanation])

    print(f"Submission CSV saved to: {OUTPUT_CSV}")
    print(f"Total images: {len(all_test_images)}")
    tampered_count = sum(1 for img in all_test_images if is_tampered(dte_results.get(img, "")))
    print(f"Predicted tampered: {tampered_count}, real: {len(all_test_images) - tampered_count}")


if __name__ == "__main__":
    main()
