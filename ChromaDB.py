from chromadb import HttpClient
from chromadb.config import Settings
import os
from dotenv import load_dotenv

class ChromaDB:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('CHROMADB_HOST', 'localhost')
        self.user = os.getenv('CHROMADB_USER')
        self.password = os.getenv('CHROMADB_PASSWORD')
        self.port = 7878
        self.client = None
        
    def connect(self):
        """Establish connection to ChromaDB"""
        try:
            self.client = HttpClient(
                settings=Settings(
                    chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
                    chroma_client_auth_credentials=f"{self.user}:{self.password}",
                ),
                host=self.host,
                port=self.port,
            )
            return self.client
        except Exception as e:
            print(f"Failed to connect to ChromaDB: {str(e)}")
            return False

    def get_collection(self, collection_name="user_info"):
        """Get or create a collection"""
        if not self.client:
            raise ConnectionError("Not connected to ChromaDB")
        return self.client.get_or_create_collection(collection_name)

    def delete_collection(self, collection_name="user_info"):
        """Delete a collection"""
        if not self.client:
            raise ConnectionError("Not connected to ChromaDB")
        try:
            self.client.delete_collection(collection_name)
            print(f"Collection '{collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete collection '{collection_name}': {str(e)}")
