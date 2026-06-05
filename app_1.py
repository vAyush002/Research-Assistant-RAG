import subprocess
import os
import sys
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_environment():
    """Load environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded")


def start_backend():
    """Start FastAPI backend server"""
    logger.info("Starting FastAPI backend server...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("FastAPI server started (PID: {})".format(process.pid))
        return process
    except Exception as e:
        logger.error(f"Failed to start FastAPI server: {str(e)}")
        return None


def start_frontend():
    """Start Streamlit frontend"""
    logger.info("Starting Streamlit frontend...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/streamlit_app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("Streamlit app started (PID: {})".format(process.pid))
        return process
    except Exception as e:
        logger.error(f"Failed to start Streamlit: {str(e)}")
        return None


def main():
    """Main function"""
    logger.info("=" * 50)
    logger.info("Smart Research Assistant")
    logger.info("=" * 50)
    
    # Load environment
    load_environment()
    
    # Start backend
    backend_process = start_backend()
    time.sleep(3)  # Wait for backend to start
    
    # Start frontend
    frontend_process = start_frontend()
    
    logger.info("\n" + "=" * 50)
    logger.info("Application started!")
    logger.info("Backend: http://localhost:8000")
    logger.info("Frontend: http://localhost:8501")
    logger.info("=" * 50 + "\n")
    
    try:
        # Keep processes running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        logger.info("Application stopped")


if __name__ == "__main__":
    main()
