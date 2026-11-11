# Verified Technical Lecture Summary & Confidence Audit

**Task:** `lecture3`  
**Course:** ISYS2099 / ISYS3434 — Database Applications  
**Lecture Topic:** Week 03 — Query Optimization  
**Instructor:** Tom Huynh (School of Science, Engineering & Technology, RMIT University Vietnam)  
**Audited Assets (Strict Local Isolation):**
- **Video Source:** `record/lecture3.mp4` (Duration: 85m 06s)
- **Audio Source:** `pipeline/lecture3/audio.mp3`
- **Slide Snapshots:** `pipeline/lecture3/slides/slide_001.png` to `slide_237.png` (237 keyframes)
- **Slide Mapping:** `pipeline/lecture3/slide_mapping.json` (237 matched keyframes)
- **Deck Alignment:** `pipeline/lecture3/deck_alignment.md` (Referenced to `lecture/lecture3.pdf`, 57 slides)
- **Transcript File:** `pipeline/lecture3/transcript.json` (723 structured segments with word-level probabilities)

---

## 1. Executive Summary

This lecture presents a comprehensive analysis of **Relational Query Optimization** within modern relational database systems, emphasizing the cost-based query optimizer in MySQL 8. The instructor, Tom Huynh, establishes the critical necessity of query optimization: while unoptimized SQL queries may appear responsive on development datasets of 1,000 rows, they inevitably degrade or fail when executed against production tables containing millions of records. Optimization reduces physical disk I/O, CPU cycles, and memory consumption, enabling applications to scale reliably without requiring expensive hardware upgrades.

The session systematically traverses the three-stage SQL execution lifecycle: **Parsing** (syntactic and semantic validation), **Optimization** (candidate execution plan enumeration, cost estimation via catalog statistics, and lowest-cost plan selection), and **Execution** (runtime storage engine interaction). The theoretical foundation of optimization is established via **Relational Algebra** ($\pi$ Project, $\sigma$ Select, $\bowtie$ Join, and $\times$ Cartesian Product) mapped directly to **Query Trees**. Through the Movie and Director worked example, the lecture proves mathematically how relational algebra transformation rules—specifically **pushing selections down the query tree** before executing joins—reduce intermediate Cartesian products from 10,000,000 tuple pairs to a compact set of 1,000 rows, cutting disk I/O by over $12\times$.

