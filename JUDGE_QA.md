# Sentryl — SIH Grand Finale Judge Defense & Technical Q&A (25 Questions)

**Problem Statement SIH26106:** "AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform"  
**Platform Version:** 1.0.2 (Frozen Master Build)  
**Document Purpose:** Comprehensive technical defense dossier for the SIH Grand Finale Jury.

---

### Q1: Why not rely solely on Gmail's native warning banners?
**Defensible Answer:**
Gmail’s native defense is an inbound Secure Email Gateway (SEG) optimized for binary classification (Deliver, Spam, or show a generic banner: *"Be careful with this message"*). While effective at volumetric spam, it leaves critical operational gaps for enterprise incident response:
1. **Zero Explainability:** Analysts receive no mathematical score breakdown or itemized signals explaining why the email was flagged.
2. **No Forensic Artifact Extraction:** Gmail does not parse the RFC 5321 `Received:` relay chain into an interactive hop-by-hop topology, nor does it export IOCs (hashes, C2 domains, route IPs) for SIEM ingestion.
3. **No Cryptographic Evidence Preservation:** If an employee forwards the email or an attacker deletes compromised infrastructure, acquisition state is lost. Sentryl immediately computes a SHA-256 acquisition digest and seals it in a tamper-evident ledger.
4. **Targeted Spear-Phishing Blindspots:** BEC emails containing zero links and zero attachments from free webmail accounts pass Gmail's perimeter filters. Sentryl detects executive impersonation, wire fraud cues, and coercive secrecy.
- **Evidence in Code:** `backend/services/graph_builder.py`, `backend/services/ioc_extractor.py`, `backend/services/evidence_vault.py`.
- **Limitation:** Sentryl does not replace perimeter MTAs; it augments triage at the endpoint.
- **What NOT to Claim:** Do not claim Sentryl catches more zero-days than Google's multi-billion-dollar infrastructure.

---

### Q2: Why implement this as a Browser Extension?
**Defensible Answer:**
1. **Last-Mile Endpoint Visibility:** Modern adversaries leverage legitimate infrastructure (e.g., SharePoint, Notion, Google Forms) with valid DKIM signatures that pass gateway appliances. The extension intercepts threats directly at the point of human interaction.
2. **Contextual DOM Extraction:** The extension inspects displayed names versus underlying `mailto:` anchors, uncovers CSS text hiding (`font-size:0px`), and inspects hyperlinks before navigation.
3. **Zero MX Reconfiguration:** Traditional gateways require altering DNS MX records and routing enterprise email through third parties. A browser extension deploys instantaneously with zero IT downtime.
4. **Dual-Mode Triage:** Normal users receive simple safe actions (`user_view`), while SOC analysts can pivot to the forensic dashboard in one click (`analyst_view`).
- **Evidence in Code:** `extension/content/gmail.js`, `extension/popup/popup.js`, `backend/models/schemas.py`.
- **Limitation:** Webmail DOM changes can impact scraping unless resilient selectors or raw `.eml` uploads are used.
- **What NOT to Claim:** Do not claim an extension alone can filter organization-wide inbound mail at the perimeter.

---

### Q3: Why is Machine Learning necessary alongside deterministic rules?
**Defensible Answer:**
Deterministic rules excel at boolean verification (e.g., "does SPF equal fail?"). However, attackers continuously mutate lures to evade static rules:
1. **Polymorphic Evasion:** Attackers inject zero-width unicode spaces (`\u200b`), mix Cyrillic homoglyphs (`pаypal`), and paraphrase urgency phrasing to bypass static regex blocklists.
2. **Cross-Feature Correlation:** Machine learning captures non-linear relationships across weak individual signals (e.g., moderate URL entropy + an unfamiliar relay node + a non-matching reply-to domain).
3. **Calibrated Confidence:** ML outputs a continuous probability distribution ($P \in [0.0, 1.0]$) that serves as an auxiliary scoring signal (0–20 points).
- **Evidence in Code:** `backend/ml/feature_extractor.py`, `backend/services/ml_inference.py`.
- **Limitation:** Linear models depend on feature engineering quality.
- **What NOT to Claim:** Do not claim deep neural networks, BERT transformers, or autonomous self-learning.

