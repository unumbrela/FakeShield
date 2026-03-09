import json
import os

dte_file = 'My_Forgery_Location_Task/DTE-FDM_output.jsonl'
mask_dir = 'My_Forgery_Location_Task/MFLM_output'

tampered = []
total = 0

with open(dte_file, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip():
            continue
        record = json.loads(line)
        total += 1
        outputs = record.get('outputs', '').lower()

        not_tampered_kw = ['has not been tampered', 'has not been artificially',
                          'not been tampered', 'no signs of tampering']

        is_tampered = True
        for kw in not_tampered_kw:
            if kw in outputs:
                is_tampered = False
                break

        if is_tampered:
            img_name = os.path.basename(record['image'])
            tampered.append(img_name)

mask_files = set(os.listdir(mask_dir)) if os.path.exists(mask_dir) else set()

print(f'Total: {total}')
print(f'Tampered: {len(tampered)}')
print(f'Mask files: {len(mask_files)}')
print(f'Missing masks: {len(tampered) - len([t for t in tampered if t in mask_files])}')
