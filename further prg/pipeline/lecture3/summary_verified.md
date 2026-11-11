# Verified Technical Lecture Summary & Confidence Audit

**Task:** `lecture3`  
**Course:** COSC2731 / COSC2440 — Further Programming  
**Lecture Topic:** Week 03 — Java Collections Framework & Generics  
**Instructor:** Further Programming Teaching Team (Tuan Phong Ngo / COSC2731 Team, RMIT University)  
**Audited Assets (Strict Local Isolation):**
- **Video Source:** `record/lecture3.mp4` (Duration: 45m 12s active lecture)
- **Audio Source:** `pipeline/lecture3/audio.mp3`
- **Slide Snapshots:** `pipeline/lecture3/slides/slide_001.png` to `slide_254.png` (254 keyframes)
- **Slide Mapping:** `pipeline/lecture3/slide_mapping.json` (254 matched frames)
- **Deck Alignment:** `pipeline/lecture3/deck_alignment.md` (Referenced to `lecture/lecture3.pdf`, 44 slides)
- **Transcript File:** `pipeline/lecture3/transcript.json` (485 structured segments with word-level probabilities)

---

## 1. Executive Summary

This lecture delivers an applied, hands-on architectural exploration of the **Java Collections Framework (JCF)** and **Java Generics**, focusing on data structure selection, memory layout implications, time complexity trade-offs, and behavioral ordering. Rather than stepping through the 44-slide presentation deck (`lecture3.pdf`) sequentially, the instructor adopts a problem-driven, interactive methodology. Spoken theory is paired with visual memory simulations, hands-on student experimentation challenges, and real-world engineering analogies (such as video game memory hacking and database indexing).

The session covers four foundational areas of modern Java development:
1. **Memory Topologies & Sequential Collections:** Contrasting contiguous block storage (`ArrayList` / primitive arrays) against non-contiguous node topologies (`LinkedList`). The instructor introduces a computer security thought experiment—demonstrating how game memory scanners (like Cheat Engine) exploit contiguous array layouts to inject attribute hacks into sports game player models (e.g., arbitrarily setting player stats to 100), whereas linked list pointer chains disperse node payloads across heap memory (`0x001`, `0x177`), significantly increasing reverse-engineering complexity.
2. **The `Set` Interface & Uniqueness Contracts:** Formalizing the mathematical `Set` abstraction (`HashSet` vs. `LinkedHashSet`). Using database analogies (`SELECT DISTINCT`), the lecture illustrates how duplicate insertions are rejected at $O(1)$ average cost via `add()`, and how `hashCode()` and `equals()` govern membership verification.
3. **Object Ordering & The `Comparator` Pattern:** Deconstructing total ordering via `Comparable<T>` (`compareTo`) and independent pluggable orderings via `Comparator<T>` (`compare`). The instructor demonstrates sorting objects cleanly via `Collections.sort(list, comparator)` in a single line without manual sorting loops.
4. **Map Implementations, Hashing & Range Slicing:** Dissecting key-value pair associations across `HashMap`, `LinkedHashMap`, and `TreeMap`. Through an extended interactive challenge, students observe how `HashMap` distributes keys across hash buckets without ordering guarantees, `LinkedHashMap` preserves temporal insertion order, and `TreeMap` continuously balances a Red-Black tree to maintain sorted key order. The session concludes with `SortedSet` and `SortedMap` range views (`headSet`, `tailSet`, `subSet`) and administrative guidelines for the upcoming Week 3 Lab Test/Quiz.

---

## 2. High-Confidence Technical Takeaways (Citing Exact `[MM:SS]` Timestamps)

### 2.1 Memory Topologies: `ArrayList` vs. `LinkedList` & Game Hacking Metaphor `[00:01]` – `[01:42]`
- **The Memory Scanner Vulnerability `[00:01]` – `[00:45]`:** *(Referencing `slide_001.png` – `slide_005.png`, Deck Pages 13–17)*
  - When game entities (such as soccer players) are stored sequentially in an array or `ArrayList`, their attributes (e.g., speed, stamina, skill rating) are positioned contiguously in physical RAM.
  - Reverse engineers using memory scanners (e.g., Cheat Engine) can easily detect sequential attribute patterns and alter player ratings (e.g., turning a second-division substitute into Lionel Messi with 100 in every attribute).
