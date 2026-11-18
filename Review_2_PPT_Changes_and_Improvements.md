# BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE
## DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)
### MAJOR PROJECT STAGE-I | PROJECT REVIEW – II (2026-2027)

---

# Vibe-Cuts Presentation Review & Text Correction Guide

**Project Title:** Vibe-Cuts: AI-Powered Automated Highlight Reel and Beat-Synced Video Generator  
**Team Members:**
- K. Aishwarya (23C31A6746)
- B. Alekhya (23C31A6719)
- G. Sahan (23C31A6733)
- E. Vishnuvardhan Reddy (23C31A6730)

**Project Guide:** Mr. K. Vijay Kumar, Assistant Professor  

---

## 1. Quick Typo & OCR Error Fix Checklist

| Slide | Original Text in PPT (`aishuamma.pptx`) | Corrected Text | Type of Issue |
|---|---|---|---|
| **Slide 2** | `workfow` | `workflow` | Spelling Typo |
| **Slide 2** | `transfomm` | `transform` | Spelling Typo |
| **Slide 2** | `ready-to- share` | `ready-to-share` | Formatting / Spacing |
| **Slide 4** | `Fasv-to-use interfacs` | `Fast, responsive interface` | Severe OCR / Spelling Typo |
| **Slide 4** | `Secure authenticatior` | `Secure authentication` | Typo (`authenticatior`) |
| **Slide 7** | `ad dressed` | `addressed` | Broken Word Spacing |
| **Slide 10** | `Video uoload /orocessinç endpoints` | `Video upload / processing endpoints` | Severe OCR / Spelling Typo |
| **Slide 10** | `· nitial clip-generation integration` | `• Initial clip-generation integration` | OCR Glitch (Missing 'I') |
| **Slide 11** | `Addstronger` | `Add stronger` | Missing Space |
| **Slide 11** | `sty/ling` | `styling` | Typo / Slash Error |
| **Slide 11** | `aspect-ratio//ayout` | `aspect-ratio / layout` | Typo / Double Slash |

---

## 2. Complete Slide-by-Slide Corrections & Final Content

---

### SLIDE 1: Title Slide
**Slide Category:** Title & Project Details  
**Key Corrections Needed:**
- Add Institution Name and Department.
- Add Academic Stage (`Major Project Stage-I | Project Review - II`).
- Format Team Member Roll Numbers and Guide Designation cleanly.

**Final Slide Text:**
```
BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE
DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)
MAJOR PROJECT STAGE-I | PROJECT REVIEW – II

Vibe-Cuts: AI-Powered Automated Highlight Reel and Beat-Synced Video Generator

TEAM MEMBERS:
• K. AISHWARYA (23C31A6746)
• B. ALEKHYA (23C31A6719)
• G. SAHAN (23C31A6733)
• E. VISHNUVARDHAN REDDY (23C31A6730)

PROJECT GUIDE:
Mr. K. Vijay Kumar, Assistant Professor
```

---

### SLIDE 2: Problem Statement
**Slide Category:** 1. Problem Statement  
**Key Corrections Needed:**
- Fix `workfow` and `transfomm`.
- Highlight beat-synchronization complexity and cloud privacy/cost limitations.

**Final Slide Text:**
```
1. PROBLEM STATEMENT

• Manual Editing Bottleneck: Converting long-form videos into short reels requires hours of tedious scrubbing, trimming, and keyframing.
• Beat Synchronization Complexity: Aligning cuts, zoom punches, and visual effects to music drops requires professional manual precision in desktop NLE tools.
• Manual Subtitle Creation: Generating, timing, and styling synchronized subtitles adds significant manual effort.
• Tool Fragmentation: Cutting, captioning, beat-matching, and 9:16 vertical formatting are handled across multiple disconnected tools.
• Privacy & Cloud Latency: Existing AI web editors require uploading gigabytes of private raw video to cloud servers, causing bandwidth delays and recurring subscription costs.
```

