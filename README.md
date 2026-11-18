# 🎬 Reel — AI Video Editor

An AI-powered video editor that auto-generates highlight reels with cinematic effects, beat sync, captions, and a 4-pillar agentic editing pipeline.

---

## ⚡ Quick Start (One Click)

### Windows
1. Unzip the folder
2. Double-click **`SETUP_AND_RUN.bat`**
3. Wait for setup to finish (3–5 mins first time)
4. Browser opens automatically at `http://localhost:5173`

### Mac / Linux
1. Unzip the folder
2. Open Terminal in the folder
3. Run:
```bash
chmod +x setup_and_run.sh && ./setup_and_run.sh
```
4. Browser opens at `http://localhost:5173`

---

## 📋 Requirements

You need these installed before running:

| Tool | Version | Download |
|------|---------|----------|
| **Node.js** | v18+ (LTS) | https://nodejs.org |
| **Python** | v3.9+ | https://python.org |
| **FFmpeg** | Any recent | https://ffmpeg.org/download.html |

> ⚠️ **FFmpeg** must be available in your system PATH for the backend AI pipeline to work.

---

## 🤖 AI Features (Optional)

For the **Gemini AI editing** features, get a free API key:
1. Go to https://aistudio.google.com/apikey
2. Create a key (free tier works)
3. The setup script will ask you to paste it, OR create `backend/.env`:
```
GEMINI_API_KEY=your_key_here
```

Without the key, the app still works — it uses a smart fallback algorithm for highlight detection.

---

## 🏗️ Manual Setup (if scripts don't work)

```bash
# Terminal 1 — Frontend
npm install
npm run dev

# Terminal 2 — Backend
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

---

## 🎯 Features

- 🎬 **Auto Highlight Detection** — AI finds the best moments
- 🥁 **Beat Sync** — Cuts synced to your BGM's beats
- 🎨 **Cinematic Mode** — CapCut-style VFX (zoom, color grade)
- 🖼️ **Aspect Ratios** — 16:9, 9:16, 1:1, 4:5
- 🎚️ **Color Adjustments** — Exposure, Contrast, Saturation
- 🤖 **Agentic Edit** — 4-pillar AI pipeline (requires Python backend + Gemini key)
- 📝 **Kinetic Captions** — Auto-generated animated subtitles

---

## 📁 Project Structure

```
reel/
├── src/                    # React + TypeScript frontend
│   ├── components/         # UI components
│   ├── lib/                # FFmpeg WASM + audio analysis
│   └── types.ts            # Shared types
├── backend/                # FastAPI Python backend
│   ├── main.py             # API server
│   ├── agent.py            # Gemini AI plan generator
│   ├── agentic_processor.py# Execution engine
│   ├── director.py         # Audio-synced FFmpeg filters
│   ├── vision.py           # Face tracking + scene detection
│   └── requirements.txt    # Python dependencies
├── SETUP_AND_RUN.bat       # Windows one-click launcher
└── setup_and_run.sh        # Mac/Linux launcher
```
