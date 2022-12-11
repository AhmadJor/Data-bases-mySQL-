-- Find films that are shorter than 90 minutes
-- and have a PG or G rating
SELECT film_id , title
FROM sakila.film
WHERE length < 90
  AND (rating = 'PG' OR rating = 'G')
