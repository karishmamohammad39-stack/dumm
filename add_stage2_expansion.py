# -*- coding: utf-8 -*-
with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    text = f.read()

chap8_expansion = """
4. **Decentralized Collaborative Real-Time Timeline Synchronizer:**
   In addition to on-device audio demixing and WebGPU acceleration, Stage-II will incorporate WebRTC data channels and CRDTs (Conflict-free Replicated Data Types) to support multi-user collaborative editing sessions. Content creation teams will be able to review, trim, and annotate highlight markers concurrently across distributed web browsers with sub-50ms peer-to-peer state synchronization, without routing video payloads through central proxy servers.
5. **Generative Multimodal B-Roll Insert Engine:**
   Stage-II will explore integrating quantized diffusion and vision-language models executing locally on client NPU hardware (e.g., Apple Neural Engine, Intel AI Boost). When acoustic pauses or thematic topic shifts are identified in the spoken dialogue, the engine will automatically suggest or procedurally generate relevant vertical B-roll inserts, transitions, and kinetic visual stickers to maintain maximum viewer retention.
"""

if "4. **Decentralized Collaborative Real-Time Timeline Synchronizer:**" not in text:
    text = text.replace("---", chap8_expansion + "\n---\n", 1)  # replace before chapter 9
    # Actually let's place it right before Chapter 9
    pos = text.find("# CHAPTER 9: REFERENCES")
    text = text[:pos] + chap8_expansion + "\n---\n\n" + text[pos:]

with open("Project_Report_Documentation.md", "w", encoding="utf-8") as f:
    f.write(text)

words = len(text.split())
print(f"Enriched Chapter 8. Total Words: {words}")
