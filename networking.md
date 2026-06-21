# Computer Networking Interview Questions

Part of the [Software Engineering Interview Handbook](./README.md).

## Table of Contents
- [OSI & TCP/IP Model](#osi--tcpip-model)
- [TCP Deep Dive](#tcp-deep-dive)
- [HTTP / HTTPS](#http--https)
- [DNS](#dns)
- [Load Balancing & CDN](#load-balancing--cdn)
- [Security](#security)

---

## OSI & TCP/IP Model

### OSI 7-Layer Model

| Layer | Name | Protocol Examples | Data Unit |
|-------|------|-------------------|-----------|
| 7 | Application | HTTP, FTP, SMTP, DNS | Message |
| 6 | Presentation | TLS/SSL, JPEG, ASCII | — |
| 5 | Session | NetBIOS, RPC | — |
| 4 | Transport | TCP, UDP | Segment |
| 3 | Network | IP, ICMP, ARP | Packet |
| 2 | Data Link | Ethernet, WiFi (802.11) | Frame |
| 1 | Physical | Fiber, copper, radio | Bit |

### TCP/IP 4-Layer Model (Practical)

| Layer | Maps to OSI | Examples |
|-------|-------------|---------|
| Application | 5-7 | HTTP, SMTP, DNS |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP |
| Network Access | 1-2 | Ethernet, WiFi |

---

## TCP Deep Dive

### Three-Way Handshake

```
Client                    Server
  |                          |
  |---- SYN (seq=x) -------->|
  |                          |
  |<--- SYN-ACK (seq=y, ack=x+1) --|
  |                          |
  |---- ACK (ack=y+1) ------>|
  |                          |
  |=== Connection Established ===|
```

**Purpose**: agree on initial sequence numbers (ISN) for both directions.

### Four-Way Termination (FIN handshake)

```
Client                    Server
  |                          |
  |---- FIN ----------------->|   Client done sending
  |<--- ACK ------------------|
  |                          |   Server may still be sending
  |<--- FIN ------------------|   Server done sending
  |---- ACK ----------------->|
  |                          |
  Client waits 2*MSL (TIME_WAIT) before closing
```

**Why TIME_WAIT?** Ensure the last ACK reaches the server; prevent old packets from corrupting a new connection on the same port.

### TCP vs UDP

| | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | Guaranteed delivery, retransmission | Best-effort, no retransmission |
| Ordering | In-order delivery | May arrive out of order |
| Flow control | Yes (sliding window) | No |
| Congestion control | Yes (AIMD, slow start) | No |
| Overhead | Higher (20-byte header min) | Lower (8-byte header) |
| Latency | Higher | Lower |
| Use cases | HTTP, SMTP, FTP, SSH | DNS, VoIP, video streaming, gaming |

### TCP Flow Control & Congestion Control

**Flow Control** (receiver limits sender):
- Receiver advertises its buffer size as `rwnd` (receive window)
- Sender cannot have more than `rwnd` bytes in-flight

**Congestion Control** (sender detects network congestion):
- **Slow Start**: begin with `cwnd = 1 MSS`, double per RTT until threshold
- **Congestion Avoidance**: linear increase once threshold reached
- **Fast Retransmit**: if 3 duplicate ACKs → packet lost, retransmit immediately (don't wait for timeout)

---

## HTTP / HTTPS

### HTTP/1.1 vs HTTP/2 vs HTTP/3

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---------|----------|--------|--------|
| Transport | TCP | TCP | QUIC (UDP) |
| Multiplexing | No (HOL blocking) | Yes (streams) | Yes (no HOL) |
| Header compression | No | HPACK | QPACK |
| Server Push | No | Yes | Yes |
| TLS | Optional | Required in practice | Built-in |

**Head-of-Line Blocking**: HTTP/1.1 — one request blocks the pipeline. HTTP/2 — fixes at HTTP layer but TCP still has HOL. HTTP/3/QUIC — fixes at transport layer.

### HTTP Status Codes (Key Groups)

| Range | Category | Key codes |
|-------|----------|-----------|
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirect | 301 Permanent, 302 Temporary, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Too Many Requests |
| 5xx | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

### HTTPS / TLS Handshake (TLS 1.3)

```
Client                      Server
  |                            |
  |-- ClientHello (ciphers) -->|
  |<- ServerHello, Cert, Key --|
  |  (verify cert via CA)      |
  |-- Finished (client key) -->|
  |<-- Finished (server key) --|
  |====== Encrypted Data ======|
```

TLS 1.3 reduced round trips from 2 to 1 (1-RTT), and supports 0-RTT for resumption.

---

## DNS

### DNS Resolution Process

```
Browser → OS cache → /etc/hosts → Recursive resolver (ISP/8.8.8.8)
  → Root nameserver → TLD nameserver (.com) → Authoritative nameserver
  → Returns A record (IP address)
```

### DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| A | Domain → IPv4 | `api.example.com → 1.2.3.4` |
| AAAA | Domain → IPv6 | `api.example.com → 2001:db8::1` |
| CNAME | Alias to another domain | `www → example.com` |
| MX | Mail exchange | `@ → mail.example.com` (priority 10) |
| TXT | Arbitrary text | SPF, DKIM verification |
| NS | Nameserver for zone | `example.com → ns1.cloudflare.com` |
| SOA | Zone authority metadata | Serial number, refresh interval |

### DNS TTL & Caching

- TTL (Time to Live): how long resolvers cache the record
- Low TTL (60-300s): faster failover, more DNS queries
- High TTL (86400s): fewer queries, slower propagation of changes

**Best practice for migrations**: lower TTL to 60s 24 hours before changing the record.

---

## Load Balancing & CDN

### CDN (Content Delivery Network)

- Static assets (JS, CSS, images) served from edge nodes geographically close to users
- Reduces latency (100ms → 5ms for cached content)
- Absorbs DDoS traffic at edge before it hits origin

**Cache control headers**:
```
Cache-Control: public, max-age=31536000, immutable   ← versioned assets
Cache-Control: no-cache                               ← always revalidate
Cache-Control: private, max-age=300                  ← user-specific content
```

### Anycast Routing

Used by Cloudflare, AWS Route53 — same IP announced from multiple locations worldwide. Client's request automatically routes to nearest PoP.

---

## Security

### Common Network Attacks

| Attack | How | Defense |
|--------|-----|---------|
| DDoS | Flood with traffic | Rate limiting, CDN, Anycast |
| Man-in-the-Middle | Intercept unencrypted traffic | HTTPS/TLS, HSTS |
| DNS Spoofing | Return fake DNS records | DNSSEC |
| SYN Flood | Half-open TCP connections exhaust server | SYN cookies |
| SQL Injection | Embed SQL in inputs | Parameterized queries, ORM |
| XSS | Inject scripts into web pages | CSP headers, input sanitization |
| CSRF | Trick browser to make authenticated requests | CSRF tokens, SameSite cookies |

### CORS (Cross-Origin Resource Sharing)

```
Origin: https://app.example.com
→ requests → https://api.example.com
```

Browser blocks by default (same-origin policy). Server opts-in via:
```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Content-Type, Authorization
```

**Preflight**: for non-simple requests (PUT, DELETE, custom headers), browser sends OPTIONS first.

### SSL Pinning

Mobile apps embed the server's certificate (or public key hash) and reject TLS connections from certificates not matching — prevents MITM even with compromised CA.
