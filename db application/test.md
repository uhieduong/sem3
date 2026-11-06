# Database Indexing & Query Optimization Lab

### Step 1: Create the Database and Table

```sql
CREATE DATABASE IF NOT EXISTS shopping;
USE shopping;

CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  category VARCHAR(50),
  price DECIMAL(10,2),
  stock INT,
  created_at DATETIME
);
```

* **What this does:** Creates a database called `shopping` and an empty table called `products` with 6 columns.
* **Important Detail:** Because `id` is defined as `PRIMARY KEY`, MySQL automatically builds a hidden index on `id` called the **clustered index**. The actual rows of the table are physically stored and sorted by `id` on disk.

---

### Step 2: Create the Generator Procedure
This is a small program inside MySQL that generates 100,000 random products for testing.

Run this entire block together (click inside it, don't highlight anything, and press **Ctrl+Shift+Enter** or the lightning bolt icon):

```sql
DELIMITER $$
CREATE PROCEDURE insert_sample_products()
BEGIN
  DECLARE i INT DEFAULT 0;
  WHILE i < 100000 DO
    INSERT INTO products (name, category, price, stock, created_at)
    VALUES (
      CONCAT('Product', (i + 1)),
      ELT(FLOOR(1 + RAND() * 8), 'Electronics', 'Computer', 'Books', 'Clothing', 'Toys', 'Home', 'Grocery', 'Office'),
      ROUND(RAND() * 1000, 2),
      FLOOR(RAND() * 1000),
      NOW() - INTERVAL FLOOR(RAND() * 365) DAY
    );
    SET i = i + 1;
  END WHILE;
END$$
DELIMITER ;
```

---

### Step 3: Insert the 100,000 Rows (The Fast Way)
The lab asks you to test two ways of inserting data. We will run the optimized version wrapped in a **transaction**:

```sql
START TRANSACTION;
CALL insert_sample_products();
COMMIT;
```

* **Why this is fast:** Normally, MySQL commits every single row to disk one by one (100,000 separate disk writes, taking over a minute). `START TRANSACTION` tells MySQL: *"Hold all 100,000 inserts in memory and write them to disk only once at the end (`COMMIT`)"*. This finishes in 1–2 seconds.

To verify your data, run:
```sql
SELECT COUNT(*) FROM products;
```
* **Expected result:** Exactly `100000`.

---

### Step 4: Learn to Read the Results (`EXPLAIN`)
For each exercise, you run two commands:
1. `EXPLAIN SELECT ...`
2. `EXPLAIN ANALYZE SELECT ...`

#### What to look for in `EXPLAIN`:
* **`type`**: How MySQL accesses rows.
  * `ALL` = **Full Table Scan** (the worst: MySQL had to read all 100,000 rows one by one).
  * `index` = Full index scan (MySQL scans the entire index tree).
  * `range` = Index range scan (MySQL jumps to a starting point in the index and reads a slice).
  * `ref` = Direct lookup (MySQL jumps straight to matching entries).
* **`key`**: Which index MySQL used. If it says `NULL`, it didn't use any index.
* **`Extra`**:
  * `Using index`: **Covering Index** (the best case). The index had all the answers; MySQL never had to touch the actual table rows!
  * `Using filesort`: MySQL had to spend CPU power to manually sort the rows.

#### What to look for in `EXPLAIN ANALYZE`:
Right-click the result cell and choose **Open Value in Viewer**. Read from the bottom indented line up:
* `rows=100000`: How many rows MySQL actually read.
* `actual time=...`: The time taken in milliseconds.

---

### Exercise 1: Count Products in 'Books'

#### 1. Measure without an index:
```sql
EXPLAIN SELECT COUNT(*) FROM products WHERE category = 'Books';
EXPLAIN ANALYZE SELECT COUNT(*) FROM products WHERE category = 'Books';
```
* **What happens:** 
  * `type`: `ALL`.
  * `key`: `NULL`.
  * `rows`: 100,000 (MySQL checked every single item in the store).

#### 2. Create an index on `category`:
```sql
CREATE INDEX idx_category ON products (category);
ANALYZE TABLE products;
```

#### 3. Measure with the index:
```sql
EXPLAIN SELECT COUNT(*) FROM products WHERE category = 'Books';
EXPLAIN ANALYZE SELECT COUNT(*) FROM products WHERE category = 'Books';
```
* **What happens:** 
  * `type`: `ref`.
  * `key`: `idx_category`.
  * `Extra`: `Using index`.
  * `rows`: ~12,500.
* **Why it's faster:** The index is a pre-sorted list of categories. MySQL jumped directly to `'Books'`, counted the ~12,500 entries in the index, and stopped. It never touched the main table (`Using index`).

#### 4. Clean up before the next exercise:
```sql
DROP INDEX idx_category ON products;
```

---

### Exercise 2: `price > 800 AND created_at >= NOW() - INTERVAL 100 DAY`

#### 1. Measure without an index:
```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM products 
WHERE price > 800 AND created_at >= NOW() - INTERVAL 100 DAY;
```
* **Result:** `Table scan, rows=100000`.

#### 2. Test two separate single indexes:
```sql
CREATE INDEX idx_price ON products (price);
CREATE INDEX idx_created ON products (created_at);
ANALYZE TABLE products;

EXPLAIN SELECT COUNT(*) FROM products 
WHERE price > 800 AND created_at >= NOW() - INTERVAL 100 DAY;
```
* **Surprise result:** MySQL often **ignores** both indexes and still does a full table scan (`ALL`)!
* **Why?** If MySQL used `idx_price`, it would find ~20,000 matching products. But to check their dates, it would have to jump to the table 20,000 times. Doing 20,000 random jumps is slower than just scanning the table from top to bottom.

#### 3. Test a composite (two-column) index:
```sql
DROP INDEX idx_created ON products;
CREATE INDEX idx_price_created ON products (price, created_at);
ANALYZE TABLE products;

EXPLAIN ANALYZE SELECT COUNT(*) FROM products 
WHERE price > 800 AND created_at >= NOW() - INTERVAL 100 DAY;
```
* **Result:** Now it uses the index and reads only ~20,000 index entries.
* **Why?** Both the `price` and the `created_at` date live right next to each other inside the index. MySQL checks the date inside the index without visiting the main table!

#### 4. Clean up:
```sql
DROP INDEX idx_price ON products;
DROP INDEX idx_price_created ON products;
```

---

### Exercise 3: `price < 100 OR created_at >= NOW() - INTERVAL 50 DAY`

Notice the **`OR`** keyword instead of `AND`.

#### 1. Why indexes fail on `OR`:
Even if you build indexes on `price` and `created_at`, one single index cannot answer an `OR` query. If MySQL searches the `price` index, products created recently with higher prices are scattered in completely different parts of the database. MySQL is forced to scan the whole table.

#### 2. The Solution: Rewrite as a `UNION`:
```sql
CREATE INDEX idx_price ON products (price);
CREATE INDEX idx_created ON products (created_at);
ANALYZE TABLE products;

EXPLAIN ANALYZE 
SELECT COUNT(*) FROM (
  SELECT id FROM products WHERE price < 100
  UNION
  SELECT id FROM products WHERE created_at >= NOW() - INTERVAL 50 DAY
) AS t;
```
* **Why this works:** The query splits into two separate halves. The top query uses `idx_price`, the bottom query uses `idx_created`, and `UNION` merges them together while removing duplicates.

#### 3. Clean up:
```sql
DROP INDEX idx_price ON products;
DROP INDEX idx_created ON products;
```

---

### Exercise 4: Categories containing the letter 'i' (`LIKE '%i%'`)

```sql
CREATE INDEX idx_category ON products (category);
ANALYZE TABLE products;

EXPLAIN SELECT COUNT(*) FROM products WHERE category LIKE '%i%';
```

* **Look at the result:** 
  * `possible_keys`: `NULL`
  * `key`: `idx_category`
  * `type`: `index`
* **What does this mean?** 
  * Imagine a telephone book sorted alphabetically. If you want names starting with `'C'` (`LIKE 'C%'`), you can flip directly to the 'C' section (`type: range`).
  * If you want names *containing* the letter `'i'` (`LIKE '%i%'`), having the book sorted alphabetically doesn't help you jump anywhere. You must read the whole phone book.
  * MySQL still used `idx_category` only because the index is smaller in file size than the entire table, but it still had to scan every entry in it (`type: index`).

#### Clean up:
```sql
DROP INDEX idx_category ON products;
```

---

### Exercise 5: Top 100 Most Expensive Products (`LIMIT 100`)

#### 1. Measure without an index:
```sql
EXPLAIN SELECT * FROM products ORDER BY price DESC LIMIT 100;
```
* **Notice `Extra`:** It says **`Using filesort`**. MySQL had to pull all 100,000 rows, sort them in temporary memory, and grab the top 100.

#### 2. Create index on `price`:
```sql
CREATE INDEX idx_price ON products (price);
ANALYZE TABLE products;

EXPLAIN SELECT * FROM products ORDER BY price DESC LIMIT 100;
EXPLAIN ANALYZE SELECT * FROM products ORDER BY price DESC LIMIT 100;
```
* **Notice `Extra`:** `Using filesort` is gone! It says **`Backward index scan`**.
* **Why it's instant:** The index is already sorted by price. MySQL starts at the very end (highest price), reads 100 items backward, and stops immediately. It only reads 100 rows instead of 100,000!

#### Clean up:
```sql
DROP INDEX idx_price ON products;
```

