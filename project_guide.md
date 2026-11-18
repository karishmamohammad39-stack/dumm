# Vibe-Cuts (Reel) - Complete Project Guide

## 1. Project Overview
**Vibe-Cuts** (also referred to as "Reel") is an advanced, automated video editing web application. It acts as an AI Director, automatically taking long raw videos and turning them into highly engaging, fast-paced, "CapCut-style" cinematic highlight reels. It syncs video cuts and visual effects (VFX) directly to the beats of a background music track. 

The project operates in two parts:
1. A **Frontend Web Application** that can process video entirely in the browser using WebAssembly.
2. An optional **Python Backend** that provides advanced AI transcription (speech-to-text) to burn subtitles into the video.

## 2. Everything Included (Core Features)
- **Automatic Beat Detection:** Analyzes any uploaded music track and finds the drop/beat points.
- **Magic Cuts (Auto-Highlight):** Automatically selects interesting parts of a long video and aligns them perfectly with the music beats.
- **Cinematic VFX (Visual Effects):** Automatically applies professional color grading, film grain, smooth "punch-in" zooms, flashbangs, and chromatic aberration (RGB split glitches).
- **Hype Text Generation:** Pops up engaging words like "EPIC", "WAIT!", and "MIND BLOWN" exactly on the beat drops.
- **AI Transcription & Subtitles:** Uses OpenAI's Whisper model to automatically transcribe the video's audio and burn the captions onto the screen.
- **In-Browser Processing:** Edits and renders the final video directly inside the user's browser for high privacy and zero server costs.

## 3. Project Implementation details
The project uses a **Client-Server architecture**, but heavily relies on the client (frontend) to do the heavy lifting of video processing to save server costs.

### A. Frontend (React + TypeScript + Vite)
The user interface is built using React. 
- **Audio Analysis (`audioAnalysis.ts`):** Uses the browser's native `Web Audio API`. It applies a "lowpass filter" to isolate the bass (kick drum) frequencies of a song. It then scans the audio waveform for volume peaks to identify exact timestamps for the beats.
- **Video Processing (`ffmpeg.ts`):** Uses `@ffmpeg/ffmpeg` (FFmpeg compiled to WebAssembly) to edit video directly in the browser. 
  - **Pass 1:** It cuts the video into smaller clips and applies a smooth zoom effect (`zoompan`).
  - **Pass 2:** It merges the clips, adds the background music, applies a cinematic color grade (increased contrast and saturation), and adds timeline-based visual effects (like screen flashes and glitched text) perfectly timed to the beat timestamps found earlier.

### B. Backend (Python + FastAPI)
The backend acts as a microservice for AI transcription and advanced server-side rendering.
- **FastAPI (`main.py`):** Provides API endpoints like `/upload` and `/transcribe`.
- **Whisper AI (`processor.py`):** Uses the `whisper` library (by OpenAI) to listen to the video's audio and convert it to text. It generates an `.srt` subtitle file.
- **Python FFmpeg (`director.py`):** Uses `ffmpeg-python` to apply server-side video filters. It uses the `librosa` library to detect audio tempo (BPM) and beats. If the tempo is high (fast song), it adds aggressive styling like chromatic aberration (splitting red, green, blue colors). Finally, it burns the generated subtitles directly onto the video frames.

## 4. Technologies, Languages, and Algorithms Used

### Languages
- **TypeScript & JavaScript:** Used for building the React frontend, handling UI logic, and orchestrating in-browser video processing.
- **Python:** Used on the backend for heavy AI tasks (speech recognition and advanced audio analysis).
- **HTML & CSS:** Standard web markup and styling for the user interface.

### Libraries & Frameworks
- **React & Vite:** For building a fast, component-based frontend UI.
- **FastAPI:** A high-performance Python framework used to create the backend API.
- **FFmpeg (WASM & Python):** The core video processing library. `@ffmpeg/ffmpeg` (WASM) is used on the frontend for browser-based editing, while `ffmpeg-python` handles backend rendering.
- **OpenAI Whisper:** An advanced Machine Learning library used to transcribe video audio into text (subtitles).
- **Librosa:** A Python library used for music and audio analysis (specifically beat tracking and tempo detection).

