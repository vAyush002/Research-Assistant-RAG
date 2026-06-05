@echo off
title Smart Research Assistant - Backend

cd /d "%~dp0"

call venv\Scripts\activate

echo Starting FastAPI Backend...
uvicorn main:app --reload

pause