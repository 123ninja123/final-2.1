# SENTRYL — FINAL RED-TEAM & SIH TECHNICAL JUDGE AUDIT
**Project**: Sentryl  
**SIH Problem Statement**: SIH26106 — *AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform*  
**Auditor Perspective**: Senior Cybersecurity Architect, SOC Incident Responder, Malicious-Email Defender, and Skeptical SIH Grand Finale Judge  
**Audit Target**: `d:\#final - 2nd face`  
**Execution Environment**: Python 3.14.3, FastAPI 0.115+, scikit-learn 1.9.0, pytest 9.1.1  
**Audit Date**: September 2026  

---

## SECTION A: EXECUTIVE VERDICT

Sentryl is a functional, highly capable, and well-architected **SOC-assistive email security and forensic triage prototype**. It successfully ingests RFC 822 `.eml` files and webmail payloads, performs deterministic multi-vector risk analysis (SPF/DKIM/DMARC authentication parsing, domain spoofing/Punycode detection, static lexical URL entropy and redirect analysis, and NLP/BEC pattern matching), constructs single-incident attack graphs, and computes cryptographic SHA-256 acquisition hashes.

However, a rigorous red-team audit reveals **significant discrepancies between previous completion claims and real-world implementation truth**:
1. **Machine Learning Claim vs Reality**: The machine learning model is trained on a **20-sample hand-crafted dataset** synthetically doubled to 40 samples via trivial string appending. A pre-split data leakage flaw guarantees a 1.00 (100%) metric during cross-validation. Furthermore, runtime detection risk scores (0–100) are computed **100% deterministically by rule heuristics**; the ML classifier functions purely as an auxiliary metadata tag and does not determine the risk score.
2. **"URL Detonation" Claim vs Reality**: Sentryl does **NOT** detonate URLs. There is no headless browser, sandbox VM, network request, DNS lookup, or execution environment. It performs **safe static lexical analysis** (regex, entropy, TLD checks). While safe from SSRF, marketing it as "detonation" is technically false.
3. **Forensic Integrity vs Legal Admissibility**: Sentryl calculates SHA-256 digests and assembles an internal audit log with synthetic millisecond offsets. However, the tamper seal is an **unkeyed SHA-256 hash** (`sha256(eid::raw_hash::timestamp)`) rather than a cryptographic HMAC or PKI digital signature. It provides **technical tamper evidence**, not statutory legal admissibility.
4. **Denial of Service / Memory Risk**: The `.eml` upload endpoint reads the entire payload into RAM before checking size thresholds (`await file.read()`), exposing the server to memory exhaustion under unconstrained streaming uploads.

**Final Verdict**: Sentryl is **DEMO READY** as an **Interactive Technical Prototype and SOC Analyst Triage Accelerator**. It is **NOT Production Ready** for autonomous perimeter email gateway deployment without database persistence, asymmetric evidence keying, rate limiting, and an enterprise-scale ML training pipeline.

---

## SECTION B: VERIFIED CAPABILITIES (WHAT ACTUALLY WORKS)

Direct code inspection and test execution confirm the following subsystems are fully implemented, functional, and defensible:

### 1. Authentic RFC 822 / MIME Parsing (`backend/services/eml_parser.py`)
- Standard library MIME tree traversal (`email.message_from_bytes(..., policy=email.policy.default)`).
- Complete extraction of folded multi-line `Received:`, `Authentication-Results:`, `DKIM-Signature:`, `Return-Path:`, and `Message-ID` headers.
- Multi-part decoding (`text/plain`, `text/html`) with HTML tag stripping.
- Safe static attachment metadata extraction (`filename`, `size_bytes`, SHA-256, MD5, Shannon byte entropy). Attachments are never written to disk or executed.

### 2. Deterministic Email Authentication Analysis (`backend/services/header_parser.py`)
- Accurately parses RFC 7208 (SPF), RFC 6376 (DKIM), and RFC 7489 (DMARC) outcomes directly from `Authentication-Results` and `Received-SPF` headers.
- Evaluates `From` vs `Reply-To` mismatch and detects deceptive mailbox redirection.

### 3. Domain Spoofing & Punycode Engine (`backend/services/domain_checker.py`)
- Standardized Levenshtein distance calculations against target high-value brands (Google, Microsoft, PayPal, Apple, Amazon, Netflix, Chase, Stripe, FedEx, DocuSign).
- Punycode detection (`xn--`) for Internationalized Domain Name (IDN) homograph attacks.
- High-abuse TLD flagging (`.xyz`, `.top`, `.work`, `.click`, `.surf`, etc.).
- Disposable email provider cross-referencing (`mailinator.com`, `tempmail.com`, `guerrillamail.com`, etc.).

### 4. Safe Static URL Lexical Inspection (`backend/services/url_checker.py`)
- Extracts URLs via regex; performs parsing using `urllib.parse`.
- Flags direct IPv4 hostnames (`http://192.168.44.12/verify.php`).
- Detects open redirect query parameters (`?redirect=`, `?url=`, `?target=`).
- Computes Shannon entropy over URL path/query to identify obfuscated hex/base64 tracking tokens.
- Flags credential solicitation keywords (`login`, `verify`, `password`, `banking`).
- **Zero outbound network connections**: Total immunity to SSRF and remote web exploits.

### 5. Social Engineering & BEC Linguistic Analysis (`backend/services/nlp_engine.py`, `backend/services/bec_detector.py`)
- Rule-based regex scoring for urgency, coercive panic, and financial keywords.
- Dedicated BEC heuristic engine detecting executive impersonation ("CEO Office", "Managing Director"), unauthorized wire transfer routing, and out-of-band communication suppression ("do not call", "in a meeting").