---

### SLIDE 3: Objectives & Target Audience
**Slide Category:** 2. Objectives of the Project  
**Key Corrections Needed:**
- State both target users and technical objectives clearly.
- Highlight WebAudio kick filtering, procedural VFX, and WebAssembly rendering.

**Final Slide Text:**
```
2. OBJECTIVES & TARGET AUDIENCE

Target Audience:
• Content Creators, Podcasters, & YouTubers
• Social Media Managers & Digital Marketers
• Educators & Students creating quick highlights

Project Objectives:
• Automated Highlight Extraction: Intelligently extract key dynamic segments from raw footage.
• Client-Side Beat Detection: Real-time bass kick isolation (<150Hz) to detect musical drop timestamps.
• Procedural CapCut-Style VFX: Auto-generate beat-synced zoom punches, flashbangs, chromatic glitch, and hype typography.
• AI Speech Transcription: Generate millisecond-accurate synchronized captions using OpenAI Whisper.
• 100% In-Browser Rendering: Utilize WebAssembly (FFmpeg WASM) for private, zero-cloud-cost video generation.
```

---

### SLIDE 4: Requirements Gathering & Specifications
**Slide Category:** 3. Requirements Gathering & Specifications  
**Key Corrections Needed:**
- Fix `Fasv-to-use interfacs` and `Secure authenticatior`.
- Separate cleanly into Functional, Non-Functional, and Hardware/Software Specifications.

**Final Slide Text:**
```
3. REQUIREMENTS GATHERING & SPECIFICATIONS

Functional Requirements:
• Real-time audio beat and tempo extraction.
• Automated highlight cutting and 9:16 vertical reframing.
• Beat-triggered visual effects (flashes, glitches, zoom punches).
• OpenAI Whisper speech-to-text caption generation and burning.
• In-browser reel preview and instant MP4 export.

Non-Functional Requirements:
• 100% Client-Side Privacy (Local WebAssembly video rendering).
• Zero Cloud Server Compute Costs (No GPU backend needed for rendering).
• High Performance: Zero-copy WORKERFS memory streaming.
• Fast and intuitive React 19 user interface.

Hardware & Software Specifications:
• Hardware: Standard PC (Intel Core i5 / Ryzen 5, 8GB+ RAM).
• Frontend: React 19, TypeScript, Vite, Web Audio API, @ffmpeg/ffmpeg (WASM).
• AI Backend: Python 3.11, FastAPI, OpenAI Whisper, Librosa.
```

---

### SLIDE 5: Literature Survey
**Slide Category:** 4. Literature Survey  
**Key Corrections Needed:**
- Clean tabular presentation of the 5 foundational research papers.
- Standardize columns: Paper & Author | Methodology | Dataset | Advantages | Limitations.

**Final Slide Text:**
```
4. LITERATURE SURVEY (5 KEY RESEARCH PAPERS)

1. Han et al. (2024) – Unleash CLIP for Video Highlight Detection
   • Method: CLIP-based multimodal feature learning
   • Dataset: QVHighlights
   • Advantages: Pretrained multimodal knowledge
   • Limitations: Highlight detection only; no automated editing or VFX

2. Xie et al. (2024) – Knowledge-Aware Multimodal Video Summarization
   • Method: Multimodal deep network combining visual & audio
   • Dataset: Public video summarization benchmarks
   • Advantages: Integrates external semantic knowledge
   • Limitations: Complex pipeline; lacks social-media 9:16 formatting

3. Argaw et al. (2024) – Scaling Video Summarization with LLMs
   • Method: LLM-assisted long-video pretraining
   • Dataset: Long-form video corpus & generated data
   • Advantages: Strong narrative context understanding
   • Limitations: Computationally heavy; requires massive GPU clusters

4. Ren et al. (2024) – TimeChat Long-Video Multimodal LLM
   • Method: Time-sensitive multimodal LLM
   • Dataset: Long-video benchmarks
   • Advantages: Accurate temporal localization and reasoning
   • Limitations: High inference latency; not suitable for browser edge

5. Sul et al. (2023) – Mr. HiSum Benchmark
   • Method: Joint highlight detection and summarization
   • Dataset: 31,892 diverse videos
   • Advantages: Large-scale standardized evaluation
   • Limitations: Benchmark only; not an end-to-end automated reel generator
```

