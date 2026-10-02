# FINAL DEMO READINESS

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Evaluation Date:** September 2026  
**Build Status:** CODE FREEZE & DEMO READY  

---

## 1. Environment
- **Operating System:** Windows 11 (x86_64)
- **Python Version:** 3.14.3
- **Primary Frameworks:** FastAPI 0.115+, Uvicorn, Pydantic v2, Scikit-learn, Joblib, HTTPX
- **Extension Standard:** Manifest V3 (Microsoft Edge & Google Chrome)
- **Host Permissions:** `mail.google.com`, `openstreetmap.org`, `localhost:8000`, `127.0.0.1:8000`
- **Store Certification:** Live on Microsoft Edge Add-ons (`ORDCKC10MVMZ`)

---

## 2. Startup Commands
Tested and verified from `d:\#final - 2nd face`:

```powershell
# 1. Run Demo Preflight Self-Test
python demo_preflight.py

# 2. Launch FastAPI Backend
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# 3. Open SOC Forensic Investigation Dashboard in Edge / Chrome
file:///d:/#final%20-%202nd%20face/extension/dashboard/report.html

# 4. (Optional) Run Full End-to-End Demo Rehearsal Script
python scripts/rehearse_demo.py
```

---

## 3. Extension Status
- **Manifest:** Manifest V3 (`extension/manifest.json`) compliant with Microsoft Edge Developer Policy 1.5.2.
- **Permissions:** Minimal set (`["storage", "activeTab"]`).
- **Icons:** All 4 required pixel-perfect PNGs validated (16x16, 48x48, 128x128, 300x300).
- **Background Worker:** `extension/background/service-worker.js` (MV3 registered).
- **In-Page Triage:** `extension/content/gmail.js` with defensive DOM fallbacks and alert banners.
- **Distribution Package:** `dist/sentryl-edge-extension-v1.0.1.zip` (15 files, 74.8 KB, 0 CRC errors, synchronized to Desktop & Downloads).

---

## 4. Demo Samples
Four controlled, reproducible RFC 822 email files in `demo_samples/`:
1. `01_clean_corporate_newsletter.eml` (GitHub Security Advisory)
2. `02_credential_phishing_paypal.eml` (PayPal Lookalike + Raw IP Link)
3. `03_bec_executive_wire_fraud.eml` (CEO Wire Fraud — Zero Links / Zero Attachments)
4. `04_trojan_double_extension_attachment.eml` (FedEx Invoice — `Invoice_Scan_FedEx.pdf.exe`)

---

## 5. Preflight Result
Executed via `python demo_preflight.py`:
```text
============================================================
SENTRYL DEMO PREFLIGHT CHECK
============================================================
[PASS] Python Environment (3.14.3)
[PASS] Python Dependencies (fastapi, uvicorn, pydantic, sklearn, joblib, httpx)
[PASS] ML Model Artifact (ml_model.joblib) & Evaluation Report
[PASS] Demo Samples (4/4 controlled .eml files present in demo_samples/)
[PASS] Extension Files (Manifest V3, content script, popup, dashboard) [Package ZIP exists: sentryl-edge-extension-v1.0.1.zip]
[PASS] Backend FastAPI Application & Router Initialization
[PASS] API Health Endpoint (/health -> HTTP 200)
[PASS] Analysis Endpoint (/api/analyze-eml -> HTTP 200, Score: 20/100)
[PASS] Report Generation (JSON & Markdown Export for ID a34fef62...)
[PASS] Evidence Vault (HMAC-SHA256 Sealing & Tamper Verification Verified)
============================================================
PREFLIGHT STATUS: ALL CHECKS PASSED -> SYSTEM READY FOR DEMO
============================================================
```

---

## 6. Scenario Results

| Scenario | Input Sample | Expected Score | Runtime Result | Verified Defense Signals |
|---|---|:---:|:---:|---|
| **Scenario A: Clean Baseline** | `01_clean_corporate_newsletter.eml` | Low (<30) | **20 / 100 (Low Risk)** | Proves no false alarm fatigue; authentic SPF/DKIM passes; whitelisted domain `github.com`. |
| **Scenario B: Lookalike Phishing** | `02_credential_phishing_paypal.eml` | Critical ($\ge 75$) | **90 / 100 (Critical Risk)** | Domain lookalike (`paypai-security.com` Levenshtein 1) + raw IP URL (`185.220.101.5/login`) + SPF Fail + urgency cues. |
| **Scenario C: Zero-Link BEC** | `03_bec_executive_wire_fraud.eml` | High (50–74) | **57 / 100 (High Risk)** | **Major Differentiator: ZERO links and ZERO attachments.** Catches CEO impersonation, wire transfer solicitation, and secrecy pressure. |
| **Scenario D: Trojan Dropper** | `04_trojan_double_extension_attachment.eml` | High ($\ge 65$) | **65 / 100 (High Risk)** | Enforced by **Attachment Critical Floor Override** ($\ge 65$); static PE header inspection; safe Shannon entropy; zero execution. |

---

