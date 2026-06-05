# Smart Research Assistant

A production-quality Generative AI application that demonstrates RAG (Retrieval-Augmented Generation), embeddings, vector databases, and modern AI stack integration.

**Powered by:** Groq LLaMA 3.1 | ChromaDB | LangChain | Streamlit | FastAPI

---

## 🎯 Features

✅ **Document Ingestion** - Upload and process PDF/TXT documents  
✅ **Semantic Search** - Find relevant information using embeddings  
✅ **RAG Pipeline** - Retrieve context and generate accurate answers  
✅ **Real-time Q&A** - Ask questions about your documents  
✅ **Chat History** - Maintain conversation history  
✅ **Source Citations** - See which documents were used  
✅ **Similarity Scores** - Understand relevance of retrieved documents  
✅ **Modern UI** - Clean Streamlit interface  
✅ **REST API** - FastAPI backend for integration  

---

## 🏗️ Project Architecture

```
Smart Research Assistant
├── Backend (FastAPI + LangChain)
│   ├── Document Preprocessing
│   ├── Embedding Generation (Sentence Transformers)
│   ├── Vector Store (ChromaDB)
│   └── RAG Pipeline (Groq LLaMA 3.1)
├── Frontend (Streamlit)
│   ├── Document Upload
│   ├── Query Interface
│   └── Results Display
└── Database (ChromaDB - Local)
```

**Tech Stack:**
- **LLM:** Groq API + LLaMA 3.1 70B
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB
- **Backend:** FastAPI + Python
- **Frontend:** Streamlit
- **Framework:** LangChain

---

## 📁 Project Structure

```
Smart_Research_Assistant/
│
├── app.py                           # Main entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (Groq API key)
├── README.md                       # This file
│
├── backend/
│   ├── main.py                     # FastAPI application
│   ├── rag_pipeline.py             # RAG pipeline implementation
│   ├── vector_store.py             # ChromaDB operations
│   ├── embeddings.py               # Embedding generation
│   ├── preprocessing.py            # Text preprocessing
│   └── utils.py                    # Utility functions
│
├── frontend/
│   └── streamlit_app.py            # Streamlit UI
│
├── data/
│   ├── pdfs/                       # PDF documents
│   └── articles/                   # Text documents (sample included)
│
├── database/
│   └── chroma_db/                  # ChromaDB storage
│
├── logs/
│   └── app.log                     # Application logs
│
└── load_sample_documents.py        # Load sample documents
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Groq API Key (get free at [console.groq.com](https://console.groq.com))
- Git (optional)

### 2. Setup Environment

```bash
# Clone or download the project
cd Smart_Research_Assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Edit `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Load Sample Documents

```bash
python load_sample_documents.py
```

This will ingest the sample documents in `data/articles/` into ChromaDB.

### 5. Run the Application

**Option A: Run both frontend and backend together**
```bash
python app.py
```

**Option B: Run separately**

Terminal 1 - Backend (FastAPI):
```bash
uvicorn backend.main:app --reload
```

Terminal 2 - Frontend (Streamlit):
```bash
streamlit run frontend/streamlit_app.py
```

### 6. Access the Application

- **Frontend:** http://localhost:8501 (Streamlit)
- **Backend:** http://localhost:8000 (FastAPI)
- **API Docs:** http://localhost:8000/docs (Swagger UI)

---

## 📚 API Endpoints

### Health Check
```
GET /health
```
Check if API is running.

### Query Documents
```
POST /query
{
    "question": "What is machine learning?",
    "top_k": 3
}

Response:
{
    "question": "What is machine learning?",
    "answer": "Machine learning is...",
    "sources": ["machine_learning_guide.txt"],
    "retrieved_docs_count": 1,
    "model": "llama-3.1-70b-versatile",
    "similarity_scores": [0.85]
}
```

### Upload Document
```
POST /upload
Form-data:
- file: <PDF or TXT file>

Response:
{
    "success": true,
    "message": "Document uploaded and processed successfully",
    "data": {
        "status": "success",
        "source": "filename.pdf",
        "chunks_created": 15,
        "document_length": 5000
    }
}
```

### Get Database Statistics
```
GET /stats

Response:
{
    "collection_name": "research_documents",
    "total_documents": 25,
    "db_path": "database/chroma_db"
}
```

### Clear Database
```
POST /clear-database

Response:
{
    "success": true,
    "message": "Knowledge base cleared successfully"
}
```

---

## 🔧 Configuration

Edit `.env` to customize:

```env
# Groq API
GROQ_API_KEY=your_key_here
LLM_MODEL=llama-3.1-70b-versatile

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Vector Database
CHROMA_DB_PATH=database/chroma_db

# Text Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_DOCUMENTS=3

# Model Parameters
TEMPERATURE=0.7

# Server Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

---

## 📖 Usage Examples

### Example 1: Upload Documents and Query
```python
# Using API directly
import requests

# Upload document
files = {'file': open('paper.pdf', 'rb')}
requests.post('http://localhost:8000/upload', files=files)

# Query
response = requests.post(
    'http://localhost:8000/query',
    json={'question': 'What are the main findings?'}
)
print(response.json()['answer'])
```

### Example 2: Using via Streamlit
1. Go to http://localhost:8501
2. Upload PDF/TXT files in the "Upload Documents" section
3. Type your question in the "Ask a Question" box
4. View retrieved sources and similarity scores
5. Chat history is maintained automatically

