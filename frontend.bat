@echo off
title Smart Research Assistant - Frontend

cd /d "%~dp0"

call venv\Scripts\activate

echo Starting Streamlit Frontend...
streamlit run streamlit_app.py

pause