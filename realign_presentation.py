import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def set_font(p, font_name="Times New Roman", size_pt=14, bold=False, italic=False, color_rgb=None, align=PP_ALIGN.LEFT):
    p.alignment = align
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.font.bold = bold
        r.font.italic = italic
        if color_rgb:
            r.font.color.rgb = color_rgb

def style_title(shape, title_text, size_pt=26):
    shape.left = Inches(0.9)
    shape.top = Inches(0.4)
    shape.width = Inches(11.5)
    shape.height = Inches(0.8)
    if shape.has_text_frame:
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = title_text
        r.font.name = "Times New Roman"
        r.font.size = Pt(size_pt)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)

def realign_all():
    src_path = r'C:\Users\ganap\Downloads\aishuamma.pptx'
    prs = Presentation(src_path)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    DARK_TEXT = RGBColor(30, 41, 59)
    HEADING_COLOR = RGBColor(15, 23, 42)
    BLUE_ACCENT = RGBColor(37, 99, 235)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides[0]
    # Shape 3 is Picture (Header/Logo banner)
    for sh in s1.shapes:
        if sh.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            sh.left = Inches(1.8)
            sh.top = Inches(0.3)
            sh.width = Inches(9.7)
            sh.height = Inches(1.7)

    # Shape 0: Main Title Box
    if len(s1.shapes) > 0 and s1.shapes[0].has_text_frame:
        sh = s1.shapes[0]
        sh.left = Inches(1.0)
        sh.top = Inches(2.2)
        sh.width = Inches(11.33)
        sh.height = Inches(1.8)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.clear()
        
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = "BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE"
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(15)
        r0.font.bold = True
        r0.font.color.rgb = BLUE_ACCENT

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)\nMAJOR PROJECT STAGE-I | PROJECT REVIEW – II (2026-2027)"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = DARK_TEXT
        p1.space_before = Pt(4)
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = "Vibe-Cuts : Automated AI Video Editing Engine"
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(26)
        r2.font.bold = True
        r2.font.color.rgb = HEADING_COLOR

    # Shape 2: Team Members Label
    if len(s1.shapes) > 2 and s1.shapes[2].has_text_frame:
        sh = s1.shapes[2]
        sh.left = Inches(1.0)
        sh.top = Inches(4.3)
        sh.width = Inches(6.0)
        sh.height = Inches(0.4)
        tf = sh.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = "PROJECT TEAM MEMBERS :"
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = HEADING_COLOR

    # Shape 1: Team Members Table
    if len(s1.shapes) > 1 and s1.shapes[1].has_table:
        sh = s1.shapes[1]
        sh.left = Inches(1.0)
        sh.top = Inches(4.75)
        sh.width = Inches(6.5)
        sh.height = Inches(1.9)
        t = sh.table
        t.columns[0].width = Inches(4.0)
        t.columns[1].width = Inches(2.5)
        
        members = [
            ("K. AISHWARYA", "23C31A6746"),
            ("B. ALEKHYA", "23C31A6719"),
            ("G. SAHAN", "23C31A6733"),
            ("E. VISHNUVARDHAN REDDY", "23C31A6730")
        ]
        for r_idx, (name, roll) in enumerate(members):
            c0 = t.cell(r_idx, 0)
            c1 = t.cell(r_idx, 1)
            c0.text = name
            c1.text = roll
            for cell in (c0, c1):
                cell.margin_left = Inches(0.1)
                cell.margin_top = Inches(0.05)
                cell.margin_right = Inches(0.1)
                cell.margin_bottom = Inches(0.05)
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.LEFT
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(13)
                        r.font.bold = True
                        r.font.color.rgb = DARK_TEXT

    # Shape 4: Guide Table
    if len(s1.shapes) > 4 and s1.shapes[4].has_table:
        sh = s1.shapes[4]
        sh.left = Inches(8.2)
        sh.top = Inches(4.75)
        sh.width = Inches(4.1)
        sh.height = Inches(1.4)
        t = sh.table
        t.columns[0].width = Inches(4.1)
        t.cell(0, 0).text = "PROJECT GUIDE"
        t.cell(1, 0).text = "Mr. K. Vijay Kumar\nAssistant Professor, CSE (DS)"
        
        for r_idx in range(len(t.rows)):
            cell = t.cell(r_idx, 0)
            cell.margin_left = Inches(0.1)
            cell.margin_top = Inches(0.05)
            cell.margin_right = Inches(0.1)
            cell.margin_bottom = Inches(0.05)
            for p_idx, p in enumerate(cell.text_frame.paragraphs):
                p.alignment = PP_ALIGN.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(14 if r_idx == 0 else 13)
                    r.font.bold = (r_idx == 0 or p_idx == 0)
                    r.font.color.rgb = HEADING_COLOR if r_idx == 0 else DARK_TEXT

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    s2 = prs.slides[1]
    style_title(s2.shapes[0], "1. Problem Statement")
    
    if len(s2.shapes) > 1 and s2.shapes[1].has_text_frame:
        sh = s2.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.35)
        sh.width = Inches(11.5)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
        tf.clear()

        problems = [
            ("Time-Consuming Manual Editing: ", "Converting long-form videos into engaging short reels requires tedious manual scrubbing, selecting, and trimming."),
            ("Difficult Highlight Identification: ", "Creators struggle to identify the most engaging or meaningful moments in lengthy videos without automated AI analysis."),
            ("Manual Caption Creation: ", "Preparing, synchronizing, and styling subtitles adds substantial manual effort and editing overhead."),
            ("Tool Fragmentation: ", "Cutting, captioning, beat-matching, audio processing, and 9:16 vertical formatting are handled across multiple disconnected tools."),
            ("Limited End-to-End Automation & Privacy: ", "A unified workflow is needed to transform long videos into ready-to-share short-form reels with zero cloud privacy risks and low compute latency.")
        ]

        for idx, (head, desc) in enumerate(problems):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(12)
            p.line_spacing = 1.2
            
            r1 = p.add_run()
            r1.text = "• " + head
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(16.5)
            r1.font.bold = True
            r1.font.color.rgb = HEADING_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15.5)
            r2.font.bold = False
            r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 3: Objectives & Target Audience
    # =========================================================================
    s3 = prs.slides[2]
    style_title(s3.shapes[0], "2. Objectives & Target Audience")
    
    # Let's clean up shape 1 and position it nicely
    if len(s3.shapes) > 1 and s3.shapes[1].has_text_frame:
        sh = s3.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.35)
        sh.width = Inches(11.5)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
        tf.clear()

        # Section 1: Target Audience
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = "Target Users & Beneficiaries:"
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(17.5)
        r0.font.bold = True
        r0.font.color.rgb = BLUE_ACCENT
        p0.space_after = Pt(4)

        users = [
            "Content Creators, YouTubers, and Podcasters seeking rapid repurposing.",
            "Social Media Managers & Digital Marketers managing multi-platform channels.",
            "Educators, Students, and General Users requiring quick automated highlights."
        ]
        for u in users:
            p = tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(3)
            r = p.add_run()
            r.text = "  • " + u
            r.font.name = "Times New Roman"
            r.font.size = Pt(15)
            r.font.color.rgb = DARK_TEXT

        # Section 2: Objectives
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        p1.space_before = Pt(12)
        p1.space_after = Pt(4)
        r1 = p1.add_run()
        r1.text = "Key Project Objectives:"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(17.5)
        r1.font.bold = True
        r1.font.color.rgb = BLUE_ACCENT

        objectives = [
            ("Automated Highlight Extraction: ", "Intelligently slice dynamic highlight segments from raw long-form footage."),
            ("Client-Side Beat Detection: ", "Isolate bass kick transients (<150Hz) using Web Audio API for musical synchronization."),
            ("AI Speech Transcription: ", "Generate millisecond-accurate synchronized captions via OpenAI Whisper."),
            ("Procedural CapCut-Style VFX: ", "Synthesize beat-synced zoom punches, flashbangs, and hype typography."),
            ("100% In-Browser Rendering: ", "Leverage WebAssembly (FFmpeg WASM) to eliminate cloud GPU server costs & protect privacy."),
            ("Turnaround Time Reduction: ", "Reduce manual short-form editing turnaround time by over 80%.")
        ]
        for head, desc in objectives:
            p = tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(3)
            
            r_h = p.add_run()
            r_h.text = "  • " + head
            r_h.font.name = "Times New Roman"
            r_h.font.size = Pt(15)
            r_h.font.bold = True
            r_h.font.color.rgb = HEADING_COLOR
            
            r_d = p.add_run()
            r_d.text = desc
            r_d.font.name = "Times New Roman"
            r_d.font.size = Pt(14.5)
            r_d.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4: Requirements Gathering & Specifications
    # =========================================================================
    s4 = prs.slides[3]
    style_title(s4.shapes[0], "3. Requirements Gathering & Specifications")

    # Left Box: Functional Requirements
    if len(s4.shapes) > 1 and s4.shapes[1].has_text_frame:
        sh1 = s4.shapes[1]
        sh1.left = Inches(0.9)
        sh1.top = Inches(1.35)
        sh1.width = Inches(5.6)
        sh1.height = Inches(5.6)
        tf1 = sh1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = Inches(0.05)
        tf1.clear()

        p_h = tf1.paragraphs[0]
        p_h.alignment = PP_ALIGN.LEFT
        r_h = p_h.add_run()
        r_h.text = "Functional Requirements"
        r_h.font.name = "Times New Roman"
        r_h.font.size = Pt(17.5)
        r_h.font.bold = True
        r_h.font.color.rgb = BLUE_ACCENT
        p_h.space_after = Pt(8)

        f_reqs = [
            "User authentication & session management",
            "Long-video upload & media stream extraction",
            "Client-side kick transient & beat drop detection",
            "Speech-to-text processing & caption alignment",
            "Important-moment detection & dynamic highlight slicing",
            "Automatic 9:16 vertical cropping & smooth zoompan",
            "Procedural beat-synced VFX (flashes, glitches, hype text)",
            "In-browser reel preview and instant MP4 export"
        ]
        for r in f_reqs:
            p = tf1.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(5)
            p.line_spacing = 1.15
            run = p.add_run()
            run.text = "• " + r
            run.font.name = "Times New Roman"
            run.font.size = Pt(14)
            run.font.color.rgb = DARK_TEXT

    # Right Box: Non-Functional & Specifications
    if len(s4.shapes) > 2 and s4.shapes[2].has_text_frame:
        sh2 = s4.shapes[2]
        sh2.left = Inches(6.8)
        sh2.top = Inches(1.35)
        sh2.width = Inches(5.6)
        sh2.height = Inches(5.6)
        tf2 = sh2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = Inches(0.05)
        tf2.clear()

        p_h = tf2.paragraphs[0]
        p_h.alignment = PP_ALIGN.LEFT
        r_h = p_h.add_run()
        r_h.text = "Non-Functional & Technical Specs"
        r_h.font.name = "Times New Roman"
        r_h.font.size = Pt(17.5)
        r_h.font.bold = True
        r_h.font.color.rgb = BLUE_ACCENT
        p_h.space_after = Pt(8)

        nf_reqs = [
            "Fast, responsive & intuitive React 19 UI",
            "100% Client-Side Privacy (Local WebAssembly)",
            "Reliable, low-latency in-browser video processing",
            "Zero Cloud Server GPU Costs (No backend GPU needed)",
            "Accurate speech-to-text transcription via Whisper AI",
            "Hardware: PC with Intel i5/Ryzen 5 & 8GB+ RAM",
            "Frontend: React 19, TypeScript, Vite, Web Audio API",
            "Backend: Python 3.11, FastAPI, Librosa, FFmpeg WASM"
        ]
        for r in nf_reqs:
            p = tf2.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(5)
            p.line_spacing = 1.15
            run = p.add_run()
            run.text = "• " + r
            run.font.name = "Times New Roman"
            run.font.size = Pt(14)
            run.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5: Literature Survey
    # =========================================================================
    s5 = prs.slides[4]
    style_title(s5.shapes[0], "4. Literature Survey (5 Key Research Papers)", size_pt=24)
    
    # Hide/clear shape 1 if empty placeholder
    if len(s5.shapes) > 1 and s5.shapes[1].has_text_frame:
        s5.shapes[1].text_frame.clear()
        s5.shapes[1].width = 0
        s5.shapes[1].height = 0

    if len(s5.shapes) > 2 and s5.shapes[2].has_table:
        sh = s5.shapes[2]
        sh.left = Inches(0.8)
        sh.top = Inches(1.25)
        sh.width = Inches(11.733)
        sh.height = Inches(5.6)
        t = sh.table
        
        col_w = [Inches(2.3), Inches(2.1), Inches(1.4), Inches(1.9), Inches(2.0), Inches(2.033)]
        for c_idx, w in enumerate(col_w):
            t.columns[c_idx].width = w

        headers = ['Paper (Author, Year)', 'Methodology', 'Dataset', 'Results / Output', 'Key Advantages', 'Identified Limitations']
        for c_idx, h in enumerate(headers):
            cell = t.cell(0, c_idx)
            cell.text = h
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.bold = True
                    r.font.size = Pt(11)
                    r.font.color.rgb = HEADING_COLOR

        rows_data = [
            ("Han et al. (2024)\nCLIP Video Highlight", "CLIP-based multimodal feature learning for video highlight detection", "QVHighlights", "Strong performance in video highlight detection", "Uses pretrained multimodal knowledge", "Focused mainly on highlight detection; no auto-editing"),
            ("Xie et al. (2024)\nMultimodal Summarizer", "Knowledge-aware multimodal deep network using visual and audio info", "Public video datasets", "Improved video summarization over baselines", "Combines multiple modalities and knowledge", "Complex processing pipeline; no social 9:16 format"),
            ("Argaw et al. (2024)\nLLM Video Summarization", "Large-language-model-assisted video summarization pretraining", "Long-form video corpus", "Improved long-video summarization capability", "Handles long-form content using LLM context", "High computational & GPU cluster requirements"),
            ("Ren et al. (2024)\nTimeChat Multimodal LLM", "Time-sensitive multimodal large language model for long videos", "Long-video benchmarks", "Strong temporal localization & video reasoning", "Understands complex temporal relationships", "High computational & edge inference latency"),
            ("Sul et al. (2023)\nMr. HiSum Benchmark", "Large-scale video highlight detection and summarization benchmark", "31,892 diverse videos", "Provides large-scale evaluation framework", "Standardized multimodal benchmark dataset", "Benchmark only; not an end-to-end reel generator")
        ]

        for r_idx, row_vals in enumerate(rows_data, 1):
            for c_idx, val in enumerate(row_vals):
                cell = t.cell(r_idx, c_idx)
                cell.text = val
                cell.margin_left = cell.margin_right = Inches(0.06)
                cell.margin_top = cell.margin_bottom = Inches(0.04)
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.LEFT
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6: Overcoming Limitations
    # =========================================================================
    s6 = prs.slides[5]
    style_title(s6.shapes[0], "5. Overcoming Limitations of Existing Work", size_pt=24)
    
    if len(s6.shapes) > 1 and s6.shapes[1].has_table:
        sh = s6.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.25)
        sh.width = Inches(11.533)
        sh.height = Inches(5.6)
        t = sh.table
        
        t.columns[0].width = Inches(2.8)
        t.columns[1].width = Inches(4.2)
        t.columns[2].width = Inches(4.533)

        headers = ['Existing Approach / Work', 'Identified Limitation', 'How Vibe-Cuts Overcomes It']
        for c_idx, h in enumerate(headers):
            cell = t.cell(0, c_idx)
            cell.text = h
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.bold = True
                    r.font.size = Pt(12)
                    r.font.color.rgb = HEADING_COLOR

        rows_data = [
            ("Video Highlight Detection Methods", "Mainly focus on identifying important timestamps rather than producing a complete short-form video.", "Vibe-Cuts uses highlight detection as one stage of an end-to-end pipeline that automatically formats and generates complete short reels."),
            ("Video Summarization Frameworks", "Generate a summarized video but lack viral social-media formatting, beat-sync, and visual effects.", "Vibe-Cuts converts selected segments into 9:16 vertical reels with beat-synced cuts, zoom punches, and procedural hype effects."),
            ("Speech-to-Text / Captioning Systems", "Generate transcripts or standalone subtitles without video editing or rhythm synchronization.", "Vibe-Cuts integrates Whisper speech-to-text with automatic subtitle burning and beat-aligned video pacing."),
            ("Heavy Multimodal LLMs", "Require complex server pipelines, massive cloud GPU resources, and high inference latency.", "Vibe-Cuts follows a modular, lightweight hybrid workflow combining client-side WebAssembly and local AI microservices."),
            ("Manual Video Editing Tools", "Users must manually select, trim, caption, and sync videos using complex desktop NLE software.", "Vibe-Cuts automates highlight selection, clipping, captioning, VFX, and 9:16 formatting in a single unified workflow.")
        ]

        for r_idx, row_vals in enumerate(rows_data, 1):
            for c_idx, val in enumerate(row_vals):
                cell = t.cell(r_idx, c_idx)
                cell.text = val
                cell.margin_left = cell.margin_right = Inches(0.08)
                cell.margin_top = cell.margin_bottom = Inches(0.05)
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.LEFT
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10.5)
                        r.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 7: Research Gap & Novelty
    # =========================================================================
    s7 = prs.slides[6]
    style_title(s7.shapes[0], "6. Research Gap & Novelty")

    if len(s7.shapes) > 1 and s7.shapes[1].has_text_frame:
        sh = s7.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.35)
        sh.width = Inches(11.5)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
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
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(11)
            p.line_spacing = 1.18
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(16)
            r1.font.bold = True
            r1.font.color.rgb = BLUE_ACCENT if "Novelty" in title else HEADING_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15)
            r2.font.bold = False
            r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 8: Proposed Methodology
    # =========================================================================
    s8 = prs.slides[7]
    style_title(s8.shapes[0], "7. Proposed Methodology & Architecture")

    if len(s8.shapes) > 1 and s8.shapes[1].has_text_frame:
        sh = s8.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.35)
        sh.width = Inches(11.5)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
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
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(10)
            p.line_spacing = 1.18
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(16)
            r1.font.bold = True
            r1.font.color.rgb = BLUE_ACCENT
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15)
            r2.font.bold = False
            r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 9: Tools, Technologies & Datasets
    # =========================================================================
    s9 = prs.slides[8]
    style_title(s9.shapes[0], "8. Tools, Technologies & Datasets")

    # Clean empty shape 2
    if len(s9.shapes) > 2 and s9.shapes[2].has_text_frame:
        s9.shapes[2].text_frame.clear()
        s9.shapes[2].width = 0
        s9.shapes[2].height = 0

    # 3 Columns
    col_configs_s9 = [
        (1, Inches(0.9), "Frontend & In-Browser", [
            "React 19 & TypeScript",
            "Vite & Tailwind CSS",
            "Web Audio API (Kick filter)",
            "@ffmpeg/ffmpeg (WASM)",
            "@ffmpeg/core worker runtime",
            "Custom video player & preview"
        ]),
        (3, Inches(4.86), "Backend & AI Models", [
            "Python 3.11 & FastAPI",
            "Uvicorn async server",
            "OpenAI Whisper (Speech ASR)",
            "Librosa (BPM Audio Analysis)",
            "FFmpeg Filtergraph Engine",
            "OpenCV & MoviePy tools"
        ]),
        (4, Inches(8.83), "Datasets & Benchmarks", [
            "UCF101 Action Dataset",
            "Multi-Genre Audio Beats",
            "Podcast & Interview Clips",
            "Vlog & Travel Raw Footage",
            "Multilingual Speech Audio",
            "Social media test benchmarks"
        ])
    ]

    for sh_idx, left_pos, head_text, items in col_configs_s9:
        if len(s9.shapes) > sh_idx and s9.shapes[sh_idx].has_text_frame:
            sh = s9.shapes[sh_idx]
            sh.left = left_pos
            sh.top = Inches(1.35)
            sh.width = Inches(3.6)
            sh.height = Inches(5.6)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
            tf.clear()

            p_h = tf.paragraphs[0]
            p_h.alignment = PP_ALIGN.LEFT
            r_h = p_h.add_run()
            r_h.text = head_text
            r_h.font.name = "Times New Roman"
            r_h.font.size = Pt(17.5)
            r_h.font.bold = True
            r_h.font.color.rgb = BLUE_ACCENT
            p_h.space_after = Pt(8)

            for it in items:
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT
                p.space_after = Pt(5)
                p.line_spacing = 1.15
                r = p.add_run()
                r.text = "• " + it
                r.font.name = "Times New Roman"
                r.font.size = Pt(14)
                r.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 10: Work Completed
    # =========================================================================
    s10 = prs.slides[9]
    style_title(s10.shapes[0], "9. Work Completed (Major Project Stage-I)")

    col_configs_s10 = [
        (1, Inches(0.9), "Frontend Interface", [
            "Responsive React 19 UI",
            "Video player & scrubber workflow",
            "Interactive timeline & hotkeys",
            "Real-time processing status toasts",
            "In-browser reel preview module",
            "Zero-copy file export logic"
        ]),
        (2, Inches(4.86), "Backend Services", [
            "FastAPI microservice structure",
            "Video upload & processing endpoints",
            "Audio extraction & Librosa analysis",
            "Initial clip-generation integration",
            "OpenAI Whisper subtitle API",
            "Timestamped .srt file generator"
        ]),
        (3, Inches(8.83), "AI & Media Engine", [
            "Web Audio kick filter verified",
            "Dynamic highlight selection tested",
            "Whisper speech transcription sync",
            "9:16 vertical cropping verified",
            "Procedural VFX filtergraphs tested",
            "Pass 1 & Pass 2 rendering verified"
        ])
    ]

    for sh_idx, left_pos, head_text, items in col_configs_s10:
        if len(s10.shapes) > sh_idx and s10.shapes[sh_idx].has_text_frame:
            sh = s10.shapes[sh_idx]
            sh.left = left_pos
            sh.top = Inches(1.35)
            sh.width = Inches(3.6)
            sh.height = Inches(5.6)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
            tf.clear()

            p_h = tf.paragraphs[0]
            p_h.alignment = PP_ALIGN.LEFT
            r_h = p_h.add_run()
            r_h.text = head_text
            r_h.font.name = "Times New Roman"
            r_h.font.size = Pt(17.5)
            r_h.font.bold = True
            r_h.font.color.rgb = BLUE_ACCENT
            p_h.space_after = Pt(8)

            for it in items:
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT
                p.space_after = Pt(5)
                p.line_spacing = 1.15
                r = p.add_run()
                r.text = "• " + it
                r.font.name = "Times New Roman"
                r.font.size = Pt(14)
                r.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 11: Future Work & Conclusion
    # =========================================================================
    s11 = prs.slides[10]
    style_title(s11.shapes[0], "10. Future Work (Stage-II Roadmap) & Conclusion", size_pt=24)

    if len(s11.shapes) > 1 and s11.shapes[1].has_text_frame:
        sh = s11.shapes[1]
        sh.left = Inches(0.9)
        sh.top = Inches(1.35)
        sh.width = Inches(11.5)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
        tf.clear()

        future_items = [
            ("AI Face Tracking & Smart Re-framing: ", "Integrate MediaPipe / YOLO face detection to dynamically center human subjects during 9:16 vertical cropping."),
            ("Vision-Language Summarization: ", "Incorporate Vision-Language Models (VLM) for multimodal semantic highlight scoring and intelligent scene ranking."),
            ("Multilingual Subtitle Styling: ", "Support multilingual captions with animated kinetic fonts, custom color grading, and subtitle styling presets."),
            ("Dynamic Style & Genre Presets: ", "Add customizable visual templates (Phonk Edit, Travel Vlog, Lo-Fi Montage) and flexible aspect-ratio options."),
            ("Direct Social Media APIs: ", "Integrate OAuth publishing directly to YouTube Shorts and Instagram Reels with one-click automated export."),
            ("Conclusion: ", "Vibe-Cuts demonstrates that automated, beat-synced video editing and AI subtitling can run locally in web browsers via WebAssembly and AI, eliminating expensive cloud GPU costs while ensuring 100% user privacy.")
        ]

        for idx, (title, desc) in enumerate(future_items):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(10)
            p.line_spacing = 1.18
            
            r1 = p.add_run()
            r1.text = "• " + title
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(15.5)
            r1.font.bold = True
            r1.font.color.rgb = BLUE_ACCENT if "Conclusion" in title else HEADING_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(14.5)
            r2.font.bold = False
            r2.font.color.rgb = DARK_TEXT

    # Save to all destination paths
    save_targets = [
        r'C:\Users\ganap\Downloads\aishuamma.pptx',
        r'C:\Users\ganap\OneDrive\Desktop\aishuamma_clean.pptx',
        r'C:\Users\ganap\OneDrive\Desktop\aishuamma_corrected.pptx',
        os.path.join(os.path.dirname(__file__), 'aishuamma_clean.pptx'),
        os.path.join(os.path.dirname(__file__), 'aishuamma_corrected.pptx')
    ]

    for target in save_targets:
        try:
            prs.save(target)
            print(f" Saved: {target}")
        except PermissionError:
            print(f" Notice: {target} is currently open in PowerPoint. Skipped.")
        except Exception as e:
            print(f" Error saving {target}: {e}")

if __name__ == '__main__':
    realign_all()
