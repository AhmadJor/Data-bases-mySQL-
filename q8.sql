-- Find all the actors who are not customers
SELECT actor.first_name, actor.last_name
FROM actor
WHERE actor.first_name NOT IN (SELECT customer.first_name FROM customer)

UNION

-- Find all the customers who are not actors
SELECT customer.first_name, customer.last_name
FROM customer
WHERE customer.first_name NOT IN (SELECT actor.first_name FROM actor);