### 6. Anti-Analysis & Evasion Detection (`backend/services/evasion_detector.py`)
- Strips and flags zero-width Unicode spaces (`\u200B`, `\u200C`, `\u200D`, `\uFEFF`).
- Identifies Cyrillic-Latin homoglyph substitutions in body and domain strings.
- Detects hidden CSS font-size manipulation (`font-size: 0px`, `display: none`).

### 7. Per-Email Incident Attack Graph (`backend/services/graph_builder.py`)
- Assembles a structured node-edge star/tree topology linking Email -> Sender -> Domain -> Auth -> URLs -> Origin IP -> ASN -> Attachments -> Hashes.
- Zero fabricated nodes; every node is derived strictly from extracted email entities.

### 8. Privacy-First PII Masking (`backend/routers/scan.py:27-41`)
- Redacts email usernames (`j***e@corp.com`), phone numbers (`***-***-4567`), and card numbers (`****-****-****-4444`) before processing when `privacyMode: true`.

---

## SECTION C: FALSE / OVERSTATED CLAIMS AUDIT

Every claim from previous documentation was evaluated against the actual codebase:

| Claim | Actual Implementation | Evidence / File | Status | Technical Risk | Required Action |
|---|---|---|---|---|---|
| **"Production Ready"** | Prototype architecture with in-memory state, no database, no auth, no worker queue | `backend/config.py`, `backend/services/report_store.py` | **FALSE** | Deployment failure under enterprise load | Rebrand as "SOC Analyst Triage Prototype" |
| **"URL Detonation"** | Static regex, TLD, open redirect, and Shannon entropy analysis; NO VM or execution | `backend/services/url_checker.py` | **FALSE** | Misleads judges into expecting dynamic sandbox | Rename to "Safe Static URL Lexical Analysis" |
| **"100% ML Accuracy / Production ML"** | Trained on 20 hand-crafted samples doubled to 40; pre-split leakage causes 1.00 score | `backend/ml/dataset.py`, `backend/ml/train_model.py` | **FALSE** | Immediate failure on unseen real-world emails | Label as "ML PROTOTYPE / LIMITED VALIDATION" |
| **"ML Drives Threat Scoring"** | Risk score (0-100) is computed strictly by rule heuristics; ML is an advisory metadata tag | `backend/services/risk_scorer.py:53-388` | **FALSE** | Misrepresents decision boundary | State that rule engine is primary and ML is auxiliary |
| **"Legally Admissible Evidence Vault"** | Generates SHA-256 hash and synthetic timeline; seal is unkeyed hash, not PKI signature | `backend/services/evidence_vault.py:65-78` | **OVERSTATED** | Inadmissible in statutory court proceedings | Claim "Tamper-Evident Evidence Handling" only |
| **"Zero Fabrication Attack Graph"** | Generates valid single-email star graph, but caps URLs at 4; does not correlate multi-user campaigns | `backend/services/graph_builder.py:63-64` | **PARTIAL** | Limited to single email, not enterprise cluster | Clarify "Single-Incident Entity Topology" |
| **"SSRF Protection"** | URL checker makes zero HTTP calls, eliminating SSRF; IP analyzer uses hardcoded table | `backend/services/url_checker.py`, `backend/services/ip_intel.py` | **VERIFIED** | None (safe by architectural omission) | Clarify safe static isolation model |
| **"Prompt Injection Shielding"** | Delimits untrusted data with `<UNTRUSTED_EMAIL_DATA>`; LLM cannot change risk score | `backend/services/llm_explainer.py:78-97` | **VERIFIED** | LLM could still generate confusing summaries | Verify deterministic fallback active |
| **"41/41 Tests Verified"** | 41 unit/integration tests pass, but zero tests for DoS streaming, HMAC forgery, or live DOM | `SECURITY_TEST_GAPS.md` | **PARTIAL** | Uncovered failure modes in edge cases | Disclose known test gaps transparently |

---

## SECTION D: SECURITY FINDINGS

```
========================================================================================
VULNERABILITY SEVERITY BREAKDOWN:
CRITICAL: 0  |  HIGH: 2  |  MEDIUM: 3  |  LOW: 2
========================================================================================
```

### 1. [HIGH] In-Memory Buffering on Large EML Uploads (DoS Vulnerability)
- **Location**: `backend/routers/scan.py:198-200`
- **Mechanism**: The endpoint `/api/analyze-eml` executes `content = await file.read()` before evaluating `if len(content) > 10_000_000: raise HTTPException(413)`.
- **Exploitation**: An adversary transmitting a 2 GB file upload stream forces the FastAPI/Uvicorn process to buffer the entire stream into RAM, causing an Out-Of-Memory (OOM) worker crash.
- **Remediation**: Check `request.headers.get('content-length')` and read the incoming byte stream in 64KB chunks, raising HTTP 413 immediately when cumulative bytes exceed 10MB.

### 2. [HIGH] Unkeyed Evidence Tamper Seal (Integrity Forgery)
- **Location**: `backend/services/evidence_vault.py:66-67`
- **Mechanism**: The tamper seal is computed as `hashlib.sha256(f"{eid}::{raw_hash}::{now_iso}".encode()).hexdigest()`.
- **Exploitation**: Because there is no secret key or asymmetric private key, any actor who modifies `raw_hash` can trivially recalculate a valid `tamper_seal_hash`. It detects accidental corruption, not malicious tampering by someone with database access.
- **Remediation**: Replace with `hmac.new(SECRET_KEY, seal_material.encode(), hashlib.sha256).hexdigest()` or sign using an Ed25519/RSA private key.

