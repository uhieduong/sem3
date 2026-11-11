# Verified Technical Lecture Summary & Confidence Audit

**Task:** `lecture3`  
**Course:** ISYS3416 / ISYS3432 — Software Engineering Fundamentals for IT  
**Lecture Topic:** Week 03 — Requirements Engineering, UML Modeling & Use Cases  
**Instructor:** Dr. Anna Felipe  
**Audited Assets (Strict Task Directory Isolation):**
- **Video Source:** `record/lecture3.mp4` (Duration: 89m 54s)
- **Audio Source:** `pipeline/lecture3/audio.mp3`
- **Slide Deck Source:** `lecture/lecture3.pdf` (39 slides)
- **Keyframe Snapshots:** `pipeline/lecture3/slides/slide_001.png` to `slide_078.png` (78 keyframes)
- **Slide Mapping:** `pipeline/lecture3/slide_mapping.json` (78 entries)
- **Deck Alignment:** `pipeline/lecture3/deck_alignment.md` (76/78 aligned presentation slides)
- **Transcript File:** `pipeline/lecture3/transcript.json` (630 structured segments with word-level probabilities)

---

## 1. Executive Summary

This lecture covers **Requirements Engineering (RE)**, **Unified Modeling Language (UML)** classification, and formal requirements specification. Dr. Anna Felipe discusses how requirements form the critical bridge between raw customer needs and downstream technical implementation. 

The lecture examines the distinction between **User Requirements** (high-level, non-technical customer statements) and **System Requirements** (detailed operational and functional contracts), as well as **Functional Requirements (FR)** versus **Non-Functional Requirements (NFR / Quality Attributes)** illustrated through an automated teller machine (ATM) case study. Dr. Felipe details requirement elicitation techniques (interviews, ethnography, observation, scenarios), introduces structural versus behavioral UML diagrams, breaks down **Use Case Diagrams** and narrative **Use Case Specifications** (including basic and alternative flows), contrasts Use Cases with Agile **User Stories** and **Acceptance Criteria** (via the INVEST matrix), and demonstrates live architectural modeling in **StarUML**.

---

## 2. High-Confidence Technical Takeaways (Citing Exact `[MM:SS]` Timestamps)

### 2.1 Course Coordination & Module Learning Outcomes `[00:02]` – `[02:18]`
- **Lecture vs. Tutorial Boundary `[00:02]` – `[00:42]`:** Theory and foundational notations are delivered in the lecture, whereas hands-on writing of requirements, diagram drafting, and grading rubric alignments are practiced in the tutorial.
- **Module Learning Outcomes (MLOs) `[01:10]` – `[02:18]`:** *(Referencing `slide_003.png`, Deck Page 2)*
  1. Explain the principles of Requirements Engineering and distinguish between functional and non-functional requirements `[01:19]`.
  2. Apply modeling techniques to elicit, specify, and validate requirements using Use Cases and User Stories `[01:24]`.
  3. Estimate user story complexity and evaluate software requirements for correctness, completeness, and feasibility `[01:55]`.

### 2.2 Lifecycle Activities & The Customer Perception Bias ("A Bird in the the Bush") `[02:19]` – `[05:31]`
- **Software Lifecycle Activities `[02:19]` – `[04:02]`:** *(Referencing `slide_004.png`, Deck Page 3)*  
  Requirements Engineering sits across the initial phases of the Software Development Life Cycle (SDLC). Business analysts act as intermediaries translating ambiguous customer statements into verifiable technical specifications. While Agile/Scrum teams capture requirements as lightweight User Stories, RUP and formal enterprise projects capture them through structured Use Case specifications `[03:15]`.
- **Cognitive Bias Demonstration `[04:03]` – `[05:31]`:** *(Referencing `slide_005.png`, Deck Page 4)*  
  Dr. Felipe presents the classic perceptual illusion sign:
  ```text
        A
      BIRD
     IN THE
    THE BUSH
  ```
  Most engineers unconsciously filter out the duplicated word (*"THE THE"*), reading it as *"A bird in the bush"*. In requirements elicitation, developers similarly project their own assumptions onto the client's words rather than listening strictly to what the client explicitly stated `[05:14]`.

