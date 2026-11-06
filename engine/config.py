"""
Pipeline Configuration & Environment Settings
Supports root semester workspace with multiple subject sub-workspaces.
"""

import os
import shutil
from pathlib import Path

# Base Root Workspace
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = WORKSPACE_ROOT / "bin"

# Binary Executables (prefer root workspace binaries)
def resolve_binary(name: str) -> Path:
    local_bin = BIN_DIR / name
    if local_bin.is_file() and os.access(local_bin, os.X_OK):
        return local_bin
    system_path = shutil.which(name)
    if system_path:
        return Path(system_path)
    raise FileNotFoundError(f"Binary '{name}' not found in workspace bin/ or system PATH.")

FFMPEG_BIN = resolve_binary("ffmpeg")
FFPROBE_BIN = resolve_binary("ffprobe")

def resolve_context(target_str: str | Path | None = None) -> tuple[Path, Path, Path, Path]:
    """
    Resolves the active subject/course directory and its record/, lecture/, pipeline/ folders.
    Works whether invoked from root sem3/ or within a subject folder (e.g. 'db application').
    """
    cwd = Path.cwd().resolve()
    target = (Path(target_str).resolve() if target_str else cwd)
    curr = target if target.is_dir() else target.parent
    course_dir = None

    while curr != WORKSPACE_ROOT and curr.parent != curr:
        if (curr / "record").exists() or (curr / "lecture").exists() or (curr / "pipeline").exists():
            course_dir = curr
            break
        curr = curr.parent

    if not course_dir:
        if (cwd / "record").exists() or (cwd / "lecture").exists():
            course_dir = cwd
        else:
            course_dir = WORKSPACE_ROOT

    return course_dir, course_dir / "record", course_dir / "lecture", course_dir / "pipeline"

# Default Context (Fallback)
DEFAULT_COURSE_DIR, RECORD_ROOT, LECTURE_ROOT, PIPELINE_ROOT = resolve_context()

# Media Format Support
SUPPORTED_VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".flv"}
SUPPORTED_AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus", ".m4b", ".wma"}
SUPPORTED_MEDIA_EXTS = SUPPORTED_VIDEO_EXTS | SUPPORTED_AUDIO_EXTS

# Audio Processing Defaults
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_BITRATE = "64k"
AUDIO_FILENAME = "audio.mp3"

# Vision & Slide Extraction Defaults
SCENE_CHANGE_THRESHOLD = 0.1
ORB_FEATURES_COUNT = 1000
MATCH_DISTANCE_THRESHOLD = 45
MIN_FEATURE_MATCHES = 40
MIN_SETTLED_DWELL_SEC = 5.0
RAPID_FLIP_THRESHOLD_SEC = 3.5
SLIDES_DIRNAME = "slides"
SLIDE_MAPPING_FILENAME = "slide_mapping.json"
DECK_ALIGNMENT_FILENAME = "deck_alignment.md"

# Transcription Defaults
DEFAULT_WHISPER_MODEL = "small"
DEFAULT_DEVICE = "cpu"
DEFAULT_COMPUTE_TYPE = "int8"
CONFIDENCE_THRESHOLD = 0.65
TRANSCRIPT_FILENAME = "transcript.json"

# Output Report Defaults
AUDIT_SUMMARY_FILENAME = "summary_verified.md"
