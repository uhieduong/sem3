"""
Workspace Setup & Directory Initializer
Sets up the canonical folder hierarchy, configurations, and verification checks.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_ROOT = WORKSPACE_ROOT / "pipeline"
RECORD_ROOT = WORKSPACE_ROOT / "record"
LECTURE_ROOT = WORKSPACE_ROOT / "lecture"
BIN_DIR = WORKSPACE_ROOT / "bin"
VSCODE_DIR = WORKSPACE_ROOT / ".vscode"
VENV_DIR = WORKSPACE_ROOT / ".venv"

GITIGNORE_CONTENT = """# Python & Environment
.venv/
__pycache__/
*.pyc

# Heavy Media Files
record/*.mp4
record/*.mkv
record/*.mov
record/*.webm
record/*.m4a
record/*.wav
record/*.mp3
record/*.aac
record/*.flac
pipeline/**/audio.mp3
pipeline/**/slides/*.png
pipeline/**/slide_timestamps.txt

# Local Binaries
bin/ffmpeg
bin/ffprobe

# OS & Editor
.DS_Store
.vscode/
"""

VSCODE_SETTINGS_CONTENT = """{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "terminal.integrated.env.osx": {
    "PATH": "${workspaceFolder}/.venv/bin:${workspaceFolder}/bin:${env:PATH}"
  }
}
"""

ACTIVATE_SH_CONTENT = """# Check if script is executed directly instead of sourced
if [ -n "$ZSH_VERSION" ]; then
  case $ZSH_EVAL_CONTEXT in *:file*) ;; *) 
    echo "⚠️  Do not run this script directly with './bin/activate.sh'."
    echo "👉  Run: source bin/activate.sh"
    return 1 2>/dev/null || exit 1
  ;; esac
  SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
elif [ -n "$BASH_VERSION" ]; then
  if [ "$0" = "$BASH_SOURCE" ]; then
    echo "⚠️  Do not run this script directly with './bin/activate.sh'."
    echo "👉  Run: source bin/activate.sh"
    exit 1
  fi
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Activate Python virtual environment if it exists
if [ -f "${WORKSPACE_DIR}/.venv/bin/activate" ]; then
  . "${WORKSPACE_DIR}/.venv/bin/activate"
fi

export PATH="${SCRIPT_DIR}:${PATH}"
echo "✓ Workspace environment activated (Python .venv + local ffmpeg ready)."
"""

def setup_directories() -> list[Path]:
    """Ensures all standard pipeline directories exist."""
    created = []
    directories = [
        RECORD_ROOT,
        LECTURE_ROOT,
        PIPELINE_ROOT,
        BIN_DIR,
        VSCODE_DIR,
    ]
    for d in directories:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(d)
    return created

def setup_configs() -> list[str]:
    """Generates standard configuration files if missing."""
    created_configs = []

    gitignore = WORKSPACE_ROOT / ".gitignore"
    if not gitignore.exists():
        with open(gitignore, "w", encoding="utf-8") as f:
            f.write(GITIGNORE_CONTENT.strip() + "\n")
        created_configs.append(".gitignore")

    vscode_settings = VSCODE_DIR / "settings.json"
    if not vscode_settings.exists():
        with open(vscode_settings, "w", encoding="utf-8") as f:
            f.write(VSCODE_SETTINGS_CONTENT.strip() + "\n")
        created_configs.append(".vscode/settings.json")

    activate_sh = BIN_DIR / "activate.sh"
    if not activate_sh.exists():
        with open(activate_sh, "w", encoding="utf-8") as f:
            f.write(ACTIVATE_SH_CONTENT.strip() + "\n")
        activate_sh.chmod(0o755)
        created_configs.append("bin/activate.sh")

    return created_configs

def check_binaries() -> dict[str, bool]:
    """Verifies that local or system FFmpeg and FFprobe exist."""
    results = {}
    for name in ["ffmpeg", "ffprobe"]:
        local_bin = BIN_DIR / name
        has_local = local_bin.is_file() and os.access(local_bin, os.X_OK)
        has_system = bool(shutil.which(name))
        results[name] = has_local or has_system
    return results

def check_python_environment() -> dict[str, bool]:
    """Checks required python libraries in .venv."""
    required = ["faster_whisper", "av", "pymupdf", "cv2", "PIL"]
    results = {}

    python_bin = VENV_DIR / "bin" / "python"
    if not python_bin.is_file():
        return {pkg: False for pkg in required}

    for pkg in required:
        res = subprocess.run(
            [str(python_bin), "-c", f"import {pkg}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        results[pkg] = (res.returncode == 0)

    return results

def run_workspace_setup():
    print("\n==========================================")
    print("🛠️  Initializing Lecture Workspace Directory")
    print("==========================================")

    created_dirs = setup_directories()
    if created_dirs:
        for d in created_dirs:
            print(f"  📁 Created directory: {d.relative_to(WORKSPACE_ROOT)}/")
    else:
        print("  ✓ Core directories already in place (record/, lecture/, pipeline/, bin/).")

    created_files = setup_configs()
    if created_files:
        for f in created_files:
            print(f"  📝 Initialized config: {f}")
    else:
        print("  ✓ Configuration files verified (.gitignore, .vscode/settings.json, bin/activate.sh).")

    # Check Binaries
    bins = check_binaries()
    print("\n📦 Binary Dependencies:")
    for bname, ok in bins.items():
        print(f"  {'✓' if ok else '✗'} {bname:<10}: {'Ready' if ok else 'Missing (check bin/)'}")

    # Check Python Packages
    pkgs = check_python_environment()
    print("\n🐍 Python Dependencies (.venv):")
    all_pkgs_ok = all(pkgs.values())
    for pkg, ok in pkgs.items():
        print(f"  {'✓' if ok else '✗'} {pkg:<15}: {'Installed' if ok else 'Missing'}")

    # Scan existing assets
    recs = sorted(list(RECORD_ROOT.glob("*.mp4")))
    decks = sorted(list(LECTURE_ROOT.glob("*.pdf")))
    tasks = [d for d in PIPELINE_ROOT.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))]

    print("\n📊 Current Workspace Assets:")
    print(f"  🎬 Video Recordings in record/ : {len(recs)} ({', '.join(r.name for r in recs) if recs else 'none'})")
    print(f"  📑 Slide Decks in lecture/     : {len(decks)} ({', '.join(d.name for r in decks for d in [r]) if decks else 'none'})")
    print(f"  📁 Pipeline Tasks in pipeline/ : {len(tasks)} ({', '.join(t.name for t in tasks) if tasks else 'none'})")

    print("\n==========================================")
    print("✨ Workspace is ready for lecture processing!")
    print("👉 Quick Start:")
    print("   1. Drop video recordings into 'record/' (e.g. record/lecture1.mp4)")
    print("   2. Drop presentation PDF decks into 'lecture/' (e.g. lecture/lecture1.pdf)")
    print("   3. Run: python run.py record/lecture1.mp4")
    print("==========================================\n")

