CREATE OR REPLACE VIEW kpi_volume_trend AS
SELECT
    oc.purchase_week,
    COUNT(DISTINCT oc.order_id) AS orders,
    COUNT(DISTINCT oc.customer_unique_id) AS unique_customers,
    ROUND(SUM(i.price + i.freight_value), 0) AS total_gmv,
    ROUND(AVG(i.price), 2) AS avg_item_price,
    ROUND(AVG(i.freight_value), 2) AS avg_freight,
    ROUND(AVG(i.freight_value / NULLIF(i.price, 0)) * 100, 1) AS freight_pct_of_price
FROM orders_clean oc
JOIN items i
    ON oc.order_id = i.order_id
GROUP BY 1
ORDER BY 1;
