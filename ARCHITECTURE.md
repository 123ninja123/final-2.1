# Sentryl — Technical Architecture & Forensic Pipeline Specification

**SIH Problem Statement SIH26106:** "AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform"  
**Document Classification:** System Architecture, Data Flow & Component Status  
**Version:** 1.0.2 (Frozen Master Build)  

---

## 1. System Overview & End-to-End Pipeline

Sentryl operates a deterministic-first multi-vector detection and evidence preservation architecture. The analysis flow moves linearly from ingestion to forensic presentation:

$$\text{INPUT EMAIL} \longrightarrow \text{STREAMING INGESTION FIREWALL (10MB CEILING)} \longrightarrow \text{RFC 822 PARSER}$$
$$\longrightarrow \text{HEADER / RELAY EXTRACTION} \longrightarrow \text{AUTHENTICATION EVALUATION} \longrightarrow \text{DOMAIN & SENDER INTEL}$$
$$\longrightarrow \text{SAFE STATIC URL ANALYSIS} \longrightarrow \text{CONTENT & BEC ANALYSIS} \longrightarrow \text{IP / INFRASTRUCTURE TELEMETRY}$$
$$\longrightarrow \text{AUXILIARY MACHINE LEARNING} \longrightarrow \text{BOUNDED RISK SCORER WITH ATTACHMENT FLOOR}$$
$$\longrightarrow \text{KEYED HMAC EVIDENCE SEALING} \longrightarrow \text{DUAL-VIEW PAYLOAD GENERATION} \longrightarrow \text{ATTACK GRAPH & FORENSIC EXPORT}$$

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. STREAMING INGESTION FIREWALL                                                                        │
│    • Live In-Browser Triage: Microsoft Edge Manifest V3 Content Script (extension/content/gmail.js)    │
│    • Raw Forensic File Ingest: RFC 822 .eml MIME Stream Upload (POST /api/analyze-eml)                 │
│    • Ingestion Ceiling: 64KB chunk inspection up to 10MB; immediately raises HTTP 413 if exceeded      │
│    • Recursion Bounds: MAX_MIME_PARTS = 100, MAX_ATTACHMENTS = 20                                     │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. CRYPTOGRAPHIC ACQUISITION (services/evidence_vault.py)                                              │
│    • Calculates SHA-256 acquisition hash immediately upon receipt                                      │
│    • Normalizes metadata into Canonical JSON (sorted keys, compact delimiters)                         │
│    • Computes server-side Keyed HMAC-SHA256 signature using EVIDENCE_HMAC_SECRET                      │
│    • Generates Step 1 & 2 of the 5-stage Chain of Custody with real chronological timestamps           │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. RFC 5322 PARSING & TRANSIT RECONSTRUCTION (services/eml_parser.py & header_parser.py)               │
│    • Parses multiline Received headers chronologically from submission to gateway                      │
│    • Isolates RFC 1918 internal subnets from public Internet routers                                   │
│    • Calculates transit hop latencies (Δt) across timestamped headers                                  │
│    • Safely inspects MIME attachments: SHA-256, Shannon entropy, double extensions                     │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. MULTI-VECTOR DETERMINISTIC SECURITY EVALUATION                                                      │
│    • Authentication (services/spf_dkim_dmarc.py): SPF, DKIM, DMARC, Return-Path, DKIM d= alignment    │
│    • Domain Intel (services/domain_intel.py): Levenshtein distance, Punycode (xn--), homoglyphs, DNS  │
│    • Safe Static URL Analysis (services/url_checker.py): Raw IP hostnames, open redirects, entropy     │
│    • Content & BEC (services/bec_detector.py & nlp_engine.py): VIP name spoofing, wire diversion      │
│    • Evasion Detection (services/evasion_detector.py): Zero-width spaces, Cyrillic glyphs, CSS hidden │
│    • Origin Infrastructure (services/ip_intel.py): Inferred GeoIP, Tor directory check, ASN lookup    │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 5. REPRODUCIBLE MACHINE LEARNING LAYER (services/ml_inference.py & ml/)                                │
│    • Dual-branch feature vector: TF-IDF lexical n-grams + 16 structured security features              │
│    • Serialized L2 Logistic Regression classifier (backend/models/ml_model.joblib)                     │
│    • Validated on 20 curated benchmark samples with leak-free 5-fold stratified CV (1.81ms latency)     │
│    • Capped as an auxiliary scoring signal (0 to 20 points)                                            │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 6. BOUNDED RISK SCORING & PROVENANCE (services/risk_scorer.py)                                         │
│    • Configurable weights: Auth (20), Domain (20), URL (20), Content (20), Infra (10), Evasion (10)    │
│    • Attachment Critical Floor Override: Clamps score to ≥ 65/100 (High Risk) for executable payloads  │
│    • Generates exact signal breakdown items with epistemological provenance (OBSERVED, INFERRED)      │
│    • Constructs dual-view payloads: user_view (simple advice) and analyst_view (deep forensics)        │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 7. FORENSIC ARTIFACT ASSEMBLY & DOSSIER SEALING                                                        │
│    • Structured IOC Extractor (services/ioc_extractor.py): IPv4, IPv6, domains, URLs, mailboxes, hash │
│    • Attack Graph Topology (services/graph_builder.py): Nodes & directed relationship edges            │
│    • Advisory Grounded Summarizer (services/llm_explainer.py): Gemini API or deterministic fallback    │
│    • Standardized Markdown Report Export (services/report_generator.py via /api/report/{id}/markdown)  │
│    • Bounded In-Memory Cache (services/report_store.py): Max 500 reports with FIFO/LRU & 24h TTL       │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 8. PRESENTATION & AUDITING LAYER                                                                       │
│    • Microsoft Edge / Chrome Extension: Dual-mode toggle (User Tips vs SOC Analyst)                    │
│    • SOC Dashboard (extension/dashboard/report.html): SVG Attack Graph, Leaflet Map, IOC CSV/JSON      │
│    • Independent Verification API: POST /api/verify-integrity for tamper detection                     │
│    • Protected Admin Endpoints: /api/admin/stats and /api/admin/clear-cache (requires X-Sentryl-Key)   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Implementation Status Matrix

