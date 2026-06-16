# AWS EC2 Deployment Guide

The app runs as a single Streamlit process. API keys are entered in the sidebar at
runtime, so no secrets need to live on the server.

## 1. Launch an EC2 instance

- Ubuntu 22.04 LTS (or similar).
- Open security-group ports:
  - `22` — SSH
  - `8501` — Streamlit
  - `8000` — only if you also run the optional FastAPI backend

> For production, prefer exposing only `80`/`443` behind Nginx as a reverse proxy.

## 2. SSH in

```bash
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>
```

## 3. Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git build-essential
```

## 4. Clone and set up

```bash
git clone <your-repo-url> app && cd app
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. (Optional) Pre-load documents

```bash
mkdir -p data && cp /path/to/your/docs/*.pdf data/
python load_sample_documents.py data
```

## 6. Run the app

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

Open `http://<EC2_PUBLIC_IP>:8501`, then enter your provider API key in the sidebar.

## 7. (Optional) Run the FastAPI backend

```bash
cp .env.example .env        # set GROQ_API_KEY
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 8. Production recommendations

- Use a `systemd` service (or `tmux`/`screen`) to keep the process running.
- Put Nginx in front of `8501` and enable HTTPS with Certbot.
- Keep API keys out of the server — the sidebar entry is per-session and safest.
