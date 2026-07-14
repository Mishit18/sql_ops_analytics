# SQL Operations Analytics: Olist Supply Chain

An end-to-end SQL-first operations analytics project on the Olist Brazilian E-Commerce dataset. The project builds a DuckDB analytics layer, computes supply-chain and customer operations KPIs, creates a visual dashboard, and translates the results into quantified operational recommendations.

## Highlights

- Built a DuckDB pipeline across 8 Olist source tables and 96,470 delivered orders.
- Computed 8 production-style KPI views covering OTDR, lead time, SLA breach, seller performance, cohort retention, GMV trend, product velocity, and freight efficiency.
- Generated 10 publication-ready dashboard plots in `outputs/`.
- Identified bottom-decile sellers driving 17.0% of seller-scorecard SLA breaches while representing 8.4% of scored seller order volume.
- Measured cohort retention: month-1 0.47%, month-3 0.25%, month-6 0.26%.

## Repository Structure

```text
sql_ops_analytics/
├── build_project.py
├── sql_ops_analytics.ipynb
├── queries/
│   ├── 00_setup_and_clean.sql
│   ├── 01_kpi_otdr_monthly.sql
│   ├── 02_kpi_lead_time_category.sql
│   ├── 03_kpi_seller_scorecard.sql
│   ├── 04_kpi_sla_breach_geo.sql
│   ├── 05_kpi_cohort_retention.sql
│   ├── 06_kpi_volume_trend.sql
│   ├── 07_kpi_product_velocity.sql
│   └── 08_kpi_freight_efficiency.sql
├── outputs/
│   ├── kpi_summary.csv
│   ├── plot_01_otdr_trend.png
│   └── plot_*.png
├── summary.md
├── requirements.txt
└── README.md
```

## KPIs

1. On-time delivery rate by month
2. Lead time by product category
3. Seller performance scorecard
4. SLA breach rate by state and month
5. Customer cohort retention
6. Order volume and GMV trend
7. Product velocity and inventory proxy
8. Delivery cost efficiency

## Key Findings

### Seller Reliability

Bottom-decile sellers account for 17.0% of seller-scorecard SLA breaches while representing only 8.4% of scored seller order volume. A vendor tiering policy using delivery reliability and review quality would focus remediation on the sellers with the largest operational impact.

### Geographic SLA Risk

AL has the highest state breach rate at 23.9% across 397 delivered orders. Long-haul state/category lanes need either improved regional carrier coverage or more realistic SLA promises.

### Customer Retention

Average retention drops sharply after first purchase: month-1 0.47%, month-3 0.25%, and month-6 0.26%. Post-delivery re-engagement and second-purchase freight incentives would target the largest repeat-order gap.

## Reproducibility

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python build_project.py
```

The script downloads the Olist dataset through KaggleHub, creates the DuckDB database locally, executes all SQL views, exports KPI tables, regenerates plots, and rewrites `summary.md`.

## Notes

- Raw Kaggle CSVs and the local DuckDB database are intentionally excluded from Git to keep the repository lightweight.
- All SQL KPI scripts are standalone and can be executed from the `queries/` directory after `00_setup_and_clean.sql` has created the base tables and cleaned view.