### A. IMPLEMENTED (Fully Operational, Tested & Verified)
| Component | Implementation File | Verification Evidence |
| :--- | :--- | :--- |
| **Streaming EML Ingest (Anti-DoS)** | `backend/routers/scan.py` | 10MB chunked streaming upload (HTTP 413) tested in `test_master_verification.py::test_eml_streaming_upload_limit_enforced`. |
| **RFC 822 / 5322 MIME Parser** | `backend/services/eml_parser.py` | Bounded recursion (`MAX_MIME_PARTS = 100`, `MAX_ATTACHMENTS = 20`) tested in `test_forensics_extended.py`. |
| **Componentized Risk Scorer** | `backend/services/risk_scorer.py` | Bounded 0–100 formula with exact signal provenance and attachment floor override ($\ge 65$). |
| **Attachment Risk Floor Override** | `backend/services/risk_scorer.py` | Clamps executable payloads to $\ge 65$ tested in `test_master_verification.py::test_attachment_critical_risk_floor`. |
| **Keyed HMAC Evidence Vault** | `backend/services/evidence_vault.py` | Canonical JSON + HMAC-SHA256 tested in `test_master_verification.py::test_keyed_tamper_seal_verification`. |
| **Tamper Verification API** | `POST /api/verify-integrity` | Cryptographically verifies bit-for-bit match; flags altered payloads with `status: TAMPERED`. |
| **Safe Static URL Inspector** | `backend/services/url_checker.py` | Static syntax, raw IP, open redirect, and Shannon entropy analysis (zero outbound packets). |
| **Dual-Branch ML Classifier** | `backend/ml/` & `ml_model.joblib` | 5-fold stratified cross-validation with zero leakage tested in `test_master_verification.py::test_ml_pipeline_leak_free_cv`. |
| **Dual-Mode View Payloads** | `backend/services/risk_scorer.py` | Outputs `user_view` and `analyst_view` in `ScanResponse`. |
| **Markdown Forensics Export** | `backend/services/report_generator.py` | `/api/report/{id}/markdown` export tested in `test_master_verification.py::test_markdown_investigation_report_export`. |
| **Protected Admin API** | `backend/routers/admin.py` | Admin routes with `X-Sentryl-Key` tested in `test_master_verification.py::test_admin_protected_endpoints`. |
| **Bounded Report Cache** | `backend/services/report_store.py` | Max 500 reports, FIFO/LRU eviction and 24h TTL tested in `test_master_verification.py::test_cache_lru_and_ttl_eviction`. |
| **Adversarial Evasion Engine** | `backend/services/evasion_detector.py` | Detects zero-width spaces (`\u200b`), Cyrillic homoglyphs (`\u0430`), and hidden CSS text (`font-size:0px`). |
| **BEC & Executive Spoofing** | `backend/services/bec_detector.py` | Detects VIP name impersonation, wire transfer demands, and Return-Path diversion channels. |
| **Safe Attachment Analyzer** | `backend/services/attachment_analyzer.py` | Static Shannon entropy calculation and double-extension detection (`.pdf.exe`, `.xlsx.exe`). Zero execution. |
| **RFC 5321 Multiline Relay Parser** | `backend/services/header_parser.py` | Reconstructs transit hops from bottom to top without synthetic Google MX hop injection. |
| **RFC 1918 Private IP Guard** | `backend/services/ip_intel.py` | Flags internal subnets (`10.0.0.0/8`, `192.168.0.0/16`) locally; never leaks intranet hops to public APIs. |
| **Observed vs Inferred Geolocation** | `backend/services/ip_intel.py` | Queries live IP-API with 1.5s timeout, LRU cache, Tor directory check, and honest disclaimer labels. |
| **Opt-In Privacy Mode** | `POST /api/scan (privacyMode=true)` | Masks PII (names, handles, internal IPs) before processing or LLM summarization. |

