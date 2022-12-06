SELECT a.first_name, a.last_name
FROM actor a, film_actor fa
WHERE a.actor_id = fa.actor_id
GROUP BY a.actor_id
HAVING (COUNT(fa.film_id) - 10) >= (
				SELECT AVG(c.films)
                FROM (SELECT COUNT(film_id) as films
						FROM film_actor
                        GROUP BY actor_id) as c);
