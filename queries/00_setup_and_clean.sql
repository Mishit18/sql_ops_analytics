CREATE OR REPLACE TABLE orders AS
SELECT * FROM read_csv_auto('../data/olist_orders_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE items AS
SELECT * FROM read_csv_auto('../data/olist_order_items_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE products AS
SELECT * FROM read_csv_auto('../data/olist_products_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE translations AS
SELECT * FROM read_csv_auto('../data/olist_product_category_name_translation.csv', ignore_errors=true);

CREATE OR REPLACE TABLE sellers AS
SELECT * FROM read_csv_auto('../data/olist_sellers_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE customers AS
SELECT * FROM read_csv_auto('../data/olist_customers_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE reviews AS
SELECT * FROM read_csv_auto('../data/olist_order_reviews_dataset.csv', ignore_errors=true);

CREATE OR REPLACE TABLE geo AS
SELECT * FROM read_csv_auto('../data/olist_geolocation_dataset.csv', ignore_errors=true);

CREATE OR REPLACE VIEW orders_clean AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_state,
    c.customer_city,
    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
    CAST(o.order_approved_at AS TIMESTAMP) AS approved_ts,
    CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS carrier_ts,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_ts,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_ts,
    DATEDIFF('day', CAST(o.order_purchase_timestamp AS TIMESTAMP),
             CAST(o.order_delivered_customer_date AS TIMESTAMP)) AS actual_lead_time_days,
    DATEDIFF('day', CAST(o.order_purchase_timestamp AS TIMESTAMP),
             CAST(o.order_estimated_delivery_date AS TIMESTAMP)) AS promised_lead_time_days,
    DATEDIFF('day', CAST(o.order_delivered_customer_date AS TIMESTAMP),
             CAST(o.order_estimated_delivery_date AS TIMESTAMP)) AS days_early_late,
    GREATEST(
        DATEDIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP),
                 CAST(o.order_delivered_customer_date AS TIMESTAMP)),
        0
    ) AS delay_days,
    CASE
        WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP) >
             CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN 1 ELSE 0
    END AS is_late,
    CASE WHEN o.order_delivered_customer_date IS NULL THEN 1 ELSE 0 END AS is_undelivered,
    DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS purchase_month,
    DATE_TRUNC('week', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS purchase_week,
    EXTRACT('year' FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS purchase_year,
    EXTRACT('month' FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS purchase_month_num,
    EXTRACT('dow' FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS day_of_week
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp IS NOT NULL;
