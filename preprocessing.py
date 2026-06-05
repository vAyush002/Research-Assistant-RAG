import re
import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Handles text cleaning and preprocessing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.!?,;:\-\(\)]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        logger.info(f"Text cleaned. Original length: varying, cleaned length: {len(text)}")
        return text
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        chunks = self.splitter.split_text(text)
        logger.info(f"Text split into {len(chunks)} chunks")
        return chunks
    
    def preprocess_document(self, text: str) -> List[str]:
        """Complete preprocessing pipeline"""
        cleaned_text = self.clean_text(text)
        chunks = self.split_text(cleaned_text)
        return chunks


def extract_metadata(filename: str, content: str) -> dict:
    """Extract metadata from document"""
    metadata = {
        "source": filename,
        "length": len(content),
        "content_preview": content[:100] if content else ""
    }
    return metadata
