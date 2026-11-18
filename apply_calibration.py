# -*- coding: utf-8 -*-
import subprocess
import json
import re

print("Running calibration script...")

with open("generate_word_doc.cjs", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update paragraph spacing after to 70
code = re.sub(r'after:\s*options\.after\s*!==\s*undefined\s*\?\s*options\.after\s*:\s*140',
              'after: options.after !== undefined ? options.after : 70', code)

# 2. Update imageFigure spacing
code = re.sub(r'spacing:\s*\{\s*before:\s*160,\s*after:\s*80\s*\}',
              'spacing: { before: 100, after: 40 }', code)
code = re.sub(r'spacing:\s*\{\s*before:\s*60,\s*after:\s*180\s*\}',
              'spacing: { before: 40, after: 100 }', code)

# 3. Compact TOC table rows and padding
code = re.sub(r'const tocRows\s*=\s*\[[\s\S]*?\];', '''// Dynamic/Calibrated Table of Contents
let tocRows = [
  ['1', 'INTRODUCTION', '1'],
  ['', '1.1 Overview and Background', '1'],
  ['', '1.2 Problem Definition and Limitations of Existing Solutions', '2'],
  ['', '1.3 Objectives of the Project', '2'],
  ['', '1.4 Scope and Feasibility of the Project', '3'],
  ['', '1.5 Organization of the Report', '3'],
  ['2', 'LITERATURE SURVEY', '4'],
  ['', '2.1 Theoretical Foundations of Audio-Visual Beat Synchronization', '4'],
  ['', '2.2 Survey of Existing Automated Video Editing Frameworks', '4'],
  ['', '2.3 Evolution of Web Computing: WebAssembly and Client-Side Media Processing', '5'],
  ['', '2.4 Deep Learning in Speech Recognition and Computer Vision', '5'],
  ['', '2.5 Comparative Literature Survey & Research Gap Analysis', '6'],
  ['3', 'SYSTEM ANALYSIS', '7'],
  ['', '3.1 Introduction', '7'],
  ['', '3.2 Existing System Analysis', '7'],
  ['', '3.3 Proposed System: The Client-First Decentralized Paradigm', '7'],
  ['', '3.4 Feasibility Study', '8'],
  ['', '3.5 System Architecture', '8'],
  ['', '3.6 System Requirements Specification (SRS)', '9'],
  ['4', 'SYSTEM DESIGN', '11'],
  ['', '4.1 Architectural Design Principles & Design Patterns', '11'],
  ['', '4.2 Comprehensive UML Modeling', '11'],
  ['', '4.3 Data Flow Modeling (DFD Level 0, Level 1 & Level 2)', '14'],
  ['', '4.4 Mathematical Formulations & Audio Digital Signal Processing', '14'],
  ['', '4.5 Dual-Pass FFmpeg WebAssembly Memory Architecture', '16'],
  ['', '4.6 Procedural VFX Mathematical Expressions & Filtergraph Compiler', '16'],
  ['', '4.7 Speech-to-Text Whisper Subtitle Engine', '17'],
  ['', '4.8 MediaPipe Dynamic 9:16 Face-Tracking Reframing', '17'],
  ['5', 'IMPLEMENTATION DETAILS', '18'],
  ['', '5.1 Technology Stack & Architectural Setup', '18'],
  ['', '5.2 Core Implementation Algorithms & Production Code', '18'],
  ['', '5.3 Web UI Component Architecture & Timeline Canvas', '22'],
  ['', '5.4 Cross-Origin Isolation & Security Configuration', '22'],
  ['6', 'SYSTEM TESTING & QUALITY ASSURANCE', '23'],
  ['', '6.1 Objectives and Test Strategy', '23'],
  ['', '6.2 Unit Testing', '23'],
  ['', '6.3 Integration Testing', '24'],
  ['', '6.4 Audio Beat Synchronization Validation', '24'],
  ['6.5', 'Whisper ASR Word Error Rate (WER) Evaluation', '25'],
  ['6.6', 'Performance, Memory & Stress Testing', '25'],
  ['6.7', 'Cross-Browser & Cross-Platform Compatibility Matrix', '26'],
  ['7', 'RESULTS AND DISCUSSION', '27'],
  ['', '7.1 Graphical User Interface Walkthrough & Features', '27'],
  ['', '7.2 Experimental Benchmark Results', '29'],
  ['', '7.3 Comparative Analysis with Commercial Platforms', '30'],
  ['', '7.4 Architectural Advantages & Technical Merits', '31'],
  ['', '7.5 Practical Industry & Commercial Applications', '31'],
  ['8', 'CONCLUSION AND FUTURE ENHANCEMENTS', '32'],
  ['', '8.1 Summary of Stage-I Contributions', '32'],
  ['', '8.2 Practical Engineering Limitations Identified', '32'],
  ['', '8.3 Future Scope & Stage-II Development Roadmap', '32'],
  ['9', 'REFERENCES', '33']
];''', code)

# 4. In academicTable, reduce row spacing if table is TOC or LOT
code = code.replace("spacing: { before: 50, after: 50 },\n            children: parseFormattedText(cellText, 21)",
                    "spacing: { before: 20, after: 20 },\n            children: parseFormattedText(cellText, 19)")

# 5. Image sizes scaled slightly to fit nicely on page
code = code.replace("'4.2.1': { file: 'figure_2.png', w: 500, h: 245", "'4.2.1': { file: 'figure_2.png', w: 480, h: 180")
code = code.replace("'4.2.2': { file: 'figure_3.png', w: 500, h: 215", "'4.2.2': { file: 'figure_3.png', w: 480, h: 175")
code = code.replace("'4.2.3': { file: 'figure_4.png', w: 500, h: 215", "'4.2.3': { file: 'figure_4.png', w: 480, h: 175")
code = code.replace("'4.2.4': { file: 'figure_5.png', w: 500, h: 225", "'4.2.4': { file: 'figure_5.png', w: 480, h: 175")

with open("generate_word_doc.cjs", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated generate_word_doc.cjs successfully.")
