# -*- coding: utf-8 -*-
import subprocess
import json
import re

print("Configuring exact 40-page layout...")

with open("generate_word_doc.cjs", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Compact table row font and spacing for TOC, LOF, LOT
code = code.replace(
    "spacing: { before: 20, after: 20 },\n            children: parseFormattedText(cellText, 19)",
    "spacing: { before: 10, after: 10 },\n            children: parseFormattedText(cellText, 17)"
)

# 2. Combine List of Figures and List of Tables on Page 6 (remove the PageBreak between them)
# Find prelimElements.push for LIST OF FIGURES and LIST OF TABLES
old_lof_lot = """prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('LIST OF FIGURES', { bold: true, size: 28 })]
  }),
  academicTable(['Figure.NO', 'CONTENTS', 'PAGE NO.'], lofRows, [15, 70, 15]),
  new Paragraph({ children: [new PageBreak()] })
);

// 7. List of Tables
const lotRows = [
  ['2.1', 'Comparative Literature Survey of Video Editing Systems', '8'],
  ['3.1', 'Hardware Requirements Specification', '13'],
  ['3.2', 'Software Requirements Specification', '14'],
  ['3.3', 'Functional Requirements Specification Matrix', '12'],
  ['3.4', 'Non-Functional Requirements & Performance Targets', '13'],
  ['4.1', 'Detailed Use Case Specification Matrix', '15'],
  ['4.2', 'Mathematical Filtergraph Transform Mapping Table', '22'],
  ['5.1', 'Software Module Decomposition and Responsibility Distribution', '24'],
  ['5.2', 'In-Browser SharedArrayBuffer Security Header Directives', '28'],
  ['6.1', 'Unit Test Cases Specification and Verification Results', '29'],
  ['6.2', 'System Integration Test Cases and End-to-End Validation', '30'],
  ['6.3', 'Whisper ASR Word Error Rate (WER) Acoustic Evaluation Matrix', '31'],
  ['6.4', 'Cross-Browser and Operating System Compatibility Matrix', '32'],
  ['7.1', 'Comprehensive Commercial Feature Matrix', '37'],
  ['7.2', 'Quantitative Rendering Performance and Latency Benchmarks', '36'],
  ['7.3', 'Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory)', '37']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [run('LIST OF TABLES', { bold: true, size: 28 })]
  }),
  academicTable(['Table.NO', 'CONTENTS', 'PAGE NO.'], lotRows, [15, 70, 15])
);"""

new_lof_lot = """// 6. List of Figures & 7. List of Tables (Formatted compactly on Page vi)
const lotRows = [
  ['2.1', 'Comparative Literature Survey of Video Editing Systems', '6'],
  ['3.1', 'Hardware Requirements Specification', '9'],
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
  ['6.4', 'Cross-Browser and Operating System Compatibility Matrix', '26'],
  ['7.1', 'Comprehensive Commercial Feature Matrix', '30'],
  ['7.2', 'Quantitative Rendering Performance and Latency Benchmarks', '29'],
  ['7.3', 'Memory Footprint Evaluation (WORKERFS vs MEMFS Linear Memory)', '30']
];

prelimElements.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 20, after: 60 },
    children: [run('LIST OF FIGURES', { bold: true, size: 24, color: COLOR_BLACK })]
  }),
  academicTable(['Figure.NO', 'CONTENTS', 'PAGE NO.'], lofRows, [15, 70, 15]),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [run('LIST OF TABLES', { bold: true, size: 24, color: COLOR_BLACK })]
  }),
  academicTable(['Table.NO', 'CONTENTS', 'PAGE NO.'], lotRows, [15, 70, 15])
);"""

if old_lof_lot in code:
    code = code.replace(old_lof_lot, new_lof_lot)
    print("Replaced LOF/LOT layout.")
else:
    print("LOF/LOT pattern not exact match, using regex replacement...")
    pattern = r'prelimElements\.push\(\s*new Paragraph\(\{\s*alignment: AlignmentType\.CENTER,\s*spacing: \{ before: 40, after: 120 \},\s*children: \[run\(\'LIST OF FIGURES\'[\s\S]*?academicTable\(\[\'Table\.NO\'[\s\S]*?\)\s*\);'
    code = re.sub(pattern, new_lof_lot, code)

with open("generate_word_doc.cjs", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved generate_word_doc.cjs.")
