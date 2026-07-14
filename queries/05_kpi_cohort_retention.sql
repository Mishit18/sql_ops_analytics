CREATE OR REPLACE VIEW kpi_cohort_retention AS
WITH first_purchase AS (
    SELECT
        customer_unique_id,
        DATE_TRUNC('month', MIN(purchase_ts)) AS cohort_month,
        COUNT(*) AS lifetime_orders
    FROM orders_clean
    GROUP BY 1
),
monthly_activity AS (
    SELECT
        oc.customer_unique_id,
        fp.cohort_month,
        DATE_TRUNC('month', oc.purchase_ts) AS activity_month,
        DATEDIFF('month', fp.cohort_month, DATE_TRUNC('month', oc.purchase_ts)) AS month_number
    FROM orders_clean oc
    JOIN first_purchase fp
        ON oc.customer_unique_id = fp.customer_unique_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_unique_id) AS cohort_customers
    FROM first_purchase
    GROUP BY 1
)
SELECT
    ma.cohort_month,
    ma.month_number,
    cs.cohort_customers,
    COUNT(DISTINCT ma.customer_unique_id) AS active_customers,
    ROUND(100.0 * COUNT(DISTINCT ma.customer_unique_id) / cs.cohort_customers, 1) AS retention_rate_pct
FROM monthly_activity ma
JOIN cohort_size cs
    ON ma.cohort_month = cs.cohort_month
WHERE ma.cohort_month >= DATE '2017-01-01'
  AND ma.month_number <= 12
GROUP BY 1, 2, 3
ORDER BY 1, 2;
