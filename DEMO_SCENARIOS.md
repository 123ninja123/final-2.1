# Sentryl — SIH Grand Finale Demo Scenarios (Controlled Forensic Dossier)

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Document Purpose:** Detailed technical specification and expected runtime behavior for the 4 controlled demonstration emails in `demo_samples/`.

---

## Scenario 1: Clean Corporate Engineering Newsletter

### 1.1 Overview
- **File:** `demo_samples/01_clean_corporate_newsletter.eml`
- **Threat Vector:** None (Benign Operational Communication)
- **Sender:** `GitHub Notifications <notifications@github.com>`
- **Subject:** `[GitHub] New security advisory published for dependency in sentryl-repo`
- **Expected Score:** **20 / 100 (Low Risk / Clean)**

### 1.2 Observed Forensic Artifacts
- **RFC 5321 Relay:** Single hop from `smtp.github.com [140.82.112.4]` to corporate mail gateway `mx.company.com`.
- **SPF Evaluation:** `Pass` (`sender IP 140.82.112.4 is authorized for github.com`).
- **DKIM Signature:** `Pass` (`v=1; a=rsa-sha256; d=github.com; s=s20210515`).
- **DMARC Policy:** `Pass` (Strict domain alignment between `From: github.com` and `d=github.com`).
- **URLs:** `https://github.com/jayasish-dev/sentryl/security/advisories` (Verified legitimate domain, valid TLS scheme, zero open redirects, normal Shannon entropy).
- **Attachments:** None.

### 1.3 Score Composition
| Vector | Points Awarded | Cap | Contributing Reason |
|---|---|---|---|
| Authentication ($S_{\text{Auth}}$) | 0 | 20 | All cryptographic authentications passed. |
| Domain Reputation ($S_{\text{Domain}}$) | 0 | 20 | Sender domain matches whitelist brand `github.com`. |
| Hyperlink Safety ($S_{\text{URL}}$) | 0 | 20 | Domain on safe whitelist; zero suspicious parameters. |
| Content & BEC ($S_{\text{Content}}$) | 0 | 20 | Standard technical advisory syntax; no wire fraud or coercive urgency. |
| Infrastructure ($S_{\text{Infra}}$) | 0 | 10 | Legitimate GitHub AS36459 enterprise hosting block. |
| Evasion Tactics ($S_{\text{Evasion}}$) | 0 | 10 | Zero hidden characters, zero Cyrillic substitutions. |
| **Auxiliary Baseline / ML** | **20** | - | Normal baseline confidence weight. |
| **Total Final Score** | **20 / 100** | **100** | **Tier: LOW RISK** |

### 1.4 Dual-Mode Presentation
- **User View:** "This email was verified as authentic. The sender identity is cryptographically confirmed by GitHub, and all links point to safe enterprise resources. No action required."
- **Analyst View:** Full cryptographic alignment verification, 1 clean transit hop, 0 flagged IOCs.

---

## Scenario 2: High-Severity Credential Phishing (PayPal Lookalike)

### 2.1 Overview
- **File:** `demo_samples/02_credential_phishing_paypal.eml`
- **Threat Vector:** Credential Harvester with Lookalike Brand Impersonation & Raw IP Link
- **Sender:** `PayPal Security Desk <support@paypai-security.com>`
- **Subject:** `URGENT: Your account has been restricted - Verify Identity Immediately`
- **Expected Score:** **90 / 100 (Critical Risk)**

### 2.2 Observed Forensic Artifacts
- **RFC 5321 Relay:** Hop from `unauthorized-relay.suspicious.net [185.220.101.5]` to destination.
- **SPF Evaluation:** `Fail` (IP `185.220.101.5` is not permitted in SPF record for `paypai-security.com`).
- **DKIM Signature:** `Fail` (Invalid or absent DKIM signature).
- **DMARC Policy:** `Fail` (Domain alignment failure).
- **Domain Spoofing:** `paypai-security.com` detected as lookalike of `paypal.com` (Levenshtein distance: 1, homoglyph replacement of 'l' with 'i').
- **Hyperlink Threat:** `http://185.220.101.5/login?redirect=update-account` (Flagged: Raw IP address hostname + HTTP insecure scheme + credential keyword `/login`).
- **Content Urgency:** Artificial urgency patterns: *"restricted"*, *"immediately"*, *"within 24 hours"*.

### 2.3 Score Composition
| Vector | Points Awarded | Cap | Contributing Reason |
|---|---|---|---|
| Authentication ($S_{\text{Auth}}$) | 20 | 20 | SPF Hardfail (+8), DKIM missing (+8), Return-Path divergence (+8) [Capped at 20]. |
| Domain Reputation ($S_{\text{Domain}}$) | 20 | 20 | Levenshtein brand squatting on `paypal.com` (+20). |
| Hyperlink Safety ($S_{\text{URL}}$) | 20 | 20 | Raw external IP address hostname (+20), `/login` credential keyword (+10) [Capped at 20]. |
| Content & BEC ($S_{\text{Content}}$) | 10 | 20 | Coercive account suspension urgency (+10). |
| Infrastructure ($S_{\text{Infra}}$) | 0 | 10 | Observed external relay node. |
| Evasion Tactics ($S_{\text{Evasion}}$) | 0 | 10 | Lexical homoglyph in domain rather than body text. |
| **ML Auxiliary Signal** | **20** | 20 | Logistic regression probability: 0.98. |
| **Total Final Score** | **90 / 100** | **100** | **Tier: CRITICAL RISK** |

