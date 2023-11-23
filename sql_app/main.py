from typing import Union, List, Set, Dict
from fastapi import FastAPI, Query, Path, Body, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from . import CRUD, models, schemas
from .database import SessionLocal, engine
#Body
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

########## Criando filmes e avaliações##############
@app.post("/movies/", response_model=schemas.Movie, tags=["Post Movies"], summary="Create a movie")
async def create_movie (movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Create a movie with all the information:

    - *id_movie*: auto increment
    - *movie*: each movie must have a name 
    - *description*: a description of the movie
    """
    
    return CRUD.create_movie(db, movie)

@app.post("/movies/{movie_id}/review", response_model=schemas.Review, tags=["Post Reviews"], summary ="Create a review")
async def create_review (review: schemas.ReviewCreate, movie_id: int, db: Session = Depends(get_db)):
    """
    Create a review with all the information:
    
    - *id_review*: each review must have a id (auto increment)
    - *id_movie*: each movie must have a id (using the id of a movie in the database)
    - *movie_name*: each movie must have a name 
    - *comment*: a comment about the movie
    - *score*: a score for the movie between 0 to 10, must be integer
    """
    db_review = CRUD.get_review(db, review, movie_id)
    if db_review:
        raise HTTPException(status_code=400, detail = "Review already exist")
    return CRUD.create_review(db, review, movie_id)

############# Obtendo todos os filmes e avaliações ###############
@app.get("/movies/", response_model=List[schemas.Movie], tags=["Get Movies"], summary="Get all movies")
async def read_all_movies (skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all the movies in the database
    
    """
    movies = CRUD.get_all_movies(db, skip=skip, limit=limit)
    return movies



@app.get("/movies/{movie_id}/reviews/", response_model=List[schemas.Review], tags=["Get Reviews"], summary="Get all reviews of certain movie")
async def read_all_reviews(movie_id: int, db: Session = Depends(get_db)):
    """
    Get all reviews of a specific movie:
    
    - *movie_id*: to choose the right movie  (using an existing id of a movie in the database)
   
    """
    db_movie = CRUD.get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="This movie does not exist")
    reviews = CRUD.get_all_reviews_movie(db, movie_id)
    return reviews

##################Pegando um filme e uma review específico######################

@app.get("/movies/{movie_id}",  response_model=schemas.Movie, tags=["Get Movies"], summary="Get a specific movie")
async def read_movies(movie_id: int, db: Session = Depends(get_db)):
    
    """
    Get a specific movie:
    
    - *movie_id*: to choose the right movie  (using an existing id of a movie in the database)
    """
    
    db_movie = CRUD.get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="This movie does not exist")
    return db_movie


@app.get("/movies/{movie_id}/reviews/{review_id}",  response_model=schemas.Review, tags=["Get Reviews"], summary="Get a specific review")
async def read_reviews(review_id: int, movie_id: int,db: Session = Depends(get_db)):
    
    """
    Get a specific review:
    - *movie_id*: to choose the right movie  (using an existing id of a movie in the database)
    - *review_id*: to choose the right review  (using an existing id of a review in the database)
    """
    db_review = CRUD.get_review(db, review_id, movie_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="This review does not exist")
    return db_review


################ Atualizando os filmes e avaliações #################

@app.put("/movies/{movie_id}", response_model=schemas.Movie, tags=["Put Movies"], summary = "Update a specific movie")
async def update_movie(movie_id: int, movie: schemas.Movie,  db: Session = Depends(get_db)):
    """
    Update a specific movie, but if you update the name of the movie you also will chage the name of all review
    related to that movie:
    
    - *movie_id*: select the movie that you want to modify
    - *id_movie*: can't be modify 
    - *movie*: chaning the name of the movie (optional)
    - *description*: changing the description (optional)
    """
    
    db_movie = CRUD.get_movie(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="This movie does not exist")
    movie = CRUD.update_movie(db, movie_id, movie)
    return movie

@app.put("/movies/{movie_id}/reviews/{review_id}", response_model=schemas.Review, tags = ["Put Reviews"], summary = "Update a specific reciew")
async def upadate_review(review_id: int, movie_id: int, review: schemas.Review, db: Session = Depends(get_db)):
    """
    Update a specific review of movie. However, you can't change the id_review and id_movie:
    - *movie_id*: select a movie to change the review for the movie 
    - *review_id*: select the review that you want to modify
    - *id_movie*: be modify
    - *id_review*: can't be modify
    - *movie_name*: be modify
    - *comment*: chaning the comment (optional)
    - *score*: changing the score (optional)
    """
    db_review = CRUD.get_review(db, review_id, movie_id)
    if db_review is None:
        raise HTTPException(status_code=400, detail = "This review does not exist")
    review = CRUD.update_review(db, review_id, review)
    return review

################ Deletando filme e avaliação############################3

@app.delete("/movies/{movie_id}", response_model=List[schemas.Movie],tags=["Delete Movies"], summary = "Delete a specific movie")
async def remove_movie(movie_id: int, db: Session = Depends(get_db)):
    
    """
    Delete a specific movie and the reviews of that movie:
    
    - *movie_id*: select the movie that you want to delete

    """
    db_movie = CRUD.get_movie(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="This review does not exist")
    return CRUD.delete_movie(db, movie_id)
    


@app.delete("/movies/{movie_id}/reviews/{review_id}", response_model=List[schemas.Review],tags=["Delete Reviews"], summary = "Delete a specific review")
async def remove_review(review_id: int, movie_id: int,db: Session = Depends(get_db)):
    
    """
    Delete a specific review:
    
    - *movie_id*: select the movie to delete the review related 
    - *review_id*: select a review that you want to delete of a movie

    """
    
    db_review = CRUD.get_review(db, review_id, movie_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="This review does not exist")
    return CRUD.delete_review(db, review_id, movie_id)

    