### 2.3 What is Requirements Engineering (RE) & The Requirements Process `[05:32]` – `[11:25]`
- **Definition of RE `[05:32]` – `[06:23]`:** *(Referencing `slide_006.png`, Deck Page 5)*  
  The systematic process of developing, identifying, analyzing, documenting, and validating the services a system must provide and the operational constraints under which it operates to ensure it meets stakeholder expectations.
- **The Core RE Process Workflow `[06:24]` – `[11:25]`:** *(Referencing `slide_007.png`, Deck Page 6)*  
  The process starts from a **Problem Statement** (e.g., manual stock auditing causing inventory record discrepancies) and proceeds through five interconnected activities:
  1. *Feasibility Study:* Assesses technical, financial, and organizational viability.
  2. *Requirements Elicitation & Analysis:* Gathers domain needs through interviews, observation, surveys, and workshops.
  3. *Requirements Specification:* Compiles formal documentation into a Software Requirements Specification (SRS), user stories, or behavioral models.
  4. *Requirements Validation:* Reviews documentation with stakeholders to guarantee consistency and correctness before code construction begins.
  5. *Requirements Management:* Controls changes and maintains traceability as business needs evolve.

### 2.4 Seven Sub-Activities in Requirements Engineering `[11:26]` – `[13:35]`
- **Process Breakdown `[11:26]` – `[13:35]`:** *(Referencing `slide_008.png` – `slide_009.png`, Deck Pages 7–8)*  
  Roger Pressman’s framework defines 7 distinct engineering activities:
  1. **Inception:** Establishing initial business context and project scope.
  2. **Elicitation:** Asking customers and users about objectives and features.
  3. **Elaboration:** Developing refined models (classes, use cases, state machines).
  4. **Negotiation:** Reconciling conflicting requirements across stakeholders regarding cost, time, and feasibility.
  5. **Specification:** Producing formal representations (SRS, user stories, prototypes).
  6. **Validation:** Reviewing specifications for ambiguity, omissions, and testability.
  7. **Management:** Tracking changes, approvals, and traceability links.

### 2.5 Types of Requirements: User Requirements vs. System Requirements `[13:36]` – `[22:11]`
- **Conceptual Distinctions `[13:36]` – `[16:21]`:** *(Referencing `slide_010.png`, Deck Page 9)*  
  - **User Requirements:** High-level natural language statements with informal diagrams describing what services the system provides and its operational constraints for non-technical stakeholders/clients `[14:03]`.
  - **System Requirements:** Detailed, structured specifications setting out precise descriptions of system functions, services, and operational constraints for developers and architectural engineers `[15:23]`.
- **Case Study Comparison: Mentcare Patient Management System `[16:22]` – `[22:11]`:** *(Referencing `slide_011.png` – `slide_012.png`, Deck Page 10)*  
  - *User Requirement (Mental Health Clinic):* "The MHC-PMS shall generate monthly summary reports showing the cost of drugs prescribed by each clinic during that month" `[17:11]`.
  - *Derived System Requirements:*
    1. On the last working day of each month, a summary report shall be automatically generated for each clinic listing drug names, total prescription units, and total costs `[17:27]`.
    2. Reports shall be restricted to authorized clinic directors and pharmacists via role-based access control `[18:45]`.
    3. User password inputs must be encrypted (e.g. SHA-256) and session timeouts enforced after inactivity `[19:00] – [19:54]`.

### 2.6 Functional vs. Non-Functional Requirements (NFRs) `[22:12]` – `[30:04]`
- **Definitions `[22:12]` – `[24:38]`:** *(Referencing `slide_013.png`, Deck Page 11)*  
  - **Functional Requirements (FR):** Statements of services the system must perform, how it reacts to specific inputs, and how it behaves in particular situations (e.g., input calculation, database persistence, user registration). Uses explicit modal verbs: *"The system shall..."* or *"The system shall not..."* `[24:41]`.
  - **Non-Functional Requirements (NFR):** Constraints placed on services or functions (performance, response latency, security, reliability, availability, portability, standards compliance) `[23:42]`.
- **ATM Case Study `[24:39]` – `[27:49]`:** *(Referencing `slide_014.png`, Deck Page 12)*  
  - *Functional:* The ATM system shall validate the PIN entered against the bank account server `[25:03]`.
  - *Non-Functional:* The ATM system shall process cash dispensation and return card within 3 seconds of transaction approval; transaction data in transit must be protected under 256-bit encryption.
