#!/usr/bin/env python3
"""
Unified CLI Entrypoint for Lecture Pipeline
Supports multi-subject semester workspaces (e.g. 'se fundamentals', 'db application').
Handles single videos (.mp4), separated audio (.m4a, .wav, .mp3) + video pairs, or audio-only sessions.
Usage:
    # Target combined video or separated audio directly:
    python run.py "db application/record/lecture2.mp4"
    python run.py "se fundamentals/record/lecture1.m4a"

    # From inside a course folder:
    cd "db application" && python ../run.py record/lecture2.mp4

    # Using task name (auto-detects .m4a audio and/or .mp4 video in record/):
    python run.py lecture2 --course "db application"
    python run.py --status lecture2 --course "db application"
    python run.py --status lecture1 --course "se fundamentals"

    # Explicit separated audio & video flags:
    python run.py lecture1 --audio record/lecture1.m4a --video record/lecture1.mp4 --course "se fundamentals"

    # Batch process all media in record/ across all subjects:
    python run.py --all
    python run.py --setup
"""

import sys
import argparse
from pathlib import Path
from engine import (
    WORKSPACE_ROOT,
    TaskPipeline,
    validate_task_name,
    check_pipeline_isolation,
    auto_detect_deck,
    align_slides_with_deck
)
from engine.config import (
    resolve_context,
    SUPPORTED_VIDEO_EXTS,
    SUPPORTED_AUDIO_EXTS
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Unified Backbone CLI for Multi-Subject Lecture Pipeline."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Path to recording (e.g. 'record/lecture2.mp4', 'record/lecture2.m4a') or task name ('lecture2')."
    )
    parser.add_argument(
        "-c", "--course", "--subject",
        dest="course",
        default=None,
        help="Subject directory name (e.g. 'db application', 'se fundamentals')."
    )
    parser.add_argument(
        "--audio",
        dest="audio",
        default=None,
        help="Path to separated audio recording (e.g. 'record/lecture1.m4a', 'record/lecture1.wav')."
    )
    parser.add_argument(
        "--video",
        dest="video",
        default=None,
        help="Path to separated video recording (e.g. 'record/lecture1.mp4')."
    )
    parser.add_argument(
        "--deck", "--slides-deck",
        dest="deck",
        default=None,
        help="Path to presentation slide deck PDF (auto-detected from course lecture/ if omitted)."
    )
    parser.add_argument(
        "--no-deck",
        action="store_true",
        help="Disable slide deck matching."
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Extract audio, slide keyframes, and align deck only (skips Whisper transcription)."
    )
    parser.add_argument(
        "--transcribe-only", "--transcribe",
        dest="transcribe_only",
        action="store_true",
        help="Run Whisper transcription only on an already-extracted task."
    )
    parser.add_argument(
        "--align-only", "--align",
        dest="align_only",
        action="store_true",
        help="Run slide deck visual alignment only on an existing task."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display audit readiness and extraction status for a task."
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Initialize and verify workspace directory structure and configuration."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all recordings currently in record/."
    )
    parser.add_argument(
        "-m", "--model",
        default="small",
        help="Whisper model size: tiny, base, small, medium, large-v3 (default: small)."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-extraction and overwrite existing cached artifacts."
    )
    return parser.parse_args()

def resolve_target_and_course(
    target_str: str | None,
    course_arg: str | None,
    audio_arg: str | None = None,
    video_arg: str | None = None
):
    course_dir = None
    if course_arg:
        course_dir = (WORKSPACE_ROOT / course_arg).resolve()
        if not course_dir.is_dir():
            print(f"Error: Course directory '{course_dir}' does not exist.")
            sys.exit(1)

    video_path = Path(video_arg).resolve() if video_arg and Path(video_arg).is_file() else None
    audio_path = Path(audio_arg).resolve() if audio_arg and Path(audio_arg).is_file() else None

    # Check if target_str is a file directly, or relative to WORKSPACE_ROOT
    candidate_file = None
    if target_str:
        t_path = Path(target_str)
        if t_path.is_file():
            candidate_file = t_path.resolve()
        elif (WORKSPACE_ROOT / t_path).is_file():
            candidate_file = (WORKSPACE_ROOT / t_path).resolve()

    if candidate_file:
        ext = candidate_file.suffix.lower()
        task_name = candidate_file.stem
        if ext in SUPPORTED_AUDIO_EXTS:
            if not audio_path:
                audio_path = candidate_file
        elif ext in SUPPORTED_VIDEO_EXTS:
            if not video_path:
                video_path = candidate_file
        if not course_dir:
            course_dir, _, _, _ = resolve_context(candidate_file)
    elif target_str:
        task_name = Path(target_str).stem
    elif audio_path:
        task_name = audio_path.stem
    elif video_path:
        task_name = video_path.stem
    else:
        print("Error: No target recording or task name specified.")
        sys.exit(1)

    if not course_dir:
        ref = audio_path or video_path
        course_dir, _, _, _ = resolve_context(ref)

    # Auto-detect matching audio and/or video files in record/ if not yet resolved
    record_root = course_dir / "record"
    if record_root.is_dir():
        if not audio_path:
            for ext in SUPPORTED_AUDIO_EXTS:
                cand = record_root / f"{task_name}{ext}"
                if cand.is_file():
                    audio_path = cand.resolve()
                    break
        if not video_path:
            for ext in SUPPORTED_VIDEO_EXTS:
                cand = record_root / f"{task_name}{ext}"
                if cand.is_file():
                    video_path = cand.resolve()
                    break

    return task_name, course_dir, video_path, audio_path

