-- Select the titles of films from the film and film_text tables
SELECT film.title, film_text.title

-- Join the film and film_text tables on the film_id column
FROM film, film_text

-- Only include rows where the film and film_text titles are different
WHERE film.film_id = film_text.film_id AND film.title <> film_text.title 

-- Order the results by the film title
ORDER BY film.title;
