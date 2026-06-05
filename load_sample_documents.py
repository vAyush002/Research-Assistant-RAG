import os
import logging
from pathlib import Path
from rag_pipeline import RAGPipeline
from utils import load_environment_variables, configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

def load_sample_documents(rag_pipeline, data_dir: str = "data"):
    """Load sample documents from data directory"""
    
    logger.info(f"Starting to load sample documents from {data_dir}")
    
    # Supported file extensions
    supported_extensions = ['.txt', '.pdf']
    
    # Find all documents
    documents_found = 0
    documents_loaded = 0
    
    # Walk through data directory
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            
            if file_extension in supported_extensions:
                documents_found += 1
                logger.info(f"Found document: {file_path}")
                
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Ingest document
                    result = rag_pipeline.ingest_document(content, file)
                    documents_loaded += 1
                    
                    logger.info(f"Successfully loaded: {file} - {result['chunks_created']} chunks created")
                    
                except Exception as e:
                    logger.error(f"Error loading {file}: {str(e)}")
    
    logger.info(f"Document loading complete. Found: {documents_found}, Loaded: {documents_loaded}")
    
    return {
        "total_found": documents_found,
        "total_loaded": documents_loaded,
        "status": "success" if documents_loaded > 0 else "no_documents_found"
    }


def main():
    """Main function to set up and load sample documents"""
    
    logger.info("Starting Smart Research Assistant setup...")
    
    # Load configuration
    try:
        config = load_environment_variables()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        return
    
    # Initialize RAG Pipeline
    try:
        rag_pipeline = RAGPipeline(
            groq_api_key=config["groq_api_key"],
            llm_model=config["llm_model"],
            embedding_model=config["embedding_model"],
            db_path=config["chroma_db_path"],
            chunk_size=config["chunk_size"],
            chunk_overlap=config["chunk_overlap"],
            top_k=config["top_k_documents"],
            temperature=config["temperature"]
        )
        logger.info("RAG Pipeline initialized")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Pipeline: {str(e)}")
        return
    
    # Load sample documents
    result = load_sample_documents(rag_pipeline)
    
    # Get database stats
    try:
        stats = rag_pipeline.get_database_stats()
        logger.info(f"Database stats: {stats}")
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
    
    logger.info("Setup complete!")
    
    return result


if __name__ == "__main__":
    main()
