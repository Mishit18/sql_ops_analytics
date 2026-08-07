# ATS Screening Pack

## Best-Fit Roles

This project is strongest for:

- Data Analyst
- Data Scientist
- Product Analyst
- Operations Analyst
- Business Analyst
- Marketplace Operations
- Supply Chain Analytics
- Strategy and Operations

It is not a causal-inference project yet. Use it as SQL-first operations analytics, KPI design, dashboarding, and business recommendation evidence.

## Recruiter Summary

Built a SQL-first DuckDB analytics warehouse on the Olist Brazilian E-Commerce dataset, analyzing 96,470 delivered orders across 8 raw operational tables. The project computes marketplace operations KPIs including on-time delivery rate, lead time, seller reliability, SLA breach geography, cohort retention, GMV/order trends, product velocity, and freight efficiency. Outputs include validated SQL views, CSV KPI tables, 10 charts, a Streamlit dashboard, an executive brief, and automated tests.

## ATS Keyword Coverage

| Area | Keywords |
|---|---|
| SQL | SQL, DuckDB, joins, CTEs, aggregations, KPI views, analytical warehouse |
| Analytics | product analytics, operations analytics, cohort analysis, retention, funnel-style repeat-order analysis |
| Business Metrics | OTDR, SLA breach, lead time, seller scorecard, GMV, AOV, product velocity, freight efficiency |
| Data Quality | schema validation, row reconciliation, delivered-order cleaning, metric grain control |
| Visualization | Streamlit, dashboard, KPI cards, matplotlib, seaborn, executive reporting |
| Strategy/Ops | seller tiering, lane-level SLA redesign, carrier coverage, retention intervention, freight corridor management |

## Resume Bullets - Data Analyst / Data Scientist

- Built a SQL-first DuckDB analytics warehouse across 8 Olist operational tables, analyzing 96,470 delivered orders and generating KPI views for OTDR, lead time, seller reliability, cohort retention, product velocity, and freight efficiency.
- Designed marketplace operations dashboard with seller scorecards, SLA geography, cohort retention, freight corridor diagnostics, and product velocity views; validated outputs with schema checks and metric consistency tests.
- Identified operational reliability gaps: overall OTDR 91.89%, worst operational month 78.64%, bottom-decile sellers contributing 17.0% of SLA breaches, and SP -> MA as the highest-risk freight corridor.

## Resume Bullets - Strategy / Ops / Product Analytics

- Diagnosed marketplace delivery reliability across 96,470 delivered orders; recommended seller tiering, lane-level SLA redesign, and targeted second-purchase incentives based on OTDR, seller breach concentration, and cohort retention.
- Quantified operational intervention opportunities: 25% reduction in bottom-decile seller lateness would prevent about 333 late deliveries, while lifting month-3 retention by 0.5 percentage points would create an estimated 481 repeat orders.
- Built executive-ready operations control room in Streamlit, converting SQL KPI outputs into reviewable recommendations across sellers, states, cohorts, product categories, and freight corridors.

## Interview Defense

### Why DuckDB instead of only pandas?

DuckDB keeps the project SQL-first and closer to analytical warehouse workflows. It also forces explicit table grains, joins, and reproducible KPI views rather than hiding metric logic inside notebook transformations.

### How did you avoid double-counting?

Order-level KPIs use delivered orders as the grain. Seller, category, and item-level outputs are separated into their own views because order items can duplicate order IDs. The methodology document states the grain for each KPI.

### Is this causal inference?

No. The project identifies operational associations and prioritization opportunities. It does not claim that faster delivery causes repeat purchase. A future extension could estimate causal impact with matching or difference-in-differences if a defensible treatment definition is created.

### What is the main business recommendation?

Start with seller reliability and lane-level SLA action. Bottom-decile sellers account for a disproportionate breach share, and specific long-haul corridors have elevated lateness and freight cost. These are more actionable than broad national delivery rules.

## Claims To Avoid

- Do not say an A/B test was run.
- Do not say delivery speed causally increases retention.
- Do not say the project uses real company internal data.
- Do not say recommendations are proven savings; they are quantified opportunities from public data.
- Do not claim a production deployment unless the dashboard is actually deployed.

## Next Optional Extension

If this project needs to become even stronger for product data science roles, add an experiment-design appendix:

- Define treatment: improved promised delivery window or second-purchase freight incentive.
- Define unit: customer or order.
- Define primary metric: repeat purchase within 90 days.
- Define guardrails: margin, cancellation rate, late delivery, review score.
- Estimate sample size using current retention baseline.

Keep the extension labeled as experiment design unless it is actually run.
