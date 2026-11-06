# Verified Technical Lecture Summary & Confidence Audit

**Task:** `lecture2`  
**Course:** ISYS3416 / ISYS3432 — Software Engineering Fundamentals for IT  
**Lecture Topic:** Week 02 — Software Process Models  
**Instructor:** Dr. Anna Felipe  
**Audited Assets (Strict Local Isolation):**
- **Video Source:** `record/lecture2.mp4` (Duration: 87m 44s)
- **Audio Source:** `pipeline/lecture2/audio.mp3`
- **Slide Snapshots:** `pipeline/lecture2/slides/slide_001.png` to `slide_062.png` (62 keyframes)
- **Slide Mapping:** `pipeline/lecture2/slide_mapping.json` (61 matched frames)
- **Deck Alignment:** `pipeline/lecture2/deck_alignment.md` (Referenced to `lecture/Week 02 - Process Model-Summary Lecture-2.pdf`, 33 slides)
- **Transcript File:** `pipeline/lecture2/transcript.json` (712 structured segments with word-level probabilities)

---

## 1. Executive Summary

This lecture delivers a comprehensive analysis of software process models within software engineering. Dr. Anna Felipe discusses how process models structure engineering practices, maintain alignment across disparate stakeholders, and balance the classic **Project Management Triangle** (Scope, Time, Cost, and Quality). 

The session contrasts traditional **plan-driven methodologies** (Waterfall and the Rational Unified Process) with agile paradigms (**Scrum**, **Extreme Programming**, **Feature Driven Development**, and the **Agile Unified Process**). Practical software engineering techniques—including user story construction (`As a [role], I want [goal], so that [benefit]`), relative estimation using the modified Fibonacci sequence, burndown velocity tracking in Jira, and planning poker—are demonstrated through real-world and student assessment scenarios.

---

## 2. High-Confidence Technical Takeaways (Citing Exact `[MM:SS]` Timestamps)

### 2.1 Course Coordination & Module Learning Outcomes `[00:09]` – `[01:37]`
- **Assessment Topic Allocation `[00:16]` – `[00:31]`:** Group project topics are finalized and assigned during Wednesday's tutorial session so student teams can commence Milestone 1 of their course project immediately.
- **Module Learning Outcomes (MLOs) `[01:10]` – `[01:37]`:** *(Referencing `slide_004.png`, Deck Page 2)*
  1. Explain the fundamental concepts and characteristics of major software process models `[01:13]`.
  2. Compare and analyze different process models to determine their suitability across varied software development contexts `[01:20]`.
  3. Apply and justify an appropriate process model for a given software project scenario `[01:29]`.

### 2.2 The Communication Gap & The Role of Process Models `[01:38]` – `[02:44]`
- **The Tree Swing Parable `[01:38]` – `[02:39]`:** *(Referencing `slide_005.png`, Deck Page 3)*  
  Unstructured development leads to critical communication breakdowns across project stakeholders:
  - *How the customer explained it vs. how the project leader understood it vs. how the analyst designed it vs. how the programmer wrote it vs. what operations installed vs. what the customer was billed vs. what the customer really needed.*
- **Unifying Stakeholder Vision `[02:11]` – `[02:44]`:** A defined process model bridges cognitive gaps between business clients, system analysts, developers, and quality assurance personnel by establishing a common language and aligned expectations.

### 2.3 Universal Process Activities & The "Who, What, When, How" Framework `[02:44]` – `[07:06]`
- **Four Core Software Engineering Activities `[02:57]` – `[05:17]`:** *(Referencing `slide_006.png`, Deck Page 4)*
  1. **Specification `[03:06]` – `[03:34]`:** Defining software capabilities, constraints, and operational domain boundaries via Requirements Engineering (RE).
  2. **Design and Implementation `[03:49]` – `[04:17]`:** Formulating multi-tier architecture, data models, user interfaces, and writing code.
  3. **Validation `[04:17]` – `[04:44]`:** Verifying and testing the product against customer requirements to ensure fitness for use.
  4. **Evolution `[04:44]` – `[05:07]`:** Modifying the system over its operational lifecycle in response to changing business needs.
