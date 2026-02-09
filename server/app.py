from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
LOCK = threading.Lock()

app = Flask(__name__)
CORS(app)

PER_PAGE = 10

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with LOCK:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

def write_data(data):
    with LOCK:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def validate_movie(payload):
    title = payload.get("title", "").strip()
    genre = payload.get("genre", "").strip()
    try:
        year = int(payload.get("year", 0))
        rating = int(payload.get("rating", 0))
    except Exception:
        return False, "Year and rating must be numbers"

    if not title or not genre:
        return False, "Title and genre are required"
    if year < 1900 or year > 2100:
        return False, "Year out of range"
    if rating < 1 or rating > 10:
        return False, "Rating must be between 1 and 10"
    return True, None

@app.route("/movies", methods=["GET"])
def list_movies():
    page = int(request.args.get("page", 1))
    data = read_data()
    total = len(data)
    total_pages = (total + PER_PAGE - 1) // PER_PAGE
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    return jsonify({
        "total": total,
        "page": page,
        "per_page": PER_PAGE,
        "total_pages": total_pages,
        "data": data[start:end]
    })

@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    data = read_data()
    for m in data:
        if m.get("id") == movie_id:
            return jsonify(m)
    abort(404)

@app.route("/movies", methods=["POST"])
def create_movie():
    payload = request.get_json() or {}
    ok, msg = validate_movie(payload)
    if not ok:
        return jsonify({"error": msg}), 400
    data = read_data()
    new_id = max([m.get("id", 0) for m in data] + [0]) + 1
    movie = {
        "id": new_id,
        "title": payload["title"].strip(),
        "genre": payload["genre"].strip(),
        "year": int(payload["year"]),
        "rating": int(payload["rating"])
    }
    data.append(movie)
    write_data(data)
    return jsonify(movie), 201

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    payload = request.get_json() or {}
    ok, msg = validate_movie(payload)
    if not ok:
        return jsonify({"error": msg}), 400
    data = read_data()
    for m in data:
        if m.get("id") == movie_id:
            m["title"] = payload["title"].strip()
            m["genre"] = payload["genre"].strip()
            m["year"] = int(payload["year"])
            m["rating"] = int(payload["rating"])
            write_data(data)
            return jsonify(m)
    abort(404)

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    data = read_data()
    new = [m for m in data if m.get("id") != movie_id]
    if len(new) == len(data):
        abort(404)
    write_data(new)
    return jsonify({"deleted": movie_id})

@app.route("/stats", methods=["GET"])
def stats():
    data = read_data()
    total = len(data)
    avg = 0
    if total:
        avg = sum([m.get("rating", 0) for m in data]) / total
    return jsonify({"total": total, "average_rating": round(avg, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
