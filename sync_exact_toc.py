# -*- coding: utf-8 -*-
import json
import re

print("Synchronizing exact verified page numbers into DOCX and MD...")

# 1. Update generate_word_doc.cjs
with open("generate_word_doc.cjs", "r", encoding="utf-8") as f:
    code = f.read()

clean_toc = """let tocRows = [
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
  ['4', 'SYSTEM DESIGN', '12'],
  ['', '4.1 Architectural Design Principles & Design Patterns', '12'],
  ['', '4.2 Comprehensive UML Modeling', '12'],
  ['', '4.3 Data Flow Modeling (DFD Level 0, Level 1 & Level 2)', '15'],
  ['', '4.4 Mathematical Formulations & Audio Digital Signal Processing', '15'],
  ['', '4.5 Dual-Pass FFmpeg WebAssembly Memory Architecture', '16'],
  ['', '4.6 Procedural VFX Mathematical Expressions & Filtergraph Compiler', '16'],
  ['', '4.7 Speech-to-Text Whisper Subtitle Engine', '17'],
  ['', '4.8 MediaPipe Dynamic 9:16 Face-Tracking Reframing', '17'],
  ['5', 'IMPLEMENTATION DETAILS', '18'],
  ['', '5.1 Technology Stack & Architectural Setup', '18'],
  ['', '5.2 Core Implementation Algorithms & Production Code', '18'],
  ['', '5.3 Web UI Component Architecture & Timeline Canvas', '21'],
  ['', '5.4 Cross-Origin Isolation & Security Configuration', '22'],
  ['6', 'SYSTEM TESTING & QUALITY ASSURANCE', '23'],
  ['', '6.1 Objectives and Test Strategy', '23'],
  ['', '6.2 Unit Testing', '23'],
  ['', '6.3 Integration Testing', '24'],
  ['', '6.4 Audio Beat Synchronization Validation', '24'],
  ['', '6.5 Whisper ASR Word Error Rate (WER) Evaluation', '25'],
  ['', '6.6 Performance, Memory & Stress Testing', '25'],
  ['', '6.7 Cross-Browser & Cross-Platform Compatibility Matrix', '25'],
  ['7', 'RESULTS AND DISCUSSION', '26'],
  ['', '7.1 Graphical User Interface Walkthrough & Features', '26'],
  ['', '7.2 Experimental Benchmark Results', '28'],
  ['', '7.3 Comparative Analysis with Commercial Platforms', '29'],
  ['', '7.4 Architectural Advantages & Technical Merits', '29'],
  ['', '7.5 Practical Industry & Commercial Applications', '30'],
  ['8', 'CONCLUSION AND FUTURE ENHANCEMENTS', '30'],
  ['', '8.1 Summary of Stage-I Contributions', '30'],
  ['', '8.2 Practical Engineering Limitations Identified', '31'],
  ['', '8.3 Future Scope & Stage-II Development Roadmap', '31'],
  ['9', 'REFERENCES', '32']
];"""

clean_lof = """const lofRows = [
  ['3.3', 'Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process', '8'],
  ['3.4', 'High-Level Client-Server System Architecture of Vibe-Cuts', '8'],
  ['4.2.1', 'UML Use Case Diagram of the Vibe-Cuts System', '13'],
  ['4.2.2', 'UML Class Diagram Representing Core System Entities and Operations', '13'],
  ['4.2.3', 'UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render', '14'],
  ['4.2.4', 'UML Activity Diagram Depicting Parallel Multithreaded Processing', '14'],
  ['7.1.1', 'Project Ingestion & Asset Library Dashboard', '26'],
  ['7.1.2', 'HomeScreen & Main Video Studio Editor', '26'],
  ['7.1.3', 'Audio Waveform & Beat Visualizer Interface', '27'],
  ['7.1.4', 'Cinematic VFX & Filter Customization Panel', '27'],
  ['7.1.5', 'Kinetic Captions & Whisper Subtitle Inspector', '27'],
  ['7.1.6', 'WASM Export & Multi-Format Render Panel', '27'],
  ['7.2.1', 'Audio Transient Extraction & Beat Peak Alignment Waveform', '28'],
  ['7.2.2', 'Procedural Zoom & Glitch VFX Synchronization Waveform', '28'],
  ['7.2.3', 'Sub-Frame Subtitle Alignment & Word-Level Highlighting', '28'],
  ['7.2.4', 'System Performance Benchmark & Processing Latency Graph', '29']
];"""

