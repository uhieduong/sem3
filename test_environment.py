#!/usr/bin/env python3
"""
Environment & Hardware Diagnostic Test Suite
Validates all runtime prerequisites, FFmpeg capabilities, Python dependencies,
and Whisper / Computer Vision subsystems before processing lectures.

Usage:
    python test_environment.py
    python test_environment.py --model small   # tests specific Whisper model loading
"""

import os
import sys
import shutil
import platform
import subprocess
import tempfile
from pathlib import Path

# Workspace Root
WORKSPACE_ROOT = Path(__file__).resolve().parent
BIN_DIR = WORKSPACE_ROOT / "bin"

# ANSI Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS_ICON = f"{GREEN}✓ PASS{RESET}"
WARN_ICON = f"{YELLOW}⚠ WARN{RESET}"
FAIL_ICON = f"{RED}✗ FAIL{RESET}"

class TestContext:
    def __init__(self):
        self.passes = 0
        self.warnings = 0
        self.failures = 0
        self.remediations = []

    def record_pass(self, title: str, detail: str = ""):
        self.passes += 1
        msg = f"  {PASS_ICON}  {title}"
        if detail:
            msg += f" ({CYAN}{detail}{RESET})"
        print(msg)

    def record_warn(self, title: str, detail: str = "", fix: str = ""):
        self.warnings += 1
        msg = f"  {WARN_ICON}  {title}"
        if detail:
            msg += f" ({detail})"
        print(msg)
        if fix:
            self.remediations.append((title, fix, "warn"))

    def record_fail(self, title: str, detail: str = "", fix: str = ""):
        self.failures += 1
        msg = f"  {FAIL_ICON}  {title}"
        if detail:
            msg += f" - {RED}{detail}{RESET}"
        print(msg)
        if fix:
            self.remediations.append((title, fix, "fail"))

def section_header(title: str):
    print(f"\n{BOLD}{BLUE}==================================================================={RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}==================================================================={RESET}")

def test_system(ctx: TestContext):
    section_header("1. System Runtime & Architecture")

    # OS & Architecture
    os_name = platform.system()
    arch = platform.machine()
    py_ver = sys.version.split()[0]
    ctx.record_pass("Host Platform", f"{os_name} {platform.release()} ({arch})")

    # Python Version (Require >= 3.10)
    ver_info = sys.version_info
    if ver_info.major == 3 and ver_info.minor in (10, 11, 12):
        ctx.record_pass("Python Interpreter", f"v{py_ver} (Standard compatible)")
    elif ver_info.major == 3 and ver_info.minor > 12:
        ctx.record_warn("Python Interpreter", f"v{py_ver} (May have binary wheel issues with torch/ctranslate2; 3.10-3.12 recommended)")
    else:
        ctx.record_fail("Python Interpreter", f"v{py_ver} (Requires Python >= 3.10 and <= 3.12)",
                        "Install Python 3.11 or 3.12 using pyenv or uv: uv python install 3.12")

    # Virtual Environment
    in_venv = (sys.prefix != sys.base_prefix) or ("VIRTUAL_ENV" in os.environ)
    if in_venv:
        ctx.record_pass("Virtual Environment Active", f"{sys.prefix}")
    else:
        ctx.record_warn(
            "Virtual Environment",
            "Running directly in system Python; a virtualenv is strongly recommended",
            "Create & activate venv: python3 -m venv .venv && source .venv/bin/activate"
        )

def resolve_binary_check(name: str) -> tuple[Path | None, str]:
    local_bin = BIN_DIR / name
    if local_bin.is_file() and os.access(local_bin, os.X_OK):
        return local_bin, "local workspace bin/"
    system_path = shutil.which(name)
    if system_path:
        return Path(system_path), "system PATH"
    return None, "not found"

