"""Bulk-load documents from a local folder into the knowledge base.

Usage:  python load_sample_documents.py [data_dir]   (default: ./data)

Ingestion needs no API key — embeddings run locally. Provider keys are only
used to generate answers in the app.
"""

import logging
import os
import sys

from embeddings import EmbeddingGenerator
from preprocessing import TextPreprocessor
from rag_pipeline import RAGPipeline
from utils import configure_logging, load_environment_variables
from vector_store import VectorStore

configure_logging()
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = (".txt", ".pdf")


def _read_document(file_path: str) -> str:
    """Read text from a .txt or .pdf file."""
    if file_path.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_sample_documents(rag_pipeline: RAGPipeline, data_dir: str = "data") -> dict:
    """Ingest every supported document found under `data_dir`."""
    logger.info(f"Loading documents from {data_dir}")
    found = loaded = 0

    for root, _dirs, files in os.walk(data_dir):
        for file in files:
            if not file.lower().endswith(SUPPORTED_EXTENSIONS):
                continue
            found += 1
            file_path = os.path.join(root, file)
            try:
                content = _read_document(file_path)
                if not content.strip():
                    logger.warning(f"No text extracted from {file}; skipping.")
                    continue
                result = rag_pipeline.ingest_document(content, file)
                loaded += 1
                logger.info(f"Loaded {file} — {result['chunks_created']} chunks")
            except Exception as e:
                logger.error(f"Error loading {file}: {e}")

    logger.info(f"Done. Found: {found}, Loaded: {loaded}")
    return {
        "total_found": found,
        "total_loaded": loaded,
        "status": "success" if loaded > 0 else "no_documents_found",
    }


def main() -> None:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    config = load_environment_variables()

    rag_pipeline = RAGPipeline(
        EmbeddingGenerator(model_name=config["embedding_model"]),
        VectorStore(db_path=config["chroma_db_path"]),
        preprocessor=TextPreprocessor(
            chunk_size=config["chunk_size"],
            chunk_overlap=config["chunk_overlap"],
        ),
        top_k=config["top_k_documents"],
    )

    load_sample_documents(rag_pipeline, data_dir)
    logger.info(f"Database stats: {rag_pipeline.get_database_stats()}")


if __name__ == "__main__":
    main()
