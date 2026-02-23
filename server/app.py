from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/movie_db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
CORS(app)

PER_PAGE = 10

# Create tables
Base.metadata.create_all(engine)

def seed_data():
    session = Session()
    if session.query(Movie).count() == 0:
        movies = [
            {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3, "image_url": "https://via.placeholder.com/100x150?text=Shawshank"},
            {"title": "The Godfather", "genre": "Crime", "year": 1972, "rating": 9.2, "image_url": "https://via.placeholder.com/100x150?text=Godfather"},
            {"title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0, "image_url": "https://via.placeholder.com/100x150?text=Dark+Knight"},
            {"title": "Pulp Fiction", "genre": "Crime", "year": 1994, "rating": 8.9, "image_url": "https://via.placeholder.com/100x150?text=Pulp+Fiction"},
            {"title": "Forrest Gump", "genre": "Drama", "year": 1994, "rating": 8.8, "image_url": "https://via.placeholder.com/100x150?text=Forrest+Gump"},
            {"title": "Inception", "genre": "Sci-Fi", "year": 2010, "rating": 8.8, "image_url": "https://via.placeholder.com/100x150?text=Inception"},
            {"title": "The Matrix", "genre": "Sci-Fi", "year": 1999, "rating": 8.7, "image_url": "https://via.placeholder.com/100x150?text=Matrix"},
            {"title": "Goodfellas", "genre": "Crime", "year": 1990, "rating": 8.7, "image_url": "https://via.placeholder.com/100x150?text=Goodfellas"},
            {"title": "The Silence of the Lambs", "genre": "Thriller", "year": 1991, "rating": 8.6, "image_url": "https://via.placeholder.com/100x150?text=Silence+of+Lambs"},
            {"title": "Schindler's List", "genre": "Historical", "year": 1993, "rating": 8.9, "image_url": "https://via.placeholder.com/100x150?text=Schindler"},
            {"title": "Fight Club", "genre": "Drama", "year": 1999, "rating": 8.8, "image_url": "https://via.placeholder.com/100x150?text=Fight+Club"},
            {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Fantasy", "year": 2001, "rating": 8.8, "image_url": "https://via.placeholder.com/100x150?text=LOTR"},
            {"title": "Star Wars: Episode V - The Empire Strikes Back", "genre": "Sci-Fi", "year": 1980, "rating": 8.7, "image_url": "https://via.placeholder.com/100x150?text=Empire+Strikes+Back"},
            {"title": "The Usual Suspects", "genre": "Mystery", "year": 1995, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Usual+Suspects"},
            {"title": "Se7en", "genre": "Thriller", "year": 1995, "rating": 8.6, "image_url": "https://via.placeholder.com/100x150?text=Se7en"},
            {"title": "The Green Mile", "genre": "Drama", "year": 1999, "rating": 8.6, "image_url": "https://via.placeholder.com/100x150?text=Green+Mile"},
            {"title": "Gladiator", "genre": "Action", "year": 2000, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Gladiator"},
            {"title": "Saving Private Ryan", "genre": "War", "year": 1998, "rating": 8.6, "image_url": "https://via.placeholder.com/100x150?text=Saving+Private+Ryan"},
            {"title": "American Beauty", "genre": "Drama", "year": 1999, "rating": 8.3, "image_url": "https://via.placeholder.com/100x150?text=American+Beauty"},
            {"title": "The Sixth Sense", "genre": "Thriller", "year": 1999, "rating": 8.1, "image_url": "https://via.placeholder.com/100x150?text=Sixth+Sense"},
            {"title": "Braveheart", "genre": "Historical", "year": 1995, "rating": 8.3, "image_url": "https://via.placeholder.com/100x150?text=Braveheart"},
            {"title": "Titanic", "genre": "Romance", "year": 1997, "rating": 7.8, "image_url": "https://via.placeholder.com/100x150?text=Titanic"},
            {"title": "The Lion King", "genre": "Animation", "year": 1994, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Lion+King"},
            {"title": "Jurassic Park", "genre": "Adventure", "year": 1993, "rating": 8.1, "image_url": "https://via.placeholder.com/100x150?text=Jurassic+Park"},
            {"title": "Terminator 2: Judgment Day", "genre": "Sci-Fi", "year": 1991, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=T2"},
            {"title": "The Departed", "genre": "Crime", "year": 2006, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Departed"},
            {"title": "Avatar", "genre": "Sci-Fi", "year": 2009, "rating": 7.8, "image_url": "https://via.placeholder.com/100x150?text=Avatar"},
            {"title": "Raiders of the Lost Ark", "genre": "Adventure", "year": 1981, "rating": 8.4, "image_url": "https://via.placeholder.com/100x150?text=Raiders"},
            {"title": "Back to the Future", "genre": "Sci-Fi", "year": 1985, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Back+to+Future"},
            {"title": "The Prestige", "genre": "Mystery", "year": 2006, "rating": 8.5, "image_url": "https://via.placeholder.com/100x150?text=Prestige"},
        ]
        for m in movies:
            movie = Movie(**m)
            session.add(movie)
        session.commit()
    session.close()

seed_data()

def validate_movie(payload):
    title = payload.get("title", "").strip()
    genre = payload.get("genre", "").strip()
    image_url = payload.get("image_url", "").strip()
    try:
        year = int(payload.get("year", 0))
        rating = float(payload.get("rating", 0))
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
    session = Session()
    page = int(request.args.get("page", 1))
    query = session.query(Movie)
    total = query.count()
    total_pages = (total + PER_PAGE - 1) // PER_PAGE
    if page < 1: page = 1
    if page > total_pages and total_pages > 0: page = total_pages
    start = (page - 1) * PER_PAGE
    movies = query.offset(start).limit(PER_PAGE).all()
    data = [{"id": m.id, "title": m.title, "genre": m.genre, "year": m.year, "rating": m.rating, "image_url": m.image_url} for m in movies]
    session.close()
    return jsonify({
        "total": total,
        "page": page,
        "per_page": PER_PAGE,
        "total_pages": total_pages,
        "data": data
    })

@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    session = Session()
    movie = session.query(Movie).get(movie_id)
    session.close()
    if not movie:
        abort(404)
    return jsonify({"id": movie.id, "title": movie.title, "genre": movie.genre, "year": movie.year, "rating": movie.rating, "image_url": movie.image_url})

@app.route("/movies", methods=["POST"])
def create_movie():
    payload = request.get_json() or {}
    ok, msg = validate_movie(payload)
    if not ok:
        return jsonify({"error": msg}), 400
    session = Session()
    movie = Movie(
        title=payload["title"].strip(),
        genre=payload["genre"].strip(),
        year=int(payload["year"]),
        rating=float(payload["rating"]),
        image_url=payload.get("image_url", "").strip() or None
    )
    session.add(movie)
    session.commit()
    session.close()
    return jsonify({"id": movie.id, "title": movie.title, "genre": movie.genre, "year": movie.year, "rating": movie.rating, "image_url": movie.image_url}), 201

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    payload = request.get_json() or {}
    ok, msg = validate_movie(payload)
    if not ok:
        return jsonify({"error": msg}), 400
    session = Session()
    movie = session.query(Movie).get(movie_id)
    if not movie:
        session.close()
        abort(404)
    movie.title = payload["title"].strip()
    movie.genre = payload["genre"].strip()
    movie.year = int(payload["year"])
    movie.rating = float(payload["rating"])
    movie.image_url = payload.get("image_url", "").strip() or None
    session.commit()
    session.close()
    return jsonify({"id": movie.id, "title": movie.title, "genre": movie.genre, "year": movie.year, "rating": movie.rating, "image_url": movie.image_url})

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    session = Session()
    movie = session.query(Movie).get(movie_id)
    if not movie:
        session.close()
        abort(404)
    session.delete(movie)
    session.commit()
    session.close()
    return jsonify({"deleted": movie_id})

@app.route("/stats", methods=["GET"])
def stats():
    session = Session()
    total = session.query(Movie).count()
    avg = session.query(Movie).with_entities(Movie.rating).all()
    avg_rating = sum([r[0] for r in avg]) / total if total else 0
    session.close()
    return jsonify({"total": total, "average_rating": round(avg_rating, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
