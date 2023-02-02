SELECT name from stars
JOIN movies
on stars.movie_id = movies.id
JOIN people
on stars.person_id = people.id
Where title = "Toy Story";
