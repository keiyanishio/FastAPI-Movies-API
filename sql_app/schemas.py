from typing import List, Union

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    movie_name: Union[str] = Field (default=None, title="Title of the movie")
    comment: Union[str, None] = Field(default=None, title="Review of the movie")
    score: int = Field(default=0, ge=0, le=10, description="The score must be greater than or equal to zero and less than ten")
    
class ReviewCreate(ReviewBase):
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "movie_name": "Star Wars 5",
                "comment": "Amazing",
                "score": 10
            }
        }
    

class Review(ReviewBase):
    id_review: int
    id_movie: int
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_review": "0",
                "id_movie": "0",
                "movie_name": "Star Wars 2",
                "comment": "Very good",
                "score": 9,
            }
        }
    


class MovieBase(BaseModel):
    movie: Union[str] = Field (default=None, title="Title of the movie")
    description: Union[str, None] = Field (default=None, title="Movie description")
    
class MovieCreate(MovieBase):
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "movie": "Star Wars 5",
                "description": "A scifi movie",
            }
    }
    

class Movie(MovieBase):
    id_movie: int
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_movie": "0",
                "movie": "Star Wars 2",
                "description": "A scifi movie",
            }
        }
        
        
        
        
        
        

    
    