# AWS EC2 Deployment Guide

This project is now configured to run on AWS EC2 using environment variables for API endpoints and host configuration.

## 1. Launch EC2 Instance

- Use Ubuntu 22.04 LTS or similar.
- Open security group ports:
  - `22` for SSH
  - `8000` for FastAPI (backend)
  - `8501` for Streamlit (frontend)

> For a production setup, you can instead expose only `80`/`443` and use Nginx as a reverse proxy.

## 2. SSH into the Instance

```bash
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>
```

## 3. Install System Packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git build-essential
```

## 4. Clone the Repo

```bash
git clone <your-repo-url> app
cd app
```

## 5. Create Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set:

- `GROQ_API_KEY`
- `API_BASE_URL=http://<EC2_PUBLIC_IP>:8000`

If you want Streamlit to call the backend by public IP, use the EC2 public address.

## 7. Initialize Data (optional)

```bash
python load_sample_documents.py
```

## 8. Start Backend and Frontend

Start backend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Start frontend:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

## 9. Access the App

- Streamlit frontend: `http://<EC2_PUBLIC_IP>:8501`
- Backend health: `http://<EC2_PUBLIC_IP>:8000/health`

## 10. Recommended Production Improvements

- Use `tmux` or `screen` to keep processes running.
- Use `systemd` services for startup.
- Use Nginx to reverse proxy `8501` and `8000` behind `80`/`443`.
- Enable HTTPS with Certbot.