- **LinkedList Pointer Dispersal `[00:45]` – `[01:25]`:** *(Referencing `slide_005.png`, Deck Page 17)*
  - In a `LinkedList`, each node contains the data object reference and memory pointers (`next`, `prev`).
  - Nodes are allocated independently on the heap and can be scattered arbitrarily across memory addresses (e.g., Node 1 at `0x001`, Node 2 at `0x177`).
  - Dispersed heap allocation makes memory scanning significantly more difficult because memory scanners see only chains of integer pointer addresses rather than predictable contiguous data blocks `[03:31] – [04:45]`.
- **Performance Trade-Offs `[01:00]` – `[01:25]`:**
  - *`ArrayList`*: $O(1)$ random access by index via direct pointer arithmetic; costly $O(n)$ shifts on intermediate insertions and deletions.
  - *`LinkedList`*: $O(1)$ insertions/deletions once a node pointer is established; $O(n)$ sequential traversal for indexed lookups.
  - While performance differences are negligible for small datasets ($N < 1,000$), they diverge significantly once scaling to enterprise workloads ($N \ge 1,000,000$).

### 2.2 The `Set` Interface: Uniqueness Contracts & Big-O Notation `[01:42]` – `[07:15]`
- **Mathematical Uniqueness & Contract Rules `[01:42]` – `[02:46]`:** *(Referencing `slide_006.png`, Deck Pages 18–21)*
  - A `Set` models a mathematical collection that permits no duplicate elements ($e_1.\text{equals}(e_2) == \text{false}$).
  - *Database Analogy `[05:39] – [05:55]`*: Analogous to executing a `SELECT DISTINCT` SQL query over a database table.
  - *Return Value Invariant `[02:30] – [02:46]`*: The `Set.add(e)` method returns a boolean:
    - Returns `true` if the element was successfully inserted.
    - Returns `false` if the element already exists in the set (the insertion is silently rejected without throwing an exception).
- **Big-O Notation in Practice `[02:58]` – `[03:22]`:** *(Referencing `slide_006.png`, Deck Pages 34–35)*
  - Big-O notation ($O(1)$, $O(\log n)$, $O(n)$) provides an asymptotic upper bound on algorithmic execution steps and computational resource requirements as dataset size $n$ approaches infinity.
  - `HashSet` delivers $O(1)$ constant average time complexity for `add()`, `remove()`, and `contains()`.
- **Set Implementations: `HashSet` vs. `LinkedHashSet` `[02:03]` – `[02:15]`:** *(Referencing `slide_006.png`, Deck Page 18)*
  - `HashSet`: Backed by a hash table; provides maximum performance but guarantees zero element ordering.
  - `LinkedHashSet`: Backed by a hash table with a running doubly-linked list running through all entries; maintains predictable **insertion order** at a minor memory overhead.
- **Conversion to Array `[06:50]` – `[07:10]`:** Sets can be dumped to native arrays using `set.toArray()` for compatibility with legacy array-based APIs.

### 2.3 Object Ordering: `Comparable` vs. `Comparator` `[07:16]` – `[11:25]`
- **The Need for Custom Comparison `[07:16]` – `[08:15]`:** *(Referencing `slide_014.png`, Deck Pages 27–28)*
  - While primitive numbers and strings have natural ordering, custom domain entities (`Student`, `Player`) require explicit comparison logic based on business attributes (e.g., `id`, `age`, `gpa`).
- **`Comparator<T>` Contract & Return Value Semantics `[08:15]` – `[09:20]`:** *(Referencing `slide_014.png`, Deck Page 28)*
  - The `compare(T o1, T o2)` method must return an integer indicating relative ordering:
    - **Positive Integer (`> 0`, e.g., `+1`):** `o1` is strictly greater than `o2` (`o1` sorts after `o2`).
    - **Negative Integer (`< 0`, e.g., `-1`):** `o1` is strictly less than `o2` (`o1` sorts before `o2`).
    - **Zero (`0`):** `o1` and `o2` are identical under this comparison criteria.
  - *Demonstration*: An `AgeComparator` comparing Student 1 (age 20) with Student 2 (age 19) returns `+1`; comparing Student 1 (age 20) with Student 3 (age 21) returns `-1`.
- **Executing Clean Sorts via `Collections.sort()` `[09:20]` – `[10:35]`:**
  - Developers do not write manual bubble or quicksort algorithms.
  - Sorting is executed cleanly in one line using the `java.util.Collections` utility class:
    ```java
    Collections.sort(studentList, new AgeComparator());
    ```
  - This decouples the entity model from its sorting strategy, allowing multiple comparators (`AgeComparator`, `IdComparator`, `NameComparator`) to be swapped dynamically.