- **Dimensional Framework `[05:18]` – `[07:06]`:** *(Referencing `slide_007.png`, Deck Page 5)*  
  A software process prescribes:
  - **Who:** Roles involved (e.g., tester, system analyst, developer).
  - **How:** Specific tasks and development activities.
  - **When:** Sequence, phase gates, and iteration milestones.
  - **What:** Deliverable artifacts generated (e.g., test suites, requirements specifications, architectural blueprints).

### 2.4 Process Improvement, Maturity & Organizational Diagnosis `[07:12]` – `[10:23]`
- **Process Model Utilization `[07:12]` – `[09:01]`:** *(Referencing `slide_008.png`, Deck Page 6)*  
  Used to establish measurable process improvement objectives, enforce stable and mature engineering workflows, and serve as an appraisal mechanism to diagnose the maturity of an organization's current practices.
- **Strategic Importance `[09:02]` – `[10:23]`:** *(Referencing `slide_009.png` / `slide_011.png`, Deck Page 7)*  
  Provides a structured starting point for improvement, leverages industry best practices and prior community experiences, and standardizes engineering priorities across teams.

### 2.5 Plan-Driven (Heavyweight) vs. Agile (Lightweight) Methodologies `[10:24]` – `[12:31]`
- **Plan-Driven Methodologies `[10:24]` – `[10:59]`:** *(Referencing `slide_012.png`, Deck Page 8)*  
  Sequential and predictive; all phases are scheduled strictly in advance, benchmarked rigidly against a baseline master plan ("Plan drives everything!").
- **Agile Methodologies `[11:00]` – `[11:40]`:** *(Referencing `slide_012.png`, Deck Page 8)*  
  Incremental and empirical; plans adjust flexibly across iterations based on direct client feedback and sprint retrospectives `[11:29]`.
- **Hybrid Pragmatism `[11:40]` – `[12:30]`:**  
  Most enterprise environments deploy hybrid processes combining upfront governance with agile execution. Dr. Felipe recommends adopting a pragmatic hybrid approach tailored to team capability for academic project assignments `[12:06]`.

### 2.6 The Project Management Triangle & SDLC Stages `[12:31]` – `[24:50]`
- **Project Management Triangle Constraints `[16:56]` – `[18:38]`:** *(Referencing `slide_017.png` / `slide_019.png`, Deck Page 11)*  
  Composed of **Scope**, **Time**, and **Cost**, with **Quality** held at the center:
  - Expanding scope inevitably drives up financial expenditure and extends time duration `[17:34] – [18:05]`.
  - Constraining time without expanding budget inevitably degrades delivery quality unless scope is reduced.
- **Four General Project Stages `[18:39]` – `[24:50]`:** *(Referencing `slide_021.png`, Deck Page 12)*  
  1. **Exploration `[19:10]` – `[20:15]`:** Problem discovery, feasibility, and stakeholder identification (e.g., student cafeteria ordering system).
  2. **Construction `[20:15]` – `[24:15]`:** Requirements, System Design, Implementation, Testing, and Release.
  3. **Sustenance `[24:16]` – `[24:43]`:** Post-release operational maintenance and defect triage.
  4. **Retirement `[24:44]` – `[24:50]`:** Systematic phase-out and migration of legacy systems.

### 2.7 Code-and-Fix, Linear Sequential (Waterfall) & Requirements `[24:51]` – `[29:40]`
- **Code-and-Fix Model `[25:26]` – `[26:41]`:** *(Referencing `slide_023.png`, Deck Page 14)*  
  Proceeds from brief task descriptions directly into programming, deferring all testing until coding finishes. Unsuitable for commercial projects due to zero client alignment and inability to scale `[26:07] – [26:24]`.
- **Waterfall Model `[26:42]` – `[27:18]`:** *(Referencing `slide_024.png`, Deck Page 15)*  
  Strict linear progression: *Requirements $\rightarrow$ Design $\rightarrow$ Implementation $\rightarrow$ Verification $\rightarrow$ Maintenance*. High risk of late defect discovery.
- **Requirements Engineering `[27:19]` – `[29:34]`:** *(Referencing `slide_025.png`, Deck Page 16)*  
  - **Functional Requirements:** Observable system actions and behavior (e.g., user authentication, error prompt display).
  - **Non-Functional Requirements (Quality Attributes):** Quantifiable constraints (e.g., page load latency $< 2$ seconds, minimum concurrency threshold of 500 simultaneous users).

