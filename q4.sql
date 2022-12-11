-- Find the full names of customers who rented the most films in May 2005
SELECT CONCAT(c.first_name , ' ',c.last_name) as full_name
FROM  customer AS c , film AS f,rental AS r
-- Join the customer, film, and rental tables
where r.rental_id = f.film_id and c.customer_id = r.customer_id  
-- Filter only records from May 2005
and r.rental_date like '2005-05-% %'
-- Group by customer ID
group by c.customer_id
-- Get only customers who rented the most films in May 2005
having count(c.customer_id) >= ALL (select count(c.customer_id) from customer as C,film as f,rental AS r
 where r.rental_id = f.film_id and c.customer_id = r.customer_id  
 and r.rental_date like '2005-05-% %'
 group by c.customer_id)
