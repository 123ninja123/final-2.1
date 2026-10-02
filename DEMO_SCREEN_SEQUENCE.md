# Sentryl — SIH Grand Finale Visual Demo Screen Sequence

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Document Purpose:** Exact presenter visual checklist detailing what to click, what to show, what to say, and what NOT to click on each screen during the live evaluation.

---

## 🖥️ Screen-by-Screen Execution Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ IDEAL VISUAL DEMO FLOW                                                                  │
│ 1. Inbox / Upload  ──> 2. Sentryl Extension ──> 3. Risk Score   ──> 4. Why Panel        │
│ 5. Authentication  ──> 6. Domain Intel      ──> 7. URL Analysis ──> 8. BEC Indicators   │
│ 9. IOC Panel       ──> 10. Timeline         ──> 11. Attack Graph──> 12. Evidence Vault  │
│ 13. Markdown Report Export                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Screen 1: Controlled Inbox / Dropzone
- **SCREEN:** Web browser showing `file:///d:/#final%20-%202nd%20face/extension/dashboard/report.html` (or Gmail inbox with extension).
- **WHAT TO SHOW:** Clean dark-mode SOC Investigation Dashboard with drag-and-drop `.eml` upload zone.
- **WHAT TO SAY:** *"Here is the Sentryl SOC Dashboard. We can triage emails live from the browser extension or ingest raw RFC 822 .eml files directly."*
- **WHAT NOT TO CLICK:** Do not click browser refresh or navigate away from the dashboard tab.

---

### Screen 2: Sentryl Extension Popup
- **SCREEN:** Extension popup (or `popup ui.html`).
- **WHAT TO SHOW:** The top shield status, active verdict, and the dual-mode toggle switch (`User Tips` vs `SOC Analyst`).
- **WHAT TO SAY:** *"The extension provides dual-mode UX: everyday employees get clear, non-technical guidance, while analysts can toggle directly into forensic triage."*
- **WHAT NOT TO CLICK:** Do not click on external documentation links that open new windows.

---

### Screen 3: Overall Risk Score
- **SCREEN:** Large circular score indicator at the top of the dashboard.
- **WHAT TO SHOW:** The 0–100 numerical score, severity badge (`Low`, `Medium`, `High`, `Critical`), and summary card.
- **WHAT TO SAY:** *"Every email receives an auditable, bounded score from 0 to 100. This is not a black-box percentage; it is a componentized index across 6 security vectors."*
- **WHAT NOT TO CLICK:** Do not manually edit the score field or resize browser during animation.

---

### Screen 4: "Why this score?" Panel
- **SCREEN:** Expandable `Score Breakdown` drawer.
- **WHAT TO SHOW:** The itemized signal table showing Signal Name (e.g., `DOMAIN_LOOKALIKE_DETECTED`), Points Added (+20), and Provenance (`OBSERVED`, `INFERRED`).
- **WHAT TO SAY:** *"Clicking 'Why?' reveals complete mathematical explainability. Every single point awarded is backed by an observable header or content signal."*
- **WHAT NOT TO CLICK:** Do not click rapid expand/collapse toggles repeatedly.

---

### Screen 5: Email Authentication Panel
- **SCREEN:** Authentication section in dashboard.
- **WHAT TO SHOW:** SPF, DKIM, DMARC, and Return-Path status badges with RFC status explanations.
- **WHAT TO SAY:** *"We evaluate full domain alignment. Here we see SPF hardfail and Return-Path divergence clearly flagged."*
- **WHAT NOT TO CLICK:** Do not click DNS query refresh buttons if offline.

---

### Screen 6: Domain Intelligence Panel
- **SCREEN:** Domain analysis card.
- **WHAT TO SHOW:** Displayed sender domain vs target brand, Levenshtein edit distance, and Punycode normalization.
- **WHAT TO SAY:** *"Our domain intelligence caught that the attacker registered `paypai-security.com`—an edit distance of 1 from `paypal.com`, substituting lowercase 'l' with 'i'."*
- **WHAT NOT TO CLICK:** Do not click the raw domain hyperlink (never visit attacker sites).

