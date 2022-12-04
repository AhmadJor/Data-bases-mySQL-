SELECT name
FROM sakila.category
WHERE REGEXP_LIKE(name,'^[^a]*a[^a]*$'); #inCase sensetive natching category