# BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE
### Department of Computer Science & Engineering (Data Science)
## MAJOR PROJECT STAGE-I: PROJECT REVIEW – II PREPARATION GUIDE & REPORT

---

# 📌 SECTION A: PROJECT DETAILS AT A GLANCE
- **Project Title:** **Vibe-Cuts (Reel): AI-Powered Automated Highlight Reel Generation and Beat-Synced Video Editing System**
- **Domain:** Data Science / Artificial Intelligence / Computer Vision & Audio Signal Processing
- **Target Platform:** Web-Based Cross-Platform Application (Client-Side WASM + AI Microservice)
- **Tech Stack:** React 19, TypeScript, Web Audio API, WebAssembly (FFmpeg WASM), Python 3.11, FastAPI, OpenAI Whisper, Librosa.

---

# 1. REQUIREMENTS GATHERING

### 1.1 Project Problem Explanation
In today's digital era, short-form video platforms (Instagram Reels, YouTube Shorts, TikTok) dominate user attention. However, creating high-engagement, cinematic short videos from long raw footage is an extremely tedious, time-consuming, and expensive process. Content creators spend hours performing repetitive tasks:
1. Manually scrubbing through footage to locate highlights.
2. Manually identifying musical beat drops and aligning cut points.
3. Applying complex visual effects (VFX) like zoom pulses, chromatic aberration, flash transitions, and hype text.
4. Manually listening, transcribing, and timing subtitles.

Existing editing software (Adobe Premiere Pro, Final Cut Pro) requires steep learning curves and high-end hardware, while cloud-based automated editors suffer from privacy issues, high subscription costs, and long server rendering queues.

### 1.2 Target Users (Who Will Use the Project?)
- **Social Media Content Creators & Influencers:** To automatically generate viral Reels/Shorts with synced beat cuts in seconds.
- **Vloggers & Travel Filmmakers:** To condense hours of raw footage into energetic montage highlights.
- **Gaming & Sports Streamers:** To automatically convert long gameplay streams into dynamic highlight clips.
- **Digital Marketers & Small Businesses:** To produce high-quality promotional video ads without hiring professional video editors.
- **Everyday Casual Users:** Anyone wanting to turn mobile phone clips into professional cinematic videos effortlessly.

### 1.3 Main Requirements of the Project
#### Functional Requirements:
1. **Audio Beat & Drop Detection:** Real-time audio waveform processing to detect kick-drum peaks and musical tempo (BPM).
2. **Automated Magic Cuts:** Intelligent slicing and random highlight sampling distributed across the raw video, synchronizing clip boundaries to musical beats.
3. **Cinematic 9:16 Transformation & Dynamic VFX:** Automated smart vertical cropping (9:16 portrait) with procedural filtergraphs (zoom-pan punch-in, contrast/saturation boost, film grain, flashbangs, chromatic RGB shift, and vignette).
4. **Beat-Triggered Hype Typography:** Overlaying animated impact keywords (e.g., "BOOM", "INSANE", "EPIC") synchronized with beat markers.
5. **AI Speech Transcription & Subtitling:** Automatic speech-to-text transcription with millisecond-level timestamped subtitle (.srt) generation and hardcoded video caption burning.
6. **Multi-Track Audio Mixing:** Seamlessly replacing or mixing original video audio with background music (BGM).

#### Non-Functional Requirements:
1. **In-Browser Client-Side Processing (Privacy & Zero Server Cost):** Video rendering occurs directly inside the user's browser using WebAssembly (`@ffmpeg/ffmpeg`), ensuring raw video never leaves the user's device.
2. **Low Latency & High Performance:** Fast seeking and zero-copy memory management via `WORKERFS` file system mounting.
3. **User-Friendly & Responsive UI:** Interactive timeline track, live video player with keyboard hotkeys, and real-time pipeline status notifications.

### 1.4 Software, Hardware, Tools & Datasets Required
- **Hardware Requirements:**
  - Processor: Multi-core Intel Core i5/AMD Ryzen 5 or higher.
  - RAM: Minimum 8 GB (16 GB recommended for seamless multi-pass video encoding).
  - Storage: 2 GB free disk space for local caching and model weights.
  - Client Device: Any modern laptop/desktop with WebAssembly and Web Audio API compatible browser (Chrome, Edge, Firefox).
