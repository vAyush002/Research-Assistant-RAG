@echo off
title Smart Research Assistant

start cmd /k backend.bat
timeout /t 5 >nul
start cmd /k frontend.bat