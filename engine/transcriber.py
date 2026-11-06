"""
Speech-to-Text Transcription Subsystem
Transcribes audio with word-level confidence flags using faster-whisper.
"""

import json
from pathlib import Path
from engine.config import (
    DEFAULT_WHISPER_MODEL,
    DEFAULT_DEVICE,
    DEFAULT_COMPUTE_TYPE,
    CONFIDENCE_THRESHOLD
)

def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

def transcribe_audio(
    audio_path: Path,
    output_path: Path,
    model_name: str = DEFAULT_WHISPER_MODEL,
    device: str = DEFAULT_DEVICE,
    compute_type: str = DEFAULT_COMPUTE_TYPE,
    threshold: float = CONFIDENCE_THRESHOLD,
    model_instance=None
) -> tuple[list[dict], object]:
    """Transcribes an audio file into structured JSON with word-level timestamps."""
    from faster_whisper import WhisperModel

    audio_path = Path(audio_path).resolve()
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if model_instance is None:
        print(f"⏳ Loading Whisper model: '{model_name}' ({device}, {compute_type})...")
        model_instance = WhisperModel(model_name, device=device, compute_type=compute_type)

    print(f"🚀 Transcribing '{audio_path.name}'...")
    segments, info = model_instance.transcribe(str(audio_path), word_timestamps=True)
    print(f"🌐 Language: {info.language} (probability: {info.language_probability:.2f})")

    transcript_data = []
    total_words, low_conf_words = 0, 0

    for i, seg in enumerate(segments, start=1):
        words = []
        has_low_conf = False

        for w in (seg.words or []):
            total_words += 1
            prob = round(w.probability, 2)
            words.append({"word": w.word, "prob": prob})
            if prob < threshold:
                has_low_conf = True
                low_conf_words += 1

        transcript_data.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "low_confidence_flag": has_low_conf,
            "words": words,
        })

        if i % 20 == 0:
            print(f"  [{format_time(seg.start)} -> {format_time(seg.end)}] {seg.text[:65]}...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Transcribed {len(transcript_data)} segments ({total_words} words, {low_conf_words} low-conf flagged)")
    return transcript_data, model_instance
