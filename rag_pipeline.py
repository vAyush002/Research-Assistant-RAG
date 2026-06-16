import logging
import uuid
from typing import Dict, List, Optional

from langchain_core.prompts import PromptTemplate

from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from preprocessing import TextPreprocessor, extract_metadata

logger = logging.getLogger(__name__)


# Supported LLM providers and their selectable models (first entry = default).
# Embeddings always run locally (sentence-transformers) and need no API key —
# the provider/key below is only used to generate the final answer.
PROVIDER_MODELS = {
    "Groq": [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
    ],
    "Anthropic (Claude)": [
        "claude-opus-4-8",
        "claude-sonnet-4-6",
        "claude-haiku-4-5",
    ],
    "OpenAI": [
        "gpt-4o",
        "gpt-4o-mini",
    ],
}


def build_llm(provider: str, api_key: str, model: str,
              temperature: float = 0.7, max_tokens: int = 2048):
    """Construct a LangChain chat model for the chosen provider.

    Each provider package is imported lazily so a missing optional dependency
    for one provider never breaks the others.
    """
    if not api_key:
        raise ValueError("An API key is required to generate answers.")

    key = provider.lower()

    if "groq" in key:
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=api_key, model=model,
            temperature=temperature, max_tokens=max_tokens,
        )

    if "anthropic" in key or "claude" in key:
        from langchain_anthropic import ChatAnthropic
        # Claude Opus 4.8 / 4.7 reject `temperature` (returns HTTP 400), so we
        # intentionally omit it for Anthropic to stay compatible across models.
        return ChatAnthropic(api_key=api_key, model=model, max_tokens=max_tokens)

    if "openai" in key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=api_key, model=model,
            temperature=temperature, max_tokens=max_tokens,
        )

    raise ValueError(f"Unsupported provider: {provider}")


def _message_text(message) -> str:
    """Extract plain text from a LangChain message, which may carry content as a
    string or as a list of content blocks (e.g. Anthropic)."""
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(block.get("text", ""))
            else:
                parts.append(getattr(block, "text", ""))
        return "".join(parts)
    return str(content)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline.

    Heavy, provider-independent components (embeddings, vector store, the text
    splitter) are injected so callers can build them once and reuse them while
    swapping the LLM (provider / key / model) freely. `llm` may be None for
    ingestion-only use — only querying requires it.
    """

    def __init__(self, embedding_generator: EmbeddingGenerator,
                 vector_store: VectorStore, llm=None,
                 preprocessor: Optional[TextPreprocessor] = None,
                 top_k: int = 3):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.preprocessor = preprocessor or TextPreprocessor()
        self.llm = llm
        self.top_k = top_k
        self.llm_model = getattr(llm, "model", getattr(llm, "model_name", "unknown")) if llm else None

        self.rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful AI Research Assistant. Use the provided context to answer the user's question accurately and concisely. If the context does not contain the answer, say so plainly.

Context:
{context}

Question: {question}

Answer: Based on the provided context, """
        )

    def ingest_document(self, document_text: str, source_name: str) -> Dict:
        """Ingest and process a document into the vector store."""
        try:
            logger.info(f"Ingesting document: {source_name}")

            chunks = self.preprocessor.preprocess_document(document_text)
            if not chunks:
                raise ValueError("Document produced no text chunks after cleaning.")

            embeddings = self.embedding_generator.generate_embeddings(chunks)

            chunk_ids = [
                f"{source_name}_chunk_{i}_{str(uuid.uuid4())[:8]}"
                for i in range(len(chunks))
            ]
            metadatas = [
                {"source": source_name, "chunk_index": i, "total_chunks": len(chunks)}
                for i in range(len(chunks))
            ]

            self.vector_store.add_documents(chunks, embeddings, metadatas, chunk_ids)

            result = {
                "status": "success",
                "source": source_name,
                "chunks_created": len(chunks),
                "document_length": len(document_text),
            }
            logger.info(f"Document ingested successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Error ingesting document: {str(e)}")
            raise

    def retrieve_context(self, question: str, top_k: int = None) -> List[Dict]:
        """Retrieve relevant context for a question."""
        try:
            if top_k is None:
                top_k = self.top_k
            query_embedding = self.embedding_generator.generate_embedding(question)
            retrieved_docs = self.vector_store.similarity_search(query_embedding, top_k)
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query")
            return retrieved_docs
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise

    def generate_answer(self, question: str, context_docs: List[Dict]) -> Dict:
        """Generate an answer using the retrieved context."""
        if self.llm is None:
            raise ValueError("No LLM configured. Provide an API key to generate answers.")
        try:
            context_text = "\n\n".join([
                f"[Source: {doc['metadata']['source']}]\n{doc['content']}"
                for doc in context_docs
            ])

            chain = self.rag_prompt | self.llm
            response = chain.invoke({"context": context_text, "question": question})
            answer = _message_text(response).strip()

            return {
                "question": question,
                "answer": answer,
                "sources": list({doc["metadata"]["source"] for doc in context_docs}),
                "retrieved_docs_count": len(context_docs),
                "model": self.llm_model,
            }
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    def query(self, question: str) -> Dict:
        """Complete RAG query pipeline: retrieve, then generate."""
        try:
            logger.info(f"Processing query: {question}")
            context_docs = self.retrieve_context(question)

            if not context_docs:
                return {
                    "question": question,
                    "answer": "No relevant documents found. Upload some documents first.",
                    "sources": [],
                    "retrieved_docs_count": 0,
                    "model": self.llm_model,
                    "similarity_scores": [],
                }

            result = self.generate_answer(question, context_docs)
            result["similarity_scores"] = [doc["similarity_score"] for doc in context_docs]
            logger.info("Query processed successfully")
            return result
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

    def get_database_stats(self) -> Dict:
        """Get knowledge base statistics."""
        return self.vector_store.get_collection_stats()