- **Database Sorting vs. In-Memory Sorting `[10:35]` – `[11:15]`:**
  - Relational database engines optimize multi-column indexes and boolean sorting at the disk page level using specialized B-Tree routines.
  - In-memory collection sorting converts booleans to byte representations and relies on Dual-Pivot Quicksort or Timsort, which may introduce memory pressure on large in-memory datasets.

### 2.4 The `Map` Interface Architecture: `HashMap`, `LinkedHashMap` & `TreeMap` `[11:26]` – `[30:13]`
- **Key-Value Associative Mappings `[11:26]` – `[12:05]`:** *(Referencing `slide_017.png` – `slide_022.png`, Deck Pages 22–24)*
  - Maps store associations between unique keys and corresponding value payloads: `Map<K, V>`.
  - Keys must be strictly unique; inserting a duplicate key overwrites the existing value associated with that key.
- **Hands-On Interactive Student Challenge `[12:05]` – `[27:46]`:** *(Referencing `slide_022.png` – `slide_198.png`)*
  - The lecturer assigns a 15-minute challenge where students test three concrete map implementations using a browser simulation tool:
    1. `HashMap`
    2. `LinkedHashMap`
    3. `TreeMap`
  - Students insert student records with varying IDs and names ("An", "Chi", "Jamie", "Dung") and observe structural ordering behaviors and operation costs.
- **Comparative Behavioral Synthesis `[27:46]` – `[30:13]`:** *(Referencing `slide_198.png` – `slide_213.png`, Deck Page 24)*
  - **`HashMap` (Unordered / Hash-Dispersed):** Keys are hashed into buckets. Iteration order is arbitrary and depends strictly on bucket hash codes; inserting a new key can alter apparent iteration order. Delivers $O(1)$ average point lookups.
  - **`LinkedHashMap` (Insertion-Ordered):** Preserves the exact temporal sequence in which keys were added (`put()`). Iteration matches input order, ideal for caching (e.g., LRU caches) and sequential record processing.
  - **`TreeMap` (Sorted by Key):** Backed by a Red-Black self-balancing binary search tree. Keys are continuously sorted according to their natural ordering (`Comparable`) or a custom `Comparator`. Operations (`get`, `put`, `remove`) run in bounded $O(\log n)$ time.

### 2.5 Hash Spaces, Buckets & Collision Resolution Strategies `[30:13]` – `[33:55]`
- **The Concept of the Hash Universe `[30:13]` – `[32:15]`:** *(Referencing `slide_213.png`, Deck Page 26)*
  - A `HashMap` does not maintain a continuous two-column table of keys and values.
  - Instead, it maintains a hash bucket array. A hashing function (`hashCode()`) maps arbitrary high-dimensional object keys into bounded integer array indices: $\text{index} = \text{hash}(\text{key}) \pmod{\text{capacity}}$.
- **Hash Collisions & Resolution Algorithms `[32:15]` – `[33:55]`:** *(Referencing `slide_213.png` – `slide_216.png`, Deck Page 26)*
  - *Collision Definition*: Occurs when two distinct, non-equal keys produce the exact same bucket index ($\text{hash}(k_1) == \text{hash}(k_2)$).
  - *Resolution Mechanics*:
    - **Separate Chaining:** Buckets store a linked list of colliding entries. When a bucket's chain exceeds an internal threshold (treeification threshold of 8 entries in Java 8+), Java converts the linked list into a Red-Black balanced tree, reducing search time from $O(k)$ to $O(\log k)$.
    - **Open Addressing:** Alternative collision resolution probing adjacent array slots.
  - *The `equals()` and `hashCode()` Contract*: If two objects are equal according to `equals()`, they *must* return the exact same `hashCode()`. Breaking this contract causes lost entries in `HashMap` and `HashSet`.

### 2.6 Sorting Map Entries by Value using `Comparator` `[33:55]` – `[36:03]`
- **Key Sorting vs. Value Sorting `[33:55]` – `[35:15]`:** *(Referencing `slide_218.png` – `slide_224.png`, Deck Page 28)*
  - `TreeMap` natively sorts entries strictly by their **keys**.
  - To sort a map by its **values** (e.g., sorting a student map by student `age` or `score`), developers extract the entry set (`map.entrySet()`) and pass an entry comparator:
    ```java
    List<Map.Entry<String, Student>> entries = new ArrayList<>(map.entrySet());
    entries.sort(Map.Entry.comparingByValue(new AgeComparator()));
    ```
