-- Find the full name, film title, and rental period for customers who have rented films
SELECT
  CONCAT(customer.first_name, ' ', customer.last_name) AS "full name",
  film.title,
  DATEDIFF(rental.return_date, rental.rental_date)/7 AS renatl_period
FROM customer, film, rental, inventory

-- Join the customer, film, rental, and inventory tables on the relevant keys
WHERE customer.customer_id = rental.customer_id
  AND inventory.film_id = film.film_id
  AND inventory.inventory_id = rental.inventory_id

-- Only include customers who have rented films for the longest period
HAVING renatl_period >= ALL (
  SELECT MAX(DATEDIFF(rental.return_date, rental.rental_date)/7) AS renatl_period
  FROM rental
);





