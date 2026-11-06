# Multi-Task Lecture Processing & Verification Pipeline

An isolated, task-partitioned workspace to ingest, transcribe, and verify multiple lecture recordings independently. Each lecture runs as a dedicated, self-contained task package inside `pipeline/<task_name>/` to guarantee that slide snapshots, transcripts, and audit summaries never cross-contaminate or mismatch.

All dependencies (`ffmpeg`, `ffprobe`, Python runtime, `faster-whisper`) are installed **locally inside this workspace** with zero global system modifications.

---

## Directory Organization

```text
se fundamentals/
├── bin/
│   ├── ffmpeg                     # Local FFmpeg binary (arm64)
│   ├── ffprobe                    # Local FFprobe binary (arm64)
│   └── activate.sh                # Shell activation script
├── .venv/                         # Isolated Python 3.12 environment
├── engine/                        # Modular Pipeline Backbone Engine
│   ├── config.py                  # Workspace paths & processing constants
│   ├── validator.py               # Strict naming & isolation guards
│   ├── audio.py                   # FFmpeg audio extraction subsystem
│   ├── vision.py                  # Slide detection & ORB deck alignment
│   ├── transcriber.py             # Faster-Whisper transcription engine
│   └── orchestrator.py            # TaskPipeline coordinator
├── run.py                         # Unified Backbone CLI Entrypoint
├── record/                        # Source recordings (.mp4)
│   ├── lecture1.mp4
│   └── lecture2.mp4
├── lecture/                       # Official PDF slide decks
│   ├── lecture1.pdf
│   └── lecture2.pdf
├── pipeline/                      # Task-partitioned pipeline outputs
│   ├── lecture1/                  # Task Package: Lecture 1
│   │   ├── audio.mp3              # Extracted 64k mono audio
│   │   ├── slides/                # Keyframe slide snapshots (PNG)
│   │   ├── slide_mapping.json     # Timestamp-to-slide lookup
│   │   ├── deck_alignment.md      # Timeline matched to lecture1.pdf
│   │   ├── transcript.json        # Structured transcript with confidence flags
│   │   └── summary_verified.md    # Verified audit summary
│   └── lecture2/                  # Task Package: Lecture 2
│       ├── audio.mp3
│       ├── slides/
│       ├── slide_mapping.json
│       ├── deck_alignment.md      # Timeline matched to lecture2.pdf
│       ├── transcript.json
│       └── summary_verified.md
├── setup_workspace.py         # Automated Directory & Workspace Setup Tool
├── audit.md                       # Strict audit & verification instructions for AI agents
└── README.md                      # This reference guide
```

---

## 1. Directory & Environment Setup

To initialize all required workspace directories (`record/`, `lecture/`, `pipeline/`, `bin/`), configurations (`.gitignore`, `.vscode/settings.json`), and verify binaries/libraries, run:

```zsh
python setup_workspace.py
# or
python run.py --setup
```

Before running processing commands in your terminal, activate the environment:

```zsh
source bin/activate.sh
```
*(Or simply open a new terminal tab in this workspace; `.vscode/settings.json` automatically loads the environment).*

---

## 2. Strict Input Naming Conventions & Task Isolation

To guarantee that lectures are **never entangled in a shared folder**, two strict checks run automatically on every execution:

### A. Task-Partitioned Directory Enforcement
All pipeline operations strictly run inside a dedicated subdirectory: `pipeline/<task_name>/`.
- The program **strictly forbids writing loose files** into the root `pipeline/` directory.
- An automatic **Pipeline Isolation Guard** runs at startup: if any loose media, transcript, or slides exist in `pipeline/` root, they are automatically quarantined to prevent multi-lecture contamination.

### B. Canonical Naming Conventions
Every input video, task name, and summary file is strictly validated before processing:

#### 1. Input Videos & Tasks:
| Pattern | Format | Examples |
| --- | --- | --- |
| **Numbered Lecture** | `lecture<N>` or `lecture_<N>` | `lecture1`, `lecture2`, `lecture03`, `lecture_4` |
| **Week-Indexed Session** | `week<NN>_<descriptor>` | `week01_intro`, `week02_process_models` |
| **Categorized Session** | `<type>_<descriptor>` | `tutorial_week02`, `workshop_agile`, `meeting_standup` |