### 3. [MEDIUM] Unauthenticated Local API Ingestion
- **Location**: `backend/main.py:56-59`, `backend/routers/scan.py:43, 194`
- **Mechanism**: All API endpoints (`/api/scan`, `/api/analyze-eml`, `/api/report/{id}`) are unauthenticated.
- **Exploitation**: Any local process or host permitted by CORS (`chrome-extension://*`, `localhost`) can issue unlimited analysis requests, filling server RAM with in-memory reports.
- **Remediation**: Implement API Key header authentication (`X-Sentryl-Key`) or JWT token authorization.

### 4. [MEDIUM] Memory Growth in Global Report Cache (Resource Exhaustion)
- **Location**: `backend/services/report_store.py:4-11`
- **Mechanism**: Reports are stored in `_REPORTS_CACHE: Dict[str, Dict[str, Any]] = {}` without an eviction policy (no LRU, TTL, or max entry cap).
- **Exploitation**: Prolonged operation under continuous scanning leads to unbounded memory consumption.
- **Remediation**: Wrap with an LRU cache or Redis instance with an explicit TTL (e.g., 24 hours).

### 5. [MEDIUM] Single-Vector Attachment Risk Thresholding Underestimation
- **Location**: `backend/services/risk_scorer.py:330-345`
- **Mechanism**: Dangerous attachment score is capped at `min(20, dangerous_count * 15)`.
- **Exploitation**: A benign-looking email sent from a clean domain with valid SPF/DKIM carrying an executable payload (`invoice.pdf.exe`) scores only 15/100 points, falling into the **"Low Risk"** band (0–29).
- **Remediation**: Add a critical override: presence of high-risk executable attachments (`.exe`, `.scr`, `.bat`, double extensions) must enforce a minimum floor of `High` risk (>= 60) regardless of clean authentication.

### 6. [LOW] Synthetic Chain-of-Custody Timestamps
- **Location**: `backend/services/evidence_vault.py:27-63`
- **Mechanism**: The 5-step chain of custody records timestamps by subtracting synthetic 10ms offsets (`t0 - 40ms`, `t0 - 30ms`, etc.) rather than measuring true execution timestamps.
- **Impact**: Technically synthetic; must be presented as a conceptual forensic timeline rather than hardware timestamping.

### 7. [LOW] Gmail UI Obfuscated DOM Class Fragility
- **Location**: `extension/content/gmail.js:26-64`
- **Mechanism**: Extracts sender and body using Gmail internal CSS classes (`.a3s`, `.hP`, `span[email]`).
- **Impact**: When Google updates Gmail's minified class names, DOM scraping fails silently, returning fallback values.
- **Mitigation**: The standalone `.eml` upload channel serves as the robust out-of-band alternative.

---

## SECTION E: ML FINDINGS & FORENSIC AUDIT

### Detailed Inspection of ML Subsystem:
- **Source Code**: `backend/ml/dataset.py`, `backend/ml/train_model.py`, `backend/ml/evaluate_model.py`
- **Artifact**: `backend/models/ml_model.joblib`
- **Report**: `backend/ml/evaluation_report.json`

```
========================================================================================
ML SUBSYSTEM REALITY AUDIT:
========================================================================================
1. Exact Number of Base Samples:       20 (10 Benign, 10 Phishing/BEC)
2. Total Augmented Samples:            40 (Exact duplicates with trivial suffix)
3. Class Distribution:                 20 Benign (50.0%) / 20 Malicious (50.0%)
4. Sample Independence:                FALSE (Augmented samples are clones)
5. Train/Test Data Leakage:            CRITICAL FLAW (Augmentation precedes splitting)
6. Cross-Validation Methodology:       FLAWED (Evaluates pre-trained model on folds)
7. Reported Accuracy:                  1.0000 (100.0%) — Artificially inflated
8. Reported F1-Score:                  1.0000 (100.0%)
9. Reported ROC-AUC:                   1.0000
10. Confusion Matrix:                  TN=20, FP=0, FN=0, TP=20
11. Runtime Risk Score Influence:      0% (Rules compute 0-100 score; ML is advisory)
12. Inference Failure Safety:          SAFE (Graceful fallback if model is missing)
========================================================================================
```

### Forensic Analysis of the Flaw:
In `backend/ml/dataset.py:239-246`:
```python
augmented = []
for s in data:
  aug = dict(s)
  aug["body"] = (
      s["body"]
      + " "
      + random.choice([
          "Please review immediately.",
          "Thank you for your prompt attention.",
      ])
  )
  augmented.append(aug)
full_dataset = data + augmented
random.shuffle(full_dataset)
```
When `full_dataset` is split (in `train_model.py`) or partitioned into 5 folds (in `evaluate_model.py`), identical base samples appear simultaneously in training and testing folds. Furthermore, in `evaluate_model.py:28-39`, the classifier is loaded pre-fitted from disk and evaluated across folds without being refitted on each training fold.

### Mandated Disclosure:
> **OFFICIAL STATUS**: **`ML PROTOTYPE / LIMITED VALIDATION`**  
> Under no circumstances should Sentryl claim "100% accurate AI" or "Production-grade ML". The current ML subsystem is a proof-of-concept pipeline demonstrating how dual-branch TF-IDF + structured feature extraction can feed a classifier. Real-world validation requires a minimum benchmark of **10,000+ real-world labeled emails** (e.g., Enron + Nazario Phishing Corpus + Apache SpamAssassin).

---

## SECTION F: FORENSIC INTEGRITY AUDIT

### 1. Evidence Hashing
- Uses SHA-256 and MD5 computed directly over raw message bytes (`backend/services/eml_parser.py:18-19`).
- Hash generation is deterministic, reproducible, and verifiable via `/api/verify-integrity`.

