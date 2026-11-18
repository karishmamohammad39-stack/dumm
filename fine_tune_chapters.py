# -*- coding: utf-8 -*-
"""
fine_tune_chapters.py
Fine-tunes Chapter 1, 2, and 3 to reduce ~900 words total,
targeting EXACTLY 40 body pages.
"""

import os
import sys

with open("Project_Report_Documentation.md", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see the current word count
print("Current words:", len(text.split()))

# 1. Streamline Chapter 1 (~280 words trimmed)
ch1_old = """The contemporary digital media landscape has experienced a profound architectural transformation driven by the proliferation of mobile-first, short-form vertical video formats (9:16 aspect ratio). Platforms such as Instagram Reels, YouTube Shorts, TikTok, and Snapchat Spotlight dominate consumer attention, generating over 140 billion daily video views across global social networks. In this hyper-competitive micro-attention economy, audience viewing psychology is characterized by rapid cognitive filtering. Empirical user behavior studies demonstrate that viewers form decisive judgments regarding whether to continue watching or swipe away within an initial interaction window of merely 1.7 to 2.5 seconds.

Consequently, content creators, digital marketing agencies, commercial brand strategists, and multimedia producers are under extraordinary pressure to produce high-energy, aesthetically engaging video narratives that immediately seize and sustain human attention. Modern video pacing relies fundamentally on multimodal perceptual cohesion—the precise temporal and rhythmic harmonization between acoustic stimuli and visual transformations. Cognitive science and psychoacoustic literature confirms that videos featuring visual transitions, punch-in camera zooms, chromatic visual glitches, and animated typography synchronized exactly with musical downbeats and bass transients achieve up to 3.2 times greater audience retention and 4.5 times higher social interaction rates than unsynchronized, static video presentations.

The historical trajectory of multimedia editing reveals an ongoing evolution of technological paradigms. During the analog era, video editing was strictly linear and hardware-bound, demanding physical tape splicing and analog mixing consoles. The digital revolution of the 1990s introduced Non-Linear Editing (NLE) software running on desktop workstations, such as Adobe Premiere Pro, Apple Final Cut Pro, and Avid Media Composer. While NLEs democratized digital video post-production by providing track-based timelines, keyframe animators, and procedural filter graphs, they remain inherently complex, labor-intensive, and steep in learning curves.

In recent years, the market witnessed the emergence of cloud-based Software-as-a-Service (SaaS) automated editing platforms (e.g., CapCut Web, Opus Clip, Descript). These cloud suites seek to automate highlight generation by shifting video processing from local desktop computers to remote server farms. However, as analyzed in the subsequent section, this centralized cloud paradigm introduces severe infrastructural bottlenecks, privacy violations, operational expense, and bandwidth throttling. This project introduces **Vibe-Cuts (Reel)**, an innovative client-first paradigm that bridges the gap between desktop computational autonomy and web-based zero-installation accessibility. By harnessing client-side WebAssembly (WASM), in-browser Web Audio digital signal processing (DSP), and procedural filtergraph compilers, Vibe-Cuts delivers professional beat-synchronized editing directly within the user's web browser without transmitting a single byte of video data across the public internet."""

ch1_new = """The contemporary digital media landscape has experienced a profound transformation driven by the proliferation of mobile-first, short-form vertical video formats (9:16 aspect ratio). Platforms such as Instagram Reels, YouTube Shorts, TikTok, and Snapchat Spotlight dominate global consumer attention, generating over 140 billion daily video views. In this hyper-competitive micro-attention economy, audience viewing psychology is characterized by rapid cognitive filtering, where viewers form decisive swipe-away judgments within an initial window of merely 1.7 to 2.5 seconds.

Consequently, content creators and media producers face immense pressure to produce rhythmically engaging narratives that immediately sustain audience attention. Modern video pacing relies fundamentally on multimodal perceptual cohesion—the precise temporal alignment between acoustic stimuli and visual transformations. Cognitive psychoacoustics confirms that video transitions, camera zooms, and visual glitches synchronized precisely with musical downbeats achieve up to 3.2 times greater audience retention than unsynchronized presentations.

While desktop Non-Linear Editors (NLEs) provide professional timelines, they remain steep in learning curves and labor-intensive. Conversely, modern cloud-based automated suites (e.g., CapCut Web, Opus Clip) introduce severe bandwidth throttling, privacy violations, and expensive server subscriptions. This project introduces **Vibe-Cuts (Reel)**: an innovative client-first web paradigm that harnesses WebAssembly (WASM), in-browser Web Audio digital signal processing (DSP), and procedural filtergraph compilers to deliver professional beat-synchronized editing directly within standard web browsers without transmitting video data over the network."""

text = text.replace(ch1_old, ch1_new)

# 2. Streamline Chapter 2 (~300 words trimmed)
ch2_old = """Audio-visual synchronization represents a core requirement in multimedia production, psychoacoustics, and computational media design. Human perception does not process auditory and visual stimuli in isolation; rather, the human brain actively binds multisensory signals through multimodal temporal integration mechanisms located in the superior colliculus and temporal cortical networks. Groundbreaking cognitive psychophysics research by Vroomen and de Gelder [13] established that human observers possess acute sensitivity to multimodal temporal alignment. When visual cuts, camera transitions, or lighting changes deviate from salient musical beats by more than 40 to 80 milliseconds, viewers experience noticeable perceptual disfluency, which breaks cognitive immersion and diminishes emotional narrative engagement. Conversely, when visual cuts align with acoustic transients within an integration window of less than 20 milliseconds, viewers experience an amplified psychological phenomenon known as perceptual synchrony, wherein the brain perceives the sound and image as a singular, unified energetic event.

From a musical acoustics perspective, rhythm is hierarchically structured into tempo (beats per minute, BPM), meter (periodic grouping of pulses into bars), beats (fundamental metric units), and downbeats (the heavily accented pulse marking the beginning of a musical bar). Research in computational music information retrieval by Müller [8] and Klapuri and Davy [15] establishes that musical transients in contemporary popular genres—including Electronic Dance Music (EDM), Hip-Hop, Pop, and Rock—are predominantly driven by percussive instruments, specifically the acoustic or synthesized bass kick drum and snare. The acoustic power spectrum of a kick drum is characterized by high-energy transient spikes concentrated in the sub-bass and bass frequency band between 40 Hz and 140 Hz, lasting between 40ms and 100ms in duration. Higher-frequency instruments occupy frequency bands above 300 Hz. Therefore, isolating acoustic downbeats with high temporal fidelity requires applying steep lowpass digital filtering to eliminate melodic harmonics and vocal interference prior to transient energy detection."""

ch2_new = """Audio-visual synchronization is a fundamental requirement in multimedia post-production and psychoacoustics. Human perception actively binds multisensory auditory and visual stimuli through temporal integration mechanisms in the superior colliculus and temporal cortex. Psychophysics research by Vroomen and de Gelder [13] established that when visual cuts deviate from salient musical beats by more than 40 to 80 milliseconds, viewers experience noticeable perceptual disfluency. Conversely, when visual transitions align with acoustic transients within an integration window of less than 20 milliseconds, observers experience perceptual synchrony—perceiving the sound and image as a singular, unified energetic event.

From a musical acoustics perspective, rhythm is hierarchically structured into tempo (BPM), meter, beats, and downbeats. Research by Müller [8] and Klapuri and Davy [15] establishes that musical transients in contemporary popular genres (EDM, Hip-Hop, Pop, Rock) are predominantly driven by percussive kick drums and bass transients. The power spectrum of a kick drum is characterized by high-energy transient spikes concentrated in the sub-bass frequency band between 40 Hz and 140 Hz, lasting 40ms to 100ms. Isolating downbeats with high temporal fidelity requires applying steep lowpass digital filtering to attenuate melodic harmonics and vocal interference prior to energy envelope detection."""

text = text.replace(ch2_old, ch2_new)

# 3. Streamline Chapter 3 (~350 words trimmed)
ch3_old = """In existing commercial automated video editing platforms, the operational architecture follows a centralized client-server model hosted in enterprise cloud environments. The typical existing system workflow encompasses five sequential stages:
1. **Client Ingestion & Egress:** The creator selects unedited video files on their local device. The client web browser initiates a multi-part upload, transferring raw video files (frequently 1 to 5 gigabytes) across the public internet.
2. **Cloud Queue Distribution:** Uploaded video assets enter distributed message queues awaiting allocation to an available GPU worker node, introducing 2 to 15 minutes of queuing delays during peak hours.
3. **Cloud Transcoding & Inference:** Remote cloud compute nodes download the video asset from cloud storage, run speech recognition models, and extract beat transients.
4. **Cloud Filtergraph Rendering:** The cloud GPU executes FFmpeg transcode commands, applying visual transitions, rendering subtitles, and re-encoding the video into an H.264 MP4 container.
5. **Egress Distribution & Download:** The final rendered MP4 is re-uploaded to cloud storage, generating a download link for the client to retrieve the file.

### Critical Deficiencies of the Existing System
This centralized workflow suffers from severe deficiencies:
- **Catastrophic Privacy Risks:** Centralized ingestion forces creators to surrender custody of raw personal media to third-party servers, creating exposure to data breaches and violating GDPR and CCPA regulations.
- **Exorbitant Cloud GPU Expenses:** Maintaining cloud GPU clusters incurs expenses exceeding $0.10 per rendered video minute, forcing platforms to impose heavy subscriptions and watermark restrictions.
- **Severe Bandwidth Waste:** Transmitting multi-gigabyte video files across internet backbones consumes immense electrical power across data centers, generating unnecessary carbon emissions.
- **Dependency on High-Speed Connectivity:** Creators working in remote locations or transit are entirely blocked from editing."""

ch3_new = """Commercial automated video editing platforms follow a centralized client-server model hosted in enterprise cloud environments. This existing workflow requires five sequential stages:
1. **Client Ingestion & Egress:** Uploading raw multi-gigabyte video files across the internet.
2. **Cloud Queue Distribution:** Assets wait in message queues, causing 2 to 15 minutes of delays.
3. **Cloud Transcoding & Inference:** Remote server GPUs download assets, run ASR models, and extract beats.
4. **Cloud Filtergraph Rendering:** Server GPUs execute FFmpeg transcode jobs to re-encode the video.
5. **Egress Distribution & Download:** Rendered MP4s are uploaded to CDNs for user download.

### Critical Deficiencies of the Existing System
This centralized architecture suffers from critical deficiencies:
- **Privacy and Security Risks:** Users surrender custody of personal or confidential video to remote third-party servers, creating data leak risks and violating GDPR/CCPA regulations.
- **Exorbitant Server GPU Costs:** Cloud rendering costs ($0.10/min) necessitate steep monthly subscriptions ($20–$50/month) and free-tier export watermarks.
- **Severe Bandwidth Throttling:** Uploading 2 to 5 GB raw footage over residential connections takes 15 to 30 minutes, crippling creator productivity.
- **Network Dependency:** Offline editing is completely impossible."""

text = text.replace(ch3_old, ch3_new)

with open("Project_Report_Documentation.md", "w", encoding="utf-8") as f:
    f.write(text)

print("New words in Project_Report_Documentation.md:", len(text.split()))