- **Software & Development Tools:**
  - Frontend: React 19, TypeScript, Vite, Tailwind/Vanilla CSS, Lucide React.
  - Client Media Engine: Web Audio API (`OfflineAudioContext`, `BiquadFilterNode`), `@ffmpeg/ffmpeg` (WASM), `@ffmpeg/core`.
  - Backend: Python 3.11, FastAPI, Uvicorn, Subprocess, FFmpeg-python.
  - AI & Signal Processing Models: OpenAI Whisper (`tiny`/`base` ASR models), Librosa (Beat Tracking & Audio Analysis).
- **Datasets / Test Data:**
  - Benchmarking Video Corpora: Standard test datasets including UCF101 and open-domain high-definition vlog/travel video samples.
  - Audio Datasets: Diverse genre audio tracks (Electronic, Pop, Cinematic, Hip-Hop) with annotated beat ground truths.

### 1.5 How Requirements Were Collected
1. **Stakeholder & Creator Workflow Survey:** Interviewed content creators and analyzed manual editing steps to quantify time bottlenecks (revealing >75% of editing time is spent on finding cuts and matching beats).
2. **Competitive Product Analysis:** Studied CapCut, Premiere Pro Auto-Reframe, and Opus Clip, identifying key gaps in server queue delays, paywalls, and privacy vulnerabilities.
3. **System Feasibility & Prototyping:** Tested browser-based WebAssembly limitations and memory boundaries, proving that `WORKERFS` streaming and Web Audio peak detection provide near real-time performance on client machines.

---

# 2. LITERATURE SURVEY

### 2.1 Five Key Research Papers (Summary & Analysis)

#### Paper 1: Let Your Video Listen to Your Music! – Beat-Aligned, Content-Preserving Video Editing with Arbitrary Music (MVAA)
- **Authors:** Xinyu Zhang, Dong Gong, Zicheng Duan, Anton van den Hengel, Lingqiao Liu
- **Published in:** 33rd ACM International Conference on Multimedia (ACM MM / arXiv:2506.18881, 2025)
- **Method / Architecture:** Proposes Music-Video Auto-Alignment (MVAA) utilizing a two-step framework: Motion-Beat alignment for keyframe insertion matching musical beats, followed by a rhythm-aware diffusion inpainting model to smooth visual transitions.
- **Dataset Used:** AVSync15k dataset and TikTok dancing video corpus.
- **Key Results:** Achieves superior rhythmic synchronization scores (F1 > 0.82) and high temporal visual consistency compared to standard heuristic warpers.
- **Advantages:** Generates seamless, dance-like video motion aligned with any arbitrary music track.
- **Limitations:** Extremely heavy computational cost; requires high-end server GPUs, making real-time client-side deployment impossible.

#### Paper 2: AudeoSynth: Music-Driven Video Montage
- **Authors:** Zicheng Liao, Yizhou Yu, Bingchen Gong, Lechao Cheng
- **Published in:** ACM Transactions on Graphics (TOG) / SIGGRAPH 2015 (DOI: 10.1145/2766966)
- **Method / Architecture:** Formulates music-driven video montage as a global optimization problem. Uses temporal rhythmic feature extraction from music and optical flow motion from video, optimized using Markov Chain Monte Carlo (MCMC) sampling.
- **Dataset Used:** User personal home video and travel video collections.
- **Key Results:** High user subjective satisfaction scores (88% preferred automated montage over random cuts).
- **Advantages:** Solid mathematical optimization framework that respects both audio tempo and visual motion speed.
- **Limitations:** Non-real-time optimization; cannot generate modern social media visual effects (glitches, dynamic zoom punches, animated captions).