- **Criticality Analysis `[27:50]` – `[30:04]`:** *(Referencing `slide_015.png`, Deck Page 14)*  
  Dr. Felipe highlights that NFRs are often **more critical** than individual functional features: if an application's security or reliability fails, or if transaction latency is unacceptable, the entire system is rendered useless even if functional buttons work properly `[27:50] – [28:30]`.

### 2.7 Requirements Elicitation and Analysis Challenges `[30:05]` – `[36:33]`
- **The Elicitation Cycle `[30:05]` – `[35:55]`:** *(Referencing `slide_017.png`, Deck Page 16)*  
  Iterative stages: *Requirements Discovery $\rightarrow$ Classification & Organization $\rightarrow$ Prioritization & Negotiation $\rightarrow$ Requirements Specification*.
- **Practical Industry Roadblocks `[35:56]` – `[36:33]`:** *(Referencing `slide_018.png` – `slide_020.png`, Deck Page 17)*  
  - Stakeholders frequently struggle to articulate their actual needs in technical terminology.
  - Conflicting requirements emerge across internal departments (e.g., marketing wants open data, security wants locked access) `[41:23]`.
  - Scope creep and shifting business priorities throughout project construction `[42:25]`.

### 2.8 Techniques to Elicit Requirements `[36:34]` – `[43:31]`
- **Core Techniques `[36:34]` – `[43:31]`:** *(Referencing `slide_021.png`, Deck Page 18)*  
  1. **Interviews:** Closed (structured against predefined questions) vs. Open (exploratory discussions).
  2. **Observation & Ethnography:** Watching end-users perform daily tasks to discover unstated operational workflows.
  3. **Surveys & Questionnaires:** Efficient for gathering statistical input from distributed customer bases.
  4. **Document Analysis:** Reviewing existing corporate forms, business rule sheets, legacy code, and workflow manuals.
  5. **Workshops / Focus Groups:** Fast-paced stakeholder alignment sessions to negotiate trade-offs.
  6. **Prototyping:** Building early mockups to elicit feedback on UI and behavioral flows.

### 2.9 Scenario-Based Design & Real-World User Scenarios `[43:32]` – `[51:27]`
- **Scenario Architecture `[43:32]` – `[46:49]`:** *(Referencing `slide_022.png` – `slide_026.png`, Deck Page 19)*  
  A scenario provides a narrative, user-centered description of how an end-user executes a task in a specific operational context. It anchors specifications in concrete interactions rather than abstract specifications `[44:21]`.
- **Retail POS Counter Example `[46:50]` – `[48:37]`:** *(Referencing `slide_027.png` – `slide_028.png`, Deck Pages 20–21)*  
  - *Context:* Customer approaches counter with products; cashier scans barcodes via handheld reader.
  - *Normal Flow:* Cashier totals items; customer presents payment; system prints receipt and updates inventory database `[47:21]`.
  - *Exception Paths:* Unreadable barcode requiring manual SKU keypad input; card declined; customer cancels transaction.
- **Iterative Nature `[48:38]` – `[51:27]`:** *(Referencing `slide_029.png`, Deck Page 22)*  
  Requirements elicitation is inherently time-consuming and non-linear, often requiring more cognitive effort and calendar time than code writing `[51:10]`.

### 2.10 Introduction to UML: Structural vs. Behavioral Modeling `[51:28]` – `[55:56]`
- **UML 2.2 Taxonomy `[51:28]` – `[55:22]`:** *(Referencing `slide_030.png` – `slide_031.png`, Deck Pages 23–24)*  
  The Unified Modeling Language provides standardized visual semantics partitioned into two broad hierarchies:
  - **Structural Diagrams (Static):** Class, Object, Component, Composite Structure, Package, Deployment, and Profile diagrams `[52:02]`.
  - **Behavioral Diagrams (Dynamic):** Use Case, Activity, State Machine, and Interaction diagrams (Sequence, Communication, Interaction Overview, Timing) `[52:40]`.
- **Course Scope Focus `[55:23]` – `[55:56]`:**  
  Dr. Felipe emphasizes that this course concentrates specifically on four diagrams: **Use Case Diagrams**, **Activity Diagrams**, **Sequence Diagrams**, and **Class Diagrams**.

