@echo off
setlocal enabledelayedexpansion
title Vibe-Cuts — AI Video Editor Launcher
color 0b

echo =========================================================
echo             VIBE-CUTS  AI VIDEO EDITOR
echo =========================================================
echo.

:: Change directory to script's own folder
cd /d "%~dp0"

:: 1. Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js is not found on your system!
    echo Please download and install Node.js (LTS version) from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

:: 2. Check Python (optional for backend, but recommended)
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Python not found in PATH.
    echo Backend Agentic Edit will be disabled, but in-browser editing will work!
    echo.
)

:: 3. Check node_modules
if not exist "node_modules\" (
    echo [SETUP] Installing frontend dependencies (one-time setup)...
    call npm install
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] npm install failed. Please check your internet connection.
        pause
        exit /b 1
    )
    echo.
)

:: 4. Start Backend Server
echo [1/3] Starting Backend API Server (port 8000)...
if exist "backend\venv\Scripts\python.exe" (
    start "Vibe-Cuts Backend" /min cmd /c "cd /d "%~dp0backend" && .\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        start "Vibe-Cuts Backend" /min cmd /c "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000"
    ) else (
        echo [INFO] Skipping backend server (Python not found).
    )
)

:: 5. Start Frontend Dev Server
echo [2/3] Starting Frontend Dev Server (port 5173)...
start "Vibe-Cuts Frontend" /min cmd /c "cd /d "%~dp0" && npm run dev"

:: 6. Wait for servers to spin up and open browser
echo [3/3] Opening browser at http://localhost:5173 ...
timeout /t 3 /nobreak >nul

start http://localhost:5173

echo.
echo =========================================================
echo     Vibe-Cuts is now RUNNING!
echo     UI:      http://localhost:5173
echo     Backend: http://127.0.0.1:8000
echo =========================================================
echo.
echo NOTE: Keep this window open while using the app.
echo Press any key when you want to stop all servers and exit...
echo.
pause >nul

echo Stopping Vibe-Cuts servers...
taskkill /FI "WINDOWTITLE eq Vibe-Cuts Frontend*" /F /T >nul 2>&1
taskkill /FI "WINDOWTITLE eq Vibe-Cuts Backend*" /F /T >nul 2>&1
echo Done! Goodbye.
timeout /t 2 >nul
exit /b 0
