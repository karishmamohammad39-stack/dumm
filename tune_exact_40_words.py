# -*- coding: utf-8 -*-
"""
tune_exact_40_words.py
Calibrates the markdown text to ~9,800 words so that
Section 2 is EXACTLY 40 pages in Microsoft Word.
"""

import os
import sys
import subprocess

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.stdout, p.stderr

with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    text = f.read()

current_words = len(text.split())
print(f"Current words: {current_words}")

# Target word count: ~9,800 words
# Let's adjust paragraphs or condense verbose sections slightly
# Let's see which sections can be concisely phrased without losing any technical depth or rigor:

# 1. In Chapter 3, condense SRS matrix descriptions slightly
# 2. In Chapter 4, keep all math and UML, condense narrative
# 3. In Chapter 5, keep code, condense explanations
# 4. In Chapter 6, keep tables, condense narrative
# 5. In Chapter 7, keep tables, condense narrative

# Let's measure word count after selective trimming:
trimmed_md = text

# Let's test a target word count of 9,800 words:
# We can create a dedicated script that builds the 9,800 word text directly
