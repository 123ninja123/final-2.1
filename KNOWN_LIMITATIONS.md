# Sentryl — Known Technical Limitations & Engineering Boundaries

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Document Classification:** Engineering Transparency & Technical Disclosure  
**Version:** 1.0.2  

---

## 1. Architectural Honesty Declaration

Sentryl was built to provide an **explainable, auditable, and tamper-evident forensic intelligence workbench**. In keeping with professional software engineering ethics and SIH evaluation standards, this document provides a comprehensive catalog of the technical boundaries, constraints, and current limitations of the platform.

We do not conceal limitations; we document them as engineering boundaries with clear mitigation strategies and enterprise roadmap paths.

---

## 2. Catalog of Current Limitations

### 2.1 In-Memory Report Storage vs. Distributed Enterprise Persistence
- **Current Implementation:** Analysis reports are stored in an in-memory dictionary cache (`backend/services/report_store.py`) bounded to 500 entries with FIFO/LRU eviction and a 24-hour TTL.
- **Operational Limitation:** If the FastAPI backend service restarts, previously stored forensic reports in memory are cleared (though original `.eml` files remain preserved on disk). Under horizontal multi-container deployments (e.g., Kubernetes), requests must be pinned to the same container unless a shared cache is used.
- **Enterprise Roadmap Solution:** Integrate PostgreSQL with TimescaleDB for persistent incident history and Redis Cluster for distributed, multi-region cache synchronization.

### 2.2 Safe Static URL Inspection vs. Dynamic Hypervisor Sandbox Detonation
- **Current Implementation:** 100% safe static lexical and syntactical analysis (checking IP hostnames, Shannon entropy, open redirect parameters, and credential keywords) with zero outbound network requests.
- **Operational Limitation:** Static analysis cannot detect payloads behind dynamic CAPTCHA challenges, multi-stage JavaScript timing delays, or server-side IP cloaking (where the phishing server serves clean HTML to security scanners and malicious HTML to victims).
- **Enterprise Roadmap Solution:** Connect Sentryl's static pipeline to an asynchronous headless browser detonation sandbox (e.g., containerized Chromium / CAPE Sandbox) in an isolated, non-production VLAN.

### 2.3 Curated Benchmark ML Dataset vs. Multi-Million Enterprise Corpus
- **Current Implementation:** The dual-branch machine learning classifier is trained on a 20-sample hand-curated security benchmark dataset (10 benign, 10 malicious) with strict 5-fold cross-validation.
- **Operational Limitation:** While achieving 1.00 cross-validation accuracy on our small 20-sample controlled benchmark using leak-free 5-fold validation, the model cannot be expected to generalize to all corporate dialects, multilingual phishing lures, or complex obfuscation without larger training datasets. This metric must never be represented as "100% accurate AI".
- **Architectural Safeguard:** The ML score is strictly capped at 20 points out of 100. Sentryl relies on deterministic RFC 7208/6376/7489 authentication and domain heuristics as the primary arbiters of risk.
- **Enterprise Roadmap Solution:** Fine-tune the feature weights on an anonymized enterprise corpus of 500,000+ historical emails (incorporating SpamAssassin, Enron, and Nazario phishing archives).

### 2.4 External Threat Intelligence & Geolocation Resilience
- **Current Implementation:** Origin IP geolocation queries IP-API with a strict 1.5-second timeout and in-memory caching. Tor exit nodes are evaluated against local IP lists.
- **Operational Limitation:** When external network connectivity is restricted, or when public APIs rate-limit anonymous requests, external geolocation and WHOIS registration age are labeled *"Telemetry Unavailable"*. Sentryl strictly refuses to fabricate mock data.
- **Enterprise Roadmap Solution:** Package a local MaxMind GeoIP2 City database directly within the Docker container and integrate commercial API keys (VirusTotal, AlienVault OTX, AbuseIPDB).

### 2.5 Webmail DOM Extraction Dependency
- **Current Implementation:** The Chrome/Edge browser extension (`extension/content/gmail.js`) inspects live Gmail webmail DOM elements to extract sender identities, recipient fields, and rendered message text.
- **Operational Limitation:** If Google deploys major obfuscated class name changes or DOM structural updates to Gmail, automated in-browser DOM scraping can fail or require selector updates.
- **Architectural Safeguard:** Sentryl provides the standalone, protocol-level `.eml` upload API (`/api/analyze-eml`). Security analysts and users can drag-and-drop raw `.eml` files exported directly from any email client, completely bypassing webmail DOM scraping.
- **Enterprise Roadmap Solution:** Implement Microsoft Graph API and Google Workspace Admin SDK webhooks to ingest emails directly from mail server transport pipelines.

### 2.6 Cryptographic Tamper-Evidence vs. Statutory Legal Admissibility
- **Current Implementation:** Server-side HMAC-SHA256 signature keyed by `EVIDENCE_HMAC_SECRET` over canonicalized JSON with a chronological 5-stage Chain of Custody.
- **Operational Limitation:** Provides strong mathematical proof that an email payload has not been altered post-acquisition. However, it does not constitute statutory legal chain-of-custody under ISO/IEC 27037 or Federal Rules of Evidence without Hardware Security Module (HSM) key storage and an external RFC 3161 certified Time-Stamping Authority (TSA).
- **Enterprise Roadmap Solution:** Integrate AWS CloudHSM or Azure Key Vault for hardware-protected private signing keys and RFC 3161 TSA timestamping.

### 2.7 Automated Mailbox Quarantine Execution
- **Current Implementation:** Advisory triage platform. Generates itemized IOC tables, SOC actions (`BLOCK`, `INVESTIGATE`, `MONITOR`, `ALLOW`), and exportable Markdown/JSON forensic dossiers.
- **Operational Limitation:** Does not automatically reach into an end-user's Microsoft 365 or Google Workspace inbox to delete or move messages without human analyst intervention.
- **Enterprise Roadmap Solution:** Develop certified Microsoft 365 Exchange transport connectors and Google Workspace Marketplace add-ons with administrative remediation privileges.
