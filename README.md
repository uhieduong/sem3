# Semester 3 Multi-Course Lecture Processing & Verification Workspace

An isolated, multi-course workspace to ingest, transcribe, and verify lecture recordings independently across all Semester 3 subjects (`db application`, `further prg`, `se fundamentals`). Each lecture runs as a dedicated, self-contained task package inside its respective course's `pipeline/<task_name>/` to guarantee that slide snapshots, transcripts, and audit summaries never cross-contaminate or mismatch.

All heavy dependencies (`ffmpeg`, `ffprobe`, Python runtime, `faster-whisper`) are installed **locally in the workspace root** with zero global system modifications.

---

## Directory Organization

```text
sem3/
├── bin/                               # Shared local FFmpeg & FFprobe binaries (arm64)
│   ├── ffmpeg
│   ├── ffprobe
│   └── activate.sh                    # Shell activation script
├── .venv/                             # Shared isolated Python environment
├── engine/                            # Modular Pipeline Backbone Engine
│   ├── config.py                      # Multi-course resolver & workspace paths
│   ├── validator.py                   # Strict naming & isolation guards
│   ├── audio.py                       # Audio extraction subsystem
│   ├── vision.py                      # Slide detection, ORB alignment & web monitor
│   ├── transcriber.py                 # Faster-Whisper transcription engine
│   └── orchestrator.py                # TaskPipeline coordinator
├── run.py                             # Unified Multi-Course CLI Entrypoint
├── naming_validator.py                # Canonical filename & summary validator
│
├── db application/                    # Course: Database Applications
│   ├── lecture/                       # Official slide decks (lecture1.pdf, etc.)
│   ├── tutorial/                      # Tutorial worksheets (tutorial1.pdf, etc.)
│   ├── record/                        # Video & audio recordings
│   └── pipeline/                      # Task packages (lecture1/, lecture2/, etc.)
│
├── further prg/                       # Course: Further Programming (Java OOP)
│   ├── code/                          # Practical Java code & exercises
│   ├── lecture/
│   ├── tutorial/
│   ├── record/
│   └── pipeline/
│
└── se fundamentals/                   # Course: Software Engineering Fundamentals
    ├── assignment/                    # Course assessment specs
    ├── lecture/
    ├── tutorial/
    ├── record/
    └── pipeline/
        ├── lecture1/                  # Task Package: Lecture 1
        │   ├── audio.mp3              # Extracted 64k mono audio (git-ignored)
        │   ├── slides/                # Keyframe slide snapshots (git-ignored)
        │   ├── slide_mapping.json     # Timestamp-to-slide lookup
        │   ├── deck_alignment.md      # Timeline matched to lecture1.pdf
        │   ├── transcript.json        # Structured transcript with confidence flags
        │   └── summary_verified.md    # Verified audit summary
        └── lecture2/                  # Task Package: Lecture 2
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
# Run from workspace root (auto-detects target course from path):
python run.py "further prg/record/lecture2.mp4"
python run.py "db application/record/lecture2.mp4"
python run.py "se fundamentals/record/lecture2.mp4"

# Or cd into the course directory directly:
cd "further prg"
python run.py record/lecture2.mp4

# Separated audio recording (.m4a, .mp3, .wav, etc.):
python run.py "further prg/record/lecture2.m4a"

# Explicit separated audio + video pairs:
python run.py lecture1 --audio record/lecture1.m4a --video record/lecture1.mp4 --course "se fundamentals"
```

### Option B: Media Extraction Only (Ready for Inspection / Audit Prep)
Extracts audio and slide keyframes and matches against the PDF deck without waiting for Whisper:
```zsh
python run.py "further prg/record/lecture2.mp4" --extract-only
```

### Option C: Inspect Task Readiness & Extraction Status
Check the status of any task package:
```zsh
python run.py --status lecture2 --course "further prg"
python run.py --status lecture2 --course "db application"
```

### Option D: Transcribe an Extracted Task
Run or re-run speech-to-text on an already extracted task:
```zsh
python run.py --transcribe lecture2 -m small --course "further prg"
```

### Option E: Slide Deck Visual Alignment & Web Search Enrichment
Match slides against an official PDF deck and correlate speech context for web screen activities:
```zsh
python run.py --align lecture2 --deck "further prg/lecture/lecture2.pdf" --course "further prg"
```

### Option F: Batch Ingest All Recordings
Process all video files currently inside a course's `record/` directory:
```zsh
python run.py --all --course "further prg"
```

---

### Option G: Step-by-Step Task Execution

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
