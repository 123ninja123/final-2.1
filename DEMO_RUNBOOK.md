# Sentryl — SIH Grand Finale Demo Runbook (3–5 Minute Live Demonstration)

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Target Audience:** SIH Grand Finale Technical Evaluation Jury  
**Total Demonstration Time:** 3 minutes 30 seconds (with 1m 30s buffer for Judge Q&A)  
**Demo Sample Files:** Located in `demo_samples/`  

---

## 1. Pre-Demo Checklist & Environment Setup

Run this check 10 minutes prior to jury evaluation:

### Step 1: Start Backend API
```powershell
# In terminal from workspace root:
cd "d:\#final - 2nd face"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Verify:* Navigate to `http://127.0.0.1:8000/docs` in your browser. Ensure all endpoints respond.

### Step 2: Open SOC Forensic Dashboard
Open in Microsoft Edge or Google Chrome:
`file:///d:/#final%20-%202nd%20face/extension/dashboard/report.html`

### Step 3: Verify Demo Samples are Ready
Verify the 4 controlled test `.eml` files exist in `demo_samples/`:
1. `01_clean_corporate_newsletter.eml`
2. `02_credential_phishing_paypal.eml`
3. `03_bec_executive_wire_fraud.eml`
4. `04_trojan_double_extension_attachment.eml`

---

## 2. Minute-by-Minute Live Presentation Script

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TIMELINE OVERVIEW                                                                      │
│ 0:00 - 0:30 (30s) : Problem Statement & Gateway Gap                                    │
│ 0:30 - 1:15 (45s) : Scenario 1 — Clean Baseline & Dual-View (Low Risk)                │
│ 1:15 - 2:15 (60s) : Scenario 2 — Credential Phishing & Attack Graph (Critical Risk)   │
│ 2:15 - 3:00 (45s) : Scenario 3 — Zero-Link BEC Wire Fraud (High Risk)                 │
│ 3:00 - 3:45 (45s) : Scenario 4 — Trojan Attachment & Cryptographic Sealing (High Risk)│
│ 3:45 - 5:00 (75s) : Technical Defense & Judge Questions                                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Act 1: The Problem & The Gateway Gap (0:00 – 0:30)
*Action:* Show the opening slide or Sentryl SOC Dashboard home screen.  
*Spoken Script:*
> "Honorable judges, traditional email gateways act as binary black boxes: they deliver an email or silently quarantine it. When a targeted threat slips through, users receive at best a vague banner like *'Be careful with this message'*, while SOC analysts have zero explainability, no extracted IOCs, and no cryptographic evidence preservation.
>
> Sentryl is an analyst-assistive email threat detection and forensic intelligence platform. We combine deterministic RFC security protocols, lexical evasion detection, lightweight machine learning, and HMAC-sealed evidence custody to turn suspicious emails into structured forensic dossiers. Let's see it live on four distinct real-world vectors."

---

### Act 2: Clean Baseline Demonstration (0:30 – 1:15)
*Action:* Drag and drop `01_clean_corporate_newsletter.eml` onto the dashboard upload box (or run Terminal Scenario 1).  
*Observed Screen:*
- Risk Score: **20 / 100 (Low Risk)**
- Authentication: SPF Pass, DKIM Pass, DMARC Aligned.
- Toggle View: Show `user_view` vs `analyst_view`.
*Spoken Script:*
> "Here is a legitimate enterprise communication—a GitHub engineering update. Sentryl parses the RFC 822 MIME structure in under 20 milliseconds. Notice our Dual-View design:
> 1. For non-technical employees, the **User View** gives clear, jargon-free assurance: 'Verified legitimate sender with authentic cryptographic signatures.'
> 2. For the SOC team, the **Analyst View** itemizes every mathematical point: SPF passed, DKIM passed, domain alignment is 100% genuine, and the risk score remains firmly at 20 (Low Risk). No false positive alarms."

---

### Act 3: Credential Phishing & Lookalike Brand Spoofing (1:15 – 2:15)
*Action:* Drag and drop `02_credential_phishing_paypal.eml`.  
*Observed Screen:*
- Risk Score: **90 / 100 (Critical Risk)**
- Signals Triggered:
  - `DOMAIN_LOOKALIKE_DETECTED` (+20 pts) — `paypai-security.com` targeting `paypal.com` (Levenshtein distance: 1).
  - `URL_RAW_IP_DETECTED` (+20 pts) — Destination URL points directly to `http://185.220.101.5/login`.
  - `AUTH_SPF_FAIL` (+8 pts) — Sender IP not in authorized SPF record.
  - `CONTENT_URGENCY` (+10 pts) — Artificial urgency / account suspension lure.
- Visual Features: Click on the **SVG Attack Graph** and **IOC Table**.
*Spoken Script:*
> "Next, a deceptive credential harvesting campaign masquerading as PayPal security. Standard users often fall for this because the display name looks real.
> Sentryl intercepts this at **90/100 (Critical Risk)**. Notice the four independent corroborating pillars:
> - Our domain intelligence catches the Levenshtein homoglyph: the attacker substituted lowercase 'l' with an 'i' (`paypa-i`).
> - Our safe static URL inspector catches a raw external IP hostname without making dangerous outbound network requests.
> - Sentryl automatically constructs this **Attack Graph**, linking the email node to the sender domain, originating IP, and extracted IOCs, ready to push directly into a SIEM blocklist."

---