---

### Q4: Why not use ONLY Machine Learning or LLMs?
**Defensible Answer:**
Relying solely on ML or LLMs in mission-critical cybersecurity is architecturally irresponsible:
1. **Hallucination & Non-Determinism:** LLMs can generate conflicting verdicts on identical inputs or hallucinate non-existent threats.
2. **Adversarial Susceptibility:** Pure deep learning models are vulnerable to prompt injection and token manipulation (e.g., appending benign text to dilute spam scores).
3. **Lack of Forensic Auditability:** A SOC analyst cannot defend "the neural network output 0.94" in a formal incident audit. Sentryl uses a **deterministic-first security model**: SPF/DKIM verification, domain spoofing metrics, URL lexical analysis, and RFC 5321 hops are strictly deterministic. ML serves as an auxiliary signal, and the LLM acts purely as an advisory text summarizer.
- **Evidence in Code:** `backend/services/risk_scorer.py:320-370`, `backend/services/llm_explainer.py:80-115`.
- **Limitation:** Natural language summaries depend on external LLM availability unless the deterministic fallback is triggered.
- **What NOT to Claim:** Do not claim the LLM calculated the numerical score.

---

### Q5: What is your exact Machine Learning model architecture and inference latency?
**Defensible Answer:**
We implemented a **Dual-Branch Hybrid Pipeline**:
- **Branch 1 (Lexical N-grams):** Sublinear TF-IDF vectorizer (unigrams + bigrams, max 300 features) extracting n-gram representations from email subject and body.
- **Branch 2 (Structured Features):** A 16-dimensional dense numerical feature vector extracting urgency cues, financial tokens, raw IP counts, Levenshtein domain distance, authentication status, dangerous attachment flags, reply-to divergence, and evasion tokens.
- **Classifier:** L2-regularized Logistic Regression (`scikit-learn`) combining both branches with sigmoid class probabilities.
- **Inference Latency:** **1.81 milliseconds** per email on a standard single-thread CPU.
- **Evidence in Code:** `backend/ml/feature_extractor.py`, `backend/ml/train_model.py`, `backend/ml/evaluation_report.json`.
- **Limitation:** Lightweight linear classifier, not a multi-billion-parameter foundation model.
- **What NOT to Claim:** Do not claim multi-modal transformer networks or GPU cluster requirements.

---

### Q6: What dataset was used to train and validate the model? How did you ensure zero data leakage?
**Defensible Answer:**
The model was evaluated on a hand-curated benchmark dataset of **20 genuine, distinct email instances** (10 benign enterprise communications, 10 real-world malicious lures) in `backend/ml/dataset.py`.
- **Elimination of Data Leakage:** In previous development phases, synthetic pre-split data duplication caused identical samples to exist across train and validation sets. In our final master build, all pre-split duplication was completely eliminated.
- **Strict Fold Isolation:** In `backend/ml/evaluate_model.py`, 5-fold stratified cross-validation is performed where TF-IDF vectorizers and feature scalers are fitted **strictly inside training folds**. Zero validation fold data is ever exposed during feature fitting.
- **Evidence in Code:** `backend/ml/dataset.py:7-180`, `backend/ml/evaluate_model.py:45-95`.
- **Limitation:** 20 samples prove pipeline functionality and feature fusion, but cannot represent the diversity of a 500,000-email enterprise corpus.
- **What NOT to Claim:** Do not claim the model was trained on millions of enterprise production emails.

---

### Q7: What are your genuine Precision, Recall, F1, and cross-validation metrics?
**Defensible Answer:**
Based on leak-free 5-fold stratified cross-validation documented in `backend/ml/evaluation_report.json`:
- **Accuracy:** 1.00 (on curated benchmark set)
- **Precision:** 1.00
- **Recall:** 1.00
- **F1-Score:** 1.00
- **ROC-AUC:** 1.00
- **Honest Generalization Caveat:** While the model achieves 1.00 on this curated benchmark because structural features (SPF failure, raw IP links, double extensions) cleanly separate threat classes, real-world high-throughput email traffic is expected to exhibit an estimated **3% to 5% false positive/negative margin**. This is why Sentryl constrains ML to only 20 points of our 100-point risk score.
- **Evidence in Code:** `backend/ml/evaluation_report.json`.
- **What NOT to Claim:** Never claim 'universal 100% accuracy in production environments'.

