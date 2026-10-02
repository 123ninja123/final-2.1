# Sentryl — Platform Security Model & Defense Architecture

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Document Purpose:** Formal technical specification of Sentryl's security boundaries, threat model, isolation mechanisms, and cryptographic integrity assurances.

---

## 1. Threat Model & Trust Boundaries

```
                 UNTRUSTED ZONE                              SENTRYL SECURE ANALYSIS PLANE
┌──────────────────────────────────────────────┐        ┌──────────────────────────────────────────────────┐
│ Adversary-Controlled Data Sources:           │        │ 1. STREAMING INGESTION FIREWALL                  │
│ • Raw RFC 822 MIME Streams                   │───────>│    • 10MB Chunked Stream Ceiling (HTTP 413)      │
│ • Spoofed RFC 5322 Email Headers             │        │    • MIME Depth Cap: 100 parts                   │
│ • Malicious URLs & Phishing Links            │        │    • Attachment Cap: 20 files                    │
│ • Double-Extension Malware Droppers          │        └────────────────────────┬─────────────────────────┘
│ • Prompt-Injection & Evasion Payloads        │                                 │ Sanitized RFC Stream
└──────────────────────────────────────────────┘                                 ▼
                                                        ┌──────────────────────────────────────────────────┐
                                                        │ 2. SAFE STATIC ANALYSIS CORE (Zero Outbound Net) │
                                                        │    • Static URL Lexical Inspector                │
                                                        │    • Deterministic Header & SPF/DKIM Analyzer    │
                                                        │    • Local Levenshtein Domain Spoofing Engine    │
                                                        │    • In-Memory PE / File Hash Calculator         │
                                                        │    • Local Dual-Branch ML Classifier             │
                                                        └────────────────────────┬─────────────────────────┘
                                                                                 │
                                                                                 ▼
                                                        ┌──────────────────────────────────────────────────┐
                                                        │ 3. CRYPTOGRAPHIC EVIDENCE VAULT                  │
                                                        │    • SHA-256 Acquisition Digest                  │
                                                        │    • Canonical JSON Keyed HMAC-SHA256 Seal       │
                                                        │    • Chronological Chain-of-Custody Timestamps   │
                                                        └────────────────────────┬─────────────────────────┘
                                                                                 │
                                                                                 ▼
     UNTRUSTED ADVISORY PLANE (Optional)                ┌──────────────────────────────────────────────────┐
┌──────────────────────────────────────────────┐        │ 4. DETERMINISTIC DECISION PLANE                  │
│ External LLM (Gemini API):                   │<───────│    • Bounded 0–100 Mathematical Risk Formula     │
│ • Encapsulated in <UNTRUSTED_DATA> tags      │        │    • Attachment Critical Floor Override (≥65)    │
│ • ZERO control over numerical score or IOCs  │───────>│    • Dual-View Payload Generation                │
│ • Graceful fallback to deterministic engine  │        │    • Bounded LRU/TTL In-Memory Cache             │
└──────────────────────────────────────────────┘        └──────────────────────────────────────────────────┘
```

---

## 2. Safe Static URL Isolation Model

### 2.1 The Architectural Decision
Many legacy security tools attempt dynamic "URL detonation" by launching headless browsers (e.g., Puppeteer, Selenium) to screenshot or crawl destination landing pages. In a production gateway or lightweight triage tool, this introduces severe vulnerabilities:
1. **Server-Side Request Forgery (SSRF):** Malicious URLs pointing to internal metadata services (e.g., `http://169.254.169.254/latest/meta-data/`) can compromise cloud infrastructure.
2. **Browser Exploits & Zero-Days:** Dynamically rendering malicious web code exposes the scanning server to sandbox escape exploits.
3. **Attacker Beaconing & Tracking:** Requesting an attacker's unique URL alerts the threat actor that the phishing email reached an active recipient and scanning infrastructure.

### 2.2 Sentryl's Static Inspection Architecture
Sentryl enforces **100% Safe Static URL Analysis** (`backend/services/url_checker.py`):
- **Zero Network I/O:** URLs are inspected exclusively via string parsing, regex decomposition, and mathematical entropy metrics without opening TCP sockets or resolving external DNS.
- **Raw IP Hostname Detection:** Rejects and flags URLs using numerical IPv4 addresses (`http://185.220.101.5/`) designed to bypass domain reputation blocklists.
- **Open Redirect Parameter Identification:** Evaluates query parameters for common redirect keys (`?redirect=`, `?url=`, `?next=`, `?dest=`) that attackers use to bounce victims off legitimate domains to phishing sites.
- **Shannon Lexical Entropy:** Computes the mathematical randomness of path and query tokens ($H(X) = -\sum P(x) \log_2 P(x)$) to detect machine-generated algorithmically generated domains (DGA) and hex-encoded tracking hashes.
- **Credential Path Harvesting:** Scans URL paths for sensitive tokens (`/login`, `/signin`, `/verify`, `/account-update`, `/wp-admin`).

---

## 3. Denial-of-Service & Memory Protection (Anti-DoS)