#### Paper 3: Context-Dependent Beat Tracking of Musical Audio
- **Authors:** Matthew E. P. Davies, Mark D. Plumbley
- **Published in:** IEEE Transactions on Audio, Speech, and Language Processing (Vol. 15, No. 3, 2007, DOI: 10.1109/TASL.2006.885257)
- **Method / Architecture:** Implements a two-state context-dependent model combining an onset detection function (spectral flux) with an adaptive tempo induction filter to track beat phases.
- **Dataset Used:** MIREX Beat Tracking Benchmark dataset.
- **Key Results:** 84.6% beat tracking accuracy across varied musical meters and tempo fluctuations.
- **Advantages:** Computationally lightweight, deterministic, and highly accurate for kick/snare detection.
- **Limitations:** Limited to 1D audio signals; provides no direct integration with video rendering or automated cut decisions.

#### Paper 4: DEMV-matchmaker: Emotional Temporal Course Representation and Deep Similarity Matching for Automatic Music Video Generation
- **Authors:** Jen-Chun Lin, Wen-Li Wei, Hsin-Min Wang
- **Published in:** IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP 2016, DOI: 10.1109/ICASSP.2016.7472182)
- **Method / Architecture:** Utilizes Emotion-oriented Deep Similarity Matching (EDSM) with affective course modeling (Valence-Arousal dimensions) to align movie shot emotional dynamics with music audio.
- **Dataset Used:** Film clip repository with manual affective valence/arousal annotations.
- **Key Results:** Outperformed standard similarity models in emotional alignment with statistically significant p < 0.01.
- **Advantages:** Selects clips that match not just the tempo, but also the emotional mood and intensity of the music.
- **Limitations:** Requires heavy pre-annotated training data; high latency; lacks automated subtitling and browser-based rendering.

#### Paper 5: Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)
- **Authors:** Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, Ilya Sutskever (OpenAI)
- **Published in:** International Conference on Machine Learning (ICML 2023 / arXiv:2212.04356)
- **Method / Architecture:** An end-to-end Encoder-Decoder Transformer model trained on 680,000 hours of weakly supervised multilingual and multitask audio collected from the internet.
- **Dataset Used:** 680k hours diverse web audio corpus across 99 languages.
- **Key Results:** Approaches human-level accuracy and robustness to background music and ambient noise without fine-tuning; low Word Error Rate (WER < 10% on clean English).
- **Advantages:** Exceptional zero-shot speech transcription with built-in millisecond timestamp estimation.
- **Limitations:** Requires significant memory footprint (~1GB+ RAM for larger models); higher latency on CPU-only edge devices.

---

### 2.2 Literature Survey Comparison Table

| S.No | Paper Title & Authors | Methodology / Architecture | Dataset Used | Key Results / Metric | Advantages | Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **MVAA: Beat-Aligned Video Editing (2025)**<br>*Zhang et al. (ACM MM)* | Motion-Beat alignment + Rhythm-aware diffusion inpainting | AVSync15k & TikTok dance videos | Rhythmic F1 > 0.82; superior temporal consistency | Highly seamless motion warp; supports arbitrary audio | Heavy GPU demand; non-real-time; expensive cloud compute |
| **2** | **AudeoSynth Video Montage (2015)**<br>*Liao et al. (ACM TOG)* | MCMC Optimization on audio rhythm & optical flow | Personal travel video collection | 88% user satisfaction rating over heuristic cuts | Robust mathematical global montage formulation | High compute time; no procedural VFX or typography |
| **3** | **Context-Dependent Beat Tracking (2007)**<br>*Davies & Plumbley (IEEE TASLP)* | Two-state model + Onset spectral flux detection | MIREX Beat Tracking Benchmark | 84.6% beat tracking accuracy | Lightweight; fast; deterministic beat detection | Audio-only processing; no video pipeline integration |
| **4** | **DEMV-matchmaker (2016)**<br>*Lin et al. (IEEE ICASSP)* | Emotion-oriented Deep Similarity Matching (EDSM) | Affective Movie & Music dataset | Statistically significant mood alignment (p < 0.01) | Synchronizes visual mood & tempo with music energy | Heavy dataset dependency; no auto-caption burning |
| **5** | **Whisper Speech Recognition (2023)**<br>*Radford et al. (OpenAI / ICML)* | Sequence-to-Sequence Transformer with Weak Supervision | 680,000 hrs multilingual web audio | Near human-level WER (< 10% on clean audio) | Extremely robust to background music; timestamped SRT | Heavy resource requirements for large models |

