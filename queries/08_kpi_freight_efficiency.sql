CREATE OR REPLACE VIEW kpi_freight_efficiency AS
SELECT
    s.seller_state,
    oc.customer_state,
    COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category_en,
    COUNT(*) AS shipments,
    ROUND(AVG(i.freight_value), 2) AS avg_freight_cost,
    ROUND(AVG(i.price), 2) AS avg_item_value,
    ROUND(AVG(i.freight_value / NULLIF(i.price, 0)) * 100, 1) AS freight_pct_of_value,
    ROUND(AVG(oc.actual_lead_time_days), 1) AS avg_lead_time,
    ROUND(100.0 * SUM(oc.is_late) / COUNT(*), 1) AS late_rate_pct
FROM orders_clean oc
JOIN items i
    ON oc.order_id = i.order_id
JOIN sellers s
    ON i.seller_id = s.seller_id
JOIN products p
    ON i.product_id = p.product_id
LEFT JOIN translations t
    ON p.product_category_name = t.product_category_name
WHERE i.freight_value > 0
GROUP BY 1, 2, 3
HAVING COUNT(*) >= 20
ORDER BY avg_freight_cost DESC;
