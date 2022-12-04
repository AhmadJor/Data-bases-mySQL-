SELECT c.category_id , avg(f.length)
FROM sakila.film as f, film_category as c
where c.film_id = f.film_id 
group by c.category_id