### 2.11 Use Case Diagrams in Detail `[55:57]` – `[65:07]`
- **Core Semantic Elements `[55:57]` – `[59:08]`:** *(Referencing `slide_032.png`, Deck Page 26)*  
  - **System Boundary:** A rectangle enclosing use cases, delineating what is internal to the application versus external entities.
  - **Actors:** Represented as **stick figures** (`slide_032.png`). Actors are external entities that interact with the system (can be human users or external software/hardware systems).
  - **Use Cases:** Enclosed inside **ovals** representing complete functional goals.
  - **Naming Convention:** Must be named strictly using an **Action Verb + Noun** phrase (e.g., *Withdraw Cash*, *Check Balance*, *Replenish Cash*, *Enroll Course*) `[57:26] – [57:41]`.
- **Use Case Granularity `[59:09]` – `[64:38]`:**  
  Dr. Felipe warns students against overly broad labels (e.g., *"Manage Students"*). Instead, decompose administrative functionality into specific CRUD actions: *Add Student*, *Update Student Profile*, *View Student Record*, or *Delete Student* `[62:12] – [62:44]`.

### 2.12 Banking Case Study: Partner Systems & Secondary Actors `[65:08]` – `[68:56]`
- **Vietcombank & Shinhan Bank Architecture `[65:08]` – `[68:11]`:** *(Referencing `slide_032.png`, Deck Page 26)*  
  - *Scenario:* A customer holding an account with **Shinhan Bank** uses an ATM owned and operated by **Vietcombank** to withdraw cash `[65:08] – [65:25]`.
  - *Primary Actor:* Bank Customer (initiates the *Withdraw Cash* interaction at the ATM).
  - *Secondary Actor:* **Shinhan Bank Core System** (an external server outside the Vietcombank ATM system boundary that validates card credentials, verifies account balance, and approves debit transactions) `[66:18] – [66:47]`.
  - *Preconditions:* Customer card inserted; valid PIN authenticated; account has sufficient funds `[67:27]`.
  - *Postconditions:* Cash dispensed; receipt printed; Shinhan Bank account debited; ATM internal cash inventory updated `[67:50] – [68:11]`.

### 2.13 Use Case Specifications: Templates, Main Flows & Alternative Flows `[68:57]` – `[73:15]`
- **Specification Template Attributes `[68:57]` – `[71:23]`:** *(Referencing `slide_034.png` – `slide_038.png`, Deck Pages 29–31)*  
  Each use case oval in a diagram must be backed by a written Use Case Specification:
  - *Use Case ID & Title:* e.g., `UC-01: Create Customer Account`.
  - *Primary Actor, Preconditions, Postconditions, and Trigger.*
  - *Main Success Scenario (Basic Flow):* Numbered two-column or narrative steps detailing the standard user-system interaction `[70:11] – [70:33]`.
- **Alternative & Exception Flows `[71:24]` – `[73:15]`:** *(Referencing `slide_039.png` – `slide_043.png`, Deck Page 32)*  
  Branching logic handling anomalies:
  - *Step 3a:* Invalid email address or duplicate user ID entered $\rightarrow$ system displays error banner and prompts re-entry `[72:25]`.
  - *Step 3b:* User cancels transaction $\rightarrow$ system discards entered form data and terminates without account creation `[72:58]`.

### 2.14 User Stories, INVEST Criteria & Acceptance Criteria `[73:16]` – `[76:48]`
- **Agile User Story Format `[73:16]` – `[74:11]`:** *(Referencing `slide_044.png`, Deck Page 34)*  
  Template: `As a [user role], I want [goal], so that [benefit]`.
- **The INVEST Quality Matrix `[74:12]` – `[75:44]`:** *(Referencing `slide_044.png` / `slide_048.png`, Deck Page 34)*  
  Effective user stories must satisfy:
  - **I**ndependent: Sliced cleanly with minimal dependency on other stories.
  - **N**egotiable: Open to collaborative adjustment between product owner and engineers.
  - **V**aluable: Delivers observable end-user or business utility.
  - **E**stimable: Well understood so developers can assign story points.
  - **S**mall: Sized appropriately to fit within a single sprint.
  - **T**estable: Equipped with clear verification criteria.
- **Acceptance Criteria `[75:45]` – `[76:48]`:** *(Referencing `slide_051.png`, Deck Page 35)*  
  Defines boundary conditions for completion using checklist points or BDD format (*Given [precondition], When [action], Then [expected result]*).

