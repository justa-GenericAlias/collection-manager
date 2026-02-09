# Collection Manager

Newest edits:
- `server/app.py` — Flask API (CRUD, paging, stats) persisted to `server/data.json`
- `server/data.json` — starts with 30 records
- `server/requirements.txt` — Python deps
- Frontend updated to call the backend API (`js/app.js`) and includes paging controls in `index.html`

Local run (development):

1. Ensure Python 3.8+ is installed.

2. Create a virtual environment and install deps:
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r server/requirements.txt
```

3. Start the Flask server:
```bash
python server/app.py
```

4. Open the applications with the link:
```bash
https://jaga-collection-manager.netlify.app/
```

Local development notes:
- `server/data.json` is the source of truth for records locally. Keep backups before editing.