# 🎬 Movie Collection API

A RESTful API built with **FastAPI** and **SQLite** for managing a personal movie collection — supporting full CRUD operations, request validation with **Pydantic**, and dynamic sorting.

> Built as part of Phitron Module 8 — Assignment 01 (FastAPI + SQLAlchemy + SQLite).

---

## 🚀 Features

- Persistent storage using **SQLite** (via SQLAlchemy ORM)
- Request validation with **Pydantic models**
- Full CRUD support: Create, Read, Update, Delete
- Query-based sorting by `duration` or `rating`
- Proper HTTP status codes and error handling (`404`, `400`, `422`)

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Validation | Pydantic |
| Language | Python 3.12+ |

---

## 📂 Project Structure

```
movie-collection-api/
├── main.py          # API routes and app entry point
├── models.py        # SQLAlchemy ORM model (movies table)
├── database.py       # DB engine, session, and Base setup
├── movies.db         # SQLite database file (auto-generated)
└── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/movie-collection-api.git
   cd movie-collection-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open the interactive docs**
   Visit `http://127.0.0.1:8000/docs` (Swagger UI) to test endpoints directly.

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/movies` | Get all movies |
| `GET` | `/movies/{movie_id}` | Get a single movie by ID |
| `GET` | `/movies/sort?sort_by=&order=` | Get movies sorted by `duration` or `rating` |
| `POST` | `/create_movies` | Add a new movie |
| `PUT` | `/movies/{movie_id}` | Update an existing movie |
| `DELETE` | `/movies/{movie_id}` | Delete a movie |

### Data Model

| Field | Type | Notes |
|---|---|---|
| `movie_id` | int | Primary key, sent by client |
| `title` | str | Movie title |
| `director` | str | Director's name |
| `genre` | str | One of: `action`, `comedy`, `drama`, `thriller` |
| `duration` | int | Runtime in minutes (must be > 0) |
| `rating` | float | Between `0` and `5` inclusive |

---

## 🔍 Example Request

**Create a movie**
```bash
curl -X POST "http://127.0.0.1:8000/create_movies" \
-H "Content-Type: application/json" \
-d '{
  "movie_id": 1,
  "title": "Inception",
  "director": "Christopher Nolan",
  "genre": "thriller",
  "duration": 148,
  "rating": 4.8
}'
```

**Sort movies by duration, ascending**
```bash
curl "http://127.0.0.1:8000/movies/sort?sort_by=duration&order=asc"
```

---

## 📖 Assignment Context

This project fulfills **Module 8 — Assignment 01: Movie Collection API** from Phitron's backend curriculum, focused on:

- Building CRUD endpoints with FastAPI
- Using Pydantic for automatic request validation
- Persisting data with SQLite instead of in-memory lists
- Working with path and query parameters

---

## 👤 Author

**Md Ismail Hossain**
Electronics and Telecommunication Engineering, CUET
Self-directed full-stack development learner
