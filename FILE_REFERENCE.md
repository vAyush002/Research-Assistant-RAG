# Project Structure & File Reference

This document explains the purpose and content of each file in the Smart Research Assistant project.

---

## 📁 Root Level Files

### `requirements.txt`
**Purpose:** Lists all Python dependencies needed for the project  
**Contents:**
- Streamlit (Frontend framework)
- FastAPI (Backend framework)
- LangChain (RAG framework)
- ChromaDB (Vector database)
- Sentence Transformers (Embeddings)
- PyPDF2 (PDF processing)
- And other utilities

**Usage:** `pip install -r requirements.txt`

### `.env`
**Purpose:** Environment configuration file with sensitive API keys  
**Key Variables:**
- `GROQ_API_KEY`: Your Groq API key (required)
- `LLM_MODEL`: Model to use (default: llama-3.1-70b-versatile)
- `EMBEDDING_MODEL`: Embedding model (default: all-MiniLM-L6-v2)
- `CHROMA_DB_PATH`: Vector database path
- `CHUNK_SIZE`: Text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_DOCUMENTS`: Number of documents to retrieve (default: 3)
- `TEMPERATURE`: LLM temperature (0-1, default: 0.7)

**Security Note:** Never commit `.env` to git. Use `.gitignore` to exclude it.

### `README.md`
**Purpose:** Main project documentation  
**Contains:**
- Project overview
- Features list
- Architecture diagram
- Setup instructions
- API endpoint documentation
- Deployment guides
- Troubleshooting section

### `SETUP_GUIDE.md`
**Purpose:** Detailed OS-specific setup instructions  
**Includes:**
- Windows setup steps
- macOS setup steps
- Linux setup steps
- Troubleshooting for each OS
- Common commands

### `.gitignore`
**Purpose:** Specifies files to exclude from version control  
**Excludes:**
- Virtual environment folder
- Python cache files
- Environment variables
- Logs
- Database files
- IDE files

---

## 🔧 Backend Files (`backend/` directory)

### `backend/__init__.py`
**Purpose:** Makes the backend folder a Python package  
**Content:** Empty or minimal initialization code

### `backend/main.py`
**Purpose:** FastAPI application entry point and API routes  
**Key Components:**
- FastAPI app initialization
- CORS middleware configuration
- RAG Pipeline setup
- API route handlers:
  - `GET /health` - Health check
  - `POST /query` - Query documents
  - `POST /upload` - Upload documents
  - `GET /stats` - Get database statistics
  - `POST /clear-database` - Clear knowledge base
  - `GET /` - Root endpoint with available routes

**Dependencies:** Uses RAG pipeline, utilities

### `backend/rag_pipeline.py`
**Purpose:** Complete RAG (Retrieval-Augmented Generation) pipeline  
**Key Classes:**
- `RAGPipeline`: Main orchestration class

**Key Methods:**
- `ingest_document()` - Process and store documents
- `retrieve_context()` - Search for relevant documents
- `generate_answer()` - Generate answer using LLM
- `query()` - Complete RAG pipeline
- `get_database_stats()` - Get knowledge base statistics

**Workflow:**
1. Document preprocessed and chunked
2. Chunks converted to embeddings
3. Stored in ChromaDB
4. Query embedded and searched
5. Top-k documents retrieved
6. Context passed to LLM
7. Answer generated and returned

### `backend/vector_store.py`
**Purpose:** ChromaDB vector database operations  
**Key Classes:**
- `VectorStore`: Manages all database operations

**Key Methods:**
- `add_documents()` - Add documents with embeddings
- `similarity_search()` - Find similar documents
- `get_all_documents()` - Retrieve all documents
- `delete_collection()` - Clear database
- `get_collection_stats()` - Get database info

**Database Structure:**
- Collection: "research_documents"
- Distance metric: Cosine similarity
- Persistent storage in local directory

### `backend/embeddings.py`
**Purpose:** Generate embeddings using Sentence Transformers  
**Key Classes:**
- `EmbeddingGenerator`: Manages embedding model

**Key Methods:**
- `generate_embedding()` - Single text embedding
- `generate_embeddings()` - Batch embeddings
- `get_model_info()` - Model information

**Model:** all-MiniLM-L6-v2 (384 dimensions, lightweight, fast)

### `backend/preprocessing.py`
**Purpose:** Text preprocessing and chunking  
**Key Classes:**
- `TextPreprocessor`: Handles text cleaning and splitting

**Key Methods:**
- `clean_text()` - Remove noise and normalize
- `split_text()` - Split into chunks
- `preprocess_document()` - Complete pipeline
- `extract_metadata()` - Extract document metadata

**Chunking Strategy:**
- RecursiveCharacterTextSplitter
- Splits on: "\n\n", "\n", " ", ""
- Configurable chunk size and overlap

### `backend/utils.py`
**Purpose:** Utility functions used across the backend  
**Key Functions:**
- `load_environment_variables()` - Load and validate .env
- `configure_logging()` - Setup logging to file and console
- `validate_pdf_file()` - Verify PDF files
- `validate_text_file()` - Verify text files
- `format_response()` - Standardize API responses
- `ensure_directory_exists()` - Create directories as needed

---

## 🎨 Frontend Files (`frontend/` directory)

### `frontend/__init__.py`
**Purpose:** Makes the frontend folder a Python package

### `frontend/streamlit_app.py`
**Purpose:** Complete Streamlit user interface  
**Key Sections:**

**Sidebar:**
- API health status indicator
- Database management (refresh, clear)
- Chat history management
- Statistics display

**Main Content:**
- Document upload section
- Query input box
- Answer display with formatting
- Source display
- Similarity score visualization
- Chat history browser

**Features:**
- Real-time streaming responses
- Beautiful formatting with custom CSS
- Interactive buttons and inputs
- Session state management
- Chat history persistence

**UI Components:**
- File uploader (supports PDF, TXT)
- Text input for questions
- Expandable chat history
- Metrics display
- Source citations

---

## 📊 Data Files (`data/` directory)

### `data/articles/machine_learning_guide.txt`
**Purpose:** Sample document about ML fundamentals  
**Content:** ~3000+ words on:
- Supervised learning
- Unsupervised learning
- Reinforcement learning
- Common algorithms
- Best practices

### `data/articles/deep_learning_neural_networks.txt`
**Purpose:** Sample document about deep learning  
**Content:** ~3000+ words on:
- Neural network architecture
- Activation functions
- Backpropagation
- CNN, RNN, LSTM, Transformers
- Training and optimization

### `data/articles/nlp_fundamentals.txt`
**Purpose:** Sample document about NLP  
**Content:** ~3000+ words on:
- NLP tasks and applications
- Text representation methods
- Language models
- Pre-trained models
- Challenges and solutions

---

## 🗄️ Database Files (`database/` directory)

### `database/chroma_db/`
**Purpose:** Local ChromaDB persistent storage  
**Contents:**
- Parquet files with embeddings
- Metadata
- Document chunks
- Index files

**Note:** Created automatically when first documents are added

---

## 📝 Logging Files (`logs/` directory)

### `logs/app.log`
**Purpose:** Application log file  
**Contains:**
- Startup messages
- Document ingestion logs
- Query processing logs
- Error messages
- Database operations

---

## 🚀 Deployment Files

### `Dockerfile`
**Purpose:** Docker container configuration  
**Defines:**
- Base image: Python 3.9
- Working directory
- Dependency installation
- Port exposure
- Health check
- Startup command

**Usage:** `docker build -t smart-research .`

### `docker-compose.yml`
**Purpose:** Multi-container orchestration  
**Services:**
- Backend (FastAPI)
- Frontend (Streamlit)
- Database volume

**Usage:** `docker-compose up`

### `deploy_aws.sh`
**Purpose:** Automated AWS EC2 deployment script  
**Performs:**
- System package updates
- Python and Node.js installation
- Project setup
- PM2 configuration
- Nginx setup
- SSL certificates (optional)

**Usage:** `bash deploy_aws.sh`

---

## 🎯 Script Files

### `app.py`
**Purpose:** Main application launcher  
**Functionality:**
- Loads environment variables
- Starts FastAPI backend
- Starts Streamlit frontend
- Manages both processes
- Handles graceful shutdown

**Usage:** `python app.py`

### `load_sample_documents.py`
**Purpose:** Populate database with sample documents  
**Functionality:**
- Walks through data directory
- Loads PDF and TXT files
- Processes documents through RAG pipeline
- Logs ingestion progress
- Reports statistics

**Usage:** `python load_sample_documents.py`

### `quick_start.bat`
**Purpose:** Windows automated setup script  
**Handles:**
- Virtual environment creation
- Dependency installation
- Environment validation
- Sample document loading
- Application startup

**Usage:** Double-click or `quick_start.bat`

### `quick_start.sh`
**Purpose:** Linux/macOS automated setup script  
**Handles:**
- Virtual environment creation
- Dependency installation
- Environment validation
- Directory creation
- Application startup

**Usage:** `bash quick_start.sh` or `./quick_start.sh`

---

## 📚 Configuration Reference

### Python Files Interaction

```
app.py (Main Entry)
  ↓
