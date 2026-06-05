# 🚀 Getting Started - Smart Research Assistant

**Welcome!** You have received a complete, production-ready AI Research Assistant. This guide will get you running in minutes.

---

## ⚡ 5-Minute Quick Start

### Step 1: Choose Your OS and Run Quick Start

**Windows:**
```
Double-click: quick_start.bat
```

**macOS/Linux:**
```bash
bash quick_start.sh
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Load sample documents
- ✅ Start both frontend and backend

### Step 2: Open Your Browser
- **Frontend (UI):** http://localhost:8501
- **API:** http://localhost:8000

### Step 3: Try It Out!
1. Go to http://localhost:8501
2. Upload a PDF/TXT file (or use sample documents already loaded)
3. Type a question
4. Get an AI-powered answer!

**That's it! 🎉**

---

## 📁 What You Have

A complete AI system with:
- **Groq LLaMA 3.1** - Latest, fastest LLM
- **ChromaDB** - Vector database for semantic search
- **FastAPI** - High-performance backend
- **Streamlit** - Beautiful modern UI
- **LangChain** - RAG framework

---

## 🗂️ File Structure

```
Smart_Research_Assistant/
├── app.py                    ← Main application file
├── requirements.txt          ← Python dependencies
├── .env                      ← Configuration (API key)
├── README.md                 ← Full documentation
├── SETUP_GUIDE.md           ← Detailed setup instructions
├── FILE_REFERENCE.md        ← What each file does
│
├── backend/                  ← FastAPI backend
│   ├── main.py              ← API server
│   ├── rag_pipeline.py      ← RAG implementation
│   ├── vector_store.py      ← Database
│   ├── embeddings.py        ← Embeddings
│   ├── preprocessing.py     ← Text processing
│   └── utils.py             ← Utilities
│
├── frontend/                 ← Streamlit UI
│   └── streamlit_app.py     ← Complete interface
│
└── data/articles/           ← Sample documents
    ├── machine_learning_guide.txt
    ├── deep_learning_neural_networks.txt
    └── nlp_fundamentals.txt
```

---

## 🎯 Common Tasks

### Task 1: First Time Setup

**Windows:**
```bash
quick_start.bat
```

**macOS/Linux:**
```bash
chmod +x quick_start.sh
./quick_start.sh
```

### Task 2: Run Backend Only

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start FastAPI
uvicorn backend.main:app --reload
```

Accessible at: http://localhost:8000

### Task 3: Run Frontend Only

```bash
# Activate virtual environment first
streamlit run frontend/streamlit_app.py
```

Accessible at: http://localhost:8501

### Task 4: Upload Your Documents

1. Go to http://localhost:8501
2. Click "Upload Documents" in the sidebar
3. Select PDF or TXT files
4. Wait for processing
5. Start asking questions!

### Task 5: Query via API

```python
import requests

# Query
response = requests.post(
    'http://localhost:8000/query',
    json={'question': 'What is machine learning?'}
)

print(response.json()['answer'])
```

### Task 6: Deploy to AWS

See `deploy_aws.sh` and `README.md` for full instructions.

```bash
bash deploy_aws.sh
```

### Task 7: Run with Docker

```bash
docker-compose up
```

---

## 🔑 API Key Setup

Your API key is already in `.env`:
```env
GROQ_API_KEY="key"
```

The API key is **already configured** - you can start using it immediately!

To change it later:
1. Edit `.env` file
2. Restart the application

---

## 🎓 Learning Resources

- **README.md** - Complete documentation
- **SETUP_GUIDE.md** - Detailed OS-specific setup
- **FILE_REFERENCE.md** - Explanation of each file
- **Code comments** - Implementation details

---

## ⚠️ Troubleshooting

### Issue: "Port 8000 already in use"
**Solution:** Kill the existing process
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Issue: "API connection error"
**Solution:** Make sure FastAPI is running
```bash
uvicorn backend.main:app --reload
```

### Issue: "API key not working"
**Solution:** Verify API key in `.env` file

For more help, see **SETUP_GUIDE.md**

---

## 🚀 What's Included

### Frontend (Streamlit)
✅ Upload documents  
✅ Ask questions  
✅ View answers with sources  
✅ Chat history  
✅ Database management  

### Backend (FastAPI)
✅ REST API  
✅ Document processing  
✅ Vector search  
✅ LLM integration  
✅ Comprehensive logging  

### Database (ChromaDB)
✅ Vector storage  
✅ Semantic search  
✅ Metadata management  
✅ Persistent storage  

### Documentation
✅ README.md  
✅ SETUP_GUIDE.md  
✅ FILE_REFERENCE.md  
✅ API docs (http://localhost:8000/docs)  

### Deployment
✅ Docker support  
✅ AWS EC2 deployment  
✅ Azure deployment  
✅ Environment configuration  

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────┐
│            User Browser (Port 8501)             │
│          Streamlit Frontend - Beautiful UI       │
└──────────────────────┬──────────────────────────┘
                       │
                       │ HTTP/REST
                       ▼
┌─────────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)             │
│  • Document Upload      • Query Processing      │
│  • RAG Pipeline         • Error Handling        │
└──────────┬─────────────────────────┬────────────┘
           │                         │
           ▼                         ▼
