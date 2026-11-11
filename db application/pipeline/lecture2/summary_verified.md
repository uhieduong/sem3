# Verified Technical Lecture Summary & Confidence Audit

**Task:** `lecture2`  
**Course:** ISYS2099 / ISYS3434 — Database Applications  
**Lecture Topic:** Week 02 — Database Indexing  
**Instructor:** Tom Huynh (School of Science, Engineering & Technology, RMIT University Vietnam)  
**Audited Assets (Strict Local Isolation):**
- **Video Source:** `record/lecture2.mp4` (Duration: 81m 49s)
- **Audio Source:** `pipeline/lecture2/audio.mp3`
- **Slide Snapshots:** `pipeline/lecture2/slides/slide_001.png` to `slide_166.png` (166 keyframes)
- **Slide Mapping:** `pipeline/lecture2/slide_mapping.json` (166 matched keyframes)
- **Deck Alignment:** `pipeline/lecture2/deck_alignment.md` (Referenced to `lecture/lecture2.pdf`, 58 slides)
- **Transcript File:** `pipeline/lecture2/transcript.json` (1,843 structured segments with word-level probabilities)

---

## 1. Executive Summary

This lecture delivers a deep architectural and mathematical treatment of **Database Indexing** within relational database management systems, using MySQL and the InnoDB engine as concrete reference implementations. The instructor, Tom Huynh, establishes from the outset that in modern data-intensive systems, overall query latency is overwhelmingly dominated by disk I/O. As datasets scale into millions of rows, full table scans become completely intractable; indexing serves as the fundamental mechanism to avoid exhaustive scans by transforming linear block traversals into logarithmic disk seeks.

The session systematically explores the physical and logical storage models of MySQL—contrasting storage engines (InnoDB, MyISAM, Memory, CSV), dissecting InnoDB's storage hierarchy (Tablespaces, Segments, Extents, 16 KB Pages, and 4 KB OS Blocks), and establishing the core performance metrics governing multi-tier web database applications: **Throughput**, **Execution Time**, **Concurrency**, and **Utilization**. Through the "Coffee Shop" thought experiment, the lecture formalizes how latency decomposes into waiting time and execution time, explaining why high-throughput systems degrade exponentially once resource utilization nears 100%.

The core of the lecture mathematically models and compares indexing data structures:
1. **Primary Indexes (Sparse):** One entry per physical block on sorted files, reducing block accesses via binary search.
2. **Secondary Indexes (Dense):** One entry per logical record on non-ordering attributes, requiring binary search over the index followed by pointer dereferencing.
3. **Multi-level Indexes & $B^+$-Trees:** Hierarchical balanced search trees that bound tree height to 3–4 levels even for millions of records, while linking leaf nodes sequentially for high-performance range scans.
4. **Composite Indexes:** Enforcing the strict **leftmost-prefix rule**, requiring equality conditions to precede range conditions.
5. **Hash Indexes:** Achieving $O(1)$ point lookups at the expense of ordering and range capabilities.

Finally, the lecture presents practical engineering guidelines for index creation, index inspection via MySQL's `EXPLAIN` utility, index maintenance overhead during data modifications (`INSERT`, `UPDATE`, `DELETE`), index selectivity thresholds (explaining why a full table scan outperforms an index scan when selectivity exceeds 15–20%), and introduces the hands-on 100,000-row `products` tutorial benchmark.

---

## 2. High-Confidence Technical Takeaways (Citing Exact `[MM:SS]` Timestamps)

### 2.1 Course Coordination & Lecture Agenda `[00:33]` – `[04:45]`
- **The Data Scale Reality `[01:17]` – `[02:43]`:** Query execution time is predominantly governed by disk access latency. In commercial enterprise environments (e.g., e-commerce platforms like Shopee), tables routinely store tens of millions of rows; unindexed queries joining multiple large tables can take hours or days to evaluate `[02:16] – [02:35]`.
- **Administrative Roadmap `[02:50]` – `[03:30]`:** Group project teams, assignment milestone specifications, and the Week 5 progress exam are previewed.
- **Five-Part Lecture Plan `[03:32]` – `[04:45]`:** *(Referencing `slide_004.png`, Deck Page 2)*
  1. *Apps & Performance:* Multi-tier web architectures and speed measurement.
  2. *Inside MySQL Storage:* Pluggable engines, InnoDB, pages, and tablespaces.
  3. *Why Indexes:* Memory hierarchy and avoiding exhaustive row scans.
  4. *How Indexes Work:* Sparse/dense primary/secondary indexes, multi-level structures, $B$-trees, $B^+$-trees, composite, and hash indexes.
  5. *Using Indexes Well:* SQL DDL, `EXPLAIN` plans, selectivity, and FULLTEXT search.

