CREATE OR REPLACE VIEW kpi_sla_breach_geo AS
SELECT
    customer_state,
    purchase_month,
    COUNT(*) AS total_orders,
    SUM(is_late) AS late_orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS breach_rate_pct,
    ROUND(AVG(CASE WHEN is_late = 1 THEN delay_days END), 1) AS avg_delay_days,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_lead_time
FROM orders_clean
GROUP BY 1, 2
ORDER BY 1, 2;

CREATE OR REPLACE VIEW kpi_sla_breach_state AS
SELECT
    customer_state,
    COUNT(*) AS total_orders,
    SUM(is_late) AS late_orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS breach_rate_pct,
    ROUND(AVG(actual_lead_time_days), 1) AS avg_lead_time,
    ROUND(AVG(CASE WHEN is_late = 1 THEN delay_days END), 1) AS avg_delay_when_late
FROM orders_clean
GROUP BY 1
ORDER BY breach_rate_pct DESC;