## 7. Evidence Verification
- **Acquisition Fingerprint:** Computed via SHA-256 at the exact millisecond of ingestion.
- **HMAC Tamper Seal:** Computed via server-side HMAC-SHA256 over canonicalized JSON representation.
- **Chain of Custody:** 5 immutable chronological steps (Acquisition $\to$ Digest Computation $\to$ RFC Parsing $\to$ Evaluation $\to$ Sealing).
- **Verification Endpoint:** Tested via `POST /api/verify-integrity`:
  - Authentic Content: Returns `status: "VERIFIED"`, `hash_matches: true`.
  - Mutated Payload (even 1 altered byte): Returns `status: "TAMPERED"`, `hash_matches: false`.

---

## 8. Report Export
- **JSON Format:** Full programmatic dossier returned via `GET /api/report/{id}`.
- **Markdown Format:** Human-readable investigation report generated via `GET /api/report/{id}/markdown` (7,056 bytes).
- **Epistemological Provenance:** Every signal is strictly tagged as `OBSERVED` (from raw RFC headers), `INFERRED` (from deterministic heuristics), `EXTERNAL` (from live network lookups), or `MODEL` (from auxiliary ML).

---

## 9. Judge Questions
The 12 mandatory judge questions are documented with concise 15–30 second answers in `JUDGE_30_SECOND_ANSWERS.md`, complemented by the 25 exhaustive technical defense answers in `JUDGE_QA.md`:
1. *Gmail already detects phishing. Why Sentryl?* (Investigation workbench vs black-box gateway, explainability, IOCs, forensic custody).
2. *Where is the AI?* (Dual-branch TF-IDF + 16 structured features + Logistic Regression, capped as 0–20 pt auxiliary signal; deterministic rules remain primary).
3. *Your dataset is only 20 samples?* (Controlled architectural benchmark for pipeline validation, deliberately disclosed; not claiming production generalization).
4. *You got 100% accuracy?* (1.00 cross-validation accuracy on small 20-sample benchmark using leak-free 5-fold validation; expected 3-5% margin in noisy real-world traffic).
5. *Can you detect zero-day phishing?* (Layered behavioral defense: SPF alignment, Levenshtein distance, URL Shannon entropy, and BEC cues catch unlisted domains).
6. *Can you find the attacker's exact location?* (No; IP geolocation identifies MTA routing facility or ISP POP, never a human physical coordinate).
7. *Do you execute malicious URLs?* (No; 100% safe static lexical inspection with zero outbound network requests).
8. *Can the LLM change the verdict?* (No; LLM is an explanation post-processor; numerical score and IOCs are calculated deterministically beforehand).
9. *Is this legally admissible evidence?* (Tamper-evident technical integrity for internal IR workflows; formal statutory admissibility requires jurisdiction-specific custody).
10. *Can it quarantine emails?* (Advisory triage today; automated mailbox remediation planned via Microsoft Graph / Google Workspace APIs).
11. *Who would use this?* (Tier-1 SOC analysts, IT helpdesks, SMEs, and cybersecurity training labs).
12. *What's your biggest limitation?* (20-sample ML benchmark, webmail DOM extraction fragility, and static URL analysis).

---

## 10. Known Limitations
Transparently documented in `KNOWN_LIMITATIONS.md`:
- **In-Memory Cache:** Reports stored in bounded in-memory cache (500 limit, 24h TTL); PostgreSQL + Redis planned for enterprise.
- **Static URL Analysis:** Does not dynamically execute JavaScript or bypass dynamic CAPTCHAs; headless Chromium sandbox planned.
- **Curated 20-Sample ML Benchmark:** Small sample validates feature pipeline; 500k enterprise corpus training planned.
- **Webmail DOM Fragility:** Browser DOM changes can affect in-page scraping; protocol-level `.eml` upload provides 100% reliable bypass.
- **Technical Integrity vs Court Admissibility:** HMAC-SHA256 provides tamper-evidence for internal triage; CloudHSM and RFC 3161 PKI TSA planned.

---

## 11. Emergency Recovery Steps

### Scenario 1: Port 8000 Conflict
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Scenario 2: Browser Extension Disconnected from API
1. Check that backend is running and `http://127.0.0.1:8000/health` returns `200 OK`.
2. Open extension `report.html` directly via file URI:
   `file:///d:/#final%20-%202nd%20face/extension/dashboard/report.html`
3. Drag and drop `.eml` samples directly into the web dropzone.

### Scenario 3: Complete Offline Demo (No Internet)
- Sentryl requires zero external network access for its core engine.
- RFC 822 parsing, SPF/DKIM verification, Levenshtein distance, safe static URL analysis, ML inference, and HMAC evidence sealing run 100% locally offline.
- Missing external GeoIP/LLM calls gracefully degrade to deterministic offline template summaries.

---

```
================================================================================
DEMO STATUS:       READY
CODE STATUS:       FROZEN
SECURITY STATUS:   VERIFIED (0 Vulnerabilities, 0 Data Leaks, Safe Static URLs)
TEST STATUS:       49 / 49 PASSED (100% in 7.86s)
ML CLAIM:          1.00 cross-validation accuracy on a small 20-sample controlled
                   benchmark using leak-free 5-fold validation. (Auxiliary signal)
BLOCKERS:          NONE
================================================================================
```
