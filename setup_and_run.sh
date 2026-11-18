#!/bin/bash
# Reel AI Video Editor - Setup & Launch (Mac/Linux)

echo ""
echo "============================================"
echo " REEL - AI Video Editor  |  Auto Setup"
echo "============================================"
echo ""

# ── Check Node.js ──
if ! command -v node &>/dev/null; then
    echo "[ERROR] Node.js is NOT installed!"
    echo "Install from: https://nodejs.org (download LTS)"
    exit 1
fi
echo "[OK] Node.js: $(node --version)"

# ── Check Python ──
PYTHON_CMD=""
if command -v python3 &>/dev/null; then PYTHON_CMD="python3"
elif command -v python &>/dev/null; then PYTHON_CMD="python"
else
    echo "[ERROR] Python is NOT installed!"
    echo "Install from: https://python.org"
    exit 1
fi
echo "[OK] Python: $($PYTHON_CMD --version)"

echo ""
echo "── Installing Frontend Dependencies ──────────────────"
if [ ! -d "node_modules" ]; then
    echo "Running: npm install (may take 2-3 minutes)..."
    npm install || { echo "[ERROR] npm install failed."; exit 1; }
    echo "[OK] Frontend dependencies installed!"
else
    echo "[OK] node_modules exists, skipping..."
fi

echo ""
echo "── Installing Backend Dependencies ───────────────────"
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi
source venv/bin/activate
echo "Installing Python packages (may take 3-5 minutes)..."
pip install -r requirements.txt -q || { echo "[ERROR] pip install failed."; exit 1; }
echo "[OK] Backend dependencies installed!"

# ── Create .env if missing ──
if [ ! -f ".env" ]; then
    echo ""
    echo "─────────────────────────────────────────────────────"
    echo " GEMINI API KEY (optional - for AI editing features)"
    echo " Get a free key: https://aistudio.google.com/apikey"
    echo "─────────────────────────────────────────────────────"
    read -p " Enter your Gemini API key (or press Enter to skip): " APIKEY
    if [ -n "$APIKEY" ]; then
        echo "GEMINI_API_KEY=$APIKEY" > .env
        echo "[OK] API key saved."
    else
        echo "GEMINI_API_KEY=DUMMY_KEY" > .env
        echo "[SKIPPED] AI features will use fallback mode."
    fi
fi

cd ..

echo ""
echo "============================================"
echo " Launching Reel..."
echo "============================================"
echo " Frontend: http://localhost:5173"
echo " Backend:  http://localhost:8000"
echo ""

# ── Launch Backend ──
osascript -e 'tell app "Terminal" to do script "cd \"'"$(pwd)/backend"'\" && source venv/bin/activate && python main.py"' 2>/dev/null || \
    (cd backend && source venv/bin/activate && python main.py &)

sleep 3

# ── Launch Frontend ──
osascript -e 'tell app "Terminal" to do script "cd \"'"$(pwd)"'\" && npm run dev"' 2>/dev/null || \
    (npm run dev &)

sleep 4

# ── Open browser ──
open http://localhost:5173 2>/dev/null || xdg-open http://localhost:5173 2>/dev/null

echo "Both servers are running! Open: http://localhost:5173"
