import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_presentation_from_review1():
    src_path = r'C:\Users\ganap\Downloads\aishuamma.pptx'
    prs = Presentation(src_path)

    # Color Palette matching Review 1 & Premium academic theme
    TITLE_COLOR = RGBColor(30, 30, 30)      # #1E1E1E
    PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1E3A8A Deep Navy
    TEXT_MAIN = RGBColor(30, 30, 30)       # #1E1E1E Charcoal
    WHITE = RGBColor(255, 255, 255)
    ROW_BG_ALT = RGBColor(241, 245, 249)   # #F1F5F9
    ROW_BG_WHITE = RGBColor(255, 255, 255)
    ACCENT_BLUE = RGBColor(29, 78, 216)    # #1D4ED8

    def format_title(shape, text, size_pt=26):
        shape.left = Inches(0.8)
        shape.top = Inches(0.4)
        shape.width = Inches(11.733)
        shape.height = Inches(0.75)
        if shape.has_text_frame:
            tf = shape.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = text
            r.font.name = "Times New Roman"
            r.font.size = Pt(size_pt)
            r.font.bold = True
            r.font.color.rgb = TITLE_COLOR

    # =========================================================================
    # SLIDE 1: Title Slide (Full names & roll numbers from Review 1)
    # =========================================================================
    s1 = prs.slides[0]
    
    # Adjust logo/banner if present
    for sh in s1.shapes:
        if sh.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            sh.left = Inches(1.8)
            sh.top = Inches(0.25)
            sh.width = Inches(9.733)
            sh.height = Inches(1.7)

    # Main Title Shape
    if len(s1.shapes) > 0 and s1.shapes[0].has_text_frame:
        sh = s1.shapes[0]
        sh.left = Inches(0.8)
        sh.top = Inches(2.15)
        sh.width = Inches(11.733)
        sh.height = Inches(1.9)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.clear()

        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = "BALAJI INSTITUTE OF TECHNOLOGY & SCIENCE"
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(16)
        r0.font.bold = True
        r0.font.color.rgb = PRIMARY_BLUE

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)\nMAJOR PROJECT STAGE-I | PROJECT REVIEW – II (2026-2027)"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12.5)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_MAIN
        p1.space_before = Pt(4)
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = "Vibe-Cuts: Automated AI Video Editing Engine"
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(27)
        r2.font.bold = True
        r2.font.color.rgb = TITLE_COLOR

    # Team Members Label
    if len(s1.shapes) > 2 and s1.shapes[2].has_text_frame:
        sh = s1.shapes[2]
        sh.left = Inches(0.8)
        sh.top = Inches(4.35)
        sh.width = Inches(6.5)
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
        r.font.color.rgb = PRIMARY_BLUE

    # Team Members Table (Review 1 format: Full Surnames & Roll Numbers)
    if len(s1.shapes) > 1 and s1.shapes[1].has_table:
        sh = s1.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(4.75)
        sh.width = Inches(6.8)
        sh.height = Inches(1.9)
        t = sh.table
        t.columns[0].width = Inches(4.4)
        t.columns[1].width = Inches(2.4)

        team_members_r1 = [
            ("23C31A6746", "KATHULA AISHWARYA"),
            ("23C31A6719", "BURA ALEKHYA"),
            ("23C31A6733", "GANAPARAPU SAHAN"),
            ("23C31A6730", "ENAKONDA VISHNUVARDHAN REDDY")
        ]
        for r_idx, (roll, name) in enumerate(team_members_r1):
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
                        r.font.size = Pt(13.5)
                        r.font.bold = True
                        r.font.color.rgb = TEXT_MAIN

    # Guide Table
    if len(s1.shapes) > 4 and s1.shapes[4].has_table:
        sh = s1.shapes[4]
        sh.left = Inches(8.3)
        sh.top = Inches(4.75)
        sh.width = Inches(4.2)
        sh.height = Inches(1.4)
        t = sh.table
        t.columns[0].width = Inches(4.2)
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
                    r.font.size = Pt(14 if r_idx == 0 else 13.5)
                    r.font.bold = (r_idx == 0 or p_idx == 0)
                    r.font.color.rgb = PRIMARY_BLUE if r_idx == 0 else TEXT_MAIN

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    s2 = prs.slides[1]
    format_title(s2.shapes[0], "1. Problem Statement")
    
    if len(s2.shapes) > 1 and s2.shapes[1].has_text_frame:
        sh = s2.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(1.35)
        sh.width = Inches(11.733)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
        tf.clear()

        problems = [
            ("Time-Consuming Manual Editing: ", "Converting long-form videos into short reels requires watching, selecting, and trimming content manually with significant effort."),
            ("Difficult Highlight Identification: ", "Creators struggle to identify the most engaging or meaningful moments in lengthy videos without automated AI analysis."),
            ("Beat Synchronization Complexity: ", "Aligning cuts, zoom punches, and visual effects to musical drops requires tedious frame-by-frame keyframing in desktop editors."),
            ("Manual Subtitle Creation: ", "Preparing, synchronizing timestamps, and styling captions adds heavy editing overhead."),
            ("Tool Fragmentation & Cloud Privacy: ", "Existing solutions require multiple disconnected tools and cloud uploads of gigabytes of raw video, causing latency and privacy risks.")
        ]

        for idx, (head, desc) in enumerate(problems):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(12)
            p.line_spacing = 1.2
            
            r1 = p.add_run()
            r1.text = "• " + head
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(17)
            r1.font.bold = True
            r1.font.color.rgb = TITLE_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(16)
            r2.font.bold = False
            r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 3: Objectives & Target Audience
    # =========================================================================
    s3 = prs.slides[2]
    format_title(s3.shapes[0], "2. Objectives & Target Audience")
    
    if len(s3.shapes) > 1 and s3.shapes[1].has_text_frame:
        sh = s3.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(1.35)
        sh.width = Inches(11.733)
        sh.height = Inches(5.6)
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.05)
        tf.clear()

        # Target Audience
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = "Target Users & Beneficiaries:"
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(18)
        r0.font.bold = True
        r0.font.color.rgb = PRIMARY_BLUE
        p0.space_after = Pt(4)

        users = [
            "Content creators, YouTubers, and podcasters seeking automated short-form reels.",
            "Social-media managers and digital marketers managing multi-platform channels.",
            "Students, educators, and general creators needing quick highlight summaries."
        ]
        for u in users:
            p = tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(3)
            r = p.add_run()
            r.text = "  • " + u
            r.font.name = "Times New Roman"
            r.font.size = Pt(15.5)
            r.font.color.rgb = TEXT_MAIN

        # Objectives
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        p1.space_before = Pt(12)
        p1.space_after = Pt(4)
        r1 = p1.add_run()
        r1.text = "Key Project Objectives:"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(18)
        r1.font.bold = True
        r1.font.color.rgb = PRIMARY_BLUE

        objectives = [
            ("Automated Highlight Extraction: ", "Intelligently slice dynamic highlight segments from raw long-form footage."),
            ("Client-Side Beat Detection: ", "Isolate bass kick transients (<150Hz) using Web Audio API for rhythm synchronization."),
            ("AI Speech Transcription: ", "Generate millisecond-accurate synchronized captions via OpenAI Whisper."),
            ("Procedural CapCut-Style VFX: ", "Synthesize beat-synced zoom punches, flashbangs, and hype typography."),
            ("100% In-Browser Rendering: ", "Leverage WebAssembly (FFmpeg WASM) to eliminate cloud GPU server costs & protect privacy."),
            ("Editing Time Reduction: ", "Reduce manual short-form editing turnaround time by over 80%.")
        ]
        for head, desc in objectives:
            p = tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(3)
            
            r_h = p.add_run()
            r_h.text = "  • " + head
            r_h.font.name = "Times New Roman"
            r_h.font.size = Pt(15.5)
            r_h.font.bold = True
            r_h.font.color.rgb = TITLE_COLOR
            
            r_d = p.add_run()
            r_d.text = desc
            r_d.font.name = "Times New Roman"
            r_d.font.size = Pt(15)
            r_d.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 4: Requirements Gathering & Specifications
    # =========================================================================
    s4 = prs.slides[3]
    format_title(s4.shapes[0], "3. Requirements Gathering & Specifications")

    if len(s4.shapes) > 1 and s4.shapes[1].has_text_frame:
        sh1 = s4.shapes[1]
        sh1.left = Inches(0.8)
        sh1.top = Inches(1.35)
        sh1.width = Inches(5.7)
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
        r_h.font.size = Pt(18)
        r_h.font.bold = True
        r_h.font.color.rgb = PRIMARY_BLUE
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
            run.font.size = Pt(14.5)
            run.font.color.rgb = TEXT_MAIN

    if len(s4.shapes) > 2 and s4.shapes[2].has_text_frame:
        sh2 = s4.shapes[2]
        sh2.left = Inches(6.8)
        sh2.top = Inches(1.35)
        sh2.width = Inches(5.7)
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
        r_h.font.size = Pt(18)
        r_h.font.bold = True
        r_h.font.color.rgb = PRIMARY_BLUE
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
            run.font.size = Pt(14.5)
            run.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 5: Literature Survey (Large 13pt Table)
    # =========================================================================
    s5 = prs.slides[4]
    to_remove = [s for s in s5.shapes if s.has_table or (s.has_text_frame and s != s5.shapes[0])]
    for s in to_remove:
        sp = s._element
        sp.getparent().remove(sp)

    format_title(s5.shapes[0], "4. Literature Survey (5 Key Research Papers)", size_pt=25)

    t_shape5 = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.15), Inches(11.733), Inches(5.8))
    t5 = t_shape5.table
    t5.columns[0].width = Inches(2.3)
    t5.columns[1].width = Inches(2.7)
    t5.columns[2].width = Inches(1.6)
    t5.columns[3].width = Inches(2.5)
    t5.columns[4].width = Inches(2.633)

    headers_s5 = ["Paper Title & Author", "Methodology / Model", "Dataset Used", "Key Advantages", "Identified Limitations"]
    for c_idx, h_text in enumerate(headers_s5):
        cell = t5.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.05)
        cell.text = h_text
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)
                run.font.bold = True
                run.font.color.rgb = WHITE

    papers_data = [
        (
            "Han et al. (2024)\nCLIP Video Highlight",
            "CLIP-based multimodal feature learning for highlight detection",
            "QVHighlights",
            "Strong highlight detection using pretrained multimodal knowledge",
            "Highlight detection only; no automated clip editing or VFX"
        ),
        (
            "Xie et al. (2024)\nMultimodal Summarizer",
            "Knowledge-aware multimodal network using visual & audio cues",
            "Public Summarization Benchmarks",
            "Integrates external knowledge; improves summarization baseline",
            "Complex processing; lacks social-media 9:16 vertical formatting"
        ),
        (
            "Argaw et al. (2024)\nLLM Video Summarization",
            "LLM-assisted long-form video summarization pretraining",
            "Long-Form Video Corpus",
            "Captures deep narrative context and long-range dependencies",
            "High computational demand; requires massive GPU clusters"
        ),
        (
            "Ren et al. (2024)\nTimeChat Multimodal LLM",
            "Time-sensitive multimodal LLM for long-video understanding",
            "Long-Video Benchmarks",
            "Accurate temporal localization and multimodal reasoning",
            "High inference latency; unsuitable for browser/edge deployment"
        ),
        (
            "Sul et al. (2023)\nMr. HiSum Benchmark",
            "Joint highlight detection and video summarization benchmark",
            "31,892 Diverse Videos",
            "Provides standardized large-scale multimodal evaluation",
            "Benchmark only; not an end-to-end automated reel generator"
        )
    ]

    for r_idx, row in enumerate(papers_data, 1):
        bg_color = ROW_BG_ALT if r_idx % 2 == 1 else ROW_BG_WHITE
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.text = val
            for p_idx, p in enumerate(cell.text_frame.paragraphs):
                p.alignment = PP_ALIGN.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    if c_idx == 0:
                        run.font.size = Pt(12.5)
                        run.font.bold = True
                        run.font.color.rgb = ACCENT_BLUE
                    else:
                        run.font.size = Pt(12)
                        run.font.bold = False
                        run.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 6: Overcoming Limitations of Existing Work (Large 13.5pt Table)
    # =========================================================================
    s6 = prs.slides[5]
    to_remove_s6 = [s for s in s6.shapes if s.has_table or (s.has_text_frame and s != s6.shapes[0])]
    for s in to_remove_s6:
        sp = s._element
        sp.getparent().remove(sp)

    format_title(s6.shapes[0], "5. Overcoming Limitations of Existing Work", size_pt=25)

    t_shape6 = s6.shapes.add_table(6, 3, Inches(0.8), Inches(1.15), Inches(11.733), Inches(5.8))
    t6 = t_shape6.table
    t6.columns[0].width = Inches(2.8)
    t6.columns[1].width = Inches(4.3)
    t6.columns[2].width = Inches(4.633)

    headers_s6 = ["Existing Approach / Work", "Identified Limitation", "How Vibe-Cuts Overcomes It"]
    for c_idx, h_text in enumerate(headers_s6):
        cell = t6.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        cell.margin_left = cell.margin_right = Inches(0.1)
        cell.margin_top = cell.margin_bottom = Inches(0.06)
        cell.text = h_text
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13.5)
                run.font.bold = True
                run.font.color.rgb = WHITE

    solutions_data = [
        (
            "Video Highlight Detection",
            "Identifies important timestamps only; does not produce a finished edited video.",
            "Vibe-Cuts uses highlight detection as a core stage in an end-to-end pipeline that outputs completed 9:16 reels."
        ),
        (
            "Video Summarization Methods",
            "Generates basic content summaries without music beat-sync, visual effects, or 9:16 layout.",
            "Vibe-Cuts converts highlights into vertical reels with beat-synced cuts, zoom punches, and procedural hype VFX."
        ),
        (
            "Speech-to-Text / Captions",
            "Generates text transcripts without automated video cutting or audio rhythm alignment.",
            "Vibe-Cuts integrates Whisper speech-to-text with auto-burned captions and beat-synchronized video pacing."
        ),
        (
            "Heavy Multimodal LLMs",
            "Requires complex cloud pipelines, massive GPU resources, and high latency.",
            "Vibe-Cuts uses a lightweight client-side architecture combining Web Audio API and in-browser WebAssembly."
        ),
        (
            "Manual Video Editing Tools",
            "Requires creators to manually trim, caption, keyframe, and sync audio in complex desktop NLEs.",
            "Vibe-Cuts automates highlight selection, clipping, captioning, VFX, and 9:16 formatting in one unified workflow."
        )
    ]

    for r_idx, row in enumerate(solutions_data, 1):
        bg_color = ROW_BG_ALT if r_idx % 2 == 1 else ROW_BG_WHITE
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.text = val
            for p_idx, p in enumerate(cell.text_frame.paragraphs):
                p.alignment = PP_ALIGN.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    if c_idx == 0:
                        run.font.size = Pt(13)
                        run.font.bold = True
                        run.font.color.rgb = ACCENT_BLUE
                    else:
                        run.font.size = Pt(12.5)
                        run.font.bold = False
                        run.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 7: Research Gap & Novelty
    # =========================================================================
    s7 = prs.slides[6]
    format_title(s7.shapes[0], "6. Research Gap & Novelty")

    if len(s7.shapes) > 1 and s7.shapes[1].has_text_frame:
        sh = s7.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(1.35)
        sh.width = Inches(11.733)
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
            r1.font.size = Pt(16.5)
            r1.font.bold = True
            r1.font.color.rgb = PRIMARY_BLUE if "Novelty" in title else TITLE_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15.5)
            r2.font.bold = False
            r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 8: Proposed Methodology
    # =========================================================================
    s8 = prs.slides[7]
    format_title(s8.shapes[0], "7. Proposed Methodology & Architecture")

    if len(s8.shapes) > 1 and s8.shapes[1].has_text_frame:
        sh = s8.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(1.35)
        sh.width = Inches(11.733)
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
            r1.font.size = Pt(16.5)
            r1.font.bold = True
            r1.font.color.rgb = PRIMARY_BLUE
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15.5)
            r2.font.bold = False
            r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 9: Tools, Technologies & Datasets
    # =========================================================================
    s9 = prs.slides[8]
    format_title(s9.shapes[0], "8. Tools, Technologies & Datasets")

    if len(s9.shapes) > 2 and s9.shapes[2].has_text_frame:
        s9.shapes[2].text_frame.clear()
        s9.shapes[2].width = 0
        s9.shapes[2].height = 0

    col_configs_s9 = [
        (1, Inches(0.8), "Frontend & In-Browser", [
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
            sh.width = Inches(3.7)
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
            r_h.font.size = Pt(18)
            r_h.font.bold = True
            r_h.font.color.rgb = PRIMARY_BLUE
            p_h.space_after = Pt(8)

            for it in items:
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT
                p.space_after = Pt(5)
                p.line_spacing = 1.15
                r = p.add_run()
                r.text = "• " + it
                r.font.name = "Times New Roman"
                r.font.size = Pt(14.5)
                r.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 10: Work Completed
    # =========================================================================
    s10 = prs.slides[9]
    format_title(s10.shapes[0], "9. Work Completed (Major Project Stage-I)")

    col_configs_s10 = [
        (1, Inches(0.8), "Frontend Interface", [
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
            sh.width = Inches(3.7)
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
            r_h.font.size = Pt(18)
            r_h.font.bold = True
            r_h.font.color.rgb = PRIMARY_BLUE
            p_h.space_after = Pt(8)

            for it in items:
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT
                p.space_after = Pt(5)
                p.line_spacing = 1.15
                r = p.add_run()
                r.text = "• " + it
                r.font.name = "Times New Roman"
                r.font.size = Pt(14.5)
                r.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 11: Future Work & Conclusion
    # =========================================================================
    s11 = prs.slides[10]
    format_title(s11.shapes[0], "10. Future Work (Stage-II Roadmap) & Conclusion", size_pt=24)

    if len(s11.shapes) > 1 and s11.shapes[1].has_text_frame:
        sh = s11.shapes[1]
        sh.left = Inches(0.8)
        sh.top = Inches(1.35)
        sh.width = Inches(11.733)
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
            r1.font.size = Pt(16)
            r1.font.bold = True
            r1.font.color.rgb = PRIMARY_BLUE if "Conclusion" in title else TITLE_COLOR
            
            r2 = p.add_run()
            r2.text = desc
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(15)
            r2.font.bold = False
            r2.font.color.rgb = TEXT_MAIN

    # Save to all target files
    save_targets = [
        r'C:\Users\ganap\Downloads\aishuamma.pptx',
        r'C:\Users\ganap\OneDrive\Desktop\Review2_Presentation_Final.pptx',
        r'C:\Users\ganap\OneDrive\Desktop\aishuamma_clean.pptx',
        r'C:\Users\ganap\OneDrive\Desktop\aishuamma_corrected.pptx',
        os.path.join(os.path.dirname(__file__), 'Review2_Presentation_Final.pptx')
    ]

    for target in save_targets:
        try:
            prs.save(target)
            print(f" Saved: {target}")
        except PermissionError:
            print(f" Notice: {target} open in PowerPoint, skipping.")
        except Exception as e:
            print(f" Error saving {target}: {e}")

if __name__ == '__main__':
    update_presentation_from_review1()