---

### 2.3 Research Gap Identified
1. **Absence of Client-Side Autonomous Editing:** Existing state-of-the-art tools force users to upload gigabytes of personal video files to remote cloud servers, creating privacy risks, bandwidth throttling, and server queue costs.
2. **Fragmented Workflows:** Available research treats beat detection, video cutting, VFX generation, and speech subtitling as isolated problems rather than an integrated, unified pipeline.
3. **Lack of Procedural Cinematic VFX Synthesis:** Most automated video editors only perform plain jump cuts. They fail to synthesize modern, viral CapCut-style effects (beat-triggered zoom punches, chromatic aberration, flashbang transitions, and dynamic hype text overlays).

### 2.4 How Our Project is Different From Existing Work
1. **Dual In-Browser & Serverless Processing:** Uses `@ffmpeg/ffmpeg` (WebAssembly) with `WORKERFS` zero-copy memory mounting to cut, grade, and render videos directly inside the client's browser with zero cloud server compute costs.
2. **Hybrid Beat Detection:** Implements browser-native Web Audio API (Lowpass Biquad Filter isolating kick frequencies) for instant client-side beat synchronization, backed by Python Librosa for high-precision BPM analysis.
3. **Procedural VFX Filtergraph Engine:** Programmatically compiles dynamic FFmpeg `filter_complex` expressions that mathematically trigger zoom pulses, RGB channel shifts, screen flashbangs, and vignette effects on exact beat timestamps.
4. **End-to-End Multimodal Integration:** Combines beat-synced highlights, procedural VFX, and OpenAI Whisper AI speech transcription into a single frictionless 1-click web interface.

---

# 3. PRESENTATION STRUCTURE (SLIDE BY SLIDE)

