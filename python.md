# Python Interview Questions

## Table of Contents

- [Language Basics](#language-basics)
- [Memory & Concurrency](#memory--concurrency)
- [Data Structures & Algorithms](#data-structures--algorithms)
- [Operating Systems (Python context)](#operating-systems-python-context)
- [Networking (Python context)](#networking-python-context)
- [Databases (Python context)](#databases-python-context)
- [Backend Engineering Workflow](#backend-engineering-workflow)
- [Supplementary Topics](#supplementary-topics)

---

## Language Basics

### 1. `type()` vs `isinstance()`

- **`type(obj)`** returns the exact type of an object. It does **not** treat a subclass as an instance of its parent: `type(sub) is Parent` → `False`.
- **`isinstance(obj, cls)`** checks inheritance: `isinstance(sub, Parent)` → `True`.

Use `isinstance()` when you care about interface/behavior; use `type()` when you need the concrete class.

### 2. Global Interpreter Lock (GIL)

**What it is:** The GIL is a feature of **CPython** (the default interpreter), not Python the language. It ensures only one thread executes Python bytecode at a time in a single process.

**Why it exists:** Protects CPython's internal state (reference counts, object structures) from race conditions without fine-grained locking on every object.

**Limitation:** CPU-bound multi-threaded Python cannot fully utilize multiple cores in one process — threads contend for the GIL.

**When the GIL is released:**
1. Before blocking I/O system calls (so other threads can run during I/O wait).
2. In Python 3.x, after a time slice threshold, the current thread may release the GIL.

**Mitigations:**
- **Multiprocessing** — separate processes, each with its own GIL → true parallelism on multiple cores.
- **Async I/O / coroutines** — single-threaded concurrency for I/O-bound work.
- Alternative interpreters (Jython, PyPy with different models).

**Interview scenario:** Single-threaded vs multi-threaded web scraper?
- **I/O-bound scraping:** Multi-threading helps — threads release the GIL during network I/O, so other threads progress.
- **CPU-bound parsing:** Multi-threading does **not** help much; use multiprocessing or native extensions.

### 3. Python Memory Management

**Garbage collection (three layers):**
1. **Reference counting** — primary mechanism; object freed when refcount hits 0. Cannot handle circular references alone.
2. **Mark-and-sweep** — detects cycles; higher maintenance cost; may leave transient dangling references during collection.
3. **Generational GC** — objects divided into generations 0, 1, 2; long-lived objects collected less often (more efficient).

**Memory pool (pymalloc):**
- Pre-allocates fixed-size blocks to reduce fragmentation.
- Objects **≤ 256 KB**: allocated from pymalloc pools.
- Objects **> 256 KB**: allocated via system `malloc`.
- On deallocation, small blocks return to the pool rather than immediately calling `free`, reducing allocator churn.

### 4. Python Coroutines

Coroutines are **cooperative**, user-scheduled functions that can suspend and resume at `await` points.

| Feature | Thread | Coroutine |
|---------|--------|-----------|
| Scheduling | OS preemptive | Event loop cooperative |
| Overhead | ~MB stack, kernel switches | ~KB, no kernel switch |
| Best for | Mixed CPU/I/O (with GIL caveats) | High-concurrency I/O |

Built on generators (`yield`) → `async`/`await` (PEP 492). Frameworks: `asyncio`, `aiohttp`, FastAPI.

### 5. String Storage and Slicing

- CPython strings are **immutable** sequences of Unicode code points (PEP 393 flexible representation).
- **Slicing creates a new string** (copy of the sliced portion) — effectively a shallow copy of the character data.
- Assignment to a slice variable does not mutate the original string.

---

## Memory & Concurrency

See also [operating-systems.md](./operating-systems.md) for process/thread fundamentals.

---

## Data Structures & Algorithms

See [algorithms.md](./algorithms.md) for detailed coverage of sorting, heaps, and top-K problems.

### Quick Reference: Time Complexities

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Binary search | O(1) | O(log n) | O(log n) | O(1) |
| Hash table lookup | O(1) | O(1) | O(n) | O(n) |

### Red-Black Tree (summary)

Self-balancing BST with O(log n) insert/search/delete. Properties:
1. Every node is red or black.
2. Root and leaves (NIL) are black.
3. Red nodes have black children.
4. Every path from node to leaves has the same number of black nodes.

Used in Python's `OrderedDict` (before 3.7 dict ordering), Java `TreeMap`, Linux CFS scheduler.

---

## Operating Systems (Python context)

### Parallelism vs Concurrency

- **Parallelism:** Multiple CPUs execute multiple tasks simultaneously (true simultaneous execution).
- **Concurrency:** One CPU interleaves multiple tasks (appears simultaneous due to fast context switching).

### Mutex (Lock)

Ensures only one thread modifies shared data at a time, preventing race conditions.

### Process vs Thread

| | Process | Thread |
|---|---------|--------|
| Unit of | Resource allocation | CPU scheduling |
| Memory | Separate address space | Shared within process |
| Overhead | High (fork, IPC) | Low |
| Crash isolation | Strong | Weak (one thread crash can kill process) |

### Multiprocessing vs Multithreading

- **Multiprocessing:** Bypasses GIL; best for CPU-bound Python.
- **Multithreading:** Best for I/O-bound Python (GIL released during I/O).

---

## Networking (Python context)

See [networking.md](./networking.md) for full TCP/HTTP/DNS coverage.

---

## Databases (Python context)

See [mysql.md](./mysql.md) for index structures and transaction isolation.

### SQL vs NoSQL (when asked)

| | Relational (MySQL, PostgreSQL) | NoSQL (Redis, MongoDB) |
|---|-------------------------------|------------------------|
| Schema | Fixed, normalized | Flexible / schemaless |
| Scaling | Vertical + read replicas | Horizontal sharding |
| Transactions | ACID (InnoDB) | Varies (Redis: limited) |
| Use case | Complex queries, consistency | Caching, documents, high write throughput |

---

## Backend Engineering Workflow

Typical backend developer responsibilities across a feature lifecycle:

1. Participate in product/requirements review.
2. Align with frontend on **API contracts** (OpenAPI/REST/gRPC).
3. Design **database schema** changes and migrations.
4. Evaluate **third-party services** (payment, auth, messaging).
5. Implement business logic and unit tests.
6. Self-test end-to-end flows.
7. Coordinate **integration testing** with frontend/mobile.
8. Hand off to PM for acceptance.
9. Support QA and fix bugs.
10. Deploy and monitor in production.

---

## Supplementary Topics

### Decorators

A decorator wraps a function to extend behavior **without modifying** the function body or call sites.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # pre/post logic
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet():
    print("hello")
```

`@my_decorator` is equivalent to `greet = my_decorator(greet)`.

**Pitfall:** Wrapped function's `__name__` and `__doc__` become the wrapper's. Fix with `functools.wraps`:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

A decorator + nested wrapper that closes over outer scope forms a **closure** (nested function, returned function, free variable reference).

### Context Managers

`with` statement uses `__enter__` / `__exit__` for resource cleanup (files, locks, DB connections). Implement manually or via `@contextmanager`.

### `*args` and `**kwargs`

- `*args` — tuple of positional arguments.
- `**kwargs` — dict of keyword arguments.
- Used for flexible APIs, decorators, and forwarding calls.

### List vs Tuple vs Set vs Dict

| Type | Mutable | Ordered | Duplicates |
|------|---------|---------|------------|
| list | Yes | Yes (3.7+) | Yes |
| tuple | No | Yes | Yes |
| set | Yes | No | No |
| dict | Yes | Yes (3.7+) | Keys unique |
