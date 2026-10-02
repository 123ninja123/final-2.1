# Sentryl — SIH Grand Finale Final Startup Guide

**Platform:** Sentryl — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform  
**SIH Problem Statement:** SIH26106  
**Status:** CODE FREEZE & VERIFIED  

---

## 1. Quick Start Commands (Tested & Verified)

### 1.1 Run One-Click Preflight Verification
Before starting any servers, verify that your environment, dependencies, ML model, demo samples, and extension packages are 100% operational:

```powershell
cd "d:\#final - 2nd face"
python demo_preflight.py
```
*Expected Output:* `PREFLIGHT STATUS: ALL CHECKS PASSED -> SYSTEM READY FOR DEMO`

---

### 1.2 Start FastAPI Backend Server
Launch the backend server using Python's `uvicorn` module on `127.0.0.1:8000`:

```powershell
cd "d:\#final - 2nd face"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Verify API Health:**
Open your browser or run in a new terminal:
```powershell
curl http://127.0.0.1:8000/health
```
*Expected Response:*
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "checks": {
    "api": "operational",
    "detector": "operational",
    "domain_intel": "operational",
    "nlp_engine": "operational",
    "ip_intel": "operational"
  }
}
```

Interactive OpenAPI documentation is available live at:
`http://127.0.0.1:8000/docs`

---

### 1.3 Launch SOC Forensic Dashboard & Frontend
You can open the SOC Forensic Investigation Dashboard directly in Microsoft Edge or Google Chrome:

**Method A: Direct Local File Open (Fastest for Live Demo)**
Paste into browser address bar:
```text
file:///d:/#final%20-%202nd%20face/extension/dashboard/report.html
```

**Method B: Optional Local Web Server**
```powershell
cd "d:\#final - 2nd face"
python -m http.server 3000
```
Then navigate to: `http://localhost:3000/extension/dashboard/report.html`

**Method C: Standalone Extension Popup Preview**
Paste into browser address bar:
```text
file:///d:/#final%20-%202nd%20face/popup%20ui.html
```

---

## 2. Browser Extension Installation (Manifest V3)

### 2.1 Microsoft Edge Installation (Recommended)
1. Open Microsoft Edge and navigate to: `edge://extensions`
2. Enable the **Developer mode** toggle in the bottom left sidebar.
3. Click **Load unpacked** in the top toolbar.
4. Select the directory: `d:\#final - 2nd face\extension`
5. The extension will appear with the shield icon: **"Sentryl — Email Threat Detection"** (v1.0.1).

*Live Store Listing:* Sentryl is officially certified and available on the Microsoft Edge Add-ons store:  
[https://microsoftedge.microsoft.com/addons/detail/ORDCKC10MVMZ](https://microsoftedge.microsoft.com/addons/detail/ORDCKC10MVMZ)

### 2.2 Google Chrome Installation
1. Open Google Chrome and navigate to: `chrome://extensions`
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** in the top left toolbar.
4. Select the directory: `d:\#final - 2nd face\extension`

---

## 3. Demo Samples Location & Catalog

The controlled demonstration `.eml` files are located in `d:\#final - 2nd face\demo_samples/`:

| Sample Filename | Target Vector | Expected Score | Demonstration Purpose |
|---|---|---|---|
| `01_clean_corporate_newsletter.eml` | Legitimate Enterprise Email | **20 / 100 (Low Risk)** | Proves system avoids false positives on authentic DKIM/SPF newsletters. |
| `02_credential_phishing_paypal.eml` | Lookalike Domain + Raw IP Link | **90 / 100 (Critical Risk)** | Demonstrates Levenshtein homoglyph spoofing (`paypai-security.com`) + raw IP link (`185.220.101.5`). |
| `03_bec_executive_wire_fraud.eml` | Zero-Link BEC Wire Fraud | **57 / 100 (High Risk)** | Major differentiator: Detects CEO wire fraud with **zero links and zero attachments**. |
| `04_trojan_double_extension_attachment.eml` | Malware Dropper (`.pdf.exe`) | **65 / 100 (High Risk)** | Demonstrates double-extension detection, static entropy analysis, critical floor override, and HMAC evidence sealing. |

---

## 4. Configuration & Environment Variables

All configuration is managed with secure, self-contained defaults in `backend/config.py`:

| Environment Variable | Default Value | Purpose |
|---|---|---|
| `EVIDENCE_HMAC_SECRET` | `sentryl-secret-key-change-in-production-2026` | Server-side secret key used to compute cryptographic HMAC-SHA256 tamper seals. |
| `ADMIN_API_KEY` | `sentryl-admin-supersecret-key-2026` | API key required for protected endpoints (`/api/admin/stats`, `/api/admin/clear-cache`). |
| `MAX_REPORTS_CACHE` | `500` | Maximum number of analysis reports retained in the in-memory FIFO/LRU store. |
| `REPORT_CACHE_TTL_SECONDS` | `86400` (24 Hours) | Time-to-live before old reports are automatically purged from memory. |
| `MAX_EML_SIZE_BYTES` | `10485760` (10 MB) | Strict streaming upload size ceiling to prevent Denial of Service. |
| `GEMINI_API_KEY` | *(None / Optional)* | If provided, enables Google Gemini natural language generation. |

### Fallback Behavior when External APIs are Absent:
- **No Gemini API Key:** The system automatically falls back to an internal **deterministic evidence-grounded template synthesizer**. The 0–100 numerical risk score, risk level, IOCs, and Attack Graph are 100% unaffected.
- **External GeoIP / RDAP Offline:** Labeled transparently as `"Telemetry Unavailable (Offline / Timeout)"`. Sentryl strictly refuses to fabricate fake data.

---

## 5. Troubleshooting & Diagnostics

### Issue 1: Port 8000 Already in Use
If another process is using port 8000:
```powershell
# Find and terminate the process holding port 8000:
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
# Then restart uvicorn:
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Issue 2: Extension Cannot Connect to Backend
- Verify `config.js` has `API_BASE_URL: "http://localhost:8000"` or `"http://127.0.0.1:8000"`.
- Ensure the FastAPI backend is running and `http://127.0.0.1:8000/health` returns `200 OK`.
- Both `http://localhost:8000/*` and `http://127.0.0.1:8000/*` are pre-authorized in `manifest.json` under `host_permissions`.

### Issue 3: In-Memory Cache Reset
If you restart the uvicorn process, in-memory cached reports are cleared. Simply re-drag and drop any `.eml` sample into the dashboard to generate a fresh report and scan ID.
