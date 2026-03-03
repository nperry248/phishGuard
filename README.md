# PhishGuard

A Chrome extension that detects phishing URLs in real time using a machine learning model. Click the extension on any page to instantly see whether the site is safe or a potential phishing threat.

## How It Works

1. You open the extension on any page
2. The extension sends the current URL to a Flask API hosted on Render
3. The API extracts 20+ features from the URL — length, special characters, HTTP headers, WHOIS registration data, redirect history, and more
4. A trained scikit-learn classifier predicts whether the URL is phishing or benign
5. The result is displayed in the popup: ✓ safe or ⚠ potential phishing

## Stack

- **Chrome Extension** (Manifest V3) — captures the active tab URL and displays the result
- **Python / Flask** — REST API deployed on Render
- **scikit-learn** — pre-trained ML classifier (`KtpCapstoneModel.pkl`)
- **python-whois, requests** — feature extraction from live URLs

## Running Locally

**Backend:**
```bash
cd webserver
pip install -r requirements.txt
python app.py
```

Update `API_URL` in `chrome/background.js` to `http://127.0.0.1:5000`.

**Extension:**
1. Open Chrome → `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select the `chrome/` folder

## Deploying the Backend (Render)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service → connect the repo
3. Set **Root Directory** to `webserver`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. After deploy, copy your Render URL and update `API_URL` in `chrome/background.js`