clean_lot = """const lotRows = [
  ['2.1', 'Comparative Literature Survey of Video Editing Systems', '6'],
  ['3.1', 'Hardware Requirements Specification', '10'],
  ['3.2', 'Software Requirements Specification', '10'],
  ['3.3', 'Functional Requirements Specification Matrix', '9'],
  ['3.4', 'Non-Functional Requirements & Performance Targets', '9'],
  ['4.1', 'Detailed Use Case Specification Matrix', '12'],
  ['4.2', 'Mathematical Filtergraph Transform Mapping Table', '16'],
  ['5.1', 'Software Module Decomposition and Responsibility Distribution', '18'],
  ['5.2', 'In-Browser SharedArrayBuffer Security Header Directives', '22'],
  ['6.1', 'Unit Test Cases Specification and Verification Results', '23'],
  ['6.2', 'System Integration Test Cases and End-to-End Validation', '24'],
  ['6.3', 'Whisper ASR Word Error Rate (WER) Acoustic Evaluation Matrix', '25'],
  ['6.4', 'Cross-Browser and Operating System Compatibility Matrix', '25'],
  ['7.1', 'Comprehensive Commercial Feature Matrix', '29'],
  ['7.2', 'Quantitative Rendering Performance and Latency Benchmarks', '28'],
  ['7.3', 'Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory)', '29']
];"""

code = re.sub(r'let tocRows\s*=\s*\[[\s\S]*?\];', clean_toc, code)
code = re.sub(r'const lofRows\s*=\s*\[[\s\S]*?\];', clean_lof, code)
code = re.sub(r'const lotRows\s*=\s*\[[\s\S]*?\];', clean_lot, code)

with open("generate_word_doc.cjs", "w", encoding="utf-8") as f:
    f.write(code)

# 2. Update Project_Report_Documentation.md
with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    md = f.read()

