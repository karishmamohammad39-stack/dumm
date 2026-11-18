# -*- coding: utf-8 -*-
"""
build_all_markdown.py
Assembles all chapters into Project_Report_Documentation.md.
"""

import os
from build_prelims import get_prelims_content
from build_ch1 import get_ch1_content
from build_ch2 import get_ch2_content
from build_ch3 import get_ch3_content
from build_ch4 import get_ch4_content
from build_ch5 import get_ch5_content
from build_ch6 import get_ch6_content
from build_ch7 import get_ch7_content
from build_ch8_refs import get_ch8_refs_content

out_path = "Project_Report_Documentation.md"

# First, read the first part of preliminary pages from generate_report_markdown.py
# (Cover, Inner Title, Certificate, Acknowledgement, Abstract)
with open("generate_report_markdown.py", "r", encoding="utf-8") as f:
    text = f.read()

# Extract the preliminary text inside f.write("""...""")
start_token = 'f.write("""'
end_token = '""")'
idx1 = text.find(start_token) + len(start_token)
idx2 = text.find(end_token, idx1)
first_prelims = text[idx1:idx2]

print("Assembling complete Project_Report_Documentation.md...")

full_content = (
    first_prelims +
    get_prelims_content() +
    "\n" + get_ch1_content() +
    "\n" + get_ch2_content() +
    "\n" + get_ch3_content() +
    "\n" + get_ch4_content() +
    "\n" + get_ch5_content() +
    "\n" + get_ch6_content() +
    "\n" + get_ch7_content() +
    "\n" + get_ch8_refs_content()
)

with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully generated {out_path} with {len(full_content)} characters and {len(full_content.split())} words.")
