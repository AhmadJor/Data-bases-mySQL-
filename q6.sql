-- Find all the actors who have acted in at least 10 movies more than the average number of
-- movies per actor, and return their first and last names.
-- Order the results by first and last names.

SELECT  actor.first_name, actor.last_name
FROM actor

-- Join the `actor` table with a subquery that calculates the number of movies each actor has
-- starred in, grouped by actor ID.

JOIN (
    SELECT actor_id, COUNT(*) as counter
    FROM film_actor
    GROUP BY actor_id
) as film_count ON actor.actor_id = film_count.actor_id

-- Join the `actor` table with another subquery that calculates the average number of movies
-- per actor, grouped by actor ID.

JOIN (
    SELECT AVG(film_count.counter) as average
    FROM (
        SELECT actor_id, COUNT(*) as counter
        FROM film_actor
        GROUP BY actor_id
    ) as film_count
) as avrage_of_count ON (avrage_of_count.average + 10) <= film_count.counter

-- Order the results by the actors' first and last names.

ORDER BY actor.first_name, actor.last_name;