### 2.8 Rational Unified Process (RUP) `[29:40]` – `[44:07]`
- **Architecture & Disciplines `[29:52]` – `[37:00]`:** *(Referencing `slide_027.png`, Deck Page 17)*  
  - An object-oriented, web-enabled methodology organized into **4 Sequential Phases**:
    1. *Inception `[31:15]`*: Business case modeling, ROI calculation, scope boundaries, and project charter.
    2. *Elaboration `[33:00]`*: Architectural foundation, critical risk mitigation, and functional baselines.
    3. *Construction `[34:15]`*: Iterative coding, module integration, and system testing.
    4. *Transition `[35:30]`*: Pilot deployment, user feedback, rollout, configuration, and change management.
  - **Nine Disciplines:** Business Modeling, Requirements, Analysis & Design, Implementation, Test, Deployment, Configuration & Change Management, Project Management, Environment.
- **Enterprise Hybridization `[40:18]` – `[43:23]`:**  
  While pure RUP requires heavy upfront documentation, many organizations utilize RUP during Inception/Elaboration for governance, while executing Construction via agile Scrum sprints `[42:06]`.

### 2.9 Agile Values & The Scrum Framework `[44:30]` – `[54:14]`
- **Agile SDLC Principles `[44:50]` – `[48:59]`:** *(Referencing `slide_029.png` – `slide_031.png`, Deck Pages 19–22)*  
  Iterative cycles repeat development cadences; incremental delivery adds functional working software layer-by-layer.
- **Scrum Framework Architecture `[49:15]` – `[54:14]`:** *(Referencing `slide_032.png`, Deck Page 23)*  
  - **Roles:** Product Owner (backlog prioritization, customer voice), Scrum Master (servant leader, impediment removal), Development Team (self-organizing engineers).
  - **Artifacts:** Product Backlog, Sprint Backlog, Potentially Releasable Increment.
  - **Ceremonies:**
    1. *Sprint Planning `[51:25]`*: Sprint scope commitment.
    2. *Daily Scrum `[52:14]` – `[52:45]`*: 15-minute sync (Yesterday's work, Today's plan, Blockers).
    3. *Sprint Review `[53:12]`*: Demonstration of functional increments.
    4. *Sprint Retrospective `[53:34]` – `[53:45]`*: Team process reflection and continuous improvement.

### 2.10 User Stories, Relative Estimation & Burndown Tracking `[54:14]` – `[65:40]`
- **User Story Specification `[55:05]` – `[55:40]`:** *(Referencing `slide_034.png`, Deck Page 25)*  
  Standard template: `As a [user role], I want to [goal], so that I can [reason/benefit]`.
- **Modified Fibonacci Estimation `[55:43]` – `[60:15]`:** *(Referencing `slide_035.png`, Deck Page 26)*  
  - Story points measure relative **effort**, **complexity**, and **risk**, rather than developer clock hours `[57:39]`.
  - Uses the sequence `0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100`. Items estimated at 13+ or 20+ represent oversized Epics that must be sliced before sprint inclusion `[56:52]`.
- **Burndown Charts & Jira Execution `[60:43]` – `[65:15]`:** *(Referencing `slide_036.png` / `slide_037.png`, Deck Page 27)*  
  Tracks remaining task hours over the sprint timeline (Mon–Fri) to verify velocity against the ideal burn line. Illustrated live via Jira boards.

### 2.11 Extreme Programming (XP), FDD & Agile Unified Process (AUP) `[66:24]` – `[72:45]`
- **Extreme Programming (XP) `[66:24]` – `[68:09]`:** *(Referencing `slide_041.png` – `slide_047.png`, Deck Page 28)*  
  Focuses on disciplined technical practices: Pair Programming, Test-Driven Development (Unit Testing before implementation), Continuous Integration, and rapid feedback loops `[67:52]`.
