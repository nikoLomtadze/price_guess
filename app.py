# app.py
from flask import Flask, render_template, request, redirect, url_for
import random, json, os

app = Flask(__name__)

# --------- Load sample listings (JSON) ----------
DATA_FILE = os.path.join(os.path.dirname(__file__), "listings.json")
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        LISTINGS = json.load(f)
else:
    # fallback small sample if there's no JSON file
    LISTINGS = [
        {"id": 1, "title": "Cozy studio, center", "image": "image1.jpg", "price": 35000, "location": "Tbilisi"},
        {"id": 2, "title": "Two-bedroom near park", "image": "image2.webp", "price": 55000, "location": "Tbilisi"},
        {"id": 3, "title": "Sunny flat, high floor", "image": "image3.webp", "price": 76000, "location": "Tbilisi"}
    ]

# --------- helper: compute score ----------
def compute_score(guess, actual):
    try:
        guess = float(guess)
        actual = float(actual)
    except Exception:
        return 0
    if actual <= 0:
        return 0
    diff = abs(guess - actual)
    # percentage difference
    pct = diff / actual
    # score: 100 = perfect, 0 = very far. clamp to 0..100
    score = max(0, int(100 - pct * 100))
    return score

# --------- Routes ----------
@app.route("/")
def index():
    listing = random.choice(LISTINGS)
    return render_template("index.html", listing=listing)

@app.route("/guess", methods=["POST"])
def guess():
    listing_id = int(request.form.get("listing_id", -1))
    guess_price = request.form.get("price", "0")
    # find listing by id
    listing = next((l for l in LISTINGS if l["id"] == listing_id), None)
    if listing is None:
        return redirect(url_for("index"))
    actual = listing.get("price", 0)
    score = compute_score(guess_price, actual)
    diff = None
    try:
        diff = abs(float(guess_price) - float(actual))
    except Exception:
        diff = None
    return render_template("result.html", listing=listing, guess=guess_price, actual=actual, score=score, diff=diff)

if __name__ == "__main__":
    # debug=True for development only
    app.run(debug=True, host="0.0.0.0", port=5000)
