

CREATE DATABASE IF NOT EXISTS filmes_db;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS movies;


CREATE TABLE if not exists movies (
    id_movie INT AUTO_INCREMENT PRIMARY KEY,
    movie VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE if not exists reviews (
    id_review INT AUTO_INCREMENT PRIMARY KEY,
    id_movie INT NOT NULL,
    movie_name VARCHAR(255) NOT NULL,
    comment VARCHAR(255),
    score INT NOT NULL,
    FOREIGN KEY (id_movie) REFERENCES movies (id_movie)
);


INSERT INTO movies (movie, description) VALUES 
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'), 
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'), 
('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'), 
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.');


INSERT INTO reviews (id_movie, movie_name, comment, score) VALUES 
(1, 'The Shawshank Redemption', 'One of the best movies of all time!', 9), 
(1, 'The Shawshank Redemption', 'Amazing acting and story!', 10), 
(2, 'The Godfather', 'A classic that everyone should watch.', 8), 
(2, 'The Godfather', 'Great acting and directing.', 9), 
(3, 'The Dark Knight', 'Heath Ledger\'s Joker is a masterpiece.', 10), 
(3, 'The Dark Knight', 'One of the best superhero movies ever made.', 9), 
(4, 'Pulp Fiction', 'A must-see for anyone who loves movies.', 8), 
(4, 'Pulp Fiction', 'Quentin Tarantino at his best.', 9);

select * from movies;
select * from reviews;