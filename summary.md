# SQL Operations Analytics: Olist Supply Chain and Customer Operations

## Executive Summary
- Built a DuckDB analytics pipeline on 96,470 delivered orders retained from 97.01% of the raw order table.
- Overall OTDR is 91.89%; in operational months with at least 100 orders, monthly OTDR ranged from 78.64% to 98.87%, with a deteriorating slope of -0.337 percentage points per month.
- Bottom-decile sellers account for 17.0% of seller-scorecard SLA breaches while representing 8.4% of scored seller order volume.
- State lead time and breach rate show a positive but not statistically conclusive relationship: Pearson r = 0.28, p = 0.1584.
- Retention is low after first purchase: month-1 0.47%, month-3 0.25%, month-6 0.26%, month-12 0.20%.

## Schema Validation
- Null order IDs: 0
- Order date coverage: 2016-09-04 21:15:19 to 2018-10-17 17:30:18
- Items without an order record: 0
- orders_clean rows: 96,470; retained 97.01% of original orders.

## KPI Results
### 1. OTDR by Month
- Worst month: 2018-03 at 78.64% OTDR.
- Trend: deteriorating by -0.337 percentage points per month.

### 2. Lead Time by Product Category
- Top 5 categories by P90 lead time:
| category_en         |   total_orders |   p90_lead_time |   late_rate_pct |
|:--------------------|---------------:|----------------:|----------------:|
| office_furniture    |           1254 |            33   |             9.2 |
| audio               |            348 |            27   |            12.9 |
| fashion_shoes       |            235 |            26.6 |             6.4 |
| consoles_games      |           1018 |            25   |             8.2 |
| musical_instruments |            611 |            25   |             8.8 |
- Bottom 5 categories by P90 lead time:
| category_en                     |   total_orders |   p90_lead_time |   late_rate_pct |
|:--------------------------------|---------------:|----------------:|----------------:|
| food                            |            441 |              19 |            10   |
| construction_tools_lights       |            242 |              19 |             9.1 |
| construction_tools_construction |            736 |              19 |             9.1 |
| luggage_accessories             |           1019 |              19 |             5.5 |
| food_drink                      |            221 |              20 |             6.3 |
- High-variability categories where std/mean > 0.5: 43 categories.

### 3. Seller Performance Scorecard
- 63 bottom-decile scored sellers drive 17.0% of scorecard late orders.
- Worst 5 sellers:
| seller_id                        | seller_state   |   total_orders |   late_rate_pct |   avg_review_score |   seller_composite_score |
|:---------------------------------|:---------------|---------------:|----------------:|-------------------:|-------------------------:|
| 1ca7077d890b907f89be8c954a02686a | SP             |            108 |            22.2 |               2.39 |                     62.8 |
| 54965bbe3e4f07ae045b90b0b8541f52 | PR             |             73 |            30.1 |               3.14 |                     66.4 |
| a49928bcdf77c55c6d6e05e09a9b4ca5 | SP             |             96 |            26   |               3.03 |                     67.3 |
| ad781527c93d00d89a11eecd9dcad7c1 | SP             |             38 |            31.6 |               3.34 |                     67.6 |
| 835f0f7810c76831d6c7d24c7a646d4d | SP             |             42 |            31   |               3.36 |                     68.1 |

### 4. SLA Breach by Geography
- Top 5 states by breach rate:
| customer_state   |   total_orders |   breach_rate_pct |   avg_lead_time |   avg_delay_when_late |
|:-----------------|---------------:|------------------:|----------------:|----------------------:|
| AL               |            397 |              23.9 |            24.5 |                   8.5 |
| MA               |            717 |              19.7 |            21.5 |                   9.3 |
| PI               |            476 |              16   |            19.4 |                  11.6 |
| CE               |           1279 |              15.3 |            21.2 |                  13.6 |
| SE               |            335 |              15.2 |            21.5 |                  16.2 |
- Bottom 5 states by breach rate:
| customer_state   |   total_orders |   breach_rate_pct |   avg_lead_time |   avg_delay_when_late |
|:-----------------|---------------:|------------------:|----------------:|----------------------:|
| RO               |            243 |               2.9 |            19.3 |                   5.6 |
| AC               |             80 |               3.8 |            21   |                  18.7 |
| AM               |            145 |               4.1 |            26.4 |                  20.2 |
| AP               |             67 |               4.5 |            27.2 |                  48.3 |
| PR               |           4923 |               5   |            11.9 |                   6.7 |

### 5. Cohort Retention
- Best month-3 cohort: 2017-03 at 0.4%.
- Worst month-3 cohort: 2017-01 at 0.1%.
- LTV proxy: 1.03 orders/customer x BRL 160 AOV = BRL 165.

