-- Compute the total amount of payments per store and month
WITH total_per_month AS 
(
    SELECT 
        store_id, 
        YEAR(payment.payment_date) AS year, 
        MONTH(payment.payment_date) AS month,
        SUM(payment.amount) AS total_amount
    FROM staff, payment
    WHERE staff.staff_id = payment.staff_id
    GROUP BY store_id, YEAR(payment.payment_date), MONTH(payment.payment_date)
)

-- Compute the difference in earnings between the current and previous months
SELECT 
    a.store_id, 
    (b.total_amount - a.total_amount) AS earning_difference
FROM total_per_month AS a, total_per_month AS b
WHERE a.store_id = b.store_id
AND a.year = b.year
AND a.month + 1 = b.month

-- Order the results by earning difference and return the top result
ORDER BY earning_difference DESC
LIMIT 1
;
