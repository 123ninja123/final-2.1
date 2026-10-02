"""
demo_preflight.py - Sentryl Grand Finale Demo Preflight Checker
Verifies environment, dependencies, files, and core endpoints WITHOUT modifying any logic.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def run_checks():
    print("=" * 60)
    print("SENTRYL DEMO PREFLIGHT CHECK")
    print("=" * 60)

    all_passed = True

    # 1. Python Environment Check
    py_ver = sys.version_info
    if py_ver >= (3, 10):
        print(f"[PASS] Python Environment ({py_ver.major}.{py_ver.minor}.{py_ver.micro})")
    else:
        print(f"[FAIL] Python Environment: Python >= 3.10 required, got {sys.version}")
        all_passed = False

    # 2. Required Dependencies Check
    required_pkgs = ["fastapi", "uvicorn", "pydantic", "sklearn", "joblib", "httpx"]
    pkg_failures = []
    for pkg in required_pkgs:
        try:
            __import__(pkg)
        except ImportError as e:
            pkg_failures.append(f"{pkg}: {e}")
    if not pkg_failures:
        print("[PASS] Python Dependencies (fastapi, uvicorn, pydantic, sklearn, joblib, httpx)")
    else:
        print(f"[FAIL] Dependencies Missing: {', '.join(pkg_failures)}")
        print("       Fix: pip install -r backend/requirements.txt")
        all_passed = False

    # 3. Model Artifact Check
    model_path = ROOT_DIR / "backend" / "models" / "ml_model.joblib"
    eval_report = ROOT_DIR / "backend" / "ml" / "evaluation_report.json"
    if model_path.exists() and eval_report.exists():
        print(f"[PASS] ML Model Artifact ({model_path.name}) & Evaluation Report")
    else:
        print("[FAIL] ML Model Artifact: ml_model.joblib or evaluation_report.json missing")
        print("       Fix: python backend/ml/train_model.py")
        all_passed = False

    # 4. Demo Samples Check
    demo_dir = ROOT_DIR / "demo_samples"
    expected_samples = [
        "01_clean_corporate_newsletter.eml",
        "02_credential_phishing_paypal.eml",
        "03_bec_executive_wire_fraud.eml",
        "04_trojan_double_extension_attachment.eml",
    ]
    missing_samples = [s for s in expected_samples if not (demo_dir / s).exists()]
    if not missing_samples:
        print(f"[PASS] Demo Samples (4/4 controlled .eml files present in {demo_dir.name}/)")
    else:
        print(f"[FAIL] Demo Samples: Missing {missing_samples}")
        all_passed = False

    # 5. Extension Files Check
    ext_dir = ROOT_DIR / "extension"
    expected_ext_files = [
        ext_dir / "manifest.json",
        ext_dir / "background" / "service-worker.js",
        ext_dir / "content" / "gmail.js",
        ext_dir / "popup" / "popup.html",
        ext_dir / "dashboard" / "report.html",
    ]
    missing_ext = [str(f.relative_to(ROOT_DIR)) for f in expected_ext_files if not f.exists()]
    dist_zips = list((ROOT_DIR / "dist").glob("sentryl-edge-extension-*.zip"))
    if not missing_ext:
        zip_str = f" [Package ZIP exists: {dist_zips[0].name}]" if dist_zips else " [ZIP missing]"
        print(f"[PASS] Extension Files (Manifest V3, content script, popup, dashboard){zip_str}")
    else:
        print(f"[FAIL] Extension Files: Missing {missing_ext}")
        all_passed = False

    # 6. Backend Imports & FastAPI App
    try:
        from backend.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        print("[PASS] Backend FastAPI Application & Router Initialization")
    except Exception as e:
        print(f"[FAIL] Backend Initialization: {e}")
        print("       Fix: Inspect stack trace in backend/main.py")
        all_passed = False
        return all_passed

    # 7. Health Endpoint Check
    try:
        resp = client.get("/health")
        if resp.status_code == 200:
            print("[PASS] API Health Endpoint (/health -> HTTP 200)")
        else:
            print(f"[FAIL] Health Endpoint: Expected HTTP 200, got {resp.status_code}")
            all_passed = False
    except Exception as e:
        print(f"[FAIL] Health Endpoint Query: {e}")
        all_passed = False

    # 8. Analysis Endpoint Test (with sample 01)
    sample_01 = demo_dir / "01_clean_corporate_newsletter.eml"
    scan_id = None
    if sample_01.exists():
        try:
            with open(sample_01, "rb") as f:
                resp = client.post("/api/analyze-eml", files={"file": ("clean.eml", f, "message/rfc822")})
            if resp.status_code == 200:
                data = resp.json()
                scan_id = data.get("scan_id")
                score = data.get("risk_score")
                print(f"[PASS] Analysis Endpoint (/api/analyze-eml -> HTTP 200, Score: {score}/100)")
            else:
                print(f"[FAIL] Analysis Endpoint: Expected HTTP 200, got {resp.status_code}")
                all_passed = False
        except Exception as e:
            print(f"[FAIL] Analysis Endpoint Execution: {e}")
            all_passed = False
    else:
        print("[SKIP] Analysis Endpoint Test: Sample 01 not found")

    # 9. Report Generation & Markdown Export Check
    if scan_id:
        try:
            # JSON Report
            resp_json = client.get(f"/api/report/{scan_id}")
            # Markdown Report
            resp_md = client.get(f"/api/report/{scan_id}/markdown")
            if resp_json.status_code == 200 and resp_md.status_code == 200 and len(resp_md.text) > 100:
                print(f"[PASS] Report Generation (JSON & Markdown Export for ID {scan_id[:8]}...)")
            else:
                print(f"[FAIL] Report Generation: JSON={resp_json.status_code}, MD={resp_md.status_code}")
                all_passed = False
        except Exception as e:
            print(f"[FAIL] Report Generation Execution: {e}")
            all_passed = False

    # 10. Evidence Vault Integrity Verification Check
    try:
        from backend.services.evidence_vault import generate_evidence_record, verify_evidence_integrity
        test_content_str = "Received: by mail.test.com; Wed, 16 Sep 2026 12:00:00 +0000\nFrom: test@test.com\n\nHello"
        ev = generate_evidence_record(raw_content=test_content_str, source_label="Preflight Self-Test")
        raw_hash = ev.raw_sha256 if hasattr(ev, "raw_sha256") else ev["raw_sha256"]
        
        # Valid verification
        valid_res = verify_evidence_integrity(claimed_sha256=raw_hash, raw_content=test_content_str)
        # Tampered verification
        tampered_res = verify_evidence_integrity(claimed_sha256=raw_hash, raw_content=test_content_str + " tampered")
        
        valid_match = valid_res.hash_matches if hasattr(valid_res, "hash_matches") else valid_res["hash_matches"]
        tampered_match = tampered_res.hash_matches if hasattr(tampered_res, "hash_matches") else tampered_res["hash_matches"]
        tampered_status = tampered_res.status if hasattr(tampered_res, "status") else tampered_res["status"]
        
        if valid_match and not tampered_match and tampered_status == "TAMPERED":
            print("[PASS] Evidence Vault (HMAC-SHA256 Sealing & Tamper Verification Verified)")
        else:
            print("[FAIL] Evidence Vault: Tamper detection logic returned unexpected verification state")
            all_passed = False
    except Exception as e:
        print(f"[FAIL] Evidence Vault: {e}")
        all_passed = False

    print("=" * 60)
    if all_passed:
        print("PREFLIGHT STATUS: ALL CHECKS PASSED -> SYSTEM READY FOR DEMO")
    else:
        print("PREFLIGHT STATUS: ONE OR MORE CHECKS FAILED -> REVIEW FIXES ABOVE")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