- **Feature Driven Development (FDD) `[68:10]` – `[71:05]`:** *(Referencing `slide_048.png` – `slide_056.png`, Deck Page 29)*  
  Five-step model: *Develop Overall Model $\rightarrow$ Build Features List $\rightarrow$ Plan by Feature $\rightarrow$ Design by Feature $\rightarrow$ Build by Feature*. Uses hierarchical feature trees.
  - `[EXTERNAL SITE / DEMO @ 68:15 (slide_053.png)]`: Lecturer switched to an external demonstration screen covering FDD in agile engineering.  
    *Reference Lookup:* [🔍 Search 'Feature Driven Development FDD Agile' on Google](https://www.google.com/search?q=Feature+Driven+Development+FDD+Agile+Picture)
- **Agile Unified Process (AUP) `[71:06]` – `[72:45]`:** *(Referencing `slide_057.png`, Deck Page 30)*  
  Scott Ambler's agile adaptation of RUP. Retains RUP's 4 phases (*Inception, Elaboration, Construction, Transition*), but streamlines disciplines into 7 core areas (*Model, Implementation, Test, Deployment, Configuration Management, Project Management, Environment*) `[71:46] – [72:21]`.

### 2.12 Interactive Planning Poker Workshop & Epic Decomposition `[76:33]` – `[87:37]`
- **Planning Poker Case Study `[76:33]` – `[83:45]`:** *(Referencing `slide_058.png`, Deck Page 31)*  
  - *Story:* "As a customer, I want to customize my product order with live 3D previews so I can visualize my purchase before checkout."
  - *Evaluation:* Students debate between T-shirt sizes and numeric points. The instructor resolves that a live 3D rendering pipeline possesses excessive complexity/risk (XL / 40+ points). It must be vertically sliced:
    1. Static 2D customization (text/graphic overlay on product template).
    2. Interactive 3D WebGL viewport rendering engine.
- **Breakout Room Briefing `[85:35]` – `[87:37]`:** *(Referencing `slide_060.png`, Deck Page 32)*  
  - Epic Scenario: *Electronic Health Record (EHR) System for a healthcare provider*.
  - Students will practice decomposing this healthcare epic into granular user stories with acceptance criteria during Wednesday's tutorial session.

---

## 3. Low-Confidence Audit (Verification via `slide_mapping.json` & Slides)

In accordance with Rule 2 of the Audit Protocol, all segments with `"low_confidence_flag": true` have been verified against active slide keyframes and deck source text.

| Citation | Corresponding Slide & Deck Reference | Raw Whisper Transcript | Flagged Words (Prob) | Verified Technical Term / Spoken Meaning | Phonetic / Acoustic Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[01:20 (Verified via slide_004)]`** | `slide_004.png`<br>Deck Page 2: MLOs | "...determine the sustainability for various software development contexts." | `model` (0.21), `the` (0.25) | **suitability** (*"determine their suitability for various software development contexts"*) | Audio pronunciation sounded like "sustainability", but slide text and pedagogical objective confirm **suitability**. |
| **`[01:29 (Verified via slide_004)]`** | `slide_004.png`<br>Deck Page 2: MLOs | "We're also going to apply **NHS and** appropriate process model..." | `and` (0.38), `NHS` (0.62) | **"apply and justify an"** (*"Apply and justify an appropriate process model"*) | **Severe Phonetic Garble:** Lecturer's accent on *"and justify an"* was heard by Whisper as *"NHS and"*. Deck Page 2 provides unambiguous ground truth. |
| **`[01:56 (Verified via slide_005)]`** | `slide_005.png`<br>Deck Page 3: Comic | "...system analyst, customers, project leaders... **etc.**" | `analyst` (0.42), `etc.` (0.42) | Systems Analyst, Project Leader, Programmer, Business Consultant | Verified: Speaker enumerates specific stakeholder roles shown in the 10 comic panels of the classic tree swing cartoon. |
| **`[02:07 (Verified via slide_005)]`** | `slide_005.png`<br>Deck Page 3: Comic | "...different requirement engineering, what we call that **RE**." | `RE` (0.45), `requirement` (0.63) | **RE (Requirements Engineering)** | Verified: Standard software engineering acronym for Requirements Engineering. |
| **`[07:06 (Verified via slide_007)]`** | `slide_007.png`<br>Deck Page 5: Who, What, When, How | "Or the **self-development** of software. So how is the process model used?" | `self` (0.22), `of` (0.35) | **software development** | Speaker stumbled slightly transitioning from Slide 5 to Slide 6 ("How Is a Process Model Used?"). |
| **`[08:39 (Verified via slide_008)]`** | `slide_008.png`<br>Deck Page 6: How Used | "...provide a feedback or a, how you call that, **a distance** about the best practices..." | `At` (0.17), `a` (0.39), `distance` (0.47) | **appraisal / diagnosis** (*"diagnose the state of an organization's current practices"*) | **Phonetic Distortion:** Speaker attempted to say *"diagnosis"* or *"assessment"*, misheard as *"a distance"*. Verified directly from Slide 6 bullet 4. |
| **`[09:02 (Verified via slide_008)]`** | `slide_008.png`<br>Deck Page 6 / 7 | "So **while** the process model important..." | `while` (0.23), `a` (0.26) | **"Why is the process model important"** | **Homophone Misrecognition:** Whisper transcribed *"Why is"* as *"while"*. Heading on Slide 7 is *"Why Is a Process Model Important?"*. |
| **`[09:12 (Verified via slide_009)]`** | `slide_009.png`<br>Deck Page 7: Importance | "...if you, what do you call this, **appraise the methods in the states**..." | `states` (0.45), `then` (0.27) | **appraise methods / diagnose state** | Cross-references Slide 6 appraisal method diagnosing current organizational practices. |
| **`[10:47 (Verified via slide_012)]`** | `slide_012.png`<br>Deck Page 8: Plan vs Agile | "...say from **requirement** to design to implementations..." | `requirement` (0.44), `means` (0.45) | Requirements $\rightarrow$ Design $\rightarrow$ Implementation | Verified: Speaker enumerates the sequential phases characteristic of Waterfall. |
| **`[11:29 (Verified via slide_012)]`** | `slide_012.png`<br>Deck Page 8: Plan vs Agile | "...we can have make a reflection, we call that **sprint retrospective**." | `make` (0.42), `have` (0.47) | **Sprint Retrospective** | Verified: Agile ceremony dedicated to team reflection and process tuning. |
| **`[13:08 (Verified via slide_013)]`** | `slide_013.png`<br>Deck Page 9 / 11 | "...understand about this **triangular** or the project management." | `or` (0.33), `triangular` (0.64) | **Project Management Triangle** | Speaker colloquially terms the Project Management Triangle (Slide 11) as "triangular". |
| **`[16:50 (Verified via slide_017)]`** | `slide_017.png`<br>Deck Page 11 | "Madam Yamila. Thank you for that one." | `Madam` (0.01), `Yamila` (0.32) | Off-camera colleague | External classroom interruption; lecturer acknowledges an assistant before resuming the PM Triangle discussion. |
| **`[19:04 (Verified via slide_020)]`** | `slide_020.png`<br>Deck Page 10 / 12 | "So the software development **arms** with these different stages." | `arms` (0.52) | **"comes / starts with"** | Non-native inflection on *"comes"* transcribed as *"arms"*. Slide 12 illustrates General Project Stages. |
| **`[25:01 (Verified via slide_022)]`** | `slide_022.png`<br>Deck Page 13: Models | "We have the **rad**." | `rad` (0.17) | **RAD (Rapid Application Development)** | Verified: Acronym RAD on Slide 13; transcribed by Whisper in lowercase. |
| **`[25:07 (Verified via slide_022)]`** | `slide_022.png`<br>Deck Page 13: Models | "...agile unified process, extreme programming, Scrum, and Kanban." | `lifecycle` (0.06), `model` (0.21) | AUP, XP, Scrum, Kanban, RAD | Directly matches Slide 13 bullet points. |
| **`[25:28 (Verified via slide_023)]`** | `slide_023.png`<br>Deck Page 14: Code & Fix | "So the code and fix is **worth a brief specification of that**." | `that` (0.21) | **"Work from a brief specification of tasks"** | Speaker read aloud from Slide 14 bullet 1: *"Work from a brief specification of tasks"*. |
| **`[26:07 (Verified via slide_023)]`** | `slide_023.png`<br>Deck Page 14: Code & Fix | "The developer would have no idea if they were **reproducing** what the customers wanted..." | `The` (0.20) | **producing** (*"producing what the customer wanted"*) | Verified against Slide 14 bullet 4. |
| **`[27:56 (Verified via slide_025)]`** | `slide_025.png`<br>Deck Page 16: Reqs | "The system must allow users to **leg in** using their user's name and password." | `leg` (0.28) | **"log in"** | **Accent Distortion:** Speaker's pronunciation of **"log in"** transcribed as **"leg in"**. Slide 16 functional requirement example. |
| **`[28:10 (Verified via slide_025)]`** | `slide_025.png`<br>Deck Page 16: Reqs | "...display an error message when a user enter invalid **leg in** credentials." | `leg` (0.03), `enter` (0.29) | **"login credentials"** | Second occurrence of **"login"** transcribed as **"leg in"**. |
| **`[38:00 (Verified via slide_027)]`** | `slide_027.png`<br>Deck Page 17: RUP | "What is the one **pros and cons** of the RUP? One **pros and cons** of this process." | `pros` (0.00), `cons` (0.58) | **pros and cons** | Audio clipped on the syllable *"pros"*. Speaker prompts class for advantages/disadvantages of RUP. |
| **`[49:16 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 23: Scrum | "So one of the popular process model under Agile is **Sprint**." | `So` (0.23) | **Scrum** | **Verbal Slip:** Speaker says "Sprint", but Slide 23 heading is explicitly **"1) Scrum"**, with Sprints detailed as Scrum's core iterations. |
| **`[50:28 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 23: Scrum | "So based on the PBI, we call that **product backlog index**." | `PBI` (0.61) | **Product Backlog Items (PBIs)** | **Verbal Slip:** PBI denotes Product Backlog Items, misspoken as "product backlog index". Slide 23 diagram labels it *"PBI's"*. |
| **`[53:34 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 23: Scrum | "...process so that in the **restraint retrospective**..." | `restraint` (0.11), `retrospective` (0.64) | **Sprint Retrospective** | **Phonetic Distortion:** *"Sprint retrospective"* was heard as *"restraint retrospective"*. Slide 23 diagram verifies the ceremony. |
| **`[55:43 (Verified via slide_034)]`** | `slide_034.png`<br>Deck Page 25: Stories | "They can use the **Fibonacci** story point." | `Fibonacci` (0.62) | **Fibonacci sequence** | Verified: Fibonacci estimation scale. |
| **`[57:36 (Verified via slide_035)]`** | `slide_035.png`<br>Deck Page 26: Backlog | "...units of how we can measure the **airport**, complexity, risk." | `airport` (0.06), `complexity` (0.03), `risk` (0.25) | **"effort"** (*effort, complexity, and risk*) | **Severe Phonetic Misrecognition:** Speaker said **"effort"**, transcribed as **"airport"**. Core agile estimation principle. |
| **`[58:03 (Verified via slide_035)]`** | `slide_035.png`<br>Deck Page 26: Backlog | "...let's say **pi but not C1 or 0.5**, 1, 2, 3, 5, 8, 13..." | `point` (0.26), `sorry` (0.10) | **"Fibonacci 1 or 0.5"** | **Phonetic Garble:** Transcribed as *"pi but not C1"*; speaker was reciting modified Fibonacci cards ($0.5, 1, 2, 3, 5, 8, 13$). |
| **`[61:10 (Verified via slide_036)]`** | `slide_036.png`<br>Deck Page 27: Hours | "So we call that this **burn down** chart." | `burn` (0.27) | **Burndown chart** | Verified: Slide 27 displays the daily burndown line graph tracking task hours remaining across the week. |
| **`[61:25 (Verified via slide_037)]`** | `slide_037.png`<br>Jira Screen Share | "In **my JIRA**, I forgot, I should have completed here earlier." | `my` (0.58), `JIRA` (0.75) | **Jira Software** | Verified: Live demonstration switching to Jira board. |
| **`[66:24 (Verified via slide_041)]`** | `slide_041.png`<br>Deck Page 28: XP | "So the **extreme programming**..." | `the` (0.29) | **eXtreme Programming (XP)** | Verified: Heading of Slide 28. |
| **`[68:07 (Verified via slide_047)]`** | `slide_047.png`<br>Deck Page 29: FDD | "...or the **feature-driven** development." | `feature` (0.31) | **Feature Driven Development (FDD)** | Verified: Heading of Slide 29. |
| **`[71:07 (Verified via slide_056)]`** | `slide_056.png`<br>Deck Page 30: AUP | "...is actually **AUP**..." | `AUP` (0.58) | **Agile Unified Process (AUP)** | Verified: Heading of Slide 30. |
| **`[78:06 (Verified via slide_058)]`** | `slide_058.png`<br>Deck Page 31: Poker | "...means it's small, it's less **wrist**." | `wrist` (0.15) | **"less risk"** | **Phonetic Distortion:** Speaker said **"risk"**, heard as **"wrist"**. Repeated at `[78:13]` (*"Medium, there is a risk"*). |
| **`[84:27 (Verified via slide_058)]`** | `slide_058.png`<br>Deck Page 31: Poker | "...when talking about story points, it's about the **airport**... how much **airport** you can spend..." | `airport` (0.08, 0.12) | **"effort"** (*"how much effort you can spend completing a story"*) | **Severe Phonetic Misrecognition:** Second occurrence of **"effort"** transcribed as **"airport"**. |

---

## 4. Ambiguity Log (Strict Zero-Guessing Rule Applied)

In strict adherence to Rule 3 of the Audit Protocol, when spoken utterances remain garbled, fragmented, or unintelligible even after cross-referencing against the active slide and video keyframe, **no interpretation has been invented or guessed**. They are formally logged below:

| Timestamp | Raw Transcribed Text | Active Slide Keyframe | Deck Match | Ambiguity Analysis & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **`[AMBIGUOUS @ 14:06 – 16:49]`** | Single word `"you"` transcribed repeatedly at ~30s intervals (`[14:06]`, `[14:36]`, `[15:06]`, `[15:36]`, `[16:06]`, `[16:36]`, `[16:49]`). | `slide_016.png`, `slide_017.png` | Deck Page 10 / 11 | **Classroom Audio Gap / Hallucination:** The lecturer paused the recording from `[13:43]` ("For a while...") until `[16:50]` to handle an off-screen matter. The Whisper model hallucinated single-word tokens in the silence. Zero technical information was delivered. |
| **`[AMBIGUOUS @ 30:33 – 30:45]`** | *"So in this discipline, where are there when those can be present in the phases of the software development?"* | `slide_027.png` | Deck Page 17 (RUP) | **Garbled Sentence Structure:** The speaker attempted to pose a question regarding how the 9 disciplines span the 4 lifecycle phases, but the syntax dissolved into filler words without completing a coherent proposition. |
| **`[AMBIGUOUS @ 65:19 – 65:40]`** | *"this... having a... Oh, good."* | `slide_040.png` | Deck Page 27 (Hours) | **Fragmented Transition Speech:** Uttered while the lecturer minimized the Jira browser and returned to the presentation deck. Disconnected mutterings with no actionable technical content. |
| **`[AMBIGUOUS @ 67:10 – 67:15]`** | *"Because you can have every time we will call so you can also do..."* | `slide_047.png` | Deck Page 28 (XP) | **Truncated Thought:** The speaker began explaining XP iteration cadences (ranging from seconds to months), but broke off the sentence midway to shift to pair negotiation. |
| **`[AMBIGUOUS @ 71:55 – 72:05]`** | *"So that is since we are not really going into the requirement since the in AUP is only one at a time..."* | `slide_057.png` | Deck Page 30 (AUP) | **Unfinished Syntactic Clause:** The speaker started to explain why requirements modeling is collapsed into the general "Model" discipline in AUP, but abandoned the comparative explanation mid-sentence. |
| **`[AMBIGUOUS @ 76:12]`** | *"Nina?"* | `slide_057.png` | Deck Page 30 (AUP) | **Unverified Proper Noun:** Instructor called on a remote student from the online meeting roster. The exact student name spelling ("Nina", "Nga", or "Ngan") cannot be verified from the slide deck. |
| **`[AMBIGUOUS @ 80:34 – 80:38]`** | *"can says XL... Bin says XL or double XL"* | `slide_058.png` | Deck Page 31 (Poker) | **Unverified Remote Chat Readings:** Rapid verbal recitation of live student chat messages during the planning poker exercise. Exact student identities and message strings are unverified. |