### Act 4: Zero-Link BEC / Executive Wire Fraud (2:15 – 3:00)
*Action:* Drag and drop `03_bec_executive_wire_fraud.eml`.  
*Observed Screen:*
- Risk Score: **57 / 100 (High Risk)**
- Threat Vector: Business Email Compromise (Zero links, zero attachments).
- Signals Triggered:
  - `BEC_EXECUTIVE_IMPERSONATION` (+15 pts) — Display name 'Satya Nadella' from unaligned domain `company-corp.work`.
  - `BEC_WIRE_FRAUD` (+15 pts) — Demands wire transfer / invoice payment.
  - `BEC_SECRECY_CUES` (+10 pts) — Demands strict confidentiality ('keep this strictly confidential').
  - `DOMAIN_SUSPICIOUS_TLD` (+12 pts) — High-abuse `.work` TLD.
*Spoken Script:*
> "Now, one of the most damaging threats in corporate cybercrime: Business Email Compromise. This email has **zero links and zero attachments**. Standard antivirus scanners score this completely clean.
> Sentryl detects the threat at **57/100 (High Risk)**. Our NLP and BEC heuristic engine isolates three high-confidence behavioral signals:
> 1. Executive role impersonation claiming to be the CEO from an unaligned external domain.
> 2. Direct solicitation of an urgent wire transfer.
> 3. Coercive secrecy pressure instructing the recipient not to contact anyone else.
> The platform warns the analyst immediately before wire approval occurs."

---

### Act 5: Trojan Payload & Cryptographic Chain of Custody (3:00 – 3:45)
*Action:* Drag and drop `04_trojan_double_extension_attachment.eml`. Then click **Verify Cryptographic Tamper Seal**.  
*Observed Screen:*
- Risk Score: **65 / 100 (High Risk)**
- Enforced By: **Attachment Critical Risk Floor Override** (clamped to $\ge 65$ for double executable `.pdf.exe`).
- Evidence Vault: Displays SHA-256 acquisition digest, HMAC-SHA256 signature, and 5-stage Chain of Custody.
- Tamper Verification: Displays `status: "VERIFIED"`, showing bit-for-bit mathematical integrity.
*Spoken Script:*
> "Our fourth scenario is a delivery lure carrying a Trojan payload: `Invoice_Scan_FedEx.pdf.exe`.
> Even if the sending domain passes SPF, Sentryl's **Attachment Critical Floor Override** guarantees an immediate High Risk floor ($\ge 65$).
> More importantly, look at the **Evidence Vault**. Sentryl computes a SHA-256 digest of the raw RFC 822 stream at the exact millisecond of ingestion, appends an immutable 5-stage chain of custody, and seals the record with server-side HMAC-SHA256.
> When we trigger the tamper verification audit, Sentryl recalculates the digest. If an attacker or insider modified even a single byte of the email headers, the verification immediately alerts: 'TAMPERED'. This provides forensic defensibility for internal incident response."

---

### Act 6: Markdown Forensics Export & SIEM Ingestion (3:45 – 4:00)
*Action:* Click **Export Markdown Report** (or navigate to `http://127.0.0.1:8000/api/report/{scan_id}/markdown`).  
*Spoken Script:*
> "Finally, with one click, the analyst exports a comprehensive Markdown Forensic Investigation Report. Every finding is tagged with strict epistemological provenance—clearly separating what was **OBSERVED** in the raw RFC headers, what was **INFERRED** by heuristics, and what was output by the **MODEL**.
> Sentryl provides transparent, explainable, and tamper-evident email defense."

---

## 3. Terminal Backup Commands (If Browser UI is Unavailable)

If presenting via terminal or API testbench:

```powershell
# Scenario 1: Clean Newsletter
curl -X POST "http://127.0.0.1:8000/api/analyze-eml" -F "file=@demo_samples/01_clean_corporate_newsletter.eml"

# Scenario 2: Credential Phishing
curl -X POST "http://127.0.0.1:8000/api/analyze-eml" -F "file=@demo_samples/02_credential_phishing_paypal.eml"

# Scenario 3: BEC Wire Fraud
curl -X POST "http://127.0.0.1:8000/api/analyze-eml" -F "file=@demo_samples/03_bec_executive_wire_fraud.eml"

# Scenario 4: Trojan Attachment
curl -X POST "http://127.0.0.1:8000/api/analyze-eml" -F "file=@demo_samples/04_trojan_double_extension_attachment.eml"

# Verify Evidence Integrity
curl -X POST "http://127.0.0.1:8000/api/verify-integrity" -H "Content-Type: application/json" -d '{"raw_content": "Received: ...", "expected_sha256": "..."}'
```

---

## 4. What to Say vs. What NOT to Say

| What to Say (Defensible & Accurate) | What NOT to Say (Overstated / Vulnerable) |
|---|---|
| "Sentryl is an analyst-assistive forensic intelligence workbench." | "Sentryl replaces Proofpoint, Mimecast, and Google Workspace gateways." |
| "Our safe static URL analysis inspects syntax, entropy, and redirects without sending outbound packets." | "We dynamically detonate malware and URLs in an isolated sandbox cloud." |
| "The ML model is an auxiliary signal (0–20 points) trained on a curated benchmark dataset." | "Our proprietary AI model detects 99.9% of all global phishing attacks." |
| "IP geolocation identifies the MTA routing data center or ISP node." | "We pinpoint the exact physical street address of the attacker." |
| "Evidence records are sealed with HMAC-SHA256 for tamper-evident audit integrity." | "Our evidence records are legally certified and admissible in high court." |
| "If external APIs timeout, the system gracefully falls back to deterministic rule evaluations." | "We have live integration with the entire global Dark Web threat intelligence network." |
