#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from feature_extractor import extract_url_features
from model import PhishModel
from database import init_db, insert_result, get_phishing_history

# ----- Config -----
DATABASE_PATH = os.environ.get("PHISHGUARD_DB", "phishguard.db")
MODEL_PATH = os.environ.get("PHISHGUARD_MODEL", "phishguard_model.pkl")
THRESHOLD = float(os.environ.get("PHISHGUARD_THRESHOLD", "0.6"))
INFO_URL = os.environ.get("PHISHGUARD_INFO_URL", "https://phishtank.org/")

app = Flask(__name__)

# Initialize DB and Model at startup
init_db(DATABASE_PATH)
model = PhishModel(MODEL_PATH)
model.ensure_trained()  # trains once if model file doesn't exist

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", info_url=INFO_URL)

@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url", "").strip()
    if not url:
        return render_template("index.html", error="Please paste a URL.", info_url=INFO_URL)

    features = extract_url_features(url)
    proba = model.predict_proba([features])[0]  # probability of phishing
    is_phishing = proba >= THRESHOLD

    # Persist only phishing URLs in history (per requirement)
    if is_phishing:
        insert_result(DATABASE_PATH, url, int(is_phishing), float(proba))

    return render_template(
        "index.html",
        prediction="Phishing URL" if is_phishing else "No Phishing",
        probability=f"{proba:.2f}",
        url_checked=url,
        info_url=INFO_URL,
        is_phishing=is_phishing
    )

@app.route("/history", methods=["GET"])
def history():
    rows = get_phishing_history(DATABASE_PATH, limit=250)
    return render_template("history.html", rows=rows, info_url=INFO_URL)

@app.route("/api/history", methods=["GET"])
def api_history():
    rows = get_phishing_history(DATABASE_PATH, limit=1000)
    return jsonify([{"id": r[0], "url": r[1], "probability": r[3], "timestamp": r[4]} for r in rows])

@app.route("/info")
def info():
    return redirect(INFO_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
