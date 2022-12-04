SELECT film_id , title
FROM sakila.film
WHERE length < 90 AND (rating = 'PG' OR rating = 'G')