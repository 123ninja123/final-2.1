# Sentryl — SIH Grand Finale Controlled Demo Scenarios

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Status:** CODE FREEZE & DEMO READY  
**Test Samples Location:** `demo_samples/`  

---

## Scenario A — Clean Corporate Engineering Communication

### 1. Scenario Overview
- **File:** `demo_samples/01_clean_corporate_newsletter.eml`
- **Sender:** `GitHub Notifications <notifications@github.com>`
- **Subject:** `[GitHub] New security advisory published for dependency in sentryl-repo`
- **Expected Risk Level:** **Low Risk**
- **Expected Risk Score:** **20 / 100**
- **Purpose:** Proves Sentryl does not exhibit alert fatigue or trigger false positives on authentic corporate communications with legitimate cryptographic authentication.

### 2. Forensic Breakdown
- **Authentication:** SPF Pass (`140.82.112.4` authorized), DKIM Pass (`d=github.com`), DMARC Aligned (`From:` matches `d=`).
- **Domain Identity:** Matches verified enterprise brand whitelist `github.com`.
- **URL Inspection:** Verified `https://github.com/...` link with valid TLS, normal Shannon entropy, zero redirects.
- **Content:** Technical advisory text without coercive wire transfers, payment requests, or artificial panic.
- **Relay Chain:** Clean 1-hop transit from GitHub's verified mail infrastructure.

### 3. Key Takeaway to Emphasize to Judges:
> *"We test legitimate emails to prove Sentryl avoids false positives. When cryptographic authentication passes and brand alignment is verified, the score remains strictly in the Low Risk tier (20/100)."*

---

## Scenario B — Lookalike Credential Phishing

### 1. Scenario Overview
- **File:** `demo_samples/02_credential_phishing_paypal.eml`
- **Sender:** `PayPal Security Desk <support@paypai-security.com>`
- **Subject:** `URGENT: Your account has been restricted - Verify Identity Immediately`
- **Expected Risk Level:** **Critical Risk**
- **Expected Risk Score:** **90 / 100**
- **Purpose:** Demonstrates multi-vector detection where an attacker pairs a lookalike domain with a raw IP destination link and urgency lures.

### 2. Forensic Breakdown & Signals
- **Domain Spoofing (+20 pts):** `paypai-security.com` detected as lookalike of `paypal.com` (Levenshtein distance: 1; substituted lowercase 'l' with 'i').
- **URL Threat (+20 pts):** Direct raw external IPv4 address: `http://185.220.101.5/login?redirect=update-account` with credential keyword `/login`.
- **Authentication Failure (+20 pts):** SPF Hardfail (IP `185.220.101.5` unauthorized) + Return-Path divergence (`unauthorized-relay.suspicious.net`).
- **Content Urgency (+10 pts):** Coercive panic keywords (*"restricted"*, *"immediately"*, *"within 24 hours"*).
- **ML Auxiliary Signal (+20 pts):** High threat probability ($P = 0.98$).
- **Attack Graph & IOCs:** Extracts IP `185.220.101.5`, domain `paypai-security.com`, and malicious URL with recommended action `BLOCK`.

### 3. Key Takeaway to Emphasize to Judges:
> *"Notice the multi-vector corroboration: domain lookalike detection, raw IP inspection, and SPF failure align to push this to 90/100 Critical Risk. Clicking 'Why?' itemizes every single point for the analyst."*

---

## Scenario C — Business Email Compromise (Zero-Link BEC)

### 1. Scenario Overview
- **File:** `demo_samples/03_bec_executive_wire_fraud.eml`
- **Sender:** `Satya Nadella <ceo-exec-office@company-corp.work>`
- **Subject:** `CONFIDENTIAL: Urgent Wire Transfer Request - Project Apex Acquisition`
- **Expected Risk Level:** **High Risk**
- **Expected Risk Score:** **57 / 100**
- **CRITICAL DIFFERENTIATOR:**
  - **NO malicious URL**
  - **NO attachment**
  - Standard signature scanners score this 0/100. Sentryl detects the threat purely through social-engineering and identity mismatch heuristics.

### 2. Forensic Breakdown & Signals
- **Executive Impersonation (+15 pts):** Display name claims to be CEO (*"Satya Nadella"*), while the sender address originates from an unaligned external domain (`company-corp.work`).
- **Financial Wire Solicitation (+15 pts):** Direct request to execute an urgent financial wire transfer for an acquisition.
- **Secrecy Pressure (+10 pts):** Explicit instructions to isolate the victim (*"strictly confidential"*, *"do not discuss with anyone in the office"*).
- **Suspicious TLD (+12 pts):** High-abuse top-level domain (`.work`).
- **Relay Infrastructure (+5 pts):** Originating from external unverified mail server.

### 3. Key Takeaway to Emphasize to Judges:
> *"This is a major differentiator: this email contains zero links and zero attachments. Traditional antivirus scanners score this completely clean. Sentryl scores it 57/100 High Risk because our NLP and BEC heuristics isolate executive role impersonation, financial solicitation, and coercive secrecy pressure."*

---

## Scenario D — Trojan Attachment with Double Extension (`.pdf.exe`)

### 1. Scenario Overview
- **File:** `demo_samples/04_trojan_double_extension_attachment.eml`
- **Sender:** `FedEx Express Dispatch <delivery-update@fedx-tracking-portal.work>`
- **Subject:** `FedEx Shipment Notification: Undelivered Package #92841029`
- **Attachment:** `Invoice_Scan_FedEx.pdf.exe`
- **Expected Risk Level:** **High Risk**
- **Expected Risk Score:** **65 / 100 (Enforced by Attachment Critical Floor Override)**
- **SAFETY RULE:** **NEVER execute the attachment.** All analysis is 100% safe static inspection.

### 2. Forensic Breakdown & Signals
- **Double Extension Detection:** Flags `.pdf.exe` masquerade exploiting default Windows hidden file extensions.
- **Static PE Inspection:** Detects Portable Executable magic bytes (`MZ\x90\x00`) inside a delivery invoice lure.
- **Static Shannon Entropy:** High entropy calculated in memory (indicating packed binary code).
- **Attachment Critical Floor Override:** Sentryl enforces an automatic minimum risk floor of **65 / 100 (High Risk)** for any executable payload, preventing clean SPF headers from diluting dangerous attachments.
- **Cryptographic Evidence Sealing:** Computes SHA-256 acquisition digest upon ingest, generates a 5-stage Chain of Custody, and signs the record with server-side HMAC-SHA256.
- **Tamper Verification:** The dashboard's **"Verify Evidence Integrity"** button confirms bit-for-bit mathematical custody.

### 3. Key Takeaway to Emphasize to Judges:
> *"We never execute attachments. Sentryl performs safe static analysis: parsing PE headers, calculating Shannon entropy, and enforcing an automatic High Risk floor (≥65). The evidence vault computes an immutable SHA-256 digest and HMAC seal at the exact millisecond of ingestion."*
