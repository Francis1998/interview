# Software Engineering Interview Handbook

A curated collection of **backend and infrastructure interview questions** with concise answers. Originally focused on Chinese tech interviews (八股); now fully translated to English and expanded for a broader audience.

Topics span languages, operating systems, databases, networking, caching, algorithms, and system design — the kinds of questions commonly asked for **backend, SRE, and platform engineering** roles.

## Topics

| Topic | File | Coverage |
|-------|------|----------|
| Python | [python.md](./python.md) | GIL, memory, coroutines, decorators, backend workflow |
| Go | [golang.md](./golang.md) | Goroutines, channels, GC, memory allocator, CSP model |
| MySQL | [mysql.md](./mysql.md) | InnoDB vs MyISAM, indexes, transactions, normalization |
| Linux | [linux.md](./linux.md) | Process/memory diagnostics, shell commands, I/O multiplexing |
| Networking | [networking.md](./networking.md) | TCP/UDP, HTTP/TLS, DNS, CDN, security |
| Operating Systems | [operating-systems.md](./operating-systems.md) | Processes, threads, user/kernel mode, IPC, interrupts |
| Redis | [redis.md](./redis.md) | Single-thread model, I/O multiplexing, eviction, LRU |
| Algorithms & DS | [algorithms.md](./algorithms.md) | Sorting, heaps, top-K, hash collisions, red-black trees |
| System Design | [system-design.md](./system-design.md) | Scalability patterns, caching, load balancing, CAP |

## How to Use

1. **Pick your stack** — start with the language and database sections most relevant to your target role.
2. **Cross-reference** — many questions overlap (e.g., TCP appears in both networking and OS sections from different angles).
3. **Practice out loud** — these are interview prompts; rehearse explaining trade-offs, not just definitions.
4. **Contribute** — PRs welcome for new questions, clearer explanations, or additional topics (Kubernetes, distributed systems, etc.).

## Roadmap

- [x] English translation of all existing content
- [x] Expanded Linux, MySQL, and OS sections
- [x] Dedicated Redis and algorithms files
- [ ] Add Kubernetes / cloud-native section
- [ ] Add distributed systems (consensus, sharding, message queues)
- [ ] Add behavioral / HR question templates

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

Content is provided for educational use. External links and diagrams retain their original attribution.
