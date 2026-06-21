# Operating Systems Interview Questions

## Table of Contents

- [Processes & Threads](#processes--threads)
- [Concurrency Concepts](#concurrency-concepts)
- [User Mode & Kernel Mode](#user-mode--kernel-mode)
- [Inter-Process Communication](#inter-process-communication)
- [Process State Transitions](#process-state-transitions)
- [I/O Models](#io-models)
- [Design Patterns (brief)](#design-patterns-brief)
- [HTTP Status Codes (reference)](#http-status-codes-reference)
- [Cookie vs Session](#cookie-vs-session)

---

## Processes & Threads

### Process vs Thread

| | Process | Thread |
|---|---------|--------|
| Definition | Unit of **resource allocation** | Unit of **CPU scheduling** |
| Address space | Independent | Shared within process |
| Context switch cost | High (TLB flush, separate memory) | Low (shared memory) |
| Crash impact | Isolated (usually) | Can terminate entire process |
| Creation | `fork()`, `exec()` | `pthread_create()` |

A process contains one or more threads. Threads share code, data, and open files but have private stacks and registers.

### Multiprocess vs Multithread

- **Multiprocess:** Strong isolation, higher overhead, true parallelism (separate address spaces).
- **Multithread:** Shared memory, lower overhead, requires synchronization (mutexes, semaphores).

For **I/O-bound server work**, threads/coroutines excel — most time spent waiting, not computing.

---

## Concurrency Concepts

### Parallelism vs Concurrency

- **Parallelism:** Multiple CPUs execute tasks simultaneously.
- **Concurrency:** Tasks interleave on one or more CPUs; logical simultaneity via time-slicing.

### Mutex vs Semaphore

- **Mutex:** Binary lock; one owner at a time; typically same thread acquires and releases.
- **Semaphore:** Counting lock; controls access to N identical resources; can signal across threads.

### Deadlock Conditions (all four required)

1. Mutual exclusion
2. Hold and wait
3. No preemption
4. Circular wait

**Prevention:** Lock ordering, timeouts, try-lock, or eliminate one condition.

---

## User Mode & Kernel Mode

### Why Two Modes?

Protect the OS and hardware from buggy or malicious user programs. User code cannot directly access physical memory or device registers.

### Memory Layout

User programs see **virtual addresses** mapped to physical RAM by the MMU. User space = lower addresses; kernel space = upper (on typical 64-bit layouts).

### Entering Kernel Mode

1. **System call** — intentional (e.g., `read()`, `write()`, `syscall` instruction).
2. **Exception** — page fault, divide by zero, illegal instruction.
3. **Hardware interrupt** — timer tick, NIC packet, disk completion.

User programs **cannot** invoke syscalls directly without going through the libc wrapper or language runtime (e.g., Go's `syscall` package, Python's C extensions).

---

## Inter-Process Communication

| Mechanism | Scope | Notes |
|-----------|-------|-------|
| **Pipe** | Related processes | Unidirectional byte stream |
| **Named pipe (FIFO)** | Unrelated processes | Filesystem path |
| **Message queue** | System-wide | Structured messages, kernel-persisted |
| **Shared memory** | Fastest | Requires separate synchronization |
| **Semaphore** | Sync primitive | P/V operations for mutual exclusion |
| **Socket** | Local or network | Only option for cross-machine IPC |
| **Signals** | Async notification | Limited data payload |

### Thread Communication

Threads in the same process communicate via:
- Shared memory (with mutex/lock protection)
- Condition variables
- Semaphores

---

## Process State Transitions

```
        +----------+
        |   NEW    |
        +----+-----+
             | admit
             v
        +----------+  interrupt   +------------+
   +--->|  READY   |<-------------|  WAITING   |
   |    +----+-----+              +-----+------+
   |         | dispatch                ^ I/O or event
   |         v                         | complete
   |    +----------+  I/O or event     |
   |    | RUNNING  |-------------------+
   |    +----+-----+
   |         | exit
   |         v
   |    +----------+
   +----| TERMINATED|
        +----------+
```

---

## I/O Models

| Model | Behavior | Example |
|-------|----------|---------|
| **Blocking I/O** | Thread waits until data ready | Default `read()` |
| **Non-blocking I/O** | Returns immediately; poll/retry | `O_NONBLOCK` |
| **I/O multiplexing** | One thread watches many fds | `select`, `poll`, `epoll` |
| **Signal-driven I/O** | Kernel signals when ready | `SIGIO` |
| **Async I/O (AIO)** | Kernel completes I/O, notifies later | Linux `io_uring` |

See [linux.md](./linux.md) for `select`/`poll`/`epoll` comparison.

### Connection-Oriented vs Connectionless

- **Connection-oriented (TCP):** State maintained; reliable, ordered delivery.
- **Connectionless (UDP):** Each datagram independent; lower latency, no setup.

---

## Design Patterns (brief)

### Singleton

One instance, global access point. In Python, use module-level object or `__new__` guard. Prefer dependency injection in testable code.

### Factory

Creator decides concrete class at runtime without exposing instantiation logic to client.

### Abstract Factory

Family of related products without specifying concrete classes — e.g., `ShapeFactory` vs `ColorFactory`.

---

## HTTP Status Codes (reference)

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 301 | Permanent redirect |
| 302 | Temporary redirect |
| 304 | Not Modified (cache valid) |
| 400 | Bad Request (malformed syntax / validation mismatch) |
| 401 | Unauthorized (authentication required) |
| 403 | Forbidden (authenticated but no permission) |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 408 | Request Timeout |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 502 | Bad Gateway (upstream invalid response) |
| 503 | Service Unavailable (maintenance/overload) |
| 504 | Gateway Timeout (upstream slow) |

### GET vs POST

| | GET | POST |
|---|-----|------|
| Visibility | Params in URL | Body (not in URL) |
| Caching | Cacheable | Typically not |
| Idempotency | Yes | No (creates side effects) |
| Size limit | URL length (~2 KB practical) | Much larger |
| Use | Read/fetch | Create/submit data |

Other methods: **PUT** (idempotent update/replace), **DELETE** (remove), **PATCH** (partial update), **OPTIONS** (CORS preflight, server capabilities), **TRACE** (echo request — rarely used).

---

## Cookie vs Session

| | Cookie | Session |
|---|--------|---------|
| Storage | Client browser | Server (memory, Redis, DB) |
| Capacity | ~4 KB per cookie | Limited by server store |
| Data type | ASCII strings | Any serializable type |
| Security | Visible to client; use `HttpOnly`, `Secure`, `SameSite` | Opaque session ID in cookie |
| Server load | None | Lookup on each request |
| Use case | Preferences, tracking, JWT | Server-side auth state |

For authentication, prefer **HttpOnly secure cookies** or **Authorization headers** with short-lived tokens.