md_toc = """# TABLE OF CONTENTS

S.NO | CONTENTS | PAGE NO.
1 | INTRODUCTION | 1
| 1.1 Overview and Background | 1
| 1.2 Problem Definition and Limitations of Existing Solutions | 2
| 1.3 Objectives of the Project | 2
| 1.4 Scope and Feasibility of the Project | 3
| 1.5 Organization of the Report | 3
2 | LITERATURE SURVEY | 4
| 2.1 Theoretical Foundations of Audio-Visual Beat Synchronization | 4
| 2.2 Survey of Existing Automated Video Editing Frameworks | 4
| 2.3 Evolution of Web Computing: WebAssembly and Client-Side Media Processing | 5
| 2.4 Deep Learning in Speech Recognition and Computer Vision | 5
| 2.5 Comparative Literature Survey & Research Gap Analysis | 6
3 | SYSTEM ANALYSIS | 7
| 3.1 Introduction | 7
| 3.2 Existing System Analysis | 7
| 3.3 Proposed System: The Client-First Decentralized Paradigm | 7
| 3.4 Feasibility Study | 8
| 3.5 System Architecture | 8
| 3.6 System Requirements Specification (SRS) | 9
4 | SYSTEM DESIGN | 12
| 4.1 Architectural Design Principles & Design Patterns | 12
| 4.2 Comprehensive UML Modeling | 12
| 4.3 Data Flow Modeling (DFD Level 0, Level 1 & Level 2) | 15
| 4.4 Mathematical Formulations & Audio Digital Signal Processing | 15
| 4.5 Dual-Pass FFmpeg WebAssembly Memory Architecture | 16
| 4.6 Procedural VFX Mathematical Expressions & Filtergraph Compiler | 16
| 4.7 Speech-to-Text Whisper Subtitle Engine | 17
| 4.8 MediaPipe Dynamic 9:16 Face-Tracking Reframing | 17
5 | IMPLEMENTATION DETAILS | 18
| 5.1 Technology Stack & Architectural Setup | 18
| 5.2 Core Implementation Algorithms & Production Code | 18
| 5.3 Web UI Component Architecture & Timeline Canvas | 21
| 5.4 Cross-Origin Isolation & Security Configuration | 22
6 | SYSTEM TESTING & QUALITY ASSURANCE | 23
| 6.1 Objectives and Test Strategy | 23
| 6.2 Unit Testing | 23
| 6.3 Integration Testing | 24
| 6.4 Audio Beat Synchronization Validation | 24
| 6.5 Whisper ASR Word Error Rate (WER) Evaluation | 25
| 6.6 Performance, Memory & Stress Testing | 25
| 6.7 Cross-Browser & Cross-Platform Compatibility Matrix | 25
7 | RESULTS AND DISCUSSION | 26
| 7.1 Graphical User Interface Walkthrough & Features | 26
| 7.2 Experimental Benchmark Results | 28
| 7.3 Comparative Analysis with Commercial Platforms | 29
| 7.4 Architectural Advantages & Technical Merits | 29
| 7.5 Practical Industry & Commercial Applications | 30
8 | CONCLUSION AND FUTURE ENHANCEMENTS | 30
| 8.1 Summary of Stage-I Contributions | 30
| 8.2 Practical Engineering Limitations Identified | 31
| 8.3 Future Scope & Stage-II Development Roadmap | 31
9 | REFERENCES | 32

---

# LIST OF FIGURES

Figure.NO | CONTENTS | PAGE NO.
3.3 | Functional Flow Chart of the Automated Highlight & Beat-Synced Generation Process | 8
3.4 | High-Level Client-Server System Architecture of Vibe-Cuts | 8
4.2.1 | UML Use Case Diagram of the Vibe-Cuts System | 13
4.2.2 | UML Class Diagram Representing Core System Entities and Operations | 13
4.2.3 | UML Sequence Diagram for Asynchronous Beat Extraction and Dual-Pass Render | 14
4.2.4 | UML Activity Diagram Depicting Parallel Multithreaded Processing | 14
7.1.1 | Project Ingestion & Asset Library Dashboard | 26
7.1.2 | HomeScreen & Main Video Studio Editor | 26
7.1.3 | Audio Waveform & Beat Visualizer Interface | 27
7.1.4 | Cinematic VFX & Filter Customization Panel | 27
7.1.5 | Kinetic Captions & Whisper Subtitle Inspector | 27
7.1.6 | WASM Export & Multi-Format Render Panel | 27
7.2.1 | Audio Transient Extraction & Beat Peak Alignment Waveform | 28
7.2.2 | Procedural Zoom & Glitch VFX Synchronization Waveform | 28
7.2.3 | Sub-Frame Subtitle Alignment & Word-Level Highlighting | 28
7.2.4 | System Performance Benchmark & Processing Latency Graph | 29

---

# LIST OF TABLES

Table.NO | CONTENTS | PAGE NO.
2.1 | Comparative Literature Survey of Video Editing Systems | 6
3.1 | Hardware Requirements Specification | 10
3.2 | Software Requirements Specification | 10
3.3 | Functional Requirements Specification Matrix | 9
3.4 | Non-Functional Requirements & Performance Targets | 9
4.1 | Detailed Use Case Specification Matrix | 12
4.2 | Mathematical Filtergraph Transform Mapping Table | 16
5.1 | Software Module Decomposition and Responsibility Distribution | 18
5.2 | In-Browser SharedArrayBuffer Security Header Directives | 22
6.1 | Unit Test Cases Specification and Verification Results | 23
6.2 | System Integration Test Cases and End-to-End Validation | 24
6.3 | Whisper ASR Word Error Rate (WER) Acoustic Evaluation Matrix | 25
6.4 | Cross-Browser and Operating System Compatibility Matrix | 25
7.1 | Comprehensive Commercial Feature Matrix | 29
7.2 | Quantitative Rendering Performance and Latency Benchmarks | 28
7.3 | Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory) | 29"""

md = re.sub(r'# TABLE OF CONTENTS[\s\S]*?(?=# CHAPTER 1: INTRODUCTION)', md_toc + '\n\n---\n\n', md)

with open("Project_Report_Documentation.md", "w", encoding="utf-8") as f:
    f.write(md)

print("Synchronized Table of Contents and Lists successfully.")