### 2.2 Database Application Eras & Three-Tier Architecture `[04:45]` – `[08:22]`
- **Architectural Eras `[04:45]` – `[06:22]`:** *(Referencing `slide_008.png`, Deck Page 4)*
  - *Desktop Era (Pre-1990s):* Client desktop software communicating directly with a central database server (e.g., legacy airline reservation networks).
  - *Web Era (Mid-1990s):* Web browsers accessing application backends (e.g., early Amazon running atop Oracle DBMS).
  - *Planet Scale (Present Day):* Modern web services serving billions of active users (e.g., Meta/Facebook managing 3+ billion monthly users running on massively distributed MySQL fleets paired with memory-caching layers like Memcached) `[05:39]`.
- **Three-Tier Web Application Model `[06:22]` – `[08:22]`:** *(Referencing `slide_009.png`, Deck Page 5)*
  1. **Presentation Tier:** Client browser (Chrome, Safari) executing UI rendering and static asset caching.
  2. **Logic Tier (Application Server):** Web servers and application runtime engines handling business logic, user authentication, and generating dynamic queries.
  3. **Database Tier (DBMS):** Relational database system (MySQL) managing storage, ACID transactions, data consistency, and disk persistence.
  - *In-Memory Caching Layer:* Memcached or Redis placed between the application logic and DBMS to intercept read traffic and serve hot keys directly from RAM without hitting disk `[07:27]`.

### 2.3 Database Performance Metrics & The Coffee Shop Model `[08:22]` – `[17:19]`
- **Four Core Performance Metrics `[08:22]` – `[10:34]`:** *(Referencing `slide_010.png`, Deck Page 6)*
  1. **Throughput:** System capacity measured in queries, transactions, or requests served per second (e.g., orders completed per unit time).
  2. **Execution Time (Service Time):** Elapsed wall-clock time required to process a single query (measured in milliseconds).
  3. **Concurrency:** Number of active, simultaneous transactions or queries contending for system resources.
  4. **Utilization:** The percentage of time a critical hardware resource is actively engaged:
     $$\text{Utilization} = \text{Throughput} \times \text{Execution Time}$$
     When utilization approaches $100\%$, incoming requests begin queuing indefinitely `[10:23]`.
- **The "Coffee Shop" Case Study `[10:34]` – `[17:19]`:** *(Referencing `slide_011.png` & `slide_012.png`, Deck Pages 7–8)*
  - *Option A (High Concurrency / Parallelism):* 10 machines, each producing 1 cup/min (Execution time: 60s; Total system throughput: 10 cups/min).
  - *Option B (Low Execution Time / Single Fast Server):* 1 ultra-fast machine producing 5 cups/min (Execution time: 12s; Total system throughput: 5 cups/min).
  - *Comparative Performance under Variable Arrival Rates ($\lambda$):*
    - *At $\lambda = 5 \text{ customers/min}$:* Option B wins decisively (12s turnaround vs 60s in Option A).
    - *At $\lambda = 10 \text{ customers/min}$:* Option A keeps up steadily ($100\%$ utilization, 60s turnaround); Option B collapses into an ever-growing queue (arrival rate exceeds max throughput of 5 cups/min).
    - *At $\lambda = 20 \text{ customers/min}$:* Both overload, but Option A's queue accumulates far slower.
  - *Core Engineering Principle:* At low load, minimizing execution time minimizes user latency; at high load, system throughput dictates whether the system remains stable or fails `[16:45]`.

### 2.4 Latency Breakdown, Bottlenecks & Optimization Tools `[17:20]` – `[19:22]`
- **Total Latency Formulation `[17:20]` – `[18:34]`:** *(Referencing `slide_013.png` & `slide_015.png`, Deck Page 9)*
  $$\text{Latency} = \text{Waiting Time (in Queue)} + \text{Execution Time}$$
  As concurrent requests rise, waiting time grows non-linearly when server utilization approaches saturation.
- **The Disk Bottleneck `[18:04]` – `[19:20]`:** CPU utilization (45%) and memory consumption (60%) are rarely the primary bottleneck; disk utilization (95%) is almost always the saturated hardware component.
- **Three Strategic Tools to Eliminate Disk Access `[18:35]` – `[19:22]`:** *(Referencing `slide_014.png`, Deck Page 10)*
  1. **Indexing (Week 2):** Bypassing full table scans to isolate target rows directly.
  2. **Query Optimization (Week 3):** Writing sargable SQL queries that allow the query optimizer to execute efficient join and filter paths.
  3. **Partitioning (Week 4):** Physically dividing monolithic tables into smaller, independently searchable partitions.

