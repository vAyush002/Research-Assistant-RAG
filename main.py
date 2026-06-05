import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import PyPDF2
import os

from rag_pipeline import RAGPipeline
from utils import load_environment_variables, configure_logging, format_response

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Load configuration
config = load_environment_variables()

# Initialize FastAPI app
app = FastAPI(
    title="Smart Research Assistant API",
    description="RAG-based AI Research Assistant API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    logger.info("RAG Pipeline initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Pipeline: {str(e)}")
    raise


# Pydantic Models
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    retrieved_docs_count: int
    model: str
    similarity_scores: Optional[List[float]] = None


class HealthResponse(BaseModel):
    status: str
    message: str


class StatsResponse(BaseModel):
    collection_name: str
    total_documents: int
    db_path: str


# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF content"""
    try:
        pdf_reader = PyPDF2.PdfReader(open(os.path.splitext("temp.pdf")[0] + ".pdf", "wb"))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise


# API Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Smart Research Assistant API is running"
    }


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the knowledge base for an answer"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing query: {request.question}")
        
        # Process query through RAG pipeline
        result = rag_pipeline.query(request.question)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or text document"""
    try:
        # Validate file
        if file.filename is None:
            raise HTTPException(status_code=400, detail="File name is required")
        
        allowed_extensions = ['.pdf', '.txt']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Only {', '.join(allowed_extensions)} files are supported"
            )
        
        logger.info(f"Processing file upload: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file_extension == '.pdf':
            import io
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:  # .txt file
            text = content.decode('utf-8')
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content found in file")
        
        # Ingest document
        result = rag_pipeline.ingest_document(text, file.filename)
        
        return format_response(
            success=True,
            message=f"Document '{file.filename}' uploaded and processed successfully",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
async def get_database_stats():
    """Get statistics about the knowledge base"""
    try:
        stats = rag_pipeline.get_database_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear-database")
async def clear_database():
    """Clear all documents from the knowledge base"""
    try:
        rag_pipeline.vector_store.delete_collection()
        
        # Reinitialize collection
        rag_pipeline.vector_store.collection = (
            rag_pipeline.vector_store.client.get_or_create_collection(
                name=rag_pipeline.vector_store.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        )
        
        logger.info("Database cleared successfully")
        return format_response(
            success=True,
            message="Knowledge base cleared successfully"
        )
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Smart Research Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "upload": "/upload",
            "stats": "/stats",
            "clear": "/clear-database"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config["fastapi_host"],
        port=config["fastapi_port"]
    )