def main():
    args = parse_args()

    if args.setup:
        from engine.setup import run_workspace_setup
        run_workspace_setup()
        return

    if args.all:
        all_courses = [
            d for d in WORKSPACE_ROOT.iterdir()
            if d.is_dir() and not d.name.startswith((".", "_", "bin", "engine"))
        ]
        total_found = 0
        for c in all_courses:
            record_dir = c / "record"
            if not record_dir.is_dir():
                continue

            # Group all media files by task name stem
            task_media: dict[str, dict[str, Path]] = {}
            for item in sorted(record_dir.iterdir()):
                if item.name.startswith("."):
                    continue
                ext = item.suffix.lower()
                stem = item.stem
                if ext in SUPPORTED_VIDEO_EXTS:
                    task_media.setdefault(stem, {})["video"] = item
                elif ext in SUPPORTED_AUDIO_EXTS:
                    task_media.setdefault(stem, {})["audio"] = item

            for stem, media in task_media.items():
                total_found += 1
                pipeline = TaskPipeline(stem, course_dir=c)
                pipeline.run(
                    video_path=media.get("video"),
                    audio_path=media.get("audio"),
                    skip_transcribe=args.extract_only,
                    model_name=args.model,
                    force=args.force
                )

        if total_found == 0:
            print("No audio or video recordings found in any course record/ folder.")
        return

    if not args.target and not args.audio and not args.video:
        print("Error: Please provide a target recording (e.g. .mp4, .m4a), or specify --audio / --video.")
        print("Usage:")
        print("  python run.py \"db application/record/lecture2.mp4\"")
        print("  python run.py \"se fundamentals/record/lecture1.m4a\"")
        print("  python run.py lecture1 --audio record/lecture1.m4a --video record/lecture1.mp4")
        sys.exit(1)

    task_name, course_dir, video_path, audio_path = resolve_target_and_course(
        args.target, args.course, audio_arg=args.audio, video_arg=args.video
    )
    pipeline = TaskPipeline(task_name, course_dir=course_dir)

    if args.status:
        pipeline.print_status()
        return

    if args.align_only:
        deck_file = Path(args.deck) if args.deck else auto_detect_deck(task_name, lecture_dir=course_dir / "lecture")
        if not deck_file or not deck_file.is_file():
            print("Error: No slide deck PDF specified or auto-detected.")
            sys.exit(1)
        align_slides_with_deck(pipeline.task_dir, deck_file)
        pipeline.print_status()
        return

    if args.transcribe_only:
        if not pipeline.audio_path.is_file() and not audio_path and not video_path:
            print(f"Error: Audio file not found for task '{task_name}' in '{course_dir.name}'.")
            sys.exit(1)
        pipeline.run(
            video_path=video_path,
            audio_path=audio_path,
            skip_audio=pipeline.audio_path.is_file() and not args.force,
            skip_slides=True,
            model_name=args.model,
            force=args.force
        )
        return

    if not video_path and not audio_path and not pipeline.audio_path.is_file():
        print(f"Error: No media file found for '{task_name}' in '{course_dir.name}/record/'.")
        print(f"Supported audio: {', '.join(sorted(SUPPORTED_AUDIO_EXTS))}")
        print(f"Supported video: {', '.join(sorted(SUPPORTED_VIDEO_EXTS))}")
        sys.exit(1)

    deck_path = Path(args.deck) if args.deck else None
    pipeline.run(
        video_path=video_path,
        audio_path=audio_path,
        deck_path=deck_path,
        no_deck=args.no_deck,
        skip_transcribe=args.extract_only,
        model_name=args.model,
        force=args.force
    )

if __name__ == "__main__":
    main()
