SELECT title FROM movies WHERE id = (SELECT movie_id FROM stars WHERE per)
