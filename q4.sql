SELECT CONCAT(c.first_name , ' ',c.last_name)
FROM  customer AS c , film AS f,rental AS r
where r.rental_id = f.film_id and c.customer_id = r.customer_id  and r.rental_date like '2005-05-% %'
group by c.customer_id
having count(c.customer_id) >= ALL (select count(c.customer_id) from customer as C,film as f,rental AS r
 where r.rental_id = f.film_id and c.customer_id = r.customer_id  and r.rental_date like '2005-05-% %'
 group by c.customer_id)