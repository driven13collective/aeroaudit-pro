# AeroAudit Pro

## 🧪 Beta Tester Instructions (AeroAudit Pro v1.0)
Welcome to the internal pilot! Please follow these guidelines while testing:

### 🚀 How to Access
- **Live Link:** [Paste your Railway URL here]
- **Environment:** Optimized for Chrome/Edge (Desktop).

### 📋 Testing Priorities
1. **Model Accuracy:** Does the YOLO model identify all infrastructure correctly in your test video?
2. **Performance:** Does the audit finish within 60 seconds of upload?
3. **UI/UX:** Is the "Run AeroVision Audit" button clear and responsive?

### 🚩 How to Report Issues
- **Bugs:** Use the GitHub "Issues" tab. Please include the video timestamp where the error occurred.
- **Improvements:** Direct message me for specific "Aramco-standard" feature requests.

> **Note:** We are currently running on a high-performance Railway tier. If you experience a 500-error, wait 30 seconds and refresh—the server may be scaling up.

## Why this fixes the Crashes
- The model loads in a background thread, so the web server can start quickly and avoid Railway startup timeouts.
- The config binds to 0.0.0.0 and uses the Railway-provided `PORT`, so the container is reachable in production.
- The Nixpacks setup installs system libraries required by OpenCV (libGL, libglib, and X11), preventing missing library errors.
- The `/health` endpoint gives Railway a simple readiness check so it can confirm the app is alive.

## Roadmap
| Feature | Status | Target Date |
| --- | --- | --- |
| Video Upload | ✅ Live | Feb 2026 |
| YOLO Detection | ✅ Live | Feb 2026 |
| PDF Audit Export | 🚧 Developing | March 2026 |
| GPU Acceleration | 📅 Planned | April 2026 |

## Code Hygiene
Use VS Code Copilot to generate a testing checklist:

```
@workspace generate a testing checklist based on the features listed in the README.
```
