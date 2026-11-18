import os
search_dir = r"c:\Users\ganap\OneDrive\Desktop\reel\teamwork_projects\vibe_cuts_engine\src"
with open(r"c:\Users\ganap\OneDrive\Desktop\reel\.agents\explorer_27\search_dummy.txt", "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(search_dir):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as infile:
                    for i, line in enumerate(infile):
                        if "dummy" in line.lower() or "mock" in line.lower():
                            out.write(f"{path}:{i+1}:{line}\n")
