# Sentryl — Final System Architecture & Pipeline Specification

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Document Purpose:** Master system architecture diagram, data flow specification, and layer isolation model.

---

## 1. Master System Architecture Diagram

```
                    ┌──────────────────┐
                    │ Gmail / Webmail  │
                    └────────┬─────────┘
                             │
                       Sentryl Extension
                             │
                             ▼
                    ┌──────────────────┐
                    │   FastAPI API    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ RFC822 / MIME    │
                    │ Parser           │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 Authentication        Identity              Content/NLP
 SPF/DKIM/DMARC        Domain/URL            BEC/Evasion
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                    ┌──────────────────┐
                    │ ML Auxiliary     │
                    │ Signal            │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Explainable      │
                    │ Risk Engine      │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
             IOCs        Timeline       Attack Graph
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌──────────────────┐
                    │ Evidence Vault   │
                    │ HMAC Integrity    │
                    └────────┬─────────┘
                             ▼
                    SOC Analyst Report
```

---

## 2. Layer-by-Layer Technical Specification

### Layer 1: Ingestion Plane
- **Browser Extension (Manifest V3):** Operates on Gmail webmail DOM (`extension/content/gmail.js`). Extracts subject, sender display name, envelope address, body text, and hyperlinks. Includes defensive fallback banners if Gmail DOM classes change.
- **Standalone .EML Upload (API Plane):** Direct protocol-level ingestion via `POST /api/analyze-eml`. Enforces 64KB chunk inspection up to a strict 10MB ceiling (`MAX_EML_SIZE_BYTES = 10MB`), immediately raising HTTP 413 if exceeded.

### Layer 2: Parser & Transit Extraction
- **RFC 822 / MIME Parser (`backend/services/eml_parser.py`):** Parses raw headers and body parts with recursion guards (`MAX_MIME_PARTS = 100`) and attachment count guards (`MAX_ATTACHMENTS = 20`).
- **Multiline Relay Tracing (`backend/services/header_parser.py`):** Unfolds multiline `Received:` headers and traverses chronologically from the initial submission client to the destination gateway. Isolates RFC 1918 private subnets and calculates hop latencies ($\Delta t$).

### Layer 3: Security Vectors (Deterministic-First)
1. **Authentication:** Evaluates RFC 7208 (SPF), RFC 6376 (DKIM), and RFC 7489 (DMARC) domain alignment and Return-Path divergence.
2. **Domain & URL Identity:** Computes Levenshtein edit distance against high-value brand whitelists, normalizes Punycode IDNs (`xn--`), detects Cyrillic homoglyphs, flags raw IP hostnames, identifies open redirect parameters (`?redirect=`), and calculates Shannon lexical entropy.
3. **Content & BEC:** Analyzes executive impersonation lures, financial wire transfer requests, coercive urgency, and secrecy pressure.
4. **Evasion Detection:** Detects zero-width unicode spaces (`\u200b`), mixed-script character injection, and CSS micro-font text hiding (`font-size:0px`).
5. **Safe Attachment Analysis:** Computes SHA-256 digests, identifies Portable Executable (PE) headers, evaluates Shannon entropy, and flags double extensions (`.pdf.exe`). Zero dynamic code execution.

### Layer 4: Auxiliary Machine Learning Signal
- **Dual-Branch Model (`backend/ml/`):** Combines sublinear TF-IDF n-grams with 16 handcrafted structural security features using regularized Logistic Regression (`backend/models/ml_model.joblib`).
- **Role:** Calibrated probability score ($P \in [0.0, 1.0]$) contributing 0 to 20 points as an auxiliary corroborating signal. Validated using leak-free 5-fold cross-validation on our 20-sample curated benchmark with **1.81ms CPU inference latency**.

### Layer 5: Explainable Bounded Risk Engine
- **Formula:** Bounded 0–100 mathematical composition across all 6 pillars plus auxiliary ML.
- **Attachment Critical Floor Override:** Enforces an automatic minimum floor of **65 / 100 (High Risk)** for executable binaries (`.exe`, `.scr`, `.bat`, `.pdf.exe`).
- **Provenance:** Every breakdown item is tagged with strict epistemological origin (`OBSERVED`, `INFERRED`, `EXTERNAL`, `MODEL`).

### Layer 6: Forensics & Cryptographic Evidence Vault
- **IOC Normalization:** Categorizes public IPv4/v6, hostnames, URLs, and file hashes with SOC containment actions (`BLOCK`, `INVESTIGATE`, `MONITOR`, `ALLOW`).
- **Attack Graph:** Constructs interactive SVG topology linking the email, sender, domain, routing IP, and indicators.
- **Keyed HMAC Sealing:** Canonicalizes evidence metadata into sorted JSON, computes a SHA-256 acquisition digest, and seals the record with server-side HMAC-SHA256 (`EVIDENCE_HMAC_SECRET`).
- **Independent Verification:** Exposes `POST /api/verify-integrity` to test bit-for-bit integrity.

### Layer 7: Dual-Mode Presentation & Export
- **User View:** Non-technical verdict, plain English summary, top "why" reasons, and safe immediate actions.
- **Analyst View:** Deep technical breakdowns, score composition, MITRE ATT&CK mappings, and raw evidence hashes.
- **Markdown Export:** One-click standardized forensic report export via `GET /api/report/{id}/markdown`.
