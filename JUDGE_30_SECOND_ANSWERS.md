# Sentryl — SIH Grand Finale Judge 30-Second Answer Cheat Sheet

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**Document Purpose:** Concise, high-impact 15–30 second spoken answers for the 12 mandatory judge questions. Zero buzzwords, complete technical honesty, and absolute defensibility.

---

### Q1: "Gmail already detects phishing. Why Sentryl?"
> *"Gmail is an inbound protective gateway designed for binary filtering: deliver, spam, or show a generic banner. It is a black box that does not explain why an email was flagged.  
> Sentryl is an **investigative triage workbench**: we provide mathematical explainability, reconstruct RFC 5321 transit timelines, extract actionable IOCs for SIEM ingestion, and preserve tamper-evident cryptographic evidence for incident response."*  
*(Timing: 22 seconds)*

---

### Q2: "Where is the AI?"
> *"Sentryl implements a **dual-branch machine learning classifier** combining TF-IDF lexical n-grams with 16 handcrafted security features using regularized Logistic Regression.  
> However, ML serves strictly as an **auxiliary signal** (0 to 20 points). Our core protocol authentication, domain Levenshtein analysis, and forensic timeline reconstruction remain **deterministic** to guarantee zero hallucination and complete auditability."*  
*(Timing: 24 seconds)*

---

### Q3: "Your dataset is only 20 samples?"
> *"Yes. The current dataset is a **controlled architectural benchmark** designed to validate that our dual-branch feature pipeline and cross-validation operate end-to-end without data leakage.  
> We deliberately disclose this boundary: this is an engineering proof-of-concept, not a claim of enterprise generalization. A production-grade model requires training on a representative corpus of 500,000+ emails."*  
*(Timing: 25 seconds)*

---

### Q4: "You got 100% accuracy?"
> *"On our curated 20-sample benchmark using leak-free 5-fold cross-validation, the measured score was 1.00 because structural features like raw IP links, SPF failures, and double extensions cleanly separate threat classes.  
> We **do NOT** interpret that as 100% real-world accuracy. In noisy corporate email streams, an estimated 3% to 5% error margin is expected, which is why ML is capped at only 20 points of our risk score."*  
*(Timing: 26 seconds)*

---

### Q5: "Can you detect zero-day phishing?"
> *"No security detector can guarantee 100% zero-day prevention.  
> However, our layered defense does not rely on static blocklists. We evaluate protocol authentication, Levenshtein brand distance, URL lexical Shannon entropy, open redirect parameters, and BEC social-engineering cues. Even if a domain is brand new, its structural anomalies trigger investigative signals."*  
*(Timing: 24 seconds)*

---

### Q6: "Can you find the attacker's exact location?"
> *"No, and we explicitly emphasize this. IP intelligence provides approximate **network, ISP, and Autonomous System (ASN)** facility data for the Mail Transfer Agent (MTA).  
> It does not establish a human perpetrator's physical street address or GPS coordinate. All geolocation output is strictly labeled 'Observed IP vs Inferred Geolocation'."*  
*(Timing: 21 seconds)*

---

### Q7: "Do you execute malicious URLs?"
> *"No. The current implementation performs **100% safe static URL analysis**.  
> We inspect host syntax, IP schemes, open redirects, and Shannon entropy without sending a single network packet or resolving external DNS. This provides total immunity to Server-Side Request Forgery (SSRF), browser exploits, and attacker tracking beacons."*  
*(Timing: 23 seconds)*

---

### Q8: "Can the LLM change the verdict?"
> *"No. The LLM is strictly an **advisory natural language explanation layer** situated at the end of the pipeline.  
> The 0–100 numerical risk score, risk level, IOCs, and Attack Graph are computed deterministically before the LLM is invoked. Even if an attacker injects prompt-jailbreak text, the system's displayed score and UI badges remain Critical."*  
*(Timing: 24 seconds)*

---

### Q9: "Is this legally admissible evidence?"
> *"No such claim. Sentryl provides **tamper-evident HMAC-SHA256 integrity verification** and a 5-stage Chain of Custody for internal security operations and incident post-mortems.  
> Formal statutory legal admissibility depends on jurisdiction-specific rules of evidence, physical chain-of-custody protocols, and certified RFC 3161 Hardware Security Modules."*  
*(Timing: 23 seconds)*

---

### Q10: "Can it quarantine emails?"
> *"Not in the current prototype. Sentryl operates today as an **advisory triage and investigation platform**, generating exportable IOCs and recommended containment actions.  
> Automated mailbox remediation requires provider-level administrative integrations such as Microsoft Graph API or Google Workspace Admin SDK, which are on our enterprise roadmap."*  
*(Timing: 22 seconds)*

---

### Q11: "Who would use this?"
> *"Our primary users are **Tier-1 SOC analysts, IT helpdesks, and SMEs** who receive forwarded suspicious email reports and spend 20 minutes manually inspecting raw headers.  
> Sentryl compresses that 20-minute manual header triage into an instant, structured forensic dossier with one-click IOC exports."*  
*(Timing: 21 seconds)*

---

### Q12: "What's your biggest limitation?"
> *"Our three most honest limitations today are:  
> 1. The auxiliary ML model is trained on a small 20-sample benchmark.  
> 2. The browser extension relies on webmail DOM integration, which can require updates when Gmail alters its markup.  
> 3. URL inspection is static analysis rather than dynamic hypervisor sandbox detonation.  
> Each limitation has a defined architectural path on our enterprise roadmap."*  
*(Timing: 27 seconds)*
