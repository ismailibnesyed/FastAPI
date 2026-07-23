from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Annotated, Optional

import models
from models import movies
from database import engine, SessionLocal
from fastapi.responses import JSONResponse

app = FastAPI()

GENRES = {
    "action": "Action",
    "comedy": "Comedy",
    "drama": "Drama",
    "thriller": "Thriller"
}

def validate_genre(genre: str):
    if genre not in GENRES:
        raise HTTPException(status_code=422, detail=f"Invalid genre '{genre}'. Must be one of {list(GENRES.keys())}")

class MovieCreate(BaseModel):
    movie_id: int = Field(gt=0)
    title: str
    director: str
    genre: str
    duration: int = Field(gt=0)
    rating: float = Field(ge=0, le=5)

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    director: Optional[str] = Field(default=None)
    genre: Optional[str] = Field(default=None)
    duration: Optional[int] = Field(default=None, gt=0)
    rating: Optional[float] = Field(default=None, ge=0, le=5)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

type db_dependency = Annotated[Session, Depends(get_db)]

# Get all movies
@app.get('/movies')
def read_movies(db: db_dependency):
    return db.query(movies).all()

# Get a specific movie
@app.get('/movies/{movie_id}')
def read_specific_movie(db: db_dependency, movie_id: int):
    specific_movie = (db.query(movies).filter(movies.movie_id == movie_id).first())

    if specific_movie is not None:
        return specific_movie
    raise HTTPException(status_code=404,  detail='Movie is not found. Please try again.')

# Create a new movie
@app.post('/create_movies/')
def create_movies(db: db_dependency, new_movie: MovieCreate ):
    # Validate genre
    validate_genre(new_movie.genre)

    # Check if movie already exists
    existing_movie = (db.query(movies).filter(movies.movie_id == new_movie.movie_id).first())

    if existing_movie is not None:
        raise HTTPException(status_code=400,detail='Movie with this movie id already exists.')

    # Create movie
    movie_published = movies(**new_movie.model_dump())

    db.add(movie_published)
    db.commit()
    db.refresh(movie_published)

    return JSONResponse(status_code=201, content={'message': 'Movie published successfully.'})


# Update movie
@app.put('/movies/{movie_id}')
def update_movie(db: db_dependency, movie_id: int,update_movies: MovieUpdate):
    # Find movie
    movie = (db.query(movies).filter(movies.movie_id == movie_id).first())

    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found.')

    # Validate genre only if genre is provided
    if update_movies.genre is not None:
        validate_genre(update_movies.genre)

    # Update only provided fields
    update_data = update_movies.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    return JSONResponse(status_code=200, content={'message': 'Movie updated successfully.'})

# Delete movie
@app.delete('/movies/{movie_id}')
def delete_movies(db: db_dependency, movie_id: int):
    # Find movie
    movie = (db.query(movies).filter(movies.movie_id == movie_id).first())

    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found.')

    # Delete movie
    db.delete(movie)
    db.commit()

    return JSONResponse(status_code=200, content={'message': 'Movie deleted successfully.'})

# Sort movies
@app.get('/movie/sort')
def sort_movies(db: db_dependency, sort_by: str = 'rating', order: str = 'desc'):
    # Validate sort_by
    if sort_by not in ['duration', 'rating']:
        raise HTTPException(status_code=422, detail="sort_by must be either 'duration' or 'rating'")

    # Validate order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=422, detail="order must be either 'asc' or 'desc'")
    column = getattr(movies, sort_by)

    if order == 'asc':
        return db.query(movies).order_by(column.asc()).all()
    return db.query(movies).order_by(column.desc()).all()

