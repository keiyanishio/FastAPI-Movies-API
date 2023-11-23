from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Movies(Base):
    __tablename__ = "movies"

    id_movie = Column(Integer, primary_key=True, index=True, autoincrement = True, nullable = False)
    movie = Column(String, unique=True, index=True, nullable = False)
    description = Column(String)

    reviews = relationship("Reviews", back_populates="movies")


class Reviews(Base):
    __tablename__ = "reviews"

    id_review = Column(Integer, primary_key=True, index=True, autoincrement = True, nullable = False)
    id_movie = Column(Integer, ForeignKey('movies.id_movie'), nullable = False)
    movie_name = Column(String, index=True, nullable = False)
    comment = Column(String, index=True)
    score = Column(Integer, nullable = False)

    movies = relationship("Movies", back_populates="reviews")
    
    