from sqlalchemy.orm import Session

from . import models, schemas



#################### Criando um filme e uma review ################################
def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movies(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def create_review(db: Session, review: schemas.ReviewCreate, movie_id: int):
    db_review = models.Reviews(**review.dict(), id_movie=movie_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


#################### Pegando todos filmes e reviews #################################
def get_all_movies(db: Session, skip: int = 0, limit: int = 100 ):
    movies = db.query(models.Movies).offset(skip).limit(limit).all()
    return movies

def get_all_reviews_movie(db: Session,movie_id: int):
    reviews = db.query(models.Reviews).filter(models.Reviews.id_movie == movie_id).all()
    return reviews


################## Pegando um filme e review específico ###############################
def get_movie( db: Session , movie_id: int):
    movie = db.query(models.Movies).filter(models.Movies.id_movie == movie_id).first()
    return movie

def get_review( db: Session , review_id: int, movie_id:int):
    movie = db.query(models.Movies).filter(models.Movies.id_movie == movie_id).first()
    if movie:
        review = db.query(models.Reviews).filter(models.Reviews.id_review == review_id,
                models.Reviews.id_movie == movie_id).first()
        return review
    return None

################# Atualizando os filmes e as reviews #################################
def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate):
    db_movie = db.query(models.Movies).filter(models.Movies.id_movie == movie_id).first()
    db_review = db.query(models.Reviews).filter(models.Reviews.id_movie == movie_id).all()
    if db_movie:
        db_movie.movie = movie.movie
        db_movie.description = movie.description
        for review in db_review:
            review.movie_name = movie.movie
        db.commit()
        db.refresh(db_movie)
    return db_movie

def update_review(db: Session, review_id: int, review: schemas.ReviewCreate):
    db_review = db.query(models.Reviews).filter(models.Reviews.id_review == review_id).first()
    if db_review:
        db_review.id_movie = review.id_movie
        db_review.movie_name = review.movie_name
        db_review.comment = review.comment
        db_review.score = review.score
        db.commit()
        db.refresh(db_review)
    return db_review


################ Deletando um filme e uma review ####################################

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movies).filter(models.Movies.id_movie == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.query(models.Reviews).filter(models.Reviews.id_movie == movie_id).delete() 
        db.commit()
        remaining_movies = db.query(models.Movies).all() 
        return remaining_movies
    return None

def delete_review(db: Session, review_id: int, movie_id: int):
    db_movie = db.query(models.Movies).filter(models.Movies.id_movie == movie_id).first()
    if db_movie:
        db_review = db.query(models.Reviews).filter(models.Reviews.id_review == review_id,
                models.Reviews.id_movie == movie_id).first()
        db.delete(db_review)
        db.commit()
        remaining_reviews = db.query(models.Reviews).all()
        return remaining_reviews
    return None