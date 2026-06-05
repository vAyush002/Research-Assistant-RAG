import logging
import chromadb
from typing import List, Dict, Tuple

import os

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages ChromaDB vector database operations"""
    
    def __init__(self, db_path: str = "database/chroma_db"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)

        # New Chroma client
        self.client = chromadb.PersistentClient(
            path=db_path
        )

        logger.info(f"ChromaDB initialized with path: {db_path}")

        self.collection_name = "research_documents"

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        logger.info(
            f"Collection '{self.collection_name}' created/retrieved"
        )
        
    def add_documents(self, documents: List[str], embeddings: List[List[float]], 
                     metadatas: List[Dict], ids: List[str]) -> None:
        """Add documents with embeddings to the vector store"""
        try:
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def similarity_search(self, query_embedding: List[float], 
                         top_k: int = 3) -> List[Dict]:
        """Search for similar documents using embedding"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            documents = []
            if results and results['documents'] and len(results['documents']) > 0:
                for doc, metadata, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    documents.append({
                        "content": doc,
                        "metadata": metadata,
                        "similarity_score": 1 - distance  # Convert distance to similarity
                    })
            
            logger.info(f"Found {len(documents)} similar documents")
            return documents
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise
    
    def get_all_documents(self) -> Dict:
        """Get all documents from the collection"""
        try:
            all_docs = self.collection.get()
            logger.info(f"Retrieved {len(all_docs['ids'])} documents from store")
            return all_docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
    
    def delete_collection(self) -> None:
        """Delete the entire collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Collection '{self.collection_name}' deleted")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_documents": count,
                "db_path": self.db_path
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            raise
