# Environment Diagnostics & Production Verification Guide

This guide ensures that when cloning or moving this repository to another machine (e.g., laptop, desktop, remote workstation, or school lab computer), you can test the entire pipeline before processing lectures, verify that all dependencies and hardware accelerators work, and check the actual outputs to guarantee that models are **not** downgraded and tasks are **not** skipped.

---

## 1. Quick Pre-Flight Commands

From the root `sem3` directory, run:

### A. Hardware & Dependency Verification
```bash
python run.py --test
# or directly:
python test_environment.py
```
To test a specific Whisper model size (e.g. `small` or `large-v3`):
```bash
python test_environment.py --model small
python test_environment.py --model large-v3
```

### B. Pre-Extraction Thumbnail & Course Match Inspection
Before extracting hours of video, verify that a recording file matches the correct course and lecture deck:
```bash
# Using run.py CLI:
python run.py lecture3 --course "db application" --preview

# Or using the dedicated tool directly:
python preview_recording.py "db application/record/lecture3.mp4"
python preview_recording.py "se fundamentals/record/lecture1.m4a"

# Scan and inspect all recordings across all courses:
python preview_recording.py --all
```
This generates a 4-keyframe contact sheet (`preview_thumbnail.jpg`), checks slide deck ORB features against the course's `lecture/*.pdf` decks, transcribes the first 30 seconds of spoken audio, and alerts if a recording was accidentally placed in the wrong course folder.

---

## 2. Typical Expected Output of `test_environment.py`

When the machine is properly configured, you should see **0 failures** and a complete pass:

```text
===================================================================
  1. System Runtime & Architecture
===================================================================
  ✓ PASS  Host Platform (Darwin 27.0.0 (arm64))
  ✓ PASS  Python Interpreter (v3.12.14 (Standard compatible))
  ✓ PASS  Virtual Environment Active (/Users/uhie/Documents/sem3/.venv)

===================================================================
  2. Multimedia Subsystems (FFmpeg & FFprobe)
===================================================================
  ✓ PASS  FFmpeg Executable (/Users/uhie/Documents/sem3/bin/ffmpeg [local workspace bin/])
  ✓ PASS  FFprobe Executable (/Users/uhie/Documents/sem3/bin/ffprobe [local workspace bin/])
  ✓ PASS  FFmpeg Version (ffmpeg version 6.0 Copyright (c) 2000-2023 the FFmpeg developers)
  ✓ PASS  Audio Transcoding (MP3 Mono 16kHz) (8972 bytes generated)
  ✓ PASS  Slide Extraction Flag (-fps_mode vfr) (Supported natively)

===================================================================
  3. Python Libraries & Deep Learning Backends
===================================================================
  ✓ PASS  faster-whisper (STT Engine) (v1.2.1)
  ✓ PASS  CTranslate2 (Inference Acceleration) (v4.8.4)
  ✓ PASS  PyAV (Audio / Video Demuxing) (v13.1.0)
  ✓ PASS  OpenCV (Keyframe Difference & Scene Hashing) (v5.0.0)
  ✓ PASS  PyMuPDF (Slide PDF Rendering & Text Extraction) (v2.1)
  ✓ PASS  Pillow (Image Processing) (v13.0.0)
  ✓ PASS  NumPy (Mathematical Computations) (v2.5.4)
  ✓ PASS  Tabulate (Status Table Formatting) (v0.10.0)
  ✓ PASS  PyYAML (Metadata & Task Configuration) (v6.0.3)
  ✓ PASS  CTranslate2 CPU Compute Types (float32, int8_float32, int8)
  ✓ PASS  CTranslate2 Accelerator (Running on CPU / NEON / AVX2 (Native Apple Silicon / CPU acceleration))

===================================================================
  4. End-to-End Functional Smoke Tests
===================================================================
  ✓ PASS  PyMuPDF & OpenCV Vector/Raster Pipeline (Rendered & Analyzed (Mean pixel intensity: 251.8))
  ⏳ Testing Whisper 'small' inference smoke test...
  ✓ PASS  Whisper Model 'small' Inference (Loaded & Transcribed cleanly (int8))

===================================================================
  5. Workspace & Multi-Course Hierarchy
===================================================================
  ✓ PASS  Course Isolation: db application (record/ (3 media), lecture/, pipeline/)
  ✓ PASS  Course Isolation: further prg (record/ (5 media), lecture/, pipeline/)
  ✓ PASS  Course Isolation: se fundamentals (record/ (4 media), lecture/, pipeline/)

===================================================================
  Diagnostic Summary
===================================================================
  Total Passes  : 24
  Total Warnings: 0
  Total Failures: 0

🎉 ALL SYSTEMS PASS: Machine is 100% verified and ready for full runs!
```

