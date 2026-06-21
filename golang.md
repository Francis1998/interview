# Go Interview Questions

## Table of Contents

- [Language Features](#language-features)
- [Concurrency & CSP](#concurrency--csp)
- [Channels & Select](#channels--select)
- [Garbage Collection](#garbage-collection)
- [Memory Allocator](#memory-allocator)
- [Core Types](#core-types)
- [Reflection & Interfaces](#reflection--interfaces)
- [Brain Teasers](#brain-teasers)
- [Large-Scale Data](#large-scale-data)

---

## Language Features

### 1. Go Select Priority (via `default`)

When multiple `case` branches in a `select` are ready, Go **chooses one at random**. Use a `default` branch for non-blocking behavior or to implement priority patterns (busy-poll lower-priority work).

### 2. Key Characteristics of Go

1. **Goroutines + channels** — concurrency via CSP; share memory by communicating.
2. **User-space coroutines** — goroutines are lightweight (~2 KB stack); avoid expensive kernel thread switches.
3. **Multi-core utilization** — goroutines multiplexed onto `GOMAXPROCS` OS threads.
4. Strong standard library, concise syntax, compiled performance comparable to C with faster iteration than dynamic languages.

### 3. Can Struct Instances Be Compared?

- Structs are **comparable** if all fields are comparable.
- **Slices, maps, and functions** are not comparable.
- Comparing **pointers** compares addresses, not pointed-to values.

### 4. `fallthrough` in `switch`

Go `switch` breaks automatically after each case (unlike C). `fallthrough` forces execution into the next case. Cannot be used on the last branch (e.g., `default`).

---

## Concurrency & CSP

### Goroutines

A goroutine is a lightweight, user-scheduled coroutine managed by the Go runtime. Scheduling is done in user space (not by the kernel directly for each goroutine).

**GMP model:**
- **G (Goroutine):** User-level task; `sched` holds context.
- **M (Machine):** OS thread wrapper; count ≈ CPU cores (can grow under blocking).
- **P (Processor):** Logical processor; holds local run queue and cache; count = `GOMAXPROCS` (default: num CPU).

When a goroutine blocks on I/O, the runtime may spin up another M so other goroutines on the same P keep running.

### Waiting for N Goroutines

```go
var wg sync.WaitGroup
for i := 0; i < 100; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        // work
    }()
}
wg.Wait()
```

**Deadlock example:** Two goroutines each lock mutex A then B, but in opposite order:

```go
// Goroutine 1: lock a, then b
// Goroutine 2: lock b, then a
// → deadlock
```

Always acquire locks in a consistent global order.

### CSP Model

**"Do not communicate by sharing memory; share memory by communicating."**

- Channels decouple sender and receiver (anonymous entities).
- Channel send/receive is **synchronous** by default (unbuffered): sender blocks until receiver is ready.

---

## Channels & Select

### Unbuffered Channel

Send blocks until receive completes — "handoff" semantics. Closing immediately after send in the same goroutine without a receiver causes panic.

### Buffered Channel

Send blocks only when buffer is full; receive blocks when empty.

### Map Iteration Order

Maps have **random iteration order**. To sort keys: collect keys into a slice, `sort.Strings(keys)`, then iterate.

---

## Garbage Collection

Go's GC runs concurrently with user code (since Go 1.5 three-color mark-and-sweep).

### Evolution

| Version | Algorithm | Notes |
|---------|-----------|-------|
| Go 1.1 | Mark-sweep | STW during mark; fragmentation |
| Go 1.2 | Three-color marking | White=unvisited, Gray=pending scan, Black=fully scanned |
| Go 1.3 | Write barrier | Prevents floating garbage during concurrent mark |
| Go 1.4 | Assist GC | Allocating goroutines help GC when allocation outpaces sweep |

### GC Cycle (simplified)

![GC cycle](./golang.assets/clip_image002.jpg)

1. **Mark prepare (STW):** Enable write barrier, scan roots setup.
2. **Mark (concurrent):** Scan roots (globals, stacks), drain gray queue.
3. **Mark termination (STW):** Rescan stacks/globals (may have changed during concurrent mark).
4. **Sweep (concurrent):** Reclaim unmarked (white) objects.
5. **Sweep termination:** Finish sweeping before next GC cycle.

Two STW pauses per cycle: mark start and mark termination.

---

## Memory Allocator

Go embeds the runtime in the binary — no separate VM. Memory split into **stack** (function locals, compiler-managed) and **heap** (dynamic allocations, GC-managed).

![GMP and memory](./golang.assets/clip_image002-1610199199949.jpg)

### Hierarchy

| Component | Role |
|-----------|------|
| **mheap** | Global heap; manages spans; source of new pages from OS |
| **mspan** | Linked list of pages (8 KB units); size classes 8 B – 32 KB |
| **mcentral** | Per size-class free lists (scan vs noscan spans) |
| **mcache** | Per-P cache for allocations ≤ 32 KB (lock-free fast path) |
| **arena** | 64 MB (64-bit) virtual memory chunks from OS |

![Span layout](./golang.assets/clip_image004.jpg)

### Allocation Strategies

- **Linear allocator:** Bump pointer; fast but cannot reuse freed blocks individually.
- **Free-list allocator:** Traverse free blocks; variants: first-fit, next-fit, best-fit.
- **Segregated fit (Go's approach):** Size-class free lists → O(1) alloc for small objects.

![Linear allocator](./golang.assets/clip_image006.jpg)

![Free-list allocator](./golang.assets/clip_image008.jpg)

---

## Core Types

### Pointers

- Go has typed pointers; no pointer arithmetic (unlike C).
- `&x` takes address; `*p` dereferences.
- Passing pointers avoids copying large structs.

### Slices

Underlying struct: `{ pointer, len, cap }` referencing a backing array.

- **Append:** If capacity exceeded, allocates new array (typically 2× growth) and copies.
- Slices are **reference types** — mutating elements visible across copies sharing backing array.

### Arrays

- **Value type** — assignment and pass-by-value copy entire array.
- Fixed length at compile time.

---

## Reflection & Interfaces

### `reflect` Package Basics

```go
var a int
t := reflect.TypeOf(a)   // reflect.Type
v := reflect.ValueOf(a)  // reflect.Value
p := reflect.New(t)      // *int allocated on heap
```

Use sparingly — loses compile-time type safety and adds overhead.

### Interface Internals

An interface value holds `(type, data)` pair. Empty interface `interface{}` (or `any`) holds any concrete type.

---

## Brain Teasers

### Poisoned Wine (1000 bottles, 10 mice, 1 week)

Encode bottle numbers in **binary**. Mouse *i* drinks from all bottles whose bit *i* is set. After one week, dead mice encode the poisoned bottle number.

2¹⁰ = 1024 ≥ 1000 → sufficient.

### Pirate Gold (5 pirates, 100 coins, majority vote or thrown overboard)

Work **backwards** from the smallest crew:

| Pirates alive | Pirate 1's offer (to 2,3,4,5) | Reasoning |
|---------------|----------------------------------|-----------|
| 2 | (100, 0) | Pirate 2 accepts anything to survive |
| 3 | (99, 0, 1) | Bribe pirate 3 (gets 0 if only 2 remain) |
| 4 | (99, 0, 1, 0) | Bribe pirate 3 |
| 5 | (98, 0, 1, 0, 1) | Bribe pirates 3 and 5 |

Pirate 1 proposes **(98, 0, 1, 0, 1)** and survives with votes from 1, 3, 5.

---

## Large-Scale Data

### Top-K in a Large Dataset

| Approach | Complexity | Notes |
|----------|------------|-------|
| Min-heap of size K | O(N log K) | Best general approach |
| Quickselect | O(N) average | In-memory only |
| Map-reduce + heap | O(N) distributed | Split, count/hash, merge |

### Deduplication at Scale

- **Bitmap:** If IDs are dense integers, use bit array.
- **2-bit bitmap:** 00= unseen, 01= seen once, 10= duplicate — detect repeats in one pass.
- **Bloom filter:** Probabilistic membership; no false negatives.

### Median of Massive Data

External merge sort or **bucket by hash range** → find bucket containing median → sort only that bucket.
