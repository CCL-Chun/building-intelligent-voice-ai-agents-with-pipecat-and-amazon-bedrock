from ChromaDB import ChromaDB

def retrieve_sample_data(limit=10):
    try:
        # Initialize and connect to ChromaDB
        db = ChromaDB()
        if not db.connect():
            print("Failed to connect to ChromaDB")
            return None

        # Get the user_info collection
        collection = db.get_collection(collection_name="user_info")

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
    retrieve_sample_data()