---

### Q8: How is the 0–100 Risk Score calculated, and what are the categorical caps?
**Defensible Answer:**
The score is calculated via a strictly componentized, bounded formula where each security pillar has a fixed mathematical ceiling:
$$\text{Risk Score} = \min\Big(100, \, S_{\text{Auth}} + S_{\text{Domain}} + S_{\text{URL}} + S_{\text{Content}} + S_{\text{Infra}} + S_{\text{Evasion}} + S_{\text{ML}}\Big)$$
1. **Email Authentication ($0 - 20$ pts):** SPF Hardfail (+8), DKIM missing/invalid (+8), DMARC policy violation (+6), Return-Path divergence (+8). Capped at 20.
2. **Domain Reputation & Spoofing ($0 - 20$ pts):** Levenshtein target brand squatting (+20), Punycode/IDN masquerade (+15), high-abuse suspicious TLD (+12). Capped at 20.
3. **URL & Redirection Threat ($0 - 20$ pts):** Raw IP hostname (+20), open redirect parameter (+12), credential keywords in path (+10), high Shannon entropy token (+10). Capped at 20.
4. **Content, BEC & Social Engineering ($0 - 20$ pts):** Executive impersonation (+15), financial wire solicitation (+15), coercive urgency (+10), secrecy cues (+10). Capped at 20.
5. **Origin Infrastructure ($0 - 10$ pts):** Confirmed Tor anonymity exit node (+10), commercial bulletproof proxy (+5). Capped at 10.
6. **Adversarial Evasion ($0 - 10$ pts):** Zero-width unicode spaces (+5), mixed-script homoglyphs (+5), CSS micro-font hidden text (+5). Capped at 10.
7. **Attachment Critical Floor Override:** Any email harboring executable payloads (`.exe`, `.scr`, `.bat`, `.pdf.exe`) is automatically clamped to a minimum floor of **65 / 100 (High Risk)** regardless of authentication passes.
- **Evidence in Code:** `backend/services/risk_scorer.py:15-385`.

---

### Q9: How do you prevent False Positives (e.g., legitimate marketing or forwarded mail)?
**Defensible Answer:**
1. **Authentication Pass Neutralization:** Verified SPF, DKIM, and DMARC passes from authentic brand domains yield 0 authentication penalty points.
2. **Subdomain vs Lookalike Disambiguation:** We parse domains using effective top-level domain logic, distinguishing valid subdomains (`mail.accounts.google.com`) from lookalike attack domains (`accounts-google.com.attacker.xyz`).
3. **No Single Point of Failure:** Urgency keywords alone only award 5–10 points in Content, leaving the email firmly in the "Low Risk" band (< 30). Reaching "Critical" (75+) requires corroboration across multiple independent vectors (e.g., domain spoofing + raw IP link + SPF fail).
- **Evidence in Code:** `backend/services/risk_scorer.py:65-120`, `backend/services/domain_intel.py:45-75`.

---

### Q10: How do you handle False Negatives (e.g., brand-new zero-day phishing campaigns)?
**Defensible Answer:**
Zero-day attacks typically use newly registered domains with no historical blocklist reputation. Sentryl catches these through **structural and lexical heuristics**:
- **Lexical Anomalies:** Flags raw IP links, open redirect parameters (`redirect_url=`), and high Shannon entropy tokens regardless of domain age.
- **Display Name vs Header Misalignment:** Flags when the sender display name says "Microsoft Support" or "CEO" while the sender domain is an arbitrary registered name.
- **Evasion Detection:** Detects zero-width spaces and hidden CSS injected to bypass keyword scanners.
- **Attachment Floor:** Intercepts double-extension droppers (`.pdf.exe`) with an automatic High Risk floor.
- **Evidence in Code:** `backend/services/url_checker.py:45-120`, `backend/services/evasion_detector.py:20-65`.

---

