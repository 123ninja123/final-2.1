# Sentryl (SIH26106) — Comprehensive Technical & Security Audit

**Auditor:** Senior Cybersecurity Architect, Senior Full-Stack Engineer, ML Security Engineer, Digital Forensics Engineer & SIH Evaluator  
**Project:** Sentryl — "AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform"  
**Audit Target:** Local Project `#final - 2nd face` (downloaded from `https://github.com/123ninja123/final`)  
**Audit Date:** 2026-09-17  
**Compliance Standard:** SIH26106 Grand Finale Defense Standard & Strict Engineering Rules (Zero Fake Data)

---

## 1. Executive Summary & Verdict

Sentryl currently possesses a **well-crafted, polished visual presentation** with dark-mode UI styling, SVG gauge animations, Leaflet map rendering, and a working Microsoft Edge Manifest V3 extension shell. The FastAPI backend boots with 14 passing automated tests.

However, behind the visual facade, **critical core claims are either mocked, simulated with static dictionaries, or based on simplistic regex heuristics**:
1. **Zero Real ML/Neural Network**: Despite claims of a "Backend Neural API", the NLP engine is 4 regular expression patterns. No trained model or inference pipeline exists.
2. **Fabricated Geolocation & Threat Intelligence**: IP analysis relies on a hardcoded dictionary of 4 IPs. Unrecognized IPs are assigned arbitrary locations (e.g. Frankfurt/Hetzner or Ashburn/Cloudflare) based on IP prefixes. The client-side fallback fabricates city, country, ISP, and Tor/VPN flags based purely on whether `finalScore >= 50`.
3. **Fabricated WHOIS & Domain Age**: Domain registration age and WHOIS privacy are synthesized (e.g. "3 days ago" or "12 years ago") without any RDAP/WHOIS lookup.
4. **Synthesized SMTP Relay Paths**: If fewer than 2 hops are parsed from headers, the backend literally injects fake hops (`mx-in.google.com` at `74.125.82.51` and `mail-frontend.internal` at `142.250.152.27`).
5. **No Evidence Integrity / Chain of Custody**: No SHA-256 evidence hashing, no tamper detection, no IOC extraction table, and no attack relationship graph.
6. **Local Development Broken in Extension**: `manifest.json` host permissions do not include `http://localhost:8000/*`, preventing the extension from communicating with the local FastAPI backend during development and demonstrations.

---