---

## 💾 Sample Documents Included

The project includes 3 sample documents for testing:
1. **machine_learning_guide.txt** - ML fundamentals
2. **deep_learning_neural_networks.txt** - Deep learning concepts
3. **nlp_fundamentals.txt** - NLP overview

Load them with:
```bash
python load_sample_documents.py
```

---

## 🎓 Resume Impact

This project demonstrates expertise in:

✅ **Machine Learning & NLP**
- Embeddings and semantic search
- RAG pipelines
- Text preprocessing and chunking

✅ **AI & Generative AI**
- LLM integration (Groq API)
- Prompt engineering
- Chat applications

✅ **Software Engineering**
- FastAPI backend development
- REST API design
- Async/await patterns
- Error handling and logging

✅ **Databases**
- Vector databases (ChromaDB)
- Database operations (CRUD)
- Similarity search

✅ **Frontend Development**
- Streamlit UI creation
- API integration
- Real-time user interfaces

✅ **DevOps & Deployment**
- Docker containerization
- Cloud deployment (AWS/Azure)
- Environment configuration

---

## 🚀 Deployment

### Deploy on AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.large or larger (for model performance)
   - Open ports: 8000 (FastAPI), 8501 (Streamlit)

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```

4. **Clone and Setup Project**
   ```bash
   git clone <your-repo>
   cd Smart_Research_Assistant
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   nano .env
   # Add: GROQ_API_KEY=your_key
   # Change: FASTAPI_HOST=0.0.0.0
   ```

6. **Load Sample Data**
   ```bash
   python load_sample_documents.py
   ```

7. **Run with PM2 (Process Manager)**
   ```bash
   npm install -g pm2
   pm2 start "uvicorn backend.main:app --host 0.0.0.0 --port 8000" --name fastapi
   pm2 start "streamlit run frontend/streamlit_app.py" --name streamlit
   pm2 save
   ```

8. **Access Application**
   ```
   http://your-instance-ip:8000    (API)
   http://your-instance-ip:8501    (Streamlit)
   ```

### Deploy on Azure

1. **Create App Service**
   ```bash
   az group create --name myResourceGroup --location eastus
   az appservice plan create --name myAppPlan --resource-group myResourceGroup --sku B2 --is-linux
   ```

2. **Deploy with Git**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppPlan --name mySmartAssistant --runtime "PYTHON|3.9"
   git remote add azure <your-azure-git-url>
   git push azure main
   ```

3. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name mySmartAssistant --settings GROQ_API_KEY=your_key
   ```

### Deploy with Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000 8501
   CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py
   ```

2. **Build and Run**
   ```bash
   docker build -t smart-research-assistant .
   docker run -p 8000:8000 -p 8501:8501 -e GROQ_API_KEY=your_key smart-research-assistant
   ```

---

## 🔒 Security Considerations

⚠️ **Before Deployment:**
1. Keep API keys in environment variables (never hardcode)
2. Use HTTPS in production
3. Implement authentication for API endpoints
4. Validate user input
5. Rate limiting on API endpoints
6. Use secrets management (AWS Secrets Manager, Azure Key Vault)

---

## ⚠️ Common Issues

### Issue: API Connection Error
**Solution:** Make sure FastAPI is running on port 8000
```bash
uvicorn backend.main:app --reload
```

### Issue: GROQ API Error
**Solution:** Verify API key in .env file and ensure it's active

### Issue: ChromaDB Not Found
**Solution:** Create database directory
```bash
mkdir -p database/chroma_db
python load_sample_documents.py
```

### Issue: Port Already in Use
**Solution:** Change port in .env or kill process on that port
```bash
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

---

## 🚀 Future Enhancements

### Core Features to Add
- [ ] Multi-document search
- [ ] Hybrid search (semantic + keyword)
- [ ] Conversation memory between sessions
- [ ] User authentication and profiles
- [ ] Document metadata filtering
- [ ] Batch document processing

### Advanced Features
- [ ] Fine-tuning on domain-specific data
- [ ] Multiple LLM provider support
- [ ] Local LLM support (Ollama, LlamaIndex)
- [ ] Multi-language support
- [ ] Web scraping integration
- [ ] PDF table extraction
- [ ] Real-time document indexing
- [ ] Analytics dashboard

### Production Features
- [ ] Database backups and replication
- [ ] API rate limiting
- [ ] User authentication (OAuth2)
- [ ] Audit logging
- [ ] Cost tracking
- [ ] Performance monitoring
- [ ] CI/CD pipelines
- [ ] Load balancing

---

## 📊 Performance Tips

1. **Batch Uploads:** Upload multiple documents at once
2. **Increase Top-K:** Retrieve more documents if answers are incomplete
3. **Chunk Size:** Adjust CHUNK_SIZE based on document type
4. **Temperature:** Lower = more focused, Higher = more creative
5. **Caching:** Implement results caching for repeated queries

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📞 Support

- **Issues:** Create an issue in the repository
- **Email:** support@smartresearch.com
- **Documentation:** See inline code comments

---

## 🎯 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)

---

## ✨ Credits

**Built with:**
- Groq LLaMA 3.1
- LangChain
- ChromaDB
- Streamlit
- FastAPI
- Sentence Transformers

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** Production Ready ✅

---

Happy coding! 🚀
