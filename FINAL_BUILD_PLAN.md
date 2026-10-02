# SENTRYL (SIH26106) — FINAL MASTER BUILD PLAN
**Project**: Sentryl — AI-Powered Email Threat Detection & Forensic Intelligence  
**Role**: Principal Cybersecurity Engineer + ML Engineer + SOC Architect + SIH Technical Judge  
**Date**: September 2026  
**Target Directory**: `d:\#final - 2nd face`  

---

## 1. CURRENT STATE

- **Architecture**: FastAPI backend (`backend/main.py`), browser extension (Manifest V3 in `extension/`), static and template-driven reporting (`report.html`, `dashboard/`).
- **Test Suite**: 41 automated pytest unit/integration tests passing in ~2.9s.
- **Strengths**: Authentic RFC 822 `.eml` parsing, deterministic SPF/DKIM/DMARC evaluation, Levenshtein domain spoofing, Shannon entropy URL analysis, zero-width space/homoglyph evasion detection, single-incident attack graph, SHA-256 acquisition hashing, Privacy Mode PII masking.
- **Identified Flaws (From Red-Team Audit)**:
  1. **ML Data Leakage**: Augmentation before splitting and pre-fitted model evaluation in K-fold CV. Only 20 base samples (doubled to 40).
  2. **Streaming Upload OOM**: `await file.read()` reads entire payload into RAM before checking the 10MB limit in `/api/analyze-eml`.
  3. **Unkeyed Evidence Tamper Seal**: `tamper_seal_hash` is computed as unkeyed `sha256(f"{eid}::{raw_hash}::{now_iso}")`, vulnerable to client-side forgery if modified.
  4. **Unbounded In-Memory Report Cache**: `_REPORTS_CACHE` in `report_store.py` has no entry cap or TTL eviction.
  5. **Synthetic Chain-of-Custody Deltas**: 10ms negative offsets simulated from `t0`.
  6. **Attachment Risk Ceiling**: Executable files alone only contribute 15 points (Low Risk), lacking a critical override floor.
  7. **Unauthenticated Admin/Maintenance Endpoints**: No separation between public demo endpoints and internal cache/maintenance operations.

---

## 2. CRITICAL FIXES (P0 - MANDATORY)

1. **Fix ML Pre-Split Data Leakage & Overhaul Pipeline**:
   - Split raw data *before* any feature extraction.
   - Fit `DualBranchFeatureExtractor` (TF-IDF + structured features) *strictly* on training folds.
   - Train `LogisticRegression` on training fold vector, evaluate on held-out validation fold.
   - Generate genuine, authentic `backend/ml/evaluation_report.json`.
   - Explicitly label as: `"Baseline ML prototype evaluated on a small benchmark dataset (20 raw curated samples; 10 benign, 10 malicious)."`.
2. **Streaming Upload Protection & File Size Limits**:
   - In `/api/analyze-eml`, stream the file in 64KB chunks up to `10 * 1024 * 1024` bytes (10MB).
   - Abort immediately with HTTP 413 if cumulative bytes exceed 10MB, without buffering excess bytes into memory.
   - Cap maximum MIME parts walked and attachment count to prevent recursive parser bombs.
3. **Keyed Evidence Vault & Authentic Timeline**:
   - Upgrade evidence sealing in `evidence_vault.py` to HMAC-SHA256 using server secret (`EVIDENCE_HMAC_SECRET`).
   - Remove synthetic millisecond deltas (`t0 - 40ms`). Record genuine real-time acquisition and hashing timestamps.
   - Retain explicit disclaimer: `"TAMPER-EVIDENT EVIDENCE HANDLING / INTEGRITY VERIFICATION"`.
4. **Bounded In-Memory Cache with TTL & LRU Eviction**:
   - Refactor `report_store.py` to enforce `MAX_CACHE_ENTRIES = 500` and `TTL = 86400s` (24h).
   - Automatically evict oldest entries when limit is reached.

---

## 3. HIGH PRIORITY FIXES (P1)

1. **Attachment Critical Floor Override**:
   - In `risk_scorer.py`, if high-risk executable attachments (`.exe`, `.scr`, `.bat`, double extensions like `.pdf.exe`) are present, enforce an automatic floor of High Risk (>= 65), preventing malicious files from being classified as "Low Risk".
2. **API Endpoint Role Separation & Access Control**:
   - Separate PUBLIC / DEMO endpoints (`/api/scan`, `/api/analyze-eml`, `/api/report/{id}`, `/api/verify-integrity`) from PROTECTED / INTERNAL maintenance endpoints (`/api/admin/clear-cache`, `/api/admin/stats`).
   - Protect administrative actions via `X-Sentryl-Key` header with configurable secret.
3. **Gmail Extension Resilient Error Boundaries**:
   - In `extension/content/gmail.js`, wrap DOM lookups in defensive try/catch blocks.
   - If selectors fail, display: `"Sentryl notice: Gmail webmail layout altered or unsupported. Use the .EML upload tool for full forensic analysis."` rather than throwing uncaught exceptions.

