# System Design Interview Questions

## Table of Contents

- [Framework for Answering](#framework-for-answering)
- [Scalability Patterns](#scalability-patterns)
- [Caching](#caching)
- [Load Balancing](#load-balancing)
- [Databases at Scale](#databases-at-scale)
- [Message Queues](#message-queues)
- [CAP & Consistency](#cap--consistency)
- [Common System Designs](#common-system-designs)
- [Reliability & Observability](#reliability--observability)

---

## Framework for Answering

1. **Clarify requirements** — functional (features), non-functional (QPS, latency, availability, consistency).
2. **Estimate scale** — DAU, read/write ratio, storage growth, bandwidth.
3. **High-level design** — boxes and arrows; client → LB → app → cache → DB.
4. **Deep dive** — pick 1–2 components; data model, APIs, bottlenecks.
5. **Trade-offs** — what you'd optimize first; what breaks at 10× scale.

---

## Scalability Patterns

| Pattern | Use When |
|---------|----------|
| **Vertical scaling** | Early stage; simpler ops |
| **Horizontal scaling** | Need more throughput than one machine |
| **Stateless app servers** | Easy scale-out behind LB |
| **Read replicas** | Read-heavy; eventual consistency OK |
| **Sharding** | Write-heavy or data exceeds single node |
| **CDN** | Static assets; global latency |
| **Async processing** | Decouple slow work (email, analytics) |

---

## Caching

### Cache Strategies

| Strategy | Behavior | Risk |
|----------|----------|------|
| **Cache-aside** | App reads cache; on miss, read DB, populate cache | Cache stampede |
| **Write-through** | Write to cache + DB together | Write latency |
| **Write-behind** | Write cache; async flush to DB | Data loss on crash |
| **Read-through** | Cache layer fetches from DB on miss | Cache layer complexity |

### Cache Invalidation

- **TTL** — simple; stale data window.
- **Event-driven** — invalidate on write (pub/sub, CDC).
- **Version keys** — bump version on schema/data change.

See [redis.md](./redis.md) for Redis-specific eviction and LRU.

---

## Load Balancing

| Algorithm | Behavior |
|-----------|----------|
| Round robin | Equal rotation |
| Weighted round robin | More traffic to stronger nodes |
| Least connections | Route to least busy server |
| Consistent hashing | Minimal remapping when nodes added/removed |
| IP hash | Sticky sessions by client IP |

**L4 vs L7:** L4 (TCP) faster; L7 (HTTP) can route by path, headers, cookies.

See [networking.md](./networking.md) for CDN and Anycast.

---

## Databases at Scale

### When to Shard

- Single instance CPU/IO saturated.
- Storage exceeds disk capacity.
- Need geographic data locality.

**Shard key selection:** High cardinality, even distribution, aligns with query patterns (avoid cross-shard joins).

### SQL vs NoSQL at Scale

- **SQL + sharding (Vitess, Citus):** Strong consistency needs, complex queries.
- **NoSQL (Cassandra, DynamoDB):** Massive write throughput, flexible schema, tunable consistency.

See [mysql.md](./mysql.md) for indexes, replication, and isolation levels.

---

## Message Queues

Decouple producers and consumers; absorb traffic spikes; enable retry.

| System | Model | Notes |
|--------|-------|-------|
| Kafka | Log-based, partitioned | High throughput, replay |
| RabbitMQ | Broker, exchanges | Flexible routing |
| SQS | Managed queue | Simple, at-least-once |
| Redis Streams | In-memory log | Lightweight, low latency |

**Delivery guarantees:** at-most-once, at-least-once (idempotent consumers), exactly-once (hard; Kafka transactions).

---

## CAP & Consistency

**CAP theorem:** In a partition, choose **Consistency** or **Availability** (Partition tolerance is mandatory in distributed systems).

| Model | Example | Trade-off |
|-------|---------|-----------|
| Strong consistency | Spanner, etcd | Higher latency |
| Eventual consistency | DynamoDB, Cassandra | Stale reads possible |
| Causal consistency | Middle ground | Ordered related events |

**PACELC extension:** If no partition, choose latency vs consistency.

---

## Common System Designs

### URL Shortener

- Hash or base62 encode ID → short URL.
- Key-value store (Redis) for hot URLs; SQL for analytics.
- Read-heavy → cache + CDN for redirects.

### Rate Limiter

- **Token bucket** or **sliding window** in Redis.
- Key: `rate:{user_id}:{window}` with INCR + EXPIRE.

### News Feed / Timeline

- **Fan-out on write:** Precompute feeds (fast read, slow write for celebrities).
- **Fan-out on read:** Merge at read time (simple, slow for high-follower users).
- Hybrid: fan-out on write for normal users; fan-out on read for celebrities.

### Chat / Messaging

- WebSocket or long-polling for delivery.
- Message store partitioned by conversation ID.
- Presence via heartbeat + Redis pub/sub.

---

## Reliability & Observability

### SLI / SLO / SLA

- **SLI:** Metric (availability, latency p99).
- **SLO:** Target (99.9% availability).
- **SLA:** Contract with penalties.

### Key Metrics

- **RED:** Rate, Errors, Duration (requests).
- **USE:** Utilization, Saturation, Errors (resources).

### Failure Handling

- Retries with exponential backoff + jitter.
- Circuit breaker (stop calling failing dependency).
- Bulkheads (isolate thread pools per dependency).
- Graceful degradation (serve cached/stale data).

### TCP TIME_WAIT (ops crossover)

High `TIME_WAIT` from short-lived client connections (scrapers, load tests). Mitigate: connection pooling, tune `tcp_tw_reuse` / `tcp_fin_timeout` (Linux), or fix missing `close()` in application code.

See [networking.md](./networking.md) for TCP lifecycle details.