### Algorithms
- **Peak Detection Algorithm (Frontend):** 
  - **Process:** The audio signal is passed through a Lowpass Biquad Filter to isolate bass frequencies (like a kick drum). The algorithm then scans chunks of the audio waveform (e.g., every 0.5 seconds).
  - **Logic:** It finds the maximum amplitude (volume) in each chunk. If this amplitude crosses a specific threshold, it registers that exact timestamp as a "beat".
- **Dynamic Programming / Beat Tracking (Librosa Backend):**
  - Uses librosa's built-in beat tracker, which estimates the global tempo (BPM) and then uses dynamic programming to find an optimal sequence of beat events that align with the audio's onset strength envelope.
- **Filter Graph Construction Algorithm:**
  - A procedural algorithm that takes the array of beat timestamps and programmatically builds a complex FFmpeg string (`filter_complex`). It constructs math expressions (like `between(t, start, end)`) to apply specific visual effects (flashes, glitched text, chromatic aberration) exactly when beats occur.

## 5. Pin-to-Pin Component Explanation

### Frontend Components (`src/`)
- **`App.tsx` (Main Controller):** The heart of the application. It manages the state for video/audio files, handles the automatic pipeline (analysis -> clip generation -> export), and coordinates all other UI components.
- **`lib/audioAnalysis.ts` (Beat Engine):** Uses the browser's `OfflineAudioContext`. It creates a Lowpass Biquad Filter to isolate bass frequencies from the uploaded music, then iterates through chunks of the audio to find amplitude peaks. It returns an array of timestamps where the beats drop.
- **`lib/ffmpeg.ts` (Video Renderer):** The core editing engine running in the browser. 
  - **Pass 1:** It uses the `WORKERFS` file system to directly read the user's video without consuming massive RAM. It cuts the video at the calculated timestamps and applies a `zoompan` filter to create a punch-in effect.
  - **Pass 2:** It stitches the cuts together, adds the background music, and dynamically generates a `filter_complex` string to apply contrast, saturation, vignette, flashing lights, and hype text specifically triggered at the beat timestamps.
- **UI Components:**
  - `Header.tsx`: Contains the main "Export" button and progress bar.
  - `Sidebar.tsx`: Handles file uploads for Video and BGM.
  - `VideoPlayer.tsx`: A custom HTML5 video player with keyboard shortcuts (Space, J, L, M) for playback and seeking.
  - `Timeline.tsx`: Displays the generated clips visually on a track, allowing users to see exactly where cuts happen and delete unwanted clips.
  - `ToolsPanel.tsx`: Houses the AI prompt processor and the manual toggle for "Cinematic Mode".
  - `PipelineStatus.tsx`: A floating toast notification that keeps the user updated on what the AI is currently doing (e.g., "Analyzing beats...", "Loading encoder...").

### Backend Components (`backend/`)
- **`main.py` (API Gateway):** A FastAPI server providing `/upload` and `/transcribe` endpoints. It receives files, saves them to a temporary directory, delegates work to the processor, and manages cleanup using BackgroundTasks.
- **`processor.py` (AI Transcription):** Loads the OpenAI Whisper Machine Learning model into memory. When a video is received, it extracts the audio, runs Whisper to convert speech into text, and generates a formatted `.srt` subtitle file.
- **`director.py` (Server-side VFX):** An alternative rendering engine. It uses `librosa` to analyze the audio's BPM (Beats Per Minute). If the BPM is greater than 120 (a high-energy track), it builds a complex FFmpeg graph to apply heavy chromatic aberration (RGB splitting and shaking). Finally, it uses a subprocess to run the system's FFmpeg tool to burn the generated subtitles permanently onto the video frames.

## 6. Project Guide: How to Use the Project
1. **Start the application:** Open the web interface in your browser.
2. **Upload Media:** Use the sidebar to upload a raw Video and an Audio track (BGM).
3. **Wait for Analysis:** The app will automatically analyze the audio track to find its beats. 
4. **Cinematic Mode:** Ensure "Cinematic Mode" is toggled on to get the cool CapCut-style effects.
5. **Generate & Export:** The app automatically generates highlight clips. Click "Export" to let the in-browser FFmpeg engine render your video. It will automatically download a file named `TRUE_CAPCUT_EDIT.mp4` when finished.

