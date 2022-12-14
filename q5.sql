#assumed the length  is in minutes and should be
#returned as such
SELECT c.name, AVG(f.length) as average_length
FROM category c, film_category fc, film f
WHERE fc.film_id = f.film_id
	AND fc.category_id = c.category_id
GROUP BY c.name