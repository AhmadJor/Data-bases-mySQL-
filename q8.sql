(SELECT DISTINCT actor.first_name, actor.last_name
FROM actor, customer
WHERE actor.first_name <> ALL (SELECT customer.first_name))
UNION
(SELECT customer.first_name, customer.last_name
FROM actor, customer
WHERE customer.first_name <> ALL (SELECT actor.first_name));