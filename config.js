/**
 * Sentryl — Centralized Production & Deployment Configuration
 * Configures the live Microsoft Edge Add-ons Store URL and Backend API base endpoint.
 */

window.APP_CONFIG = {
  // Backend API URL (Local development & demonstration endpoint)
  API_BASE_URL: (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || !window.location.hostname))
    ? "http://localhost:8000"
    : "http://localhost:8000",

  // Approved live listing on the Microsoft Edge Add-ons Store
  EDGE_EXTENSION_STORE_URL: "https://microsoftedge.microsoft.com/addons/detail/ORDCKC10MVMZ",

  // Official Public HTTPS Privacy Policy URL (Microsoft Edge Add-ons Compliant)
  PRIVACY_POLICY_URL: "https://sentryl-eta.vercel.app/privacy",

  // Application metadata
  VERSION: "1.0.1",
  APP_NAME: "Sentryl",
  SUPPORTED_BROWSER: "Microsoft Edge (Chromium MV3)"
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = window.APP_CONFIG;
}