### 2.15 Comparing Use Cases vs. User Stories `[76:49]` – `[78:56]`
- **Comparative Analysis `[76:49]` – `[78:56]`:** *(Referencing `slide_059.png`, Deck Page 36)*  
  | Dimension | **Use Case** | **User Story** |
  | :--- | :--- | :--- |
  | **Format** | UML diagram (actors, ovals) + formal multi-page specification table | Short text card (`As a... I want... so that...`) |
  | **Detail Level** | Comprehensive; details basic, alternative, and exception paths | Lightweight; acts as an invitation for conversation |
  | **Perspective** | System and procedural interaction focus | User-centric business value focus |
  | **Suitability** | Large enterprise, mission-critical, or plan-driven (RUP/Waterfall) systems | Fast-paced agile and iterative projects (Scrum/XP) |

### 2.16 Live Modeling in StarUML & Assignment Briefing `[78:57]` – `[89:53]`
- **Live Demonstration `[80:27]` – `[83:55]`:** *(Referencing `slide_065.png` – `slide_067.png`)*  
  Dr. Felipe launches **StarUML** on macOS to model the banking case study live:
  - Adding the system boundary rectangle (*"Vietcombank ATM System"*).
  - Adding the primary actor stick figure (*"Bank Customer"*).
  - Placing use case ovals (*"Withdraw Cash"*).
  - Adding the secondary actor stick figure (*"Shinhan Bank System"*).
  - Drawing directed associations showing the cross-system verification handshake.
- **Assignment 1 Support `[84:22]` – `[89:53]`:**  
  Dr. Felipe answers student questions regarding Assignment 1, explaining how swimlanes partition actor responsibilities in activity diagrams and advising students to practice use case specifications on Canvas.

---

## 3. Low-Confidence Audit (Verification via `slide_mapping.json` & Slides)

In accordance with Rule 2 of the Audit Protocol, segments marked with `"low_confidence_flag": true` have been verified against active slide keyframes and source deck pages.