## 2. Complete Runtime Flow Trace

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. INBOX LAYER (Gmail Webmail DOM)                                                     │
│ - Content script (gmail.js) queries DOM for sender, subject, body, and URLs           │
│ - LIMITATION: Gmail DOM does NOT expose raw RFC 822 headers or Reply-To in default view│
│ - Consequence: headers="" and replyTo="" are sent to detector                         │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. EXTENSION ENGINE LAYER (engine/detector.js)                                         │
│ - Tries to POST to https://api.sentryl.ai/api/scan (unresolvable placeholder domain)   │
│ - Timeout fires (3.5s) → Falls back to local executeClientScan()                       │
│ - ISSUE: Fabricates GeoIP & domain age based on score >= 50                            │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ (If routed to local backend: http://localhost:8000)
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. FASTAPI BACKEND PIPELINE (routers/scan.py)                                          │
│ - extract_ips(headers): If headers="", returns []                                      │
│ - origin_ip fallback: Defaults to "185.220.101.42" (Tor exit node in Germany!)         │
│ - parse_relay_path(): Synthesizes fake Google MX hops if len(hops) < 2                 │
│ - analyze_domain(): Exact match / Levenshtein; fakes WHOIS age & privacy               │
│ - check_urls(): Regex for raw IP, suspicious TLD, and 9 keywords                       │
│ - analyze_auth_headers(): Regex on header text for spf=pass/fail, dkim, dmarc           │
│ - analyze_text(): 4 regex pattern sets (Urgency, Credential, BEC, Authority)           │
│ - calculate_risk(): Unnormalized weighted sum (sum of weights = 120%), clamped at 100 │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. PRESENTATION & FORENSIC DOSSIER (popup.html / report.html)                           │
│ - Popup displays risk gauge, checks list, and scenario injection buttons               │
│ - Report page loads Leaflet map and displays static/mocked relay path                  │
│ - MISSING: Attack graph, IOC table, Evidence hash, Tamper verification, Explainability │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Project Audit Matrix

| FEATURE | STATUS | REAL / MOCK | PROBLEM / VULNERABILITY | REQUIRED FIX | PRIORITY |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Manifest & Host Permissions** | Partially Implemented | Real | `manifest.json` lacks `http://localhost:8000/*` and `http://127.0.0.1:8000/*`. Extension fails to talk to local backend; always falls back to client mock. | Add local dev hosts to `host_permissions` & allow configurable local endpoint in extension settings. | **P0** |
| **Default IP Fallback** | Partially Implemented | Mock/Bug | When Gmail headers are empty, backend defaults origin IP to `"185.220.101.42"` (Hetzner Tor node), falsely marking legitimate emails as high risk. | Distinguish between "Header Missing" vs "Observed IP". Do not assume Tor node if headers are absent. | **P0** |
| **IP Intelligence & Geolocation** | Partially Implemented | Mock | `services/ip_intel.py` uses a hardcoded 4-IP dictionary. Prefixes like `185.` are hardcoded to Frankfurt/Tor. Client-side fakes location based on score. | Integrate real DNS/RDAP/free GeoIP lookup (ip-api / GeoLite2 / cymru ASN) with local offline caching; show observed vs inferred. | **P0** |
| **Domain Intelligence & WHOIS** | Partially Implemented | Mock (WHOIS) / Real (Levenshtein) | Levenshtein distance is real, but WHOIS age (`age_days=3`, `created_date="12 years ago"`) and MX record validity are completely hardcoded. | Use real DNS lookup (`dnspython` / `socket`) for MX and real RDAP API for domain registration age; state "Unavailable" if API offline. | **P1** |
| **SMTP Relay Path Parser** | Partially Implemented | Mock (Synthetic) | If only 1 hop exists, `parse_relay_path()` injects fake hops (`mx-in.google.com`, `mail-frontend.internal`). | Parse RFC 5321/5322 Received headers authentically. Never inject fake hops. | **P1** |
| **Risk Scoring & Explainability** | Partially Implemented | Real Heuristic | Weights sum to 120% (35+30+25+20+10). No componentized breakdown (Auth, Domain, URL, Content, Infra, ThreatIntel). No "Why this score?" breakdown. | Restructure to 0–100 transparent formula with 7 distinct components and an interactive "Why this score?" evidence drawer. | **P1** |
| **ML / NLP Threat Engine** | Not Implemented | Mock / Claims Only | README claims "Backend Neural API", but `nlp_engine.py` is 4 regex patterns. No ML model or dataset exists. | Implement genuine baseline ML classifier (TF-IDF + structured email features + LogisticRegression/RandomForest) with reproducible training & eval scripts. | **P1** |
| **IOC Extraction** | Not Implemented | Missing | No structured IOC extraction table (IPv4, IPv6, Domains, URLs, Hashes, Mailboxes). | Build comprehensive regex & RFC-compliant IOC extractor with Copy/Export capabilities. | **P1** |
| **Attack / Relationship Graph** | Not Implemented | Missing | No visual IOC correlation graph (Sender → Domain → URL → IP → ASN → Auth). | Build interactive SVG/Canvas attack graph showing only verified relationships. | **P1** |
| **Evidence Preservation & Hashing** | Not Implemented | Missing | Uploaded or scanned emails have no cryptographic hash (SHA-256), timestamped chain of custody, or tamper detection. | Implement technical evidence record with SHA-256 acquisition hashing, event timeline, and tamper check button. | **P1** |
| **Raw .EML Upload & Forensics** | Not Implemented | Missing | Only accepts stripped JSON fields. Analysts cannot upload raw `.eml` files for header & MIME attachment inspection. | Add `/api/analyze-eml` endpoint supporting RFC 822 parsing, header extraction, and safe attachment metadata inspection. | **P1** |
| **Attachment Safety Analysis** | Not Implemented | Missing | Zero attachment extraction or analysis. No entropy, double-extension, or dangerous MIME detection. | Add static metadata inspector for attachments (hash, extension, MIME, size, entropy). Strictly no execution. | **P1** |
| **BEC & Impersonation Engine** | Partially Implemented | Real Heuristics | Only 1 regex pattern for BEC. No executive name spoofing check, no display name vs domain mismatch correlation. | Build dedicated BEC module detecting executive name impersonation, wire/banking cues, and Return-Path divergence. | **P2** |
| **Email Authentication (SPF/DKIM/DMARC)** | Partially Implemented | Real Regex | Checks substring in headers. Does not verify alignment between visible `From`, `Return-Path`, and `DKIM d=` domain. | Add authentication alignment engine explaining SPF/DKIM/DMARC results and domain alignment in plain language. | **P2** |
| **URL Detonation / Static Threat Intel** | Partially Implemented | Real Heuristic | Only checks raw IP and 9 keywords. No punycode, homoglyphs, URL encoding, or Safe Browsing/VirusTotal API integration. | Add static URL analyzer (entropy, punycode, redirect indicators) and optional real Safe Browsing/VirusTotal integration with graceful offline fallback. | **P2** |
| **Adversarial & Evasion Detection** | Partially Implemented | Real (Homoglyphs) | Basic homoglyphs dictionary. Missing punycode decoding, zero-width spaces, hidden HTML text, and obfuscated URLs. | Add evasion indicators module detecting punycode (`xn--`), hidden CSS/zero-width chars, and URL hex/octal encodings. | **P2** |
| **Privacy Mode & PII Masking** | Not Implemented | Missing | No data minimization or PII masking. Full email text processed without redaction options. | Add configurable Privacy Mode masking recipient, sender user part, phone numbers, and financial details. | **P2** |
| **Analyst Mode vs User Mode** | Partially Implemented | Missing Switch | Extension and report have fixed views without a simplified User Mode vs deep SOC Analyst Mode. | Implement UI toggle for User Mode (Simple verdict) vs Analyst Mode (full IOCs, headers, graph, evidence). | **P2** |
| **One-Click Investigation Flow** | Partially Implemented | Partial | In-page banner button sends message to open report, but report just reloads default PayPal scenario if storage sync fails. | Seamlessly pass current email state and scan ID into the investigation dashboard via chrome.storage or query param. | **P2** |

---

## 4. Architectural Gaps & Codebase Issues Identified

1. **Security Vulnerabilities in Input Processing**:
   - `extract_ips` does not validate whether extracted substrings are valid public IPv4/IPv6 addresses (e.g., version strings like `1.2.3.4` can match).
   - In `backend/main.py`, CORS allows `chrome-extension://*` and `edge-extension://*`, but wildcards in scheme origins are rejected by some browser security engines without proper handling.
   - Attachments from uploaded emails must never be executed or served back with executable MIME types.

2. **Gmail DOM Fragility**:
   - `gmail.js` searches for specific obfuscated classes (`table.Bs.nH .gE`, `h2.hP`, `div.a3s.aiL`). Gmail frequently alters obfuscated class names.
   - Better approach: use multi-selector fallback chains and support direct `.eml` upload as the primary gold-standard forensic investigation flow.

3. **Client-Side vs Backend Engine Duplication**:
   - `extension/engine/detector.js` duplicates `domain_intel.py`, `nlp_engine.py`, `url_checker.py`, and `risk_scorer.py` in vanilla JS. When rules are updated in Python, JS becomes out of sync.
   - Solution: maintain the offline client-side fallback as a resilient baseline, but ensure scoring formulas and heuristic rules are strictly synchronized and grounded.

4. **Lack of Unit & Integration Test Coverage for Edge Cases**:
   - Existing 14 tests only test happy paths with the 4 hardcoded scenarios.
   - Need comprehensive tests for: clean emails, Unicode homoglyphs, malformed headers, missing IP, punycode, oversized inputs, and evidence hash verification.

---

## 5. Prioritized Remediation Roadmap

- **Step 1 (P0)**: Fix `manifest.json` host permissions, eliminate all fake geolocation/WHOIS fallbacks, ensure backend works cleanly with local extension.
- **Step 2 (P0 & P1)**: Implement authentic RFC 822 / `.eml` parsing, real header analysis, and authentic IP/ASN/Geo resolution.
- **Step 3 (P1)**: Build Componentized 0–100 Explainable Risk Score with "Why this score?" breakdown.
- **Step 4 (P1)**: Implement IOC Extraction engine (IPv4/v6, domains, URLs, hashes, emails) and Attack Graph.
- **Step 5 (P1)**: Implement Technical Evidence Preservation (SHA-256 acquisition hashing, event timeline, tamper check).
- **Step 6 (P1)**: Build a genuine, lightweight, reproducible Machine Learning baseline classifier using `scikit-learn` (trained on reproducible email feature sets with precision/recall/F1/ROC-AUC evaluation).
- **Step 7 (P2)**: Enhance the Forensic Dashboard (`report.html`) into a serious SOC investigation suite with Analyst Mode, Evasion Indicators, and .eml upload.
- **Step 8 (P2)**: Expand automated test suite across all edge cases (25+ tests) and perform full security verification.
