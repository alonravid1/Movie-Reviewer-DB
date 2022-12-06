#assuming that t"rented largest number of films "
#isn't accounting return date, and that the same movie
#rented twice counts as two for the number of films.
SELECT concat(c.first_name, ' ', c.last_name) as full_name
FROM customer c, rental r
WHERE c.customer_id = r.customer_id
HAVING COUNT(r.rental_id) >= ALL(
				SELECT COUNT(r.rental_id)
				FROM rental r, customer c
				WHERE r.customer_id = c.customer_id
					AND r.rental_date between '2006/05/01' and '2006/05/31');
