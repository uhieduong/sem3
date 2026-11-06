# Lecture Technical Audit & Verification Protocol

When an AI agent is instructed to audit and summarize a lecture, it **must operate strictly within the dedicated task directory** under `pipeline/<task_name>/` (e.g., `pipeline/lecture1/` or `pipeline/lecture2/`).

> [!IMPORTANT]
> **Zero Cross-Contamination Rule:**
> Every lecture task is completely self-contained. Never inspect slides or transcripts belonging to another task folder.

---

## Agent Output Naming Convention

When generating the verified summary, the agent must output strictly to:

- **Task Summary Path:** `pipeline/<task_name>/summary_verified.md`

### Output Rules for Agent:
1. **Canonical Location:** The verified summary MUST be placed directly inside the task directory: `pipeline/<task_name>/summary_verified.md` (e.g., `pipeline/lecture1/summary_verified.md`, `pipeline/lecture2/summary_verified.md`).
2. **No Loose Files:** Never output summaries or loose markdown files to the root `pipeline/` directory. The root `pipeline/` directory must contain only task folders.
3. **Strict Filename:** The filename must strictly be `summary_verified.md`. Do not use alternative or generic filenames (e.g., `summary.md`, `notes.md`, or `lecture2.md`).
4. **Markdown Format:** The file must be valid Markdown (`.md`).

---

## Task Assets Specification

For a specified task `<task_name>`:
- **Audio File:** `pipeline/<task_name>/audio.mp3` (normalized mono 16kHz audio ingested from video or separated audio like `.m4a`, `.wav`, `.mp3`)
- **Transcript File:** `pipeline/<task_name>/transcript.json`
- **Slide Snapshots:** `pipeline/<task_name>/slides/slide_*.png` (when video recording is present)
- **Slide Mapping:** `pipeline/<task_name>/slide_mapping.json` (maps timestamps to slide images, deck page numbers, and titles)
- **Deck Alignment Report:** `pipeline/<task_name>/deck_alignment.md` (timeline table against official presentation deck)

> [!NOTE]
> If a lecture was ingested from separated audio only (no video track), `pipeline/<task_name>/slides/` and `slide_mapping.json` will be absent. The agent performs the audit directly from `transcript.json` citing timestamps `[MM:SS]`.

---

## Slide Lookup & Navigation Procedure
When auditing an utterance at timestamp `[MM:SS]` (or second `S`):
1. Open `pipeline/<task_name>/slide_mapping.json` (or `deck_alignment.md`).
2. Find the entry whose `time_sec` is the largest value $\le S$ (the visual currently active on screen).
3. **Handling Slide Flipping (Rapid Transitions):**
   - Check `is_transient` and `action_label`. If the instructor was flipping back and forth quickly (`is_transient: true`), check `settled_target` to identify the desired destination slide where the instructor stopped and began explaining the concept.
   - Audit the utterance against the settled destination slide topic rather than intermediate transient frames.
4. **Handling Slide Jump-Backs / Reviews:**
   - If the action is `review_earlier_slide`, note that the instructor intentionally navigated backwards to an earlier slide (e.g., to reference a previous diagram or compare methodologies) before continuing forward.
5. **Handling External Websites & Applications:**
   - If `is_external: true` (`🌐 External Website / App`), the instructor opened an external browser window, documentation site, terminal, or tool outside the presentation deck.
   - Inspect `spoken_context`, `search_query`, and `search_url` in `slide_mapping.json` or in the top table of `deck_alignment.md`.
6. Verify the speaker's actual meaning using the official slide text or the flagged external reference.

---

## Summary Rules

The speaker has a non-native English accent. Generate the verified summary adhering strictly to these 4 rules:

1. **High-Confidence Points:**
   Summarize key conceptual and technical takeaways clearly, citing the exact `[MM:SS]` timestamp where the discussion begins.

2. **Low-Confidence Audit:**
   For all segments with `"low_confidence_flag": true`:
   - Look up the corresponding slide from `slide_mapping.json`.
   - Use the slide's text and diagrams to clarify phonetically garbled words or technical jargon (e.g., terminology, variable names, architectures).
   - Document the correction with citation `[MM:SS (Verified via slide_XXX)]`.

3. **External Website & Demo References:**
   When the instructor navigates to an external website or application:
   - Flag it explicitly with the citation:
     `[EXTERNAL SITE / DEMO @ MM:SS]`
   - Include the **Suggested Search Query & Direct Link** from `deck_alignment.md` so the user can easily find and bookmark the website referenced by the lecturer.
   - Summarize what the lecturer demonstrated or searched for while the external screen was active.

4. **Zero-Guessing Rule:**
   If an utterance remains unintelligible or ambiguous even after reviewing the active slide image or external context, **do not hallucinate or guess** what the speaker intended. Mark it explicitly as:
   `[AMBIGUOUS @ MM:SS]`
