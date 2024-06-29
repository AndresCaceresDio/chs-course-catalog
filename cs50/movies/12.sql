SELECT title FROM movies WHERE id = (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE birth = 1973));
