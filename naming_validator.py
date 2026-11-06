#!/usr/bin/env python3
"""
Naming Convention Validator CLI
Validates task names, recording video files, and summary markdown files.
Usage:
    python naming_validator.py lecture1
    python naming_validator.py record/lecture1.mp4
    python naming_validator.py record/lecture1.m4a
    python naming_validator.py pipeline/lecture2/summary_verified.md
    python naming_validator.py summary_verified.md
"""

import sys
from pathlib import Path
from engine.validator import validate_task_name, validate_summary_filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python naming_validator.py <task_name_or_filename>")
        sys.exit(1)

    target = sys.argv[1]
    path = Path(target)

    if path.suffix.lower() == ".md":
        validate_summary_filename(path.name, source_path=target)
        print(f"✓ Summary file '{path.name}' satisfies naming conventions!")
    else:
        stem = path.stem
        validate_task_name(stem, source_path=target)
        print(f"✓ Task/recording name '{stem}' satisfies naming conventions!")

