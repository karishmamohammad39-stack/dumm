@echo off
title Vibe-Cuts AI Server
echo ==========================================
echo        ✨ Starting Vibe-Cuts ✨
echo ==========================================
echo.
echo Initializing Python AI Backend...

cd backend

:: Wait 3 seconds, then open the default web browser
start cmd /c "timeout /t 3 >nul && start http://localhost:8000"

:: Activate virtual environment and start the FastAPI server
call venv\Scripts\activate.bat
python -m uvicorn main:app --host 0.0.0.0 --port 8000
