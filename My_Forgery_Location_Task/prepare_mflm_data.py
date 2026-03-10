"""
Prepare MFLM fine-tuning data from competition training set.

MFLM expects:
  {dataset_dir}/{name}/{split}/image/*.jpg
  {dataset_dir}/{name}/{split}/mask/*.png
  {dataset_dir}/{name}/{split}/lisa_train_output.json  (for training)
  {dataset_dir}/{name}/{split}/lisa_val_output.json    (for validation)

lisa JSON format: list of {"image": "filename.jpg", "query": "...", "outputs": "..."}

We organize as:
  mflm_data/scene_text/train/image/*.jpg
  mflm_data/scene_text/train/mask/*.png
  mflm_data/scene_text/train/lisa_train_output.json
  mflm_data/scene_text/val/image/*.jpg
  mflm_data/scene_text/val/mask/*.png
  mflm_data/scene_text/val/lisa_val_output.json

Only Black (forged) images have masks, so only those are used.
We split 800 Black into 720 train + 80 val.
PNG images are converted to JPG (MFLM glob only matches *.jpg).
"""
import os
import json
import random
import shutil
from PIL import Image

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TASK_DIR, "dataset", "train")
OUTPUT_DIR = os.path.join(TASK_DIR, "mflm_data")

QUERY = "Is this image tampered? If yes, please describe the tampering."
TRAIN_RATIO = 0.9
RANDOM_SEED = 42


def main():
    random.seed(RANDOM_SEED)

    black_img_dir = os.path.join(DATASET_DIR, "Black", "Image")
    black_mask_dir = os.path.join(DATASET_DIR, "Black", "Mask")
    black_cap_dir = os.path.join(DATASET_DIR, "Black", "Caption")

    all_images = sorted(os.listdir(black_img_dir))
    random.shuffle(all_images)

    split_idx = int(len(all_images) * TRAIN_RATIO)
    train_images = all_images[:split_idx]
    val_images = all_images[split_idx:]

    print(f"Total Black images: {len(all_images)}")
    print(f"Train: {len(train_images)}, Val: {len(val_images)}")

    for split_name, split_images in [("train", train_images), ("val", val_images)]:
        img_out_dir = os.path.join(OUTPUT_DIR, "scene_text", split_name, "image")
        mask_out_dir = os.path.join(OUTPUT_DIR, "scene_text", split_name, "mask")
        os.makedirs(img_out_dir, exist_ok=True)
        os.makedirs(mask_out_dir, exist_ok=True)

        json_entries = []
        converted_png = 0

        for img_name in split_images:
            base_name = os.path.splitext(img_name)[0]

            # Target filename must be .jpg for MFLM glob
            target_img_name = base_name + ".jpg"
            src_img_path = os.path.join(black_img_dir, img_name)
            dst_img_path = os.path.join(img_out_dir, target_img_name)

            if img_name.lower().endswith('.png'):
                # Convert PNG to JPG
                img = Image.open(src_img_path).convert('RGB')
                img.save(dst_img_path, 'JPEG', quality=95)
                converted_png += 1
            else:
                shutil.copy2(src_img_path, dst_img_path)

            # Copy mask (always .png, keep as .png)
            src_mask_path = os.path.join(black_mask_dir, base_name + ".png")
            dst_mask_path = os.path.join(mask_out_dir, base_name + ".png")
            if os.path.exists(src_mask_path):
                shutil.copy2(src_mask_path, dst_mask_path)
            else:
                print(f"WARNING: no mask for {img_name}")

            # Read caption for explanation
            cap_path = os.path.join(black_cap_dir, base_name + ".md")
            if os.path.exists(cap_path):
                with open(cap_path, 'r', encoding='utf-8') as f:
                    caption = f.read().strip()
            else:
                caption = "该区域存在篡改痕迹。"

            json_entries.append({
                "image": target_img_name,
                "query": QUERY,
                "outputs": caption
            })

        # Write JSON
        if split_name == "train":
            json_path = os.path.join(OUTPUT_DIR, "scene_text", split_name, "lisa_train_output.json")
        else:
            json_path = os.path.join(OUTPUT_DIR, "scene_text", split_name, "lisa_val_output.json")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_entries, f, ensure_ascii=False, indent=2)

        print(f"[{split_name}] Images: {len(split_images)}, PNG->JPG converted: {converted_png}")
        print(f"[{split_name}] JSON saved: {json_path}")

    print(f"\nMFLM data prepared at: {OUTPUT_DIR}")
    print(f"Use: --dataset_dir {OUTPUT_DIR} --tamper_segm_data 'scene_text|train' --val_tamper_dataset 'scene_text|val'")


if __name__ == "__main__":
    main()