### 2. Chain of Custody & Timestamps
- The chain of custody logs five sequential lifecycle steps: Acquisition -> Hash Calculation -> RFC 5322 Parsing -> Risk Scoring -> Dossier Sealing.
- **Limitation**: Timestamps are synthetically generated using negative millisecond deltas from `t0`. It represents an execution log rather than RFC 3161 trusted hardware timestamping.

### 3. Tamper Seal Implementation
- **Implementation**: `tamper_seal_hash = sha256(f"{eid}::{raw_hash}::{now_iso}")`.
- **Limitation**: Without an asymmetric key pair or secret HMAC salt, the seal demonstrates **internal consistency**, not cryptographic non-repudiation.
- **Admissibility Assessment**: Does **NOT** meet statutory standards for legal court admissibility (e.g., Federal Rules of Evidence Rule 902(14) or Indian Evidence Act Section 65B) because it lacks an independent PKI witness, hardware security module (HSM), or trusted time-stamp authority (TSA).
- **Correct Technical Term**: **"Tamper-Evident Forensic Integrity Tracking"**.

---

## SECTION G: EXTENSION SECURITY AUDIT

### 1. Manifest V3 Conformance (`extension/manifest.json`)
- Conforms strictly to Manifest V3 (`"manifest_version": 3`).
- Service worker background lifecycle: `"background": { "service_worker": "background/service-worker.js" }`.
- **Permissions Minimized**: Restricted to `["storage", "activeTab"]`. No broad intercept permissions (`<all_urls>`, `webRequest`, `cookies` are absent).

### 2. Cross-Site Scripting (XSS) & DOM Injection
- In `extension/content/gmail.js:97-100`, untrusted strings are sanitized via `escapeHtml()` using `document.createElement('div').textContent` before rendering UI banners.
- No `eval()`, `new Function()`, or unescaped `innerHTML` injection of raw email content.

### 3. Host Permissions & Network Boundaries
- Host permissions are limited to `https://mail.google.com/*`, `http://localhost:8000/*`, and production endpoints.
- Communicates only with the configured local or remote backend; no third-party telemetry beacons.

### 4. DOM Selector Fragility
- Content script targets minified Gmail elements (`span[email]`, `div.a3s.aiL`, `h2.hP`).
- **Failure Mode**: When Gmail deploys UI updates, DOM scraping returns fallback values (`unknown-sender@mail.net`). The extension does not crash, but cannot scan until updated.

---

## SECTION H: PRIVACY AUDIT

### Exact Data Flow Architecture:

```
[Raw Email] 
   │
   ├── Privacy Mode Enabled?
   │      ├── YES: PII Masked (Usernames, Phone, Cards redacted)
   │      └── NO:  Raw text preserved in memory
   │
   ├── Execution in Backend:
   │      ├── RFC 822 Parsing: Local CPU memory only
   │      ├── Authentication: Local header parsing
   │      ├── Static URL Check: Local regex & Shannon entropy (0 outbound calls)
   │      ├── ML Inference: Local joblib model in RAM (0 outbound calls)
   │      └── Attack Graph: In-memory node assembly
   │
   ├── Report Storage:
   │      └── Stored in RAM dictionary (_REPORTS_CACHE)
   │      └── ZERO disk writes of email text; ZERO external database sync
   │
   └── External Transmission:
          ├── Gemini LLM: ONLY if GEMINI_API_KEY is configured
          │      └── Transmits: Sender, Subject, Risk Score, Intent
          │      └── NEVER transmits: Attachments, Raw RFC headers, or Full Body
          └── If GEMINI_API_KEY unset: ZERO external bytes transmitted
```

### Privacy Assessment:
- **Raw Email Retention**: Stored exclusively in server RAM during runtime. Never written to SQLite, PostgreSQL, or disk. Lost upon server restart.
- **Third-Party Telemetry**: **Zero**.
- **Privacy Mode Defensibility**: Highly defensible for sensitive corporate environments when self-hosted on-premises.

---

## SECTION I: TEST GAPS SUMMARY

From `SECURITY_TEST_GAPS.md`:
1. **Streaming Upload DoS**: Lack of chunked byte-limit enforcement before memory buffering.
2. **Unkeyed Seal Forgery**: Inability to detect malicious seal recalculation without HMAC.
3. **MIME Parser Fuzzing**: Absence of deep nesting and circular boundary bomb tests.
4. **Adversarial ML Evasion**: Absence of token-stuffing tests against TF-IDF weights.
5. **Gmail DOM Mutation**: Zero automated end-to-end tests for UI selector updates.
6. **Concurrent Cache Saturation**: Absence of load testing on in-memory report cache.

---

## SECTION J: SIH JUDGE ATTACK QUESTIONS (20 TOUGH QUESTIONS)

### Q1: "Gmail already detects phishing. Why do we need you?"
- **Defensible Answer**: "Gmail is a protective consumer shield designed to filter obvious spam and phishing silently. It operates as a black box: it does not explain why an email was flagged, does not reveal the underlying relay hops, does not extract IOCs for SIEM ingestion, and does not preserve cryptographic chain-of-custody evidence for forensic investigation. Sentryl is an analyst-assistive investigative workbench: it turns every suspicious message into a structured forensic dossier with attack graphs, authentication breakdowns, and exportable indicators."
- **Evidence in Code**: `backend/services/graph_builder.py`, `backend/services/ioc_extractor.py`, `backend/services/evidence_vault.py`.
- **Limitation**: Sentryl does not replace enterprise perimeter mail transfer agents (MTAs); it augments triage.
- **What NOT to Claim**: Never claim Sentryl blocks more zero-day threats than Google's multi-billion-dollar infrastructure.