---

### Screen 7: URL & Redirection Analysis
- **SCREEN:** Hyperlinks table in dashboard.
- **WHAT TO SHOW:** Highlighted row showing raw IP hostname (`http://185.220.101.5/login`), Shannon entropy score, and credential harvesting path.
- **WHAT TO SAY:** *"Sentryl performs 100% safe static URL analysis: evaluating IP schemes, open redirects, and Shannon entropy without sending outbound network packets."*
- **WHAT NOT TO CLICK:** **CRITICAL:** NEVER click on the phishing destination link.

---

### Screen 8: BEC & Social Engineering Indicators
- **SCREEN:** Content Analysis card for Scenario C (`03_bec_executive_wire_fraud.eml`).
- **WHAT TO SHOW:** Executive impersonation badge, wire transfer cues, and coercive secrecy tags.
- **WHAT TO SAY:** *"Here in Scenario C, with zero links and zero attachments, Sentryl still triggers 57/100 High Risk because our BEC engine isolates CEO impersonation and urgent wire demands."*
- **WHAT NOT TO CLICK:** Do not jump back to Scenario A while discussing BEC.

---

### Screen 9: Structured IOC Panel
- **SCREEN:** Indicators of Compromise (IOC) table.
- **WHAT TO SHOW:** Categorized table of IPv4, domain, URL, and hash artifacts alongside recommended SOC actions (`BLOCK`, `INVESTIGATE`).
- **WHAT TO SAY:** *"Every relevant artifact is normalized into an IOC table with one-click CSV and JSON export for SIEM firewall blocklists."*
- **WHAT NOT TO CLICK:** Do not click 'Clear All' if present.

---

### Screen 10: Forensic Relay Timeline
- **SCREEN:** Transit Hops / Relay Timeline section.
- **WHAT TO SHOW:** Chronological hop-by-hop cards from bottom origin MTA to destination gateway, with inter-hop latency ($\Delta t$).
- **WHAT TO SAY:** *"We parse RFC 5321 multiline Received headers chronologically, isolating internal RFC 1918 hops and calculating transit delays."*
- **WHAT NOT TO CLICK:** Do not click external map zoom controls rapidly.

---

### Screen 11: Interactive Attack Graph
- **SCREEN:** SVG Attack Graph topology canvas.
- **WHAT TO SHOW:** Visual nodes connecting Email $\to$ Sender Mailbox $\to$ Domain $\to$ Origin IP $\to$ URLs $\to$ Attachments.
- **WHAT TO SAY:** *"The Attack Graph visually connects the dots for tier-1 analysts, showing exactly how attacker infrastructure and lures intersect."*
- **WHAT NOT TO CLICK:** Do not drag nodes violently off the canvas view boundary.

---

### Screen 12: Evidence Vault & HMAC Tamper Verification
- **SCREEN:** Cryptographic Evidence Record at the bottom of the dossier.
- **WHAT TO SHOW:** SHA-256 acquisition digest, 5-stage Chain of Custody, server-side HMAC seal, and the **"Verify Evidence Integrity"** button. Click the button and show the green **"VERIFIED"** badge.
- **WHAT TO SAY:** *"At ingestion, we compute a SHA-256 digest and seal it with server-side HMAC-SHA256. Clicking verify proves bit-for-bit mathematical custody. If a single byte is altered, it alerts TAMPERED."*
- **WHAT NOT TO CLICK:** Do not click the verification button more than twice.

---

### Screen 13: Investigation Report Export
- **SCREEN:** Top action bar / Export dropdown.
- **WHAT TO SHOW:** Click **"Export Markdown Report"** (or view the exported `.md` file).
- **WHAT TO SAY:** *"Finally, with one click, the analyst exports a full Markdown forensic report with strict provenance tags separating observed facts from inferred signals."*
- **WHAT NOT TO CLICK:** Do not open massive external text editors that hide the browser.
