SELECT c.first_name as "first name", c.last_name as "last name"
FROM customer c
WHERE c.first_name NOT IN (
	SELECT first_name
    FROM actor)
UNION
SELECT a.first_name, a.last_name
FROM actor a
WHERE a.first_name NOT IN (
	SELECT first_name
    FROM customer)