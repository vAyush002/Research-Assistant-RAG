"""Smart Research Assistant — single-file Streamlit app.

Runs the full RAG pipeline in-process (no separate backend needed):
  streamlit run streamlit_app.py

Embeddings run locally (sentence-transformers); the API key entered in the
sidebar is used only to generate the final answer with the chosen provider.
The key lives in session memory only — it is never written to disk or logged.
"""

import io
import logging
from datetime import datetime

import streamlit as st
from pypdf import PdfReader

from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from preprocessing import TextPreprocessor
from rag_pipeline import RAGPipeline, build_llm, PROVIDER_MODELS

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header { font-size: 2.8em; font-weight: bold; color: #1f77b4; margin-bottom: 4px; }
    .subheader { font-size: 1.2em; color: #666; margin-bottom: 16px; }
    .response-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px;
                    border-left: 5px solid #1f77b4; margin: 10px 0; }
    .source-box { background-color: #e8f4f8; padding: 12px; border-radius: 8px; margin: 8px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Where to get a key for each provider (shown as help text in the sidebar).
PROVIDER_KEY_HELP = {
    "Groq": "Get a free key at https://console.groq.com/keys",
    "Anthropic (Claude)": "Get a key at https://console.anthropic.com/settings/keys",
    "OpenAI": "Get a key at https://platform.openai.com/api-keys",
}


# --- Cached heavy resources (loaded once, reused across reruns) -------------
@st.cache_resource(show_spinner="Loading embedding model…")
def get_embedder() -> EmbeddingGenerator:
    return EmbeddingGenerator()


@st.cache_resource(show_spinner="Connecting to vector database…")
def get_vector_store() -> VectorStore:
    return VectorStore()


@st.cache_resource
def get_preprocessor() -> TextPreprocessor:
    return TextPreprocessor()


# --- Session state ----------------------------------------------------------
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("api_keys", {})  # per-provider, in-memory only


def extract_text(uploaded_file) -> str:
    """Extract text from an uploaded PDF or TXT file."""
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()
    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    return data.decode("utf-8", errors="ignore")


# --- Header -----------------------------------------------------------------
st.markdown("<div class='main-header'>🤖 Smart Research Assistant</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subheader'>Local RAG over your documents — answer with Groq, Claude, or OpenAI</div>",
    unsafe_allow_html=True,
)

# --- Sidebar: model + key configuration ------------------------------------
with st.sidebar:
    st.header("⚙️ Model & API Key")

    provider = st.selectbox("LLM Provider", list(PROVIDER_MODELS.keys()), index=0)

    api_key = st.text_input(
        f"{provider} API key",
        type="password",
        value=st.session_state.api_keys.get(provider, ""),
        help=PROVIDER_KEY_HELP.get(provider, ""),
        placeholder="Paste your key (kept in memory only)",
    )
    st.session_state.api_keys[provider] = api_key

    model = st.selectbox("Model", PROVIDER_MODELS[provider], index=0)

    with st.expander("Advanced settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        if provider.startswith("Anthropic"):
            st.caption("Temperature is ignored for Claude Opus/Sonnet 4.x.")
        top_k = st.slider("Documents to retrieve (top-k)", 1, 10, 3)
        max_tokens = st.slider("Max answer tokens", 256, 4096, 2048, 256)

    st.caption("🔒 Embeddings run locally. Your key is used only to generate answers "
               "and is never stored on disk.")

    st.divider()
    st.subheader("📊 Knowledge Base")
    vstore = get_vector_store()
    try:
        doc_count = vstore.get_collection_stats().get("total_documents", 0)
    except Exception:
        doc_count = 0
    st.metric("Chunks indexed", doc_count)

    if st.button("🗑️ Clear Knowledge Base", use_container_width=True):
        try:
            vstore.delete_collection()
            vstore.collection = vstore.client.get_or_create_collection(
                name=vstore.collection_name, metadata={"hnsw:space": "cosine"}
            )
            st.success("Knowledge base cleared.")
            st.rerun()
        except Exception as e:
            st.error(f"Error clearing database: {e}")

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


embedder = get_embedder()
preprocessor = get_preprocessor()

# --- Document upload --------------------------------------------------------
st.subheader("📤 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload PDF or TXT files to build your knowledge base",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    ingest_pipeline = RAGPipeline(embedder, vstore, preprocessor=preprocessor)
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}…"):
            try:
                text = extract_text(uploaded_file)
                if not text.strip():
                    st.warning(f"No extractable text in {uploaded_file.name}.")
                    continue
                result = ingest_pipeline.ingest_document(text, uploaded_file.name)
                st.success(f"✅ {uploaded_file.name}: {result['chunks_created']} chunks indexed")
            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {e}")
    st.rerun()

st.divider()

# --- Ask a question ---------------------------------------------------------
st.subheader("🔍 Ask a Question")
question = st.text_input("Your question:", placeholder="e.g., What are the key findings?")

if st.button("🚀 Get Answer", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not api_key:
        st.error(f"Please enter your {provider} API key in the sidebar.")
    else:
        try:
            with st.spinner("🔄 Searching documents and generating an answer…"):
                llm = build_llm(provider, api_key, model,
                                temperature=temperature, max_tokens=max_tokens)
                pipeline = RAGPipeline(embedder, vstore, llm=llm,
                                       preprocessor=preprocessor, top_k=top_k)
                result = pipeline.query(question)

            st.markdown("### 💡 Answer")
            st.markdown(f"<div class='response-box'>{result['answer']}</div>", unsafe_allow_html=True)

            if result.get("sources"):
                st.markdown("### 📚 Sources")
                for source in result["sources"]:
                    st.markdown(f"<div class='source-box'>{source}</div>", unsafe_allow_html=True)

            scores = result.get("similarity_scores") or []
            if scores:
                st.markdown("### 📊 Relevance Scores")
                cols = st.columns(len(scores))
                for i, score in enumerate(scores):
                    cols[i].metric(f"Doc {i + 1}", f"{score:.0%}")

            st.session_state.chat_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question": question,
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "model": f"{provider} · {model}",
            })
        except Exception as e:
            st.error(f"Error generating answer: {e}")

# --- Chat history -----------------------------------------------------------
if st.session_state.chat_history:
    st.divider()
    st.subheader("📋 History")
    for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
        n = len(st.session_state.chat_history) - i + 1
        with st.expander(f"Q{n} · {chat['timestamp']} · {chat.get('model', '')}"):
            st.markdown(f"**Q:** {chat['question']}")
            st.markdown(f"**A:** {chat['answer']}")
            if chat["sources"]:
                st.caption("Sources: " + ", ".join(chat["sources"]))

st.divider()
st.caption("Smart Research Assistant · Streamlit + LangChain + ChromaDB · "
           "embeddings: all-MiniLM-L6-v2 (local)")
