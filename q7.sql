SELECT CONCAT(c.first_name , ' ',c.last_name) , f.title , cast(f.rental_duration / 7 as decimal(10,4))
FROM customer as c , film as f ,rental as r 
where r.customer_id = c.customer_id and f.film_id = r.rental_id and f.rental_duration >= ALL (
SELECT f.rental_duration
FROM customer as c , film as f ,rental as r 
where r.customer_id = c.customer_id and f.film_id = r.rental_id)