#### 2. Summary Markdown Files:
| Pattern | Location | Description |
| --- | --- | --- |
| **Task Summary** | `pipeline/<task_name>/summary_verified.md` | Sole canonical summary file, strictly self-contained in its task directory |

> [!WARNING]
> Loose summary files in the root `pipeline/` directory (e.g. `pipeline/lecture2.md`) and generic filenames (e.g. `summary.md`, `notes.md`) are **rejected and quarantined** to prevent multi-lecture contamination.

To check any filename or summary file before running:
```zsh
python naming_validator.py "pipeline/lecture2/summary_verified.md"
python naming_validator.py "record/lecture1.mp4"
```

---

## 3. Running Tasks with the Unified CLI (`run.py`)

The pipeline provides a consolidated entrypoint, [`run.py`](./run.py), powered by the modular `engine/` backbone:

### Option A: End-to-End Execution
Process any combined video (`.mp4`), separated audio (`.m4a`, `.wav`), or audio+video pairs from start to finish:
```zsh
# Standard combined video:
python run.py record/lecture1.mp4

# Separated audio recording (.m4a, .mp3, .wav, etc.):
python run.py record/lecture1.m4a

# Explicit separated audio + video pairs:
python run.py lecture1 --audio record/lecture1.m4a --video record/lecture1.mp4 --course "se fundamentals"
```

### Option B: Media Extraction Only (Ready for Inspection / Audit Prep)
Extracts audio and slide keyframes and matches against the PDF deck without waiting for Whisper:
```zsh
python run.py record/lecture1.mp4 --extract-only
```

### Option C: Inspect Task Readiness & Extraction Status
Check the status of any task package:
```zsh
python run.py --status lecture1
python run.py --status lecture2
```

### Option D: Transcribe an Extracted Task
Run or re-run speech-to-text on an already extracted task:
```zsh
python run.py --transcribe lecture1 -m small
```

### Option E: Slide Deck Visual Alignment
Match or re-match slides against an official deck:
```zsh
python run.py --align lecture1 --deck lecture/lecture1.pdf
```

### Option F: Batch Ingest All Recordings
Process all video files currently inside `record/`:
```zsh
python run.py --all
```

---

### Option B: Step-by-Step Task Execution

If you prefer manual control for a task (e.g., `lecture1`):

#### 1. Setup Task Directories
```zsh
mkdir -p pipeline/lecture1/slides
```

#### 2. Extract Audio
```zsh
ffmpeg -i record/lecture1.mp4 -vn -ac 1 -b:a 64k pipeline/lecture1/audio.mp3
```

#### 3. Extract Slide Snapshots & Keyframe Timestamps
```zsh
ffmpeg -i record/lecture1.mp4 -vf "select='gt(scene,0.1)',showinfo" -vsync vfr pipeline/lecture1/slides/slide_%03d.png 2> pipeline/lecture1/slide_timestamps.txt
```

#### 4. Transcribe Audio
The script is task-aware and automatically routes to the right folder:
```zsh
# Run specific task by name:
python transcribe.py lecture1

# Or run by task directory:
python transcribe.py pipeline/lecture1

# Or batch transcribe all pending tasks:
python transcribe.py --all
```

---

## 4. Auditing & Verified Summarization

When you or an AI agent perform an audit on a lecture:
1. Refer to the rules in [`audit.md`](./audit.md).
2. Point the agent to the specific task folder (e.g. `pipeline/lecture2/`).
3. The agent cross-references:
   - `pipeline/<task>/transcript.json`
   - `pipeline/<task>/slide_mapping.json` (maps timestamps, dwell times, rapid flips, and settled slide targets)
   - `pipeline/<task>/deck_alignment.md` (timeline with slide transitions and flagged external websites/tools)
   - `pipeline/<task>/slides/`
4. **Slide Navigation Dynamics:**
   - When the lecturer switches back and forth between slides quickly before settling on a topic, `slide_mapping.json` and `deck_alignment.md` mark intermediate frames as `⏩ Rapid Flip (→ Slide X)` and point to the desired settled destination.
5. **External Websites & Application Detection:**
   - When the lecturer opens an external website, browser documentation, or tool, the frame is flagged as `🌐 External Website / App` along with the spoken audio context, a synthesized search query, and a direct Google search link so students can look up the site immediately.
6. The agent writes the final verified notes strictly to `pipeline/<task>/summary_verified.md`.
