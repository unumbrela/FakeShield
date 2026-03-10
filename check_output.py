import json
import csv

# 检查 DTE-FDM 输出
with open('My_Forgery_Location_Task/DTE-FDM_output.jsonl', 'r', encoding='utf-8') as f:
    first = json.loads(f.readline())
    print("=== DTE-FDM 原始输出 ===")
    print(first['outputs'][:150])

# 检查 CSV 输出
with open('My_Forgery_Location_Task/submission.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    row = next(reader)
    print("\n=== CSV 中的 explanation ===")
    print(row[3][:150])