### Q11: How do you detect Domain Spoofing, Punycode, and Brand Lookalikes?
**Defensible Answer:**
Our domain intelligence engine (`backend/services/domain_intel.py`) implements a four-stage inspection:
1. **Target Brand Whitelist:** Compares the domain against verified high-value enterprise domains (`google.com`, `paypal.com`, `microsoft.com`, `fedex.com`).
2. **Levenshtein Distance:** Flags domains within edit distance 1–2 of major enterprise targets (e.g., `paypai-security.com` $\to$ `paypal.com`).
3. **Keyword Concatenation:** Detects patterns where brand names are paired with security lure tokens (`paypal-security-update.com`).
4. **Punycode (IDN) Normalization:** Decodes `xn--` ASCII-compatible encoding and maps Cyrillic lookalikes (`а`, `е`, `о`, `р`, `с`) to Latin equivalents prior to similarity scoring.
- **Evidence in Code:** `backend/services/domain_intel.py:25-95`.

---

### Q12: How do SPF, DKIM, and DMARC work, and how does Sentryl evaluate them?
**Defensible Answer:**
- **SPF (RFC 7208):** Verifies if the sending mail server IP is authorized by the domain owner in DNS. Evaluated as `Pass`, `Fail`, `Softfail`, or `Neutral`.
- **DKIM (RFC 6376):** Cryptographically signs email headers and body with a private key. The receiver validates using the sender's public key published in DNS (`_domainkey`).
- **DMARC (RFC 7489):** Solves the visible `From:` spoofing loophole by requiring **Domain Alignment**—enforcing that the visible `From:` header matches the domain validated by SPF or DKIM.
- **Sentryl's Enhancement:** Translates raw header strings into clear analyst explanations: *"SPF Softfail: Sending IP is not in authorized SPF record. Visible From domain does not align with authenticated identity."*
- **Evidence in Code:** `backend/services/spf_dkim_dmarc.py:15-110`.

---

### Q13: Can an IP address identify the exact sender physical location?
**Defensible Answer:**
**NO.** Claiming that an IP address gives an exact physical sender location is technically false.
- **Technical Reality:** IP geolocation identifies only the physical data center or ISP node of the **Mail Transfer Agent (MTA)** or router that forwarded the email. Consumer ISPs allocate dynamic IP blocks that resolve only to a regional POP (Point of Presence) or city-level gateway.
- **Sentryl's Defense:** Sentryl explicitly labels all geolocation output as **"Observed IP vs Inferred Geolocation"** with the disclosure: *"City/ISP level routing node, not human physical coordinate"*. We detect VPNs, commercial hosting proxies, and Tor exit relays without making false physical tracking claims.
- **Evidence in Code:** `backend/services/ip_intel.py:30-80`, `extension/dashboard/report.html`.

---

### Q14: How does Forensic Relay Tracing work across RFC 5321 multiline headers?
**Defensible Answer:**
Email transit follows RFC 5321. Each relay MTA prepends a `Received:` header line at the top of the header stack. Sentryl’s parser (`backend/services/header_parser.py`):
1. Handles RFC 822 folded multiline continuation (lines beginning with whitespace).
2. Traverses headers chronologically from bottom (initial client submission) to top (corporate recipient gateway).
3. Extracts IP addresses, filters out RFC 1918 private subnets (`10.0.0.0/8`, `192.168.0.0/16`) for external GeoIP queries, and computes inter-hop transit delays ($\Delta t$).
- **Evidence in Code:** `backend/services/header_parser.py:20-115`.

---

### Q15: How are Indicators of Compromise (IOCs) extracted and mapped to SOC actions?
**Defensible Answer:**
`backend/services/ioc_extractor.py` performs deterministic extraction across 6 artifact types:
1. **Network IOCs:** Public IPv4 and IPv6 addresses extracted from `Received:` headers and body URLs.
2. **Domain IOCs:** Sender domain, Reply-To domain, and destination hostnames parsed from hyperlinks.
3. **URL IOCs:** Full HTTP/HTTPS URI strings with suspicious query parameters isolated.
4. **Identity IOCs:** Sender mailbox, Reply-To address, and recipient targets.
5. **Cryptographic Hashes:** SHA-256 and MD5 hashes computed for all attached files.
6. **Message Metadata:** RFC 5322 `Message-ID` for mail server search.
Each IOC is assigned a SOC action (`BLOCK`, `INVESTIGATE`, `MONITOR`, `ALLOW`) and can be exported as structured JSON or CSV.
- **Evidence in Code:** `backend/services/ioc_extractor.py:15-95`.

