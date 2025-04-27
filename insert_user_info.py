import os, json
from dotenv import load_dotenv
from ChromaDB import ChromaDB

# 讀取環境變數
load_dotenv()

# 連線
db = ChromaDB()
if not db.connect():
    print("Failed to connect to ChromaDB")
    exit(1)

# 取得或建立 collection
try:
    collection = db.get_collection("user_info")
except Exception as e:
    print(f"Error creating or getting collection: {str(e)}")
    exit(1)
if not collection:
    print("Collection 'user_info' does not exist, creating a new one.")
    collection = db.get_collection("user_info")

# 載入 JSON
with open("data/chromadb_ready.json", "r", encoding="utf-8") as f:
    entries = json.load(f)

# 準備欄位
ids = [str(e["id"]) for e in entries]
documents = [json.dumps(e["document"], ensure_ascii=False) for e in entries]
metadatas = [e["metadata"] for e in entries]

# 執行插入
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print(f"已成功插入 {len(ids)} 筆至 collection 'user_info'")