---

## 3. Typical Expected Output of `run.py` (Full Pipeline Run)

When you process a lecture (e.g. `python run.py lecture3 --course "db application"`), the console output follows this exact structure:

```text
==========================================
🚀 Running Task: [db application] -> lecture3
📁 Directory   : db application/pipeline/lecture3
==========================================
🔊 Processing video (lecture3.mp4) → mono 64k at db application/pipeline/lecture3/audio.mp3...
✓ Audio processing completed successfully.
🖼️  Detecting scene changes (> 0.1) and extracting slides...
✓ Extracted 78 slides into db application/pipeline/lecture3/slides

📑 Loading slide deck: lecture3.pdf
🔬 Matching 78 video snapshots against 57 deck slides...
✅ Aligned 78 / 78 slides to 'lecture3.pdf'

⏳ Loading Whisper model: 'small' (cpu, int8)...
🚀 Transcribing 'audio.mp3'...
🌐 Language: en (probability: 0.99)
  [00:00 -> 00:45] Good morning everyone, today we cover database indexes...
  [00:45 -> 01:30] Let us turn to slide number three on B-Trees...
✅ Transcribed 120 segments (4520 words, 18 low-conf flagged)
✓ Enriched slide alignment with transcript context (0 external activities flagged)

✨ Task 'lecture3' in 'db application' processed!

==========================================
📋 Course: db application | Task: lecture3
📁 Path  : db application/pipeline/lecture3
==========================================
  🔊 Audio Extracted      : ✓ Yes
  🖼️  Slide Keyframes      : ✓ 78 slides
  📑 Deck Alignment       : ✓ Yes
  📝 Whisper Transcript   : ✓ Yes
  ⚖️  Verified Audit Notes : ⏳ Pending
  🚀 Ready for Agent Audit: ✓ Ready
==========================================
```

---

## 4. How to Verify No Tasks Were Skipped & No Models Were Downgraded

Check these 4 indicators:

| Check Item | Desired Value | Symptom if Failing / Degraded |
| :--- | :--- | :--- |
| **Model Size** | `'small'` (or `'large-v3'`) | If output says `'tiny'` or `'base'`, someone specified `-m tiny` or modified defaults. |
| **Compute Type** | `int8` (Apple Silicon CPU) or `float16` (NVIDIA CUDA) | If output says `float32` on GPU, GPU compute types are misconfigured. |
| **Slide Keyframes** | `> 0 slides` (e.g. 70-250 slides) | If `0 slides` or `- None`, FFmpeg scene detection failed or video stream was missing. |
| **Deck Alignment** | `✅ Aligned X / Y slides` | If `0 / 0`, slide deck matching was skipped or deck PDF was not found in `lecture/`. |
| **Ready for Agent Audit** | `✓ Ready` | If `✗ Incomplete`, one of the artifacts (`audio.mp3`, `transcript.json`, `slide_mapping.json`) was not generated. |

---

## 5. Troubleshooting Common Failures on a New Machine

### A. `FFmpeg Executable: not found`
* **Zero-Sudo Fix for Mac:**
  ```bash
  curl -L https://evermeet.cx/ffmpeg/getrelease/zip -o ff.zip && unzip -o ff.zip -d bin/ && chmod +x bin/ffmpeg && rm ff.zip
  curl -L https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip -o ffp.zip && unzip -o ffp.zip -d bin/ && chmod +x bin/ffprobe && rm ffp.zip
  xattr -d com.apple.quarantine bin/ffmpeg bin/ffprobe 2>/dev/null
  ```
* **Zero-Sudo Fix for Linux (Ubuntu/Debian/CentOS):**
  ```bash
  wget -qO- https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C bin/
  chmod +x bin/ffmpeg bin/ffprobe
  ```

### B. `faster-whisper / ctranslate2: missing package`
* Run:
  ```bash
  pip install -r requirements.txt
  ```

### C. `Slide Extraction Flag (-fps_mode vfr): rejected`
* Ensure the local FFmpeg build in `bin/ffmpeg` is version 5.1 or newer. Run `bin/ffmpeg -version` to verify.