┌──────────────────┐      ┌────────────────────┐
│   ChromaDB       │      │  Groq LLaMA 3.1    │
│  Vector Search   │      │  Language Model    │
│ (Local Storage)  │      │   (Cloud API)      │
└──────────────────┘      └────────────────────┘
```

---

## 📈 Next Steps

### Immediate (Now)
1. ✅ Run quick start script
2. ✅ Open Streamlit UI
3. ✅ Upload test documents
4. ✅ Ask questions

### This Week
1. Deploy to AWS EC2 (see `deploy_aws.sh`)
2. Customize UI (edit `frontend/streamlit_app.py`)
3. Upload your own documents
4. Test with more complex queries

### This Month
1. Add authentication
2. Set up monitoring
3. Deploy to production
4. Add to portfolio

---

## 🎯 Key Commands Reference

```bash
# Setup
python -m venv venv                    # Create env
venv\Scripts\activate                  # Windows activate
source venv/bin/activate               # macOS/Linux activate
pip install -r requirements.txt        # Install deps

# Run
python app.py                          # Run both frontend+backend
uvicorn backend.main:app --reload      # Backend only
streamlit run frontend/streamlit_app.py # Frontend only

# Data
python load_sample_documents.py        # Load samples

# Deployment
docker-compose up                      # Docker
bash deploy_aws.sh                     # AWS
```

---

## 🔧 Configuration

All configuration is in `.env`:

```env
# API
GROQ_API_KEY=your_key_here
LLM_MODEL=llama-3.1-70b-versatile

# Database
CHROMA_DB_PATH=database/chroma_db
TOP_K_DOCUMENTS=3

# Performance
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TEMPERATURE=0.7

# Server
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

---

## 📚 Sample Documents

Three sample documents are included:

1. **Machine Learning Guide** - ML fundamentals
2. **Deep Learning** - Neural networks and transformers
3. **NLP Fundamentals** - Natural language processing

They're automatically loaded with `python load_sample_documents.py`

---

## 💡 Usage Tips

1. **Upload PDFs and TXT files** - Automatically extracted
2. **Ask natural language questions** - No special syntax needed
3. **Check sources** - See which documents were used
4. **Similarity scores** - Understand relevance
5. **Clear database** - Start fresh anytime
6. **Chat history** - View previous conversations

---

## 🌟 Features Showcase

### Modern UI
- Clean, professional design
- Real-time interactions
- Responsive layout
- Beautiful formatting

### Powerful RAG
- Semantic search
- Context-aware answers
- Source attribution
- Similarity scoring

### Production Ready
- Error handling
- Logging system
- Input validation
- CORS support

### Easy Deployment
- Docker support
- Cloud ready
- Environment config
- One-click setup

---

## 📞 Getting Help

**For setup issues:**
- See `SETUP_GUIDE.md`
- Check logs in `logs/app.log`

**For API questions:**
- See `README.md`
- Visit API docs at `http://localhost:8000/docs`

**For file information:**
- See `FILE_REFERENCE.md`

**For deployment:**
- See `deploy_aws.sh`
- See deployment section in `README.md`

---

## ✨ What's Special About This

1. **Complete** - Everything you need, nothing you don't
2. **Production Ready** - Error handling, logging, configuration
3. **Well Documented** - Multiple guides, code comments, API docs
4. **Modern Stack** - Latest LLMs, frameworks, and tools
5. **Easy to Deploy** - Local, Docker, AWS, Azure support
6. **Portfolio Ready** - Showcase full-stack AI skills

---

## 🎉 You're Ready!

Everything is set up and ready to go:

```
✅ Backend API        - Groq LLaMA 3.1
✅ Frontend UI        - Streamlit
✅ Vector Database    - ChromaDB
✅ Sample Data        - Ready to load
✅ Documentation      - Complete
✅ Deployment Files   - Ready
✅ API Key            - Configured
```

**Start with:** `quick_start.bat` (Windows) or `bash quick_start.sh` (macOS/Linux)

**Then open:** http://localhost:8501

---

## 📖 Documentation Map

```
START HERE
    ↓
    └─→ This File (Quick start)
        ├─→ README.md (Full documentation)
        ├─→ SETUP_GUIDE.md (Detailed setup)
        ├─→ FILE_REFERENCE.md (File explanations)
        └─→ Code Comments (Implementation details)
```

---

## 🚀 Ready to Launch?

1. Run the quick start script
2. Open the UI
3. Upload documents
4. Ask questions
5. Deploy to cloud
6. Show off to employers!

**Happy building! 🎉**

---

**Questions?** Check the relevant documentation file above.  
**Need help?** See SETUP_GUIDE.md for detailed instructions.  
**Ready to deploy?** See deploy_aws.sh or docker-compose.yml.

---

**Version:** 1.0  
**Status:** Ready to Use ✅  
**Last Updated:** 2024
