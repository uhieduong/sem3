"""
Task Pipeline Orchestrator
Coordinates audio extraction, slide keyframing, deck alignment, and transcription.
Supports course-aware isolation across multiple subjects.
"""

from pathlib import Path
from engine.config import (
    WORKSPACE_ROOT,
    resolve_context,
    AUDIO_FILENAME,
    SLIDES_DIRNAME,
    SLIDE_MAPPING_FILENAME,
    TRANSCRIPT_FILENAME,
    DECK_ALIGNMENT_FILENAME,
    AUDIT_SUMMARY_FILENAME,
    DEFAULT_WHISPER_MODEL,
    DEFAULT_DEVICE,
    DEFAULT_COMPUTE_TYPE,
    CONFIDENCE_THRESHOLD,
    SUPPORTED_VIDEO_EXTS,
    SUPPORTED_AUDIO_EXTS
)
from engine.validator import validate_task_name, check_pipeline_isolation
from engine.audio import extract_audio
from engine.vision import extract_slides, align_slides_with_deck, auto_detect_deck, enrich_slide_mapping
from engine.transcriber import transcribe_audio

class TaskPipeline:
    def __init__(self, task_name: str, task_dir: Path | None = None, course_dir: Path | None = None):
        validate_task_name(task_name)
        self.task_name = task_name

        if course_dir:
            self.course_dir = Path(course_dir).resolve()
            self.pipeline_root = self.course_dir / "pipeline"
        elif task_dir:
            self.course_dir, _, _, self.pipeline_root = resolve_context(task_dir)
        else:
            self.course_dir, _, _, self.pipeline_root = resolve_context()

        self.task_dir = (task_dir or (self.pipeline_root / task_name)).resolve()
        self.task_dir.mkdir(parents=True, exist_ok=True)

        self.audio_path = self.task_dir / AUDIO_FILENAME
        self.slides_dir = self.task_dir / SLIDES_DIRNAME
        self.mapping_path = self.task_dir / SLIDE_MAPPING_FILENAME
        self.transcript_path = self.task_dir / TRANSCRIPT_FILENAME
        self.deck_alignment_path = self.task_dir / DECK_ALIGNMENT_FILENAME
        self.summary_path = self.task_dir / AUDIT_SUMMARY_FILENAME

    def find_summary_path(self) -> Path | None:
        """Finds the canonical verified summary file for this task."""
        canonical = self.task_dir / AUDIT_SUMMARY_FILENAME
        return canonical if canonical.is_file() else None

    def status(self) -> dict:
        slides_count = len(list(self.slides_dir.glob("slide_*.png"))) if self.slides_dir.is_dir() else 0
        summary_file = self.find_summary_path()
        has_transcript = self.transcript_path.is_file()
        has_mapping = self.mapping_path.is_file()
        return {
            "task_name": self.task_name,
            "course": self.course_dir.name,
            "directory": str(self.task_dir.relative_to(WORKSPACE_ROOT)),
            "has_audio": self.audio_path.is_file(),
            "slides_count": slides_count,
            "has_mapping": has_mapping,
            "has_deck_alignment": self.deck_alignment_path.is_file(),
            "has_transcript": has_transcript,
            "has_summary": summary_file is not None,
            "summary_path": str(summary_file.relative_to(WORKSPACE_ROOT)) if summary_file else None,
            "ready_for_audit": has_transcript and (has_mapping or slides_count == 0)
        }

    def print_status(self):
        st = self.status()
        summary_label = f"✓ Completed ({st['summary_path']})" if st['has_summary'] else "⏳ Pending"
        slides_label = f"✓ {st['slides_count']} slides" if st['slides_count'] else ("- None (audio-only)" if st['has_transcript'] else "✗ Missing")
        print(f"\n==========================================")
        print(f"📋 Course: {st['course']} | Task: {st['task_name']}")
        print(f"📁 Path  : {st['directory']}")
        print(f"==========================================")
        print(f"  🔊 Audio Extracted      : {'✓ Yes' if st['has_audio'] else '✗ Missing'}")
        print(f"  🖼️  Slide Keyframes      : {slides_label}")
        print(f"  📑 Deck Alignment       : {'✓ Yes' if st['has_deck_alignment'] else '- None'}")
        print(f"  📝 Whisper Transcript   : {'✓ Yes' if st['has_transcript'] else '✗ Missing'}")
        print(f"  ⚖️  Verified Audit Notes : {summary_label}")
        print(f"  🚀 Ready for Agent Audit: {'✓ Ready' if st['ready_for_audit'] else '✗ Incomplete'}")
        print(f"==========================================\n")

    def run(
        self,
        video_path: Path | None = None,
        audio_path: Path | None = None,
        deck_path: Path | None = None,
        no_deck: bool = False,
        skip_audio: bool = False,
        skip_slides: bool = False,
        skip_transcribe: bool = False,
        model_name: str = DEFAULT_WHISPER_MODEL,
        device: str = DEFAULT_DEVICE,
        compute_type: str = DEFAULT_COMPUTE_TYPE,
        threshold: float = CONFIDENCE_THRESHOLD,
        force: bool = False
    ):
        check_pipeline_isolation(self.pipeline_root)

        print(f"\n==========================================")
        print(f"🚀 Running Task: [{self.course_dir.name}] -> {self.task_name}")
        print(f"📁 Directory   : {self.task_dir.relative_to(WORKSPACE_ROOT)}")
        print(f"==========================================")

        # 1. Audio Ingestion & Extraction
        # Prioritize separated audio (e.g. .m4a, .mp3, .wav), then video recording
        audio_source = audio_path or (video_path if (video_path and Path(video_path).is_file()) else None)

        if not skip_audio:
            if audio_source:
                extract_audio(audio_source, self.task_dir, force=force)
            elif self.audio_path.is_file():
                print(f"✓ Pipeline audio already present: {self.audio_path.relative_to(WORKSPACE_ROOT)}")
            else:
                raise FileNotFoundError(
                    f"No audio source found for task '{self.task_name}'. "
                    f"Please provide an audio recording (e.g. .m4a, .mp3, .wav) or video recording (.mp4)."
                )

        # 2. Slide Keyframe Extraction & Deck Alignment (video only)
        has_video = video_path and Path(video_path).is_file() and Path(video_path).suffix.lower() in SUPPORTED_VIDEO_EXTS
        if not skip_slides:
            if has_video:
                extract_slides(video_path, self.task_dir, force=force)
                if not no_deck:
                    resolved_deck = deck_path or auto_detect_deck(
                        self.task_name,
                        lecture_dir=self.course_dir / "lecture"
                    )
                    if resolved_deck and resolved_deck.is_file():
                        align_slides_with_deck(self.task_dir, resolved_deck)
                    elif deck_path:
                        print(f"⚠️  Specified slide deck not found: {deck_path}")
            else:
                print(f"ℹ️  No video file provided (audio-only task). Skipping slide keyframe extraction.")

        # 3. Speech-to-Text Transcription
        if not skip_transcribe:
            if not self.transcript_path.is_file() or force:
                transcribe_audio(
                    self.audio_path,
                    self.transcript_path,
                    model_name=model_name,
                    device=device,
                    compute_type=compute_type,
                    threshold=threshold
                )
            else:
                print(f"✓ Transcript exists: {self.transcript_path.relative_to(WORKSPACE_ROOT)}")

            # Enrich slide transitions and external website references with transcript text if slides were extracted
            if self.mapping_path.is_file():
                enrich_slide_mapping(self.task_dir)

        print(f"\n✨ Task '{self.task_name}' in '{self.course_dir.name}' processed!")
        self.print_status()
