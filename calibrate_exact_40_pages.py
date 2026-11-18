# -*- coding: utf-8 -*-
"""
calibrate_exact_40_pages.py
Generates the ~9,800-word version of Project_Report_Documentation.md,
compiles Project_Report_Documentation.docx, and verifies the Word COM page count.
"""

import os
import sys
import subprocess
import json

# Let's read the 12,519 word text from Project_Report_Documentation.md
with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    text = f.read()

words = len(text.split())
print(f"Initial Word Count: {words}")

# We will write out a tailored ~9,800 word version that keeps all technical substance,
# all tables (Table 2.1, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3),
# all figures (3.1, 3.2, 4.1, 4.2, 4.3, 4.4, 7.1 to 7.10), all math, and all algorithms!