---

### Q16: How is Technical Evidence preserved, sealed, and audited?
**Defensible Answer:**
Sentryl implements an automated **Evidence Vault** (`backend/services/evidence_vault.py`):
1. **Acquisition Digest:** At the millisecond of ingestion, raw RFC 822 bytes are hashed with SHA-256.
2. **Server-Side Keyed HMAC Seal:** The evidence metadata is normalized into canonical JSON and signed using HMAC-SHA256 keyed by `EVIDENCE_HMAC_SECRET`.
3. **5-Stage Chain of Custody:** Generates an immutable timestamped audit trail (Acquisition $\to$ Digest Computation $\to$ Parsing $\to$ Multi-Vector Evaluation $\to$ Dossier Sealing).
- **Evidence in Code:** `backend/services/evidence_vault.py:25-90`.

---

### Q17: How do you detect and prove Evidence Tampering using HMAC-SHA256?
**Defensible Answer:**
1. When an evidence record is generated, Sentryl computes a composite HMAC-SHA256 tamper seal over the canonical JSON representation of the acquisition hash and timestamp.
2. **Verification Endpoint (`POST /api/verify-integrity`):** An analyst or auditor submits the stored raw content and claimed hash. Sentryl recalculates the SHA-256 digest and HMAC seal. If even a single byte of headers or body text was modified post-acquisition, the endpoint returns `status: "TAMPERED"` and highlights the cryptographic mismatch.
- **Evidence in Code:** `backend/services/evidence_vault.py:95-130`, `backend/routers/scan.py:310-345`.

---

### Q18: How do you protect user privacy and PII (Opt-in Privacy Mode)?
**Defensible Answer:**
1. **Opt-in Privacy Mode (`privacyMode: true`):** Sanitizes Personally Identifiable Information before logging or LLM summarization:
   - Email user handles $\to$ `[REDACTED_USER]@domain.com`
   - Employee names $\to$ `[REDACTED_NAME]`
   - Private IP addresses $\to$ `[INTERNAL_IP]`
2. **In-Memory Attachment Processing:** Attachment payloads are hashed and inspected for PE headers in memory; file buffers are immediately released and never persisted to cloud storage.
3. **Intranet Isolation:** Private RFC 1918 hops are never transmitted to external GeoIP APIs.
- **Evidence in Code:** `backend/services/privacy_filter.py`, `backend/services/ip_intel.py:25-40`.

---

### Q19: Can your system safely inspect malicious URLs without triggering payload execution or SSRF?
**Defensible Answer:**
**YES, 100%.** Sentryl uses **Safe Static URL Analysis**, not dynamic browser execution:
- We parse URL syntax, validate schemes, compute Shannon entropy, and inspect query parameters without sending a single network packet or resolving DNS.
- This provides complete immunity to Server-Side Request Forgery (SSRF), browser sandbox escape zero-days, and attacker telemetry beaconing.
- **Evidence in Code:** `backend/services/url_checker.py:40-150`.
- **Limitation:** Static analysis cannot detect payloads hidden behind dynamic CAPTCHAs or multi-stage JavaScript redirects.
- **What NOT to Claim:** Do not claim dynamic sandbox detonation.

---

### Q20: Can an attacker manipulate your risk score or jailbreak the LLM via prompt injection?
**Defensible Answer:**
1. **Score Formula Immunity:** Weights and thresholds are enforced strictly on the server; an attacker has no control over scoring math.
2. **LLM Decision Plane Isolation:** The LLM is invoked strictly *after* the risk score, risk level, and IOCs are deterministically computed.
3. **Prompt Injection Defense:** Untrusted email fields are enclosed inside `<UNTRUSTED_EMAIL_DATA>` delimiters. Even if an attacker injects text telling the LLM to output "This email is safe", the system's displayed score, risk tier, and UI badges remain Critical.
- **Evidence in Code:** `backend/services/llm_explainer.py:75-105`, `backend/routers/scan.py:140-165`.

---