---

### Q2: "Where is your real AI?"
- **Defensible Answer**: "Sentryl's AI architecture consists of two distinct components: (1) a local dual-branch scikit-learn classifier combining TF-IDF body n-grams with 9 structured security features (SPF status, domain spoofing, URL entropy, dangerous attachments), and (2) an LLM-assisted forensic explainer that translates deterministic indicators into natural language analyst summaries. However, our primary risk scoring engine is intentionally deterministic rule-based heuristics to guarantee explainability and prevent hallucination."
- **Evidence in Code**: `backend/ml/feature_extractor.py:46-95`, `backend/ml/train_model.py:31-39`, `backend/services/llm_explainer.py:81-97`.
- **Limitation**: The model is a lightweight linear prototype trained on a small curated benchmark.
- **What NOT to Claim**: Do not claim deep neural networks, BERT transformers, or autonomous reinforcement learning.

---

### Q3: "40 samples? How can you claim accuracy?"
- **Defensible Answer**: "We do not claim production-grade generalization from 40 samples. We explicitly designate our ML model as an 'ML Prototype / Limited Validation'. The 40 samples serve as a functional architectural testbed to prove our dual-branch feature pipeline works end-to-end. Our primary operational detection relies on our deterministic heuristic engine, which evaluates RFC authentication standards and lexical anomalies independent of dataset size."
- **Evidence in Code**: `backend/ml/dataset.py:7-233`, `backend/ml/evaluation_report.json`.
- **Limitation**: The 100% accuracy metric is an artifact of synthetic augmentation and small sample size.
- **What NOT to Claim**: Never claim '100% accuracy' or 'tested on production datasets'.

---

### Q4: "What happens with a zero-day phishing email?"
- **Defensible Answer**: "A zero-day phishing campaign using a freshly registered domain and novel lure text will bypass static signature blacklists. However, Sentryl evaluates structural anomalies: if the email has an unaligned Return-Path, a newly registered high-abuse TLD, high Shannon lexical entropy in the destination URL, or coercive financial keywords, multiple non-signature checks trigger and elevate the risk score."
- **Evidence in Code**: `backend/services/url_checker.py:144-150`, `backend/services/domain_checker.py:83-92`, `backend/services/bec_detector.py:40-75`.
- **Limitation**: A sophisticated attacker using a compromised legitimate corporate account with valid SPF/DKIM and clean links can evade detection.
- **What NOT to Claim**: Do not claim 100% zero-day prevention.

---

### Q5: "How do you avoid false positives?"
- **Defensible Answer**: "We avoid false positives through transparent multi-vector scoring with capped categorical weights. No single indicator can mark an email as Critical. Authentication failure alone is capped at 20 points; URL anomalies are capped at 20; NLP urgency is capped at 8. An email only reaches 'Critical' (75+) if anomalies align across multiple independent vectors (authentication + domain + URL + content)."
- **Evidence in Code**: `backend/services/risk_scorer.py:11-26, 115, 178, 226, 290`.
- **Limitation**: Legitimate corporate newsletters using third-party tracking links and urgent marketing language can occasionally trigger 'Suspicious' (30-45).
- **What NOT to Claim**: Do not claim 'zero false positives'.

---

### Q6: "Can your system explain WHY?"
- **Defensible Answer**: "Yes. Explainability is our core architectural foundation. Every risk assessment returns an itemized `score_breakdown` detailing the exact signal (e.g., `AUTH_SPF_FAIL`), observed value, points added, and forensic reason. This is complemented by an evidence-grounded summary that cites observed facts without extrapolation."
- **Evidence in Code**: `backend/services/risk_scorer.py:65-74, 381-390`, `backend/services/llm_explainer.py:23-40`.
- **Limitation**: When Gemini API is active, natural language summaries depend on external LLM availability.
- **What NOT to Claim**: Do not claim the LLM generated the mathematical score.

---

### Q7: "Can an attacker manipulate your risk score?"
- **Defensible Answer**: "An attacker cannot directly manipulate the scoring formula because weights and thresholds are strictly server-side. However, an attacker can attempt evasion by passing SPF/DKIM on their own domain, stripping known phishing keywords, and using homoglyphs. Sentryl counters this with dedicated evasion detectors for zero-width spaces, Cyrillic substitutions, and hidden CSS."
- **Evidence in Code**: `backend/services/evasion_detector.py:15-85`.
- **Limitation**: Attackers who compromise legitimate executive Microsoft 365 accounts with clean reputation can keep scores artificially low.
- **What NOT to Claim**: Do not claim immunity to sophisticated spear phishing.

---

### Q8: "Can the LLM be prompt-injected?"
- **Defensible Answer**: "No. Sentryl's architecture isolates the LLM from the decision plane. The risk score, risk level, IOCs, and recommended actions are calculated deterministically before the LLM is invoked. Untrusted email fields are sanitized and enclosed in `<UNTRUSTED_EMAIL_DATA>` delimiters with strict system prompt boundaries. Even if the LLM were jailbroken to say 'This email is safe', the system's displayed score, indicators, and UI badges remain Critical."
- **Evidence in Code**: `backend/services/llm_explainer.py:78-97`, `backend/routers/scan.py:139-165`.
- **Limitation**: A prompt injection could alter the English wording of the 3-bullet text summary.
- **What NOT to Claim**: Do not claim the LLM is impossible to jailbreak textually.

---

