select distinct name from stars
join people
ON stars.person_id = people.id
join movies
on stars.movie_id = movies.id
where year = 2004
order by birth;