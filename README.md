# Movies API
A RESTful API built with FastAPI, SQLAlchemy, and MySQL to manage a movie catalog and their respective reviews.

## Features
- Create, list, retrieve, update, and delete movies

- Create, list, retrieve, update, and delete reviews for each movie

## Data Model
### Movies

- id_movie (Primary Key)

- movie

- description

### Reviews

- id_review (Primary Key)

- id_movie (Foreign Key)

- movie_name

- comment

- score
