# Collection Manager

This workspace contains a static frontend and a small Flask backend that persists data to JSON files. It's a starting foundation for Solo Project 2 (client/server Collection Manager).

What I added:
- `server/app.py` — Flask API (CRUD, paging, stats) persisted to `server/data.json`
- `server/data.json` — starts with 30 records
- `server/requirements.txt` — Python deps
- Frontend updated to call the backend API (`js/app.js`) and includes paging controls in `index.html`

Local run (development):

1. Ensure Python 3.8+ is installed.
2. Create a virtualenv and install deps:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r server/requirements.txt
```

3. Start the Flask server:

```bash
python server/app.py
```

4. Serve the frontend by opening `index.html` in a browser, or run a local static server. The frontend expects the API at `http://localhost:5000` by default.

Notes about deployment and the submission checklist:
- The frontend can be deployed to Netlify (static site). Use the Netlify URL for the frontend.
- The Flask backend must be deployed to a separate host that allows file persistence (for example Render, Railway, or a small VPS). Netlify Functions are serverless and do not provide durable file storage, so the backend should not be deployed to Netlify functions if JSON persistence is required.
- When deployed, update `API_BASE` in `js/app.js` (or set `window.API_BASE`) to point to the deployed API URL.

Checklist for submission (what you still need to do to finalize deployment):
- Deploy frontend to Netlify (Netlify URL must be public and work in incognito)
- Deploy Flask backend to a host that allows file persistence and CORS from the Netlify domain
- Confirm the app starts with at least 30 records and CRUD operations persist across sessions/devices
- Ensure paging is exactly 10 records per page (server uses `per_page=10`)

If you want, I can:
- Help deploy the frontend to Netlify and the Flask backend to a free host (Render/Railway) and wire the URLs together.
- Add a small GitHub Actions workflow to deploy the frontend automatically.

Local development notes:
- `server/data.json` is the source of truth for records locally. Keep backups before editing.
