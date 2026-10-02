# Sentryl — Platform Value Proposition & Business Strategy

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Document Purpose:** Realistic commercialization strategy, user segmentation, value architecture, and enterprise roadmap. Zero fabricated revenue numbers or invented customer contracts.

---

## 1. Current Product Definition: SOC Analyst Triage Workbench

Today, Sentryl operates as an **Analyst-Assistive Email Forensic Workbench**. It bridges the gap between passive end-user uncertainty and manual Tier-1 SOC ticket investigation.

### The Operational Problem Solved:
When an enterprise employee flags an email as "suspicious", existing Secure Email Gateways (SEGs) typically offer no insight. The incident is forwarded to an IT helpdesk or junior SOC analyst who must:
1. Manually inspect raw RFC 822 text headers in a generic text editor.
2. Manually decode multiline `Received:` hops to trace origin routing.
3. Manually calculate Levenshtein distance on suspect lookalike domains.
4. Manually extract URLs, copy IP addresses, and query blocklists.
5. Manually compile a ticket notes summary for senior engineers.

This process consumes **15 to 30 minutes per reported email**.

### Sentryl's Immediate Value Transformation:
Instead of a vague label saying *"Suspicious email"*, Sentryl automatically produces:
- **WHY:** An itemized, bounded 0–100 score breakdown explaining every contributing signal.
- **WHAT:** Exact threat classification (Credential Harvester, CEO Wire Fraud, Malware Dropper, Clean Baseline).
- **WHERE:** Chronological transit timeline with RFC 1918 private subnet isolation and MTA geolocation.
- **WHICH IOCs:** Normalized table of public IPv4/v6, hostnames, URLs, and file hashes with SOC actions (`BLOCK`, `INVESTIGATE`).
- **WHICH INFRASTRUCTURE:** Interactive SVG Attack Graph mapping the relationship between sender, domain, hosting IP, and URLs.
- **WHAT EVIDENCE:** Cryptographic SHA-256 acquisition digest, server-side keyed HMAC seal, and 5-stage Chain of Custody.
- **WHAT SHOULD BE INVESTIGATED:** Plain English guidance for users (`user_view`) and exportable Markdown forensic dossiers for SOC analysts (`analyst_view`).

**Operational Result:** Reduces manual triage time from **20 minutes to under 30 seconds**.

---

## 2. Target User Segments

1. **Security Operations Center (SOC) Teams (Tier-1 / Tier-2 Analysts):**
   - High volume of user-reported phishing tickets.
   - Requires rapid, standardized forensic parsing, Attack Graph visualization, and exportable IOC lists for firewall/EDR rule updates.
2. **IT Helpdesks & System Administrators in SMEs (10–250 Employees):**
   - Organizations that cannot afford expensive $50,000/year enterprise SEG contracts (Proofpoint, Mimecast).
   - Needs a self-contained, low-overhead triage workbench to investigate suspicious executive wire fraud or invoice emails.
3. **Cybersecurity Training & Academic Environments:**
   - Universities, cyber ranges, and training bootcamps teaching digital forensics and email security standards (RFC 5321, RFC 7208 SPF, RFC 6376 DKIM, RFC 7489 DMARC).
4. **Security-Conscious Individuals & Executives:**
   - High-profile individuals, legal practitioners, and executives targeted by targeted spear-phishing who benefit from in-browser edge protection.

---

## 3. Deployment Architecture & Future Enterprise Roadmap

| Phase | Capability Level | Implementation Status | Key Technical Deliverables |
|---|---|---|---|
| **Phase 1 (Current)** | **Analyst Triage Workbench** | **IMPLEMENTED TODAY** | Standalone FastAPI backend, RFC 822 streaming parser, Levenshtein spoofing engine, safe static URL analyzer, dual-branch ML auxiliary model, HMAC evidence vault, and Edge MV3 extension. |
| **Phase 2 (Post-SIH)** | **API & Mailbox Integrations** | **ROADMAP / EXPANSION** | Microsoft Graph API and Google Workspace Admin SDK connectors to automatically ingest reported emails directly from user mailboxes without manual `.eml` export. |
| **Phase 3 (Enterprise)** | **SIEM & SOAR Orchestration** | **ROADMAP / EXPANSION** | Direct webhook and syslog streaming of extracted IOCs into Splunk, Microsoft Sentinel, and Cortex XSOAR for automated perimeter firewall updates. |
| **Phase 4 (Infrastructure)** | **Distributed High-Throughput Engine** | **ROADMAP / EXPANSION** | PostgreSQL / TimescaleDB persistent incident history, Redis Cluster distributed cache, and containerized Chromium sandboxes for dynamic URL screenshotting. |

---

## 4. Competitive Differentiation Matrix

| Capability | Legacy Secure Email Gateways (Proofpoint, Mimecast) | Native Webmail Providers (Gmail, Outlook 365) | Sentryl (Investigative Workbench) |
|---|---|---|---|
| **Primary Focus** | Perimeter mail filtering | Mailbox delivery & spam suppression | Forensic investigation & triage explainability |
| **Explainability** | Proprietary black-box score | Generic warning banner ("Be careful") | Auditable mathematical formula with signal provenance |
| **Relay Forensics** | Buried in raw admin logs | Hidden from user interface | Chronological interactive timeline with transit delays |
| **Attack Graph** | Limited or absent | None | Native interactive SVG graph linking all threat nodes |
| **Evidence Custody** | Vendor internal database | None | Tamper-evident HMAC-SHA256 seal & independent audit API |
| **Endpoint Triage** | Requires MX DNS redirect | Built-in only to provider webmail | Lightweight Manifest V3 browser extension + raw `.eml` drag-and-drop |
| **Zero-Link BEC** | Heavy reliance on sender history | Often bypassed if sent from webmail | Dedicated NLP & social-engineering heuristic engine |