def test_ffmpeg(ctx: TestContext):
    section_header("2. Multimedia Subsystems (FFmpeg & FFprobe)")

    ffmpeg_bin, ffmpeg_loc = resolve_binary_check("ffmpeg")
    ffprobe_bin, ffprobe_loc = resolve_binary_check("ffprobe")

    # 1. Existence check
    if ffmpeg_bin:
        ctx.record_pass("FFmpeg Executable", f"{ffmpeg_bin} [{ffmpeg_loc}]")
    else:
        ctx.record_fail(
            "FFmpeg Executable",
            "ffmpeg binary not found in workspace bin/ or system PATH",
            "Download static binary to bin/ (zero sudo):\n"
            "  macOS: curl -L https://evermeet.cx/ffmpeg/getrelease/zip -o ff.zip && unzip -o ff.zip -d bin/ && chmod +x bin/ffmpeg && rm ff.zip\n"
            "  Linux: wget -qO- https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C bin/ ffmpeg"
        )

    if ffprobe_bin:
        ctx.record_pass("FFprobe Executable", f"{ffprobe_bin} [{ffprobe_loc}]")
    else:
        ctx.record_fail(
            "FFprobe Executable",
            "ffprobe binary not found in workspace bin/ or system PATH",
            "Download static binary to bin/ (zero sudo):\n"
            "  macOS: curl -L https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip -o ffp.zip && unzip -o ffp.zip -d bin/ && chmod +x bin/ffprobe && rm ffp.zip"
        )

    if not ffmpeg_bin:
        return

    # 2. Version and Option Support
    try:
        ver_proc = subprocess.run([str(ffmpeg_bin), "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        ver_line = ver_proc.stdout.splitlines()[0] if ver_proc.stdout else "Unknown version"
        ctx.record_pass("FFmpeg Version", ver_line)
    except Exception as e:
        ctx.record_fail("FFmpeg Version Check", str(e))

    # 3. Audio Extraction Smoke Test (synthetic 1s tone -> mono 64kbps MP3)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_mp3 = Path(tmpdir) / "test_tone.mp3"
        audio_cmd = [
            str(ffmpeg_bin), "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=440:duration=1",
            "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
            str(test_mp3)
        ]
        try:
            res = subprocess.run(audio_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0 and test_mp3.is_file() and test_mp3.stat().st_size > 0:
                ctx.record_pass("Audio Transcoding (MP3 Mono 16kHz)", f"{test_mp3.stat().st_size} bytes generated")
            else:
                ctx.record_fail("Audio Transcoding (MP3 Mono 16kHz)", f"FFmpeg error: {res.stderr[-300:]}")
        except Exception as e:
            ctx.record_fail("Audio Transcoding Test", str(e))

        # 4. Slide Extraction Option Test (-fps_mode vfr check)
        vfr_cmd = [
            str(ffmpeg_bin), "-y",
            "-f", "lavfi",
            "-i", "testsrc=duration=0.5:size=320x240:rate=10",
            "-vf", "select='gt(scene,0.1)',showinfo",
            "-fps_mode", "vfr",
            "-f", "null", "-"
        ]
        try:
            res = subprocess.run(vfr_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                ctx.record_pass("Slide Extraction Flag (-fps_mode vfr)", "Supported natively")
            else:
                ctx.record_fail("Slide Extraction Flag (-fps_mode vfr)", f"Option rejected: {res.stderr[-300:]}")
        except Exception as e:
            ctx.record_fail("Slide Extraction Flag Test", str(e))

def test_python_packages(ctx: TestContext):
    section_header("3. Python Libraries & Deep Learning Backends")

    packages = [
        ("faster_whisper", "faster-whisper (STT Engine)"),
        ("ctranslate2", "CTranslate2 (Inference Acceleration)"),
        ("av", "PyAV (Audio / Video Demuxing)"),
        ("cv2", "OpenCV (Keyframe Difference & Scene Hashing)"),
        ("fitz", "PyMuPDF (Slide PDF Rendering & Text Extraction)"),
        ("PIL", "Pillow (Image Processing)"),
        ("numpy", "NumPy (Mathematical Computations)"),
        ("tabulate", "Tabulate (Status Table Formatting)"),
        ("yaml", "PyYAML (Metadata & Task Configuration)"),
    ]

    for module_name, desc in packages:
        try:
            mod = __import__(module_name)
            ver = getattr(mod, "__version__", "installed")
            ctx.record_pass(desc, f"v{ver}")
        except ImportError as e:
            ctx.record_fail(
                desc,
                f"Missing package ({e})",
                f"Install missing dependencies: pip install -r requirements.txt"
            )

    # Hardware acceleration check (CUDA / MPS)
    try:
        import ctranslate2
        cpu_types = ctranslate2.get_supported_compute_types("cpu")
        ctx.record_pass("CTranslate2 CPU Compute Types", ", ".join(cpu_types))
        try:
            cuda_types = ctranslate2.get_supported_compute_types("cuda")
            if cuda_types:
                ctx.record_pass("CTranslate2 GPU (CUDA) Compute Types", ", ".join(cuda_types))
        except Exception:
            ctx.record_pass("CTranslate2 Accelerator", "Running on CPU / NEON / AVX2 (Native Apple Silicon / CPU acceleration)")
    except Exception as e:
        ctx.record_warn("CTranslate2 Compute Query", str(e))

def test_whisper_and_vision_smoke(ctx: TestContext, test_whisper_model: str = "base"):
    section_header("4. End-to-End Functional Smoke Tests")

    # 1. Computer Vision & PyMuPDF in-memory test
    try:
        import fitz
        import cv2
        import numpy as np

        # Create dummy PDF in memory and render
        doc = fitz.open()
        page = doc.new_page(width=300, height=200)
        page.insert_text((50, 100), "Lecture Diagnostics Test", fontsize=18)
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_val = float(np.mean(gray))
        doc.close()

        ctx.record_pass("PyMuPDF & OpenCV Vector/Raster Pipeline", f"Rendered & Analyzed (Mean pixel intensity: {mean_val:.1f})")
    except Exception as e:
        ctx.record_fail("PyMuPDF & OpenCV Test", str(e), "Reinstall PyMuPDF and opencv-python-headless: pip install --force-reinstall pymupdf opencv-python-headless")

    # 2. Whisper Model Loading & Inference Test
    try:
        from faster_whisper import WhisperModel
        import ctranslate2

        print(f"  ⏳ Testing Whisper '{test_whisper_model}' inference smoke test...")
        compute_type = "int8" if "int8" in ctranslate2.get_supported_compute_types("cpu") else "float32"
        model = WhisperModel(test_whisper_model, device="cpu", compute_type=compute_type)

        # Transcribe a synthesized 1s tone
        ffmpeg_bin, _ = resolve_binary_check("ffmpeg")
        if ffmpeg_bin:
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "diag_audio.mp3"
                subprocess.run([
                    str(ffmpeg_bin), "-y",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=1.5",
                    "-vn", "-ac", "1", "-ar", "16000", str(audio_path)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

                segments, info = model.transcribe(str(audio_path), word_timestamps=True)
                list(segments)  # evaluate generator

                ctx.record_pass(f"Whisper Model '{test_whisper_model}' Inference", f"Loaded & Transcribed cleanly ({compute_type})")
        else:
            ctx.record_warn("Whisper Model Inference", "Skipped synthetic audio run due to missing FFmpeg")
    except Exception as e:
        ctx.record_fail(
            f"Whisper Model '{test_whisper_model}' Inference",
            f"Failed: {e}",
            "Verify faster-whisper installation: pip install --upgrade --force-reinstall faster-whisper ctranslate2"
        )

def test_workspace_isolation(ctx: TestContext):
    section_header("5. Workspace & Multi-Course Hierarchy")

    expected_courses = ["db application", "further prg", "se fundamentals"]
    for c in expected_courses:
        cdir = WORKSPACE_ROOT / c
        if not cdir.is_dir():
            ctx.record_warn(f"Course Folder: {c}", "Directory not found")
            continue

        record_dir = cdir / "record"
        lecture_dir = cdir / "lecture"
        pipeline_dir = cdir / "pipeline"

        sub_ok = record_dir.is_dir() and lecture_dir.is_dir() and pipeline_dir.is_dir()
        if sub_ok:
            rec_count = len(list(record_dir.glob("*.*"))) if record_dir.exists() else 0
            ctx.record_pass(f"Course Isolation: {c}", f"record/ ({rec_count} media), lecture/, pipeline/")
        else:
            ctx.record_warn(f"Course Isolation: {c}", "Missing subfolders (record/, lecture/, pipeline/)")

def print_summary(ctx: TestContext):
    section_header("Diagnostic Summary")
    print(f"  Total Passes  : {GREEN}{ctx.passes}{RESET}")
    print(f"  Total Warnings: {YELLOW}{ctx.warnings}{RESET}")
    print(f"  Total Failures: {RED}{ctx.failures}{RESET}")

    if ctx.failures > 0:
        print(f"\n{BOLD}{RED}❌ CRITICAL PRE-FLIGHT CHECKS FAILED ({ctx.failures} failure(s)){RESET}")
        print("Please resolve the following before running the lecture pipeline:")
        for title, fix, severity in ctx.remediations:
            if severity == "fail":
                print(f"\n• {BOLD}{title}{RESET}:")
                print(f"  {fix}")
        print(f"\n{BOLD}Do not run 'python run.py' until all failures are resolved.{RESET}\n")
        sys.exit(1)
    elif ctx.warnings > 0:
        print(f"\n{BOLD}{YELLOW}⚠️  PASSED WITH WARNINGS ({ctx.warnings} warning(s)){RESET}")
        print("The pipeline can run, but consider addressing:")
        for title, fix, severity in ctx.remediations:
            if severity == "warn":
                print(f"• {title}: {fix}")
        print(f"\n{GREEN}{BOLD}✓ Machine is validated and ready to process lectures!{RESET}\n")
    else:
        print(f"\n{GREEN}{BOLD}🎉 ALL SYSTEMS PASS: Machine is 100% verified and ready for full runs!{RESET}\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test environment and hardware readiness for lecture transcription.")
    parser.add_argument("--model", default="base", help="Whisper model size to test (default: base for fast smoke test)")
    args = parser.parse_args()

    ctx = TestContext()
    test_system(ctx)
    test_ffmpeg(ctx)
    test_python_packages(ctx)
    test_whisper_and_vision_smoke(ctx, test_whisper_model=args.model)
    test_workspace_isolation(ctx)
    print_summary(ctx)