### Q21: What happens when external Threat Intelligence or LLM APIs fail or time out?
**Defensible Answer:**
Sentryl adheres to **Graceful Degradation with Zero Fabrication**:
1. **1.5-Second Strict Timeouts:** External HTTP queries (GeoIP, RDAP) utilize strict 1.5s connection and read timeouts.
2. **Deterministic LLM Fallback:** If the Gemini API is offline or unconfigured, Sentryl immediately switches to an internal evidence-grounded template synthesizer.
3. **Honest Labeling:** Missing external telemetry is labeled `"Telemetry Unavailable"`. The system never fabricates synthetic data.
- **Evidence in Code:** `backend/services/ip_intel.py:15-40`, `backend/services/llm_explainer.py:100-120`.

---

### Q22: What happens if Gmail updates its web DOM structure?
**Defensible Answer:**
Browser DOM scraping is inherently vulnerable to webmail UI updates:
1. Sentryl’s extension utilizes multi-selector fallbacks (`[data-message-id]`, `h2[data-thread-perm-id]`, standard ARIA roles) and displays a warning banner if DOM elements are not found.
2. **Protocol-Level Fallback:** Sentryl provides the standalone **Raw `.eml` Ingestion Engine** (`/api/analyze-eml`). Analysts and users can drag-and-drop `.eml` files exported directly from any client, completely bypassing webmail HTML layouts.
- **Evidence in Code:** `extension/content/gmail.js:30-85`, `backend/routers/scan.py:195-280`.

---

### Q23: How do you protect the backend from Denial-of-Service (MIME bombs, giant uploads, memory exhaustion)?
**Defensible Answer:**
1. **10MB Streaming Upload Limit:** In `/api/analyze-eml`, uploads are inspected in 64KB chunks up to `MAX_EML_SIZE_BYTES = 10MB`. Exceeding this immediately triggers HTTP 413.
2. **MIME Parser Bounds:** Deeply nested MIME structures are capped at `MAX_MIME_PARTS = 100`, and attachments are capped at `MAX_ATTACHMENTS = 20`.
3. **Cache Eviction:** The in-memory analysis cache is capped at `MAX_REPORTS_CACHE = 500` with FIFO/LRU eviction and a 24-hour TTL.
- **Evidence in Code:** `backend/routers/scan.py:200-240`, `backend/services/eml_parser.py:15-35`, `backend/services/report_store.py:10-50`.

---

### Q24: What are Sentryl's biggest technical limitations today?
**Defensible Answer:**
Our three most significant engineering boundaries today are:
1. **Auxiliary ML Dataset Size:** The ML classifier is trained on a 20-sample curated benchmark designed to validate the dual-branch pipeline rather than generalize across all global dialects.
2. **Static URL Analysis:** URL inspection is purely static lexical analysis rather than dynamic headless browser detonation.
3. **Technical Integrity vs Statutory Admissibility:** Evidence records provide tamper-evident HMAC seals for internal incident response, but do not constitute RFC 3161 certified digital signatures from an external licensed TSA.
- **Evidence in Code:** `backend/ml/dataset.py`, `backend/services/url_checker.py`, `backend/services/evidence_vault.py`.
- **Strength:** Transparent self-awareness of engineering boundaries builds credibility with senior technical judges.

---

### Q25: What is genuinely implemented today versus what is planned on the enterprise roadmap?
**Defensible Answer:**
- **100% Genuinely Implemented Today:** RFC 822 MIME stream parsing with 10MB streaming limit, multiline RFC 5321 relay hop reconstruction, SPF/DKIM/DMARC authentication analysis, Levenshtein domain spoofing, Shannon entropy URL analysis, BEC keyword heuristics, zero-width space and homoglyph evasion detection, single-email attack graph generation, HMAC-SHA256 evidence integrity sealing, dual-view payload generation, Markdown report export, and 49 automated pytest tests.
- **Planned Post-SIH Enterprise Roadmap:** Persistent PostgreSQL/Timescale storage, Redis distributed cache, containerized Chromium sandbox detonation, Microsoft Graph API automated mailbox quarantine connectors, and RFC 3161 PKI timestamping.
- **Evidence in Code:** Complete verified repository codebase across `backend/`, `extension/`, and `demo_samples/`.
