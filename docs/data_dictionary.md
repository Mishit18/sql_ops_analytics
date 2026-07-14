# Data Dictionary

## Core Tables

| Table | Description | Key fields |
|---|---|---|
| `orders` | Raw order lifecycle table | `order_id`, `customer_id`, status and timestamp fields |
| `items` | Order-item detail with seller, product, price, and freight | `order_id`, `order_item_id`, `product_id`, `seller_id`, `price`, `freight_value` |
| `products` | Product category and package dimensions | `product_id`, `product_category_name`, weight and size fields |
| `translations` | Portuguese to English category mapping | `product_category_name`, `product_category_name_english` |
| `sellers` | Seller geography | `seller_id`, `seller_city`, `seller_state` |
| `customers` | Customer geography and unique customer identity | `customer_id`, `customer_unique_id`, `customer_city`, `customer_state` |
| `reviews` | Order-level review scores | `order_id`, `review_score` |
| `geo` | Brazilian geolocation reference data | zip prefix, latitude, longitude, city, state |

## Analytical View: `orders_clean`

| Field | Definition |
|---|---|
| `order_id` | Unique order identifier |
| `customer_unique_id` | Stable customer identity used for cohort retention |
| `customer_state` | Destination state |
| `purchase_ts` | Purchase timestamp |
| `delivered_ts` | Delivered-to-customer timestamp |
| `estimated_ts` | Estimated delivery date |
| `actual_lead_time_days` | Days from purchase to customer delivery |
| `promised_lead_time_days` | Days from purchase to estimated delivery |
| `days_early_late` | Estimated delivery date minus actual delivery date |
| `delay_days` | Days late, floored at zero |
| `is_late` | 1 when delivered after estimated delivery date |
| `purchase_month` | Month bucket for trend and cohort analysis |
| `purchase_week` | Week bucket for volume and GMV analysis |

## Output Tables

| Output | Purpose |
|---|---|
| `outputs/kpi_summary.csv` | Single-file metric summary for quick review |
| `outputs/otdr.csv` | Monthly OTDR trend |
| `outputs/lead_category.csv` | Category lead-time distribution metrics |
| `outputs/seller.csv` | Seller scorecard |
| `outputs/sla_state.csv` | State-level SLA breach metrics |
| `outputs/cohort.csv` | Cohort retention table |
| `outputs/volume.csv` | Weekly orders and GMV |
| `outputs/velocity.csv` | Product velocity and inventory proxy |
| `outputs/freight.csv` | Freight efficiency by seller/customer/category lane |
| `outputs/corridors.csv` | Route-level freight and lateness summary |
