CREATE OR REPLACE VIEW kpi_product_velocity AS
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category_en,
    COUNT(i.order_item_id) AS units_sold,
    COUNT(DISTINCT oc.order_id) AS orders,
    ROUND(SUM(i.price), 0) AS total_revenue,
    ROUND(AVG(i.price), 2) AS avg_unit_price,
    ROUND(COUNT(i.order_item_id) * 1.0 /
          NULLIF(DATEDIFF('week', MIN(oc.purchase_ts), MAX(oc.purchase_ts)), 0), 1) AS units_per_week,
    ROUND(AVG(p.product_weight_g) / 1000.0, 2) AS avg_weight_kg,
    ROUND(AVG((p.product_length_cm * p.product_height_cm * p.product_width_cm) / 1000000.0), 3)
          AS avg_volume_m3
FROM orders_clean oc
JOIN items i
    ON oc.order_id = i.order_id
JOIN products p
    ON i.product_id = p.product_id
LEFT JOIN translations t
    ON p.product_category_name = t.product_category_name
GROUP BY 1
ORDER BY units_per_week DESC;
