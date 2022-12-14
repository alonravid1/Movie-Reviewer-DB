#assumed that dividing the date difference by 7 is ts
#the expected representation of a time as weeks.
#assumed accuracy up to days a
SELECT
	concat(cu.first_name, ' ', cu.last_name) as full_name,
    f.title,
    DATEDIFF(r.return_date, r.rental_date)/7 as duration
FROM customer cu, film f, rental r, inventory i
WHERE cu.customer_id = r.customer_id
	AND r.inventory_id = i.inventory_id
    AND i.film_id = f.film_id
HAVING duration = (
					SELECT MAX(DATEDIFF(r.return_date, r.rental_date)/7)
                    FROM rental r
                    );
