CREATE OR REPLACE VIEW kpi_lead_time_category AS
WITH order_category AS (
    SELECT DISTINCT
        oc.order_id,
        COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category_en,
        oc.actual_lead_time_days,
        oc.is_late
    FROM orders_clean oc
    JOIN items i
        ON oc.order_id = i.order_id
    JOIN products p
        ON i.product_id = p.product_id
    LEFT JOIN translations t
        ON p.product_category_name = t.product_category_name
)
SELECT
    category_en,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_lead_time,
    ROUND(MEDIAN(actual_lead_time_days), 1) AS median_lead_time,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY actual_lead_time_days), 1) AS p75_lead_time,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY actual_lead_time_days), 1) AS p90_lead_time,
    ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY actual_lead_time_days), 1) AS p99_lead_time,
    ROUND(STDDEV(actual_lead_time_days), 1) AS lead_time_std,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS late_rate_pct
FROM order_category
GROUP BY 1
HAVING COUNT(DISTINCT order_id) >= 200
ORDER BY p90_lead_time DESC;