### B. PARTIAL (Functional Baseline with Documented Boundaries)
| Component | Current Reality | Documented Boundary |
| :--- | :--- | :--- |
| **External Threat Intel Feeds** | Static lexical heuristics (entropy, open redirects, suspicious TLDs) + local cache. | Paid external APIs (VirusTotal, AlienVault OTX) require enterprise API keys; system states "External reputation unavailable" rather than faking data. |
| **Domain Registration RDAP** | Real DNS MX validation + RDAP query structure with fallback. | Domain RDAP endpoints rate-limit anonymous queries; system flags "Registration age unavailable" if query times out. |
| **Grounded LLM Summarizer** | Evidence-grounded synthesis via Gemini API if `GEMINI_API_KEY` present; deterministic template if absent. | LLM is strictly an advisory post-processor and cannot modify numerical risk scores or tamper records. |

### C. PLANNED (Enterprise Post-SIH Roadmap)
| Component | Architecture Description | Target Phase |
| :--- | :--- | :--- |
| **Distributed Cache & Storage** | PostgreSQL / TimescaleDB for historical incidents + Redis Cluster for horizontal scaling. | v1.2 (Enterprise) |
| **Automated Mailbox Quarantine** | Microsoft Graph API & Google Workspace Admin connectors for one-click administrative remediation. | v1.3 (Enterprise) |
| **Hypervisor Sandbox Detonation** | Ephemeral micro-VM detonation for zero-day attachment dynamic behavioral tracing. | v2.0 (Forensics Core) |
| **RFC 3161 PKI Time-Stamping** | Integration with Hardware Security Modules (HSM) and certified external Time-Stamping Authorities. | v2.0 (Forensics Core) |

---

## 3. Unified Internal Schema Specification

```json
{
  "scan_id": "string (UUIDv4)",
  "risk_score": "integer (0 to 100)",
  "risk_level": "string ('low' | 'medium' | 'high' | 'critical')",
  "summary": "string (Analyst executive summary)",
  "checks": [
    { "name": "string", "status": "pass | warn | fail", "detail": "string" }
  ],
  "score_breakdown": {
    "auth_risk": "int (0-20)",
    "domain_risk": "int (0-20)",
    "url_risk": "int (0-20)",
    "content_risk": "int (0-20)",
    "infra_risk": "int (0-10)",
    "evasion_risk": "int (0-10)",
    "total_score": "int (0-100)",
    "breakdown_items": [
      {
        "signal": "string (e.g. DOMAIN_LOOKALIKE_DETECTED)",
        "weight": "int",
        "observed_value": "string",
        "contribution": "int",
        "points": "int",
        "category": "string",
        "reason": "string",
        "evidence": "string",
        "provenance": "string ('OBSERVED' | 'INFERRED' | 'EXTERNAL' | 'MODEL')"
      }
    ]
  },
  "user_view": {
    "verdict": "string ('Safe' | 'Suspicious' | 'Dangerous')",
    "plain_summary": "string (Non-technical explanation)",
    "why_reasons": ["string (Top bullet points)"],
    "safe_actions": ["string (Immediate steps for employee)"]
  },
  "analyst_view": {
    "technical_summary": "string",
    "mitre_attack_techniques": ["string"],
    "score_composition": { ... },
    "evidence_hash": "string (SHA-256)",
    "hmac_tamper_seal": "string (HMAC-SHA256)"
  },
  "authentication": {
    "status": "Pass | Warn | Fail",
    "spf": "boolean",
    "dkim": "boolean",
    "dmarc": "boolean"
  },
  "sender_analysis": {
    "domain": "string",
    "is_spoofed": "boolean",
    "target_brand": "string | null"
  },
  "url_analysis": {
    "status": "Safe | Suspicious | Malicious",
    "flagged_urls": [ ... ],
    "malicious_count": "int"
  },
  "content_analysis": {
    "nlp": { ... },
    "bec": { ... },
    "evasion": [ ... ]
  },
  "ip_analysis": {
    "geolocation": { "ip": "string", "country": "string", "city": "string", "isp": "string", "is_tor": "bool" }
  },
  "threat_intelligence": {
    "ml_prediction": {
      "phishing_probability": "float (0.0 to 1.0)",
      "confidence": "float",
      "prediction": "string",
      "top_features": [ ... ]
    }
  },
  "iocs": [
    {
      "ioc_type": "ipv4 | domain | url | email | sha256 | message_id",
      "value": "string",
      "source": "string",
      "risk": "safe | suspicious | malicious",
      "action": "block | investigate | monitor | allow"
    }
  ],
  "attack_graph": {
    "nodes": [ { "id": "string", "label": "string", "type": "string", "risk": "string" } ],
    "edges": [ { "source": "string", "target": "string", "label": "string" } ]
  },
  "evidence_record": {
    "evidence_id": "string",
    "raw_sha256": "string (64-char hex)",
    "canonical_hash": "string (64-char hex)",
    "hmac_signature": "string (64-char hex)",
    "integrity_status": "string ('UNVERIFIED' | 'VERIFIED' | 'TAMPERED')",
    "acquisition_timestamp": "ISO 8601 string",
    "file_size_bytes": "int",
    "chain_of_custody": [
      { "step": "int", "event": "string", "timestamp": "string", "actor": "string", "detail": "string" }
    ],
    "disclaimer": "string"
  }
}
```