---

### SLIDE 6: Overcoming Limitations of Existing Work
**Slide Category:** 5. Overcoming Limitations of Existing Work  
**Key Corrections Needed:**
- Connect academic limitations directly to Vibe-Cuts technical solutions.

**Final Slide Text:**
```
5. OVERCOMING LIMITATIONS OF EXISTING WORK

• Video Highlight Detection Methods:
  - Limitation: Only identifies timestamps without editing or formatting.
  - Vibe-Cuts Solution: Converts detected highlights directly into complete, beat-synced 9:16 vertical reels.

• Video Summarization Frameworks:
  - Limitation: Focus on text/visual summaries without viral short-form aesthetics (VFX, hype text, music).
  - Vibe-Cuts Solution: Synthesizes procedural CapCut-style effects (zoom punches, flashbangs, chromatic aberration).

• Speech-to-Text & Captioning Tools:
  - Limitation: Standalone transcription without automated video cutting or audio beat alignment.
  - Vibe-Cuts Solution: Combines Whisper speech-to-text with auto-burned captions and beat-synced transitions.

• Heavy Cloud AI Models:
  - Limitation: Require expensive server GPUs, high latency, and cloud data uploads.
  - Vibe-Cuts Solution: Lightweight hybrid model utilizing client-side Web Audio API and WebAssembly rendering.
```

---

### SLIDE 7: Research Gap & Novelty
**Slide Category:** 6. Research Gap & Novelty  
**Key Corrections Needed:**
- Fix `ad dressed` typo.
- Articulate the 3 clear research gaps clearly.

**Final Slide Text:**
```
6. RESEARCH GAP & NOVELTY

1. Absence of Client-Side Autonomous Editing:
   - Existing AI tools force users to upload raw footage to cloud servers, introducing bandwidth bottlenecks, privacy concerns, and costly SaaS paywalls.

2. Fragmented Multimodal Architectures:
   - Research treats beat tracking, video cutting, VFX generation, and speech transcription as disjointed tasks rather than a unified real-time pipeline.

3. Lack of Procedural Beat-Synced VFX Synthesis:
   - Automated editors perform simple cuts but fail to generate dynamic viral effects (beat-triggered zoom punches, flashbangs, chromatic glitches, and hype typography).

👉 Vibe-Cuts Novelty: An integrated client-side architecture combining real-time audio analysis, procedural VFX, AI subtitles, and in-browser WASM rendering into a single end-to-end workflow.
```

---

### SLIDE 8: Proposed Methodology & System Architecture
**Slide Category:** 7. Proposed Methodology & System Architecture  
**Key Corrections Needed:**
- Replace general bullets with the concrete 6-step pipeline.

**Final Slide Text:**
```
7. PROPOSED METHODOLOGY & SYSTEM ARCHITECTURE

• Step 1: Media Ingestion
  - Upload raw video and background music track directly in the React interface.

• Step 2: Client-Side Beat Detection
  - Web Audio API applies lowpass biquad filter (<150Hz) to detect bass kick drops and extract precise timestamps.

• Step 3: Pass 1 – Reframing & Zoompan
  - FFmpeg WebAssembly reframes video to 9:16 portrait and applies smooth dynamic zoom punches.

• Step 4: Pass 2 – Procedural VFX & Audio Mix
  - Mathematical filtergraphs apply contrast boosts, flashbangs, chromatic glitches, and mix the background audio.

• Step 5: AI Speech-to-Text Subtitling
  - FastAPI backend runs OpenAI Whisper to generate timestamped .srt subtitles and burn them into the video.

• Step 6: Client-Side Export
  - Direct zero-copy browser export of the final ready-to-publish MP4 reel.
```