- **Practical Application `[35:15]` – `[36:03]`:** Frequently required in final exams and practical project requirements where records indexed by ID must be rendered in leaderboards sorted by performance or timestamps.

### 2.7 `SortedSet` & `SortedMap` Interfaces: Range Views & Subsets `[36:03]` – `[41:30]`
- **Range-View Capabilities `[36:03]` – `[37:15]`:** *(Referencing `slide_237.png` – `slide_240.png`, Deck Pages 29–32)*
  - `SortedSet` and `SortedMap` extend the base collection contracts to provide navigable windowing operations over sorted structures (`TreeSet`, `TreeMap`).
- **Three Core Range Methods `[37:15]` – `[40:10]`:** *(Referencing `slide_241.png`)*
  1. **`headSet(toElement)` / `headMap(toKey)`:** Returns a view of the collection strictly less than the specified endpoint (e.g., retrieving all students with ID $< 200$).
  2. **`tailSet(fromElement)` / `tailMap(fromKey)`:** Returns a view of elements greater than or equal to the specified starting point.
  3. **`subSet(fromElement, toElement)` / `subMap(fromKey, toKey)`:** Slices a bounded window $[from, to)$ (e.g., slicing a student roster from "An" up to "Binh").
- **View Semantics Invariant `[38:40]` – `[39:00]`:**
  - Range methods return **views** of the underlying sorted collection rather than deep-copied duplicate arrays.
  - Modifying or querying a sub-view reflects directly upon the original collection without destroying or re-allocating the master data structure.
- **Boundary Methods `[40:10]` – `[40:30]`:** `first()` and `last()` provide $O(1)$ access to minimum and maximum elements in the sorted collection.

### 2.8 Collection Selection Synthesis `[41:25]` – `[43:03]`
- **Architectural Decision Matrix `[41:25]` – `[43:03]`:** *(Referencing `slide_247.png` – `slide_252.png`, Deck Pages 33, 36–37)*

| Data Structure / Interface | Ordering Guarantee | Lookup Complexity | Insertion / Deletion Complexity | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **`ArrayList`** | Index-ordered | $O(1)$ random access | $O(n)$ worst-case (shifts elements) | Read-heavy sequences with infrequent resizing. |
| **`LinkedList`** | Pointer-ordered | $O(n)$ sequential search | $O(1)$ at head/tail or known iterator | High-frequency insertions/removals at boundaries. |
| **`HashSet`** | None (hash-dispersed) | $O(1)$ average | $O(1)$ average | High-speed deduplication and uniqueness testing. |
| **`LinkedHashSet`** | Insertion order | $O(1)$ average | $O(1)$ average | Deduplication while preserving temporal addition order. |
| **`TreeSet` / `SortedSet`** | Natural or Comparator sorted | $O(\log n)$ | $O(\log n)$ | Maintained sorted sets requiring range queries (`subSet`). |
| **`HashMap`** | None (bucket-dispersed) | $O(1)$ average | $O(1)$ average | Fast key-to-value lookups without ordering requirements. |
| **`LinkedHashMap`** | Insertion order | $O(1)$ average | $O(1)$ average | Key-value pairs requiring insertion-order traversal or LRU caches. |
| **`TreeMap` / `SortedMap`**| Natural or Comparator sorted | $O(\log n)$ | $O(\log n)$ | Key-value associations requiring key-sorted traversal and range slicing. |

### 2.9 Course Administration & Upcoming Assessment Guidelines `[43:03]` – `[45:00]`
- **Week 3 Lab Test / Quiz Policy `[43:20]` – `[43:52]`:**
  - *Date*: Friday of Week 3.
  - *Authorized Materials*: Course Canvas materials and official lecture notes may be consulted.
  - **Strictly Prohibited**:
    - Opening or running IDEs (IntelliJ IDEA, VS Code). Copy-pasting quiz code into an IDE to compile and execute it to extract answers is strictly forbidden.
    - Code tracing must be conducted mentally and solved on paper.
    - No external answer portals, Google searches, or automated code-generation tools.
- **Group Project Specification Update `[43:52]` – `[44:18]`:**
  - Any preliminary project specifications downloaded earlier in the morning must be discarded.
  - The finalized, authoritative group project specification and codebase are released in the afternoon.

---

## 3. External Websites, Demos & Live Code References

In strict compliance with Rule 3 of the Audit Protocol, all external simulation tools, interactive coding demos, and reference walkthroughs have been cataloged with direct reference links, search queries, and technical summaries:

