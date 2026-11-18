import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)  # 16:9 widescreen layout

    # Colors
    NAVY = RGBColor(15, 23, 42)       # #0f172a
    BLUE = RGBColor(37, 99, 235)      # #2563eb
    DARK_GRAY = RGBColor(51, 65, 85)  # #334155
    LIGHT_BG = RGBColor(248, 250, 252) # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    ACCENT_CYAN = RGBColor(14, 165, 233)

    blank_slide_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="MAJOR PROJECT STAGE-I | PROJECT REVIEW - II"):
        # Header background bar
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_before = Pt(4)

        # Thin accent line under header
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.04)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE
        line.line.color.rgb = BLUE

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    
    # Background card
    bg_card = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9)
    )
    bg_card.fill.solid()
    bg_card.fill.fore_color.rgb = LIGHT_BG
    bg_card.line.color.rgb = RGBColor(226, 232, 240)

    title_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(4.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = BLUE

    p_dept = tf1.add_paragraph()
    p_dept.text = "DEPARTMENT OF CSE (DATA SCIENCE) | MAJOR PROJECT STAGE-I"
    p_dept.font.size = Pt(12)
    p_dept.font.color.rgb = DARK_GRAY
    p_dept.space_after = Pt(24)

    p_main = tf1.add_paragraph()
    p_main.text = "Vibe-Cuts (Reel): AI-Powered Automated Highlight Reel and Beat-Synced Video Generator"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = NAVY
    p_main.space_after = Pt(20)

    p_info = tf1.add_paragraph()
    p_info.text = "Project Review – II | Academic Year 2026-2027\nPresented by: [Team Members / Roll Numbers]\nUnder the Guidance of: [Project Guide / Coordinator Name]"
    p_info.font.size = Pt(14)
    p_info.font.color.rgb = DARK_GRAY
    p_info.line_spacing = 1.3

    s1.notes_slide.notes_text_frame.text = "Good morning respected coordinators and reviewers. Today, our team is presenting Project Review II for our major project titled 'Vibe-Cuts: AI-Powered Automated Highlight Reel and Beat-Synced Video Generator'."

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_header(s2, "1. Problem Statement")

    s2_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf2 = s2_box.text_frame
    tf2.word_wrap = True

    points_s2 = [
        ("Explosion of Short-Form Content:", "Platforms like Instagram Reels, YouTube Shorts, and TikTok dominate digital media consumption, requiring creator consistency."),
        ("Manual Editing Bottlenecks:", "Creating high-engagement reels from hours of raw video requires tedious scrubbing, finding exciting moments, and manual keyframe editing."),
        ("Beat Synchronization Complexity:", "Aligning cut points, zoom punches, and visual effects to music drops requires professional skill and frame-by-frame precision in tools like Premiere Pro."),
        ("Privacy & Cloud Latency Limitations:", "Existing AI editing web tools force users to upload gigabytes of private raw video to cloud servers, leading to bandwidth throttling, long render queues, and high subscription fees.")
    ]

    for title, desc in points_s2:
        p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
        p.text = "•  " + title + " "
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = NAVY
        p.space_before = Pt(12)
        
        p_sub = tf2.add_paragraph()
        p_sub.text = "    " + desc
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = DARK_GRAY

    s2.notes_slide.notes_text_frame.text = "Here we explain the core problem: Manual editing is too slow for creators, syncing video cuts to music beats is hard, and existing cloud editing platforms raise severe privacy concerns and costs."

    # ==========================================
    # SLIDE 3: OBJECTIVES
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_header(s3, "2. Objectives of the Project")

    s3_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf3 = s3_box.text_frame
    tf3.word_wrap = True

    objectives = [
        ("Automated Highlight Extraction:", "Intelligently slice and sample dynamic highlight segments from raw long-form videos with zero manual timeline scrubbing."),
        ("Client-Side Audio Beat Detection:", "Implement browser-native Web Audio API filtering (<150Hz kick isolation) to detect exact musical drop points in real-time."),
        ("Procedural CapCut-Style VFX Generation:", "Programmatically generate complex mathematical filtergraphs for beat-synced zoom punches, flashbangs, chromatic aberration, and hype typography."),
        ("AI Speech Transcription & Subtitling:", "Integrate OpenAI Whisper to automatically convert video speech to millisecond-accurate subtitles and burn them into the output."),
        ("100% In-Browser Rendering (Zero Cloud Cost):", "Harness WebAssembly (@ffmpeg/ffmpeg) and WORKERFS zero-copy memory streaming for secure, client-side video rendering.")
    ]

    for title, desc in objectives:
        p = tf3.add_paragraph() if tf3.paragraphs[0].text else tf3.paragraphs[0]
        p.text = "✔  " + title + " "
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = BLUE
        p.space_before = Pt(10)
        
        p_sub = tf3.add_paragraph()
        p_sub.text = "    " + desc
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = DARK_GRAY

    s3.notes_slide.notes_text_frame.text = "Our primary objectives focus on automating cut generation, beat-synced visual effects, AI subtitling, and eliminating cloud server compute costs via WebAssembly."

    # ==========================================
    # SLIDE 4: REQUIREMENTS
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_header(s4, "3. Requirements Gathering & Specifications")

    # Left column: Functional & Non-Functional
    left_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf4_l = left_box.text_frame
    tf4_l.word_wrap = True

    p_f = tf4_l.paragraphs[0]
    p_f.text = "Functional Requirements:"
    p_f.font.bold = True
    p_f.font.size = Pt(16)
    p_f.font.color.rgb = NAVY

    f_reqs = [
        "Real-time audio beat & tempo extraction.",
        "Automated magic highlight cut generation.",
        "9:16 vertical re-framing & smooth zoompan.",
        "Beat-triggered VFX (Glitches, Flashes, Hype Text).",
        "OpenAI Whisper speech-to-text subtitle burning."
    ]
    for req in f_reqs:
        p = tf4_l.add_paragraph()
        p.text = "• " + req
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(4)

    p_nf = tf4_l.add_paragraph()
    p_nf.text = "Non-Functional Requirements:"
    p_nf.font.bold = True
    p_nf.font.size = Pt(16)
    p_nf.font.color.rgb = NAVY
    p_nf.space_before = Pt(14)

    nf_reqs = [
        "100% Privacy: In-browser WebAssembly rendering.",
        "Zero Cloud Cost: No expensive backend GPU servers.",
        "High Performance: Zero-copy WORKERFS memory streaming.",
        "Responsive, modern React 19 user interface."
    ]
    for req in nf_reqs:
        p = tf4_l.add_paragraph()
        p.text = "• " + req
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(4)

    # Right column: Hardware, Software & Collection Method
    right_box = s4.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tf4_r = right_box.text_frame
    tf4_r.word_wrap = True

    p_hw = tf4_r.paragraphs[0]
    p_hw.text = "Hardware & Software Specifications:"
    p_hw.font.bold = True
    p_hw.font.size = Pt(16)
    p_hw.font.color.rgb = NAVY

    specs = [
        "Hardware: Standard PC (Intel i5/Ryzen 5, 8GB+ RAM).",
        "Frontend: React 19, TypeScript, Vite, Web Audio API.",
        "Media Engine: @ffmpeg/ffmpeg (WASM), @ffmpeg/core.",
        "Backend: Python 3.11, FastAPI, Librosa, Whisper AI."
    ]
    for sp in specs:
        p = tf4_r.add_paragraph()
        p.text = "• " + sp
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(4)

    p_col = tf4_r.add_paragraph()
    p_col.text = "Requirements Collection Methodology:"
    p_col.font.bold = True
    p_col.font.size = Pt(16)
    p_col.font.color.rgb = NAVY
    p_col.space_before = Pt(14)

    cols = [
        "Creator Workflow Surveys (Identified 75%+ time loss).",
        "Comparative Market Analysis (CapCut vs Premiere Pro).",
        "Feasibility Prototyping on browser WASM heap limits."
    ]
    for c in cols:
        p = tf4_r.add_paragraph()
        p.text = "• " + c
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(4)

    s4.notes_slide.notes_text_frame.text = "This slide outlines our functional and non-functional requirements, technical specifications, and how we surveyed content creators to identify the major workflow bottlenecks."

    # ==========================================
    # SLIDE 5: LITERATURE SURVEY
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_header(s5, "4. Literature Survey (5 Key Research Papers)")

    # Add a summary table of 5 papers
    rows, cols_count = 6, 5
    table_shape = s5.shapes.add_table(rows, cols_count, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = table_shape.table

    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.5)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.5)
    table.columns[4].width = Inches(2.533)

    headers = ["Paper Title & Author", "Methodology / Model", "Dataset Used", "Key Advantages", "Identified Limitations"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = WHITE

    papers_data = [
        ("MVAA (2025)\nZhang et al. (ACM MM)", "Motion-Beat Keyframing + Rhythm Diffusion Inpainting", "AVSync15k & TikTok dance videos", "Seamless motion warp aligned to music beats", "Requires heavy server GPUs; non-real-time"),
        ("AudeoSynth (2015)\nLiao et al. (ACM TOG)", "MCMC optimization on audio rhythm & optical flow", "Travel & home video corpus", "Rigorous mathematical montage optimization", "Slow optimization; lacks procedural VFX/text"),
        ("Beat Tracking (2007)\nDavies & Plumbley (IEEE)", "Two-state model + Onset spectral flux detection", "MIREX Beat Tracking Benchmark", "Deterministic, lightweight kick detection", "Audio only; no video rendering integration"),
        ("DEMV-matchmaker (2016)\nLin et al. (IEEE ICASSP)", "Emotion-oriented Deep Similarity Matching (EDSM)", "Affective Movie & Soundtrack clips", "Synchronizes emotional mood of music and video", "Heavy dataset dependence; no auto-subtitles"),
        ("Whisper AI (2023)\nRadford et al. (OpenAI)", "Encoder-Decoder Transformer + Weak Supervision", "680k hrs multilingual web audio", "Robust speech transcription with timestamps", "High memory footprint on edge devices")
    ]

    for row_idx, data in enumerate(papers_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = NAVY

    s5.notes_slide.notes_text_frame.text = "We studied 5 seminal papers covering audio-visual sync, music video montage, beat tracking, emotional matching, and AI speech recognition."

    # ==========================================
    # SLIDE 6: RESEARCH GAP
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_header(s6, "5. Research Gap & Novelty")

    s6_box = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf6 = s6_box.text_frame
    tf6.word_wrap = True

    gaps = [
        ("1. Absence of Client-Side Autonomous Video Editing:", "Current state-of-the-art tools force users to upload gigabytes of personal video to cloud servers, introducing bandwidth bottlenecks, privacy vulnerabilities, and expensive SaaS subscription paywalls."),
        ("2. Fragmented Multimodal Architectures:", "Existing academic literature treats beat tracking, video cutting, VFX generation, and speech transcription as disjointed research problems with no unified, real-time pipeline."),
        ("3. Lack of Procedural CapCut-Style VFX Synthesis:", "Most automated editors perform simple jump cuts without synthesizing modern viral visual effects (beat-triggered zoom punches, flashbangs, chromatic aberration, and hype typography).")
    ]

    for title, desc in gaps:
        p = tf6.add_paragraph() if tf6.paragraphs[0].text else tf6.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(220, 38, 38) # Red accent for gaps
        p.space_before = Pt(14)
        
        p_sub = tf6.add_paragraph()
        p_sub.text = "  " + desc
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = DARK_GRAY

    s6.notes_slide.notes_text_frame.text = "Our literature survey revealed 3 critical gaps: cloud dependency, fragmented workflows, and lack of procedural cinematic visual effects."

    # ==========================================
    # SLIDE 7: PROPOSED SOLUTION
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_header(s7, "6. Proposed Solution & System Architecture")

    # Workflow Steps
    steps = [
        ("Step 1: Media Ingestion", "Upload raw video & background audio in React UI."),
        ("Step 2: Beat Detection", "Web Audio API isolates bass kicks (<150Hz) & extracts timestamps."),
        ("Step 3: Pass 1 (Cut & Zoom)", "FFmpeg WASM crops to 9:16 portrait with smooth zoompan punch."),
        ("Step 4: Pass 2 (VFX & Mix)", "Procedural filtergraph adds flashes, chromatic glitch & hype text."),
        ("Step 5: AI Subtitles", "Python FastAPI runs OpenAI Whisper to burn timestamped subtitles."),
        ("Step 6: Instant Export", "Zero-copy browser download of TRUE_CAPCUT_EDIT.mp4.")
    ]

    for i, (st, desc) in enumerate(steps):
        col = i % 3
        row = i // 3
        
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.9 + row * 2.5)
        
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BLUE
        card.line.width = Pt(1.5)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.15)
        
        p1 = tf.paragraphs[0]
        p1.text = st
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = NAVY
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = DARK_GRAY
        p2.space_before = Pt(6)

    s7.notes_slide.notes_text_frame.text = "Our proposed architecture runs a 6-step pipeline from client ingestion and beat detection to 2-pass WebAssembly video filtering and Whisper subtitle burning."

    # ==========================================
    # SLIDE 8: TOOLS AND DATASETS
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_header(s8, "7. Tools, Technologies & Datasets")

    # Left Box: Tech Stack
    t_box = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf8_l = t_box.text_frame
    tf8_l.word_wrap = True

    p1 = tf8_l.paragraphs[0]
    p1.text = "Core Technology Stack:"
    p1.font.bold = True
    p1.font.size = Pt(16)
    p1.font.color.rgb = NAVY

    techs = [
        ("React 19 & TypeScript:", "Component-based, type-safe web application UI."),
        ("Web Audio API:", "Browser-native offline audio analysis for bass kick isolation."),
        ("@ffmpeg/ffmpeg (WASM):", "C-based FFmpeg compiled to WebAssembly for in-browser rendering."),
        ("FastAPI & Uvicorn:", "High-performance Python backend for AI microservices."),
        ("OpenAI Whisper (tiny/base):", "Deep learning Automatic Speech Recognition (ASR)."),
        ("Librosa:", "Python audio signal processing library for tempo and BPM tracking.")
    ]
    for title, desc in techs:
        p = tf8_l.add_paragraph()
        p.text = "• " + title + " " + desc
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(4)

    # Right Box: Datasets
    d_box = s8.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tf8_r = d_box.text_frame
    tf8_r.word_wrap = True

    p2 = tf8_r.paragraphs[0]
    p2.text = "Datasets & Test Benchmarks:"
    p2.font.bold = True
    p2.font.size = Pt(16)
    p2.font.color.rgb = NAVY

    datasets = [
        ("UCF101 Benchmark Dataset:", "Standardized video action dataset used for validating automated scene cut detection."),
        ("Multi-Genre Audio Beat Ground Truths:", "Curated electronic, pop, and phonk tracks used to benchmark beat detection precision."),
        ("Open-Domain Vlog & Travel Footage:", "High-definition 1080p/4K raw clips used to test 9:16 reframing, color grading, and rendering speed."),
        ("Multilingual Speech Audio Samples:", "Speech recordings used to evaluate Whisper subtitle Word Error Rate (WER) and timestamp alignment.")
    ]
    for title, desc in datasets:
        p = tf8_r.add_paragraph()
        p.text = "• " + title + " " + desc
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(6)

    s8.notes_slide.notes_text_frame.text = "Here we detail the technologies used (React, Web Audio API, FFmpeg WASM, Whisper, Librosa) and our validation datasets (UCF101, beat benchmarks, vlog footage)."

    # ==========================================
    # SLIDE 9: WORK COMPLETED (STAGE-I)
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_header(s9, "8. Work Completed (Major Project Stage-I)")

    s9_box = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf9 = s9_box.text_frame
    tf9.word_wrap = True

    completed_items = [
        ("✅ Modern Responsive User Interface:", "Built interactive UI with custom video player, keyboard shortcuts (J/K/L/Space/M), interactive timeline track, and real-time status toasts."),
        ("✅ Client-Side Beat Detection Engine:", "Implemented OfflineAudioContext lowpass biquad filter (150Hz) to isolate kick transients and extract beat drop timestamps in the browser."),
        ("✅ 2-Pass FFmpeg WASM Video Pipeline:", "Implemented Pass 1 (smart 9:16 crop & smooth zoompan) and Pass 2 (BGM audio mixing and concat list generation)."),
        ("✅ Procedural CapCut-Style VFX Generator:", "Constructed dynamic filtergraphs supporting contrast boost, vignette, screen flashbangs, chromatic aberration, and hype typography ('BOOM', 'INSANE', 'EPIC')."),
        ("✅ Python AI Backend Integration:", "Developed FastAPI server providing OpenAI Whisper speech transcription, .srt subtitle file generation, and Librosa BPM analysis.")
    ]

    for title, desc in completed_items:
        p = tf9.add_paragraph() if tf9.paragraphs[0].text else tf9.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green for completed
        p.space_before = Pt(8)
        
        p_sub = tf9.add_paragraph()
        p_sub.text = "    " + desc
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = DARK_GRAY

    s9.notes_slide.notes_text_frame.text = "In Stage-I, we have completed the core functional prototype: the frontend interface, Web Audio beat engine, 2-pass WebAssembly video pipeline, procedural VFX generator, and Whisper AI backend."

    # ==========================================
    # SLIDE 10: FUTURE WORK (STAGE-II)
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_header(s10, "9. Future Work & Conclusion (Stage-II Roadmap)")

    s10_box = s10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf10 = s10_box.text_frame
    tf10.word_wrap = True

    future_items = [
        ("🔄 AI Face Tracking & Smart Re-framing:", "Integrate MediaPipe / YOLO face detection to dynamically center human subjects during vertical 9:16 cropping."),
        ("🔄 Intelligent Video Summarization:", "Incorporate Vision-Language Models (VLM) to automatically score and rank the most exciting video moments rather than uniform sampling."),
        ("🔄 Dynamic Style Presets:", "Add customizable genre templates (Anime Phonk Edit, Cinematic Travel Vlog, Lo-Fi Chill Montage)."),
        ("🔄 Direct Social Media Publishing API:", "Integrate OAuth APIs for one-click publishing directly to YouTube Shorts and Instagram Reels."),
        ("📌 Conclusion:", "Vibe-Cuts successfully demonstrates that professional, beat-synced video editing can be automated directly within web browsers using WebAssembly and AI, eliminating cloud rendering costs while preserving complete user privacy.")
    ]

    for title, desc in future_items:
        p = tf10.add_paragraph() if tf10.paragraphs[0].text else tf10.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = BLUE
        p.space_before = Pt(8)
        
        p_sub = tf10.add_paragraph()
        p_sub.text = "    " + desc
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = DARK_GRAY

    s10.notes_slide.notes_text_frame.text = "For Stage-II, we will add face tracking, AI video summarization, and direct social media publishing. Thank you, we are now ready for your questions."

    output_path = os.path.join(os.path.dirname(__file__), "Project_Review_2_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
