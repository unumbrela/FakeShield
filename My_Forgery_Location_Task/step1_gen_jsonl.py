"""
Step 1: Generate test.jsonl for DTE-FDM input from competition test images.
"""
import os
import json

TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "dataset", "test")
OUTPUT_JSONL = os.path.join(os.path.dirname(__file__), "test_input.jsonl")

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