backend/main.py (FastAPI Server)
  ├── backend/rag_pipeline.py (Core RAG)
  │   ├── backend/embeddings.py (Embedding Gen)
  │   ├── backend/vector_store.py (ChromaDB)
  │   └── backend/preprocessing.py (Text Processing)
  ├── backend/utils.py (Helpers)
  └── Groq API (LLaMA 3.1)

frontend/streamlit_app.py (UI)
  └── Calls backend/main.py APIs
```

---

## 🔄 Data Flow

### Document Upload
```
Streamlit UI
  ↓
POST /upload
  ↓
Extract Text (PDF/TXT)
  ↓
Preprocessing (Clean, Chunk)
  ↓
Embedding Generation
  ↓
ChromaDB Storage
  ↓
Success Response
```

### Query Processing
```
Streamlit UI
  ↓
POST /query
  ↓
Generate Query Embedding
  ↓
Similarity Search (ChromaDB)
  ↓
Retrieve Top-K Documents
  ↓
Format Context
  ↓
Call Groq LLaMA API
  ↓
Generate Answer
  ↓
Return Answer + Sources
  ↓
Display in UI
```

---

## 📈 File Size Reference

- `backend/main.py`: ~300 lines
- `backend/rag_pipeline.py`: ~250 lines
- `frontend/streamlit_app.py`: ~350 lines
- `README.md`: ~500 lines
- `requirements.txt`: ~15 lines
- Sample documents: ~9000 words total

---

## 🔐 Security Considerations

**Sensitive Files to Protect:**
- `.env` - Contains API keys
- `.env.local` - Local overrides
- `database/chroma_db/` - User data
- `logs/` - May contain sensitive info

**Never Commit to Git:**
- `.env` files
- API keys
- Database files
- Logs

**Use `.gitignore` to exclude these**

---

## 💾 Backup Recommendations

**Important to Backup:**
- `.env` (but securely)
- `database/chroma_db/` (user data)
- Custom documents in `data/`

**Safe to Regenerate:**
- `logs/`
- `venv/` (virtual environment)
- Python cache files

---

## 📞 File Modification Guide

### To Add New API Endpoint
Edit: `backend/main.py`
- Add new route decorator
- Add request model (Pydantic)
- Implement handler logic

### To Customize UI
Edit: `frontend/streamlit_app.py`
- Modify layout (columns, containers)
- Update colors and styling
- Add new widgets

### To Change LLM Model
Edit: `.env`
- Change `LLM_MODEL` value
- Example: `llama-3.1-8b-instant`

### To Adjust Text Chunking
Edit: `.env`
- Modify `CHUNK_SIZE`
- Modify `CHUNK_OVERLAP`
- Or edit `backend/preprocessing.py`

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Compatibility:** Python 3.8+
