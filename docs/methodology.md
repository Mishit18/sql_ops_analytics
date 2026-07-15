# Methodology

## Dataset Scope

The analysis uses the Olist Brazilian E-Commerce dataset and loads 8 CSV files into DuckDB:

- orders
- order items
- products
- product category translations
- sellers
- customers
- order reviews
- geolocation

The cleaned analytical base table keeps delivered orders with non-null purchase and delivery timestamps. This produces 96,470 delivered orders and retains 97.01% of the raw order table.

## Data Quality Gates

The pipeline checks:

- null `order_id` values in the raw order table
- date coverage of purchase timestamps
- order status distribution
- order item rows without matching order records
- review score distribution
- retained row count in `orders_clean`

The project requires at least 90,000 rows in `orders_clean`.

## Metric Grain

Operational metrics are computed at the correct analytical grain:

- OTDR and SLA breach metrics use one row per delivered order.
- Category lead-time metrics deduplicate order-category combinations to avoid over-counting multi-item orders.
- Seller scorecard metrics aggregate at seller-order grain before seller-level scoring.
- Freight efficiency is shipment/category-route grain because freight is stored on order-item rows.
- Cohort retention uses `customer_unique_id`, not `customer_id`, to track repeat behavior across purchases.

## KPI Definitions

| KPI | Definition |
|---|---|
| OTDR | Delivered orders on or before estimated delivery date divided by delivered orders |
| SLA breach rate | Delivered orders after estimated delivery date divided by delivered orders |
| Actual lead time | Days from purchase timestamp to delivered customer timestamp |
| Delay days | Days delivered after estimated delivery date, floored at zero |
| Seller composite score | 50% delivery reliability plus 50% review score normalized to 100 |
| Cohort retention | Customers active in month N divided by cohort customers |
| Product velocity | Units sold per week over observed selling window |
| Freight efficiency | Freight cost and freight-to-item-value ratio by seller-state/customer-state/category lane |

## Reporting Choices

The raw monthly OTDR table includes all months. For narrative trend reporting, operational months are filtered to months with at least 100 delivered orders so one-off early dataset rows do not dominate the business interpretation.

State-level lead time and SLA breach correlation is reported as directional rather than conclusive because the Pearson p-value is above conventional statistical significance thresholds. The recommendation therefore focuses on lane-level testing.

## Reproducibility

Run:

```bash
python build_project.py
```

The pipeline rebuilds the SQL layer, recalculates metrics, exports CSVs, regenerates plots, updates `summary.md`, and refreshes the notebook.

Validate committed outputs:

```bash
python scripts/validate_project.py
pytest
```

Explore the dashboard:

```bash
streamlit run dashboard/app.py
```