### Q9: "Can you prove the email wasn't modified?"
- **Defensible Answer**: "We prove post-acquisition integrity via cryptographic SHA-256 and MD5 hashing of the raw email payload upon arrival. Any post-ingestion alteration to headers, body, or attachments produces a hash mismatch detectable via `/api/verify-integrity`."
- **Evidence in Code**: `backend/services/eml_parser.py:18-20`, `backend/services/evidence_vault.py:80-118`.
- **Limitation**: This proves the email was not altered *after* reaching Sentryl; it cannot prove the sender did not manipulate headers prior to delivery.
- **What NOT to Claim**: Do not claim statutory legal chain-of-custody compliance without HSM/PKI signatures.

---

### Q10: "Can you identify the real sender?"
- **Defensible Answer**: "We trace the real originating sender infrastructure by parsing the bottom-most trusted `Received:` header in the relay path and extracting the connecting IP address and PTR record, rather than trusting the mutable `From:` header."
- **Evidence in Code**: `backend/services/header_parser.py:65-98`, `backend/services/eml_parser.py:28-36`.
- **Limitation**: If the adversary routes traffic through Tor exit nodes, commercial VPNs, or compromised proxy relays, the IP identifies the exit gateway, not the physical perpetrator.
- **What NOT to Claim**: Do not claim Sentryl can unmask a physical human behind a VPN.

---

### Q11: "Does IP geolocation reveal their exact location?"
- **Defensible Answer**: "No, and we explicitly emphasize this. IP geolocation reveals the registered geographic allocation of the Autonomous System (ASN) or internet service provider, typically accurate to the city or regional ISP data center level. It does not provide GPS or street-level physical location."
- **Evidence in Code**: `backend/services/ip_intel.py:15-45`.
- **Limitation**: Geolocation of cloud providers (AWS, Azure) reflects data centers, not attackers.
- **What NOT to Claim**: Never claim 'pinpointing the attacker's physical address'.

---

### Q12: "Can your system safely inspect malicious URLs?"
- **Defensible Answer**: "Yes, because our URL inspection engine is 100% static. Sentryl parses URL syntax, validates host schemes, evaluates lexical entropy, and checks for open redirects without sending a single network packet or resolving DNS. This provides total immunity to SSRF, browser exploits, and malicious payload delivery."
- **Evidence in Code**: `backend/services/url_checker.py:40-150`.
- **Limitation**: Static analysis cannot detect malicious content hosted behind dynamic CAPTCHA cloaking or multi-stage JavaScript redirects.
- **What NOT to Claim**: Do not claim dynamic sandbox detonation or screenshot capture.

---

### Q13: "Can you automatically quarantine emails?"
- **Defensible Answer**: "Currently, Sentryl operates as an investigative and advisory platform providing actionable triage recommendations (e.g., 'Block sender domain', 'Quarantine message'). Direct automated mailbox quarantine requires Microsoft Graph API or Google Workspace Admin API integration, which is planned in our enterprise roadmap."
- **Evidence in Code**: `backend/services/llm_explainer.py:53-69`.
- **Limitation**: Requires human analyst action to execute quarantine in the mail client.
- **What NOT to Claim**: Do not claim automated active remediation in Google/Microsoft production mailboxes.

---

### Q14: "What happens if threat-intelligence APIs fail?"
- **Defensible Answer**: "Sentryl is built on a zero-remote-dependency architecture. Our core engine uses local RFC header parsing, local Levenshtein domain distance, local URL lexical analysis, and a local offline ML model. If external APIs (like Gemini or external IP lookup) are offline or unconfigured, the system falls back seamlessly to deterministic rule evaluation with zero service disruption."
- **Evidence in Code**: `backend/services/ip_intel.py:15-35`, `backend/services/llm_explainer.py:104-116`.
- **Limitation**: Lacks real-time querying of commercial threat feeds like VirusTotal or AlienVault OTX.
- **What NOT to Claim**: Do not claim real-time synchronization with external global threat intelligence clouds.

---

### Q15: "What happens if Gmail changes its UI?"
- **Defensible Answer**: "Browser DOM scraping is inherently vulnerable to web client UI updates. If Google updates Gmail class names, the extension's in-page DOM extraction can degrade. To solve this, Sentryl provides a standalone, protocol-level `.eml` upload channel (`/api/analyze-eml`) that parses standard RFC 822 MIME bytes completely independent of webmail HTML layouts."
- **Evidence in Code**: `backend/routers/scan.py:194-280`, `backend/services/eml_parser.py:15-116`.
- **Limitation**: The Chrome extension content script requires maintenance when Gmail updates its markup.
- **What NOT to Claim**: Do not claim the Chrome extension is immune to Gmail web UI refactoring.

---

### Q16: "What makes this different from existing email security products?"
- **Defensible Answer**: "Commercial Secure Email Gateways (SEGs like Proofpoint or Mimecast) are expensive, perimeter-focused enterprise appliances that silently discard emails without user insight. Sentryl provides transparent, on-demand, interactive forensic triage with visual attack graphs, itemized scoring evidence, and privacy-preserving local execution accessible to SMEs, Tier-1 SOC analysts, and end users."
- **Evidence in Code**: `backend/services/graph_builder.py`, `backend/services/risk_scorer.py:381-390`.
- **Limitation**: We do not yet offer distributed high-throughput mail gateway filtering.
- **What NOT to Claim**: Do not claim Sentryl outperforms mature multi-million dollar enterprise SEGs today.

---

