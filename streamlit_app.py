import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subheader {
        font-size: 1.5em;
        color: #555;
        margin-bottom: 20px;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .source-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'db_stats' not in st.session_state:
    st.session_state.db_stats = None


def get_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def query_api(question: str):
    """Send query to API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question},
            timeout=30
        )
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to API. Make sure FastAPI server is running on port 8000"}, 500
    except Exception as e:
        return {"error": str(e)}, 500


def upload_document(uploaded_file):
    """Upload document to API"""
    try:
        files = {'file': (uploaded_file.name, uploaded_file.getbuffer())}
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            timeout=30
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def get_database_stats():
    """Get database statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=5)
        return response.json(), response.status_code
    except:
        return None, 500


def clear_database():
    """Clear the database"""
    try:
        response = requests.post(f"{API_BASE_URL}/clear-database", timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


# Main UI
st.markdown("<div class='main-header'>🤖 Smart Research Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Powered by Groq LLaMA 3.1 & ChromaDB</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Health Check
    api_health = get_api_health()
    if api_health:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Offline - Start FastAPI server")
        st.info("Run: `uvicorn backend.main:app --reload`")
    
    st.divider()
    
    # Database Management
    st.subheader("📊 Knowledge Base")
    
    if st.button("📈 Refresh Stats", use_container_width=True):
        stats, _ = get_database_stats()
        st.session_state.db_stats = stats
    
    if st.session_state.db_stats:
        st.metric("Total Documents", st.session_state.db_stats.get("total_documents", 0))
    
    if st.button("🗑️ Clear Database", use_container_width=True):
        result, status = clear_database()
        if status == 200:
            st.success("Database cleared!")
            st.session_state.db_stats = None
        else:
            st.error("Error clearing database")
    
    st.divider()
    
    # Chat History
    st.subheader("💬 Chat History")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
    
    if len(st.session_state.chat_history) > 0:
        st.write(f"Total conversations: {len(st.session_state.chat_history)}")


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        help="Upload documents to build your knowledge base"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                result, status = upload_document(uploaded_file)
                if status == 200:
                    st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                    if 'chunks_created' in result.get('data', {}):
                        st.info(f"Created {result['data']['chunks_created']} chunks")
                else:
                    st.error(f"❌ Error uploading {uploaded_file.name}: {result.get('error', 'Unknown error')}")

with col2:
    st.subheader("📊 Stats")
    stats, _ = get_database_stats()
    if stats:
        st.metric("Documents", stats.get("total_documents", 0))
    else:
        st.metric("Documents", "N/A")

st.divider()

# Query Section
st.subheader("🔍 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is machine learning?",
    help="Ask any question about your uploaded documents"
)

if st.button("🚀 Get Answer", use_container_width=True, type="primary"):
    if not question.strip():
        st.warning("Please enter a question")
    elif not api_health:
        st.error("API is not connected. Please start the FastAPI server.")
    else:
        with st.spinner("🔄 Searching and generating answer..."):
            result, status = query_api(question)
            
            if status == 200:
                # Add to chat history
                st.session_state.chat_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question,
                    "answer": result.get("answer"),
                    "sources": result.get("sources", []),
                    "scores": result.get("similarity_scores", [])
                })
                
                # Display answer
                st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                st.markdown("### 💡 Answer")
                st.write(result.get("answer", "No answer generated"))
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display sources
                if result.get("sources"):
                    st.markdown("### 📚 Sources")
                    for source in result.get("sources", []):
                        st.markdown(f"<div class='source-box'>{source}</div>", 
                                  unsafe_allow_html=True)
                
                # Display similarity scores
                if result.get("similarity_scores"):
                    st.markdown("### 📊 Relevance Scores")
                    cols = st.columns(len(result.get("similarity_scores", [])))
                    for i, score in enumerate(result.get("similarity_scores", [])):
                        with cols[i]:
                            st.metric(f"Document {i+1}", f"{score:.2%}")
                
                st.success("✅ Answer generated successfully!")
                
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")

st.divider()

# Chat History Display
if st.session_state.chat_history:
    st.subheader("📋 Chat History")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
        with st.expander(f"Conversation {len(st.session_state.chat_history) - i + 1} - {chat['timestamp']}"):
            st.markdown(f"**Q:** {chat['question']}")
            st.markdown(f"**A:** {chat['answer']}")
            if chat['sources']:
                st.markdown(f"**Sources:** {', '.join(chat['sources'])}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; margin-top: 20px;'>
        <p>Smart Research Assistant v1.0 | Built with Streamlit, FastAPI, LangChain & ChromaDB</p>
        <p>Powered by Groq LLaMA 3.1</p>
    </div>
""", unsafe_allow_html=True)
