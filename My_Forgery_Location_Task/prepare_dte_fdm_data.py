"""
Prepare DTE-FDM fine-tuning data from competition training set.

Expected output format (JSON list):
[
  {
    "image": "/abs/path/to/image.jpg",
    "conversations": [
      {"from": "human", "value": "<image>\nPrompt text"},
      {"from": "gpt", "value": "Caption/explanation text"}
    ]
  },
  ...
]

Uses:
- Black (forged, 800): image + caption as ground truth explanation
- White (real, 200): image + caption as ground truth explanation
"""
import os
import json

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TASK_DIR, "dataset", "train")
OUTPUT_PATH = os.path.join(TASK_DIR, "dte_fdm_train.json")

PROMPT = """请仔细分析这张场景文本图像（如票据、合同、公告、证件等），判断其是否被伪造或篡改。请用中文详细回答以下问题：

1. 这张图像是否被篡改？如果被篡改，请描述篡改的具体区域位置。

2. 判断依据：请从以下多个维度进行细致分析：
   - 文字内容：检查数字、日期、金额、姓名等关键文字是否存在替换、修改的痕迹
   - 字体一致性：同类文字的字体、字号、粗细、间距是否一致
   - 文字边缘：放大观察文字边缘是否清晰自然，有无模糊、锯齿、过度锐化等异常
   - 文字与背景融合：文字与纸张背景的融合是否自然，有无明显的拼接痕迹
   - 排版对齐：文字排列、行距、对齐方式是否符合原始文档规范
   - 印章签名：如有印章或签名，检查其清晰度、颜色、压痕是否真实
   - 纸张纹理：背景纹理、折痕、污渍等是否连续一致
   - 光照阴影：整体光照方向是否统一，阴影是否合理
   - 分辨率：不同区域的清晰度、分辨率是否一致
   - 物理规律：透视关系、比例尺度是否符合常识

请给出详细、具体、有逻辑的分析，避免模糊笼统的描述。"""


def main():
    data_list = []

    # Process Black (forged) images
    black_img_dir = os.path.join(DATASET_DIR, "Black", "Image")
    black_cap_dir = os.path.join(DATASET_DIR, "Black", "Caption")
    black_images = sorted(os.listdir(black_img_dir))

    for img_name in black_images:
        img_path = os.path.abspath(os.path.join(black_img_dir, img_name))
        base_name = os.path.splitext(img_name)[0]
        cap_path = os.path.join(black_cap_dir, base_name + ".md")

        if not os.path.exists(cap_path):
            print(f"WARNING: no caption for {img_name}, skipping")
            continue

        with open(cap_path, 'r', encoding='utf-8') as f:
            caption = f.read().strip()

        record = {
            "image": img_path,
            "conversations": [
                {"from": "human", "value": f"<image>\n{PROMPT}"},
                {"from": "gpt", "value": caption}
            ]
        }
        data_list.append(record)

    # Process White (real) images
    white_img_dir = os.path.join(DATASET_DIR, "White", "Image")
    white_cap_dir = os.path.join(DATASET_DIR, "White", "Caption")
    white_images = sorted(os.listdir(white_img_dir))

    for img_name in white_images:
        img_path = os.path.abspath(os.path.join(white_img_dir, img_name))
        base_name = os.path.splitext(img_name)[0]
        cap_path = os.path.join(white_cap_dir, base_name + ".md")

        if not os.path.exists(cap_path):
            print(f"WARNING: no caption for {img_name}, skipping")
            continue

        with open(cap_path, 'r', encoding='utf-8') as f:
            caption = f.read().strip()

        record = {
            "image": img_path,
            "conversations": [
                {"from": "human", "value": f"<image>\n{PROMPT}"},
                {"from": "gpt", "value": caption}
            ]
        }
        data_list.append(record)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"DTE-FDM training data saved to: {OUTPUT_PATH}")
    print(f"Total samples: {len(data_list)} (Black: {len(black_images)}, White: {len(white_images)})")


if __name__ == "__main__":
    main()
