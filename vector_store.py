import logging
from typing import List, Dict

import numpy as np

logger = logging.getLogger(__name__)


class VectorStore:
    """In-memory vector store using cosine similarity (NumPy).

    Drop-in replacement for the previous ChromaDB-backed store. ChromaDB pulls
    in opentelemetry/grpc/protobuf, which fails to import on some Python builds
    (notably the protobuf "Descriptors cannot be created directly" crash on
    Python 3.14). This keeps the same public API without those dependencies.

    State lives in memory for the life of the process. On Streamlit Cloud the
    filesystem is ephemeral and documents are re-ingested per session, so
    on-disk persistence added no value here anyway.
    """

    def __init__(self, db_path: str = "database/chroma_db"):
        self.db_path = db_path
        self.collection_name = "research_documents"
        self._ids: List[str] = []
        self._documents: List[str] = []
        self._metadatas: List[Dict] = []
        self._embeddings: List[np.ndarray] = []  # unit-normalized vectors
        logger.info("In-memory vector store initialized")

    @staticmethod
    def _normalize(vector: List[float]) -> np.ndarray:
        arr = np.asarray(vector, dtype=np.float32)
        norm = np.linalg.norm(arr)
        return arr if norm == 0 else arr / norm

    def add_documents(self, documents: List[str], embeddings: List[List[float]],
                      metadatas: List[Dict], ids: List[str]) -> None:
        """Add (or upsert) documents with embeddings."""
        try:
            for doc, emb, meta, doc_id in zip(documents, embeddings, metadatas, ids):
                norm_emb = self._normalize(emb)
                if doc_id in self._ids:
                    idx = self._ids.index(doc_id)
                    self._documents[idx] = doc
                    self._metadatas[idx] = meta
                    self._embeddings[idx] = norm_emb
                else:
                    self._ids.append(doc_id)
                    self._documents.append(doc)
                    self._metadatas.append(meta)
                    self._embeddings.append(norm_emb)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def similarity_search(self, query_embedding: List[float],
                          top_k: int = 3) -> List[Dict]:
        """Return the top_k most similar documents by cosine similarity."""
        try:
            if not self._embeddings:
                return []

            query = self._normalize(query_embedding)
            matrix = np.vstack(self._embeddings)        # (n, dim), normalized
            scores = matrix @ query                     # cosine similarity
            top_idx = np.argsort(scores)[::-1][:top_k]

            documents = [
                {
                    "content": self._documents[idx],
                    "metadata": self._metadatas[idx],
                    "similarity_score": float(scores[idx]),
                }
                for idx in top_idx
            ]
            logger.info(f"Found {len(documents)} similar documents")
            return documents
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise

    def get_all_documents(self) -> Dict:
        """Return every stored document (mirrors the old Chroma .get() shape)."""
        return {
            "ids": list(self._ids),
            "documents": list(self._documents),
            "metadatas": list(self._metadatas),
        }

    def delete_collection(self) -> None:
        """Clear all stored documents."""
        self._ids.clear()
        self._documents.clear()
        self._metadatas.clear()
        self._embeddings.clear()
        logger.info(f"Collection '{self.collection_name}' cleared")

    def count(self) -> int:
        return len(self._ids)

    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection."""
        return {
            "collection_name": self.collection_name,
            "total_documents": len(self._ids),
            "db_path": self.db_path,
        }
