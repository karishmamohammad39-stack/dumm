import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_deck():
    src_path = r'C:\Users\ganap\Downloads\aishuamma.pptx'
    prs = Presentation(src_path)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    # Shape 0: Title
    if len(s1.shapes) > 0 and s1.shapes[0].has_text_frame:
        tf = s1.shapes[0].text_frame
        tf.clear()
        p1 = tf.paragraphs[0]
        p1.text = "BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.name = 'Times New Roman'
        
        p2 = tf.add_paragraph()
        p2.text = "DEPARTMENT OF CSE (DATA SCIENCE) | MAJOR PROJECT REVIEW – II"
        p2.font.size = Pt(11)
        p2.font.name = 'Times New Roman'
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = "Vibe-Cuts : Automated AI Video Editing Engine"
        p3.font.size = Pt(28)
        p3.font.bold = True
        p3.font.name = 'Times New Roman'

    # Table 4 (Team Guide)
    if len(s1.shapes) > 4 and s1.shapes[4].has_table:
        t_guide = s1.shapes[4].table
        if len(t_guide.rows) >= 2:
            cell_g = t_guide.cell(1, 0)
            cell_g.text = "Mr. K. Vijay Kumar\nAssistant Professor, CSE (DS)"
            for p in cell_g.text_frame.paragraphs:
                p.font.name = 'Times New Roman'
                p.font.size = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 2: Problem statement
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    if len(s2.shapes) > 0 and s2.shapes[0].has_text_frame:
        s2.shapes[0].text_frame.text = "Problem Statement"
        for p in s2.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s2.shapes) > 1 and s2.shapes[1].has_text_frame:
        tf = s2.shapes[1].text_frame
        tf.clear()
        
        p_items = [
            ("Time-Consuming Manual Editing: ", "Converting long-form videos into short reels requires watching, selecting, and trimming content manually."),
            ("Difficult Highlight Identification: ", "Users struggle to identify the most engaging or meaningful moments in lengthy videos without AI assistance."),
            ("Manual Caption Creation: ", "Preparing, timing, and styling subtitles/captions manually adds substantial editing effort."),
            ("Tool Fragmentation: ", "Cutting, captioning, beat-matching, audio processing, and 9:16 vertical formatting are handled across multiple disconnected tools."),
            ("Limited End-to-End Automation: ", "A unified workflow is needed to transform long videos into ready-to-share short-form content with zero cloud privacy risks.")
        ]
        
        for idx, (title, desc) in enumerate(p_items):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.JUSTIFY
            p.space_after = Pt(10)
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.bold = True
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(17)
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.bold = False
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(16)

    # -------------------------------------------------------------
    # SLIDE 3: Objectives & Users
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    if len(s3.shapes) > 0 and s3.shapes[0].has_text_frame:
        s3.shapes[0].text_frame.text = "Objectives & Target Audience"
        for p in s3.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s3.shapes) > 1 and s3.shapes[1].has_text_frame:
        tf = s3.shapes[1].text_frame
        tf.clear()

        # Section 1
        p_u_title = tf.paragraphs[0]
        p_u_title.text = "Who Will Use This Project:"
        p_u_title.font.bold = True
        p_u_title.font.name = 'Times New Roman'
        p_u_title.font.size = Pt(18)
        p_u_title.space_after = Pt(4)

        users = [
            "Content creators, YouTubers, and podcasters",
            "Social-media managers and digital marketers",
            "Students, educators, and general users who need quick short-form content"
        ]
        for u in users:
            p = tf.add_paragraph()
            p.text = "  • " + u
            p.font.name = 'Times New Roman'
            p.font.size = Pt(15)
            p.space_after = Pt(2)

        # Section 2
        p_o_title = tf.add_paragraph()
        p_o_title.text = "Objectives:"
        p_o_title.font.bold = True
        p_o_title.font.name = 'Times New Roman'
        p_o_title.font.size = Pt(18)
        p_o_title.space_before = Pt(10)
        p_o_title.space_after = Pt(4)

        objs = [
            "Automatically identify important and engaging moments in long videos.",
            "Generate beat-synced short clips with minimal manual editing work.",
            "Convert speech into millisecond-accurate synchronized captions via Whisper AI.",
            "Create vertical 9:16 reels with procedural visual effects (glitches, zooms, flashes).",
            "In-browser WebAssembly rendering to eliminate cloud GPU costs and protect privacy.",
            "Reduce overall video editing time by more than 80%."
        ]
        for o in objs:
            p = tf.add_paragraph()
            p.text = "  • " + o
            p.font.name = 'Times New Roman'
            p.font.size = Pt(15)
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 4: Requirements Gathering & Specifications
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    if len(s4.shapes) > 0 and s4.shapes[0].has_text_frame:
        s4.shapes[0].text_frame.text = "Requirements Gathering & Specifications"
        for p in s4.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    # Left box: Functional
    if len(s4.shapes) > 1 and s4.shapes[1].has_text_frame:
        tf1 = s4.shapes[1].text_frame
        tf1.clear()
        p_head = tf1.paragraphs[0]
        p_head.text = "Functional Requirements"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(18)
        p_head.space_after = Pt(6)

        f_reqs = [
            "User authentication and session management",
            "Long-video upload & audio stream extraction",
            "Client-side audio beat and transient detection",
            "Speech-to-text processing & caption alignment",
            "Important-moment detection & dynamic highlight slicing",
            "Automatic 9:16 vertical conversion & zoompan",
            "Procedural beat-synced VFX (flashes, glitches, text)",
            "In-browser reel preview and instant MP4 export"
        ]
        for r in f_reqs:
            p = tf1.add_paragraph()
            p.text = "• " + r
            p.font.name = 'Times New Roman'
            p.font.size = Pt(14)
            p.space_after = Pt(2)

    # Right box: Non-Functional & Specs
    if len(s4.shapes) > 2 and s4.shapes[2].has_text_frame:
        tf2 = s4.shapes[2].text_frame
        tf2.clear()
        p_head = tf2.paragraphs[0]
        p_head.text = "Non-Functional Requirements"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(18)
        p_head.space_after = Pt(6)

        nf_reqs = [
            "Fast, responsive & intuitive user interface",
            "100% Client-Side Privacy (Local WebAssembly)",
            "Reliable, low-latency video processing",
            "Accurate speech-to-text transcription",
            "Zero Cloud Server GPU Costs",
            "Secure authentication and data safety",
            "Scalable, modular system architecture",
            "Broad format support (MP4, MOV, AAC, MP3)"
        ]
        for r in nf_reqs:
            p = tf2.add_paragraph()
            p.text = "• " + r
            p.font.name = 'Times New Roman'
            p.font.size = Pt(14)
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 5: Literature Survey
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    if len(s5.shapes) > 0 and s5.shapes[0].has_text_frame:
        s5.shapes[0].text_frame.text = "Literature Survey (5 Key Research Papers)"
        for p in s5.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s5.shapes) > 2 and s5.shapes[2].has_table:
        t = s5.shapes[2].table
        # Format table headers
        headers = ['Paper (Author, Year)', 'Methodology', 'Dataset', 'Results / Output', 'Key Advantages', 'Identified Limitations']
        for c_idx, h in enumerate(headers):
            cell = t.cell(0, c_idx)
            cell.text = h
            for p in cell.text_frame.paragraphs:
                p.font.name = 'Times New Roman'
                p.font.bold = True
                p.font.size = Pt(11)
        
        # Clean row font sizes
        for r_idx in range(1, len(t.rows)):
            for c_idx in range(len(t.columns)):
                cell = t.cell(r_idx, c_idx)
                for p in cell.text_frame.paragraphs:
                    p.font.name = 'Times New Roman'
                    p.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # SLIDE 6: Overcoming Limitations
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    if len(s6.shapes) > 0 and s6.shapes[0].has_text_frame:
        s6.shapes[0].text_frame.text = "Overcoming the Limitations of Existing Work"
        for p in s6.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s6.shapes) > 1 and s6.shapes[1].has_table:
        t = s6.shapes[1].table
        headers = ['Existing Approach / Work', 'Identified Limitation', 'How Vibe-Cuts Overcomes It']
        for c_idx, h in enumerate(headers):
            cell = t.cell(0, c_idx)
            cell.text = h
            for p in cell.text_frame.paragraphs:
                p.font.name = 'Times New Roman'
                p.font.bold = True
                p.font.size = Pt(12)
        
        table_rows = [
            ("Video Highlight Detection Methods", "Mainly focus on identifying important timestamps rather than producing a complete short-form video.", "Vibe-Cuts uses highlight detection as one stage of an end-to-end pipeline that automatically formats and generates short reels."),
            ("Video Summarization Methods", "Generate a summarized video but lack viral social-media formatting, beat-sync, and visual effects.", "Vibe-Cuts converts selected segments into 9:16 vertical reels with beat-synced cuts, zoom punches, and hype effects."),
            ("Speech-to-Text / Captioning Systems", "Generate transcripts or standalone subtitles without video editing or rhythm synchronization.", "Vibe-Cuts integrates Whisper speech-to-text with automatic subtitle burning and beat-aligned video pacing."),
            ("Heavy Multimodal LLMs", "Require complex server pipelines, massive GPU resources, and high inference latency.", "Vibe-Cuts follows a modular, lightweight hybrid workflow combining client-side WebAssembly and local AI."),
            ("Manual Video Editing Tools", "Users must manually select, trim, caption, and sync videos using complex desktop NLE software.", "Vibe-Cuts automates highlight selection, clipping, captioning, VFX, and 9:16 formatting in one click.")
        ]
        
        for r_idx, row_data in enumerate(table_rows, 1):
            for c_idx, text in enumerate(row_data):
                cell = t.cell(r_idx, c_idx)
                cell.text = text
                for p in cell.text_frame.paragraphs:
                    p.font.name = 'Times New Roman'
                    p.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # SLIDE 7: Research Gap & Novelty
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    if len(s7.shapes) > 0 and s7.shapes[0].has_text_frame:
        s7.shapes[0].text_frame.text = "Research Gap & Novelty"
        for p in s7.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s7.shapes) > 1 and s7.shapes[1].has_text_frame:
        tf = s7.shapes[1].text_frame
        tf.clear()

        gaps = [
            ("Fragmented Multimodal Research: ", "Existing research addresses video summarization, highlight detection, captioning, and beat tracking as separate, disjointed tasks."),
            ("Lack of End-to-End Reel Generation: ", "Academic benchmarks focus on detecting important timestamps rather than producing complete, formatted social-media short videos."),
            ("Absence of Client-Side Editing: ", "Current AI tools force users to upload raw footage to remote servers, causing bandwidth bottlenecks, high subscription costs, and privacy vulnerabilities."),
            ("Lack of Procedural Cinematic VFX: ", "Automated editors perform basic cuts without synthesizing modern viral effects (beat-triggered zoom punches, flashbangs, chromatic glitch, and hype typography)."),
            ("Vibe-Cuts Novelty: ", "Bridges these gaps by unifying client-side Web Audio beat detection, procedural VFX filtergraphs, OpenAI Whisper captions, and WebAssembly rendering into a zero-cloud-cost workflow.")
        ]

        for idx, (title, desc) in enumerate(gaps):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.JUSTIFY
            p.space_after = Pt(10)
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.bold = True
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(16)
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.bold = False
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(15)

    # -------------------------------------------------------------
    # SLIDE 8: Proposed Methodology
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    if len(s8.shapes) > 0 and s8.shapes[0].has_text_frame:
        s8.shapes[0].text_frame.text = "Proposed Methodology & Architecture"
        for p in s8.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s8.shapes) > 1 and s8.shapes[1].has_text_frame:
        tf = s8.shapes[1].text_frame
        tf.clear()

        steps = [
            ("Step 1: Media Ingestion – ", "Upload and analyze long-form video and audio directly in the React interface with instant waveform visualization."),
            ("Step 2: Client-Side Beat Detection – ", "Web Audio API applies lowpass biquad filtering (<150Hz) to isolate bass kicks and extract beat drop timestamps."),
            ("Step 3: Highlight Selection & Slicing – ", "Identify engaging moments and slice dynamic highlight segments automatically based on energy peaks."),
            ("Step 4: 9:16 Reframing & Procedural VFX – ", "FFmpeg WebAssembly reframes video to 9:16 portrait and synthesizes beat-synced zoom punches, flashbangs, and glitches."),
            ("Step 5: AI Caption & Subtitle Generation – ", "FastAPI backend runs OpenAI Whisper to transcribe speech and burn synchronized, styled .srt subtitles into the video."),
            ("Step 6: Preview & Instant Export – ", "Allow users to preview the generated reel and download the final ready-to-share MP4 with zero cloud GPU cost.")
        ]

        for idx, (title, desc) in enumerate(steps):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.JUSTIFY
            p.space_after = Pt(8)
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.bold = True
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(16)
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.bold = False
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(15)

    # -------------------------------------------------------------
    # SLIDE 9: Tools & Datasets
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    if len(s9.shapes) > 0 and s9.shapes[0].has_text_frame:
        s9.shapes[0].text_frame.text = "Tools, Technologies & Datasets"
        for p in s9.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    # Box 1: Frontend
    if len(s9.shapes) > 1 and s9.shapes[1].has_text_frame:
        tf1 = s9.shapes[1].text_frame
        tf1.clear()
        p_head = tf1.paragraphs[0]
        p_head.text = "Frontend & In-Browser"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        fe_items = [
            "React 19 & TypeScript",
            "Vite & Tailwind CSS",
            "Web Audio API (Kick filter)",
            "@ffmpeg/ffmpeg (WASM)",
            "Video Player & Preview"
        ]
        for it in fe_items:
            p = tf1.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(16)
            p.space_after = Pt(2)

    # Box 3: Backend & AI
    if len(s9.shapes) > 3 and s9.shapes[3].has_text_frame:
        tf3 = s9.shapes[3].text_frame
        tf3.clear()
        p_head = tf3.paragraphs[0]
        p_head.text = "Backend & AI Models"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        be_items = [
            "Python 3.11 & FastAPI",
            "OpenAI Whisper (Speech ASR)",
            "Librosa (BPM Analysis)",
            "FFmpeg Filtergraph Engine",
            "OpenCV / MoviePy"
        ]
        for it in be_items:
            p = tf3.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(16)
            p.space_after = Pt(2)

    # Box 4: Datasets
    if len(s9.shapes) > 4 and s9.shapes[4].has_text_frame:
        tf4 = s9.shapes[4].text_frame
        tf4.clear()
        p_head = tf4.paragraphs[0]
        p_head.text = "Datasets & Benchmarks"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        ds_items = [
            "UCF101 Action Dataset",
            "Multi-Genre Audio Beats",
            "Podcast & Interview Clips",
            "Vlog & Travel Raw Footage",
            "Multilingual Speech Audio"
        ]
        for it in ds_items:
            p = tf4.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(16)
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 10: Work Completed
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    if len(s10.shapes) > 0 and s10.shapes[0].has_text_frame:
        s10.shapes[0].text_frame.text = "Work Completed (Stage-I Status)"
        for p in s10.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    # Box 1: Frontend
    if len(s10.shapes) > 1 and s10.shapes[1].has_text_frame:
        tf1 = s10.shapes[1].text_frame
        tf1.clear()
        p_head = tf1.paragraphs[0]
        p_head.text = "Frontend Interface"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        items = [
            "Responsive React 19 UI",
            "Custom video player workflow",
            "Interactive timeline & hotkeys",
            "Status toasts & progress tracking",
            "In-browser reel preview module"
        ]
        for it in items:
            p = tf1.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(15)
            p.space_after = Pt(2)

    # Box 2: Backend (Fixed severe typos!)
    if len(s10.shapes) > 2 and s10.shapes[2].has_text_frame:
        tf2 = s10.shapes[2].text_frame
        tf2.clear()
        p_head = tf2.paragraphs[0]
        p_head.text = "Backend Services"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        items = [
            "FastAPI microservice structure",
            "Video upload & processing endpoints",  # FIXED uoload /orocessinç
            "Audio extraction & Librosa analysis",
            "Initial clip-generation integration",  # FIXED · nitial
            "OpenAI Whisper subtitle API"
        ]
        for it in items:
            p = tf2.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(15)
            p.space_after = Pt(2)

    # Box 3: AI / Video
    if len(s10.shapes) > 3 and s10.shapes[3].has_text_frame:
        tf3 = s10.shapes[3].text_frame
        tf3.clear()
        p_head = tf3.paragraphs[0]
        p_head.text = "AI & Media Engine"
        p_head.font.bold = True
        p_head.font.name = 'Times New Roman'
        p_head.font.size = Pt(20)
        p_head.space_after = Pt(6)

        items = [
            "Web Audio beat detection verified",
            "Dynamic highlight selection tested",
            "Whisper speech transcription sync",
            "9:16 vertical cropping verified",
            "Procedural VFX filtergraphs tested"
        ]
        for it in items:
            p = tf3.add_paragraph()
            p.text = "• " + it
            p.font.name = 'Times New Roman'
            p.font.size = Pt(15)
            p.space_after = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 11: Future Work
    # -------------------------------------------------------------
    s11 = prs.slides[10]
    if len(s11.shapes) > 0 and s11.shapes[0].has_text_frame:
        s11.shapes[0].text_frame.text = "Future Work (Stage-II Roadmap) & Conclusion"
        for p in s11.shapes[0].text_frame.paragraphs:
            p.font.name = 'Times New Roman'
            p.font.bold = True

    if len(s11.shapes) > 1 and s11.shapes[1].has_text_frame:
        tf = s11.shapes[1].text_frame
        tf.clear()

        future_items = [
            ("AI Face Tracking & Smart Re-framing: ", "Integrate MediaPipe / YOLO face detection to dynamically center speakers during 9:16 vertical cropping."),
            ("Vision-Language Summarization: ", "Incorporate Vision-Language Models (VLM) for multimodal semantic highlight scoring and intelligent scene ranking."),
            ("Multilingual Subtitle Styling: ", "Support multilingual captions with animated kinetic fonts, custom color grading, and subtitle styling presets."),
            ("Dynamic Style & Genre Presets: ", "Add customizable visual templates (Phonk Edit, Travel Vlog, Lo-Fi Montage) and flexible aspect-ratio / layout options."),
            ("Direct Social Media APIs: ", "Integrate OAuth publishing directly to YouTube Shorts and Instagram Reels with one-click export."),
            ("Project Conclusion: ", "Vibe-Cuts demonstrates that automated, beat-synced video editing and AI subtitling can run locally in web browsers, eliminating expensive cloud GPU costs while ensuring 100% user privacy.")
        ]

        for idx, (title, desc) in enumerate(future_items):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.JUSTIFY
            p.space_after = Pt(8)
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.bold = True
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(15.5)
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.bold = False
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(14.5)

    # Save to all locations
    downloads_out = r'C:\Users\ganap\Downloads\aishuamma.pptx'
    desktop_out = r'C:\Users\ganap\OneDrive\Desktop\aishuamma_corrected.pptx'
    project_out = os.path.join(os.path.dirname(__file__), 'aishuamma_corrected.pptx')

    prs.save(downloads_out)
    prs.save(desktop_out)
    prs.save(project_out)

    print("Successfully updated presentation across:")
    print(f" 1. {downloads_out}")
    print(f" 2. {desktop_out}")
    print(f" 3. {project_out}")

if __name__ == '__main__':
    update_deck()
