"""
Vision & Slide Intelligence Subsystem
Extracts slide keyframe snapshots, analyzes slide navigation/transitions,
flags external websites/apps with suggested search queries, and aligns snapshots
against PDF presentation decks.
"""

import re
import json
import subprocess
import urllib.parse
from collections import Counter
from pathlib import Path
from engine.config import (
    WORKSPACE_ROOT,
    LECTURE_ROOT,
    FFMPEG_BIN,
    SCENE_CHANGE_THRESHOLD,
    ORB_FEATURES_COUNT,
    MATCH_DISTANCE_THRESHOLD,
    MIN_FEATURE_MATCHES,
    MIN_SETTLED_DWELL_SEC,
    RAPID_FLIP_THRESHOLD_SEC,
    SLIDES_DIRNAME,
    SLIDE_MAPPING_FILENAME,
    DECK_ALIGNMENT_FILENAME,
    TRANSCRIPT_FILENAME
)

def format_dwell(seconds: float) -> str:
    """Formats dwell time into human-readable representation."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s:02d}s"

def pick_best_title_context(prev_title: str | None, next_title: str | None, context: str) -> str:
    """Selects the most relevant slide title based on word overlap with spoken context."""
    candidates = []
    for t in [prev_title, next_title]:
        if t and not t.startswith("Slide ") and "Non-deck" not in t:
            clean = re.sub(r'^[0-9]+[\)\.]\s*', '', t).strip()
            # Ignore purely numeric slide page numbers or overly brief labels
            if clean and not clean.isdigit() and len(clean) > 2 and clean not in candidates:
                candidates.append(clean)
    if not candidates:
        return ""

    ctx_lower = context.lower()
    scored = []
    for c in candidates:
        words = [w.lower() for w in re.findall(r'\b[A-Za-z]{3,}\b', c)]
        match_count = sum(1 for w in words if w in ctx_lower)
        scored.append((match_count, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]

def synthesize_search_query(context: str, prev_title: str | None, next_title: str | None) -> tuple[str, str]:
    """
    Synthesizes a precise search query and direct Google search link
    for an external website or application demonstrated in lecture.
    """
    if not context or not context.strip():
        best_title = pick_best_title_context(prev_title, next_title, "")
        q = f"{best_title} documentation" if best_title else "lecture reference documentation"
        return q, f"https://www.google.com/search?q={urllib.parse.quote_plus(q)}"

    # 1. Explicit URLs in speech
    url_match = re.search(r'\b(?:https?://|www\.)[^\s]+', context, re.IGNORECASE)
    if url_match:
        url = url_match.group(0).rstrip(".,;:")
        return url, url if url.startswith("http") else f"https://{url}"

    # 2. Explicit domain names
    domain_match = re.search(r'\b[a-zA-Z0-9-]+\.(?:com|org|edu|gov|io|dev|net|ai)\b', context, re.IGNORECASE)
    if domain_match:
        dom = domain_match.group(0)
        return dom, f"https://{dom}"

    # 3. Clean topic context from slide titles
    best_title = pick_best_title_context(prev_title, next_title, context)

    # 4. Extract acronyms / uppercase terms (e.g., FDD, XP, RUP, API, SQL, CSS, W3C, OOP)
    abbrevs = list(dict.fromkeys(re.findall(r'\b[A-Z]{2,6}\b', context)))

    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "and", "or", "in", "on", "at", "to", "for", "with",
        "that", "this", "it", "they", "we", "you", "i", "so", "of", "as", "by", "from", "be", "have", "has",
        "can", "see", "call", "called", "going", "what", "more", "focused", "actually", "under", "still",
        "next", "peer", "same", "also", "then", "just", "look", "like", "here", "there", "about", "some",
        "which", "when", "where", "how", "all", "any", "both", "each", "few", "more", "most", "other",
        "will", "would", "should", "could", "into", "over", "such", "than", "them", "these", "those",
        "your", "yours", "my", "mine", "our", "ours", "their", "theirs", "his", "her", "hers",
        "okay", "ok", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "got", "thing", "things", "let", "lets", "example", "examples", "way", "ways", "yeah", "yes",
        "right", "want", "need", "well", "know", "mean", "said", "say", "saying", "tell", "telling",
        "come", "goes", "make", "take", "give", "put", "use", "using", "used", "shows", "showing"
    }

    words = [w.lower() for w in re.findall(r'\b[A-Za-z]{3,}\b', context) if w.lower() not in stopwords]
    counts = Counter(words)

    query_parts = []
    if best_title and not best_title.isdigit():
        query_parts.append(best_title)
    for a in abbrevs[:2]:
        if a not in query_parts:
            query_parts.append(a)

    for w, _ in counts.most_common(5):
        if not any(w in qp.lower() for qp in query_parts):
            query_parts.append(w.capitalize())

    final_query = " ".join(query_parts[:4])
    return final_query, f"https://www.google.com/search?q={urllib.parse.quote_plus(final_query)}"

def auto_detect_deck(task_name: str, lecture_dir: Path | None = None) -> Path | None:
    """Finds a matching PDF slide deck in lecture/ based on task name."""
    search_dir = lecture_dir or LECTURE_ROOT
    if not search_dir.exists():
        return None

    clean_task = task_name.lower().replace("_", "").replace("-", "")
    for pdf in search_dir.glob("*.pdf"):
        clean_pdf = pdf.stem.lower().replace(" ", "").replace("_", "").replace("-", "")
        if clean_task in clean_pdf or clean_pdf in clean_task:
            return pdf
        # Match numeric components e.g. lecture1 vs lecture1.pdf or week01.pdf
        for i in range(1, 20):
            if f"lecture{i}" in clean_task or f"week{i}" in clean_task or f"week0{i}" in clean_task:
                if f"lecture{i}" in clean_pdf or f"week{i}" in clean_pdf or f"week0{i}" in clean_pdf:
                    return pdf
    return None

def extract_slides(video_path: Path, task_dir: Path, force: bool = False) -> list[dict]:
    """Extracts keyframe slides on scene changes and records frame timestamps."""
    slides_dir = task_dir / SLIDES_DIRNAME
    mapping_path = task_dir / SLIDE_MAPPING_FILENAME
    raw_timestamps = task_dir / "slide_timestamps.txt"

    if mapping_path.exists() and slides_dir.exists() and any(slides_dir.iterdir()) and not force:
        print(f"✓ Slides already extracted: {slides_dir.relative_to(WORKSPACE_ROOT)}")
        with open(mapping_path, "r", encoding="utf-8") as f:
            return json.load(f)

    slides_dir.mkdir(parents=True, exist_ok=True)
    print(f"🖼️  Detecting scene changes (> {SCENE_CHANGE_THRESHOLD}) and extracting slides...")

    cmd = [
        str(FFMPEG_BIN), "-y",
        "-i", str(video_path),
        "-vf", f"select='gt(scene,{SCENE_CHANGE_THRESHOLD})',showinfo",
        "-vsync", "vfr",
        str(slides_dir / "slide_%03d.png")
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    _, stderr_data = proc.communicate()

    with open(raw_timestamps, "w", encoding="utf-8") as f:
        f.write(stderr_data)

    mapping = []
    idx = 1
    for line in stderr_data.splitlines():
        if "Parsed_showinfo" in line and "pts_time:" in line:
            m = re.search(r"pts_time:\s*([\d\.]+)", line)
            if m:
                pts = float(m.group(1))
                minutes, seconds = divmod(int(pts), 60)
                mapping.append({
                    "slide": f"slide_{idx:03d}.png",
                    "time_sec": pts,
                    "timestamp": f"{minutes:02d}:{seconds:02d}"
                })
                idx += 1

    # Preliminary duration calculation
    for i in range(len(mapping)):
        curr_t = mapping[i]["time_sec"]
        next_t = mapping[i + 1]["time_sec"] if i + 1 < len(mapping) else curr_t + 45.0
        dur = max(0.1, round(next_t - curr_t, 2))
        mapping[i]["duration_sec"] = dur
        mapping[i]["dwell_str"] = format_dwell(dur)

    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"✓ Extracted {len(mapping)} slides into {slides_dir.relative_to(WORKSPACE_ROOT)}")
    return mapping

def analyze_slide_transitions(
    mapping: list[dict],
    transcript: list[dict] | None = None
) -> tuple[list[dict], list[dict]]:
    """
    Analyzes navigation dynamics:
    - Calculates slide dwell times
    - Identifies transient / rapid flipping before settling on desired slide
    - Detects reviews of earlier slides and forward jumps
    - Flags external website / application views with spoken context and search queries
    """
    if not mapping:
        return mapping, []

    # Estimate end time for last slide
    last_time = mapping[-1]["time_sec"] + 45.0
    if transcript:
        last_time = max(last_time, transcript[-1]["end"])

    # 1. Compute duration and basic status
    for i in range(len(mapping)):
        curr_t = mapping[i]["time_sec"]
        next_t = mapping[i + 1]["time_sec"] if i + 1 < len(mapping) else last_time
        dur = max(0.1, round(next_t - curr_t, 2))
        mapping[i]["duration_sec"] = dur
        mapping[i]["dwell_str"] = format_dwell(dur)

        is_ext = (mapping[i].get("deck_page") is None)
        mapping[i]["is_external"] = is_ext
        mapping[i]["is_settled"] = (dur >= MIN_SETTLED_DWELL_SEC)
        mapping[i]["is_transient"] = (dur < MIN_SETTLED_DWELL_SEC)

    # 2. Find next settled slide for every transient slide
    for i in range(len(mapping)):
        if mapping[i]["is_transient"]:
            for j in range(i + 1, len(mapping)):
                if mapping[j]["is_settled"] and not mapping[j]["is_external"]:
                    mapping[i]["settled_target"] = {
                        "slide": mapping[j]["slide"],
                        "deck_page": mapping[j].get("deck_page"),
                        "deck_title": mapping[j].get("deck_title"),
                        "timestamp": mapping[j]["timestamp"]
                    }
                    break

    # 3. Label navigation actions and correlate external websites
    last_settled_page = None
    external_events = []

    for i, m in enumerate(mapping):
        dur = m["duration_sec"]
        p = m.get("deck_page")

        # Surrounding slide titles for query synthesis
        prev_title = None
        for k in range(i - 1, -1, -1):
            if mapping[k].get("deck_title") and not mapping[k].get("is_external"):
                prev_title = mapping[k]["deck_title"]
                break
        next_title = None
        for k in range(i + 1, len(mapping)):
            if mapping[k].get("deck_title") and not mapping[k].get("is_external"):
                next_title = mapping[k]["deck_title"]
                break

        if m["is_external"]:
            m["nav_action"] = "external_screen"
            m["action_label"] = "🌐 External Website / App"

            ctx = ""
            if transcript:
                t_start = max(0, m["time_sec"] - 5.0)
                t_end = m["time_sec"] + dur + 5.0
                segs = [s["text"].strip() for s in transcript if not (s["end"] < t_start or s["start"] > t_end)]
                ctx = " ".join(segs)

            q, url = synthesize_search_query(ctx, prev_title, next_title)
            m["spoken_context"] = ctx
            m["search_query"] = q
            m["search_url"] = url

            external_events.append({
                "timestamp": m["timestamp"],
                "slide": m["slide"],
                "duration_sec": dur,
                "dwell_str": m["dwell_str"],
                "context": ctx or "(Audio transcript pending)",
                "search_query": q,
                "search_url": url
            })
        elif m["is_transient"]:
            tgt = m.get("settled_target")
            if tgt and tgt.get("deck_page"):
                m["nav_action"] = "rapid_flip"
                m["action_label"] = f"⏩ Rapid Flip (→ Slide {tgt['deck_page']})"
            else:
                m["nav_action"] = "rapid_flip"
                m["action_label"] = "⏩ Rapid Flip"
        else:
            # Settled presentation slide
            if last_settled_page is None:
                m["nav_action"] = "start_presentation"
                m["action_label"] = f"🎯 Start ({m['dwell_str']})"
            elif p is not None:
                if p < last_settled_page:
                    m["nav_action"] = "review_earlier_slide"
                    m["action_label"] = f"⏪ Review Earlier Slide (from p.{last_settled_page})"
                elif p > last_settled_page + 1:
                    m["nav_action"] = "jump_forward"
                    m["action_label"] = f"⏩ Jump Forward (from p.{last_settled_page})"
                elif p == last_settled_page:
                    m["nav_action"] = "continued_topic"
                    m["action_label"] = f"🎯 Continued ({m['dwell_str']})"
                else:
                    m["nav_action"] = "sequential_advance"
                    m["action_label"] = f"🎯 Settled ({m['dwell_str']})"
            last_settled_page = p

    return mapping, external_events

def generate_deck_alignment_report(
    task_dir: Path,
    deck_name: str,
    total_pages: int,
    mapping: list[dict],
    external_events: list[dict],
    aligned_count: int
) -> None:
    """Exports the rich markdown timeline and external activity reference table."""
    report_path = task_dir / DECK_ALIGNMENT_FILENAME
    settled_count = sum(1 for m in mapping if m.get("is_settled") and not m.get("is_external"))
    transient_count = sum(1 for m in mapping if m.get("is_transient") and not m.get("is_external"))

    lines = [
        f"# Slide Deck Alignment & Navigation Report\n",
        f"- **Task:** `{task_dir.name}`",
        f"- **Deck Source:** `{deck_name}` ({total_pages} slides)",
        f"- **Total Video Keyframes:** {len(mapping)}",
        f"- **Aligned Presentation Slides:** {aligned_count} / {len(mapping)}",
        f"- **Settled Topics:** {settled_count} slides | **Rapid Transitions:** {transient_count} flips",
        f"- **External Websites / Tools Flagged:** {len(external_events)}\n"
    ]

    if external_events:
        lines.append("## 🌐 External Websites & Application Activities Detected")
        lines.append("When the instructor switched away from slides to demonstrate an external site, tool, or document:\n")
        lines.append("| Timestamp | Duration | Video Frame | Spoken Context / Activity | Suggested Search | Direct Search Link |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for ev in external_events:
            ctx_summary = f"\"{ev['context'][:90]}...\"" if len(ev['context']) > 90 else f"\"{ev['context']}\""
            lines.append(
                f"| `{ev['timestamp']}` | {ev['dwell_str']} | `{ev['slide']}` | {ctx_summary} | "
                f"`{ev['search_query']}` | [🔍 Search Google]({ev['search_url']}) |"
            )
        lines.append("\n---\n")

    lines.append("## 📑 Complete Slide Navigation & Alignment Timeline\n")
    lines.append("| Timestamp | Video Frame | Deck Slide | Slide Title | Dwell | Status / Action | Score |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for item in mapping:
        ts = item.get("timestamp", "--:--")
        sname = item.get("slide", "")
        p = item.get("deck_page")
        page_str = f"Page {p}" if p else "—"
        title = item.get("deck_title", "Unknown")
        dwell = item.get("dwell_str", "")
        action = item.get("action_label", "")
        score = f"{item.get('deck_matches', 0)} pts"

        lines.append(f"| `{ts}` | `{sname}` | {page_str} | **{title}** | {dwell} | {action} | {score} |")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def align_slides_with_deck(
    task_dir: Path,
    deck_path: Path,
    min_matches: int = MIN_FEATURE_MATCHES
) -> list[dict]:
    """Matches video slide snapshots against PDF deck pages using ORB features."""
    import cv2
    import pymupdf
    import numpy as np

    deck_path = Path(deck_path).resolve()
    slides_dir = task_dir / SLIDES_DIRNAME
    mapping_file = task_dir / SLIDE_MAPPING_FILENAME

    if not deck_path.is_file():
        print(f"Warning: Deck not found at {deck_path}")
        return []

    if mapping_file.is_file():
        with open(mapping_file, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    else:
        mapping = [{"slide": f.name, "time_sec": None, "timestamp": "00:00"}
                   for f in sorted(slides_dir.glob("slide_*.png"))]

    print(f"\n📑 Loading slide deck: {deck_path.name}")
    doc = pymupdf.open(str(deck_path))
    total_pages = len(doc)

    # Render PDF pages to grayscale images & extract headings
    pdf_imgs, pdf_titles = [], []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=100)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
        pdf_imgs.append(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
        lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]
        pdf_titles.append(lines[0] if lines else f"Slide {i + 1}")

    orb = cv2.ORB_create(ORB_FEATURES_COUNT)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    pdf_descs = [orb.detectAndCompute(p, None) for p in pdf_imgs]

    print(f"🔬 Matching {len(mapping)} video snapshots against {total_pages} deck slides...")
    aligned_count = 0

    for item in mapping:
        slide_path = slides_dir / item.get("slide", "")
        if not slide_path.is_file():
            continue

        v_img = cv2.imread(str(slide_path), cv2.IMREAD_GRAYSCALE)
        if v_img is None:
            continue

        v_kp, v_desc = orb.detectAndCompute(v_img, None)
        if v_desc is None:
            item.update({"deck_page": None, "deck_title": "Non-deck visual (speaker/demo)", "deck_matches": 0, "deck_slide": None})
            continue

        scores = []
        for p_idx, (_, p_desc) in enumerate(pdf_descs):
            if p_desc is not None:
                matches = bf.match(v_desc, p_desc)
                scores.append((len([m for m in matches if m.distance < MATCH_DISTANCE_THRESHOLD]), p_idx + 1))

        if not scores:
            item.update({"deck_page": None, "deck_title": "Non-deck visual (speaker/demo)", "deck_matches": 0, "deck_slide": None})
            continue

        scores.sort(reverse=True)
        best_count, best_page = scores[0]

        if best_count >= min_matches:
            aligned_count += 1
            title = pdf_titles[best_page - 1]
            item.update({
                "deck_page": best_page,
                "deck_title": title,
                "deck_matches": best_count,
                "deck_slide": f"Slide {best_page} of {total_pages}"
            })
        else:
            item.update({
                "deck_page": None,
                "deck_title": "Non-deck visual (speaker/demo)",
                "deck_matches": best_count,
                "deck_slide": None
            })

    # Check for transcript to enrich transition and external web detection
    transcript = None
    transcript_path = task_dir / TRANSCRIPT_FILENAME
    if transcript_path.is_file():
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

    mapping, external_events = analyze_slide_transitions(mapping, transcript=transcript)

    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    generate_deck_alignment_report(task_dir, deck_path.name, total_pages, mapping, external_events, aligned_count)

    print(f"✅ Aligned {aligned_count} / {len(mapping)} slides to '{deck_path.name}'")
    if external_events:
        print(f"🌐 Flagged {len(external_events)} external website/app screen(s) with search queries.")
    return mapping

def enrich_slide_mapping(task_dir: Path) -> list[dict]:
    """
    Re-analyzes slide transitions and correlates external web screens
    once speech-to-text transcript is available.
    """
    mapping_file = task_dir / SLIDE_MAPPING_FILENAME
    transcript_file = task_dir / TRANSCRIPT_FILENAME

    if not mapping_file.is_file():
        return []

    with open(mapping_file, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    transcript = None
    if transcript_file.is_file():
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript = json.load(f)

    mapping, external_events = analyze_slide_transitions(mapping, transcript=transcript)

    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    # Re-generate report if alignment exists
    report_file = task_dir / DECK_ALIGNMENT_FILENAME
    deck_name = "Presentation Deck"
    total_pages = 0
    aligned_count = sum(1 for m in mapping if m.get("deck_page"))

    if report_file.is_file():
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()
        m_deck = re.search(r"Deck Source:\*\* `([^`]+)` \((\d+) slides\)", content)
        if m_deck:
            deck_name = m_deck.group(1)
            total_pages = int(m_deck.group(2))

    if total_pages > 0 or report_file.is_file():
        generate_deck_alignment_report(task_dir, deck_name, total_pages, mapping, external_events, aligned_count)
        print(f"✓ Enriched slide alignment with transcript context ({len(external_events)} external activities flagged)")

    return mapping
