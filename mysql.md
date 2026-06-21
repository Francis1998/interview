# MySQL Interview Questions

## Table of Contents

- [Storage Engines](#storage-engines)
- [Indexes & B-Trees](#indexes--b-trees)
- [Transactions & Isolation](#transactions--isolation)
- [SQL Operations](#sql-operations)
- [Normalization](#normalization)
- [Query Optimization](#query-optimization)
- [Replication & Scaling](#replication--scaling)

---

## Storage Engines

### InnoDB vs MyISAM

| Feature | InnoDB | MyISAM |
|---------|--------|--------|
| Index type | Clustered (PK leaf = row data) | Non-clustered (index separate from data) |
| Row-level locking | Yes (via index) | Table-level lock |
| Transactions | ACID supported | Not supported |
| Foreign keys | Supported | Not supported |
| Crash recovery | Redo log | Repair tables |
| Full-text (legacy) | Yes (5.6+) | Yes |

**Clustered index:** Logical and physical order match — table data stored in PK B+ tree leaf pages.

**Secondary index:** Leaf nodes store PK values; requires **回表 (back to table)** lookup for non-covered columns.

---

## Indexes & B-Trees

### Why B-Tree / B+ Tree (not binary tree or hash)?

Disk I/O dominates. Tree height = number of disk reads. B-trees are **wide and shallow** — each node holds many keys (sized to fit one disk page, typically 16 KB).

### B-Tree Properties

1. Each non-leaf node has at most M children (M = order).
2. Root has between 2 and M children.
3. Non-root non-leaf nodes have between ⌈M/2⌉ and M children.
4. All leaves at same depth.
5. k keys split node into k+1 child ranges.

### B+ Tree Properties

1. Non-leaf nodes store **keys only** (no row data) — more keys per page, shorter tree.
2. **All data in leaf nodes**, linked as a doubly linked list → efficient range scans.
3. Non-leaf nodes are index-only copies of subtree boundary keys.
4. Duplicate keys may appear in internal nodes (as separators).

### B-Tree vs B+ Tree

| | B-Tree | B+ Tree |
|---|--------|---------|
| Data location | Any node | Leaves only |
| Range queries | Tree traversal | Leaf linked-list scan |
| Internal node keys | May include data | Index-only |
| MySQL usage | Less common | InnoDB default |

Tutorial with diagrams: [B-Tree vs B+ Tree (blog)](https://www.cnblogs.com/xueqiuqiu/articles/8779029.html)

### Composite (联合) Index — Leftmost Prefix Rule

Index on `(a, b, c, d)`:

- Queries filtering on `a`, or `a,b`, or `a,b,c` use the index.
- **Cannot skip `a`** — `WHERE b = 1` alone won't use this index efficiently.
- Range condition (e.g., `c > 4`) uses index through `a,b,c` but **not `d`** (scan stops at first range column).

**Column order tip:** Put **high-cardinality** columns first (e.g., `user_id` before `gender`).

### Covering Index

Query columns all present in index → no table lookup (Extra: `Using index` in EXPLAIN).

---

## Transactions & Isolation

### ACID

| Property | Meaning |
|----------|---------|
| **Atomicity** | All or nothing (`COMMIT` / `ROLLBACK`) |
| **Consistency** | DB moves from one valid state to another |
| **Isolation** | Concurrent transactions don't interfere improperly |
| **Durability** | Committed data survives crash (redo log) |

### Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|------------|---------------------|--------------|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | No | Possible | Possible |
| REPEATABLE READ (InnoDB default) | No | No | Mostly no (MVCC + gap locks) |
| SERIALIZABLE | No | No | No |

**Anomalies:**
- **Dirty read:** Read uncommitted data from another transaction.
- **Non-repeatable read:** Same row returns different values within one transaction.
- **Phantom read:** Same range query returns different row counts (new rows inserted).
- **Lost update:** Two transactions overwrite each other's changes.

InnoDB REPEATABLE READ uses **MVCC** (Multi-Version Concurrency Control) with undo logs for consistent snapshots.

---

## SQL Operations

### `UNION` vs `UNION ALL`

- **`UNION`:** Combines result sets and **deduplicates** (sort/hash overhead).
- **`UNION ALL`:** Concatenates without dedup — faster when duplicates are acceptable.

Column count and compatible types required; column names from first SELECT used.

### `GROUP BY`

Aggregates rows sharing column values:

```sql
SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5;
```

`WHERE` filters before grouping; `HAVING` filters after aggregation.

---

## Normalization

### Three Normal Forms

1. **1NF — Atomic values:** Each column holds indivisible values (no arrays in a cell).
2. **2NF — No partial dependency:** Non-key columns depend on the **entire** primary key (relevant for composite keys).
3. **3NF — No transitive dependency:** Non-key columns depend only on the primary key, not on other non-key columns.

Denormalization (controlled redundancy) is acceptable for read-heavy workloads when justified by profiling.

---

## Query Optimization

### EXPLAIN

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123 AND status = 'paid';
```

Key columns: `type` (access method), `key` (index used), `rows` (estimated scan), `Extra` (`Using index`, `Using filesort`, `Using temporary`).

### Common Slow Query Fixes

1. Add or adjust indexes (watch leftmost prefix).
2. Avoid `SELECT *` — use covering indexes.
3. Replace `OR` with `UNION` when it prevents index use.
4. Paginate with keyset/cursor pagination instead of large `OFFSET`.
5. Avoid functions on indexed columns (`WHERE YEAR(created_at) = 2024` → range on `created_at`).

---

## Replication & Scaling

### Master-Slave Replication

- **Binary log (binlog)** on master → relay log on replica → apply SQL.
- Async by default; semi-sync for durability trade-off.
- Replicas serve read traffic; writes go to master.

### Sharding (when single instance isn't enough)

- **Horizontal:** Split rows by shard key (user_id mod N).
- **Vertical:** Split tables/columns by domain.
- Challenges: cross-shard joins, rebalancing, global IDs.

See [system-design.md](./system-design.md) for broader scaling patterns.