### 2.5 MySQL Storage Architecture & InnoDB Internals `[19:34]` – `[26:12]`
- **Pluggable Storage Engine Architecture `[19:34]` – `[22:08]`:** *(Referencing `slide_018.png`, Deck Page 12)*
  - MySQL decouples the upper SQL Server Layer (Connection handling, Query Parsing, Cost-Based Optimizer, Caches & Buffers) from the underlying storage layer.
  - Different engines handle physical file storage, indexing mechanisms, and transaction locking independently:
    - **InnoDB:** Default since MySQL 5.5 `[23:00]`. Fully ACID compliant, supports row-level locking, foreign key constraints, and automatic crash recovery via write-ahead logging (redo log).
    - **MyISAM:** Legacy engine `[21:01]`. Table-level locking only, non-transactional, no foreign keys; fast for read-only workloads, but vulnerable to corruption during crashes.
    - **Memory (HEAP):** Stores all data exclusively in RAM for microsecond access; volatile upon server restart.
    - **CSV:** Directly reads and writes plain comma-separated text files; ideal for data import/export pipelines `[21:32]`.
    - **Archive:** Highly compressed storage optimized for append-only log ingestion.
- **InnoDB Logical to Physical Storage Hierarchy `[23:20]` – `[25:05]`:** *(Referencing `slide_021.png`, Deck Page 15)*
  - **Tablespace:** Top-level storage container consisting of one or more physical OS files.
  - **Segments:** Dedicated allocations within a tablespace (e.g., data segment for leaf nodes, index segment for non-leaf nodes, rollback segment for undo logs).
  - **Extents:** Contiguous blocks of 64 pages ($64 \times 16\text{ KB} = 1\text{ MB}$) allocated to ensure sequential disk reads.
  - **Pages:** The fundamental unit of disk I/O in InnoDB ($16\text{ KB}$). InnoDB never reads or writes individual rows from disk; it reads and writes entire 16 KB pages.
  - **OS Disk Blocks:** Physical sectors on disk, typically $4\text{ KB}$ each (1 InnoDB page $= 4$ OS blocks) `[24:57]`.
- **Tablespace Types `[25:06]` – `[26:12]`:** *(Referencing `slide_022.png` – `slide_027.png`, Deck Pages 16–19)*
  - *System Tablespace (`ibdata1`):* Shared storage for data dictionary, undo logs, doublewrite buffer, and legacy table data.
  - *File-Per-Table Tablespaces (`innodb_file_per_table=ON`):* Default in modern MySQL. Each table receives its own dedicated `.ibd` file (e.g., `products.ibd`). Dropping or truncating a table immediately frees physical disk space back to the operating system filesystem.
  - *General Tablespaces (`CREATE TABLESPACE`):* Shared user-created tablespaces grouping specific tables together.

### 2.6 The Memory Hierarchy & Search Complexity `[26:13]` – `[35:22]`
- **The Memory Hierarchy Gap `[27:34]` – `[28:40]`:** *(Referencing `slide_032.png`, Deck Page 22)*
  - CPU Registers: $< 1\text{ ns}$ access time.
  - L1 / L2 / L3 Caches: $1\text{ ns} – 20\text{ ns}$.
  - Main Memory (RAM): $\approx 100\text{ ns}$.
  - Solid-State Drives (NVMe / SSD): $\approx 100\ \mu\text{s}$ (1,000 times slower than RAM).
  - Hard Disk Drives (HDD): $\approx 5\text{--}10\text{ ms}$ (50,000 to 100,000 times slower than RAM due to physical head seek and rotational latency).
- **Search Complexity in Unindexed Files `[28:41]` – `[35:22]`:** *(Referencing `slide_033.png`, `slide_034.png`, `slide_038.png`, Deck Pages 23–24)*
  - Query: `SELECT * FROM people WHERE id = 123456;`
  - *Unsorted File (Full Table Scan):* Must inspect blocks sequentially. Best case $= 1$ block read; Worst case $= B$ block reads; Average cost $= B / 2$ block reads `[30:48]`.
  - *Sorted File on Primary Key (Binary Search):* If physical records are kept sorted on disk by `id`, binary search requires at most $\lceil \log_2(B) \rceil$ block accesses `[33:29] – [34:42]`.
  - *Problem:* Keeping a multi-gigabyte file physically sorted on disk under frequent inserts and deletes is computationally prohibitive.

