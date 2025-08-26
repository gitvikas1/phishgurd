# PhishGuard — Phishing URL Detector

PhishGuard is a simple, educational web app that estimates whether a URL looks **phishing** using
hand-crafted URL features and a lightweight **Logistic Regression** model trained on synthetic data.
It also stores detected phishing URLs in a **History** page to help visitors learn common patterns.

> ⚠️ Educational use only. Not a security guarantee. When in doubt, avoid entering credentials.

## Features

- Paste a URL to check; get a verdict and confidence score.
- Stores **only phishing** detections in SQLite and shows them on a History page.
- "Learn" button links to a phishing information resource (defaults to PhishTank).
- Auto-trains a compact model on first run if none exists.

## Tech

- Python, Flask
- scikit-learn (Logistic Regression)
- SQLite (via `sqlite3`)

## Project Structure

```
phishguard/
├─ app.py
├─ model.py
├─ feature_extractor.py
├─ database.py
├─ phishguard_model.pkl        # created on first run
├─ phishguard.db               # created on first detection
├─ templates/
│  ├─ index.html
│  └─ history.html
└─ static/
   └─ style.css
```

## Quickstart

1. **Clone & enter**

```bash
git clone <your-repo-url>.git
cd phishguard
```

2. **Setup environment & install deps**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

3. **Run**

```bash
python app.py
# Open http://localhost:5000
```

The first run will generate `phishguard_model.pkl`. When you submit URLs, phishing detections will
be saved into `phishguard.db` and listed under **History**.

## Environment Variables (optional)

- `PHISHGUARD_DB`: path to SQLite database (default: `phishguard.db`)
- `PHISHGUARD_MODEL`: path to model pickle (default: `phishguard_model.pkl`)
- `PHISHGUARD_THRESHOLD`: float in [0,1], phishing cutoff (default: `0.6`)
- `PHISHGUARD_INFO_URL`: URL for the info button (default: `https://phishtank.org/`)

## Deploy Notes

- This app requires a backend server; it can't run on GitHub Pages alone.
- You can deploy to services like **Render**, **Railway**, **Fly.io**, **Azure Web Apps**, etc.
- Remember to persist or mount a volume if you want the DB/model to survive restarts.

## Acknowledgements

Inspired by anti-phishing communities such as **PhishTank**.
```

