import os, json
from dotenv import load_dotenv
from ChromaDB import ChromaDB

def create_product_document(product_id, product_info):
    # 讀取環境變數
    load_dotenv()

    # 連線
    db = ChromaDB()
    if not db.connect():
        print("Failed to connect to ChromaDB")
        exit(1)

    # 取得或建立 collection
    try:
        collection = db.get_collection("product_info")
    except Exception as e:
        print(f"Error creating or getting collection: {str(e)}")
        exit(1)
    if not collection:
        print("Collection 'product_info' does not exist, creating a new one.")
        collection = db.get_collection("product_info")

    # 載入 JSON
    with open("data/product_info.json", "r", encoding="utf-8") as f:
        entries = json.load(f)

    # 準備欄位
    ids = [str(e["id"]) for e in entries]
    documents = [json.dumps(e["document"], ensure_ascii=False) for e in entries]
    metadatas = [e["metadata"] for e in entries]

    # 執行插入
    collection.add(
        ids=ids,
        metadatas=metadatas,
        documents=documents
    )

    print(f"已成功插入 {len(ids)} 筆至 collection 'product_info'")

def get_product_document(product_id, product_info):
    # 讀取環境變數
    load_dotenv()

    # 連線
    db = ChromaDB()
    if not db.connect():
        print("Failed to connect to ChromaDB")
        exit(1)

    # 取得 collection
    try:
        collection = db.get_collection("product_info")
    except Exception as e:
        print(f"Error getting collection: {str(e)}")
        exit(1)

    metadata = {
        '$and': [
            {
                "product_id": {
                    '$eq' : product_id
                }
            },
            {
                "product_info": {
                    '$eq' : product_info
                }
            }
        ]
    }

    # 查詢文件
    results = collection.get(
        where=metadata
    )

    if results and len(results) > 0:
        return results
    else:
        return None

def retrieve_sample_data(limit=10):
    try:
        # Initialize and connect to ChromaDB
        db = ChromaDB()
        if not db.connect():
            print("Failed to connect to ChromaDB")
            return None

        # Get the user_info collection
        collection = db.get_collection(collection_name="product_info")

        # Retrieve up to 10 records
        results = collection.get(limit=limit)
        
        if not results['ids']:
            print("No data found in the collection")
            return None

        # Print the retrieved data
        print(f"Retrieved {len(results['ids'])} records:")
        for id_, doc, meta in zip(results['ids'], results['documents'], results['metadatas']):
            print(f"\nUser ID: {id_}")
            print("Document:")
            print(doc)
            print("Metadata:")
            print(meta)

        return results

    except Exception as e:
        print(f"Error retrieving data: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    product_id = "A"
    product_info = "main_features"
    
    # Create a product document
    # create_product_document(product_id, product_info)
    
    # Retrieve a product document
    # retrieved_document = get_product_document(product_id, product_info)
    
    # retrieved_document = retrieve_sample_data()

    if retrieved_document:
        print("Retrieved Document:", retrieved_document)
    else:
        print("No document found for the given product ID and information.")