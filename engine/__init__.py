"""
Lecture Processing & Audit Pipeline Engine
"""

from engine.config import (
    WORKSPACE_ROOT,
    PIPELINE_ROOT,
    RECORD_ROOT,
    LECTURE_ROOT
)
from engine.validator import validate_task_name, check_pipeline_isolation
from engine.audio import extract_audio
from engine.vision import extract_slides, align_slides_with_deck, auto_detect_deck
from engine.transcriber import transcribe_audio
from engine.orchestrator import TaskPipeline

__all__ = [
    "WORKSPACE_ROOT",
    "PIPELINE_ROOT",
    "RECORD_ROOT",
    "LECTURE_ROOT",
    "validate_task_name",
    "check_pipeline_isolation",
    "extract_audio",
    "extract_slides",
    "align_slides_with_deck",
    "auto_detect_deck",
    "transcribe_audio",
    "TaskPipeline",
]

