@echo off
title Smart Research Assistant

cd /d "%~dp0"
call venv\Scripts\activate

echo Starting Smart Research Assistant...
streamlit run streamlit_app.py

pause
