# Redis Interview Questions

## Table of Contents

- [Why Redis Is Fast](#why-redis-is-fast)
- [Single-Threaded Model](#single-threaded-model)
- [I/O Multiplexing](#io-multiplexing)
- [Data Structures](#data-structures)
- [Persistence](#persistence)
- [Eviction & Memory](#eviction--memory)
- [LRU Implementation](#lru-implementation)
- [Scaling Redis](#scaling-redis)

---

## Why Redis Is Fast

1. **In-memory storage** — microsecond read/write vs millisecond disk.
2. **Single-threaded event loop** — no lock contention on data structures; no context-switch overhead between threads.
3. **Efficient data structures** — SDS strings, quicklist, skiplist+dict for ZSET, etc.
4. **I/O multiplexing** — one thread handles thousands of concurrent connections via `epoll`/`kqueue`.
5. **Simple protocol (RESP)** — minimal parsing overhead.

Bottleneck is usually **memory size** or **network bandwidth**, not CPU — unless running complex Lua scripts or huge values.

---

## Single-Threaded Model

Redis's main command processing is **single-threaded** (since Redis 6, I/O threads can assist with read/write but command execution remains single-threaded by default).

**Trade-off:**
- ✅ No fine-grained locking; atomic operations are natural.
- ❌ Cannot use multiple cores for one instance → run **multiple Redis instances** (cluster or separate DBs) for CPU scaling.

---

## I/O Multiplexing

**Multiplexing:** One thread monitors many sockets; only active ones trigger reads/writes.

Redis uses an event library (ae) wrapping:
- Linux: **epoll**
- macOS/BSD: **kqueue**
- Fallback: **select**

### select vs poll vs epoll

| | select | poll | epoll |
|---|--------|------|-------|
| fd limit | 1024 | Unlimited | Unlimited |
| Ready fd discovery | Scan all O(n) | Scan all O(n) | Return ready list O(k) |
| fd registration | Re-register each call | Re-register each call | Register once, kernel tracks |

**Why multiplexing beats thread-per-connection:** 10,000 idle connections don't need 10,000 blocked threads — one thread waits on epoll, wakes only for active fds.

See [linux.md](./linux.md) for kernel-level details.

---

## Data Structures

| Type | Underlying | Use Case |
|------|------------|----------|
| String | SDS | Counters, cache values, bitmaps |
| Hash | Dict (zipmap for small) | Objects, field maps |
| List | quicklist (linked ziplists) | Queues, timelines |
| Set | Dict (intset for integers) | Tags, unique items |
| Sorted Set | Skiplist + dict | Leaderboards, priority queues |
| Stream | Radix tree + listpack | Event logs, consumer groups |

---

## Persistence

| Mode | Mechanism | Durability | Performance |
|------|-----------|------------|-------------|
| **RDB** | Point-in-time snapshot | May lose last N minutes | Fast restart |
| **AOF** | Append every write | Configurable (everysec fsync) | Slower, larger files |
| **Hybrid** | RDB + AOF (Redis 4+) | Best of both | Recommended production |

---

## Eviction & Memory

When `maxmemory` is reached, Redis evicts keys per policy:

| Policy | Behavior |
|--------|----------|
| `noeviction` | Return errors on writes |
| `allkeys-lru` | Evict any key — LRU |
| `volatile-lru` | Evict keys with TTL — LRU |
| `allkeys-lfu` | Evict least frequently used |
| `volatile-ttl` | Evict key with shortest TTL |

### When Data Grows Too Large

1. Set appropriate **`maxmemory`** and eviction policy.
2. Store **hot data only** — Redis is a cache, not primary store.
3. Use **TTL** on cache entries.
4. **Shard** across Redis Cluster nodes.
5. Compress large values or store references to object storage.

---

## LRU Implementation

Redis approximates LRU (not strict LRU) for O(1) operations.

**Python `OrderedDict` pattern** (common interview answer):

- HashMap: key → LRU node
- Doubly linked list: MRU at head, LRU at tail
- Get/put: O(1) move to head
- Evict: O(1) remove tail

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cache: OrderedDict = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

---

## Scaling Redis

| Strategy | When |
|----------|------|
| **Read replicas** | Read-heavy; eventual consistency OK |
| **Redis Sentinel** | Automatic failover for master-replica |
| **Redis Cluster** | Horizontal sharding; 16,384 hash slots |
| **Client-side sharding** | Simple apps; consistent hashing |

**Session storage:** Redis hash or string with TTL; session ID in HttpOnly cookie.
