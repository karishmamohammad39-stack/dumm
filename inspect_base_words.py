with open("generate_expanded_report_master.py", "r", encoding="utf-8") as f:
    code = f.read()

start_marker = 'md_report = r"""'
end_marker = '"""\n\n# Write out the Markdown file'
idx1 = code.find(start_marker) + len(start_marker)
idx2 = code.find(end_marker, idx1)
base_md = code[idx1:idx2]

print("Words in base_md:", len(base_md.split()))

# Let's count words per chapter in base_md
chapters = base_md.split("# CHAPTER ")
for idx, ch in enumerate(chapters):
    if idx == 0:
        print("Prelim:", len(ch.split()))
    else:
        title = ch.split("\n")[0]
        print(f"Chapter {idx} ({title}): {len(ch.split())} words")