### 2.4 Extracted IOCs & SOC Actions
| IOC Type | Extracted Value | Risk Rating | Recommended Action |
|---|---|---|---|
| Domain | `paypai-security.com` | Malicious | `BLOCK` (DNS Firewall / Sinkhole) |
| IPv4 | `185.220.101.5` | Malicious | `BLOCK` (Perimeter Firewall / WAF) |
| URL | `http://185.220.101.5/login?redirect=update-account` | Malicious | `BLOCK` (Secure Web Gateway / EDR) |
| Identity | `support@paypai-security.com` | Malicious | `BLOCK` (Email Gateway Filter) |

---

## Scenario 3: Zero-Link Business Email Compromise (BEC Wire Fraud)

### 3.1 Overview
- **File:** `demo_samples/03_bec_executive_wire_fraud.eml`
- **Threat Vector:** Executive Impersonation & Direct Wire Transfer Diversion
- **Sender:** `Satya Nadella <ceo-exec-office@company-corp.work>`
- **Subject:** `CONFIDENTIAL: Urgent Wire Transfer Request - Project Apex Acquisition`
- **Expected Score:** **57 / 100 (High Risk)**

### 3.2 Observed Forensic Artifacts
- **Payload Characteristics:** **Zero links and zero attachments**. Traditional antivirus and signature-based gateways score this 0/100.
- **Sender Alignment:** Display name states *"Satya Nadella"*, but sender address domain is `company-corp.work` (Mismatch with legitimate corporate domain).
- **High-Abuse TLD:** `.work` top-level domain.
- **Content Urgency & Secrecy:** *"strictly confidential"*, *"wire transfer"*, *"acquire target before competitor disclosure"*, *"do not discuss with anyone in the office"*.
- **Return-Path:** `untracked-mailbox@company-corp.work`.

### 3.3 Score Composition
| Vector | Points Awarded | Cap | Contributing Reason |
|---|---|---|---|
| Authentication ($S_{\text{Auth}}$) | 0 | 20 | Self-hosted domain passing basic SPF (~all). |
| Domain Reputation ($S_{\text{Domain}}$) | 12 | 20 | Suspicious high-abuse `.work` TLD (+12). |
| Hyperlink Safety ($S_{\text{URL}}$) | 0 | 20 | Zero URLs present. |
| Content & BEC ($S_{\text{Content}}$) | 20 | 20 | Executive Impersonation (+15), Wire Fraud Solicitation (+15), Secrecy Cues (+10) [Capped at 20]. |
| Infrastructure ($S_{\text{Infra}}$) | 5 | 10 | Suspicious relay infrastructure (+5). |
| Evasion Tactics ($S_{\text{Evasion}}$) | 0 | 10 | Plaintext deception. |
| **ML Auxiliary Signal** | **20** | 20 | High BEC lexical feature weighting. |
| **Total Final Score** | **57 / 100** | **100** | **Tier: HIGH RISK** |

### 3.4 Key Takeaway for Judges
This proves Sentryl does not merely look for bad links. It understands social engineering context and protects corporate finance teams against multimillion-dollar CEO fraud attacks.

---

## Scenario 4: Trojan Payload with Double Extension (`.pdf.exe`)

### 4.1 Overview
- **File:** `demo_samples/04_trojan_double_extension_attachment.eml`
- **Threat Vector:** Malware Dropper with Masqueraded Double Extension
- **Sender:** `FedEx Express Dispatch <delivery-update@fedx-tracking-portal.work>`
- **Subject:** `FedEx Shipment Notification: Undelivered Package #92841029`
- **Attachment:** `Invoice_Scan_FedEx.pdf.exe` (Size: 48,128 bytes, Executable PE Header)
- **Expected Score:** **65 / 100 (High Risk)** — *Enforced by Attachment Critical Floor Override*

### 4.2 Observed Forensic Artifacts
- **Attachment Name:** `Invoice_Scan_FedEx.pdf.exe` (Exploits Windows default behavior of hiding known file extensions to trick users into believing it is an Adobe PDF document).
- **Static File Inspection:**
  - PE header signature detected (`MZ\x90\x00`).
  - High Shannon entropy (compressed/packed executable binary).
  - SHA-256 Digest: Pre-computed in memory.
  - Zero execution / Safe static analysis.
- **Domain Heuristics:** `fedx-tracking-portal.work` (Levenshtein distance 1 from `fedex.com` + high-abuse `.work` TLD).

### 4.3 Score Composition & Critical Risk Floor
- **Raw Vector Sum:** Domain risk (+12 for `.work`) + Content urgency (+10) + ML auxiliary (+20) + Auth warning = ~42 points.
- **Attachment Critical Floor Override:** Because an executable payload with a double extension (`.pdf.exe`) was detected, Sentryl's risk engine enforces an automatic **Risk Floor Override of 65/100 (High Risk)**.
- **Judge Defense Value:** Demonstrates defense-in-depth: even if a malware author sets up pristine SPF and DKIM on a custom domain, Sentryl will never classify an executable dropper as low or medium risk.

### 4.4 Cryptographic Evidence Integrity Audit
- **Raw Acquisition Digest:** Computed via SHA-256 upon stream intake.
- **HMAC Signature:** Keyed by server-side `EVIDENCE_HMAC_SECRET`.
- **Chain of Custody:** 5 immutable chronological timestamps.
- **Tamper Verification:** When tested via `POST /api/verify-integrity`:
  - Authentic Content: Returns `status: "VERIFIED"`, `match: true`.
  - Mutated Payload (even 1 altered byte): Returns `status: "TAMPERED"`, `match: false`.
