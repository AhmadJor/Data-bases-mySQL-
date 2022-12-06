SELECT first_name, last_name 
FROM actor, film_actor
WHERE (SELECT COUNT(film_id)
		FROM film_actor
        WHERE actor.actor_id = film_actor.actor_id 
        GROUP BY actor_id) > (9 + (SELECT AVG((SELECT COUNT(film_id)
		FROM film_actor
        WHERE actor.actor_id = film_actor.actor_id
        GROUP BY actor_id))))
ORDER BY first_name, last_name ;