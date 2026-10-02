# Sentryl — SIH Grand Finale 4-Minute Live Demo Script

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Target Jury:** SIH Grand Finale Technical Evaluation Committee  
**Total Presentation Time:** 4 Minutes Exact  
**Status:** FROZEN & REHEARSED  

---

## ⏱️ Timeline & Action Script

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TIMELINE OVERVIEW                                                                      │
│ 00:00 - 00:20 (20s) : Problem Statement & The Investigative Gap                        │
│ 00:20 - 00:45 (25s) : System Architecture & Pipeline Overview                          │
│ 00:45 - 01:30 (45s) : Scenario A — Clean Corporate Baseline (Low Risk)                │
│ 01:30 - 02:20 (50s) : Scenario B — Lookalike Credential Phishing (90/100 Critical)     │
│ 02:20 - 03:00 (40s) : Scenario C — Zero-Link Business Email Compromise (57/100 High)  │
│ 03:00 - 03:35 (35s) : Scenario D & Forensics — Timeline, Attack Graph & HMAC Integrity│
│ 03:35 - 04:00 (25s) : Final Positioning & Value Wrap-Up                                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Problem Statement (00:00 – 00:20)
**Presenter Action:** Show Sentryl title slide or the clean home view of the SOC Forensic Dashboard.  
**Spoken Script:**
> *"Email providers already detect many threats. The problem we address is investigation: why is this email suspicious, what evidence supports it, and what indicators should an analyst investigate?
>
> Traditional gateways act as black boxes—they show a generic warning banner or silently discard messages. Sentryl turns incoming emails into structured, explainable, and tamper-evident forensic intelligence."*

---

### Phase 2: Introduce Sentryl Architecture (00:20 – 00:45)
**Presenter Action:** Show the linear pipeline graphic or explain the architectural layers.  
```text
EMAIL ──> AUTHENTICATION ──> IDENTITY ──> URL/CONTENT ──> ML + RULES ──> RISK ENGINE ──> FORENSICS ──> IOC + GRAPH + EVIDENCE
```
**Spoken Script:**
> *"Sentryl operates a deterministic-first multi-vector pipeline.
> When an email arrives, we parse the RFC 822 MIME stream, evaluate SPF/DKIM authentication, inspect domain and URL identity statically, extract content and BEC signals, apply a lightweight auxiliary ML model, and feed everything into an explainable 0–100 bounded risk engine.
> The result is a complete forensic dossier: extracted IOCs, an interactive attack graph, and a cryptographic evidence record."*

---

### Phase 3: Clean Email Baseline (00:45 – 01:30)
**Presenter Action:** Drag and drop `demo_samples/01_clean_corporate_newsletter.eml` into the dashboard dropzone.  
**Screen Display:**
- Score: **20 / 100 — LOW RISK**
- Authentication: SPF Pass, DKIM Pass, DMARC Aligned.
- Toggle between `User View` and `Analyst View`.  
**Spoken Script:**
> *"First, we analyze a legitimate corporate email from GitHub.
> Sentryl processes the payload in under 30 milliseconds and assigns a score of 20 out of 100—firmly in the Low Risk tier.
> We also test legitimate emails to reduce unnecessary alerts.
> Both SPF and DKIM pass, the domain aligns with our verified brand whitelist, and the user receives a simple, clear verdict: this email is authentic and safe to interact with."*

---

### Phase 4: Lookalike Phishing with Deep Explainability (01:30 – 02:20)
**Presenter Action:** Drag and drop `demo_samples/02_credential_phishing_paypal.eml`.  
**Screen Display:**
- Score: **90 / 100 — CRITICAL RISK**
- Click **"Why this score?"** to expand the itemized breakdown.  
**Spoken Script:**
> *"Next, we ingest an active credential harvesting campaign impersonating PayPal.
> The risk score immediately jumps to 90 out of 100: CRITICAL.
> Now, let's click 'Why?'.
> Rather than a black-box percentage, Sentryl explains the exact mathematical composition:
> - Domain similarity: Our Levenshtein engine caught that `paypai-security.com` substituted lowercase 'l' with an 'i'.
> - SPF failure: The sending relay is not authorized in DNS.
> - Suspicious URL: The destination link points directly to a raw external IP address with a login harvesting path.
> - Urgency: The body uses coercive account suspension lures.
> Every point is backed by observable evidence."*

---

### Phase 5: Zero-Link BEC Wire Fraud (02:20 – 03:00)
**Presenter Action:** Drag and drop `demo_samples/03_bec_executive_wire_fraud.eml`.  
**Screen Display:**
- Score: **57 / 100 — HIGH RISK**
- Threat Indicators: VIP Impersonation, Financial Wire Request, Secrecy Pressure.  
**Spoken Script:**
> *"Now for one of our biggest differentiators: Business Email Compromise.
> Look closely at this email—it has no malicious URL and no attachment. Traditional signature and antivirus filters score this 0 out of 100.
> But Sentryl scores it 57 out of 100: HIGH RISK.
> No malicious URL was required. The threat is in the identity and social-engineering signals:
> 1. Executive impersonation: The display name claims to be the CEO, but originates from an unaligned `.work` domain.
> 2. Financial wire transfer solicitation.
> 3. Coercive secrecy pressure instructing the recipient not to discuss the request with anyone in the office."*

---

### Phase 6: Forensics, Attack Graph & Evidence Integrity (03:00 – 03:35)
**Presenter Action:** Scroll down on the dashboard. Click on the **Forensic Timeline**, **IOC Panel**, and **Attack Graph**. Then click **"Verify Evidence Integrity"**.  
**Screen Display:**
- Interactive SVG Attack Graph mapping relationships.
- IOC Table with recommended actions (`BLOCK`, `INVESTIGATE`).
- Evidence Vault showing SHA-256 acquisition digest, HMAC seal, and 5-stage Chain of Custody.
- Tamper Verification badge: **"VERIFIED"** (Green).  
**Spoken Script:**
> *"For the SOC analyst, Sentryl automatically constructs the complete investigative picture:
> - The Forensic Timeline reconstructs hop-by-hop relay transit.
> - The IOC Panel categorizes IPs, domains, and hashes with one-click export.
> - The Attack Graph visually correlates the sender, domain, hosting IP, and indicators.
> Most importantly, look at the Evidence Vault. At the exact millisecond of ingestion, we compute a SHA-256 acquisition digest and seal it with server-side HMAC-SHA256.
> When we click 'Verify Evidence Integrity'—it returns VERIFIED. If an attacker or insider alters even a single character, the system immediately flags it as TAMPERED."*

---

### Phase 7: Final Positioning (03:35 – 04:00)
**Presenter Action:** Show the export button (`Export Markdown Report`) and return to presenter camera / main slide.  
**Spoken Script:**
> *"With one click, the analyst exports a full Markdown forensic investigation report ready for SIEM ingestion.
>
> To conclude: Sentryl does not replace Gmail's threat filtering.
> It adds an explainable investigation and forensic intelligence layer for users and security analysts.
>
> Thank you, and we look forward to your questions."*
