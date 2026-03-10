import json

# 读取第一条记录
with open('My_Forgery_Location_Task/DTE-FDM_output.jsonl', 'r', encoding='utf-8') as f:
    line = f.readline()
    record = json.loads(line)

print("Image:", record['image'])
print("\nOutputs (前200字符):")
print(record['outputs'][:200])
print("\n是否包含中文:", any('\u4e00' <= c <= '\u9fff' for c in record['outputs']))