### Q17: "Who would actually pay for this?"
- **Defensible Answer**: "Our primary target market is twofold: (1) Managed Security Service Providers (MSSPs) and Tier-1 SOC teams who need a rapid, standardized triage tool to accelerate manual phishing ticket analysis, and (2) SMEs and educational institutions that cannot afford $50,000/year enterprise SEG contracts but need actionable email threat intelligence."
- **Evidence in Code**: `backend/models/schemas.py` (Structured JSON API ready for SIEM/SOAR ingestion).
- **Limitation**: No billing or multi-tenant subscription engine is implemented in the codebase today.
- **What NOT to Claim**: Do not invent paying customers, revenue numbers, or customer contracts.

---

### Q18: "Can this scale beyond a college demo?"
- **Defensible Answer**: "The algorithmic core (stateless FastAPI endpoints, linear feature extractors, and regex parsers) processes emails in under 50ms per message. To scale to an enterprise production gateway, three architectural components must be added: a persistent PostgreSQL/Timescale database, a Redis/Celery worker queue for asynchronous batch ingestion, and a persistent Redis cache for report storage."
- **Evidence in Code**: `backend/main.py:34-41` (`X-Process-Time` consistently logs under 0.04s).
- **Limitation**: The current in-memory report store cannot scale horizontally across clustered containers.
- **What NOT to Claim**: Do not claim current multi-node Kubernetes clustering.

---

### Q19: "What are your biggest limitations?"
- **Defensible Answer**: "Our three most significant limitations today are: (1) The machine learning classifier is a lightweight prototype trained on a small 20-sample benchmark dataset; (2) Evidence vault seals use unkeyed hashes rather than PKI hardware signatures; and (3) URL inspection is purely static lexical analysis rather than dynamic sandbox detonation."
- **Evidence in Code**: `backend/ml/dataset.py:7-20`, `backend/services/evidence_vault.py:66-67`, `backend/services/url_checker.py:40-65`.
- **Strength**: Honest self-awareness of technical boundaries builds credibility with senior judges.
- **What NOT to Claim**: Never attempt to conceal or minimize these three known limitations.

---

### Q20: "Which part is genuinely implemented today?"
- **Defensible Answer**: "100% of our code in this repository is genuine and operational today: RFC 822 MIME parsing, SPF/DKIM/DMARC header analysis, Levenshtein domain spoofing, Shannon entropy URL analysis, BEC keyword matching, zero-width space and homoglyph evasion detection, single-email attack graph generation, SHA-256 evidence integrity hashing, and our 41 automated pytest tests."
- **Evidence in Code**: Complete repository verification across `backend/` and `extension/`.
- **Limitation**: Datasets, persistence layers, and external sandbox detonation remain future roadmap milestones.
- **What NOT to Claim**: Do not claim completed features that exist only as concepts.

---

## SECTION K: BUSINESS REALITY CHECK (6 DEPLOYMENT MODELS)

### 1. Individual Security Assistant (Browser Extension)
- **CUSTOMER**: Privacy-conscious knowledge workers, executives, freelance professionals.
- **PROBLEM**: Phishing emails slipping into personal or Google Workspace webmail.
- **SENTRYL VALUE**: Instant in-browser threat badge and visual explanation before clicking.
- **REQUIRED INTEGRATIONS**: Chrome Web Store, Edge Add-ons Store.
- **CURRENT READINESS**: **HIGH (75%)**. Manifest V3 extension and Gmail content script are functional.
- **MISSING COMPONENTS**: Automated update pipeline, cross-browser Safari/Firefox support, OAuth login.

### 2. SME Email Security Layer
- **CUSTOMER**: Small-to-medium enterprises (10–250 employees) without a dedicated 24/7 SOC.
- **PROBLEM**: High vulnerability to BEC and invoice fraud without budget for Proofpoint.
- **SENTRYL VALUE**: Centralized email scanning portal with PII masking and zero cloud data leaks.
- **REQUIRED INTEGRATIONS**: Microsoft 365 Exchange transport rules, Google Workspace Marketplace app.
- **CURRENT READINESS**: **MEDIUM (45%)**. Backend APIs work; lacks multi-tenant tenant isolation.
- **MISSING COMPONENTS**: Multi-tenancy, RBAC, organization-wide dashboard, billing.

### 3. IT Helpdesk Investigation Tool
- **CUSTOMER**: Corporate IT support staff handling employee "Is this email safe?" tickets.
- **PROBLEM**: IT techs spending 15 minutes per ticket manually inspecting raw email headers.
- **SENTRYL VALUE**: Drag-and-drop `.eml` upload returning instant forensic dossier in < 5 seconds.
- **REQUIRED INTEGRATIONS**: Jira Service Management, ServiceNow ticketing webhooks.
- **CURRENT READINESS**: **HIGH (70%)**. `/api/analyze-eml` delivers complete analysis immediately.
- **MISSING COMPONENTS**: Webhook dispatch, PDF/STIX incident report export button.

### 4. SOC Analyst Investigation Layer (Tier-1 Triage)
- **CUSTOMER**: Enterprise Security Operations Centers (SOCs) and MSSPs.
- **PROBLEM**: High volume of user-reported phishing alerts causing alert fatigue.
- **SENTRYL VALUE**: Automated extraction of IOCs, attack graphs, and RFC authentication summaries for ingestion.
- **REQUIRED INTEGRATIONS**: Splunk, Microsoft Sentinel, Cortex XSOAR, MISP.
- **CURRENT READINESS**: **MEDIUM (50%)**. Produces structured JSON IOCs and attack graphs.
- **MISSING COMPONENTS**: STIX/TAXII 2.1 export formats, API authentication, SIEM connector scripts.