### Slide 1: Title Slide
- **Title:** Vibe-Cuts: AI-Driven Automated Highlight Reel and Beat-Synced Video Generator
- **Department:** Department of Computer Science & Engineering (Data Science)
- **Institution:** Balaji Institute of Technology & Science
- **Presenter Names & Hall Ticket Numbers:** [Add Your Team Members' Names & Roll Nos]
- **Under the Guidance of:** [Add Guide / Project Coordinator Name]

### Slide 2: Problem Statement
- Manual editing of short-form videos (Reels/Shorts/TikTok) is slow, repetitive, and requires high skill and expensive editing suites.
- Aligning video cuts and visual effects to music beats manually requires frame-by-frame precision.
- Existing cloud automated editors suffer from privacy vulnerabilities, expensive subscriptions, and slow cloud upload/rendering queues.

### Slide 3: Objectives
- To develop an automated web application that generates professional highlight reels from raw footage with zero manual editing.
- To implement real-time audio beat detection for frame-accurate cut synchronization.
- To programmatically apply cinematic visual effects (zooms, chromatic aberration, flashes, hype text) synced to music tempo.
- To integrate OpenAI Whisper AI for automatic speech transcription and subtitle burning.
- To achieve zero-cloud rendering using in-browser WebAssembly (FFmpeg WASM) for total privacy and zero server cost.

### Slide 4: Requirements
- **Functional:** Audio beat extraction, random highlight sampling, procedural filtergraph generation, Whisper speech-to-text, 9:16 vertical re-framing.
- **Non-Functional:** Zero-upload client-side rendering, sub-minute processing time, low memory footprint, responsive modern UI.
- **Hardware & Software:** Multi-core CPU, 8GB RAM, React 19, TypeScript, Web Audio API, FFmpeg WASM, Python FastAPI, Whisper, Librosa.

### Slide 5: Literature Survey
- Reviewed 5 seminal research papers covering:
  - *MVAA (ACM MM 2025):* Motion-beat alignment & inpainting.
  - *AudeoSynth (ACM TOG 2015):* Optimization of music-driven montage.
  - *Context Beat Tracking (IEEE TASLP 2007):* Onset detection and tempo estimation.
  - *DEMV-Matchmaker (IEEE ICASSP 2016):* Deep similarity & mood matching.
  - *Whisper (ICML 2023):* Robust multilingual speech recognition.

### Slide 6: Research Gap
- Existing systems require cloud GPU servers or paid SaaS subscriptions.
- Lack of client-side privacy-first video rendering architectures.
- Existing tools do plain cuts without synthesizing modern beat-synced VFX (zoom punches, flashbangs, chromatic glitch).

### Slide 7: Proposed Solution & System Architecture
- **Step 1 (Ingestion):** User uploads raw video and BGM in React UI.
- **Step 2 (Beat Detection):** Web Audio API isolates bass kick frequencies (<150Hz) and extracts peak timestamps.
- **Step 3 (Pass 1 - Cut & Zoom):** FFmpeg WASM streams video via `WORKERFS` and crops to 9:16 with smooth zoompan.
- **Step 4 (Pass 2 - VFX & Concat):** Generates procedural `filter_complex` applying contrast, saturation, flashbangs, chromatic aberration, and hype text on beat triggers.
- **Step 5 (AI Subtitles):** Optional FastAPI backend runs Whisper AI to transcribe audio and burn subtitles.
- **Step 6 (Instant Export):** Automatic client-side download of `TRUE_CAPCUT_EDIT.mp4`.

### Slide 8: Tools and Datasets
- **Frontend Technologies:** React 19, TypeScript, Vite, Web Audio API, `@ffmpeg/ffmpeg` WASM.
- **Backend Technologies:** Python 3.11, FastAPI, OpenAI Whisper, Librosa, FFmpeg.
- **Datasets / Validation Benchmarks:** UCF101 benchmark clips, multi-genre music tracks with beat annotations, sample vlogs for WER validation.

### Slide 9: Work Completed (Major Project Stage-I)
- ✅ Completed complete frontend UI with Video Player, interactive Timeline, and Status Toasts.
- ✅ Implemented Web Audio API kick-drum beat detection engine.
- ✅ Implemented 2-pass FFmpeg WASM in-browser rendering with zero-copy `WORKERFS` streaming.
- ✅ Implemented procedural CapCut-style VFX filter generator (Zoom punch, Flash, Vignette, Hype typography).
- ✅ Implemented Python FastAPI backend with Whisper speech transcription and Librosa tempo analysis.

### Slide 10: Future Work (Stage-II Objectives)
- 🔄 Integrate Computer Vision (YOLO / MediaPipe) for smart face-tracking during 9:16 vertical re-framing.
- 🔄 Implement AI video summarization using vision-language models to score and pick the most exciting video moments automatically.
- 🔄 Add customizable preset styles (Anime Edit, Cinematic Vlog, Fast Phonk Beat).
- 🔄 Direct social media sharing integration (YouTube Shorts / Instagram API).

---

# 4. QUICK REVISION Q&A FOR VIVA REVIEW

**Q1: What is the main innovation of your project compared to tools like CapCut?**
**Ans:** While CapCut requires users to manually place keyframes or uploads video to cloud servers, Vibe-Cuts operates entirely inside the client's web browser using WebAssembly. This provides instant processing, 100% privacy (video never leaves the PC), and zero hosting/server compute costs.

**Q2: How does your beat detection algorithm work?**
**Ans:** We use the browser's `OfflineAudioContext` with a `BiquadFilterNode` configured as a low-pass filter at 150 Hz to isolate kick drums and bass transients. We then scan the audio data in fixed chunks to find volume peaks exceeding our threshold, returning exact second-level beat timestamps.

**Q3: How do you bypass browser memory limits when rendering large video files?**
**Ans:** Standard WebAssembly crashes if large video files are loaded directly into RAM. We solved this by using FFmpeg WASM's `WORKERFS` virtual filesystem. `WORKERFS` mounts the native browser `File` handle directly, allowing FFmpeg to stream video chunks directly from the disk without consuming browser heap memory.

**Q4: How do you apply visual effects on the exact beat timestamps?**
**Ans:** We dynamically compile an FFmpeg `filter_complex` string using mathematical enable expressions such as `between(t, beat_time, beat_time + 0.15)`. This enables effects like `negate` (glitch), `eq=brightness=0.4` (flashbang), and `drawtext` (hype keywords) specifically during the fraction of a second a beat hits.
