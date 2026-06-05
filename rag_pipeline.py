import logging
import uuid
from typing import List, Dict, Tuple
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from preprocessing import TextPreprocessor, extract_metadata

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG (Retrieval-Augmented Generation) pipeline"""
    
    def __init__(self, groq_api_key: str, llm_model: str = "llama-3.3-70b-versatile",
                 embedding_model: str = "all-MiniLM-L6-v2", 
                 db_path: str = "database/chroma_db",
                 chunk_size: int = 1000, chunk_overlap: int = 200,
                 top_k: int = 3, temperature: float = 0.7):
        """Initialize RAG pipeline components"""
        
        logger.info("Initializing RAG Pipeline...")
        
        # Initialize components
        self.embedding_generator = EmbeddingGenerator(model_name=embedding_model)
        self.vector_store = VectorStore(db_path=db_path)
        self.preprocessor = TextPreprocessor(chunk_size=chunk_size, 
                                            chunk_overlap=chunk_overlap)
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model_name=llm_model,
            temperature=temperature
        )
        
        self.top_k = top_k
        self.llm_model = llm_model
        
        # RAG prompt template
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful AI Research Assistant. Use the provided context to answer the user's question accurately and concisely.

Context:
{context}

Question: {question}

Answer: Based on the provided context, """
        )
        
        logger.info("RAG Pipeline initialized successfully")
    
    def ingest_document(self, document_text: str, source_name: str) -> Dict:
        """Ingest and process a document"""
        try:
            logger.info(f"Ingesting document: {source_name}")
            
            # Preprocess document
            chunks = self.preprocessor.preprocess_document(document_text)
            
            # Extract metadata
            metadata = extract_metadata(source_name, document_text)
            
            # Generate embeddings
            embeddings = self.embedding_generator.generate_embeddings(chunks)
            
            # Create IDs for chunks
            chunk_ids = [f"{source_name}_chunk_{i}_{str(uuid.uuid4())[:8]}" 
                        for i in range(len(chunks))]
            
            # Create metadatas for each chunk
            metadatas = [
                {
                    "source": source_name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            # Add to vector store
            self.vector_store.add_documents(chunks, embeddings, metadatas, chunk_ids)
            
            result = {
                "status": "success",
                "source": source_name,
                "chunks_created": len(chunks),
                "document_length": len(document_text)
            }
            
            logger.info(f"Document ingested successfully: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error ingesting document: {str(e)}")
            raise
    
    def retrieve_context(self, question: str, top_k: int = None) -> List[Dict]:
        """Retrieve relevant context for a question"""
        try:
            if top_k is None:
                top_k = self.top_k
            
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(question)
            
            # Search vector store
            retrieved_docs = self.vector_store.similarity_search(query_embedding, top_k)
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> Dict:
        """Generate answer using retrieved context"""
        try:
            context_text = "\n\n".join([
                f"[Source: {doc['metadata']['source']}]\n{doc['content']}"
                for doc in context_docs
            ])

            chain = self.rag_prompt | self.llm

            response = chain.invoke(
                {
                    "context": context_text,
                    "question": question
                }
            )

            answer = response.content

            result = {
                "question": question,
                "answer": answer.strip(),
                "sources": list(
                    set(
                        [doc["metadata"]["source"] for doc in context_docs]
                    )
                ),
                "retrieved_docs_count": len(context_docs),
                "model": self.llm_model
            }

            return result

        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise


    def query(self, question: str) -> Dict:
        """Complete RAG query pipeline"""
        try:
            logger.info(f"Processing query: {question}")

            # Retrieve relevant documents
            context_docs = self.retrieve_context(question)

            if not context_docs:
                return {
                    "question": question,
                    "answer": "No relevant documents found.",
                    "sources": [],
                    "retrieved_docs_count": 0,
                    "model": self.llm_model
                }

            # Generate answer
            result = self.generate_answer(question, context_docs)

            # Add similarity scores
            result["similarity_scores"] = [
                doc["similarity_score"]
                for doc in context_docs
            ]

            logger.info("Query processed successfully")

            return result

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise


    def get_database_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return self.vector_store.get_collection_stats()