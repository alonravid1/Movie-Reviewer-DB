#assumes that the first month of a year should be
#checked against the last month of the previous year
SELECT a.store_id, ABS(a.total_payment-b.total_payment) as earning_difference
FROM (
	#create two tables containing the store, year, month and total payments
	SELECT st.store_id, YEAR(p.payment_date) as year, MONTH(p.payment_date) as month,
    SUM(p.amount) as total_payment
    FROM payment p, staff st
    WHERE st.staff_id = p.staff_id
	GROUP BY st.store_id, YEAR(p.payment_date),MONTH(p.payment_date)
	) AS a,
    (
	SELECT st.store_id, YEAR(p.payment_date) as year, MONTH(p.payment_date) as month,
    SUM(p.amount) as total_payment
    FROM payment p, staff st
    WHERE st.staff_id = p.staff_id
	GROUP BY st.store_id, YEAR(p.payment_date),MONTH(p.payment_date)
	) AS b
WHERE ((a.month = (b.month + 1)
		AND a.year = b.year)
    OR (a.month = 1
		AND b.month = 12
        AND a.year = (b.year + 1)))
	AND a.store_id = b.store_id
ORDER BY earning_difference DESC
LIMIT 1;