At the physical execution layer, the lecture examines:
1. **Access Paths:** Contrasting full table scans (`ALL`), index point lookups (`const`, `eq_ref`, `ref`), and index range scans (`range`).
2. **Sorting & LIMIT Optimization:** Distinguishing in-memory Quicksort from disk-based External Merge Sort (Filesort), demonstrating how indexing the sort column allows MySQL to stream ordered index leaves and terminate immediately upon satisfying a `LIMIT` clause.
3. **Join Algorithms:** Formally comparing **Nested-Loop Join** (including Index Nested-Loop), **Hash Join** (MySQL 8's two-phase build/probe engine for large unindexed equi-joins), and **Sort-Merge Join**.

Finally, the session provides practical operational mastery of MySQL diagnostic utilities: reading standard **`EXPLAIN`** plans (evaluating access `type`, `key`, `rows`, and `Extra`) and advanced **`EXPLAIN ANALYZE`** tree outputs (introduced in MySQL 8.0.18 to contrast estimated costs with true runtime milliseconds and loop counts). The lecture concludes with authoritative guidelines for authoring **sargable** (Search ARGument-able) SQL, demonstrating why wrapping indexed columns in scalar functions (e.g., `YEAR(Bdate) = 1990`) blinds the optimizer into full table scans, how to rewrite correlated subqueries into efficient joins, and previews the Week 3 tutorial benchmarking `company` (indexed) against `company_no_key` (unindexed).

---

## 2. High-Confidence Technical Takeaways (Citing Exact `[MM:SS]` Timestamps)

### 2.1 Course Administration & Agenda Overview `[00:16]` – `[04:33]`
- **Administrative Preview `[00:56]` – `[02:14]`:** Student team formation for the course group project and guidelines for the upcoming in-class test are previewed.
- **Five-Part Agenda `[02:20]` – `[04:33]`:** *(Referencing `slide_007.png`, Deck Page 2)*
  1. *Why Optimize:* Symptoms of slow queries and the internal SQL execution pipeline.
  2. *Cost-Based Optimization:* Query trees, relational algebra, and intermediate I/O reduction.
  3. *How Query Parts Run:* Physical access paths, in-memory vs external sorting, and the 3 join algorithms.
  4. *MySQL Tools:* Diagnostic inspection via `EXPLAIN` and `EXPLAIN ANALYZE`.
  5. *Optimization Guides:* Sargable queries, `AND` vs `OR`, join order heuristics, and subquery rewrites.

### 2.2 Why Query Optimization Matters & The SQL Pipeline `[04:33]` – `[10:16]`
- **The Imperative for Optimization `[04:33]` – `[05:45]`:** *(Referencing `slide_013.png`, Deck Page 4)*
  - Queries operating on 1,000 rows execute in milliseconds, but as datasets scale to 10+ million rows, unoptimized queries cause massive latency spikes, timeouts, and severe server resource exhaustion `[04:40]`.
  - Optimization minimizes physical block reads (I/O), CPU cycles, and memory consumption, allowing applications to scale without hardware upgrades.
  - *Week 2 Teaser Callback:* Queries containing `WHERE YEAR(Bdate) = 1990` ignore existing indexes on `Bdate` due to non-sargability, a flaw resolved in Part 5 `[05:26]`.
- **Warning Signs & Diagnostic Philosophy `[05:45]` – `[07:34]`:** *(Referencing `slide_014.png`, Deck Page 5)*
  - Key warning signs: exponential latency growth as tables expand, page timeouts, high CPU/disk saturation, and temporary tables or full table scans proliferating in MySQL slow query logs `[06:46]`.
  - *Core Principle:* *"Diagnose before you treat."* Pinpoint the exact slow query and evaluate its execution plan using `EXPLAIN` before attempting to add random indexes `[07:25]`.
- **The Three-Stage SQL Pipeline `[07:34]` – `[08:56]`:** *(Referencing `slide_015.png`, Deck Page 6)*
  1. **Parse Stage:**
     - *Syntax Check:* Verifies valid SQL grammar (e.g., misspelled keywords like `SELEC name FROM Student` trigger `Error 1064: Syntax error` and halt execution immediately).
     - *Semantic Check:* Validates catalog metadata—verifying whether referenced tables and column identifiers physically exist (e.g., querying nonexistent column `nme` triggers `Error 1054: Unknown column`).
  2. **Optimize Stage:** The query optimizer enumerates candidate execution strategies, estimates computational and I/O costs using catalog statistics, and selects the lowest-cost plan `[08:07]`.
  3. **Execute Stage:** The execution engine calls the underlying storage engine (InnoDB) API to retrieve and return rows `[08:34]`.
- **Quiz: Optimizer Plan Selection `[08:56]` – `[10:16]`:** *(Referencing `slide_016.png`, Deck Page 7)*
  - *Question:* When multiple plans produce identical results, how does MySQL decide which to execute?
  - *Resolution:* **Option 2** (The optimizer estimates each plan's cost from data statistics and picks the cheapest). It does *not* execute every plan, nor does it blindly follow written SQL syntax order `[10:00]`.

### 2.3 Cost-Based Optimization, Query Trees & Relational Algebra `[10:16]` – `[30:01]`
- **Query Trees Structure `[10:37]` – `[12:12]`:** *(Referencing `slide_018.png`, Deck Page 9)*
  - Internal nodes represent relational algebra operators ($\pi$ Project, $\sigma$ Select, $\bowtie$ Join).
  - Leaf nodes represent base storage tables (or index access paths).
  - Data flows strictly **bottom-up**: base tables feed through intermediate filtering/joining nodes to the root, which outputs the final result set `[10:50] – [11:08]`.
- **Four Core Relational Algebra Operators `[12:12]` – `[15:47]`:** *(Referencing `slide_019.png`, Deck Page 10)*
  1. **$\pi$ (Project):** Corresponds to the SQL `SELECT` column list; extracts specific attributes (e.g., $\pi_{\text{dirname}}(\text{Director})$) `[12:26]`.
  2. **$\sigma$ (Select):** Corresponds to the SQL `WHERE` clause; filters tuples based on predicate conditions (e.g., $\sigma_{\text{dirname} = \text{'Allen, Woody'}}(\text{Director})$). *Crucial pedagogical distinction: relational selection $\sigma$ is filtering, not the SQL SELECT keyword* `[12:40] – [12:52]`.
  3. **$\bowtie$ (Join):** Equi-join on predicate conditions (e.g., $\text{Movie} \bowtie_{m.\text{dirnumb} = d.\text{dirnumb}} \text{Director}$) `[13:00]`.
  4. **$\times$ (Cartesian Product):** Unconditional cross-multiplication of two relations (e.g., `FROM Movie, Director` without a `WHERE` join condition). If Relation $A$ has 10 rows and Relation $B$ has 5 rows, $A \times B$ produces $50$ tuples `[13:28] – [13:50]`.
- **Quiz: SQL to Relational Algebra Mapping `[14:44]` – `[15:47]`:** *(Referencing `slide_020.png`, Deck Page 11)*
  - Query: `SELECT dirname FROM Director WHERE dirnumb = 3;`
  - *Resolution:* **Option 3** ($\pi_{\text{dirname}}(\sigma_{\text{dirnumb} = 3}(\text{Director}))$). The relation is first filtered by selection $\sigma$, then projected via $\pi$ `[15:30]`.
- **Movie & Director Worked Cost Example `[15:54]` – `[26:40]`:** *(Referencing `slide_023.png` – `slide_036.png`, Deck Pages 12–17)*
  - *Dataset Parameters:* `Movie` table $= 10,000\text{ rows}$; `Director` table $= 1,000\text{ rows}$.
  - *Query:* Find titles of movies directed by Woody Allen (`dirnumb` foreign key join, filter `dirname = 'Allen, Woody'`).
  - **Tree 1 (Cartesian Product $\times \rightarrow \sigma \rightarrow \pi$):**
    - First executes `Movie` $\times$ `Director`, producing $10,000 \times 1,000 = \mathbf{10,000,000\text{ intermediate tuple pairs}}$.
    - Subsequently filters by join condition and director name.
    - Massive memory and temporary disk buffer footprint `[21:28] – [22:16]`.
  - **Tree 2 (Join $\bowtie \rightarrow \sigma \rightarrow \pi$):**
    - Executes `Movie` $\bowtie$ `Director` first, producing an intermediate relation of $10,000\text{ rows}$.
    - Filters the 10,000 joined records for Woody Allen.
  - **Tree 3 (Selection Pushed Down $\sigma \rightarrow \bowtie \rightarrow \pi$):**
    - Pushes selection down directly to the `Director` table *before* joining:
      $$\sigma_{\text{dirname} = \text{'Allen, Woody'}}(\text{Director}) \rightarrow \mathbf{1\text{ row}}$$
    - Joins the single Woody Allen director tuple against `Movie` ($1 \times 10,000 \rightarrow 10,000$ comparisons).
    - **Performance Gain:** Tree 3 requires over **$12\times$ less I/O** than Tree 1 and completely avoids generating the 10M-record Cartesian cross-product `[25:15] – [26:22]`.
- **Scaling Up & Cost Principle `[26:40]` – `[30:01]`:** *(Referencing `slide_037.png` & `slide_038.png`, Deck Pages 18–19)*
  - If `Movie` scales to 1,000,000 rows and `Director` to 100,000 rows:
    Tree 1 generates $10^6 \times 10^5 = \mathbf{10^{11}\text{ rows}}$ (100 billion tuples, crashing the server), while Tree 3 filters `Director` to 1 row and only scans the 1M movies.
  - *Quiz Resolution:* Tree 3 is cheapest because **filtering early dramatically reduces the cardinality of intermediate relations** entering subsequent join operators `[27:51] – [30:01]`.

### 2.4 Physical Access Paths, Sorting & Join Algorithms `[30:08]` – `[50:21]`
- **WHERE Access Paths `[30:08]` – `[31:53]`:** *(Referencing `slide_042.png` / `slide_077.png`, Deck Page 21)*
  - *Full Table Scan (`ALL`):* Reads all physical data pages sequentially. Chosen when no matching index exists or when the query matches a large percentage of table rows ($>15\text{--}20\%$).
  - *Index Lookup (`ref` / `eq_ref` / `const`):* Directly traverses $B^+$-tree indexes to isolate target keys.
  - *Index Range Scan (`range`):* Traverses index to the range boundary, then scans along the doubly-linked leaf nodes.
- **Projection Overhead & `SELECT *` Antipattern `[31:53]` – `[32:43]`:** *(Referencing `slide_078.png`, Deck Page 22)*
  - Projection (choosing columns) is executed in RAM on retrieved tuples and is computationally cheap.
  - However, specifying unnecessary columns (`SELECT *`) prevents MySQL from utilizing **Covering Indexes** (where all requested columns reside in the index itself), forcing unnecessary disk reads to retrieve base table rows `[32:15]`.
- **ORDER BY: Sorting Costs & The LIMIT Optimization `[32:44]` – `[38:25]`:** *(Referencing `slide_079.png` & `slide_080.png`, Deck Pages 23–24)*
  - *In-Memory Sort:* If sorted data fits within `sort_buffer_size`, MySQL executes an in-memory Quicksort.
  - *External Merge Sort (Filesort):* If data exceeds memory, MySQL divides rows into chunks, writes temporary files to disk, and merges them. Disk I/O rises drastically `[33:15]`.
  - *The `ORDER BY ... LIMIT 10` Benchmark:*
    - *Without Index on Sort Column:* MySQL must scan **all 100,000 rows**, sort them in a Filesort buffer, and only then discard 99,990 rows to return 10.
    - *With Index on Sort Column:* The $B^+$-tree is already sorted physically. MySQL walks the first 10 index leaf entries, fetches 10 corresponding data rows, and **terminates execution immediately** (reading 10 rows instead of 100,000) `[35:33] – [37:45]`.
- **Three Join Algorithms at a Glance `[38:25]` – `[45:34]`:** *(Referencing `slide_083.png` – `slide_097.png`, Deck Pages 25–28)*
  1. **Nested-Loop Join `[38:25]` – `[41:40]`:**
     - *Algorithm:* Outer loop iterates through each row of the outer table; inner loop scans the inner table for matches.
     - *Simple Nested-Loop:* Cost is $O(|R| \times |S|)$; catastrophic on large tables.
     - *Index Nested-Loop:* Outer table scans $|R|$ rows, but inner table lookups use an index ($O(\log |S|)$ per row). Highly efficient when the inner join column is indexed.
  2. **Hash Join `[41:41]` – `[43:08]`:**
     - Designed for **equi-joins on large tables lacking indexes** (introduced natively in MySQL 8 to replace block nested-loop).
     - *Phase 1 (Build):* Scans the smaller input table and builds an in-memory hash table using the join attribute as the hash key `[60:46]`.
     - *Phase 2 (Probe):* Scans the larger input table sequentially, hashing each row's join attribute to probe the in-memory hash table for matching rows. Cost is linear: $O(|R| + |S|)$.
  3. **Sort-Merge Join `[43:08]` – `[43:30]`:**
     - Requires both input tables to be sorted on the join attribute.
     - Walks both relations simultaneously in a single coordinated sequential pass. Excellent when inputs are already ordered by clustered indexes.
- **Join Algorithm Comparison & Optimizer Selection `[43:31]` – `[50:21]`:** *(Referencing `slide_098.png` – `slide_114.png`, Deck Pages 28–30)*
  - Small tables or presence of secondary index $\rightarrow$ Nested-Loop Join.
  - Large unindexed tables joined on equality $\rightarrow$ Hash Join.
  - Pre-sorted inputs $\rightarrow$ Sort-Merge Join.

### 2.5 Diagnostic Utilities: EXPLAIN & EXPLAIN ANALYZE `[50:21]` – `[62:32]`
- **Root Causes of Slow Queries `[50:31]` – `[52:06]`:** *(Referencing `slide_118.png`, Deck Page 32)*
  Scanning excessive rows, missing indexes on filter/join columns, unindexed join attributes forcing repetitive scans, and disk-based filesorts.
- **Reading EXPLAIN Column Metrics `[52:06]` – `[55:13]`:** *(Referencing `slide_124.png` & `slide_125.png`, Deck Pages 33–34)*
  - `select_type`: `SIMPLE` (flat query), `PRIMARY` / `SUBQUERY`, or `DEPENDENT SUBQUERY` (correlated subquery executing per outer row).
  - `type`: Access method ranked from best to worst:
    $$\mathbf{const} > \mathbf{eq\_ref} > \mathbf{ref} > \mathbf{range} > \mathbf{index} > \mathbf{ALL}$$
    - `const`: Primary key or unique index lookup with constant value (1 row).
    - `eq_ref`: 1 row read per outer row via unique/primary key join.
    - `ref`: Non-unique index lookup matching multiple rows.
    - `range`: Index range scan using operators (`BETWEEN`, `<`, `>`, `IN`).
    - `index`: Full index scan (scans entire index tree without seeking).
    - `ALL`: Full table scan reading all data pages from disk.
  - `possible_keys`: Indexes available to the optimizer.
  - `key`: The specific index actually chosen by the optimizer (`NULL` if no index used).
  - `rows`: Estimated number of rows MySQL expects to inspect.
  - `filtered`: Percentage of rows filtered out by remaining conditions ($100\%$ is ideal).
  - `Extra`: Critical operational flags (`Using index` = covering index; `Using where` = engine filtered rows; `Using filesort` = separate sort pass; `Using temporary` = disk/memory temp table; `Using hash join` = hash join executed).
- **EXPLAIN on COMPANY vs COMPANY_NO_KEY `[55:13]` – `[57:56]`:** *(Referencing `slide_126.png` – `slide_130.png`, Deck Pages 35–37)*
  - Running `SELECT * FROM EMPLOYEE WHERE Dno = 4;`:
    - On indexed `company`: uses `ref` access on `idx_dno`, inspecting only 3 rows.
    - On unindexed `company_no_key`: uses `ALL` access, inspecting all employee rows.
- **EXPLAIN ANALYZE (MySQL 8.0.18+) `[57:56]` – `[62:32]`:** *(Referencing `slide_139.png`, `slide_140.png`, `slide_156.png`, Deck Pages 38–40)*
  - While `EXPLAIN` shows static estimates derived from statistics, `EXPLAIN ANALYZE` physically runs the query and prints the true execution tree `[57:56]`.
  - Output breakdown:
    `-> Inner hash join (D.Dnumber = E.Dno)  (cost=115.00 rows=100) (actual time=0.12..0.85 rows=30 loops=1)`
    - `cost=115.00 rows=100`: Optimizer's upfront statistical estimate.
    - `actual time=0.12..0.85`: Milliseconds to return the first row (0.12 ms) and complete all rows (0.85 ms).
    - `rows=30 loops=1`: Actual number of rows produced across 1 iteration loop.
  - Crucial for diagnosing "optimizer mistakes" where stale statistics lead the optimizer to severely underestimate table cardinality `[58:49] – [60:04]`.

### 2.6 Optimization Guidelines: Sargability, Patterns & Subqueries `[62:33]` – `[78:00]`
- **Sargable Queries ("Search ARGument-able") `[62:33]` – `[71:02]`:** *(Referencing `slide_171.png` – `slide_179.png`, Deck Pages 42–44)*
  - A query predicate is **sargable** if the database engine can directly seek into an index without evaluating scalar transformations row by row `[62:47]`.
  - **The Cardinal Rule:** *Do not apply functions or arithmetic operators to the indexed column in the WHERE clause.*
  - *Non-Sargable vs Sargable Transformations:*
    - *Date Functions:*
      `WHERE YEAR(order_date) = 2024` $\rightarrow$ **Non-sargable (`type: ALL`, 100,000 rows scanned)**.
      *Fix:* `WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'` $\rightarrow$ **Sargable (`type: range`, index seek)** `[65:13] – [66:22]`.
    - *Arithmetic Operations:*
      `WHERE price * 1.1 > 100` $\rightarrow$ **Non-sargable**.
      *Fix:* `WHERE price > 100 / 1.1` $\rightarrow$ **Sargable** (moves math to the constant side).
    - *String / Substring Operations:*
      `WHERE SUBSTRING(name, 1, 3) = 'Tom'` $\rightarrow$ **Non-sargable**.
      *Fix:* `WHERE name LIKE 'Tom%'` $\rightarrow$ **Sargable** (prefix seek).
- **LIKE and REGEXP Matching `[71:02]` – `[72:43]`:** *(Referencing `slide_180.png` & `slide_181.png`, Deck Pages 45–46)*
  - `LIKE 'Smith%'` (Trailing wildcard): **Sargable**. The $B^+$-tree uses the fixed `'Smith'` prefix to execute a range seek.
  - `LIKE '%Smith'` or `LIKE '%Smith%'` (Leading wildcard): **Non-sargable**. Any string could match; forces full table scan (`ALL`).
  - `REGEXP`: **Non-sargable**. Regular expression evaluation requires inspecting every single row string.
- **AND vs OR Predicates `[72:43]` – `[73:47]`:** *(Referencing `slide_182.png`, Deck Page 47)*
  - `WHERE colA = 1 AND colB = 2`: Can utilize an index on `colA`, an index on `colB`, or optimally a composite `INDEX(colA, colB)`.
  - `WHERE colA = 1 OR colB = 2`: Both columns must have independent indexes to allow an `index_merge` union. If either column lacks an index, MySQL **abandons index usage entirely and falls back to a full table scan (`ALL`)**.
- **Join Ordering Heuristics `[73:47]` – `[74:55]`:** *(Referencing `slide_183.png`, Deck Page 48)*
  When joining tables $A$, $B$, and $C$, the optimizer chooses the join order that minimizes intermediate result sets—prioritizing the most selective, smallest table as the outer driving table `[74:26]`.
- **Correlated Subqueries vs JOINs `[74:55]` – `[76:48]`:** *(Referencing `slide_184.png` – `slide_188.png`, Deck Pages 49–51)*
  - Correlated subqueries (`WHERE EXISTS (SELECT ... WHERE o.customer_id = c.id)`) conceptually re-execute for every single outer row (`DEPENDENT SUBQUERY`), causing $O(N \times M)$ overhead `[75:20]`.
  - Rewriting into an inner or semi-join (`SELECT DISTINCT c.id, c.name FROM customers c JOIN orders o ON o.customer_id = c.id`) allows the optimizer complete flexibility to reorder tables and leverage indexes `[75:29]`.
  - *Anti-joins:* To find customers with no orders, prefer `NOT EXISTS` or `LEFT JOIN ... WHERE o.customer_id IS NULL` over `NOT IN (...)`, as `NOT IN` fails or produces unintended empty sets if the subquery returns even a single `NULL` value `[75:46]`.

### 2.7 Classroom Quick Check, Key Takeaways & Tutorial Briefing `[76:49]` – `[85:06]`
- **Interactive Quick-Check Quiz `[78:00]` – `[81:51]`:** *(Referencing `slide_191.png`, Deck Page 54)*
  - *Q1:* Which WHERE clause can use an index on `order_date`?  
    **Answer: Option 1 (`order_date >= '2024-01-01' AND order_date < '2025-01-01'`)**; Options 2 and 3 wrap the column in `YEAR()` and `DATE_FORMAT()`, blinding the index `[79:51] – [80:07]`.
  - *Q2:* A query reads 100,000 rows to return 289. What do you check first?  
    **Answer: Option 2 (Check whether the WHERE clause is sargable and indexed)**; adding hardware or writing nested subqueries does not resolve the scan `[80:15] – [80:43]`.
  - *Q3:* Two large tables joined on equality with no usable index. Which algorithm does MySQL 8 use?  
    **Answer: Option 3 (Hash join)**; MySQL 8 automatically builds an in-memory hash table for unindexed equi-joins `[80:58] – [81:36]`.
- **Lecture Takeaways `[81:51]` – `[84:30]`:** *(Referencing `slide_230.png` – `slide_234.png`, Deck Page 55)*
  - The optimizer evaluates candidate plans based on estimated cost; filter rows early to avoid Cartesian intermediate products.
  - Joins execute via nested-loop or hash join algorithms; indexes on join keys make nested-loop fast.
  - Use `EXPLAIN` to view the plan, and `EXPLAIN ANALYZE` to inspect actual elapsed times and row counts.
  - Always run `ANALYZE TABLE` after populating large datasets or creating new indexes to refresh optimizer catalog statistics `[82:18] – [82:23]`.
  - Write sargable, index-friendly SQL by avoiding scalar functions on indexed fields.
- **Tutorial Assignment Briefing `[76:49]` – `[77:47]`:** *(Referencing `slide_189.png` & `slide_190.png`, Deck Pages 52–53)*
  Students will benchmark identical queries across two Canvas databases: `company` (enforcing primary and foreign keys with B+-tree indexes) versus `company_no_key` (unindexed tables). Exercises explore `AND` vs `OR`, join ordering, subqueries versus joins, and measuring execution time differences using `EXPLAIN ANALYZE`.

---

## 3. Low-Confidence Audit (Verification via `slide_mapping.json` & Slides)

In accordance with Rule 2 of the Lecture Verification Protocol, all segments with `"low_confidence_flag": true` and word-level acoustic distortions have been audited and verified against the slide deck keyframes and context:

| Citation | Corresponding Slide & Deck Reference | Raw Whisper Transcript | Flagged Words (Prob) | Verified Technical Term / Spoken Meaning | Phonetic / Acoustic Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[03:28 (Verified via slide_007)]`** | `slide_007.png`<br>Deck Page 2: Plan | "...talk about the **circle ball queries** and versus all also..." | `circle` (0.11), `ball` (0.24) | **sargable queries** (*"sargable queries and AND versus OR"*) | **Severe Phonetic Garble:** Lecturer's pronunciation of "sargable" (/ˈsɑːrdʒəbəl/) was heard as "circle ball". Slide 2 explicitly lists "Sargable queries". |
| **`[07:38 (Verified via slide_015)]`** | `slide_015.png`<br>Deck Page 6: Pipeline | "...stages the first one is your **sql stacking** is that is that is what..." | `what` (0.03), `stacking` (0.26) | **"SQL text / SQL statements"** | Accent distortion on "text" transcribed as "stacking". Slide 6 diagram lists "SQL text: what you send". |
| **`[11:03 (Verified via slide_018)]`** | `slide_018.png`<br>Deck Page 9: Query Trees | "...note here we have different operation here we have the **projections**..." | `projections` (0.12), `internal` (0.21) | **Projection ($\pi$)** | Verified: Internal node in Slide 9 query tree representing relational projection. |
| **`[11:33 (Verified via slide_018)]`** | `slide_018.png`<br>Deck Page 9: Query Trees | "...this is how we call **sigma** okay this is how you call it **sigma**..." | `sigma` (0.01), `call` (0.32) | **Selection ($\sigma$)** | Low probability on Greek letter "sigma" ($\sigma_{\text{dept\_name}=\text{'Music'}}$). |
| **`[11:50 (Verified via slide_018)]`** | `slide_018.png`<br>Deck Page 9: Query Trees | "...selecting the column name which is your **pie** okay we also mean project..." | `pie` (0.27), `also` (0.33) | **Pi ($\pi$)** (*"which is your $\pi$, which also means project"*) | Whisper transcribed Greek symbol $\pi$ as food homophone "pie". |
| **`[13:00 (Verified via slide_019)]`** | `slide_019.png`<br>Deck Page 10: Rel Algebra | "...yep **allen woody woody** is the director and join here..." | `allen` (0.01), `woody` (0.28) | **Woody Allen** ($\sigma_{\text{dirname}=\text{'Allen, Woody'}}(\text{Director})$) | Speaker read aloud the name from Slide 10 example; transcribed with reversed word order. |
| **`[13:28 (Verified via slide_019)]`** | `slide_019.png`<br>Deck Page 10: Rel Algebra | "...but you also can do **Cartesian products** this one could cross..." | `products` (0.33) | **Cartesian Product ($\times$)** | Cross-product operator on Slide 10. |
| **`[21:28 (Verified via slide_027)]`** | `slide_027.png`<br>Deck Page 14: Tree 1 | "...and then it's generate an intermediate table here with **10 million**..." | `million` (0.18) | **10,000,000 tuple pairs** ($10,000 \times 1,000$) | Slide 14 Tree 1 intermediate cardinality calculation. |
| **`[25:15 (Verified via slide_034)]`** | `slide_034.png`<br>Deck Page 17: Cost | "...Tree 3 give you **12 times less IO**..." | `12` (0.21), `times` (0.30) | **$12\times$ less I/O** | Headline of Slide 17: *"12× less I/O"*. |
| **`[33:15 (Verified via slide_079)]`** | `slide_079.png`<br>Deck Page 23: Sorting | "...we have to doing what we call that a **file shot** or external merge shot..." | `shot` (0.19, 0.22) | **"filesort or external merge sort"** | Non-native pronunciation of "sort" (/sɔːrt/) transcribed as "shot". Slide 23 covers in-memory sort vs external merge sort (Filesort). |
| **`[35:33 (Verified via slide_080)]`** | `slide_080.png`<br>Deck Page 24: LIMIT | "...if you say **order by stock limit 10** without an index..." | `stock` (0.21), `limit` (0.18) | **`ORDER BY stock LIMIT 10`** | Matches Slide 24 SQL benchmark comparing indexed vs unindexed order execution. |
| **`[41:45 (Verified via slide_086)]`** | `slide_086.png`<br>Deck Page 26: Hash Join | "...algorithm number two is **hash joy** for equi join..." | `joy` (0.21), `equi` (0.29) | **Hash Join for equi-joins** | "Join" transcribed phonetically as "joy". Slide 26 title: *"Join algorithm 2: hash join (equi-joins)"*. |
| **`[60:46 (Verified via slide_156)]`** | `slide_156.png`<br>Deck Page 39: Hash Join | "...it's building the **hash table** okay it's very important within hash table here for lookup D then it actually scan through the whole E..." | `hash` (0.02), `table` (0.17) | **Build phase (Hash Table) and Probe phase** | Lecturer explaining Slide 39 EXPLAIN ANALYZE hash join output: building hash table on Department $D$, probing with Employee $E$. |
| **`[62:33 (Verified via slide_171)]`** | `slide_171.png`<br>Deck Page 42: Sargable | "...part number five uh so **circle ball queries** right what is **circle ball query**..." | `circle` (0.00), `ball` (0.14) | **Sargable queries** | Second occurrence: lecturer defines "sargable" from Slide 42 (*"Sargable = Search ARGument-able"*). |
| **`[65:13 (Verified via slide_172)]`** | `slide_172.png`<br>Deck Page 43: Sargable | "...convert from not a **circle ball** query to a **circle ball** query how much it gonna be run faster..." | `circle` (0.01), `ball` (0.19) | **non-sargable to sargable query** | Slide 43 benchmark comparing `YEAR(order_date) = 2024` with date range rewrite. |
| **`[75:20 (Verified via slide_184)]`** | `slide_184.png`<br>Deck Page 49: Subqueries | "...this is not very efficient because this is a **nested loop** this one can be rewrite by just the normal join..." | `nested` (0.07), `loop` (0.15) | **nested loop / correlated subquery** | Slide 49 explanation of rewriting correlated `EXISTS` subqueries into standard joins. |
| **`[79:36 (Verified via slide_191)]`** | `slide_191.png`<br>Deck Page 54: Quiz | "...**minus zero eight** gonna juice..." | `minus` (0.07), `zero` (0.11), `juice` (0.22) | **"MySQL 8 gonna choose"** | **Severe Acoustic Distortion:** Lecturer said "MySQL 8 gonna choose", heard as "minus zero eight gonna juice". Q3 on Slide 54. |
| **`[81:36 (Verified via slide_229)]`** | `slide_229.png`<br>Deck Page 54: Quiz | "...that's gonna be the **hard choice** that would be option number three here..." | `hard` (0.16), `choice` (0.24) | **"Hash join" (Option 3)** | Resolving Q3: Whisper mistranscribed "Hash join" as "hard choice". |
| **`[82:23 (Verified via slide_231)]`** | `slide_231.png`<br>Deck Page 55: Takeaways | "...you always say **analyze table** right this is for what because you want to refresh the **minus square statistic**..." | `minus` (0.03), `square` (0.12) | **MySQL statistics** (*"refresh MySQL statistics" via `ANALYZE TABLE`*) | Transcribed "MySQL" as "minus square". Slide 55 takeaways. |
| **`[82:43 (Verified via slide_232)]`** | `slide_232.png`<br>Deck Page 55: Takeaways | "...so for joining is running using the **next loop** or the **hash loop**..." | `next` (0.13), `hash` (0.18) | **nested-loop or hash join** | Pronunciation of "nested" heard as "next". Matches Slide 55 bullet 2. |
| **`[83:24 (Verified via slide_232)]`** | `slide_232.png`<br>Deck Page 55: Takeaways | "...write the **cycle cycle** and index friendly SQL here..." | `cycle` (0.22) | **"sargable and index-friendly SQL"** | Mistranscription of "sargable" as "cycle cycle". Directly references Slide 55 bullet 4. |

---

## 4. Ambiguity Log (Strict Zero-Guessing Rule Applied)

In strict adherence to Rule 4 of the Lecture Verification Protocol, all utterances that remain incomplete, fragmented, or unintelligible after cross-referencing against the slide keyframes have been preserved without fabrication:

| Timestamp | Raw Transcribed Text | Active Slide Keyframe | Deck Match | Ambiguity Analysis & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **`[AMBIGUOUS @ 00:00 – 00:15]`** | Microphone rustling and ambient background noise before `[00:16]`. | `slide_001.png` – `slide_003.png` | Deck Page 1 (Title) | **Pre-Lecture Background Noise / Classroom Setup:** Ambient audio before Tom Huynh opens the lecture. Zero technical information delivered. |
| **`[AMBIGUOUS @ 01:10 – 01:45]`** | *"windows mic for your tutorial in workshop majority of you using windows okay I think we have roughly gonna have some information regarding the instruction also requirement for the in class test as well..."* | `slide_006.png` | Deck Page 1 (Title) | **Administrative Hardware Survey Tangent:** Lecturer chatted with students about laptop operating systems (Windows vs Mac) and Canvas test setup procedures before starting Slide 2. Syntax dissolved into casual banter. |
| **`[AMBIGUOUS @ 09:05 – 09:35]`** | *"one to run um questions and then we have option one two three let's try that so option one will be that you wrote uh you ask well in so which one is the most uh correct one..."* | `slide_016.png` | Deck Page 7 (Quiz) | **Classroom Polling Setup Pause:** Verbal mutterings while the instructor configured a multi-choice poll in the online meeting software. |
| **`[AMBIGUOUS @ 45:35 – 47:20]`** | *"be the optimizer... I'll give you some time to think... option A B C... let's see what people think in the chat..."* | `slide_098.png` – `slide_100.png` | Deck Page 29 (Solo Activity) | **Solo Exercise Wait State:** Extended classroom silence and sporadic mutterings while students calculated join algorithm choices in the chat. |
| **`[AMBIGUOUS @ 78:20 – 78:45]`** | *"really slow though... let the polls really really slow yeah i think someone in my self should fix this... which is not really efficient right so let's try again..."* | `slide_191.png` | Deck Page 54 (Quiz) | **Technical Software Glitch Comment:** Instructor complained colloquially about the responsiveness of the classroom polling tool before reading the final quiz questions. |
| **`[AMBIGUOUS @ 84:50 – 85:06]`** | *"we're gonna still go through uh to talk like usual um yep okay well good if you have a question you can send to me on our look I will answer them thank you very much guys bye bye"* | `slide_234.png` – `slide_237.png` | Deck Page 56 / 57 (Thank You) | **Informal Dismissal / Farewell:** Closing pleasantries instructing students to email questions on Outlook. |

