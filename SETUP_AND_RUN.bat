@echo off
title Reel AI Video Editor - Setup & Launch
color 0A
echo.
echo  ============================================
echo   REEL - AI Video Editor  ^|  Auto Setup
echo  ============================================
echo.

:: ── Check Node.js ──
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo  [ERROR] Node.js is NOT installed!
    echo.
    echo  Please install Node.js from: https://nodejs.org
    echo  Download the LTS version and re-run this file.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo  [OK] Node.js found: %NODE_VER%

:: ── Check Python ──
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo  [ERROR] Python is NOT installed!
    echo.
    echo  Please install Python from: https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
echo  [OK] Python found: %PY_VER%

echo.
echo  ── Installing Frontend Dependencies ──────────────────
if not exist "node_modules" (
    echo  Running: npm install  (this may take 2-3 minutes...)
    npm install
    if %errorlevel% neq 0 (
        echo  [ERROR] npm install failed. Check your internet connection.
        pause
        exit /b 1
    )
    echo  [OK] Frontend dependencies installed!
) else (
    echo  [OK] node_modules already exists, skipping...
)

echo.
echo  ── Installing Backend Dependencies ───────────────────
cd backend
if not exist "venv" (
    echo  Creating Python virtual environment...
    python -m venv venv
)
echo  Installing Python packages (this may take 3-5 minutes)...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo  [ERROR] pip install failed. Check your internet connection.
    pause
    exit /b 1
)
echo  [OK] Backend dependencies installed!

:: ── Create .env if missing ──
if not exist ".env" (
    echo.
    echo  ─────────────────────────────────────────────────────
    echo   GEMINI API KEY REQUIRED
    echo  ─────────────────────────────────────────────────────
    echo.
    echo  To use the AI editing features, you need a free
    echo  Gemini API key from: https://aistudio.google.com/apikey
    echo.
    set /p APIKEY=" Enter your Gemini API key (or press Enter to skip): "
    if not "!APIKEY!"=="" (
        echo GEMINI_API_KEY=!APIKEY!> .env
        echo  [OK] API key saved to backend\.env
    ) else (
        echo GEMINI_API_KEY=DUMMY_KEY> .env
        echo  [SKIPPED] Using dummy key - AI features will use fallback mode.
    )
)

cd ..

echo.
echo  ============================================
echo   Setup Complete! Launching...
echo  ============================================
echo.
echo  - Frontend will open at: http://localhost:5173
echo  - Backend API running at: http://localhost:8000
echo.
echo  Close this window to stop both servers.
echo.

:: ── Launch Backend in a new window ──
start "Reel Backend (Python)" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate.bat && echo Backend starting... && python main.py"

:: ── Wait 3s for backend to start ──
timeout /t 3 /nobreak >nul

:: ── Launch Frontend ──
start "Reel Frontend (Vite)" cmd /k "cd /d "%~dp0" && echo Frontend starting... && npm run dev"

:: ── Wait 4s then open browser ──
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo  Both servers are running!
echo  Press any key to close this launcher (servers keep running).
pause >nul