---

## 4. DIFFERENTIATION FEATURES (THE "WHY SENTRYL?" EXPERIENCE)

1. **The "Why This Email?" Experience**:
   - Top 3–7 strongest evidence signals clearly highlighted in plain English with exact numerical score contribution and observed fact.
   - Distinct **User Mode** (simple verdict + why + safe actions) vs **Analyst Mode** (full technical evidence, RFC headers, IOCs, attack graph, evidence seal).
2. **Hero Forensic Transmission Timeline**:
   - Parse RFC 5321 `Received:` headers into chronological relay hops with genuine header timestamps (or `"Timestamp unavailable in header"`).
   - Display hop number, transmitting server, receiving server, IP, and security checks.
3. **Comprehensive IOC Extraction & Investigation Panel**:
   - Extract real IPs, domains, URLs, sender addresses, Message-ID, attachment hashes.
   - Structured IOC table with Type, Value, Source, Confidence, and Copy/Export capabilities.
4. **Evidence-Driven Attack Graph**:
   - Clean entity-relationship star/tree topology linking Email -> Sender -> Domain -> Auth -> URLs -> IP -> ASN -> Attachments -> Hashes.
   - Clicking nodes reveals provenance and risk explanation.
5. **Dedicated BEC & Adversarial Evasion Detectors**:
   - Distinct sections for executive impersonation, wire transfer diversion, zero-width spaces, Cyrillic homoglyphs, and hidden CSS.

---

## 5. DEMO FEATURES (3-5 MINUTE JUDGE WALKTHROUGH)

- Controlled demonstration scenario suite:
  1. `legitimate_security_alert.eml` (Google security alert, valid SPF/DKIM, score < 15, Clean)
  2. `credential_phishing_paypal.eml` (Lookalike domain, raw IP URL, score > 80, Critical)
  3. `bec_executive_wire_fraud.eml` (CEO impersonation, urgent wire transfer, score > 70, High)
  4. `suspicious_attachment_trojan.eml` (Double extension `.pdf.exe`, high entropy, score > 75, High)
- One-click "Verify Evidence Integrity" showing cryptographic green checkmark, plus tamper test showing immediate detection of altered bytes.

---

## 6. TEST PLAN

Expand the 41-test suite to include:
1. `test_ml_pipeline_leak_free_cv()`: Validates TF-IDF is fit exclusively on train folds.
2. `test_eml_upload_streaming_size_limit()`: Verifies HTTP 413 on files exceeding 10MB.
3. `test_cache_lru_and_ttl_eviction()`: Confirms cache never exceeds 500 entries.
4. `test_keyed_tamper_seal_verification()`: Confirms HMAC verification and detects forged seals.
5. `test_attachment_critical_risk_floor()`: Confirms `.exe` attachment elevates clean email to High Risk.
6. `test_admin_endpoint_security()`: Validates protected endpoints reject unauthorized requests.

---

## 7. FILES EXPECTED TO CHANGE

- `backend/ml/dataset.py` (Clean benchmark samples, remove pre-split duplicate augmentation)
- `backend/ml/feature_extractor.py` (Ensure clean fit/transform separation)
- `backend/ml/train_model.py` (Pipeline-based training without leakage)
- `backend/ml/evaluate_model.py` (True K-fold CV where estimator & vectorizer are fitted strictly on train fold)
- `backend/ml/evaluation_report.json` (Real leak-free evaluation metrics)
- `backend/services/ml_inference.py` (Robust inference bundle loading)
- `backend/routers/scan.py` (Streaming upload 64KB chunks with 10MB limit; User vs Analyst view payload)
- `backend/services/evidence_vault.py` (HMAC-SHA256 tamper seal, eliminate synthetic millisecond deltas)
- `backend/services/report_store.py` (Bounded LRU/TTL cache)
- `backend/services/risk_scorer.py` (Attachment critical floor override, provenance breakdown)
- `backend/services/header_parser.py` (Authentic chronological hop timeline)
- `backend/config.py` (Configurable `EVIDENCE_HMAC_SECRET`, `ADMIN_API_KEY`, cache settings)
- `backend/main.py` (Admin router inclusion, clean CORS)
- `extension/content/gmail.js` (Defensive error boundaries)
- `backend/tests/test_master_verification.py` (Comprehensive new security and regression tests)

---

## 8. FILES THAT MUST NOT BE REWRITTEN

- `backend/models/schemas.py` (Preserve stable core Pydantic contract; only add optional fields if necessary)
- `backend/services/domain_checker.py` (Working Levenshtein and Punycode logic)
- `backend/services/url_checker.py` (Working static regex and Shannon entropy logic)
- `backend/services/nlp_engine.py` & `bec_detector.py` (Working heuristic pattern engines)
- `backend/services/evasion_detector.py` (Working zero-width and homoglyph logic)
- `backend/services/ip_intel.py` (Working RFC 1918 and local IP analysis logic)
- Existing tests in `backend/tests/` (Must continue to pass 100%)