### 5. Educational / Cybersecurity Training Platform
- **CUSTOMER**: Universities, cybersecurity bootcamps, corporate security awareness trainers.
- **PROBLEM**: Students lack interactive visual tools to understand email headers and attack infrastructure.
- **SENTRYL VALUE**: Interactive attack graphs, breakdown of SPF/DKIM mechanics, and evasion tactics visualizer.
- **REQUIRED INTEGRATIONS**: Canvas/Moodle LMS, preloaded forensic challenge datasets.
- **CURRENT READINESS**: **HIGH (80%)**. UI visualizers and breakdown items make email mechanics intuitive.
- **MISSING COMPONENTS**: Student progress tracking, interactive quiz/challenge mode.

### 6. Enterprise Email Gateway Integration (MTA In-Line)
- **CUSTOMER**: Large enterprises processing millions of messages daily.
- **PROBLEM**: Inline blocking and quarantine before delivery to inboxes.
- **SENTRYL VALUE**: Lightweight, fast heuristic and forensic engine.
- **REQUIRED INTEGRATIONS**: Postfix/Milter, Haraka, Microsoft 365 Mail Flow Rules.
- **CURRENT READINESS**: **LOW (20%)**. Sentryl is currently an HTTP API, not an SMTP daemon.
- **MISSING COMPONENTS**: SMTP/Milter protocol handler, asynchronous queue, high-availability clustering.

---

## SECTION L: CRITICAL FIXES (PRIORITIZED ROADMAP)

```
========================================================================================
TECHNICAL REMEDIATION ROADMAP (POST-AUDIT):
========================================================================================
[P0 - MUST FIX BEFORE PRODUCTION DEPLOYMENT]
1. Streaming Upload Byte Enforcement: Read file stream in 64KB chunks to prevent OOM DoS.
2. Keyed Tamper Seal (HMAC/PKI): Implement server-side HMAC-SHA256 secret for evidence vault.
3. API Authentication & Rate Limiting: Add X-Sentryl-Key and slowapi 60 req/min rate limiter.
4. Persistent Database Integration: Migrate _REPORTS_CACHE to PostgreSQL with TTL eviction.

[P1 - IMPORTANT FOR SCALING & GENERALIZATION]
5. Production Dataset Expansion: Retrain ML model on 10,000+ real samples without data leakage.
6. True K-Fold CV Pipeline: Refit feature extractor and model strictly inside validation folds.
7. Attachment Critical Override: Elevate executable attachments (.exe, double ext) to High risk.
8. STIX 2.1 / MISP Exporter: Enable one-click export of extracted IOCs for SOC analysts.

[P2 - FUTURE ENHANCEMENTS]
9. Dynamic Sandbox Connector: Optional webhook integration with Cuckoo/CAPE sandbox for URLs.
10. Multi-Tenant RBAC: Organization accounts, role-based access, and enterprise billing.
========================================================================================
```

---

## SECTION M: DEMO-SAFE CLAIMS (WHAT TO DEFEND WITH PRIDE)

When presenting Sentryl to SIH judges, defend these genuine achievements with complete confidence:

1. **"Authentic RFC 822 / MIME Protocol Analysis"**: Sentryl genuinely parses raw headers, MIME parts, and attachments using standard Internet protocols.
2. **"Deterministic, Transparent Risk Scoring"**: Every point in our 0–100 score is explained with itemized evidence; no black-box mysteries.
3. **"Safe Static URL Lexical Inspection"**: We extract entropy, punycode, and open-redirect markers without making dangerous outbound network requests.
4. **"Advanced Evasion Detection"**: We detect zero-width Unicode characters, Cyrillic homoglyphs, and hidden CSS font manipulations designed to bypass traditional filters.
5. **"Evidence-Grounded Attack Graphs"**: Every node and edge in our attack graph is derived strictly from observed email entities.
6. **"Privacy-First Architecture"**: In Privacy Mode, PII is masked before analysis; in offline mode, zero data leaves the local server.
7. **"Fast & Lightweight"**: Complete email triage executes in under 40 milliseconds.

---

## SECTION N: CLAIMS WE MUST NOT MAKE (FATAL DEMO MISTAKES)

Avoid these fatal overstatements during the judge defense:

1. **DO NOT CLAIM "100% Machine Learning Accuracy"**: State honestly: *"Our ML classifier is a functional prototype evaluated on a curated benchmark; our operational defense relies on our deterministic heuristic engine."*
2. **DO NOT CLAIM "URL Detonation Sandbox"**: State honestly: *"We perform safe, static lexical URL analysis and entropy inspection, avoiding dynamic execution risks."*
3. **DO NOT CLAIM "Legally Admissible Courtroom Evidence"**: State honestly: *"We provide technical cryptographic tamper-evidence and chain-of-custody tracking."*
4. **DO NOT CLAIM "Replaces Enterprise Gateways"**: State honestly: *"Sentryl is an analyst triage accelerator and investigation workbench, designed to augment existing email infrastructure."*
5. **DO NOT CLAIM "Pinpoints Physical Attacker Address"**: State honestly: *"IP geolocation reveals ISP routing and regional ASN allocations, not physical street addresses."*

---

```
========================================================================================
FINAL RED-TEAM AUDIT SUMMARY:
========================================================================================
RED TEAM STATUS: REVIEW COMPLETE & DEFENSIVE POSITION LOCKED
CRITICAL:        0
HIGH:            2 (ML pre-split data leakage, streaming upload OOM risk)
MEDIUM:          3 (Unauthenticated API, unkeyed tamper seal, unbounded in-memory cache)
LOW:             2 (Synthetic chain-of-custody deltas, Gmail DOM selector maintenance)
BLOCKERS:        0 (System is fully functional, stable, and all 41 tests pass)
DEMO READY:      YES (As a SOC Analyst Triage Workbench & Technical Prototype)
========================================================================================
```
