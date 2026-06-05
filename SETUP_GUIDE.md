# Setup Guide: Smart Research Assistant

This guide provides step-by-step instructions for setting up the Smart Research Assistant on different operating systems.

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB (for models and database)
- **Internet:** Required for Groq API
- **OS:** Windows, macOS, or Linux

---

## Prerequisites

### 1. Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (you'll need it in Step 3)

### 2. Install Python

**Windows:**
- Download from [python.org](https://www.python.org)
- Run installer, check "Add Python to PATH"
- Verify: `python --version`

**macOS:**
```bash
brew install python@3.9
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

---

## Installation Instructions

### Windows

#### Step 1: Open Command Prompt or PowerShell

Press `Win + R`, type `cmd`, press Enter

#### Step 2: Navigate to Project Directory

```cmd
cd C:\path\to\Smart_Research_Assistant
```

#### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

#### Step 4: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of the command line.

#### Step 5: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

#### Step 6: Install Dependencies

```cmd
pip install -r requirements.txt
```

#### Step 7: Configure API Key

1. Open `.env` file in Notepad
2. Replace `your_groq_api_key_here` with your actual API key
3. Save the file

#### Step 8: Load Sample Documents

```cmd
python load_sample_documents.py
```

Wait for the process to complete.

#### Step 9: Run the Application

**Option A: Run everything together**
```cmd
python app.py
```

**Option B: Run separately**

Terminal 1 - FastAPI Backend:
```cmd
uvicorn backend.main:app --reload
```

Terminal 2 - Streamlit Frontend (new command prompt):
```cmd
streamlit run frontend/streamlit_app.py
```

#### Step 10: Access the Application

- Frontend: Open browser and go to `http://localhost:8501`
- API: Open browser and go to `http://localhost:8000`

---

### macOS

#### Step 1: Open Terminal

Press `Cmd + Space`, type `terminal`, press Enter

#### Step 2: Navigate to Project Directory

```bash
cd ~/path/to/Smart_Research_Assistant
```

#### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

#### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` at the start of the prompt.

#### Step 5: Upgrade pip

```bash
pip install --upgrade pip
```

#### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 7: Configure API Key

```bash
nano .env
```

Replace the placeholder with your API key, then press `Ctrl + X`, `Y`, `Enter` to save.

#### Step 8: Load Sample Documents

```bash
python load_sample_documents.py
```

#### Step 9: Run the Application

**Option A: Run everything together**
```bash
python app.py
```

**Option B: Run separately**

Terminal 1 - FastAPI Backend:
```bash
uvicorn backend.main:app --reload
```

Terminal 2 - Streamlit Frontend (new terminal):
```bash
streamlit run frontend/streamlit_app.py
```

#### Step 10: Access the Application

- Frontend: Open browser and go to `http://localhost:8501`
- API: Open browser and go to `http://localhost:8000`

---

### Linux (Ubuntu/Debian)

#### Step 1: Open Terminal

Press `Ctrl + Alt + T`

#### Step 2: Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-dev build-essential
```

#### Step 3: Navigate to Project Directory

```bash
cd ~/path/to/Smart_Research_Assistant
```

#### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
```

#### Step 5: Activate Virtual Environment

```bash
source venv/bin/activate
```

#### Step 6: Upgrade pip

```bash
pip install --upgrade pip
```

#### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 8: Configure API Key

```bash
nano .env
```

Replace the placeholder with your API key, press `Ctrl + X`, `Y`, `Enter` to save.

#### Step 9: Load Sample Documents

```bash
python load_sample_documents.py
```

#### Step 10: Run the Application

**Option A: Run everything together**
```bash
python app.py
```

**Option B: Run separately**

Terminal 1 - FastAPI Backend:
```bash
uvicorn backend.main:app --reload
```

Terminal 2 - Streamlit Frontend (new terminal):
```bash
streamlit run frontend/streamlit_app.py
```

#### Step 11: Access the Application

- Frontend: Open browser and go to `http://localhost:8501`
- API: Open browser and go to `http://localhost:8000`

---

## Troubleshooting

### Issue: "Command not found: python"
**Solution:** Use `python3` instead or add Python to PATH

### Issue: "Permission denied" on Linux/Mac
**Solution:** Run `chmod +x deploy_aws.sh` before executing

### Issue: "Module not found" errors
**Solution:** Make sure virtual environment is activated
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Issue: Port already in use
**Solution A:** Kill the process on that port
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Solution B:** Change port in `.env` file

### Issue: API Key not working
**Solution:**
1. Verify API key from [console.groq.com](https://console.groq.com)
2. Check `.env` file has correct key (no extra spaces)
3. Restart the application

### Issue: Out of memory
**Solution:** Reduce `TOP_K_DOCUMENTS` in `.env` or close other applications

---

## Useful Commands

### Check if ports are available
```bash
# Windows
netstat -ano

# Linux/Mac
lsof -i -P -n | grep LISTEN
```

### View application logs
```bash
tail -f logs/app.log
```

### Clear database
```bash
rm -rf database/chroma_db
```

### Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Deactivate virtual environment
```bash
deactivate
```

---

## Next Steps

1. ✅ Application is running
2. Upload test documents or use sample documents
3. Ask questions about your documents
4. Check logs in `logs/app.log` if there are issues
5. Deploy to cloud (see main README.md for instructions)

---

## Getting Help

- Check logs: `logs/app.log`
- API docs: `http://localhost:8000/docs`
- Streamlit help: `streamlit help`
- Contact support or create an issue

---

**Happy exploring!** 🚀