### 2.7 Indexing Fundamentals: Worked Mathematical Comparison `[35:23]` – `[45:45]`
- **Definition of an Index `[35:23]` – `[36:32]`:** *(Referencing `slide_040.png`, Deck Page 26)*
  An auxiliary access structure consisting of sorted records of the form:
  $$\langle \text{Search Key Value}, \text{Pointer to Data Block / Record} \rangle$$
- **The Worked Example Baseline Specification `[36:33]` – `[38:47]`:** *(Referencing `slide_043.png`, Deck Page 27)*
  - Total records: $r = 300,000$ records.
  - Record size: $R = 100\text{ bytes}$ (fixed length).
  - Block size: $B = 4,096\text{ bytes}$ ($4\text{ KB}$).
  - Data Blocking Factor:
    $$Bfr = \left\lfloor \frac{4096}{100} \right\rfloor = 40\text{ records per block}$$
  - Total Data Blocks required:
    $$B = \left\lceil \frac{300,000}{40} \right\rceil = 7,500\text{ blocks}$$
  - *Full Table Scan Cost:* Average $\frac{7,500}{2} = 3,750$ block accesses.
- **Primary Index (Sparse) Mechanics `[38:48]` – `[40:48]` & `[41:31]` – `[43:39]`:** *(Referencing `slide_046.png`, `slide_048.png`, `slide_059.png`, Deck Pages 28–29)*
  - Built on a physically ordered primary key field.
  - **Sparse Property:** Only stores **one index entry per data block** (using the block's anchor / first key).
  - Total index entries: $r_i = 7,500\text{ entries}$ (one for each data block).
  - Index Entry Size: Key ($9\text{ bytes}$) + Block Pointer ($6\text{ bytes}$) $= 15\text{ bytes}$.
  - Index Blocking Factor:
    $$Bfr_i = \left\lfloor \frac{4096}{15} \right\rfloor = 273\text{ entries per index block}$$
  - Total Primary Index Blocks:
    $$B_i = \left\lceil \frac{7,500}{273} \right\rceil = 28\text{ blocks}$$
  - **Search Cost:**
    Binary search on the sorted index blocks $+$ 1 access to retrieve the target data block:
    $$\text{Total Block Accesses} = \lceil \log_2(28) \rceil + 1 = 5 + 1 = \mathbf{6\text{ block accesses}}$$
    *(Reduces disk reads from 3,750 to 6).*
- **Secondary Index (Dense) Mechanics `[40:49]` – `[45:45]`:** *(Referencing `slide_051.png`, `slide_065.png`, `slide_070.png`, `slide_071.png`, Deck Pages 30–31)*
  - Built on a non-ordering attribute or secondary search key.
  - **Dense Property:** Must contain **one index entry for every single logical record** in the table.
  - Total index entries: $r_i = 300,000\text{ entries}$.
  - Total Secondary Index Blocks:
    $$B_i = \left\lceil \frac{300,000}{273} \right\rceil = 1,099\text{ blocks}$$
  - **Search Cost:**
    Binary search on dense index $+$ 1 data block fetch:
    $$\text{Total Block Accesses} = \lceil \log_2(1,099) \rceil + 1 = 11 + 1 = \mathbf{12\text{ block accesses}}$$

### 2.8 Multi-Level Indexes, $B$-Trees, and $B^+$-Trees `[45:46]` – `[56:05]`
- **Multi-Level Indexing `[45:46]` – `[48:17]`:** *(Referencing `slide_080.png` – `slide_084.png`, Deck Pages 32–34)*
  - Eliminates binary search across 1,099 index blocks by constructing a sparse primary index *on top of the index itself*:
    - Level 1 (Base index): 1,099 blocks.
    - Level 2: $\lceil 1099 / 273 \rceil = 5$ blocks.
    - Level 3 (Top / Root): $\lceil 5 / 273 \rceil = 1$ root block (fits comfortably in memory).
  - Search cost drops to exactly $3\text{ index block reads} + 1\text{ data block read} = \mathbf{4\text{ block accesses}}$ `[47:34]`.
- **$B$-Tree Structure & Node Splitting `[48:18]` – `[52:15]`:** *(Referencing `slide_085.png` & `slide_086.png`, Deck Pages 35–36)*
  - Balanced multiway tree of order $m$. Every node (except root) contains at least $\lceil m/2 \rceil$ children.
  - Node capacity: at most $m-1$ search keys and $m$ child pointers.
  - When an insert causes a node to overflow ($m$ keys), the node splits into two halves, and the median key is promoted to the parent node `[49:09] – [51:50]`.
  - *Limitation:* $B$-trees store record data pointers in internal nodes as well as leaf nodes, reducing the fan-out capacity of internal nodes.
- **$B^+$-Tree Architecture & Advantages `[52:16]` – `[54:27]`:** *(Referencing `slide_089.png` & `slide_090.png`, Deck Pages 37–38)*
  - Internal nodes store **only search keys and child page pointers**, maximizing the fan-out ratio and minimizing tree height (typically height 3 or 4 for millions of records).
  - **All data pointers reside exclusively in leaf nodes**.
  - Leaf nodes are linked sequentially via a **doubly-linked list** (`prev` and `next` pointers), enabling high-speed range scans (`WHERE price BETWEEN 35 AND 65`) without traversing back up through ancestor nodes `[53:31]`.
- **InnoDB's Dual $B^+$-Tree Architecture `[54:28]` – `[56:05]`:** *(Referencing `slide_091.png`, Deck Page 39)*
  - **Clustered Index (Primary Key):** The table *is* the index. The leaf pages of the clustered index contain the complete, physical row data. If no primary key is explicitly defined, InnoDB promotes the first `NOT NULL UNIQUE` column, or automatically creates a hidden 6-byte `DB_ROW_ID`.
  - **Secondary Index:** Leaf pages store the indexed column values paired with the corresponding **primary key value** (acting as the row pointer).
  - *Bookmark Lookup Cost:* Querying via a secondary index requires traversing the secondary $B^+$-tree to find the primary key, then performing a second traversal down the clustered index tree to retrieve the full row columns (unless the query is completely satisfied by a *Covering Index*) `[55:40]`.

### 2.9 Composite Indexes & Hash Indexes `[56:06]` – `[60:33]`
- **Composite Indexes & The Leftmost-Prefix Rule `[56:06]` – `[58:18]`:** *(Referencing `slide_094.png`, Deck Page 40)*
  - An index created on multiple attributes: `CREATE INDEX idx_city_age ON people (city, age);`
  - Records are sorted first strictly by `city`. Within duplicate `city` values, entries are sorted by `age`.
  - *Seek Eligibility:*
    - `WHERE city = 'Hanoi' AND age = 22` $\rightarrow$ Full index seek on both columns.
    - `WHERE city = 'Hanoi'` $\rightarrow$ Index seek on `city`.
    - `WHERE age = 22` $\rightarrow$ **Cannot seek**; requires a full index scan or table scan because the leading sort order is missing `[57:38]`.
- **Hash Indexes `[58:19]` – `[60:33]`:** *(Referencing `slide_095.png`, Deck Page 41)*
  - Computes a hash function over search keys to map directly into an array of bucket pointers ($O(1)$ constant time lookup).
  - *Critical Drawbacks:* Completely unordered. Ineffective for range queries (`BETWEEN`, `<`, `>`), sorting (`ORDER BY`), or prefix matching. Primarily utilized in MySQL's `MEMORY` storage engine and internal InnoDB *Adaptive Hash Index*.

### 2.10 Practical SQL DDL, `EXPLAIN` & Selectivity Trade-Offs `[60:34]` – `[73:46]`
- **SQL DDL Commands `[60:34]` – `[61:37]`:** *(Referencing `slide_097.png`, Deck Page 43)*
  ```sql
  CREATE INDEX idx_category ON products (category);
  SHOW INDEXES FROM products;
  DROP INDEX idx_category ON products;
  ```
- **Query Diagnostics with `EXPLAIN` `[61:38]` – `[62:25]`:** *(Referencing `slide_098.png`, Deck Page 44)*
  Inspects the query execution plan:
  - `type`: Indicates access path quality (`const` $\rightarrow$ `eq_ref` $\rightarrow$ `ref` $\rightarrow$ `range` $\rightarrow$ `index` $\rightarrow$ `ALL` [full scan]).
  - `possible_keys` vs `key`: Which indexes were evaluated vs which index the optimizer chose.
  - `rows`: Estimated number of rows MySQL must examine.
- **The Indexing Cost Trade-off `[62:26]` – `[64:16]`:** *(Referencing `slide_099.png`, Deck Page 45)*
  Indexes accelerate `SELECT` statements, but penalize data modification operations (`INSERT`, `UPDATE`, `DELETE`) because every index tree must be updated synchronously, and they consume substantial disk space.
- **Selectivity & Why Full Table Scans Beat Index Lookups `[64:17]` – `[68:35]`:** *(Referencing `slide_100.png` & `slide_103.png`, Deck Pages 46–47)*
  - **Selectivity:** The fraction of rows satisfying a query filter condition:
    $$\text{Selectivity} = \frac{\text{Matching Rows}}{\text{Total Rows}}$$
  - *High Selectivity (Few Rows, e.g., 0.1%):* Index lookup is vastly superior.
  - *Low Selectivity (Many Rows, e.g., $> 15\text{--}20\%$):* A secondary index lookup forces random disk I/O as the engine bounces back and forth between secondary index pages and clustered data pages. In contrast, a full table scan performs fast, sequential disk prefetching. When a query matches 40% of rows (as in Slide 47's 6-page example), the optimizer deliberately ignores available indexes in favor of a sequential scan `[66:11] – [67:47]`.
- **Query Design Guidelines `[68:36]` – `[73:46]`:** *(Referencing `slide_108.png`, `slide_109.png`, `slide_112.png`, Deck Pages 48–50)*
  - *Guideline 1 (Retrieval):* Place equality filter columns first, followed by range filter columns in composite indexes:
    `WHERE category = 'Books' AND price BETWEEN 10 AND 50` $\rightarrow$ `INDEX(category, price)`.
    After a range condition, subsequent columns in the composite index can only filter, not seek `[72:58]`.
  - *Guideline 2 (Modification):* Differentiate between columns in the `WHERE` clause (which benefit from indexing to locate target rows) and columns in the `SET` clause (which should be indexed sparingly to avoid write bottlenecks) `[73:07] – [73:46]`.

### 2.11 Interactive Classroom Quiz, Key Takeaways & Tutorial Briefing `[73:56]` – `[81:49]`
- **Classroom Quick-Check Resolution `[73:56]` – `[78:07]`:** *(Referencing `slide_114.png`, Deck Page 52)*
  - *Q1:* Given `INDEX(city, age)`, which condition can NOT seek with it?  
    **Answer: Option 2 (`age = 22`)**, because `city` is omitted, violating the leftmost-prefix rule `[76:35] – [77:02]`.
  - *Q2:* Best index type for `WHERE price BETWEEN 100 AND 200`?  
    **Answer: Option 2 ($B^+$-Tree)**; Hash cannot do ranges, and FULLTEXT is for natural language text `[77:11]`.
  - *Q3:* 7,500 data blocks, 273 index entries/block. How many blocks for primary index?  
    **Answer: Option 1 (28 blocks)**, calculated as $\lceil 7500 / 273 \rceil = 28$ `[77:57]`.
- **Lecture Takeaways `[78:08]` – `[80:14]`:** *(Referencing `slide_129.png` / `slide_155.png`, Deck Page 53)*
  Disk access dominates query cost; $B^+$-trees compress thousands of block reads to 3–4; index `WHERE` and `JOIN` columns; always verify query plans with `EXPLAIN`.
- **Tutorial Assignment Briefing `[80:15]` – `[81:49]`:** *(Referencing `slide_161.png`, `slide_162.png`, `slide_165.png`, Deck Pages 54–56)*
  Students will create a `shopping` database, populate a 100,000-row `products` table via a stored procedure (`insert_sample_products()`), benchmark 5 target queries with and without indexes, record timing differences, inspect `EXPLAIN` output, and experiment with `FULLTEXT` indexing against `bbc-articles.csv`.

---

## 3. Low-Confidence Audit (Verification via `slide_mapping.json` & Slides)

In accordance with Rule 2 of the Lecture Verification Protocol, all segments with `"low_confidence_flag": true` and word-level acoustic distortions have been audited and verified against the slide deck keyframes and context:

| Citation | Corresponding Slide & Deck Reference | Raw Whisper Transcript | Flagged Words (Prob) | Verified Technical Term / Spoken Meaning | Phonetic / Acoustic Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[04:35 (Verified via slide_005)]`** | `slide_005.png`<br>Deck Page 3: Part 01 | "...what are the **three T's**, and..." | `three` (0.23), `are` (0.23) | **"three tiers"** (*"what are the three tiers"*) | **Phonetic Slur:** Lecturer pronounced "tiers" as /tɪəz/, which Whisper mistranscribed as the letter "T's". Slide 3 and Slide 5 explicitly define "Three tiers". |
| **`[06:16 (Verified via slide_008)]`** | `slide_008.png`<br>Deck Page 4 / 5 | "...So there are **three T** of the web..." | `T` (0.32) | **"three tiers"** (*"three tiers of web database applications"*) | Second occurrence of "tiers" misheard as the letter "T". |
| **`[07:27 (Verified via slide_009)]`** | `slide_009.png`<br>Deck Page 5: Three Tiers | "...**cache** in the memcache, this won't go to the database tier anymore." | `cache` (0.01) | **cached in Memcached** | Low probability on the initial clipped syllable "cache". Verified against cache layer annotation on Slide 5. |
| **`[20:26 (Verified via slide_018)]`** | `slide_018.png`<br>Deck Page 12: Engines | "By default, every single engine that you **arrive** is going to be written in using the engine InnoDB." | `arrive` (0.13) | **"write" / "table you create"** | Accent distortion on "write" heard as "arrive". Context is default storage engine for newly created tables. |
| **`[21:01 (Verified via slide_018)]`** | `slide_018.png`<br>Deck Page 12: Engines | "This is the **legacy of the engines**, mostly only for read." | `legacy` (0.23) | **MyISAM** (*legacy storage engine*) | Lecturer pointed to the MyISAM block on Slide 12 while discussing legacy table engines. |
| **`[24:42 (Verified via slide_021)]`** | `slide_021.png`<br>Deck Page 15: Storage | "And inside the pages, we have **blocks**." | `And` (0.05), `pages` (0.17) | **OS Disk Blocks (4 KB)** | Verified against diagram on Slide 15 showing 16 KB pages composed of 4 KB operating system disk blocks. |
| **`[34:30 (Verified via slide_038)]`** | `slide_038.png`<br>Deck Page 20 / 24 | "And if I have **IE items**, then it's going to be exactly three times." | `IE` (0.37) | **"eight items" ($2^3 = 8$)** | **Phonetic Misrecognition:** Speaker explained binary search $\log_2(8) = 3$ comparisons. Whisper heard "eight items" as "IE items". |
| **`[39:20 (Verified via slide_048)]`** | `slide_048.png`<br>Deck Page 28: Primary Index | "...point here, **block three**..." | `point` (0.16), `three` (0.19) | **block accesses / anchor keys** | Speaker pointing to block boundaries in the primary index worked calculation. |
| **`[43:58 (Verified via slide_065)]`** | `slide_065.png`<br>Deck Page 31: Secondary Index | "...that give you a **math index block**." | `math` (0.04) | **"max / data index blocks" (1,099 blocks)** | Misrecognized calculation of $\lceil 300,000 / 273 \rceil = 1,099$ index blocks on Slide 31. |
| **`[48:51 (Verified via slide_085)]`** | `slide_085.png`<br>Deck Page 35: B-Tree | "We got **2 neurons** here, k1, k2." | `neurons` (0.09) | **"2 keys" ($K_1, K_2$)** | **Severe Acoustic Distortion:** Lecturer's pronunciation of "nodes" / "keys" was transcribed as "neurons". Slide 35 explicitly labels search keys $K_1, K_2$ and pointers $P_1, P_2, P_3$. |
| **`[52:18 (Verified via slide_089)]`** | `slide_089.png`<br>Deck Page 37: B+ Tree | "...which is the **B plus 3**." | `plus` (0.09), `3` (0.34) | **$B^+$-Tree** | Whisper transcribed "$B^+$-tree" phonetically as "B plus 3". |
| **`[53:17 (Verified via slide_089)]`** | `slide_089.png`<br>Deck Page 37: B+ Tree | "...and the amount of level in the **B plus 3**..." | `plus` (0.13) | **$B^+$-Tree tree height / levels** | Verified against Slide 37 comparison diagram. |
| **`[66:11 (Verified via slide_103)]`** | `slide_103.png`<br>Deck Page 47: Full Scan | "...imagine we have **six pages** here... sit read **six pages**..." | `pages` (0.16), `sit` (0.24) | **read 6 pages sequentially** | Slide 47 worked diagram: 6 data pages $\times$ 4 rows = 24 rows, illustrating sequential I/O efficiency. |
| **`[73:12 (Verified via slide_112)]`** | `slide_112.png`<br>Deck Page 50: Updates | "...**awfully** or update **awfully**... the indexing stock because if you do that **awfully**..." | `awfully` (0.01, 0.03, 0.06) | **"often" / "frequently"** (*"update frequently"*) | **Severe Phonetic Distortion:** Lecturer's accent on "often" (/ˈɒftən/ or /ˈɔːfən/) transcribed repeatedly as "awfully". Slide 50 states: *"frequently updated columns make writes slower"*. |
| **`[75:07 (Verified via slide_114)]`** | `slide_114.png`<br>Deck Page 52: Quiz | "...is it **h** or **b plus three** of full text..." | `h` (0.02), `plus` (0.18) | **Hash or $B^+$-Tree** | Q2 options on Slide 52: 1. Hash, 2. B+-tree, 3. FULLTEXT. Speaker said "Hash", transcribed as single letter "h". |
| **`[76:35 (Verified via slide_114)]`** | `slide_114.png`<br>Deck Page 52: Quiz | "...then among all the **c** with the same name... jump into the **h** right way..." | `c` (0.06), `way` (0.16) | **"city" and "age"** | Q1 analysis of `INDEX(city, age)`. "c" refers to column `city`, and "h" was misheard for `age`. |
| **`[77:57 (Verified via slide_128)]`** | `slide_128.png`<br>Deck Page 52: Quiz | "...that gives you **28**..." | `that` (0.08) | **28 index blocks** ($\lceil 7,500 / 273 \rceil = 28$) | Q3 calculation confirming Option 1 on Slide 52. |
| **`[78:33 (Verified via slide_129)]`** | `slide_129.png`<br>Deck Page 53: Takeaways | "...B plus three cut a thousand **bridge** to handful that's correct..." | `plus` (0.02), `bridge` (0.05) | **"reads"** (*"cut thousands of reads to a handful"*) | **Phonetic Garble:** Lecturer said "reads", transcribed as "bridge". Directly matches Slide 53 / Slide 34 bullet: *"multilevel B+-trees cut thousands of reads to a handful"*. |
| **`[80:19 (Verified via slide_161)]`** | `slide_161.png`<br>Deck Page 54: Tutorial | "...**role play around** in your database here..." | `role` (0.16) | **"row playground"** | Heading of Slide 54: *"Tutorial this week: build a 100,000-row playground"*. Transcribed phonetically as "role play around". |

---

## 4. Ambiguity Log (Strict Zero-Guessing Rule Applied)

In strict accordance with Rule 4 of the Lecture Verification Protocol, all utterances that remain incomplete, fragmented, or unintelligible after cross-referencing against the slide keyframes have been preserved without fabrication:

| Timestamp | Raw Transcribed Text | Active Slide Keyframe | Deck Match | Ambiguity Analysis & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **`[AMBIGUOUS @ 00:00 – 00:32]`** | Repeated single token `"you"` at `[00:21]` (prob 0.31). | `slide_001.png` – `slide_003.png` | Deck Page 1 (Title) | **Pre-Lecture Background Noise / Whisper Hallucination:** Audio contains microphone setup rustling and classroom ambient noise before Tom Huynh begins speaking at `[00:33]` ("All right afternoon everyone..."). Zero technical content delivered. |
| **`[AMBIGUOUS @ 03:03 – 03:20]`** | *"say releasing the specific, you know, the stretches and procedure, how would yourself for the team in week 5, the exam I think is happening in week 5 or something..."* | `slide_003.png` | Deck Page 1 (Title) | **Syntactically Fragmented Administrative Tangent:** Instructor rambled colloquially about team registration procedures and midterm exam scheduling before opening Slide 2. The exact sentence structure disintegrated into filler words. |
| **`[AMBIGUOUS @ 32:43 – 34:00]`** | *"So, you know, this is just a math, right? Two to the power of three is eight... One, two, three, four..."* | `slide_038.png` | Deck Page 20 (Divider) | **Off-Deck Mathematical Demonstration:** The lecturer switched back to divider Slide 20 and verbally calculated powers of two ($2^1, 2^2, 2^3$) to explain binary search depth without referencing specific slide text. |
| **`[AMBIGUOUS @ 74:10 – 74:25]`** | *"question one two three... question two one two three... question four three... one two three"* | `slide_114.png` | Deck Page 52 (Quiz) | **Muttered In-Class Voting Instructions:** Rapid verbal enumeration reminding students to submit options 1, 2, or 3 into the live classroom chat for each quiz question. |
| **`[AMBIGUOUS @ 76:08 – 76:20]`** | *"um... alright so... some people answering that already..."* | `slide_114.png` | Deck Page 52 (Quiz) | **Classroom Chat Wait State:** Unstructured pause while the instructor monitored incoming student responses in the chat window. |
| **`[AMBIGUOUS @ 79:45 – 80:05]`** | *"the... blah blah blah... index speed... this is actually very very... I think the RAM is pretty bad... alright"* | `slide_160.png` | Deck Page 53 (Takeaways) | **Trailing Verbal Muttering / Equipment Aside:** Instructor trailed off into filler phrases ("blah blah blah") while commenting off-hand on computer memory latency before advancing to the tutorial slides. |