To prevent resource exhaustion from parser bombs, decompression loops, or oversized payloads, Sentryl implements multi-layered defensive limits:

### 3.1 Streaming Ingestion Ceiling
In `backend/routers/scan.py`:
- File uploads to `/api/analyze-eml` are read in **64-kilobyte streaming chunks**.
- Cumulative byte size is tracked in real-time against `MAX_EML_SIZE_BYTES = 10 * 1024 * 1024` (10 Megabytes).
- If the stream exceeds 10MB, Sentryl aborts immediately with **HTTP 413 Payload Too Large** before allocating memory buffers.

### 3.2 MIME Recursion & Attachment Bounds
In `backend/services/eml_parser.py`:
- **Max MIME Parts (`MAX_MIME_PARTS = 100`):** Protects against deeply nested MIME multipart bombs designed to cause stack overflows.
- **Max Attachments (`MAX_ATTACHMENTS = 20`):** Limits attachment iteration to prevent CPU exhaustion.
- **Attachment In-Memory Buffer Limit (`MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024`):** Individual attachments are bounded to 5MB for in-memory SHA-256 and PE header inspection. Content buffers are released immediately after hashing.

### 3.3 Cache Memory Bounds (Anti-Memory Leak)
In `backend/services/report_store.py`:
- The in-memory analysis cache is capped at `MAX_REPORTS_CACHE = 500`.
- Implements **FIFO / LRU eviction**: When capacity is reached, the oldest entries are evicted automatically.
- Implements **Time-To-Live (TTL)**: Records older than `REPORT_CACHE_TTL_SECONDS = 86400` (24 hours) are purged upon query.

---

## 4. Cryptographic Evidence Integrity Model

### 4.1 Server-Side Keyed HMAC-SHA256
In `backend/services/evidence_vault.py`:
- **Acquisition Digest:** At the millisecond of ingestion, the raw RFC 822 payload is hashed with SHA-256.
- **Keyed Tamper Seal:** A cryptographically secure tamper seal is generated using HMAC-SHA256, keyed by `EVIDENCE_HMAC_SECRET` from system configuration:
  $$\text{Tamper Seal} = \text{HMAC-SHA256}_{K}\Big(\text{CanonicalJSON}(\text{EvidenceMetadata})\Big)$$
- **Canonicalization:** Metadata keys are deterministically sorted and normalized with compact JSON delimiters (`separators=(',', ':')`) to guarantee repeatable, bit-for-bit integrity checks.

### 4.2 Independent Verification Endpoint (`POST /api/verify-integrity`)
Any security analyst, auditor, or judge can submit an email's raw content and expected hash:
- Recalculates the SHA-256 digest independently on the server.
- Verifies constant-time equality via `hmac.compare_digest`.
- If an attacker or insider modified even a single whitespace character, Sentryl returns:
  ```json
  {
    "status": "TAMPERED",
    "verified": false,
    "calculated_sha256": "...",
    "expected_sha256": "..."
  }
  ```

### 4.3 Legal Admissibility Boundary Disclosure
Sentryl explicitly clarifies:
> *"Cryptographic evidence records provide tamper-evident technical integrity for internal security operations and incident post-mortems. They do not constitute statutory legal chain-of-custody compliance under court evidentiary rules (such as ISO/IEC 27037 or RFC 3161 PKI Time-Stamp Authorities with Hardware Security Modules)."*

---

## 5. PII Masking & Privacy Mode

When `privacyMode: true` is provided in the scan request:
- **Email Handles:** Normalized via regex to `[REDACTED_USER]@domain.com`.
- **Employee Names:** Substituted with `[REDACTED_NAME]`.
- **Private RFC 1918 IPs:** Substituted with `[INTERNAL_IP]`.
- **External GeoIP Boundary:** Internal RFC 1918 subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and loopback addresses (`127.0.0.1`) are detected locally and are **never transmitted to external GeoIP APIs**.

---

## 6. Administrative Access Control

Administrative endpoints (`backend/routers/admin.py`):
- `GET /api/admin/stats` (Server health, uptime, memory cache usage)
- `POST /api/admin/clear-cache` (Manual memory cache eviction)
- **Access Guard:** Every request must provide the `X-Sentryl-Key` HTTP header matching the server's configured `ADMIN_API_KEY`. Unauthenticated requests receive immediate **HTTP 401 Unauthorized** responses.

---

## 7. LLM Advisory Isolation & Prompt Injection Defense

1. **Decision Plane Isolation:** The LLM is invoked strictly *after* the deterministic risk score (0–100), risk tier, authentication status, and IOC table are calculated. The LLM has zero authority to alter numerical scores.
2. **Untrusted Data Encapsulation:** All external email subject lines, body snippets, and header strings passed to Gemini API are strictly encapsulated inside `<UNTRUSTED_EMAIL_DATA>` delimiters.
3. **Deterministic Fallback Engine:** If the Gemini API is unreachable, unconfigured, or returns invalid syntax, Sentryl automatically falls back to an internal deterministic template synthesizer.