| Citation | Corresponding Slide & Deck Reference | Raw Whisper Transcript | Flagged Words (Prob) | Verified Technical Term / Spoken Meaning | Phonetic / Acoustic Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[04:33 (Verified via slide_005)]`** | `slide_005.png`<br>Deck Page 4: Customer Say | "...I missed the **double z**..." | `z.` (0.16), `a` (0.37) | **"double the"** | **Phonetic Slur:** Lecturer said *"I missed the double 'the'"*, referencing the triangle reading *"A BIRD IN THE THE BUSH"*. Transcribed as *"double z"*. |
| **`[05:44 (Verified via slide_006)]`** | `slide_006.png`<br>Deck Page 5: What is RE | "**RE**, we call that RE, is the systematic process..." | `RE,` (0.02) | **RE (Requirements Engineering)** | Acronym pronounced quickly; verified from Slide 5 title and text. |
| **`[16:24 (Verified via slide_011)]`** | `slide_011.png`<br>Deck Page 10: User & System Reqs | "...the **meant care** system..." | `meant` (0.28), `differentiate` (0.09) | **Mentcare** (*MHC-PMS*) | **Acoustic Misrecognition:** Ian Sommerville's classic Mental Health Care Patient Management System (**Mentcare**) heard as *"meant care"*. |
| **`[19:00 (Verified via slide_012)]`** | `slide_012.png`<br>Deck Page 10: User & System Reqs | "...and **increase** user's password to ensure security..." | `increase` (0.23) | **"encrypt"** (*"encrypt user's password"*) | **Severe Phonetic Misrecognition:** Speaker said *"encrypt"*, transcribed as *"increase"*. Verified from cybersecurity and password storage context on Slide 10. |
| **`[20:01 (Verified via slide_012)]`** | `slide_012.png`<br>Deck Page 10: User & System Reqs | "...ensure user's session management **shooting login**..." | `shooting` (0.01), `login.` (0.00) | **"during login"** | Accent slur on *"during login"* heard as *"shooting login"*. |
| **`[20:46 (Verified via slide_012)]`** | `slide_012.png`<br>Deck Page 10: User & System Reqs | "...third **party** payment provided..." | `party` (0.03) | **third-party payment provider** | Low-probability word capture on payment gateway integration discussion. |
| **`[23:54 (Verified via slide_013)]`** | `slide_013.png`<br>Deck Page 11: FR & NFR | "...like, say, **burst** on the performance..." | `burst` (0.30) | **"based"** (*"based on performance"*) | Accent inflection on *"based"* heard as *"burst"*. Slide 11 lists NFR performance constraints. |
| **`[25:03 (Verified via slide_014)]`** | `slide_014.png`<br>Deck Page 12: ATM FR | "...ATM system shall validate the **feed number** entered by the user..." | `feed` (0.37) | **PIN number** (*"validate the PIN number"*) | **Severe Technical Misrecognition:** Slide 12 bullet 2 reads: *"The ATM system shall validate the PIN number entered by the user"*. Whisper misrecognized *"PIN"* as *"feed"*. |
| **`[27:30 (Verified via slide_015)]`** | `slide_015.png`<br>Deck Page 14 | "The **text stock**, usually that's the user's requirement..." | `stock,` (0.17) | **tech stack** (*technology stack*) | Colloquial pronunciation of "tech stack" transcribed as "text stock". |
| **`[30:26 (Verified via slide_017)]`** | `slide_017.png`<br>Deck Page 16: Elicitation | "...requirement **priorityization** and negotiation..." | `priorityization` (0.19) | **prioritization** | Slide 16 box: *"Requirements prioritization and negotiation"*. |
| **`[36:42 (Verified via slide_021)]`** | `slide_021.png`<br>Deck Page 18: Techniques | "...use of the system as **serious** of interaction..." | `serious` (0.30) | **"series of interactions"** | **Homophone Misrecognition:** Slide 18 Scenario bullet: *"System described as a series of interactions"*. |
| **`[45:15 (Verified via slide_026)]`** | `slide_026.png`<br>Deck Page 19: Scenario Design | "...if you're applying **rup** so we are using use case..." | `excuse` (0.05) | **RUP (Rational Unified Process)** | Verified: Methodology comparison between RUP and Agile. |
| **`[47:21 (Verified via slide_027)]`** | `slide_027.png`<br>Deck Page 20: Scenario Example | "...say maybe it or say cost uh **pos** no system..." | `pos` (0.44), `cost` (0.26) | **POS (Point of Sale)** | Verified acronym: Retail Point of Sale (POS) system on Slide 20. |
| **`[51:37 (Verified via slide_030)]`** | `slide_030.png`<br>Deck Page 23: UML | "**uml** diagram no unified modeling language..." | `uml` (0.15) | **UML (Unified Modeling Language)** | Acronym captured in lowercase. |
| **`[56:49 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Use Case | "...the **skeleton band** so this is we identified the role..." | `band` (0.42) | **"stick figure"** | **Severe Acoustic Distortion:** Lecturer pointed to the actor notation, describing the *"stick figure"*, which Whisper heard as *"skeleton band"*. Slide 26 diagram shows the standard stick figure actor. |
| **`[57:08 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Use Case | "...and then **cash the flannish** or in terms of the ATM..." | `cash` (0.27) | **"Cash Replenisher"** | **Phonetic Garble:** On Slide 26, the secondary actor is explicitly labeled **"Cash Replenisher"**. Whisper transcribed *"cash the flannish"*. |
| **`[57:33 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Use Case | "...combinations of a **verb and a noun**..." | `verb` (0.06), `withdraw` (0.13) | Verb + Noun naming convention | Verified against Slide 26 examples: *Withdraw Cash*, *Check Balance*. |
| **`[59:35 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Use Case | "...take note two words **bur and now**..." | `take` (0.06), `bur` (0.17) | **"verb and noun"** | Second phonetic clipping of *"verb and noun"*. |
| **`[62:12 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Use Case | "...let's say you have the **crud** no or view..." | `crud` (0.52), `update` (0.18) | **CRUD (Create, Read, Update, Delete)** | Verified standard software engineering data operations. |
| **`[65:08 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Banking Case | "...so I am a **shin hand** bank account holder..." | `shin` (0.14), `hand` (0.16) | **Shinhan Bank** | **Proper Noun Misrecognition:** Major international bank operating in Vietnam (**Shinhan Bank**), transcribed as *"shin hand"*. |
| **`[65:25 (Verified via slide_032)]`** | `slide_032.png`<br>Deck Page 26: Banking Case | "**bitcom bank** and shin hand are partners..." | `bitcom` (0.21) | **Vietcombank** | **Proper Noun Misrecognition:** The primary Vietnamese state-owned commercial bank (**Vietcombank**) heard phonetically as *"bitcom bank"*. |
| **`[70:17 (Verified via slide_038)]`** | `slide_038.png`<br>Deck Page 31: UC Example | "...the systems **valid data** customers detail..." | `valid` (0.32), `etc` (0.21) | **validates customer's details** | Transcription grammatical error; Slide 31 Step 3 reads: *"System validates customer's details"*. |
| **`[73:46 (Verified via slide_048)]`** | `slide_048.png`<br>Deck Page 34: INVEST | "...it will go with this what we call **invests** no..." | `invests` (0.54) | **INVEST matrix** | Verified: Agile quality criteria on Slide 34 (*Independent, Negotiable, Valuable, Estimable, Small, Testable*). |
| **`[76:59 (Verified via slide_059)]`** | `slide_059.png`<br>Deck Page 36: Comparison | "...ML diagram actors **obels** and system..." | `actors` (0.18), `obels` (0.26) | **"ovals"** (*"UML diagram actors, ovals, and system"*)| **Acoustic Misrecognition:** Lecturer pronounced *"ovals"* (the UML symbol for use cases), misrecognized as *"obels"*. Slide 36 lists UML diagram symbols. |
| **`[81:12 (Verified via slide_067)]`** | `slide_067.png`<br>Screen Share (StarUML) | "...in this **star you ml** I can select any diagrams..." | `you` (0.04), `yeah` (0.11) | **StarUML** | **Software Application Misrecognition:** The commercial modeling tool **StarUML** was split into *"star you ml"*. Visual frame `slide_067.png` shows the StarUML window. |

---

## 4. Ambiguity Log (Strict Zero-Guessing Rule Applied)

In compliance with Rule 3 of the Audit Protocol, spoken utterances that remain garbled, fragmented, or structurally incomplete even after cross-referencing against the active slide and video keyframe are logged without speculative interpretation:

| Timestamp | Raw Transcribed Text | Active Keyframe Snapshot | Deck Match | Ambiguity Analysis & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **`[AMBIGUOUS @ 03:32 – 03:40]`** | *"occurring. We'll say what is already existing. So in this requirement, so..."* | `slide_004.png` | Deck Page 3 | **Broken Sentence Fragment:** The speaker began contrasting brownfield systems with new development, but abandoned the clause midway through filler words before jumping to slide 4. |
| **`[AMBIGUOUS @ 49:06 – 49:15]`** | *"very how how old was that it's not easy because this is the the since this is going to be the..."* | `slide_029.png` | Deck Page 22 | **Grammatical Stumble / Train of Thought Breakdown:** Lecturer attempted to emphasize why requirements gathering is demanding, but stumbled over repeated words (*"how how old was that"*) without finishing the thought. |
| **`[AMBIGUOUS @ 68:39 – 68:45]`** | *"oh how many how many..."* | `slide_032.png` | Deck Page 26 | **Fragmented Musing:** The instructor paused while reviewing the chat window, muttering disjointed words before transitioning to the Use Case Specification slide. |
| **`[AMBIGUOUS @ 75:21 – 75:28]`** | *"the user stories will be tested so this is how no how you go into..."* | `slide_048.png` | Deck Page 34 | **Truncated Clause:** Speaker started explaining the "Testable" attribute of the INVEST matrix, but trailed off into conversational filler without completing the sentence. |
| **`[AMBIGUOUS @ 77:48 – 77:55]`** | *"uh technically uh experienced or knowledgeable no so it may it you might have a lack of um..."* | `slide_059.png` | Deck Page 36 | **Unfinished Proposition:** Instructor discussed developer skill prerequisites for formal UML use cases, but paused and trailed off without naming what is lacked. |
| **`[AMBIGUOUS @ 84:43 – 84:50]`** | *"uh why the discussion board is not here I think I post it here you only have..."* | `slide_070.png` | Canvas Screen Share | **Navigation Mumble:** Instructor searched through Canvas modules looking for a discussion thread while muttering off-mic. No technical content delivered. |
| **`[AMBIGUOUS @ 89:52 – 89:54]`** | Single word `"you"` transcribed during closing audio silence. | `slide_078.png` | Post-lecture screen | **Acoustic Silence Hallucination:** Background ambient noise after lecture conclusion was hallucinated as single token `"you"`. Zero instructional speech present. |