---

## 7. Viva Questions and Answers

**Q1: What is the main goal of this project?**
**Ans:** The main goal is to fully automate the video editing process by creating high-energy, cinematic highlight reels that are automatically synced to the beats of a music track, similar to popular TikTok or CapCut edits.

**Q2: How does the application detect beats in the music?**
**Ans:** On the frontend, it uses the Web Audio API to apply a lowpass filter (which isolates bass/kick drums) and then scans the audio data for volume peaks. On the backend, it uses a Python library called `librosa` to analyze the audio waveform and tempo.

**Q3: How is video edited directly in the browser without a backend server?**
**Ans:** It uses FFmpeg WebAssembly (WASM). FFmpeg is a powerful C-based video editing tool that has been compiled to run directly inside modern web browsers. It mounts the uploaded files to a virtual file system and runs command-line video filters.

**Q4: What is the role of the Python backend in this project?**
**Ans:** The backend provides heavy AI processing that browsers cannot easily handle. Specifically, it uses OpenAI's Whisper model to transcribe speech to text and burn accurate subtitles onto the video.

**Q5: What is "Cinematic Mode" and how is it implemented?**
**Ans:** Cinematic Mode is a feature that applies visual effects. It is implemented by generating complex FFmpeg filter strings (called a `filter_complex`). It dynamically adds instructions to crop the video to 9:16 portrait, increase contrast/saturation, and trigger screen flashes and text overlays specifically at the timestamps where beats were detected.

**Q6: What technologies were used in the Frontend?**
**Ans:** React for the UI, TypeScript for type safety, Vite for fast building, Web Audio API for beat detection, and FFmpeg WASM for video rendering.

**Q7: How did you solve the memory limitation issues of processing video in the browser?**
**Ans:** The project uses native File mounting (WORKERFS) in FFmpeg WASM. This allows FFmpeg to stream the video directly from the user's hard drive (zero-copy) instead of loading the entire massive video file into the browser's limited RAM.

---

## 8. IEEE Foundational Base Papers

To further understand the academic and technical foundation of this project, you can refer to these highly cited, foundational research papers published exclusively in **IEEE** conferences and journals:

**1. Automated Music Video Generation (The Core Concept)**
- **Title:** [*Automated Music Video Generation using WEB Image Resource*](https://doi.org/10.1109/ICASSP.2007.366341)
- **Authors:** Rui Cai, Lei Zhang, Feng Jing, Wei Lai, and Wei-Ying Ma
- **Published:** 2007 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)
- **Relevance:** This is a foundational IEEE paper that outlines a prototype for performing music segmentation based on beat detection, followed by concatenating visual segments to align with the musical rhythm.

**2. Beat Tracking & Audio Analysis (The Math Behind the Beats)**
- **Title:** [*Context-Dependent Beat Tracking of Musical Audio*](https://doi.org/10.1109/TASL.2006.885257)
- **Authors:** Matthew E. P. Davies and Mark D. Plumbley
- **Published:** IEEE Transactions on Audio, Speech, and Language Processing (Volume 15, Issue 3, 2007)
- **Relevance:** This is one of the most highly cited IEEE papers on beat tracking algorithms. It laid the groundwork for modern, programmatic onset envelope analysis (detecting kick drums and volume peaks) which is the core logic used in both our frontend Web Audio API and the backend `librosa` integration.

**3. Deep Similarity Matching & Effects Synchronization**
- **Title:** [*DEMV-matchmaker: Emotional temporal course representation and deep similarity matching for automatic music video generation*](https://doi.org/10.1109/ICASSP.2016.7472182)
- **Authors:** Jen-Chun Lin, Wen-Li Wei, and Hsin-Min Wang
- **Published:** 2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)
- **Relevance:** This paper delves into advanced deep similarity matching to align emotional context and rhythm between music and video. It acts as the conceptual base for our "Cinematic Mode" which applies aggressive visual filters (aberration, glitch text) during high-energy, fast-tempo segments.
