#!/usr/bin/env python3
"""
Pre-Extraction Recording Preview & Course Verification Tool
Extracts thumbnail contact sheets, inspects video/audio metadata,
runs fast intro audio transcription, and verifies visual slide alignment
against course lecture decks BEFORE running the full processing pipeline.

Usage:
    # Preview a specific recording file:
    python preview_recording.py "db application/record/lecture3.mp4"
    python preview_recording.py "se fundamentals/record/lecture1.m4a"

    # Preview by task name and course:
    python preview_recording.py lecture3 --course "db application"

    # Scan and verify all recordings across all courses:
    python preview_recording.py --all
"""

import os
import re
import sys
import json
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path

# Workspace Root & Binaries
WORKSPACE_ROOT = Path(__file__).resolve().parent
BIN_DIR = WORKSPACE_ROOT / "bin"

# ANSI Terminal Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

SUPPORTED_VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".flv"}
SUPPORTED_AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus"}
SUPPORTED_MEDIA_EXTS = SUPPORTED_VIDEO_EXTS | SUPPORTED_AUDIO_EXTS

def resolve_binary(name: str) -> Path:
    local = BIN_DIR / name
    if local.is_file() and os.access(local, os.X_OK):
        return local
    system_path = shutil.which(name)
    if system_path:
        return Path(system_path)
    raise FileNotFoundError(f"Binary '{name}' not found in workspace bin/ or system PATH.")

