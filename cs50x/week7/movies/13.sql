SELECT DISTINCT(name) FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE title IN(SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE name = "Kevin Bacon" AND birth = "1958")
AND name != "Kevin Bacon";