---

### SLIDE 9: Tools, Technologies & Datasets
**Slide Category:** 8. Tools, Technologies & Datasets  
**Key Corrections Needed:**
- Format into clear categories: Frontend/WASM, AI Backend, Datasets/Benchmarks.

**Final Slide Text:**
```
8. TOOLS, TECHNOLOGIES & DATASETS

Frontend & In-Browser Engine:
• React 19, TypeScript, Vite, Tailwind CSS
• Web Audio API (OfflineAudioContext bass filtering)
• @ffmpeg/ffmpeg & @ffmpeg/core (WebAssembly video processing)

Backend & AI Models:
• Python 3.11, FastAPI, Uvicorn
• OpenAI Whisper (Automatic Speech Recognition & Subtitling)
• Librosa (Audio Signal Processing & BPM analysis)

Datasets & Benchmarks:
• UCF101 Dataset (Action recognition & scene cut validation)
• Multi-Genre Beat Ground Truths (Electronic, Pop, Phonk music beat benchmarks)
• Open-Domain Vlog & Podcast Footage (1080p/4K 9:16 reframing tests)
• Multilingual Speech Audio (Whisper Word Error Rate & timestamp evaluation)
```

---

### SLIDE 10: Work Completed (Stage-I Status)
**Slide Category:** 9. Work Completed (Stage-I)  
**Key Corrections Needed:**
- Fix `uoload /orocessinç` and `· nitial`.
- Present concrete deliverables with checkmarks.

**Final Slide Text:**
```
9. WORK COMPLETED (STAGE-I STATUS)

✅ Modern Interactive User Interface:
   - Built responsive React 19 UI with video player, keyboard shortcuts (J/K/L/Space/M), interactive timeline track, and status toasts.

✅ Browser-Native Beat Detection Engine:
   - Implemented Web Audio API kick transient extraction and real-time beat drop timestamp detection.

✅ 2-Pass WebAssembly Video Pipeline:
   - Integrated FFmpeg WASM for 9:16 smart cropping, zoompan keyframing, and background audio mixing.

✅ Procedural CapCut-Style VFX Generator:
   - Dynamic filtergraphs for screen flashbangs, chromatic aberration glitch, vignette, and hype typography ("BOOM", "INSANE", "EPIC").

✅ AI Speech Transcription Backend:
   - FastAPI microservice with OpenAI Whisper for automatic speech-to-text and synchronized subtitle file (.srt) generation.
```

---

### SLIDE 11: Future Work (Stage-II Roadmap) & Conclusion
**Slide Category:** 10. Future Work & Conclusion  
**Key Corrections Needed:**
- Fix `Addstronger`, `sty/ling`, `aspect-ratio//ayout`.
- Outline clear Stage-II milestones and conclude with the impact statement.

**Final Slide Text:**
```
10. FUTURE WORK (STAGE-II ROADMAP) & CONCLUSION

Stage-II Development Roadmap:
🔄 AI Face Tracking & Smart Re-framing:
   - Integrate MediaPipe / YOLO face detection to dynamically center human subjects during 9:16 cropping.
🔄 Vision-Language Summarization:
   - Incorporate Vision-Language Models (VLM) for semantic scoring and highlight ranking.
🔄 Dynamic Style & Genre Presets:
   - Add customizable visual templates (Phonk Edit, Cinematic Travel Vlog, Lo-Fi Montage).
🔄 Direct Social Media Publishing APIs:
   - One-click OAuth publishing directly to YouTube Shorts and Instagram Reels.

📌 Conclusion:
Vibe-Cuts demonstrates that professional beat-synced video editing and AI subtitling can run directly in web browsers via WebAssembly and AI, eliminating expensive cloud GPU costs while ensuring 100% user privacy.
```
