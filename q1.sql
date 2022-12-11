-- Find all categories whose name contains one 'a'
SELECT name
FROM category
WHERE name REGEXP '^[^a]*a[^a]*$'
