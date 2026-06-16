import os
import logging
from dotenv import load_dotenv


def load_environment_variables():
    load_dotenv()

    return {
        "groq_api_key": os.getenv("GROQ_API_KEY"),

        "llm_model": os.getenv(
            "LLM_MODEL",
            "llama-3.3-70b-versatile"
        ),

        "embedding_model": os.getenv(
            "EMBEDDING_MODEL",
            "all-MiniLM-L6-v2"
        ),

        "chroma_db_path": os.getenv(
            "CHROMA_DB_PATH",
            "database/chroma_db"
        ),

        "chunk_size": int(
            os.getenv("CHUNK_SIZE", 1000)
        ),

        "chunk_overlap": int(
            os.getenv("CHUNK_OVERLAP", 200)
        ),

        "top_k_documents": int(
            os.getenv("TOP_K_DOCUMENTS", 3)
        ),

        "temperature": float(
            os.getenv("TEMPERATURE", 0.7)
        ),

        "fastapi_host": os.getenv(
            "FASTAPI_HOST",
            "0.0.0.0"
        ),

        "fastapi_port": int(
            os.getenv("FASTAPI_PORT", 8000)
        )
    }


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def format_response(success=True,
                    message="",
                    data=None):

    return {
        "success": success,
        "message": message,
        "data": data
    }