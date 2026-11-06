"""
Input Validation & Task Isolation System
Enforces canonical naming conventions for recordings, tasks, and summary files,
and guarantees that lecture tasks remain strictly isolated.
"""

import sys
import re
from pathlib import Path
from engine.config import PIPELINE_ROOT

# Strict Canonical Task Pattern:
# 1. lecture<N> or lecture_<N>   (e.g., lecture1, lecture02, lecture_1)
# 2. week<NN>_<descriptor>       (e.g., week01_intro, week2_process_models)
# 3. <type>_<descriptor>         (e.g., tutorial_week01, meeting_standup)
VALID_TASK_REGEX = re.compile(
    r"^(lecture[0-9]+|week[0-9]{1,2}(?:_[a-z0-9]+)+|(?:lecture|tutorial|workshop|meeting|seminar)(?:_[a-z0-9]+)+)$"
)

# Canonical Summary File:
# Strictly summary_verified.md inside pipeline/<task_name>/
CANONICAL_SUMMARY_FILENAME = "summary_verified.md"

def validate_task_name(task_name: str, source_path: str | Path | None = None) -> bool:
    """
    Validates task_name against canonical naming convention.
    Raises SystemExit with a detailed error message if validation fails.
    """
    clean_name = task_name.strip()

    if VALID_TASK_REGEX.match(clean_name):
        return True

    print("\n" + "=" * 65)
    print("❌ NAMING CONVENTION ERROR: Input Rejected")
    print("=" * 65)
    print(f"Provided Name: '{task_name}'")
    if source_path:
        print(f"Source File  : '{source_path}'")
    print("\nOperation ABORTED to prevent multi-lecture data entanglement.")
    print("Every input task and recording must strictly follow one of these patterns:\n")
    print("  1. lecture<N>              → Examples: lecture1, lecture02, lecture_3")
    print("  2. week<NN>_<descriptor>   → Examples: week01_intro, week02_process_model")
    print("  3. <type>_<descriptor>     → Examples: tutorial_week02, meeting_project_pitch")
    print("                             (types allowed: lecture, tutorial, workshop, meeting, seminar)")
    print("\nStrict Rules:")
    print("  • Must be strictly LOWERCASE.")
    print("  • No spaces, periods, or special characters (use '_' only).")
    print("  • Must identify the specific session (e.g. not generic 'presentation' or 'audio').")

    suggestion = suggest_rename(clean_name)
    print(f"\n💡 Suggested valid rename: '{suggestion}'")
    if source_path:
        src = Path(source_path)
        ext = src.suffix or ".mp4"
        print(f"   Fix command: mv \"{src}\" \"{src.parent / (suggestion + ext)}\"")
    print("=" * 65 + "\n")
    sys.exit(1)

def validate_summary_filename(
    filename: str,
    expected_task_name: str | None = None,
    source_path: str | Path | None = None
) -> bool:
    """
    Validates that a summary markdown file conforms to the canonical naming convention:
    strictly 'summary_verified.md' located inside the dedicated task directory:
    pipeline/<task_name>/summary_verified.md
    """
    path = Path(filename)
    clean_name = path.name.strip()

    is_valid = (clean_name == CANONICAL_SUMMARY_FILENAME)

    # If full path given, check that parent directory matches expected_task_name if provided
    if is_valid and expected_task_name and len(path.parts) > 1:
        parent_dir = path.parent.name
        if parent_dir != expected_task_name:
            is_valid = False

    if is_valid:
        return True

    print("\n" + "=" * 65)
    print("❌ SUMMARY NAMING CONVENTION ERROR: File Rejected")
    print("=" * 65)
    print(f"Provided Summary File: '{clean_name}'")
    if expected_task_name:
        print(f"Bound Task Name      : '{expected_task_name}'")
    if source_path:
        print(f"Source Location      : '{source_path}'")

    print("\nSummary files must strictly adhere to the canonical format:\n")
    print("  Dedicated Task Summary:  pipeline/<task_name>/summary_verified.md")
    print("  → Example: pipeline/lecture2/summary_verified.md")

    print("\nStrict Rules:")
    print("  • Must be named strictly 'summary_verified.md'.")
    print("  • Must be placed directly inside its task directory (never loose in pipeline/).")
    print("  • Extension must always be '.md' (Markdown).")

    suggestion = suggest_summary_rename(clean_name, expected_task_name)
    print(f"\n💡 Suggested canonical path: '{suggestion}'")
    if source_path:
        src = Path(source_path)
        print(f"   Fix command: mv \"{src}\" \"{suggestion}\"")
    print("=" * 65 + "\n")
    sys.exit(1)

def suggest_rename(raw_name: str) -> str:
    """Generates a normalized valid candidate from a raw/messy name."""
    name = re.sub(r"[^a-zA-Z0-9]+", "_", raw_name.lower()).strip("_")

    week_match = re.search(r"week[_\s]*([0-9]{1,2})", name)
    lec_match = re.search(r"(?:lecture|lec)[_\s]*([0-9]+)", name)

    if week_match:
        w_num = int(week_match.group(1))
        return f"week{w_num:02d}_lecture"
    elif lec_match:
        l_num = int(lec_match.group(1))
        return f"lecture{l_num}"
    elif name.startswith("meeting"):
        return "meeting_general"
    elif name.startswith("tutorial") or "tute" in name:
        return "tutorial_session"
    else:
        return f"lecture_{name}" if name else "lecture1"

def suggest_summary_rename(raw_filename: str, task_name: str | None = None) -> str:
    """Generates a valid canonical summary path from a raw/messy name."""
    if task_name:
        return f"pipeline/{task_name}/summary_verified.md"

    stem = Path(raw_filename).stem.lower()
    for drop in ["_summary_verified", "_summary", "summary_verified", "summary", "notes"]:
        stem = stem.replace(drop, "")
    stem = stem.strip("_-")
    clean_task = suggest_rename(stem) if stem else "lecture1"
    return f"pipeline/{clean_task}/summary_verified.md"

def check_pipeline_isolation(pipeline_root: Path = PIPELINE_ROOT, auto_quarantine: bool = True) -> bool:
    """
    Guarantees that pipeline/ contains ONLY isolated task directories.
    Loose files or legacy directories in pipeline root are strictly forbidden and quarantined.
    """
    if not pipeline_root.exists():
        return True

    loose_files = []
    loose_dirs = []

    for item in pipeline_root.iterdir():
        if item.name.startswith("."):
            continue
        if item.is_file():
            # Loose files are strictly forbidden at the pipeline root
            loose_files.append(item)
        elif item.is_dir() and item.name in ["slides", "output"]:
            loose_dirs.append(item)

    if not loose_files and not loose_dirs:
        return True

    print("\n⚠️  PIPELINE ISOLATION GUARD: Found loose items in pipeline root!")
    for f in loose_files:
        print(f"   - File: {f.name}")
    for d in loose_dirs:
        print(f"   - Legacy Folder: {d.name}/")

    if auto_quarantine:
        quarantine_dir = pipeline_root / "_legacy_loose_files"
        quarantine_dir.mkdir(exist_ok=True)
        print(f"📦 Quarantining loose items into '{quarantine_dir.name}/' to avoid data collision...")
        for f in loose_files:
            f.rename(quarantine_dir / f.name)
        for d in loose_dirs:
            if not any(d.iterdir()):
                d.rmdir()
            else:
                d.rename(quarantine_dir / d.name)
        print("✓ Root pipeline directory is now clean and strictly task-partitioned.\n")

    return True
