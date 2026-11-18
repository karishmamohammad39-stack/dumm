import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def fix_presentation():
    src_path = r'C:\Users\ganap\Downloads\aishuamma.pptx'
    prs = Presentation(src_path)

    HEADER_BG = RGBColor(30, 58, 138)      # Deep Royal Navy #1e3a8a
    HEADER_TEXT = RGBColor(255, 255, 255)  # Pure White
    ROW_BG_ALT = RGBColor(241, 245, 249)   # Light Slate Tint #f1f5f9
    ROW_BG_WHITE = RGBColor(255, 255, 255) # Pure White
    TEXT_DARK = RGBColor(15, 23, 42)       # High Contrast Slate #0f172a
    ACCENT_BLUE = RGBColor(29, 78, 216)    # Crisp Blue #1d4ed8
    TEXT_RED = RGBColor(185, 28, 28)       # Crimson Accent for Limitations #b91c1c
    TEXT_GREEN = RGBColor(4, 120, 87)      # Emerald Accent for Solutions #047857

    # =========================================================================
    # SLIDE 5: Literature Survey (5 Key Research Papers)
    # =========================================================================
    s5 = prs.slides[4]
    
    # Remove all old tables/placeholders on slide 5
    to_remove = [s for s in s5.shapes if s.has_table or (s.has_text_frame and s != s5.shapes[0])]
    for s in to_remove:
        sp = s._element
        sp.getparent().remove(sp)

    # Title
    t_shape = s5.shapes[0]
    t_shape.left = Inches(0.8)
    t_shape.top = Inches(0.35)
    t_shape.width = Inches(11.733)
    t_shape.height = Inches(0.7)
    tf = t_shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = "4. Literature Survey (5 Key Research Papers)"
    r.font.name = "Times New Roman"
    r.font.size = Pt(25)
    r.font.bold = True
    r.font.color.rgb = TEXT_DARK

    # Add brand new 6x5 Table
    t_shape5 = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.15), Inches(11.733), Inches(5.8))
    t5 = t_shape5.table
    
    # Set column widths
    t5.columns[0].width = Inches(2.3)
    t5.columns[1].width = Inches(2.7)
    t5.columns[2].width = Inches(1.6)
    t5.columns[3].width = Inches(2.5)
    t5.columns[4].width = Inches(2.633)

    headers_s5 = ["Paper Title & Author", "Methodology / Model", "Dataset Used", "Key Advantages", "Identified Limitations"]
    for c_idx, h_text in enumerate(headers_s5):
        cell = t5.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        cell.margin_left = cell.margin_right = Inches(0.08)
        cell.margin_top = cell.margin_bottom = Inches(0.05)
        cell.text = h_text
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)
                run.font.bold = True
                run.font.color.rgb = HEADER_TEXT

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
                        run.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: Overcoming Limitations of Existing Work
    # =========================================================================
    s6 = prs.slides[5]

    # Remove all old tables/placeholders on slide 6
    to_remove_s6 = [s for s in s6.shapes if s.has_table or (s.has_text_frame and s != s6.shapes[0])]
    for s in to_remove_s6:
        sp = s._element
        sp.getparent().remove(sp)

    # Title
    t_shape6 = s6.shapes[0]
    t_shape6.left = Inches(0.8)
    t_shape6.top = Inches(0.35)
    t_shape6.width = Inches(11.733)
    t_shape6.height = Inches(0.7)
    tf6 = t_shape6.text_frame
    tf6.clear()
    p6 = tf6.paragraphs[0]
    p6.alignment = PP_ALIGN.LEFT
    r6 = p6.add_run()
    r6.text = "5. Overcoming Limitations of Existing Work"
    r6.font.name = "Times New Roman"
    r6.font.size = Pt(25)
    r6.font.bold = True
    r6.font.color.rgb = TEXT_DARK

    # Add brand new 6x3 Table
    t_shape6 = s6.shapes.add_table(6, 3, Inches(0.8), Inches(1.15), Inches(11.733), Inches(5.8))
    t6 = t_shape6.table
    
    t6.columns[0].width = Inches(2.8)
    t6.columns[1].width = Inches(4.3)
    t6.columns[2].width = Inches(4.633)

    headers_s6 = ["Existing Approach / Work", "Identified Limitation", "How Vibe-Cuts Overcomes It"]
    for c_idx, h_text in enumerate(headers_s6):
        cell = t6.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        cell.margin_left = cell.margin_right = Inches(0.1)
        cell.margin_top = cell.margin_bottom = Inches(0.06)
        cell.text = h_text
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13.5)
                run.font.bold = True
                run.font.color.rgb = HEADER_TEXT

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
                    elif c_idx == 1:
                        run.font.size = Pt(12.5)
                        run.font.bold = False
                        run.font.color.rgb = TEXT_DARK
                    else:
                        run.font.size = Pt(12.5)
                        run.font.bold = False
                        run.font.color.rgb = TEXT_DARK

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
            print(f" Successfully saved: {target}")
        except PermissionError:
            print(f" Notice: {target} is currently open in PowerPoint. Skipped.")
        except Exception as e:
            print(f" Error saving {target}: {e}")

if __name__ == '__main__':
    fix_presentation()