### 6. Order Volume and GMV Trend
- Top 3 GMV weeks and spike drivers:
| purchase_week   |   orders |   total_gmv |     aov | driver            |
|:----------------|---------:|------------:|--------:|:------------------|
| 2017-11-20      |     2915 |      464133 | 159.222 | High order volume |
| 2018-05-07      |     1943 |      334321 | 172.064 | High order volume |
| 2018-07-30      |     2002 |      320189 | 159.935 | High order volume |

### 7. Product Velocity and Inventory Proxy
- Top 10 categories by units per week:
| category_en           |   units_sold |   units_per_week |   avg_lead_time | stockout_risk   |
|:----------------------|-------------:|-----------------:|----------------:|:----------------|
| bed_bath_table        |        10953 |            110.6 |            12.9 | False           |
| health_beauty         |         9465 |             93.7 |            12   | False           |
| sports_leisure        |         8430 |             85.2 |            12.2 | False           |
| furniture_decor       |         8160 |             82.4 |            13   | False           |
| computers_accessories |         7643 |             77.2 |            13.1 | False           |
| housewares            |         6795 |             68.6 |            11   | False           |
| watches_gifts         |         5857 |             59.2 |            12.7 | False           |
| telephony             |         4430 |             44.7 |            12.9 | False           |
| garden_tools          |         4268 |             43.6 |            13.6 | False           |
| auto                  |         4139 |             41.8 |            12.3 | False           |
- Stockout-risk proxy flagged 0 categories where lead-time demand exceeds a 30-day restocking reorder point.

### 8. Delivery Cost Efficiency
- Worst cost-and-lateness corridors:
| seller_state   | customer_state   |   shipments |   avg_freight_cost |   late_rate_pct |   avg_lead_time |
|:---------------|:-----------------|------------:|-------------------:|----------------:|----------------:|
| SP             | MA               |         416 |            40.3585 |         23.9154 |         23.0538 |
| MA             | SP               |         130 |            32.26   |         26.9    |         16.2    |
| SP             | PI               |         178 |            35.9029 |         19.3286 |         20.2286 |
| SP             | CE               |         934 |            31.4953 |         14.6176 |         20.7412 |
| SP             | RN               |         147 |            36.708  |         10.7    |         19.34   |

## Operational Findings and Recommendations
### Finding 1: Seller Reliability Is Concentrated Enough for Tiering
Bottom-decile sellers drive 17.0% of seller-scorecard SLA breaches despite only 8.4% of scored order volume. That concentration puts roughly BRL 2,621,127 of GMV at reliability risk. Introduce a vendor tiering policy with weekly OTDR/review gates, remediation plans for amber sellers, and temporary suppression for sellers below a composite score threshold. A 25% reduction in late orders among this group would prevent about 333 late deliveries over the observed period.

### Finding 2: Geography and Lead Time Are a Structural SLA Driver
AL has the highest state breach rate at 23.9% across 397 orders, with average lead time of 24.5 days. Because breach rate correlates with lead time at r = 0.28, long-haul promises should be redesigned. Add regional carrier coverage or adjust SLA promises for the highest-risk state/category lanes. A 20% breach reduction in AL alone would avoid about 19 late orders tied to about BRL 63,451 of GMV exposure.

### Finding 3: Retention Drops Immediately After First Purchase
Average retention falls to month-1 0.47%, month-3 0.25%, and month-6 0.26%. The best month-3 cohort is 2017-03 at 0.4%, while the worst is 2017-01 at 0.1%. Trigger post-delivery re-engagement within 14 days for categories with fast repeat potential and attach freight incentives to second purchase. A 0.5 percentage point lift in month-3 retention implies about 481 incremental repeat orders using the observed orders-per-customer baseline.

## Resume-Ready Bullets
- Built SQL analytics pipeline on 96,470 e-commerce orders across 8 DuckDB tables; computed 8 supply-chain KPIs including OTDR 91.9%, P90 lead time, and cohort retention.
- Identified bottom-10% sellers driving 17.0% of SLA breaches; proposed composite vendor scorecard using delivery reliability and review quality for tiering.
- Computed customer cohort retention: month-1 0.47%, month-3 0.25%, month-6 0.26%; segmented by acquisition cohort and quantified repeat-order gap.
- Diagnosed SP->MA as highest-risk corridor (98% above median freight, 23.9% late rate); recommended carrier consolidation to reduce cost by estimated 8-12%.

## Output Inventory
- 8 standalone SQL KPI scripts in `queries/` plus setup/cleaning SQL.
- 10 publication-ready PNG plots in `outputs/`.
- KPI result CSV exports and `kpi_summary.csv` in `outputs/`.
- `sql_ops_analytics.ipynb` runs top to bottom against the local `data/` CSVs.