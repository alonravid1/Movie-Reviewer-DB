#assuming no duplicate films since film_id is a key
SELECT film_id, title
FROM film
WHERE length < 90 AND rating REGEXP 'PG|G';