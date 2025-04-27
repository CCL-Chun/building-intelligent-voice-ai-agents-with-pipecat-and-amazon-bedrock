import pandas as pd
import json
from datetime import datetime

# 讀取 CSV
df = pd.read_csv('data/user_rawdata.csv')

# 建立轉換函數：將「有/是」轉為 True，「無/否」轉為 False
def to_bool(val):
    if isinstance(val, str):
        if val in ["有", "是", "True", "true"]:
            return True
        if val in ["無", "否", "False", "false"]:
            return False
    return val

# 分組並轉換為指定格式（使用 標籤分類1 作為 catagory）
entries = []
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
grouped = df.groupby(['客代', '標籤分類1'])
id_counter = 1
for (cust, cat1), group in grouped:
    # 建立 document
    doc = {}
    for name, sub in group.groupby('標籤名稱'):
        values = sub['標籤值'].map(to_bool).tolist()
        # 若只有一個值，則不使用 list
        doc[name] = values if len(values) > 1 else values[0]
    entry = {
        "id": id_counter,
        "metadata": {
            "created_at": now,
            "updated_at": now,
            "catagory": cat1,
            "user_id": str(cust)
        },
        "document": doc
    }
    entries.append(entry)
    id_counter += 1

# 儲存為 JSON
output_path = 'data/chromadb_ready.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)


print(entries[5:15])