def format_duration(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

def get_media_info(media_path: Path) -> dict:
    """Uses ffprobe to extract stream metadata, duration, resolution, and codecs."""
    ffprobe_bin = resolve_binary("ffprobe")
    cmd = [
        str(ffprobe_bin),
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(media_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return {"error": res.stderr}

    data = json.loads(res.stdout)
    fmt = data.get("format", {})
    streams = data.get("streams", [])

    duration = float(fmt.get("duration", 0.0))
    size_mb = media_path.stat().st_size / (1024 * 1024)

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    info = {
        "duration": duration,
        "duration_str": format_duration(duration),
        "size_mb": round(size_mb, 2),
        "has_video": video_stream is not None,
        "has_audio": audio_stream is not None,
    }

    if video_stream:
        info["video_codec"] = video_stream.get("codec_name", "unknown")
        info["width"] = int(video_stream.get("width", 0))
        info["height"] = int(video_stream.get("height", 0))
        info["resolution"] = f"{info['width']}x{info['height']}"
        r_frame_rate = video_stream.get("r_frame_rate", "0/1")
        try:
            num, den = map(int, r_frame_rate.split("/"))
            info["fps"] = round(num / den, 1) if den > 0 else 0.0
        except Exception:
            info["fps"] = 0.0

    if audio_stream:
        info["audio_codec"] = audio_stream.get("codec_name", "unknown")
        info["sample_rate"] = int(audio_stream.get("sample_rate", 0))
        info["channels"] = int(audio_stream.get("channels", 1))

    return info

def extract_thumbnail_grid(video_path: Path, output_image: Path, duration: float) -> list[str]:
    """
    Extracts 4 frames across the video and stitches them into a 2x2 contact sheet
    with timestamp overlays.
    """
    import cv2
    import numpy as np

    ffmpeg_bin = resolve_binary("ffmpeg")
    # Sample 4 timestamps: early title (15s/30s), 15%, 45%, 75% of duration
    sample_secs = [
        min(30.0, duration * 0.05),
        max(60.0, duration * 0.20),
        max(180.0, duration * 0.50),
        max(300.0, duration * 0.80),
    ]
    sample_secs = sorted(list(set([round(s, 1) for s in sample_secs if s < duration])))
    if not sample_secs:
        sample_secs = [0.0]

    frames = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, sec in enumerate(sample_secs):
            tmp_frame = Path(tmpdir) / f"frame_{idx:02d}.jpg"
            ts_str = format_duration(sec)
            cmd = [
                str(ffmpeg_bin), "-y",
                "-ss", str(sec),
                "-i", str(video_path),
                "-vframes", "1",
                "-q:v", "2",
                str(tmp_frame)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if tmp_frame.is_file():
                mat = cv2.imread(str(tmp_frame))
                if mat is not None:
                    # Draw timestamp label banner on frame
                    h, w = mat.shape[:2]
                    cv2.rectangle(mat, (10, 10), (190, 50), (20, 20, 20), -1)
                    cv2.putText(mat, f"[{ts_str}]", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                    frames.append(mat)

    if not frames:
        return []

    # Target thumbnail cell size
    cell_w, cell_h = 640, 360
    resized = [cv2.resize(f, (cell_w, cell_h)) for f in frames]

    while len(resized) < 4:
        # Pad with blank tiles if video is very short
        blank = np.zeros((cell_h, cell_w, 3), dtype=np.uint8)
        resized.append(blank)

    top_row = np.hstack([resized[0], resized[1]])
    bottom_row = np.hstack([resized[2], resized[3]])
    grid = np.vstack([top_row, bottom_row])

    output_image.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_image), grid)
    return [format_duration(s) for s in sample_secs]

def match_thumbnail_against_decks(thumb_img_path: Path, course_dir: Path) -> dict:
    """
    Compares the thumbnail against all PDF presentation decks in the course's lecture/ directory
    using ORB feature detection, extracting title slides and match confidence.
    """
    import cv2
    import pymupdf
    import numpy as np

    if not thumb_img_path or not thumb_img_path.is_file():
        return {"matched": False, "reason": "No thumbnail image available"}

    img = cv2.imread(str(thumb_img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return {"matched": False, "reason": "Failed to read thumbnail image"}

    orb = cv2.ORB_create(nfeatures=1500)
    kp_thumb, des_thumb = orb.detectAndCompute(img, None)
    if des_thumb is None or len(kp_thumb) < 10:
        return {"matched": False, "reason": "Insufficient visual features in thumbnail"}

    lecture_dir = course_dir / "lecture"
    pdf_decks = list(lecture_dir.glob("*.pdf")) if lecture_dir.is_dir() else []
    if not pdf_decks:
        return {"matched": False, "reason": f"No PDF decks found in {lecture_dir.relative_to(WORKSPACE_ROOT)}"}

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    best_match = None
    highest_score = 0

    for deck_file in pdf_decks:
        try:
            doc = pymupdf.open(str(deck_file))
            # Check first 5 slides (title & agenda slides)
            pages_to_check = min(5, len(doc))
            for p_idx in range(pages_to_check):
                page = doc[p_idx]
                pix = page.get_pixmap(dpi=100)
                pdf_mat = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
                pdf_gray = cv2.cvtColor(pdf_mat, cv2.COLOR_RGB2GRAY)
                kp_pdf, des_pdf = orb.detectAndCompute(pdf_gray, None)

                if des_pdf is None:
                    continue

                matches = bf.match(des_thumb, des_pdf)
                good = [m for m in matches if m.distance < 55]
                score = len(good)

                if score > highest_score:
                    highest_score = score
                    # Extract page title / text
                    text_lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]
                    title = " | ".join(text_lines[:2]) if text_lines else "Untitled Slide"
                    best_match = {
                        "deck_name": deck_file.name,
                        "deck_path": deck_file,
                        "page": p_idx + 1,
                        "title": title[:70],
                        "score": score,
                    }
            doc.close()
        except Exception:
            continue

    if best_match and best_match["score"] >= 25:
        confidence = "HIGH" if best_match["score"] >= 60 else "MEDIUM"
        best_match["confidence"] = confidence
        best_match["matched"] = True
        return best_match

    return {
        "matched": False,
        "score": highest_score,
        "best_attempt": best_match["deck_name"] if best_match else "None",
        "reason": "Feature matches below threshold (likely demo screen or title slide not in top 5 pages)"
    }

def transcribe_intro_speech(media_path: Path, max_seconds: int = 30) -> str:
    """Transcribes the first 30s of audio using Whisper tiny for instant verification."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return "(faster-whisper not installed; skipping audio preview)"

    ffmpeg_bin = resolve_binary("ffmpeg")
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_snippet = Path(tmpdir) / "intro.mp3"
        cmd = [
            str(ffmpeg_bin), "-y",
            "-ss", "00:00:00",
            "-t", str(max_seconds),
            "-i", str(media_path),
            "-vn", "-ac", "1", "-ar", "16000",
            str(audio_snippet)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0 or not audio_snippet.is_file():
            return "(No audio stream available)"

        try:
            model = WhisperModel("tiny", device="cpu", compute_type="int8")
            segments, _ = model.transcribe(str(audio_snippet))
            text = " ".join([s.text.strip() for s in segments]).strip()
            return text if text else "(Silence / No spoken dialogue in first 30 seconds)"
        except Exception as e:
            return f"(Whisper quick-check error: {e})"

def cross_check_other_courses(thumb_path: Path, current_course_dir: Path) -> dict | None:
    """Checks if this recording might actually belong to another course in the workspace."""
    other_courses = [
        d for d in WORKSPACE_ROOT.iterdir()
        if d.is_dir() and d != current_course_dir and not d.name.startswith((".", "_", "bin", "engine"))
    ]
    for other in other_courses:
        match = match_thumbnail_against_decks(thumb_path, other)
        if match.get("matched") and match.get("score", 0) >= 50:
            match["other_course"] = other.name
            return match
    return None

def preview_single_recording(media_path: Path, course_dir: Path | None = None, skip_audio: bool = False):
    media_path = Path(media_path).resolve()
    if not media_path.is_file():
        print(f"{RED}Error: Media file not found at '{media_path}'{RESET}")
        return

    # Infer course directory if not explicitly provided
    if not course_dir:
        curr = media_path.parent
        while curr != WORKSPACE_ROOT and curr.parent != curr:
            if (curr / "record").is_dir() or (curr / "lecture").is_dir():
                course_dir = curr
                break
            curr = curr.parent
        if not course_dir:
            course_dir = WORKSPACE_ROOT

    task_name = media_path.stem
    print(f"\n{BOLD}{BLUE}==================================================================={RESET}")
    print(f"{BOLD}🔍 Pre-Flight Recording Inspection: {CYAN}{media_path.name}{RESET}")
    print(f"📁 Course Folder : {BOLD}{course_dir.name}{RESET}")
    print(f"{BOLD}{BLUE}==================================================================={RESET}")

    # 1. Media Info & Streams
    info = get_media_info(media_path)
    if "error" in info:
        print(f"{RED}Failed to probe media: {info['error']}{RESET}")
        return

    print(f"  ⏱️  Duration       : {BOLD}{info['duration_str']}{RESET} ({info['size_mb']} MB)")
    if info["has_video"]:
        print(f"  🎬 Video Track    : {info['resolution']} @ {info['fps']} fps ({info.get('video_codec', 'unknown')})")
    else:
        print(f"  🎬 Video Track    : {YELLOW}None (Audio-Only Recording){RESET}")

    if info["has_audio"]:
        print(f"  🔊 Audio Track    : {info.get('sample_rate', 0)} Hz, {info.get('channels', 1)} ch ({info.get('audio_codec', 'unknown')})")
    else:
        print(f"  🔊 Audio Track    : {RED}None (Silent Video){RESET}")

    # 2. Thumbnail Generation
    thumb_path = None
    if info["has_video"]:
        preview_dir = course_dir / "pipeline" / task_name
        preview_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = preview_dir / "preview_thumbnail.jpg"
        sample_times = extract_thumbnail_grid(media_path, thumb_path, info["duration"])
        if thumb_path.is_file():
            print(f"  🖼️  Thumbnail Grid : {GREEN}Generated (4 keyframes: {', '.join(sample_times)}){RESET}")
            print(f"     👉 Open image : {CYAN}file://{thumb_path}{RESET}")

    # 3. Slide Deck Matching
    deck_match = None
    if thumb_path and thumb_path.is_file():
        deck_match = match_thumbnail_against_decks(thumb_path, course_dir)
        if deck_match.get("matched"):
            conf_color = GREEN if deck_match['confidence'] == 'HIGH' else YELLOW
            print(f"  📑 Slide Deck     : {conf_color}✓ Matched '{deck_match['deck_name']}'{RESET} (Page {deck_match['page']}, Score: {deck_match['score']} pts)")
            print(f"     Slide Title    : \"{deck_match['title']}\"")
        else:
            print(f"  📑 Slide Deck     : {YELLOW}- Low match ({deck_match.get('reason')}){RESET}")
            # Cross-check other courses in case it was put in the wrong course folder
            cross = cross_check_other_courses(thumb_path, course_dir)
            if cross:
                print(f"     {RED}⚠️  POTENTIAL MISPLACEMENT!{RESET}")
                print(f"     This video matches {BOLD}'{cross['other_course']}'{RESET} deck '{cross['deck_name']}' ({cross['score']} pts)!")

    # 4. Spoken Intro Audio Preview
    if info["has_audio"] and not skip_audio:
        print(f"  🎙️  Spoken Intro   : Transcribing first 30s with Whisper tiny...")
        intro_text = transcribe_intro_speech(media_path)
        print(f"     💬 {CYAN}\"{intro_text[:140]}...\"{RESET}" if len(intro_text) > 140 else f"     💬 {CYAN}\"{intro_text}\"{RESET}")

    # 5. Course Verification Verdict
    print(f"\n{BOLD}📋 Course Verification Verdict:{RESET}")
    if deck_match and deck_match.get("matched"):
        print(f"  {GREEN}{BOLD}✅ VERIFIED FOR '{course_dir.name}'{RESET}")
        print(f"  Matches {deck_match['deck_name']} (Page {deck_match['page']}). Safe to run full extraction.\n")
    elif not info["has_video"]:
        print(f"  {BLUE}ℹ️  AUDIO-ONLY RECORDING{RESET}")
        print(f"  Audio is ready for Whisper transcription.\n")
    else:
        print(f"  {YELLOW}{BOLD}⚠️  MANUAL REVIEW RECOMMENDED{RESET}")
        print(f"  Please open {CYAN}file://{thumb_path}{RESET} to verify title slide before launching full extraction.\n")

def main():
    parser = argparse.ArgumentParser(description="Pre-extraction recording inspection & course verification.")
    parser.add_argument("target", nargs="?", default=None, help="Recording file path or task name.")
    parser.add_argument("-c", "--course", default=None, help="Course directory name (e.g. 'db application').")
    parser.add_argument("--all", action="store_true", help="Inspect all recordings across all courses.")
    parser.add_argument("--no-audio", action="store_true", help="Skip Whisper intro audio transcription.")
    args = parser.parse_args()

    if args.all:
        courses = [d for d in WORKSPACE_ROOT.iterdir() if d.is_dir() and not d.name.startswith((".", "_", "bin", "engine"))]
        total = 0
        for c in sorted(courses, key=lambda x: x.name):
            rec_dir = c / "record"
            if not rec_dir.is_dir():
                continue
            for item in sorted(rec_dir.iterdir()):
                if item.suffix.lower() in SUPPORTED_MEDIA_EXTS:
                    total += 1
                    preview_single_recording(item, course_dir=c, skip_audio=args.no_audio)
        if total == 0:
            print("No media recordings found in any course record/ folder.")
        return

    if not args.target:
        parser.print_help()
        print("\nExamples:")
        print("  python preview_recording.py \"db application/record/lecture3.mp4\"")
        print("  python preview_recording.py lecture3 --course \"se fundamentals\"")
        print("  python preview_recording.py --all")
        sys.exit(1)

    target_path = Path(args.target)
    course_dir = (WORKSPACE_ROOT / args.course).resolve() if args.course else None

    # Resolve target if given as a task name e.g. 'lecture3'
    if not target_path.is_file():
        if course_dir:
            for ext in SUPPORTED_MEDIA_EXTS:
                cand = course_dir / "record" / f"{args.target}{ext}"
                if cand.is_file():
                    target_path = cand
                    break
        else:
            # Search in all courses
            for c in WORKSPACE_ROOT.iterdir():
                if c.is_dir() and not c.name.startswith((".", "_")):
                    for ext in SUPPORTED_MEDIA_EXTS:
                        cand = c / "record" / f"{args.target}{ext}"
                        if cand.is_file():
                            target_path = cand
                            course_dir = c
                            break

    preview_single_recording(target_path, course_dir=course_dir, skip_audio=args.no_audio)

if __name__ == "__main__":
    main()

