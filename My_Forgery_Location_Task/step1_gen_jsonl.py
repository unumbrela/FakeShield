"""
Step 1: Generate test.jsonl for DTE-FDM input from competition test images.
"""
import os
import json

TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "dataset", "test")
OUTPUT_JSONL = os.path.join(os.path.dirname(__file__), "test_input.jsonl")

PROMPT = (
    "Was this photo taken directly from the camera without any processing? "
    "Has it been tampered with by any artificial photo modification techniques such as ps? "
    "Please zoom in on any details in the image, paying special attention to the edges of the objects, "
    "capturing some unnatural edges and perspective relationships, some incorrect semantics, "
    "unnatural lighting and darkness etc."
)

def main():
    images = sorted([
        f for f in os.listdir(TEST_IMAGE_DIR)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ])
    print(f"Found {len(images)} test images in {TEST_IMAGE_DIR}")

    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
        for img_name in images:
            img_path = os.path.abspath(os.path.join(TEST_IMAGE_DIR, img_name))
            record = {"image": img_path, "text": PROMPT}
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Generated {OUTPUT_JSONL} with {len(images)} entries")

if __name__ == "__main__":
    main()