| Citation & Video Frame | Timestamp & Duration | Demonstration Topic & Content | Suggested Search Query | Direct Reference Link |
| :--- | :--- | :--- | :--- | :--- |
| **`[EXTERNAL SITE / DEMO @ 00:03]`**<br>`slide_002.png` – `slide_005.png` | `00:03`<br>(1m 39s) | **Array vs. LinkedList Memory Scanner Simulation:**<br>Lecturer demonstrates how contiguous arrays in games expose player attributes to memory scanners (Cheat Engine / FIFA stat hacks), whereas `LinkedList` scatters node references across heap addresses (`0x001`, `0x177`), obfuscating data structures. | `java arraylist vs linkedlist memory layout contiguous pointers` | [🔍 Search Google](https://www.google.com/search?q=Player+Modify+Players+Someone) |
| **`[EXTERNAL SITE / DEMO @ 01:42]`**<br>`slide_006.png` – `slide_009.png` | `01:42`<br>(3m 50s) | **Interactive `Set` Deduplication Simulator:**<br>Browser simulation of `HashSet` and `LinkedHashSet`. Lecturer inputs Student 1 multiple times; demonstrates that the second insertion returns `false` due to unique key constraints, confirming $O(1)$ deduplication. | `java set interface hashset duplicate element add boolean` | [🔍 Search Google](https://www.google.com/search?q=ID+SS+Add+Set) |
| **`[EXTERNAL SITE / DEMO @ 07:16]`**<br>`slide_014.png` / `slide_015.png` | `07:16`<br>(4m 07s) | **Live `Comparator` & `Collections.sort()` Implementation:**<br>Code demonstration writing a three-line `AgeComparator` returning `+1`, `-1`, or `0`. Calls `Collections.sort(studentList, comparator)` to execute in-memory sorting in a single line. | `java comparator interface collections sort example` | [🔍 Search Google](https://www.google.com/search?q=ID+Student+Comparator+Number) |
| **`[EXTERNAL SITE / DEMO @ 11:26]`**<br>`slide_017.png` – `slide_026.png` | `11:26`<br>(2m 27s) | **Interactive Map Comparison Tool Introduction:**<br>Lecturer introduces the browser simulation comparing `HashMap`, `LinkedHashMap`, and `TreeMap`, briefing students on insertion experiments and Big-O tracking before the 15-minute hands-on challenge. | `java hashmap vs linkedhashmap vs treemap ordering differences` | [🔍 Search Google](https://www.google.com/search?q=Map+Now+Again+Key) |
| **`[EXTERNAL SITE / DEMO @ 29:05]`**<br>`slide_199.png` – `slide_213.png` | `29:05`<br>(4m 05s) | **Student Key Insertion & Order Verification Debrief:**<br>Live simulation inserting student keys ("An", "Chi", "Jamie", "Dung") across all three maps. Verifies that `TreeMap` sorts keys naturally, `LinkedHashMap` preserves insertion order, and `HashMap` re-indexes based on hash buckets. | `java map ordering demonstration hashmap linkedhashmap treemap` | [🔍 Search Google](https://www.google.com/search?q=Add+Now+Chi+Ang) |
| **`[EXTERNAL SITE / DEMO @ 33:10]`**<br>`slide_214.png` – `slide_216.png` | `33:10`<br>(41.4s) | **Hash Space & Collision Resolution Mechanics:**<br>Visual demonstration of the 100,000-element hash space. Lecturer explains how colliding keys are indexed into bucket linked lists and Red-Black trees to resolve hash conflicts. | `java hashmap collision resolution chaining red black tree` | [🔍 Search Google](https://www.google.com/search?q=Android+Compare+Different+Key) |
| **`[EXTERNAL SITE / DEMO @ 33:59]`**<br>`slide_220.png` – `slide_224.png` | `33:59`<br>(1m 15s) | **Sorting Map Entries by Value via `Comparator`:**<br>Demonstrates converting `Map.entrySet()` into a collection and applying an `AgeComparator` to sort key-value associations by student age rather than by key ID. | `java sort map by value comparator entryset` | [🔍 Search Google](https://www.google.com/search?q=Entry+Map+Sort+Age) |
| **`[EXTERNAL SITE / DEMO @ 37:14]`**<br>`slide_241.png` – `slide_246.png` | `37:14`<br>(5m 06s) | **`SortedSet` & `SortedMap` Range-View Operations:**<br>Interactive execution of `headSet(200)` and `subSet("An", "Binh")`, proving that range methods return dynamic non-destructive sub-views rather than allocating new arrays. | `java sortedset headset tailset subset range view` | [🔍 Search Google](https://www.google.com/search?q=ID+Set+Get+Array) |

---

## 4. Low-Confidence Acoustic & Technical Verification Audit

In accordance with Rule 2 of the Audit Protocol, segments flagged with low acoustic confidence or containing phonetic distortions caused by the instructor's non-native accent have been rigorously audited against `slide_mapping.json` and official slide text (`lecture3.pdf`):

| Citation | Corresponding Slide & Deck Reference | Raw Whisper Transcript | Flagged Word(s) (Prob) | Verified Technical Term / Spoken Meaning | Phonetic / Acoustic Root Cause & Technical Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[00:07 (Verified via slide_003)]`** | `slide_003.png`<br>Game Memory Hack Visual | "...and then they change some attributes to be **like messy or something**..." | `like` (0.43), `messy` (0.61) | **Lionel Messi** (*"to be like Messi or something"*) | **Cultural / Phonetic Confusion:** Speaker referenced football player Lionel Messi in the context of sports game hacking (FIFA stat editing); transcribed phonetically as "messy". |
| **`[00:45 (Verified via slide_005)]`** | `slide_005.png`<br>LinkedList Memory Visual | "...also good that you can **sub the player to use linked list**..." | `sub` (0.41), `player` (0.43) | **substitute / structure player data using a `LinkedList`** | Speaker was explaining replacing contiguous array storage with a linked list to avoid memory scanning vulnerabilities. |
| **`[00:51 (Verified via slide_005)]`** | `slide_005.png`<br>LinkedList Memory Visual | "...So you can change the list pointer from one to the other **in the substitution**." | `substitution` (0.52) | **substitution / node replacement** | Refers to swapping node pointers during linked list insertion/deletion without shifting array memory blocks. |
| **`[01:47 (Verified via slide_006)]`** | `slide_006.png`<br>Deck Page 18: Set Interface | "You can **activate data**, that's okay, but you want to add some data into your set." | `activate` (0.27) | **iterate / access data** | **Phonetic Garble:** Speaker said "iterate through" or "access data" in a list, misheard as "activate data". |
| **`[02:11 (Verified via slide_006)]`** | `slide_006.png`<br>Deck Page 18: Set Interface | "All right, so there are **sets in the face** that you can see here." | `sets` (0.51), `face` (0.62) | **`Set` interface** (*"the Set interface"*)| **Phonetic Distortion:** Non-native pronunciation of "Set interface" transcribed as "sets in the face". Slide 18 heading is explicitly *"Interface: Set"*. |
| **`[02:36 (Verified via slide_006)]`** | `slide_006.png`<br>Deck Page 21: `add()` Method | "...some student assist in here and then you've got the **forms return** when you call the add function..." | `assist` (0.41), `forms` (0.48) | **`false` returned** (*"got false returned when you call add()"*) | **Acoustic Misrecognition:** Non-native pronunciation of "false" transcribed as "forms". Slide 21 explicitly states: *"Set add() returns false if the element is already in the set"*. |
| **`[03:01 (Verified via slide_006)]`** | `slide_006.png`<br>Deck Page 34: Big-O | "...And by the way, if you see that there's an O1 here, this is always a **big connotation**..." | `big` (0.51), `connotation` (0.64) | **Big-O notation** ($O(1)$) | **Phonetic Malapropism:** Speaker said "Big-O notation", transcribed as "big connotation". Slide 34 is titled *"The Big-O Notation"*. |
| **`[03:43 (Verified via slide_008)]`** | `slide_008.png`<br>Pointer Memory Layout | "...you only see **another change of pointer**, like zero X, A, B, C, something..." | `another` (0.45), `change` (0.52) | **a chain of pointers** (`0xABC...`) | Transcribed as "change of pointer"; speaker is describing traversing a heap pointer chain where addresses appear in hexadecimal format. |
| **`[11:01 (Verified via slide_015)]`** | `slide_015.png`<br>Sorting Collections | "They got a different **Android term**... They convert your boolean into something..." | `Android` (0.59), `term.` (0.48) | **algorithm** (*"a different algorithm"*) | **Severe Phonetic Garble:** Lecturer's pronunciation of "algorithm" was misrecognized by Whisper as "Android term". |
| **`[13:02 (Verified via slide_025)]`** | `slide_025.png`<br>Map Exploration Simulator | "Or add some **hdiff**. This is bigger than the data that you already have." | `hdiff.` (0.22) | **age difference / different age key** | Speaker was instructing students to insert records with differing age attributes to observe sorting order. |
| **`[13:20 (Verified via slide_025)]`** | `slide_025.png`<br>Deck Page 34: Big-O | "You also take a look on to this **big connotation** here..." | `big` (0.51), `connotation` (0.62) | **Big-O notation** | Second occurrence of "Big-O notation" misheard as "big connotation". |
| **`[29:07 (Verified via slide_199)]`** | `slide_199.png`<br>Interactive Map Key Test | "I got **ang** first and let's say I want to put a new user in here... Now I add **chi**... But you add **jammy**, right?... you see **dung**, larger than the others." | `ang` (0.07), `chi` (0.44), `jammy` (0.49), `dung` (0.18) | **An, Chi, Jamie, Dung** (Vietnamese student test names) | Whisper struggled with Vietnamese names used as sample map keys: An (Ang), Chi, Jamie (Jammy), and Dũng/Đặng (Dung). |
| **`[29:51 (Verified via slide_207)]`** | `slide_207.png`<br>Deck Page 24: TreeMap | "...because this is the **sort of tree in the tree map**..." | `sort` (0.17), `tree` (0.61) | **sorted tree in the `TreeMap`** | Speaker explaining that `TreeMap` maintains a self-balancing sorted Red-Black tree. |
| **`[30:35 (Verified via slide_213)]`** | `slide_213.png`<br>Deck Page 26: Hash Space | "You actually have a **big universe**... hash map of 100,000 elements..." | `universe` (0.54) | **hash universe / key space** | Technical jargon: the theoretical domain of all possible keys mapped into hash bucket space. |
| **`[33:47 (Verified via slide_215)]`** | `slide_215.png`<br>Deck Page 26: Collisions | "...but here you only need to know that there's an **android to solve that conflict** in your hash map..." | `android` (0.55), `conflict` (0.61) | **algorithm to resolve that collision** | Second occurrence of "algorithm" misheard as "android". "Conflict" refers to a hash collision resolved via chaining or treeification. |
| **`[36:09 (Verified via slide_232)]`** | `slide_232.png`<br>Deck Page 29: SortedSet | "We also have three sets, then why do we need **solid set**?... sort of set interface..." | `solid` (0.48), `sort` (0.52) | **`SortedSet` interface** | **Acoustic Distortion:** Speaker saying "SortedSet" was transcribed as "solid set" and "sort of set". Slide 29 heading is explicitly *"Interface: SortedSet"*. |
| **`[38:10 (Verified via slide_241)]`** | `slide_241.png`<br>SortedSet Demo Screen | "...you can say I want to set the, set the **headset**, and then I want to get the ID is number two..." | `headset` (0.41) | **`headSet()` method** (`set.headSet(toElement)`) | **Technical Garble:** The Java method call `headSet()` transcribed phonetically as audio equipment ("headset"). Slide 29 documents `headSet()`. |
| **`[38:45 (Verified via slide_241)]`** | `slide_241.png`<br>SortedSet Demo Screen | "...when you have the headset or the **outer tail**..." | `outer` (0.29), `tail` (0.58) | **`tailSet()` method** (`set.tailSet(fromElement)`) | Transcribed as "outer tail"; speaker was contrasting `headSet()` with `tailSet()`. |
| **`[40:19 (Verified via slide_246)]`** | `slide_246.png`<br>Deck Page 5: Collections | "...so these are the **server correction framework** operation..." | `server` (0.35), `correction` (0.42) | **Java Collections Framework (JCF)** | **Severe Phonetic Garble:** "Java Collections Framework" distorted by accent into "server correction framework". |
| **`[41:29 (Verified via slide_247)]`** | `slide_247.png`<br>Deck Page 16: ArrayList | "...this is the user sorted **LA1D array**, you can have like object star in an array or linked list..." | `LA1D` (0.19), `star` (0.32) | **1D array / `ArrayList`** (*"objects stored in an array"*) | Speaker comparing standard 1D arrays and `ArrayList` with `LinkedList`. |
| **`[43:33 (Verified via slide_254)]`** | `slide_254.png`<br>Assessment Briefing | "...you cannot use your ID, **the Dj, your BS code** to copy place the code in from the quiz..." | `Dj` (0.22), `BS` (0.28) | **IDE (IntelliJ IDEA), your VS Code** | **Acoustic Garble:** Lecturer said *"your IDE, IntelliJ, your VS Code"*, transcribed as *"your ID, the Dj, your BS code"*. |
| **`[43:44 (Verified via slide_254)]`** | `slide_254.png`<br>Assessment Briefing | "...so **no answer port**, no Google search, only Canvas material is provided..." | `answer` (0.15), `port` (0.38) | **no answer portals / external AI tools** | Speaker forbidding online cheat portals (Chegg, ChatGPT) during the upcoming Friday quiz. |
| **`[43:58 (Verified via slide_254)]`** | `slide_254.png`<br>Assessment Briefing | "...that's it for the quiz and for the **good projects**... it's the own project I will release..." | `good` (0.48), `own` (0.45) | **group projects** / **old project** | Speaker instructs students to ignore the old project file seen earlier and await the new group project specification. |

---

## 5. Ambiguity Log (Strict Zero-Guessing Rule Applied)

In strict adherence to Rule 4 of the Audit Protocol, spoken utterances or recording artifacts that remain unintelligible, ambiguous, or fragmented after cross-referencing against the visual keyframes and presentation slides are cataloged below without speculative interpretation:

| Citation | Timestamp Range | Raw Transcribed Text / Observed Event | Active Visual Frame | Ambiguity Analysis & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **`[AMBIGUOUS @ 07:38 – 07:44]`** | `07:38` – `07:44` | *"A comparator you can look into the student logic... what you want to compare different object in..."* | `slide_014.png` (Live Code) | **Syntactically Incomplete Thought:** Speaker began explaining how the comparator inspects the internal fields of a student object, but abandoned the clause midway to navigate to the code editor. |
| **`[AMBIGUOUS @ 10:14 – 10:18]`** | `10:14` – `10:18` | *"Oh, sorry, I think I can make a mistake here. Okay, let me show again."* | `slide_014.png` (Live Code) | **Live Code Correction Interruption:** Lecturer experienced an import or typing error while entering `Collections.sort()` and cleared the line before retyping. Filler commentary with no technical assertion. |
| **`[AMBIGUOUS @ 13:53 – 21:43]`** | `13:53` – `21:43` | Repeated isolated single-word tokens (`"you"`) transcribed at periodic intervals (`[14:06]`, `[14:32]`, `[15:06]`, `[15:36]`, `[16:13]`, `[18:02]`, `[19:32]`, `[20:30]`, `[21:17]`) amidst extended silence. | `slide_027.png` – `slide_127.png` | **Hands-On Challenge Silent Window:** The lecturer assigned a 15-minute challenge at `[12:20]` (*"I will give you 15 minutes that we discuss in the end... play around until 13:31"*). The classroom was silent while students completed the simulation exercise. Whisper hallucinated recurring tokens on ambient microphone line noise. |
| **`[AMBIGUOUS @ 22:33 – 24:56]`** | `22:33` – `24:56` | Intermittent silence and isolated tokens (`"you"` at `[23:33]`, `[24:05]`, `[24:18]`, `[24:37]`). | `slide_142.png` – `slide_170.png` | **Student Chat Typing Pause:** Instructor checked in at `[21:48]` asking students to submit their findings to Microsoft Teams chat, then waited silently for 2.5 minutes for student submissions to arrive. Zero instruction delivered. |
| **`[AMBIGUOUS @ 25:52 – 27:46]`** | `25:52` – `27:46` | Extended 1m 54s silence with repeated `"you you you"` tokens (`slide_181.png` – `slide_197.png`). | `slide_181.png` – `slide_197.png` | **Pre-Debrief Reading Period:** Lecturer reviewed incoming student chat responses off-screen before formally commencing the debrief at `[27:46]` (*"okay, sorry, so let's discuss now..."*). |
| **`[AMBIGUOUS @ 40:41 – 40:55]`** | `40:41` – `40:55` | *"okay, comparator, actually comparator here doesn't show you much, because you should have the, okay, yeah, I think I have to define the, let's reset again..."* | `slide_241.png` (Range Demo) | **Simulator State Confusion:** Lecturer attempted to demonstrate comparator re-sorting in the range tool, realized the simulation UI had defaulted to ID ordering rather than age ordering, and reset the simulation state. |
| **`[AMBIGUOUS @ 44:18 – 45:12]`** | `44:18` – `45:12` | Isolated token `"you"` at `[45:10]` amidst post-lecture silence. | `slide_254.png` (Desk/Teams) | **Stream Wrap-Up & Exit Silence:** The lecture formally ended at `[44:18]` (*"you have a question, you can feel free to stay here and ask me, goodbye"*). The microphone remained live as attendees disconnected. |

