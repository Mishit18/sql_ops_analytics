CREATE OR REPLACE VIEW kpi_seller_scorecard AS
WITH review_per_order AS (
    SELECT order_id, AVG(review_score) AS review_score
    FROM reviews
    GROUP BY 1
),
seller_order AS (
    SELECT
        s.seller_id,
        s.seller_state,
        s.seller_city,
        oc.order_id,
        oc.actual_lead_time_days,
        oc.is_late,
        SUM(i.price) AS order_gmv,
        AVG(r.review_score) AS review_score
    FROM orders_clean oc
    JOIN items i
        ON oc.order_id = i.order_id
    JOIN sellers s
        ON i.seller_id = s.seller_id
    LEFT JOIN review_per_order r
        ON oc.order_id = r.order_id
    GROUP BY 1, 2, 3, 4, 5, 6
)
SELECT
    seller_id,
    seller_state,
    seller_city,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_gmv), 0) AS total_gmv,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_lead_time,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS late_rate_pct,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) AS bad_reviews,
    ROUND(100.0 * SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS bad_review_rate_pct,
    ROUND(
        (100 - 100.0 * SUM(is_late) / COUNT(*)) * 0.5 +
        (COALESCE(AVG(review_score), 0) / 5.0 * 100) * 0.5,
    1) AS seller_composite_score
FROM seller_order
GROUP BY 1, 2, 3
HAVING COUNT(*) >= 30
ORDER BY seller_composite_score ASC;
