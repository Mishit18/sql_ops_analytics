CREATE OR REPLACE VIEW kpi_otdr_monthly AS
SELECT
    purchase_month,
    COUNT(*) AS total_orders,
    SUM(is_late) AS late_orders,
    COUNT(*) - SUM(is_late) AS on_time_orders,
    ROUND(100.0 * (COUNT(*) - SUM(is_late)) / COUNT(*), 2) AS otdr_pct,
    ROUND(AVG(CASE WHEN is_late = 1 THEN delay_days END), 1) AS avg_delay_when_late_days,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY actual_lead_time_days), 1) AS p95_lead_time
FROM orders_clean
GROUP BY 1
ORDER BY 1;
