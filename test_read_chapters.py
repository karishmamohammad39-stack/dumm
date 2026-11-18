# -*- coding: utf-8 -*-
import os
import sys
import re

print("========================================================")
print("Calibrating Project Report Documentation to ~40 Body Pages")
print("Balaji Institute of Technology & Science - CSE (Data Science)")
print("========================================================")

# Read the full current expanded report
with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    full_md = f.read()

# Separate preliminaries from body chapters
prelim_part = full_md[:full_md.find("# CHAPTER 1: INTRODUCTION")]
body_part = full_md[full_md.find("# CHAPTER 1: INTRODUCTION"):]

# Split into chapters
raw_chapters = re.split(r'(?=# CHAPTER \d+:)', body_part)
# raw_chapters[0] is empty or whitespace
chapters = [c.strip() for c in raw_chapters if c.strip()]

print(f"Loaded {len(chapters)} chapters.")
for idx, c in enumerate(chapters, 1):
    first_line = c.split("\n")[0]
    words = len(c.split())
    print(f"Chapter {idx}: {first_line} ({words} words)")
