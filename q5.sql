-- Calculate the average length of films in each category
SELECT c.category_id, AVG(f.length) AS avg_length

-- Join the film and film_category tables
FROM sakila.film AS f
INNER JOIN film_category AS c
    ON c.film_id = f.film_id

-- Group the results by category
GROUP BY c.category_id
