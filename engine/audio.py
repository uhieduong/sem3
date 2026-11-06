"""
Audio Extraction Subsystem
Extracts normalized 64kbps mono MP3 audio using the local FFmpeg binary.
"""

import sys
import subprocess
from pathlib import Path
from engine.config import (
    WORKSPACE_ROOT,
    FFMPEG_BIN,
    AUDIO_FILENAME,
    AUDIO_CHANNELS,
    AUDIO_BITRATE,
    AUDIO_SAMPLE_RATE,
    SUPPORTED_AUDIO_EXTS
)

def extract_audio(source_path: Path, task_dir: Path, force: bool = False) -> Path:
    """
    Extracts or converts speech-optimized mono MP3 audio from a video recording
    or separated audio recording (e.g. .m4a, .mp3, .wav, .aac, .flac).
    Transcodes and places into pipeline/<task_name>/audio.mp3.
    """
    source_path = Path(source_path).resolve()
    task_dir = Path(task_dir).resolve()
    task_dir.mkdir(parents=True, exist_ok=True)

    audio_path = task_dir / AUDIO_FILENAME
    if audio_path.exists() and not force:
        print(f"✓ Audio already extracted: {audio_path.relative_to(WORKSPACE_ROOT)}")
        return audio_path

    is_audio_source = source_path.suffix.lower() in SUPPORTED_AUDIO_EXTS
    source_label = f"separated audio ({source_path.name})" if is_audio_source else f"video ({source_path.name})"
    print(f"🔊 Processing {source_label} → mono {AUDIO_BITRATE} at {audio_path.relative_to(WORKSPACE_ROOT)}...")
    cmd = [
        str(FFMPEG_BIN), "-y",
        "-i", str(source_path),
        "-vn",
        "-ac", str(AUDIO_CHANNELS),
        "-ar", str(AUDIO_SAMPLE_RATE),
        "-b:a", AUDIO_BITRATE,
        str(audio_path)
    ]

    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error processing audio from {source_path}: {res.stderr[-500:]}")
        sys.exit(1)

    print(f"✓ Audio processing completed successfully.")
    return audio_path

