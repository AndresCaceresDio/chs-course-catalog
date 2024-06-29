SELECT rating, title FROM ratings, movies WHERE movie_id = id AND year = 2010 ORDER BY rating DESC, title LIMIT 8;
