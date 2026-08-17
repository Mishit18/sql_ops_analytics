# SQL Operations Analytics Business Casebook

## 30-Second Pitch

This project turns raw e-commerce order, seller, freight, cohort, and delivery data into an operations control tower. It uses DuckDB SQL queries, KPI tables, visual dashboards, and validation checks to identify SLA deterioration, seller risk, product velocity, freight inefficiency, and cohort retention issues.

## Executive Findings

| Metric | Value |
|---|---:|
| Total delivered orders | 96,470 |
| Total GMV | 15,418,394.83 |
| Overall on-time delivery rate | 91.89% |
| Worst monthly OTDR | 78.64% |
| OTDR trend | Deteriorating |
| Bottom seller count | 63 |
| Bottom seller breach share | 17.00% |
| Bottom seller order share | 8.40% |
| Month-3 retention | 0.25% |
| Average order value | 159.83 |

## Decisions Supported

1. SLA intervention: investigate the worst OTDR month and categories with highest P90 lead time before adding more demand.
2. Seller operations: prioritize the bottom 63 sellers because they create 17.00% of SLA breaches while representing only 8.40% of orders.
3. Retention: treat cohort retention as a lifecycle problem, not only a delivery problem; month-3 retention is weak and needs repeat-purchase interventions.
4. Freight efficiency: compare freight cost, distance, lead time, and seller score before changing logistics partners.
5. Dashboarding: use OTDR trend, seller score, SLA state view, product velocity, and cohort heatmap as weekly operating views.

## Interview Questions Covered

- How would you define OTDR and SLA breach in SQL?
- Which sellers should operations teams call first?
- How do you separate volume issues from service-quality issues?
- Which product categories have delivery-risk problems?
- How would you build a weekly business review dashboard?
- What checks make the SQL pipeline reproducible?

## ATS Keywords

SQL, DuckDB, CTEs, window functions, joins, KPI dashboard, SLA breach, OTDR, seller scorecard, cohort retention, product velocity, freight efficiency, lead-time analytics, operations analytics, e-commerce analytics, data validation, executive reporting.
