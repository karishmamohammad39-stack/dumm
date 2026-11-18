with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    text = f.read()

chapters = text.split("# CHAPTER ")
for idx, ch in enumerate(chapters):
    if idx == 0:
        continue
    title = ch.split("\n")[0]
    w = len(ch.split())
    print(f"Chapter {idx} ({title}): {w} words")
