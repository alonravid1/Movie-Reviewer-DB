SELECT f.title, ft.title
FROM film f, film_text ft
WHERE f.film_id = ft.film_id
	AND f.title <> ft.title
ORDER BY f.title;